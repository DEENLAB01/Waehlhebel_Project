# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Standaloan_Flashing.py
# Title   : Standaloan Flashing
# Task    : Test for Standaloan Flashing
#
# Author  : Mohammed Abdul Karim
# Date    : 16.02.2020
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 06.04.2022 | Mohammed     | initial
# ******************************************************************************

# Imports #####################################################################
import time
from _automation_wrapper_ import TestEnv
from ttk_tools.vector.vflash_api import VFlashAPI
import time
import functions_gearselection
import ttk_tools.vector.vflash_api as vflash_api

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
    testresult.setTestcaseId("TestSpec_XX")

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
    #testenv.startupECU()
    hil.cl30_on__.set(1)
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present aktivieren", ""])
    #canape_diag.enableTesterPresent()

    testresult.append([" \x0a Setze alle E2E Botschaft Timeout", "INFO"])
    hil.SiShift_01__period.setState("aus")
    hil.ORU_Control_A_01__period.setState("aus")
    hil.ORU_Control_D_01__period.setState("aus")
    hil.ORU_01__period.setState("aus")
    hil.OTAMC_D_01__period.setState("aus")
    hil.VDSO_05__period.setState("aus")

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up, add next parent chapter
    testresult.append(["[-0]", ""])

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
    testresult.append(["[+] Schreiben des ECU Standalone-Modes 1: 0x2E C1 10 BD DB 6B 3A", ""])
    response, result = canape_diag.sendDiagRequest(request_defined_1)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, expected_response_1))

    # test step 6.2
    testresult.append(["[.] Schreiben des ECU Standalone-Modes 2: 0x2E C1 11 42 24 94 C5", ""])
    response, result = canape_diag.sendDiagRequest(request_defined_2)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, expected_response_2))

    time.sleep(1)
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
        testresult.append(canape_diag.checkResponse(response, expected_response))


    testresult.append(["[.] SW-Flashtool starten:  vFlash Software Pfade anrufen.", "INFO"])

    flash_file_path = r"C:\Users\DEENLAB01\Desktop\SW0080\OTA\Template_1.vflash"
    vflash_dll_path = r'C:\Program Files (x86)\Vector vFlash 7\Bin\VFlashAutomation.dll'
    activate_network = False

    testresult.append(["[.] Setzen Flash Timeout 2000 Sekunden", "INFO"])
    flash_timeout = 2000
    vf = VFlashAPI(vflash_dll_path)

    print ("# vFlash Automation: ")
    print ("    vflash dll path: %s" % (vf.dll_path))
    print ("    flash file path: %s" % (flash_file_path))

    print ("# vFlash Automation: Flash Progress:")

    try:
        vf.flash(flash_file_path, testresult, activate_network, flash_timeout)
        testresult.append(["\x0aPrüfe Vflash: SW0080 Flashen Erfolgerich", "PASSED"])
    except vflash_api.VFlashResultError, ex:
        testresult.append(["\x0a Vflash: SW0080 Flashen Erfolgerich nicht Erfolgerich %s" % ex, "FAILED"])

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
