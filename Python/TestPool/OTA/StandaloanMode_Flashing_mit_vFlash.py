# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : StandaloanMode_Flashing_mit_vFlash.py
# Title   : StandaloanMode_Flashing_mit_vFlash
# Task    : Standaloan Mode Flashing mit vFlash Tools
#
# Author  : Mohammed Abdul Karim
# Date    : 01.08.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 01.08.2022 | Mohammed | initial
# 1.1  | 02.08.2022 | Mohammed | Added TestSpec ID
# ******************************************************************************

# ******************************************************************************


from _automation_wrapper_ import TestEnv  # @UnresolvedImport
from ttk_tools.vector.vflash_api import VFlashAPI
import ttk_tools.vector.vflash_api as vflash_api
import time
from ttk_checks import basic_tests
import functions_gearselection
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################

    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    flash_file_path = r"C:\Users\DEENLAB01\Desktop\SW0111\vFlash_Prod\Project1.vflash" ## must be ISOCAN via vFlash
    vflash_dll_path = r'C:\Program Files (x86)\Vector vFlash 7\Bin\VFlashAutomation.dll'
    activate_network = False
    flash_timeout = 2000
    vf = VFlashAPI(vflash_dll_path)

    print "# vFlash Automation: "
    print "    vflash dll path: %s" % (vf.dll_path)
    print "    flash file path: %s" % (flash_file_path)

    test_list = [identifier_dict['Status_ECU_Standalone-Mode'],
                 identifier_dict['ECU_standalone_mode_1'],
                 identifier_dict['ECU_standalone_mode_2']]

    request_defined_1 = [0x2E, 0xC1, 0x10, 0xBD, 0xDB, 0x6B, 0x3A]
    request_defined_2 = [0x2E, 0xC1, 0x11, 0x42, 0x24, 0x94, 0xC5]
    expected_response_1 = [0x6E, 0xC1, 0x10]
    expected_response_2 = [0x6E, 0xC1, 0x11]
    request_Standalone_Modes_status_1 = [0x22, 0xC1, 0x10]
    request_Standalone_Modes_status_2 = [0x22, 0xC1, 0x11]
    request_Standalone_Modes_status = [0x22, 0xC1, 0x01]
    expected_Standalone_Modes_status = [0x62, 0xC1, 0x01, 0x01]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_405")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: KL30 ein und KL15 aus", ""])
    #testenv.startupECU()
    hil.cl30_on__.set(1)
    hil.cl15_on__.set(0)

    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present und Warte 100ms", ""])
    canape_diag.disableTesterPresent()
    time.sleep(.1)

    Physical_ID = 0x1C400053
    response_CAN_ID = 0x1C420053
    Functional_req_CAN_ID = 0x1C410000

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Setze in Vflash: Physical_ID = 0x1C400053, Response_CAN_ID = 0x1C420053 und Functional_req_CAN_ID = 0x1C410000 ", ""])
    testresult.append(["Setze vFlash Tool --> Configure --> Communication: Physical CAN ID = %s , Response CAN ID = %s, Functional Request CAN ID = %s" %(Physical_ID,response_CAN_ID, Functional_req_CAN_ID), "INFO"])

    # test step 2
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # test step 3-3.2
    testresult.append(["[.] Auslesen DID: 0xF1F2 (KL30 Signal Read)", ""])
    request = [0x22] + [0xF1, 0xF2]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["[+] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Prüfe Voltage : 13-16 V", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.vbat_cl30__V.get(),  # letzer Sendetimestamp
            min_value=6.0,
            max_value=16.0,
            descr="Check that value is in range"
        )
    )
    testresult.append(["[-0]", ""])

    # test step 4-4.2
    testresult.append(["[.] Auslesen DID: 0xF1F3 (Temeprature Sensor Read)", ""])
    request = [0x22] + [0xF1, 0xF3]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["[+] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Prüfe Raumtemperatur zwischen -40 to 90 Grad", ""])
    if len(response) > 3:
        data = response[3:]  # just take data of complete response
        temp_value_dec = 0
        i = len(response) - 3 - 1
        for temp_value in data:
            temp_value_dec += temp_value << (i * 8)  # set all bytes together
            i -= 1

        testresult.append(["Empfangene Daten (Rohwert): {}\nEntspricht dem Temeprature Sensor Wert : {} Grad"
                          .format(str(HexList(data)), temp_value_dec),
                           "INFO"])
        testresult.append(basic_tests.checkRange(temp_value_dec, 0, 0x5A))

    else:
        testresult.append(["Keine Auswertung möglich, da falsche oder keine Response empfangen wurde!", "FAILED"])
    testresult.append(["[-0]", ""])

    # test step 5
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 6
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060 und Warte 1 Sekunde", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))
    time.sleep(1)

    # test step 7
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 8-8.2
    testresult.append(["[.] Seed anfragen: 0x2761", ""])
    seed, result = canape_diag.requestSeed()
    testresult.extend(result)
    testresult.append(["[+] Key berechnen: <key 1>", ""])
    key, result = canape_diag.calculateKey(seed)
    testresult.extend(result)
    testresult.append(["[.] Key senden: 0x2762 + <key 1>", ""])
    verdict = canape_diag.sendKey(key)
    testresult.extend(verdict)
    testresult.append(["[-0]", ""])

    # test step 9-9.5
    testresult.append(["[.] Auf \"Standalone aktiv\" setzen und warte 2 Sekunde", ""])
    hil.SiShift_01__period.setState("aus")
    hil.ORU_Control_A_01__period.setState("aus")
    hil.ORU_Control_D_01__period.setState("aus")
    hil.ORU_01__period.setState("aus")
    hil.OTAMC_D_01__period.setState("aus")
    hil.VDSO_05__period.setState("aus")
    time.sleep(2)

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
    testresult.append(["[-0]", ""])

    # test step 8-8.3
    testresult.append(["[.] SW-Flashing starten:vFlash Software Pfade anrufen.", ""])
    try:
        vf.flash(flash_file_path, testresult, activate_network, flash_timeout)
        testresult.append(["\x0aStandaLoanMode Flashing: SW0111 Erfolgreich", "PASSED"])
    except vflash_api.VFlashResultError, ex:
        testresult.append(["ORUnext Flashing: SW0111 nicht Erfolgreich %s" % ex, "FAILED"])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.shutdownECU()
    testenv.breakdown()
    # #########################################################################