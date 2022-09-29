# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_ODX_File_Jobs.py
# Title   : Diagnose ODX File Jobs
# Task    : Test for reading the ODX identifier and version
#
# Author  : S. Stenger
# Date    : 25.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 25.05.2021 | StengerS     | automated test
# 1.1  | 25.05.2021 | Mohammed     | Added Ticket Id
# 1.2  | 03.12.2021 | H. Förtsch   | reworked test script by test spec
# *****************************************************************************

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
    testresult.setTestcaseId("TestSpec_127")

    # Initialize variables ####################################################
    test_list = [identifier_dict['ASAM ODX File Identifier'],
                 identifier_dict['ASAM ODX File Version']]

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

    for test_data in test_list:
        testresult.append(["[.] '{}' auslesen: {}"
                           .format(test_data['name'], HexList(test_data['identifier'])),
                           ""])
        request = [0x22] + test_data['identifier']
        response, result = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

        testresult.append(["[.] Datenlänge überprüfen", ""])
        if 'exp_data_length' in test_data:
            testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))
        else:
            testresult.append(canape_diag.checkDataRange(response, 3, 25))

        testresult.append(["[.] Inhalt auf Korrektheit überprüfen", ""])
        testresult.append(canape_diag.checkResponse(response[3:],
                                                    test_data['expected_response'],
                                                    ticket_id='Fehler Id:EGA-PRM-8'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    del testenv
    # #########################################################################

print "Done."
