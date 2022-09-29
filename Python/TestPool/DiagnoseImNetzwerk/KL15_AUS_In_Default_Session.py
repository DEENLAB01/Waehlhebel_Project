# ******************************************************************************
# -*- coding: latin1 -*-
# File    : KL15_AUS_In_Default_Session.py
# Title   : KL15 AUS In Default Session
# Task    : A minimal "KL15_AUS_In_Default_Session!" test script
#
# Author  : Mohammed Abdul Karim
# Date    : 14.10.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 14.10.2021 | Mohammed  | initial
# 1.1  | 04.11.2021 | Devang    | Added evaluation method
# 1.2  | 17.12.2021 | Mohammed  | Rework according to Test specification
# 1.3  | 14.01.2022 | Mohammed  | Rework according to Test specification changed
# 1.4  | 17.03.2022 | Devangbhai  | Rework according to Test specification changed
# 1.5  | 17.03.2022 | Devangbhai  | Added the test step 8.1 and changed the test step 9. Added the Ticket ID
# 1.6  | 20.07.2022 | Mohammed     | Added Fehler Id test step 11

# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import time
from ttk_daq import eval_signal
from functions_nm import _checkStatus
from time import time as t


def check_cycletime(sec, application_msg=True, nm_msg=False):
    Waehlhebel_04__timestamp_list = []
    DS_Waehlhebel__timestamp_list = []
    KN_Waehlhebel__timestamp_list = []
    NM_Waehlhebel__timestamp_list = []

    timeout = sec + t()
    while timeout > t():
        timestamp_Waehlhebel_04 = hil.Waehlhebel_04__timestamp.get()
        timestamp_DS_Waehlhebel = hil.DS_Waehlhebel__timestamp.get()
        timestamp_KN_Waehlhebel = hil.KN_Waehlhebel__timestamp.get()
        timestamp_NM_Waehlhebel = hil.NM_Waehlhebel__timestamp.get()

        if len(Waehlhebel_04__timestamp_list) == 0 or Waehlhebel_04__timestamp_list[-1] != timestamp_Waehlhebel_04:
            Waehlhebel_04__timestamp_list.append(timestamp_Waehlhebel_04)
        elif len(DS_Waehlhebel__timestamp_list) == 0 or DS_Waehlhebel__timestamp_list[-1] != timestamp_DS_Waehlhebel:
            DS_Waehlhebel__timestamp_list.append(timestamp_DS_Waehlhebel)
        elif len(KN_Waehlhebel__timestamp_list) == 0 or KN_Waehlhebel__timestamp_list[-1] != timestamp_KN_Waehlhebel:
            KN_Waehlhebel__timestamp_list.append(timestamp_KN_Waehlhebel)
        elif len(NM_Waehlhebel__timestamp_list) == 0 or NM_Waehlhebel__timestamp_list[-1] != timestamp_NM_Waehlhebel:
            NM_Waehlhebel__timestamp_list.append(timestamp_NM_Waehlhebel)

    new_sec = sec * 1000
    Waehlhebel_04__timestamp = 10
    DS_Waehlhebel__timestamp = 1000
    KN_Waehlhebel__timestamp = 500
    NM_Waehlhebel_timestamp = 200

    testresult.append(basic_tests.checkRange((len(Waehlhebel_04__timestamp_list)) if application_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / Waehlhebel_04__timestamp) - 5) if application_msg else 0, ((new_sec / Waehlhebel_04__timestamp) + 5) if application_msg else 0, "Prüfen, ob die Applikation Botschaft Waehlhebel_04 mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (Waehlhebel_04__timestamp, sec) if application_msg else "Prüfen, ob die Waehlhebel_04 Botschaft nicht gesendet wird."))
    testresult.append(basic_tests.checkRange((len(DS_Waehlhebel__timestamp_list)) if application_msg else (len(DS_Waehlhebel__timestamp_list) - 1), ((new_sec / DS_Waehlhebel__timestamp) - 2) if application_msg else 0, ((new_sec / DS_Waehlhebel__timestamp) + 2) if application_msg else 0, "Prüfen, ob die Applikation Botschaft DS_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % ( DS_Waehlhebel__timestamp, sec)if application_msg else "Prüfen, ob die DS_Waehlhebel Botschaft nicht gesendet wird."))
    testresult.append(basic_tests.checkRange((len(KN_Waehlhebel__timestamp_list)) if application_msg else (len(KN_Waehlhebel__timestamp_list) - 1), ((new_sec / KN_Waehlhebel__timestamp) - 2) if application_msg else 0,((new_sec / KN_Waehlhebel__timestamp) + 2) if application_msg else 0, "Prüfen, ob die Applikation Botschaft KN_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % ( KN_Waehlhebel__timestamp, sec)if application_msg else "Prüfen, ob die KN_Waehlhebel Botschaft nicht gesendet wird."))
    testresult.append(basic_tests.checkRange((len(NM_Waehlhebel__timestamp_list)) if nm_msg else (len(NM_Waehlhebel__timestamp_list) - 1), ((new_sec / NM_Waehlhebel_timestamp) - 2) if nm_msg else 0, ((new_sec / NM_Waehlhebel_timestamp) + 2) if nm_msg else 0, "Prüfen, ob die Applikation Botschaft NM_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (NM_Waehlhebel_timestamp, sec) if nm_msg else "Prüfen, ob die Applikation Botschaft NM_Waehlhebel nicht  gesendet wird." ))


# Instantiate test environment
testenv = TestEnv()
hil = testenv.getHil()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_317")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    nm_Waehlhebel_Diag = hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value
    meas_vars = [nm_Waehlhebel_Diag]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+]Schalte KL30 ein und KL15 aus", ""])
    hil.cl30_on__.set(1)
    hil.cl15_on__.set(0)

    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["\x0aSignal-Aufzeichnung von NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(["\xa0 Start DAQ Measurement", ""])
    daq.startMeasurement(meas_vars)

    # 1. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\x0a1. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # 2
    testresult.append(["\x0a2. Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )
    ## 3
    testresult.append(["\x0a3. Warte 5 s", "INFO"])
    time.sleep(5.0)

    # 4. Erneut Default Session anfordern: 0x1001
    testresult.append(["\x0a4. Erneut Default Session anfordern: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # 5. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\x0a5. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    #6
    testresult.append(["\x0a6. Warte 7 Sekund", ""])
    time.sleep(7.0)

    #7
    testresult.append(["\x0a7. Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )

    #8
    testresult.append(["\x0a8. Warte 5 Sekund", ""])
    time.sleep(5.0)

    # test step 8.1
    testresult.append(["\x0a8.1  Prüfe 5s lang, dass NM Botschaft nicht gesendet wird. Es werden nur applikation Botschaft gesendet.",""])
    check_cycletime(5, application_msg=True, nm_msg=False)

    testresult.append(["\x0a9. Prüfen ob der zuletzt gesendete Wert des Signals NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag = 1 ist.", ""])
    testresult.append(
        _checkStatus(current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value, nominal_status=1,
                     descr="Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag__value = 1(zuletzt gesendete Wert) ist",
                     ticket_id='Fehler Id:EGA-PRM-142'))

    # 10. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\x0a10. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default', ticket_id="Fehler Id:EGA-PRM-189"))

    #11
    testresult.append(["\x0a11. Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(
        _checkStatus(current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value, nominal_status=1,
                     descr="Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag__value = 1 (aktiv) ist",
                     ticket_id='FehlerId:EGA-PRM-259'))

    testresult.append(["\x0a12. Warte 1 Minute", ""])
    time.sleep(60)

    # 13. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\x0a13. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    diag_request = [0x22, 0xF1, 0x86]
    response, [description, verdict]  = canape_diag.sendDiagRequest(diag_request)
    testresult.append(
        basic_tests.compare(
            left_value=response,
            operator="==",
            right_value=[],
            descr="Prüfe, Kein antwort erhalten",
        )
    )

    # 14
    testresult.append(["\x0a14. Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(
        _checkStatus(current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value, nominal_status=1,
                     descr="Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag__value = 1 (zuletzt gesendete Wert) ist",
                     ticket_id='Fehler Id:EGA-PRM-142'))

    # testresult.append(
    #     ["\x0a14.1  Prüfe 5s lang, dass NM Botschaft nicht gesendet wird. Es werden nur applikation Botschaft gesendet.",
    #      ""])
    # check_cycletime(5, application_msg=True, nm_msg=False)

    #
    testresult.append(["\x0a Stoppe DAQ Measurement", ""])
    daq_data = daq.stopMeasurement()
    plot_data = {}
    for mes in [nm_Waehlhebel_Diag]:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(
        daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))

finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print "Done."
