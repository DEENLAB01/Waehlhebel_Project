# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Factory_Mode.py
# Title   : Diagnose Factory Mode
# Task    : A minimal "Factory_Mode!" test script
#
# Author  : Mohammed Abdul Karim
# Date    : 21.02.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 16.02.2022 | Mohammed     | initial
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
    testresult.setTestcaseId("TestSpec_158_00")

    # Initialize functions ####################################################

    # Initialize variables ####################################################
    test_data = [identifier_dict['VW Spare Part Number'],
                 identifier_dict['System Supplier Identifier'],
                 identifier_dict['ECU Serial Number'],
                 identifier_dict['System Supplier ECU Hardware Number'],
                 identifier_dict['System Supplier ECU Hardware Version Number'],
                 identifier_dict['System Supplier ECU Software Number'],
                 identifier_dict['System Supplier ECU Software Version Number'],
                 identifier_dict['VW System Name Or Engine Type'],
                 identifier_dict['VW ECU Hardware Version Number'],
                 identifier_dict['VW Workshop System Name'],
                 identifier_dict['VW FAZIT Identification String']]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up, add next parent chapter
    testresult.append(["[-0]", ""])

    testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                      .format(HexList(test_data['identifier']), test_data['name']),
                       ""])
    request = [0x22] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    ecu_serial_number_orig = response[3:]
    for test_data in test_data:
        #cu_serial_number_orig = response[3:]
        testresult.append(["[.] {}".format(test_data['name']), ""])

        testresult.append(["[+] '{}' auslesen: {}"
                          .format(test_data['name'],
                                  HexList(test_data['identifier'])),
                           ""])
        request = [0x22] + test_data['identifier']
        [response, result] = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

        testresult.append(["[.] Datenlänge überprüfen", ""])
        testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))


        # test step 4
    ecu_serial_number_orig = response[3:]
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    # test step 5
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 6
    testresult.append(["[.] Security Access aktivieren", ""])

    # test step 6.1
    testresult.append(["[.] Seed anfragen: 0x2761", ""])
    seed, result = canape_diag.requestSeed()
    testresult.extend(result)

    # test step 6.2
    testresult.append(["[.] Key berechnen: <key 1>", ""])
    key, result = canape_diag.calculateKey(seed)
    testresult.extend(result)

    # test step 6.3
    testresult.append(["[.] Key senden: 0x2762 + <key 1>", ""])
    verdict = canape_diag.sendKey(key)
    testresult.extend(verdict)

    # ecu_serial_number = [0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37,
    #                      0x38, 0x39, 0x31, 0x32]
    # request = [0x2E, 0xF1, 0x8C]
    # testresult.append(["[-] Schreibe ECU Serial Number: 0x{} + 0x{}"
    #                   .format("".join("{:02X}".format(x) for x in request),
    #                           "".join("{:02X}".format(x) for x in ecu_serial_number)),
    #                    ""])
    # response, result = canape_diag.sendDiagRequest(request + ecu_serial_number)
    #
    # testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    # testresult.append(canape_diag.checkPositiveResponse(response, request))
    #
    # # test step 8
    # testresult.append(["[.] Prüfe Inhalt: 0x{}"
    #                   .format(" ".join("{:02X}".format(x) for x in ecu_serial_number)),
    #                    ""])
    # request = [0x22, 0xF1, 0x8C]
    # response, result = canape_diag.sendDiagRequest(request)
    # testresult.append(result)
    # testresult.append(canape_diag.checkResponse(response[3:], ecu_serial_number))
    #
    # # test step 9
    # request = [0x2E, 0xF1, 0x8C]
    # testresult.append(["[.] Schreibe originale ECU Serial Number: 0x{} + 0x{}"
    #                   .format(" ".join("{:02X}".format(x) for x in request),
    #                           " ".join("{:02X}".format(x) for x in ecu_serial_number_orig)),
    #                    ""])
    # response, result = canape_diag.sendDiagRequest(request + ecu_serial_number_orig)
    #
    # testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    # testresult.append(canape_diag.checkPositiveResponse(response, request))

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
