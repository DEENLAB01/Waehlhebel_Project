# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : simplified_bus_tests.py
# Task    : Example implementation of "simplified" bus test functions
#           (adapted test functions to suit specific project needs)
#
# Author  : J. Tremmel
# Date    : 24.08.2015
# Copyright 2015 - 2016 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 11.05.2021 | A. Neumann | handoverd from J. Tremmel
# 1.1  | 30.06.2021 | Mohammed   |  Added TestcaseId Number
# ******************************************************************************
from ttk_bus import bus_tests  # @UnresolvedImport
import re
from result_list import ResultList  # @UnresolvedImport (in test_support libs)
from ttk_base._variables_base import DummyVar  # @UnresolvedImport (only in base lib in TTk 1.x)
import time
from ttk_checks import basic_tests  # @UnresolvedImport
from ttk_base.values_base import meta  # @UnresolvedImport

var_access_failures = {}

# just for convenience: collect info on vars involved in FAILED bus tests
failed_cal_vars = {}
failed_bus_vars = {}


# #############################################################################
def checkVarAccess(var):
    """ Utility function: Check access to the supplied variable.

        Parameters:
            var - variable (HilVar, CalVar, ...) to check

        Returns True if access was successful, otherwise False
    """
    global var_access_failures
    try:
        if not hasattr(var, "get"):
            return None  # not an expected variable

        test_data = var.get()
        if isinstance(test_data, (int, long, float)):
            # return value has to be numeric for all variables used in
            # simplified_bus_tests
            return True

        alias = getattr(var, "alias", var)
        var_access_failures[var] = "%s: %s" % (alias, test_data)

    except Exception, ex:
        print "> checkVarAccess: %s: %s" % (type(ex).__name__, ex)
        var_access_failures[var] = "%s: %s" % (getattr(var, "alias", var), ex)

    return False


# #############################################################################
def isDummy(var):
    """ Utility function: Return True if "var" is just a dummy implementation,
        either directly a DummyVar or marked with an "is_dummy" attribute.
    """
    return isinstance(var, DummyVar) or getattr(var, "is_dummy", False)


# #############################################################################
def getMaxValidPeriod(cycletime_ms):
    """
        return the max valid allow period, where no failure shall occur

        Eissmann Anforderung CAN_3244:
        cycletime <= 50ms: min = 450ms / soll = 500ms / max = 5s
        cycletime > 50ms: min = 9*cycletime / soll = 10*cycletime / max = 5s
    """

    if cycletime_ms <= 50:
        min_valid = 450
    else:
        min_valid = 8 * cycletime_ms
        if min_valid >= 5000:
            min_valid = min_valid - cycletime_ms

    return min_valid


# #############################################################################
def _getNotTestedResult(descr, reason, var1, var2, var1_label="Var 1", var2_label="Var 2"):
    """ Get a result entry with verdict NOT TESTED and some additional
        information on the involved variables.

        Parameters:
            descr      - additional description
            reason     - info why this result is NOT TESTED
            var1       - first variable involved in not-actuall-tested-check
            var2       - second variable involved in not-actually-tested check
            var1_label - label text for var1
            var2_label - label text for var2

        Returns a testresult entry [<description>, "NOT TESTED"]
    """
    if not descr:
        descr = getattr(var1, "descr", "") or getattr(var1, "alias", "") or var1
    return [
        "%s\n\n"
        "Not Tested Reason: %s\n\n"
        "%s: %s\n"
        "%s: %s" % (
            descr,
            reason.strip(),
            var1_label, getattr(var1, "alias", var1),
            var2_label, getattr(var2, "alias", var2),
        ),
        "NOT TESTED"
    ]


