# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_VW_Data_Set_Number_Or_ECU_Data_Container_Number.py
# Title   : Diagnose VW Data Set Number Or ECU Data Container Number
# Task    : Test for Diag identifier F1A0
#
# Author  : M. Abdul Karim
# Date    : 10.06.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 27.09.2021 | Mohammed   | initial
# 1.1  | 12.10.2021 | Mohammed  | Added TestSpec ID
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport


# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_255")

    # Initialize variables ####################################################
    test_dict = {
        1: identifier_dict['VW Data Set Number Or ECU Data Container Number']
    }

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    for test in test_dict:
        test_data = test_dict[test]
        testresult.append(["[.] '%s' auslesen: %s" % (test_data['name'], str(HexList(test_data['identifier']))), ""])
        request = [0x22] + test_data['identifier']
        [response, result] = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

        testresult.append(["\xa0Datenlänge überprüfen", ""])
        testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

        testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
        expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']
        testresult.append(canape_diag.checkResponse(response, expected_response))

    # Wechsel in Extended Session: 0x1003
    testresult.append(["[.] In die Extended Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))
    for test in test_dict:
        test_data = test_dict[test]
        testresult.append(["[.] '%s' auslesen: %s" % (test_data['name'], str(HexList(test_data['identifier']))), ""])
        request = [0x22] + test_data['identifier']
        [response, result] = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

        testresult.append(["\xa0Datenlänge überprüfen", ""])
        testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

        testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
        expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']
        testresult.append(canape_diag.checkResponse(response, expected_response))


    # Wechsel in Wechsel in Factory Mode: 0x1060
    testresult.append(["[.] In die Factory Mode wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    for test in test_dict:
        test_data = test_dict[test]
        testresult.append(["[.] '%s' auslesen: %s" % (test_data['name'], str(HexList(test_data['identifier']))), ""])
        request = [0x22] + test_data['identifier']
        [response, result] = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

        testresult.append(["\xa0Datenlänge überprüfen", ""])
        testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

        testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
        expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']
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