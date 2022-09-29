# ******************************************************************************
# -*- coding: latin1 -*-
# File    : PFIFF_339001.py
# Title   : PFIFF_339001
# Task    : Test for PFIFF_339001
#
# Author  : Mohammed Abdul Karim
# Date    : 04.04.2022
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 04.04.2022 | Mohammed     | initial
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
    testresult.setTestcaseId("TestSpec_339001")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    test_list = [identifier_dict['Status_ECU_Standalone-Mode'],
                 identifier_dict['ECU_standalone_mode_1'],
                 identifier_dict['ECU_standalone_mode_2']]

    request_defined_1 = [0x2E, 0xC1, 0x10, 0xE9, 0x5F, 0x34, 0x49]
    request_defined_2 = [0x2E, 0xC1, 0x11, 0x94, 0x68, 0x5E, 0xA4]
    request_undefined_1 = [0x2E, 0xC1, 0x10, 0xDB, 0xDB, 0x6B, 0x3A]
    request_undefined_2 = [0x2E, 0xC1, 0x11, 0x42, 0x24, 0x94, 0xC5]
    expected_response_1 = [0x6E, 0xC1, 0x10]
    expected_response_2 = [0x6E, 0xC1, 0x11]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

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

    testresult.append([" \x0a Setze alle E2E Botschaft Timeout", "INFO"])
    # hil.SiShift_01__period.setState("aus")
    hil.ORU_Control_A_01__period.setState("aus")
    hil.ORU_Control_D_01__period.setState("aus")
    hil.ORU_01__period.setState("aus")
    hil.OTAMC_D_01__period.setState("aus")

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up, add next parent chapter
    testresult.append(["[-0]", ""])


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


    # TEIL 3 ##################################################################
    # test step 6
    testresult.append(["[-] Auf \"Standalone aktiv\" setzen", ""])

    # test step 6.1
    testresult.append(["[+] Schreiben des ECU Standalone-Modes 1: 0X2E C1 10 E9 5F 34 49", ""])
    response, result = canape_diag.sendDiagRequest(request_defined_1)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, expected_response_1))

    # test step 6.2
    testresult.append(["[.] Schreiben des ECU Standalone-Modes 2: 0X2E C1 11 94 68 5E A4", ""])
    response, result = canape_diag.sendDiagRequest(request_defined_2)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, expected_response_2))

    # test step 5.8
    testresult.append(["[.] Schreiben des ECU Standalone-Modes 1: 0X2E C1 10 BD DB 6B 3A", ""])
    response, result = canape_diag.sendDiagRequest(request_undefined_1)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, expected_response_1))

    # test step 5.9
    testresult.append(["[.] Schreiben des ECU Standalone-Modes 2: 0X2E C1 11 42 24 94 C5", ""])
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