# #############################################################################
def _addTestcaseID(result, testcase_id=None):
    """ Add supplied testcase-ID(s) to result.
        Parameters:
            result         - result entry containing at least
                             [<description>, <verdict>]
            testcase_id    - a single testcase ID or a list of multiple
                             testcase ids. If testcase_id is None, result will
                             remain unmodified.
        Returns: - (result is updated directly)
    """
    if not isinstance(testcase_id, (list, tuple)):
        testcase_id = [testcase_id]

    for tc_id in testcase_id:
        if tc_id is None: continue  # just in case: skip un-set testcase ids
        # insert testcase id before verdict
        result.insert(-1, "[[TCID]] %s" % (tc_id))


# #############################################################################
def _addComment(result, comment=""):
    """ Add supplied comment to result (as, well, comment).
        Parameters:
            result    - result entry containing at least
                             [<description>, <verdict>]
            comment   - comment text (or list of comment lines) to add
                        If comment is empty, result will remain unmodified.
        Returns: - (result is updated directly)
    """
    if isinstance(comment, (list, tuple)):
        comment = "\n".join(comment)

    comment = comment.strip()
    if comment:
        # insert comment before verdict
        result.insert(-1, "[[COMMENT]] %s" % (comment))


# #############################################################################
def testRxSigSeq(set_sig, check_var, set_values, check_values=None,
                 abs_tol=None, descr="", testcase_id=None, not_tested_reason=""):
    """ Run testRxSignal on a sequence of set/check values and provide
        a single resulting verdict for all sub-tests.
        Parameters:
            bus_signal        - bus signal to set
            check_var         - (cal) variable to check
            set_values        - list of values to set
            check_values      - list of values to check, defaults to set_values
            abs_tol           - absolute tolerance for float value checks;
                                None: interpret values as integer
            descr             - additional description to add to result entry
            testcase_id       - optional testcase id; will be set to result
                                if not None.
            not_tested_reason - if a reason string has been supplied, it will
                                be added to the result description and the
                                verdict will be forced to "NOT TESTED"

        Returns a single test result (typically [<description>, <verdict>] or
        [<description>, "[[TCID]] <testcase_id>", <verdict>])
    """
    bus_signal = set_sig
    if not set_values:
        set_values = []

    if not check_values:
        check_values = set_values[:]

    if not_tested_reason.strip():
        return _getNotTestedResult(
            descr, not_tested_reason,
            bus_signal, check_var,
            "HIL-Tx var", "CAL-Rx var"
        )

    var_accessible = checkVarAccess(check_var)
    if not var_accessible:
        # check var not accessible: no use to run complete test value sequence.
        # Limit test to a two values so we retain all other associated information
        # in the test result
        set_values = [set_values[0], set_values[-1]]
        check_values = [check_values[0], check_values[-1]]

    subresult = ResultList()
    if descr:
        subresult.append(["%s" % (descr), ""])

    # set last value first, so the first value may be sent "on change"
    # (assuming that set_values[-1] != set_values[0])
    bus_signal.set(set_values[-1])
    time.sleep(.100)
    for set_val, check_val in zip(set_values, check_values):
        tol = abs_tol
        if tol is None and isinstance(check_val, float):
            tol = 0.001  # fallback

        subresult.append(
            bus_tests.testRxSignal(
                bus_signal,
                set_value=set_val,
                check_var_list=[{'var': check_var, 'value': check_val, 'abs_pos': tol}],
            )
        )

    bus_signal.reset()

    result = subresult.getCombinedResult()
    resulting_verdict = result[-1]

    bus_var = getattr(bus_signal, "signal_var", bus_signal)
    signal_name = getattr(bus_var, "alias", bus_var)
    if signal_name.startswith("DUMMY_SIGNAL_"):
        failed_bus_vars[signal_name] = re.sub("^DUMMY_SIGNAL_", "", signal_name)
    if var_accessible and resulting_verdict != "PASSED":
        failed_cal_vars[signal_name] = check_var

    comments = []
    if isDummy(bus_signal):
        comments.append("Bus Signal n/a on HIL")
    if isDummy(check_var):
        comments.append("Cal Var n/a")

    # add comment to result (if we have one)
    _addComment(result, comments)

    # add testcase-id to result if one has been supplied
    _addTestcaseID(result, testcase_id)

    return result


