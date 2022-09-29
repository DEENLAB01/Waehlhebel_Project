# *****************************************************************************
# -*- coding: latin1 -*-
# File    : FactoryMode_Write_VW_ECU_Hardware_Version_Number.py
# Title   : Diagnose EGA VW ECU Hardware Version Number
# Task    : A minimal "Diagnose_EGA_VW_ECU_Hardware_Version_Number!" test script
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
    testresult.setTestcaseId("TestSpec_412")

    # Initialize variables ####################################################
    test_data = identifier_dict['VW ECU Hardware Version Number']

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

    vw_hw_version_number_orig = response[3:]

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 2
    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    # test step 3
    testresult.append(["[.] Inhalt auf Korrektheit überprüfen", ""])
    testresult.append(canape_diag.checkResponse(vw_hw_version_number_orig, test_data['expected_response']))

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
    vw_hw_version_number = [0x48, 0x30, 0x33]
    request = [0x2E, 0xF1, 0xA3]
    testresult.append(["[-] Schreibe VW ECU Hardware Version Number: 0x{} + 0x{}"
                       .format("".join("{:02X}".format(x) for x in request),
                               "".join("{:02X}".format(x) for x in vw_hw_version_number)),
                       ""])
    response, result = canape_diag.sendDiagRequest(request + vw_hw_version_number)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 8
    testresult.append(["[.] Prüfe Inhalt: 0x{}"
                       .format(" ".join("{:02X}".format(x) for x in vw_hw_version_number)),
                       ""])
    request = [0x22, 0xF1, 0xA3]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response[3:], vw_hw_version_number))

    # test step 9
    request = [0x2E, 0xF1, 0xA3]
    testresult.append(["[.] Schreibe originale VW ECU Hardware Version Number: 0x{} + 0x{}"
                      .format(" ".join("{:02X}".format(x) for x in request),
                              " ".join("{:02X}".format(x) for x in vw_hw_version_number_orig)),
                       ""])
    response, result = canape_diag.sendDiagRequest(request + vw_hw_version_number_orig)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 10
    testresult.append(["[.] Prüfe Inhalt: 0x{}"
                      .format(" ".join("{:02X}".format(x) for x in vw_hw_version_number_orig)),
                       ""])
    request = [0x22, 0xF1, 0xA3]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response[3:], vw_hw_version_number_orig))

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
