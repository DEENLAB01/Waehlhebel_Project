# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Verify_ContainsVersion_via_DID_F1B4.py
# Title   : Verify_ContainsVersion_via_DID_F1B4
# Task    : Verify Contains Version of QLAH OTA
#
# Author  : Mohammed Abdul Karim
# Date    : 02.05.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name     | Description
# -----------------------------------------------------------------------------
# 1.0  | 02.05.2021 | Mohammed  | initial
# 1.1  | 05.05.2022 | Mohammed  | Reworked
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
from ttk_checks import basic_tests

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()


    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_364")

    # Initialize variables ####################################################
    test_data = identifier_dict['Technical_specifications_version']

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Wechsel in Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # test step 2
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 3
    testresult.append(["[.] '{}' auslesen: {}"
                       .format(test_data['name'],
                               HexList(test_data['identifier'])),
                       ""])
    request = [0x22] + test_data['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[+0]", ""])

    # test step 4
    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    testresult.append(["[.] Inhalt auf Korrektheit überprüfen", ""])
    exp_response = [0x62] + test_data['identifier'] + test_data['expected_response']
    testresult.append(canape_diag.checkResponse(response, exp_response))

    testresult.append(["[-] Prüfe QLAH-OTA (Byte21==02 and Byte22==01)", ""])
    #testresult.append(["[+]", ""])
    testresult.append(canape_diag.checkResponse(response[3:], test_data['expected_response']))
    if len(response)>=21:
        testresult.append(["[+] Prüfe Byte21 = 0x02", ""])
        testresult.append(
            basic_tests.checkStatus(
                current_status=response[20+3],
                nominal_status=0x02,
                descr="Prüfe, Byte21 = 0x02 ist",
            )
        )
        testresult.append(["[.] Prüfe Byte22 = 0x01", ""])
        testresult.append(
            basic_tests.checkStatus(
                current_status=response[21+3],
                nominal_status=0x01,
                descr="Prüfe, Byte22 = 0x02 ist",
            )
        )

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    del(testenv)
    # #########################################################################

print "Done."