# #############################################################################
def testTxSigSeq(check_sig, set_var, set_values, check_values=None,
                 abs_tol=None, descr="", testcase_id=None, not_tested_reason="",
                 additional_set_vars=None):
    """ Run testTxSignal on a sequence of set/check values and provide
        a single resulting verdict for all sub-tests.

        Parameters:
            bus_signal        - bus signal to check
            set_var           - (cal) variable to set
            set_values        - list of values to set
            check_values      - list of values to check, defaults to set_values
            abs_tol           - absolute tolerance for float value checks;
                                None: interpret values as integer
            descr             - additional description text to add to result entry
            testcase_id       - optional testcase id; will be set to result
                                if not None
            not_tested_reason - if a reason string has been supplied, it will
                                be added to the result description and the
                                verdict will be forced to "NOT TESTED"
            additional_set_vars - list of additional set var dicts with
                                  { 'var': ..., 'value': ... } which will be
                                  set after the default set var
                                  (this is only needed for special cases -JT)

        Returns a single test result (typically [<description>, <verdict>] or
        [<description>, "[[TCID]] <testcase_id>", <verdict>])
    """
    bus_signal = check_sig
    if not set_values:
        set_values = []

    if not check_values:
        check_values = set_values[:]

    if not additional_set_vars:
        additional_set_vars = []

    if not_tested_reason.strip():
        return _getNotTestedResult(
            descr or bus_signal.descr or bus_signal.alias,
            not_tested_reason,
            bus_signal, set_var,
            "HIL-Rx var", "CAL-Tx var"
        )

    subresult = ResultList()
    if descr:
        subresult.append(["%s" % (descr), ""])

    var_accessible = checkVarAccess(set_var)
    if not var_accessible:
        # set var not accessible: no use to run complete test value sequence.
        # Limit test to a single value so we retain all other associated
        # information in the test result
        set_values = [set_values[0], set_values[-1]]
        check_values = [check_values[0], check_values[-1]]

    for set_val, check_val in zip(set_values, check_values):
        tol = abs_tol
        if tol is None and isinstance(check_val, float):
            tol = 0.001  # fallback
        subresult.append(
            bus_tests.testTxSignal(
                set_var_list=[{'var': set_var, 'value': set_val}] + additional_set_vars,
                bus_signal_data=bus_signal,
                check_value=check_val,
                abs_pos=tol,
            )
        )

    set_var.reset()

    result = subresult.getCombinedResult()
    resulting_verdict = result[-1]

    bus_var = getattr(bus_signal, "signal_var", bus_signal)
    signal_name = getattr(bus_var, "alias", bus_var)
    if signal_name.startswith("DUMMY_SIGNAL_"):
        failed_bus_vars[signal_name] = re.sub("^DUMMY_SIGNAL_", "", signal_name)
    if var_accessible and resulting_verdict != "PASSED":
        failed_cal_vars[signal_name] = set_var

    comments = []
    if isDummy(bus_signal):
        comments.append("Bus Signal n/a on HIL")
    if isDummy(set_var):
        comments.append("Cal Var n/a")

    # add comment to result (if we have one)
    _addComment(result, comments)

    # add testcase-id to result if one has been supplied
    _addTestcaseID(result, testcase_id)

    return result


