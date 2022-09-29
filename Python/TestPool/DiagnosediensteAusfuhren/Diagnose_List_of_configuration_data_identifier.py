# *****************************************************************************
# -*- coding: latin-1 -*-
# File    : Diagnose_List_of_configuration_data_identifier.py
# Task    : Test for Diagnosejob 0x22 0x0250
#
# Author  : An3Neumann
# Date    : 17.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 17.06.2021 | An3Neumann   | initial
# 1.1  | 23.08.2021 | Mohammed     | Added Ticket Id
# 1.2  | 22.12.2021 | H. Förtsch   | reworked test script by test spec
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests

from functions_diag import HexList
from diag_identifier import identifier_dict
from functions_common import calcBytes2Value

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_155")

    # Initialize functions ####################################################

    # Initialize variables ####################################################
    test_data = identifier_dict['Integrity_validation_data_configuration_list']

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                       .format(HexList(test_data['identifier']), test_data['name']),
                       ""])
    request = [0x22] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 2
    testresult.append(["[.] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 3
    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    # test step 4
    testresult.append(["[.] Inhalt der Response überprüfen", ""])
    response_content = response[3:]

    # test step 4.1
    testresult.append(["[+] Prüfe Anzahl ausgegebener DataIdentifier", ""])
    count_di = calcBytes2Value(response_content[:2])  # Response Bytes 1 und 2
    testresult.append(
        basic_tests.checkStatus(
            current_status = len(response_content) - 2,
            nominal_status = count_di * 2,  # pro Dataidentifier 2 Bytes
            descr          = "Angabe Anzahl Dataidentifier prüfen: {value} (0x{value:04X})"
                             .format(value = count_di)))

    # test step 4.2
    testresult.append(["[.] Prüfe, dass eigener DataIdentifier nicht mit ausgegeben wird", ""])
    data_identifier = response_content[2:]
    # convert to more readable string
    if data_identifier:
        data_identifier = '0x{}'.format(''.join(['{:02X}'.format(x) for x in data_identifier]))
    else:
        data_identifier = "None"
    testresult.append(
        basic_tests.compare(data_identifier,
                            "!=",
                            '0x{}'.format(''.join(['{:02X}'.format(x) for x in test_data['identifier']])),
                            descr = "Response bytes: {}".format(data_identifier)))

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
