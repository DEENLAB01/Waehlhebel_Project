# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : STANDALONE_ACTIVE_Mode_2.py
# Title   : STANDALONE_ACTIVE_Mode_2
# Task    : STANDALONE ACTIVE in Mode 2
#           
# Author  : M.A. Mushtaq
# Date    : 23.02.2022
# Copyright 2022 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 23.02.2022 | M.A. Mushtaq | initial
# 1.1  | 20.04.2022 | Mohammed     | Added VDSO_05 Signal
# 1.2  | 05.05.2022 | Mohammed     | Reworked
# 1.3  | 12.05.2022 | Mohammed     | Added Testschritte
# ******************************************************************************

# ******************************************************************************

from _automation_wrapper_ import TestEnv # @UnresolvedImport
from diag_identifier import DIAG_SESSION_DICT,identifier_dict
import time
import functions_gearselection
from ttk_checks import basic_tests

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################

    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    test_list = [identifier_dict['Status_ECU_Standalone-Mode'],
                 identifier_dict['ECU_standalone_mode_1'],
                 identifier_dict['ECU_standalone_mode_2']]

    request_defined_1 = [0x2E, 0xC1, 0x10, 0xBD, 0xDB, 0x6B, 0x3A]
    res_defined_1 = [0x62, 0xC1, 0x10, 0xBD, 0xDB, 0x6B, 0x3A]
    request_defined_2 = [0x2E, 0xC1, 0x11, 0x42, 0x24, 0x94, 0xC5]
    res_defined_2 = [0x62, 0xC1, 0x11, 0x42, 0x24, 0x94, 0xC5]
    request_undefined_1 = [0x62, 0xC1, 0x10, 0x00, 0x00, 0x00, 0x00]
    request_undefined_2 = [0x62, 0xC1, 0x11, 0x00, 0x00, 0x00, 0x00]
    expected_response_1 = [0x6E, 0xC1, 0x10]
    expected_response_2 = [0x6E, 0xC1, 0x11]
    request_Standalone_Modes_status_1 = [0x22, 0xC1, 0x10]
    request_Standalone_Modes_status_2 = [0x22, 0xC1, 0x11]
    request_Standalone_Modes_status = [0x22, 0xC1, 0x01]
    expected_Standalone_Modes_status = [0x62, 0xC1, 0x01, 0x01]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_284")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    time.sleep(5)
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()
    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1-1.2
    testresult.append(["[.] Auslesen DID: 0xF1F2 (KL30 Signal Read)", ""])
    request = [0x22] + [0xF1, 0xF2]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["[+] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Prüfe Voltage : 13-16 V", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.vbat_cl30__V.get(),  # letzer Sendetimestamp
            min_value=6.0,
            max_value=16.0,
            descr="Check that value is in range"
        )
    )
    testresult.append(["[-0]", ""])

    # test step 2-2.1
    testresult.append(["[.] Auslesen DID: 0xF1F3 (Temeprature Sensor Read)", ""])
    request = [0x22] + [0xF1, 0xF3]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["[+] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    testresult.append(["[-0]", ""])

    testresult.append(["[.] Setze alle E2E Messages Timeout", ""])
    hil.SiShift_01__period.setState("aus")
    hil.ORU_Control_A_01__period.setState("aus")
    hil.ORU_Control_D_01__period.setState("aus")
    hil.ORU_01__period.setState("aus")
    hil.OTAMC_D_01__period.setState("aus")
    hil.VDSO_05__period.setState("aus")
    time.sleep(2)
    testresult.append(["[+0]", ""])

    for i in range(2):
        if i==0:
            testresult.append(["[-] 'Setze  Standalone Mode 2 inactive und Mode 1 aktiv", ""])
        else:
            testresult.append(["[-] 'Setze Stand-alone mode 1 und 2 Auf Standalone aktiv", ""])

        testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
        testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

        testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
        testresult.extend(canape_diag.checkDiagSession('factory_mode'))

        testresult.append(["[.] Security Access aktivieren", ""])

        testresult.append(["[+] Seed anfragen: 0x2761", ""])
        seed, result = canape_diag.requestSeed()
        testresult.extend(result)

        testresult.append(["[.] Key berechnen: <key 1>", ""])
        key, result = canape_diag.calculateKey(seed)
        testresult.extend(result)

        testresult.append(["[.] Key senden: 0x2762 + <key 1>", ""])
        verdict = canape_diag.sendKey(key)
        testresult.extend(verdict)
        testresult.append(["[-0]", ""])
        if i == 0:
            testresult.append(["[.] Schreiben des Standalone_Modes_1: %s " %request_defined_1, ""])
            response, verdict = canape_diag.sendDiagRequest(request_defined_1)
            testresult.append(verdict)
            testresult.append(canape_diag.checkResponse(response, expected_response_1))
            testresult.append(["[.] Auslesen Standalone_Modes_1 Status ", ""])
            response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_status_1)
            testresult.append(verdict)
            testresult.append(canape_diag.checkResponse(response, res_defined_1))

            testresult.append(["[.] Auslesen Standalone_Modes_2 Status ", ""])
            response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_status_2)
            testresult.append(verdict)
            testresult.append(canape_diag.checkResponse(response, request_undefined_2))
            testresult.append(verdict)
        else:
            testresult.append(["[.] Schreiben des Standalone_Modes_2: %s " % request_defined_2, ""])
            response, verdict = canape_diag.sendDiagRequest(request_defined_2)
            testresult.append(verdict)
            testresult.append(canape_diag.checkResponse(response, expected_response_2))

            testresult.append(["[.] Auslesen des Standalone_Modes_2 Status ", ""])
            response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_status_2)
            testresult.append(verdict)
            testresult.append(canape_diag.checkResponse(response, res_defined_2))

            testresult.append(["[.] Schreiben des Standalone_Modes_1: %s " % request_defined_1, ""])
            response, verdict = canape_diag.sendDiagRequest(request_defined_1)
            testresult.append(verdict)
            testresult.append(canape_diag.checkResponse(response, expected_response_1))

            testresult.append(["[.] Auslesen Standalone_Modes Status ", ""])
            response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_status)
            testresult.append(verdict)
            testresult.append(canape_diag.checkResponse(response, expected_Standalone_Modes_status))
            testresult.append(verdict)

        testresult.append(["[+0]", ""])
        testresult.append(["[.] Setze VDSO_05_period Signal an und Warte Zykluszeit", ""])
        hil.VDSO_05__period.setState("an")
        time.sleep(.02)

        testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
        testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

        testresult.append(["[.] Lese aktuelle Extended Session aus und warte 2 Sekunde", ""])
        testresult.extend(canape_diag.checkDiagSession('extended'))
        time.sleep(2)

        #testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
        test_data = DIAG_SESSION_DICT['programming']
        request = test_data['identifier']
        response, result = canape_diag.sendDiagRequest(request)
        testresult.append(result)
        if i==0:
            testresult.append(["[.] Auf negative Response überprüfen", ""])
            testresult.append(canape_diag.checkNegativeResponse(response, request, 0x22))
            testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))
            time.sleep(5)
        else:
            testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
            testresult.extend(canape_diag.changeAndCheckDiagSession('programming', read_active_session=False))

            testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
            testresult.extend(canape_diag.checkDiagSession('programming'))


    # TEST POST CONDITIONS ####################################################
    #testresult.append(["[-0]", ""])
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################