def checkInhibitTiming(time_stamp_variable, set_variable, set_values, cycle_time_value_ms, message_name,
                       inhibit_time_ms, tol_perc=0.1):
    """It is checked if the cycle time of a cyclic signal sent from the ECU is correct ("==" or "<=" value).
        Waits until the time-stamp changes and then checks the difference between the time-stamps for 10 times.

        Parameters:
            time_stamp_variable         -  time-stamp variable of a cyclic CAN bus vars signal in us
            set_variable                -  variable of signal, to send signal and trigger event
            set_values                  -  values to set (min. 2 values) in a list []
            cycle_time_value_ms         -  cycle time of the message in ms
            message_name                -  name of the message as string
            inihibit_time_ms            -  inhibit time of message in ms. If this time is not None it
                                           will be checked, that time is between inhibit time and cycletime
            tol_perc                    -  tolerance of cycletime in % (0-1)
            operator                    -  check if cycle time is "==" or "<=" given value (if inhibit time is None)

        Returns:
            a testresult entry. Passed if cycle time was correct
    """
    nr_loops = 10

    if len(set(set_values)) < 2:  # mind 2 unterschiedliche Werte
        raise ValueError("minimum 2 different values has to be handoverd")

    while len(set_values) < nr_loops:
        set_values += set_values

    cycle_time_value_s = cycle_time_value_ms / 1000.0
    time_stamp_1 = time_stamp_variable.get()
    time_stamp_2 = time_stamp_variable.get()

    subresult = ResultList()
    for _i in range(nr_loops):
        start_time = time.time()

        # trigger event by send signal
        set_variable.set(set_values[_i])

        while (time_stamp_1 == time_stamp_2):
            time_stamp_2 = time_stamp_variable.get()

            # timeout with 5* cycle time
            if (time.time() - start_time) > (5 * cycle_time_value_s):
                return ([
                    "Waiting for the time-stamp to change timed out after %s s!" % (
                            5 * cycle_time_value_s
                    ),
                    "FAILED"])
                break;

        # calc measured cycletime
        cycle_time_ms = (time_stamp_2 - time_stamp_1) / 1000.0

        subresult.append(
            basic_tests.checkRange(
                value=cycle_time_ms,
                min_value=inhibit_time_ms - inhibit_time_ms * tol_perc,
                max_value=cycle_time_value_ms + cycle_time_value_ms * tol_perc,
                descr="Check that the cycle time of the message %s is between %sms and  %s %s%%" % (
                    message_name, inhibit_time_ms, cycle_time_value_ms, u"\u00B1", tol_perc * 100)
            )
        )

        time_stamp_1 = time_stamp_2

    return subresult.getCombinedResult()


def checkTiming(time_stamp_variable, cycle_time_value_ms, message_name, tol_perc=0.1, operator="==", result="long"):
    """It is checked if the cycle time of a cyclic signal sent from the ECU is correct ("==" or "<=" value).
        Waits until the time-stamp changes and then checks the difference between the time-stamps for 10 times.

        Parameters:
            time_stamp_variable         -  time-stamp variable of a cyclic CAN bus vars signal in us
            cycle_time_value_ms         -  cycle time of the message in ms
            message_name                -  name of the message as string
            tol_perc                    -  tolerance of cycletime in % (0-1)
            operator                    -  check if cycle time is "==" or "<=" given value
            result                      - long/short: long, all steps in a subresult - short, only descr with verdict

        Returns:
            a testresult entry. Passed if cycle time was correct
    """

    cycle_time_value_s = cycle_time_value_ms / 1000.0
    time_stamp_1 = time_stamp_variable.get()
    time_stamp_2 = time_stamp_variable.get()

    subresult = ResultList() if result == "long" else ""
    if result == "long":
        subresult.enableEcho(False)  # no need to echo results twice
    verdict_all = "PASSED"
    cycle_time_all = []
    timeout = 5 * cycle_time_value_s

    for _i in range(10):
        start_time = time.time()

        while (time_stamp_1 == time_stamp_2):
            time_stamp_2 = time_stamp_variable.get()

            # timeout with 5* cycle time
            if (time.time() - start_time) > (timeout):
                return (["Warte auf Timestampänderung der Botschaft %s, Timeout nach %ss (5*Zykluszeit)!"
                         % (message_name, timeout), "FAILED"])
                break;

        # calc measured cycletime
        cycle_time_ms = (time_stamp_2 - time_stamp_1) / 1000.0
        cycle_time_all.append(cycle_time_ms)
        if operator == "==":
            descr, verdict = basic_tests.compare(
                left_value=cycle_time_ms,
                operator=operator,
                right_value=meta(cycle_time_value_ms, "ms"),
                abs_tol=cycle_time_value_ms * tol_perc,
                descr="Pruefe die Zykluszeit der Botschaft %s: %s %s ms %s %s%%"
                      % (message_name, operator, cycle_time_value_ms, u"\u00B1", (tol_perc * 100))
            )
            if result == 'long':
                subresult.append([descr, verdict])
            else:
                verdict_all = verdict if verdict == "FAILED" else verdict_all

        elif operator == "<=":
            cycletime_offset = cycle_time_value_ms + cycle_time_value_ms * tol_perc  # cycletime plus tolerance
            descr, verdict = basic_tests.compare(
                left_value=cycle_time_ms,
                operator=operator,
                right_value=meta(cycletime_offset, "ms"),
                descr="Pruefe die Zykluszeit der Botschaft %s: %s %sms %s %s%%" % (
                    message_name, operator, cycle_time_value_ms, u"\u00B1", tol_perc * 100)
            )
            if result == 'long':
                subresult.append([descr, verdict])
            else:
                verdict_all = verdict if verdict == "FAILED" else verdict_all

        time_stamp_1 = time_stamp_2

    if result == 'long':
        return subresult.getCombinedResult()
    else:
        descr = "Durchschnittliche Zykluszeit der Botschaft %s: %sms" % (
        message_name, sum(cycle_time_all) / len(cycle_time_all))
        return [descr, verdict_all]


