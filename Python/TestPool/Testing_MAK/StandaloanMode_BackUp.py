# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_ECU_standalone_mode.py
# Title   : Diagnose ECU standalone mode
# Task    : Test for reading the standalone mode and status
#
# Author  : S. Stenger
# Date    : 25.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 25.05.2021 | StengerS     | initial
# 1.1  | 31.05.2021 | StengerS     | added info for not implemented jobs
# 1.2  | 22.06.2021 | StengerS     | added write jobs
# 1.3  | 22.06.2021 | Mohammed     | added Ticket ID
# 1.4  | 09.12.2021 | H. Förtsch   | reworked test script by test spec
# 1.5  | 19.01.2022 | Mohammed     | Corrected step 5.4 and 4.3, 4.4: NRC values
# 1.6  | 28.01.2021 | Mohammed     | reworked test script after Adding preconditions
# 1.7  | 22.06.2021 | Mohammed     | added new Ticket ID
# 1.8  | 23.06.2022 | Mohammed     | Added E2E Botschaft Timeout
# ******************************************************************************

# Imports #####################################################################
import time
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_gearselection
# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_129")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    test_list = [identifier_dict['Status_ECU_Standalone-Mode'],
                 identifier_dict['ECU_standalone_mode_1'],
                 identifier_dict['ECU_standalone_mode_2']]

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
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory())
    #############################################
    testresult.append([" \x0a Setze alle E2E Botschaft Timeout", "INFO"])
    hil.SiShift_01__period.setState("aus")
    hil.ORU_Control_A_01__period.setState("aus")
    hil.ORU_Control_D_01__period.setState("aus")
    hil.ORU_01__period.setState("aus")
    hil.OTAMC_D_01__period.setState("aus")
    hil.ORU_01__period.setState("aus")
    #############################################

    ############################
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\x0a" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append([" \x0a Warte 1 Sekunde  ", "INFO"])
    time.sleep(1)


    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up, add next parent chapter
    #testresult.append(["[-0]", ""])

    # test steps 1, 2 and 3
    for test_data in test_list:
        testresult.append(["[.] {}".format(test_data['name']), ""])
        testresult.append(["[+] Diagnose Request schicken: 0x22 {} (Lese {})"
                           .format(HexList(test_data['identifier']), test_data['name']),
                           ""])
        request = [0x22] + test_data['identifier']
        response, result = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

        testresult.append(["[.] Länge der Response überprüfen", ""])
        testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

        # silently go one chapter level up, add next parent chapter
        testresult.append(["[-0]", ""])

    # test steps 4
    testresult.append(["[.] Prüfen, das Schreiben in Default, Extended und Programming Session abgelehnt wird", ""])
    # silently create a new subchapter level
    testresult.append(["[+0]", ""])
    for session in ['default', 'extended', 'programming']:
        # test steps 4.1, 4.5 and 4.9
        testresult.append(["[.] Wechsel in die {} Session".format(session.capitalize()), ""])
        testresult.extend(canape_diag.changeAndCheckDiagSession(session, read_active_session=False))

        # test steps 4.2, 4.6 and 4.10
        testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
        testresult.extend(canape_diag.checkDiagSession(session))

        # test steps 4.3, 4.7 and 4.11
        testresult.append(["[.] Schreiben des ECU Standalone-Modes 1: 0x2E C1 10 11 22 33 44", ""])
        testresult.extend(canape_diag.changeAndCheckDiagSession(session))
        response, result = canape_diag.sendDiagRequest(request_undefined_1)
        testresult.append(result)
        testresult.append(canape_diag.checkNegativeResponse(response,
                                                            request_undefined_1,
                                                            0x7F if session == "default" else 0x31))

        # test steps 4.4, 4.8 and 4.12
        testresult.append(["[.] Schreiben des ECU Standalone-Modes 2: 0x2E C1 11 11 22 33 44", ""])
        response, result = canape_diag.sendDiagRequest(request_undefined_2)
        testresult.append(result)
        testresult.append(canape_diag.checkNegativeResponse(response,
                                                            request_undefined_2,
                                                            0x7F if session == "default" else 0x31))

    # TEIL 2 ##################################################################
    # test steps 5
    testresult.append(["[-] Auf \"Standalone inaktiv\" setzen", ""])
    hil.SiShift_01__period.setState("aus")

    # test step 5.1
    testresult.append(["[+] Wechsel in die Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession("default", read_active_session=False))

    # test step 5.2
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 5.3
    testresult.append(["[.] Wechsel in den Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession("factory_mode", read_active_session=False))

    # test step 5.4
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 5.5
    testresult.append(["[.] Seed anfragen: 0x2761", ""])
    seed, result = canape_diag.requestSeed()
    testresult.extend(result)

    # test step 5.6
    testresult.append(["[.] Key berechnen", ""])
    key, result = canape_diag.calculateKey(seed)
    testresult.append(result)

    # test step 5.7
    testresult.append(["[.] Key senden: 0x2762 + {}".format(HexList(key)), ""])
    result = canape_diag.sendKey(key)
    testresult.extend(result)

    # test step 5.8
    testresult.append(["[.] Schreiben des ECU Standalone-Modes 1: 0x2E C1 10 11 22 33 44", ""])
    response, result = canape_diag.sendDiagRequest(request_undefined_1)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, expected_response_1))

    # test step 5.9
    testresult.append(["[.] Schreiben des ECU Standalone-Modes 2: 0x2E C1 11 11 22 33 44", ""])
    response, result = canape_diag.sendDiagRequest(request_undefined_2)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, expected_response_2))

    # test steps 5.10, 5.11, 5.12
    for test_data in test_list:
        testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                           .format(HexList(test_data['identifier']), test_data['name']),
                           ""])
        request = [0x22] + test_data['identifier']
        response, result = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
        expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']['inactive']
        testresult.append(canape_diag.checkResponse(response, expected_response))

    # TEIL 3 ##################################################################
    # test step 6
    testresult.append(["[-] Auf \"Standalone aktiv\" setzen", ""])

    # test step 6.1
    testresult.append(["[+] Schreiben des ECU Standalone-Modes 1: 0x2E C1 10 BD DB 6B 3A", ""])
    response, result = canape_diag.sendDiagRequest(request_defined_1)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, expected_response_1))

    # test step 6.2
    testresult.append(["[.] Schreiben des ECU Standalone-Modes 2: 0x2E C1 11 42 24 94 C5", ""])
    response, result = canape_diag.sendDiagRequest(request_defined_2)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, expected_response_2))

    # test steps 6.3, 6.4, 6.5
    for test_data in test_list:
        testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                           .format(HexList(test_data['identifier']), test_data['name']),
                           ""])
        request = [0x22] + test_data['identifier']
        response, result = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
        expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']['active']
        testresult.append(canape_diag.checkResponse(response, expected_response, ticket_id='Fehler Id:EGA-PRM-228'))

    # TEIL 4 ##################################################################
    # test step 7
    testresult.append(["[-] Nur Anpasskanal 1 schreiben, muss nach 30 Sekunden auf 0 gesetzt werden", ""])

    # test step 7.1
    testresult.append(["[+] Anpasskanal 1 auf 'definierten' Wert setzen", ""])
    response, result = canape_diag.sendDiagRequest(request_defined_1)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, expected_response_1))

    # test step 7.2
    testresult.append(["[.] 28 Sekunden warten", ""])
    time.sleep(28)

    # test steps 7.3, 7.4, 7.5
    for test_data in test_list:
        if test_data["name"] == 'Status_ECU_Standalone-Mode':
            testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                               .format(HexList(test_data['identifier']), test_data['name']),
                               ""])
            request = [0x22] + test_data['identifier']
            response, result = canape_diag.sendDiagRequest(request)
            testresult.append(result)

            testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
            expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']['active']
            testresult.append(canape_diag.checkResponse(response, expected_response, ticket_id='Fehler Id:EGA-PRM-262'))

        elif test_data["name"] == 'ECU_standalone_mode_1':
            testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                               .format(HexList(test_data['identifier']), test_data['name']),
                               ""])
            request = [0x22] + test_data['identifier']
            response, result = canape_diag.sendDiagRequest(request)
            testresult.append(result)

            testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
            expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']['active']
            testresult.append(canape_diag.checkResponse(response, expected_response, ticket_id='Fehler Id:EGA-PRM-228'))

        elif test_data["name"] == 'ECU_standalone_mode_2':
            testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                               .format(HexList(test_data['identifier']), test_data['name']),
                               ""])
            request = [0x22] + test_data['identifier']
            response, result = canape_diag.sendDiagRequest(request)
            testresult.append(result)

            testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
            expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']['inactive']
            testresult.append(canape_diag.checkResponse(response, expected_response, ticket_id='Fehler Id:EGA-PRM-228'))

    # test step 7.6
    testresult.append(["[.] 3 Sekunden warten", ""])
    time.sleep(3)

    # test steps 7.7, 7.8, 7.9
    for test_data in test_list:
        testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                           .format(HexList(test_data['identifier']), test_data['name']),
                           ""])
        request = [0x22] + test_data['identifier']
        response, result = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
        expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']['inactive']
        testresult.append(canape_diag.checkResponse(response, expected_response, ticket_id='Fehler Id:EGA-PRM-228'))

    # TEIL 5 ##################################################################
    # test step 8
    testresult.append(["[-] Auf \"Standalone aktiv\" setzen", ""])

    # test step 8.1
    testresult.append(["[+] Schreiben des ECU Standalone-Modes 1: 0x2E C1 10 BD DB 6B 3A", ""])
    response, result = canape_diag.sendDiagRequest(request_defined_1)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, expected_response_1))

    # test step 8.2
    testresult.append(["[.] Schreiben des ECU Standalone-Modes 2: 0x2E C1 11 42 24 94 C5", ""])
    response, result = canape_diag.sendDiagRequest(request_defined_2)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, expected_response_2))

    # test steps 8.3, 8.4, 8.5
    for test_data in test_list:

        testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                           .format(HexList(test_data['identifier']), test_data['name']),
                           ""])
        request = [0x22] + test_data['identifier']
        response, result = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        if test_data["name"] == 'Status_ECU_Standalone-Mode':
            testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
            expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']['active']
            testresult.append(canape_diag.checkResponse(response, expected_response, ticket_id='Fehler Id:EGA-PRM-228'))
        else:
            testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
            testresult.append(canape_diag.checkPositiveResponse(response, request))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    del testenv
    # #########################################################################

print "Done."
