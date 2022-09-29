# ******************************************************************************
# -*- coding: latin1 -*-
# File    : kein_Bus_KnockOut_KL15_EIN.py
# Title   :kein_Bus_KnockOut_KL15_EIN
# Task    : Test for kein_Bus_KnockOut_KL15_EIN
#
# Author  : Mohammed Abdul Karim
# Date    : 17.12.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 17.12.2021 | Mohammed   | initial
# 1.2  | 11.02.2022 | Devangbhai | Rework according to new specification
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList
from diag_identifier import identifier_dict
import functions_common
from ttk_checks import basic_tests
import functions_gearselection
import time
from time import time as t
import os

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_com = functions_common.FunctionsCommon(testenv)

    # Initialize variables ####################################################
    diag_ident_KN_CTR = identifier_dict['Knockout_counter']
    diag_ident_KN_TMR = identifier_dict['Knockout_timer']
    diag_ident_KN_TEST_MODE = identifier_dict['Knockout_test_mode']

    test_variable = hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value
    test_variable.alias = "KN_Waehlhebel:BusKnockOutTimer"

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_206")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[.] Wechsle in die Extended Session", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    testresult.append(["[.] BusKnockOut_Tmr und ECUKnockOut_Tmr auf 15 setzen"])
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x0F, 0x0F]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] BusKnockOut_Ctr und ECUKnockOut_Ctr auf 0 setzen"])
    request = [0x2E] + diag_ident_KN_CTR['identifier'] + [0x00, 0x00]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.]  ECU ausschalten", ""])
    testenv.canape_Diagnostic = None
    testenv.asap3 = None
    testenv.canape_Diagnostic = None
    del (canape_diag)
    testenv.shutdownECU()

    testresult.append(["[.]  Warte 10sekund", ""])
    time.sleep(10)

    testresult.append(["[.] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()

    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # test step 1
    testresult.append(["\x0a 1. Prüfe BusKnockOut_Ctr und speichere Wert in busctr_start. Und prüfe  BusKnockOut_Tmr und speichere Wert in busTmr_start"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    busctr_start = None

    if response[0:3] == [98, 2, 202]:
        busctr_start = response[4]
        if busctr_start is not None:
            busctr_start = busctr_start
            testresult.append(
                ["\xa0 Gespeichere Wert für BusKnockOut_Ctr (Variable) für späteren Vergleich ist %s" % busctr_start])
        else:
            busctr_start = 0
            testresult.append(
                ["\xa0 Gespeichere Wert für BusKnockOut_Ctr (Variable) für späteren Vergleich ist %s" % busctr_start])
    else:
        testresult.append(["\xa0 Kein Positive response erhalten.  BusKnockOut_Ctr kann nicht auslasen", "FAILED"])

    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BusKnockoutTmr_start = None

    if response[0:3] == [98, 2, 203]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BusKnockoutTmr_start = response[4]
        if BusKnockoutTmr_start is not None:
            if BusKnockoutTmr_start > 64:
                BusKnockoutTmr_start = BusKnockoutTmr_start - 64  # removing the active coupling value bit
            else:
                BusKnockoutTmr_start = BusKnockoutTmr_start  # No active NVEM coupling
        else:
            BusKnockoutTmr_start = 0

        testresult.append(["\xa0 Gespeichere Wert für BusKnockOut_timer (Variable) für späteren Vergleich ist %s" % BusKnockoutTmr_start])
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 2
    testresult.append(["\x0a 2.Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    if BusKnockoutTmr_start is not None:
        testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, BusKnockoutTmr_start,
                                               descr="KN_Waehlhebel_BUSKnockOutTimer = BusKnockoutTmr_start ")]

    # test step 3
    testresult.append(["\x0a 3. Warte 1,5 Minuten"])
    time.sleep(1.5*60)

    # test step 4
    testresult.append(["\x0a 4.Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    if BusKnockoutTmr_start is not None:
        testresult += [
            basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, BusKnockoutTmr_start,
                                    descr="KN_Waehlhebel_BUSKnockOutTimer = BusKnockoutTmr_start (Timer läuft nicht) ")]

    # test step 5
    testresult.append(["\x0a 5. Warte 1,5 Minuten"])
    time.sleep(1.5 * 60)

    # test step 6
    testresult.append(["\x0a 6.Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    if BusKnockoutTmr_start is not None:
        testresult += [
            basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, BusKnockoutTmr_start,
                                    descr="KN_Waehlhebel_BUSKnockOutTimer = BusKnockoutTmr_start (Timer läuft nicht) ")]

    # test step 7
    testresult.append(["\x0a 7. Warte 12,5 Minuten"])
    time.sleep(12.50 * 60)

    # test step 8
    testresult.append(["\x0a 8.Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    if BusKnockoutTmr_start is not None:
        testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, BusKnockoutTmr_start,
                                    descr="KN_Waehlhebel_BUSKnockOutTimer = BusKnockoutTmr_start (Timer läuft nicht) ")]

    # test step 9
    testresult.append(["\x0a 9. Prüfe  BUSKnockOut_Ctr (22 02 CA)"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BUSKnockOut_Ctr_end = None

    if response[0:3] == [98, 2, 202]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BUSKnockOut_Ctr_end = response[4]
        if BUSKnockOut_Ctr_end is not None:
            BUSKnockOut_Ctr_end = BUSKnockOut_Ctr_end
        else:
            BUSKnockOut_Ctr_end = 0
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    if busctr_start and BUSKnockOut_Ctr_end is not None:
        testresult += [basic_tests.checkStatus(busctr_start, BUSKnockOut_Ctr_end, descr=" BusKnockOut_Ctr == busctr_start (unverändert)")]

    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()
    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)