def checkNoTiming(time_stamp_variable, cycle_time_value_ms, message_name):
    """It is checked that no signal will be send, no timestamp ("==" or "<=" value).
        Waits until the time-stamp changes and then checks the difference between the time-stamps for 10 times.

        Parameters:
            time_stamp_variable         -  time-stamp variable of a cyclic CAN bus vars signal in us
            cycle_time_value_ms         -  cycle time of the message in ms
            message_name                -  name of the message as string
        Returns:
            a testresult entry. Passed no message will be send
    """

    cycle_time_value_s = cycle_time_value_ms / 1000.0
    time_stamp_1 = time_stamp_variable.get()
    time_stamp_2 = time_stamp_variable.get()

    start_time = time.time()
    while (time_stamp_1 == time_stamp_2):
        time_stamp_2 = time_stamp_variable.get()

        # timeout with 5* cycle time
        if (time.time() - start_time) > (5 * cycle_time_value_s):
            return (["Warte auf Timestampänderung der Botschaft %s, Timeout nach %ss (5*Zykluszeit)!"
                     % (message_name, 5 * cycle_time_value_s), "PASSED"])
            break;

    # calc measured cycletime
    cycle_time_ms = (time_stamp_2 - time_stamp_1) / 1000.0

    return "Botschaft %s sendet weiterhin (%s)" % (message_name, cycle_time_ms), "FAILED"


