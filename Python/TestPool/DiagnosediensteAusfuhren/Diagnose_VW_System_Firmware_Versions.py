# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_VW_System_Firmware_Versions.py
# Title   : Diagnose VW System Firmware Versions
# Task    : Test for diag identifier F1B8
#
# Author  : M. Abdul Karim
# Date    : 10.06.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ********************************* Version ***********************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 21.06.2021 | StengerS     | initial
# 1.1  | 09.12.2021 | H. Förtsch   | reworked test script by test spec
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
    testresult.setTestcaseId("TestSpec_140")

    # Initialize variables ####################################################
    test_data = identifier_dict['VW_system_firmware_versions']

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

    # 1. Auslesen der System-Firmware-Versionen: 0x22F1B8
    # 2. Länge der Response überprüfen
    # 3. Anzahl der FW Versionen auswerten
    # 4. System-Firmware-Versionen auf Korrekheit überprüfen

    # test step 1
    testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                       .format(HexList(test_data['identifier']), test_data['name']),
                       ""])
    request = [0x22] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 2
    testresult.append(["[.] Länge der Response überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    # test step 3
    testresult.append(["[.] Anzahl der FW Versionen auswerten", ""])
    testresult.append(["Testspezifikation: <count> = <exp_count>", "TODO"])

    # test step 4
    testresult.append(["[.] System-Firmware-Versionen auf Korrekheit überprüfen", ""])
    expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']
    testresult.append(canape_diag.checkResponse(response, expected_response, ticket_id='FehlerId:EGA-PRM-210'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################
