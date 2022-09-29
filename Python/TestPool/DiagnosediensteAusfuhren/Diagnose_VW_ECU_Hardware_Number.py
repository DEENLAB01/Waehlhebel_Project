# *****************************************************************************
# -*- coding: latin1 -*-
# File    :Diagnose_VW_ECU_Hardware_Number.py
# Title   :Diagnose VW ECU Hardware Number
# Task    : Test for Diag ECU Hardware number
#
# Author  : Devangbhai Patel
# Date    : 27.09.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ********************************* Version ***********************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 27.09.2021 | Devangbhai   | initial
# 1.1  | 27.09.2021 | Mohammed     | Rework
# 1.2  | 12.10.2021 | Mohammed     | Added TestSpec ID
# 1.2  | 22.12.2021 | H. Förtsch   | reworked test script by test spec
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv

from functions_diag import HexList
from diag_identifier import identifier_dict

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_252")

    # Initialize functions ####################################################

    # Initialize variables ####################################################
    test_data = identifier_dict['VW ECU Hardware Number']

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

    # -------------------------------------------------------------------------
    def _checkTestData():
        # test step
        testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                           .format(HexList(test_data['identifier']), test_data['name']),
                           ""])
        request = [0x22] + test_data['identifier']
        response, result = canape_diag.sendDiagRequest(request)
        testresult.append(result)
    
        # test step
        testresult.append(["[.] Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
    
        # test step
        testresult.append(["[.] Datenlänge überprüfen", ""])
        testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))
    
        # test step
        testresult.append(["[.] Inhalt der Response überprüfen", ""])
        expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']
        testresult.append(canape_diag.checkResponse(response, expected_response))

    # test step 1 - 4
    _checkTestData()

    # test step 5
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 6 - 9
    _checkTestData()

    # test step 10
    testresult.append(["[.] Wechsel in Factory mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    # test step 11 - 14
    _checkTestData()


    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

print "Done."