def setTestcaseId(testresult, name):
    """ Set Testcase name for Teststep
        name: messagename__signalname
    """
    tc_mapping = {
        "DEV_Waehlhebel_Req_00__DEV_Waehlhebel_Req_00_Data": "CAN_27",
        "NM_Airbag__NM_Airbag_01_FCAB": "CAN_75",
        "Dimmung_01__DI_KL_58xd": "CAN_24",
        "Dimmung_01__DI_KL_58xt": "CAN_25",
        "Systeminfo_01__SI_P_Mode_gueltig": "CAN_130",
        "Systeminfo_01__SI_P_Mode": "CAN_131",
        "NVEM_12__NVEM_Abschaltstufe": "CAN_92",
        "KN_Waehlhebel__Waehlhebel_Abschaltstufe": "CAN_60",
        "KN_Waehlhebel__KN_Waehlhebel_BusKnockOut": "CAN_70",
        "KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer": "CAN_69",
        "KN_Waehlhebel__Waehlhebel_KD_Fehler": "CAN_68",
        "KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut": "CAN_64",
        "KN_Waehlhebel__NM_Waehlhebel_FCIB": "CAN_72",
        "KN_Waehlhebel__Waehlhebel_SNI_10": "CAN_63",
        "KN_Waehlhebel__NM_Waehlhebel_Subsystemaktiv": "CAN_67",
        "KN_Waehlhebel__Waehlhebel_Transport_Mode": "CAN_61",
        "KN_Waehlhebel__NM_Waehlhebel_Lokalaktiv": "CAN_66",
        "KN_Waehlhebel__Waehlhebel_KompSchutz": "CAN_59",
        "KN_Waehlhebel__Waehlhebel_Nachlauftyp": "CAN_62",
        "KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer": "CAN_71",
        "KN_Waehlhebel__KN_Waehlhebel_DiagPfad_V12": "CAN_65",
        "OBDC_Funktionaler_Req_All_FD__OBDC_Funktion_Req_All_FD_Data": "CAN_99",
        "NM_Waehlhebel__NM_Waehlhebel_FCAB": "CAN_81",
        "NM_Waehlhebel__NM_Waehlhebel_UDS_CC": "CAN_84",
        "NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen": "CAN_89",
        "NM_Waehlhebel__NM_Waehlhebel_NM_State": "CAN_83",
        "NM_Waehlhebel__NM_Waehlhebel_SNI_10": "CAN_82",
        "NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin": "CAN_88",
        "NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12": "CAN_85",
        "NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15": "CAN_86",
        "NM_Waehlhebel__NM_Waehlhebel_CBV_CRI": "CAN_80",
        "NM_Waehlhebel__NM_Waehlhebel_CBV_AWB": "CAN_79",
        "NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag": "CAN_87",
        "OTAMC_D_01__VehicleProtectedEnvironment_D": "CAN_123",
        "OTAMC_D_01__OTAMC_D_01_CRC": "CAN_121",
        "OTAMC_D_01__OTAMC_D_01_BZ": "CAN_122",
        "DS_Waehlhebel__DS_Waehlhebel_StMemChanged": "CAN_44",
        "DS_Waehlhebel__DS_Waehlhebel_Lokalaktiv": "CAN_48",
        "DS_Waehlhebel__DS_Waehlhebel_DiagAdr": "CAN_40",
        "DS_Waehlhebel__DS_Waehlhebel_IdentValid": "CAN_47",
        "DS_Waehlhebel__DS_Waehlhebel_MemSelChanged": "CAN_46",
        "DS_Waehlhebel__DS_Waehlhebel_MemSel10Changed": "CAN_45",
        "DS_Waehlhebel__DS_Waehlhebel_ConfDTCChanged": "CAN_42",
        "DS_Waehlhebel__DS_Waehlhebel_TestFailedChanged": "CAN_41",
        "DS_Waehlhebel__DS_Waehlhebel_WIRChanged": "CAN_43",
        "DS_Waehlhebel__DS_Waehlhebel_Subsystemaktiv": "CAN_49",
        "SiShift_01__SIShift_StLghtDrvPosn": "CAN_128",
        "SiShift_01__SiShift_01_CRC": "CAN_125",
        "SiShift_01__SiShift_01_BZ": "CAN_126",
        "SiShift_01__SIShift_FlgStrtNeutHldPha": "CAN_127",
        "NM_HCP1__NM_HCP1_FCAB": "CAN_77",
        "ISOx_Waehlhebel_Resp_FD__ISOx_Waehlhebel_Resp_FD_Data": "CAN_57",
        "ISOx_Waehlhebel_Req_FD__ISOx_Waehlhebel_Req_FD_Data": "CAN_55",
        "Diagnose_01__UH_Monat": "CAN_18",
        "Diagnose_01__UH_Tag": "CAN_19",
        "Diagnose_01__DW_Kilometerstand": "CAN_16",
        "Diagnose_01__UH_Stunde": "CAN_20",
        "Diagnose_01__UH_Minute": "CAN_21",
        "Diagnose_01__UH_Jahr": "CAN_17",
        "Diagnose_01__UH_Sekunde": "CAN_22",
        "ORU_01__ORU_Status": "CAN_109",
        "ClampControl_01__KST_KL_15": "CAN_14",
        "DIA_SAAM_Req__DIA_SAAM_Req_Data": "CAN_33",
        "OBD_03__OBD_Warm_Up_Cycle": "CAN_95",
        "OBD_03__OBD_Driving_Cycle": "CAN_94",
        "OBD_04__MM_PropulsionSystemActive": "CAN_97",
        "XCP_Waehlhebel_DTO_01__XCP_Waehlhebel_DTO_01_Data": "CAN_146",
        "OBDC_Waehlhebel_Resp_FD__OBDC_Waehlhebel_Resp_FD_Data": "CAN_107",
        "DPM_01__DPM_01_CRC": "CAN_35",
        "DPM_01__DPM_FlgStrtNeutHldPha": "CAN_38",
        "DPM_01__DPM_01_BZ": "CAN_36",
        "DPM_01__DPM_StLghtDrvPosn": "CAN_37",
        "ISOx_Funkt_Req_All_FD__ISOx_Funkt_Req_All_FD_Data": "CAN_53",
        "Waehlhebel_04__Waehlhebel_04_CRC": "CAN_135",
        "Waehlhebel_04__WH_Zustand_N_Haltephase_2": "CAN_141",
        "Waehlhebel_04__Waehlhebel_04_BZ": "CAN_136",
        "Waehlhebel_04__WH_SensorPos_roh": "CAN_137",
        "Waehlhebel_04__WH_Entsperrtaste_02": "CAN_138",
        "Waehlhebel_04__WH_Fahrstufe": "CAN_140",
        "Waehlhebel_04__WH_P_Taste": "CAN_139",
        "ORU_Control_A_01__OnlineRemoteUpdateControlOldA": "CAN_114",
        "ORU_Control_A_01__ORU_Control_A_01_BZ": "CAN_112",
        "ORU_Control_A_01__OnlineRemoteUpdateControlA": "CAN_113",
        "ORU_Control_A_01__ORU_Control_A_01_CRC": "CAN_111",
        "OBDC_Waehlhebel_Req_FD__OBDC_Waehlhebel_Req_FD_Data": "CAN_105",
        "DEV_Waehlhebel_Resp_FF__DEV_Waehlhebel_Resp_FF_Data": "CAN_29",
        "OBDC_SSN_SAAM_Req__OBDC_SSN_SAAM_Req_Data": "CAN_101",
        "DIA_SAAM_Resp__DIA_SAAM_Resp_Data": "CAN_31",
        "XCP_Waehlhebel_CRO_01__XCP_Waehlhebel_CRO_01_Data": "CAN_144",
        "VDSO_05__VDSO_Vx3d": "CAN_133",
        "ORU_Control_D_01__ORU_Control_D_01_BZ": "CAN_117",
        "ORU_Control_D_01__OnlineRemoteUpdateControlD": "CAN_118",
        "ORU_Control_D_01__ORU_Control_D_01_CRC": "CAN_116",
        "ORU_Control_D_01__OnlineRemoteUpdateControlOldD": "CAN_119",
        "OBDC_SSN_SAAM_Resp__OBDC_SSN_SAAM_Resp_Data": "CAN_101",
    }
    if name in tc_mapping.keys():
        tc_id = tc_mapping[name]
    else:
        tc_id = ""
    testresult.setTestcaseId(tc_id)


###############################################################################
###############################################################################

# #############################################################################
if __name__ == "__main__":
    from _automation_wrapper_ import TestEnv

    testenv = TestEnv()
    testenv.setup()
    hil = testenv.getHil()



