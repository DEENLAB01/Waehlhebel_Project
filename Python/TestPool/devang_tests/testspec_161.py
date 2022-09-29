# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_Parametrierung_Knockout_Counter.py
# Title   : Diagnose_Parametrierung_Knockout_Counter
# Task    : A minimal "Diagnose Parametrierung Knockout Counter!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 03.11.2021 | Devangbhai  | initial
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

testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    hil = testenv.getHil()
    testresult = testenv.getResults()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_com = functions_common.FunctionsCommon(testenv)
    test_dict = {
        1: identifier_dict['Knockout_test_mode'],
        2: identifier_dict['Knockout_counter'],
        3: identifier_dict['Knockout_timer']
    }

    request_dict = {1: {
        'identifier': [0x2E, 0x02, 0xCA],
        'name': 'Knockout_counter_write',
        'expected_response': [0x6E, 0x02, 0xCA],
        'exp_data_length': 3},
        2: {
            'identifier': [0x2E, 0x02, 0xCB],
            'name': 'Knockout_timer_write',
            'expected_response': [0x6E, 0x02, 0xCB],  # ToDo
            'exp_data_length': 3,  # Bytes
        },
        3: {
            'identifier': [0x2E, 0x09, 0xF3],
            'name': 'Knockout_test_mode_write',
            'expected_response': [0x6E, 0x09, 0xF3],  # ToDo
            'exp_data_length': 3
        },
    }

    # Initialize variables ####################################################
    test_variable = hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value
    test_variable.alias = "KN_Waehlhebel:ECUKnockOutTimer"

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_161")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # 1. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa01. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    testresult.append(["\xa01.1 Auslesen der Knockout Counter: 0x2202CA"])
    for test in test_dict:
        test_data = test_dict[test]
        if test_data['name'] == 'Knockout_counter':
            request = [0x22] + test_data['identifier']
            expected_response = [0x62, 0x02, 0xCA]
            [response, result] = canape_diag.sendDiagRequest(request)
            canape_diag.checkPositiveResponse(response, request)
            if response == expected_response:
                testresult.append(["\xa01.2 Länge der Response überprüfen"])
                testresult.append(basic_tests.checkStatus(len(response[3:]), 2, descr='Länge der Response ist 2 byte'))

    testresult.append(["\xa02. Schreiben im Factory Mode"])

    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    testresult.append(["\xa02.2 Wechsel in die Factory Session: 0x10, 0x60", ""])

    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    testresult.append(["\xa02.5 Seed anfragen: 0x2761"])
    seed, result = canape_diag.requestSeed()
    testresult.extend(result)

    testresult.append(["\xa02.6 Key berechnen:"])
    key, verdictkey = canape_diag.calculateKey(seed)
    testresult.append(verdictkey)

    testresult.append(["\xa02.7 Key senden: 0x2712 + <berechnet key>:"])
    verdict = canape_diag.sendKey(key)
    testresult.extend(verdict)

    testresult.append(["\xa02.8 Schreiben der Knockout Counter: 0x2E02CA + C8C8 (jew. 200dez)"])
    req = [0x2E, 0x02, 0xCA, 0xC8, 0xC8]
    [response, result] = canape_diag.sendDiagRequest(req)
    testresult.append(result)
    if response == [0x6E, 0x02, 0xCA]:
        testresult.append(["Positive Response: 0x6E 02CA", "PASSED"])
        testresult.append(["\xa02.9 Auslesen der Knockout Counter: 0x2202CA"])
        for test in test_dict:
            test_data = test_dict[test]
            if test_data['name'] == 'Knockout_counter':
                request = [0x22] + test_data['identifier']
                expected_response = [0x62, 0x02, 0xCA, 0xC8, 0xC8]
                [response, result] = canape_diag.sendDiagRequest(request)
                if response == expected_response:
                    testresult.append(basic_tests.checkStatus(response[3:], [0xC8, 0xC8], descr='Positive Response überprüfen: 0x6202CA + C8C8 '))
                else:
                    testresult.append(["Positive Response überprüfen: 0x6202CA + C8C8 ", "FAILED"])

    else:
        testresult.append(["Negative Antwort %s" %response, "FAILED"])
        testresult.append(["\xa02.9 Auslesen der Knockout Counter: 0x2202CA"])
        testresult.append(["Positive Response überprüfen: 0x6202CA + C8C8 ", "FAILED"])


    testresult.append(["\xa03  Anpasswerte wieder auf vorherige Werte setzen"])
    testresult.append(["\xa03.1  Schreiben der Knockout Counter: 0x2E02CA + 0x0F0F"])
    req = [0x2E, 0x02, 0xCA, 0x0F, 0x0F]
    [response, result] = canape_diag.sendDiagRequest(req)
    testresult.append(result)
    if response == [0x6E, 0x02, 0xCA]:
        testresult.append(["Positive Response: 0x6E 02CA", "PASSED"])
        testresult.append(["\xa03.2 Auslesen der Knockout Counter: 0x2202CA"])
        for test in test_dict:
            test_data = test_dict[test]
            if test_data['name'] == 'Knockout_counter':
                request = [0x22] + test_data['identifier']
                expected_response = [0x62, 0x02, 0xCA, 0x0F, 0x0F]
                [response, result] = canape_diag.sendDiagRequest(request)
                if response == expected_response: testresult.append(basic_tests.checkStatus(response[3:], [0x0F, 0x0F], descr='Positive Response überprüfen: 0x6202CA + 0x0F0F'))
                else:
                    testresult.append(["Positive Response überprüfen: 0x6202CA + 0x0F0F ", "FAILED"])

    else:
        testresult.append(["Negative Antwort %s" %response, "FAILED"])
        testresult.append(["\xa03.2 Auslesen der Knockout Counter: 0x2202CA"])
        testresult.append(["Positive Response überprüfen: 0x6202CA + 0x0F0F ", "FAILED"])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print "Done."
