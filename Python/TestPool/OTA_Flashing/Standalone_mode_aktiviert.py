# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : Standalone_mode_aktiviert.py
# Task    : Standalone_mode_aktiviert
#
# Author  : Mohammed Abdul Karim
# Date    : 18.02.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 18.02.2022 | Mohammed  | initial
# ******************************************************************************

from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import time


# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_xxxx")

    # Initialize functions ####################################################
    #func_common = functions_common.FunctionsCommon(testenv)


    # Initialize variables ####################################################
    test_dict = {
        1: identifier_dict['Status_ECU_Standalone-Mode'],
        2: identifier_dict['ECU_standalone_mode_1'],
        3: identifier_dict['ECU_standalone_mode_2']
    }
    request_defined_1 = [0x2E, 0xC1, 0x10, 0xBD, 0xDB, 0x6B, 0x3A]
    request_defined_2 = [0x2E, 0xC1, 0x11, 0x42, 0x24, 0x94, 0xC5]
    request_undefined_1 = [0x2E, 0xC1, 0x10, 0x11, 0x22, 0x33, 0x44]
    request_undefined_2 = [0x2E, 0xC1, 0x11, 0x11, 0x22, 0x33, 0x44]
    expected_response_1 = [0x6E, 0xC1, 0x10]
    expected_response_2 = [0x6E, 0xC1, 0x11]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    time.sleep(1)
    canape_diag = testenv.getCanapeDiagnostic()
    # testresult.append(["[.] Deaktiviere Tester Present", ""])
    # canape_diag.disableTesterPresent()
    #
    # canape_diag = testenv.getCanapeDiagnostic()
    # testresult.append(["[.] Tester Present deaktivieren", ""])
    # canape_diag.disableTesterPresent()

    testresult.append(["\xa0 In Default Session auslesen", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    testresult.append(["\x0a Wechsel in Factory Mode:  0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    testresult.append(["\xa0 Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    testresult.append(["\xa0 Seed anfragen: 0x2761"])
    seed, result = canape_diag.requestSeed()
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(result)

    testresult.append(["\xa0 Key berechnen:"])
    key, verdictkey = canape_diag.calculateKey(seed)
    testresult.append(verdictkey)

    testresult.append(["\xa0 Key senden: 0x2762 + <berechnet key>:"])
    verdict = canape_diag.sendKey(key)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(verdict)

    testresult.append(["[-] ECU auf 'Standalone aktiv' setzen ", ""])
    testresult.append(["[+] Anpasskanal 1 und 2 auf 'definierte' Werte setzen", ""])
    [response, result] = canape_diag.sendDiagRequest(request_defined_1)
    testresult.append(result)
    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_defined_1))

    testresult.append(canape_diag.checkResponse(response, expected_response_1))
    [response, result] = canape_diag.sendDiagRequest(request_defined_2)
    testresult.append(result)
    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkResponse(response, expected_response_2))

    for test in test_dict:
        test_data = test_dict[test]

        testresult.append(["[.] '%s' auslesen: %s" % (test_data['name'], str(HexList(test_data['identifier']))), ""])
        request = [0x22] + test_data['identifier']
        [response, result] = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
        expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']['active']
        testresult.append(canape_diag.checkResponse(response, expected_response))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup #################################################################
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

print "Done."
##################################################################