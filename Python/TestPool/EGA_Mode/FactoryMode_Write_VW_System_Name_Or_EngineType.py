# *****************************************************************************
# -*- coding: latin1 -*-
# File    : FactoryMode_Write_VW_System_Name_Or_EngineType.py
# Title   : Diagnose EGA VW System Name Or Engine Type
# Task    : A minimal "Diagnose_EGA_VW_System_Name_Or_EngineType!" test script
#
# Author  : Mohammed Abdul Karim
# Date    : 17.02.2022
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 17.02.2022 | Mohammed     | initial
# 1.1  | 03.08.2022 | Mohammed     | Added Test ID
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
    testresult.setTestcaseId("TestSpec_411")

    # Initialize variables ####################################################
    test_data = identifier_dict['VW System Name Or Engine Type']

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\nStarte Testprozess: %s"%testenv.script_name.split('.py')[0], ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] '%s' auslesen: %s" %(test_data['name'], HexList(test_data['identifier'])), ""])
    request = [0x22] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    engine_type_orig = response[3:]

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 2
    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    # test step 3
    testresult.append(["[.] Inhalt auf Korrektheit überprüfen", ""])
    testresult.append(canape_diag.checkResponse(engine_type_orig, test_data['expected_response']))

    # test step 4
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    # test step 5
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 6
    testresult.append(["[.] Security Access aktivieren", ""])

    # test step 6.1
    testresult.append(["[+] Seed anfragen: 0x2761", ""])
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

    # test step 7
    engine_type = [0x30, 0x30, 0x37, 0x38, 0x39, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48]
    request = [0x2E, 0xF1, 0x97]
    testresult.append(["[-] Schreibe VW System Name Or Engine Type: 0x{} + 0x{}"
                       .format("".join("{:02X}".format(x) for x in request),
                               "".join("{:02X}".format(x) for x in engine_type)),
                       ""])
    response, result = canape_diag.sendDiagRequest(request + engine_type)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 8
    testresult.append(["[.] Prüfe Inhalt: 0x{}"
                       .format(" ".join("{:02X}".format(x) for x in engine_type)),
                       ""])
    request = [0x22, 0xF1, 0x97]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response[3:], engine_type))

    # test step 9
    request = [0x2E, 0xF1, 0x97]
    testresult.append(["[.] Schreibe originale VW System Name Or Engine Type: 0x{} + 0x{}"
                      .format(" ".join("{:02X}".format(x) for x in request),
                              " ".join("{:02X}".format(x) for x in engine_type_orig)),
                       ""])
    response, result = canape_diag.sendDiagRequest(request + engine_type_orig)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 10
    testresult.append(["[.] Prüfe Inhalt: 0x{}"
                      .format(" ".join("{:02X}".format(x) for x in engine_type_orig)),
                       ""])
    request = [0x22, 0xF1, 0x97]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response[3:], engine_type_orig))

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
