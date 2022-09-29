# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Flashen_vFlash.py
# Title   : Flashen über vFlash
# Task    : Flashen_vFlash
#
# Author  : Mohammed Abdul Karim
# Date    : 05.05.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 05.04.2022 | Mohammed     | initial
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import functions_hil
from ttk_tools.vector.vflash_api import VFlashAPI
import time
import functions_gearselection
import ttk_tools.vector.vflash_api as vflash_api

from ttk_checks import basic_tests
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict
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
    test_list = [identifier_dict['VW Application Software Version Number'],
                 identifier_dict['VW ECU Hardware Version Number'],
                 identifier_dict['VW_system_firmware_versions']]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_3")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: LK30 und Kl15 an", ""])
    testenv.startupECU()  # startup before cal vars are called
    testresult.append(["[+] Setze Waehlhebelposition P aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    #testresult.append(["\xa0" + descr, verdict])
    #time.sleep(1)
    testresult.append(["[.] Setze VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    testresult.append(["[.] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 1 (VPE_PRODUCTION)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 0 (IDLE)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 0 (IDLE)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)
    testresult.append(["[.] Warte 2 Sekunde", ""])
    time.sleep(2)
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()
    #testresult.append(["[-0]", ""])

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    testresult.append(["[.] SW-Flashtool starten:  vFlash Software Pfade anrufen.", ""])
    flash_file_path = r"C:\Users\DEENLAB01\Desktop\SW0111\vFlash_Prod\Project1.vflash" ### must be vFlash path with ISO CAN ID
    vflash_dll_path = r'C:\Program Files (x86)\Vector vFlash 7\Bin\VFlashAutomation.dll'
    activate_network = False

    testresult.append(["[.] Setzen Flash Timeout 2000 Sekunden", ""])
    flash_timeout = 2000
    vf = VFlashAPI(vflash_dll_path)

    print ("# vFlash Automation: ")
    print ("    vflash dll path: %s" % (vf.dll_path))
    print ("    flash file path: %s" % (flash_file_path))

    print ("# vFlash Automation: Flash Progress:")

    try:
        vf.flash(flash_file_path, testresult, activate_network, flash_timeout)
        testresult.append(["\x0aPrüfe Vflash: SW 0111 Flashen Erfolgerich", "PASSED"])
    except vflash_api.VFlashResultError, ex:
        testresult.append(["\x0a Vflash: SW 0111 Flashen Erfolgerich nicht Erfolgerich %s" % ex, "FAILED"])
    #testresult.append(["[-0]", ""])

    time.sleep(2)
    # test step 6 to 9
    for test_data in test_list:
        testresult.append(["[.] {}".format(test_data['name']), ""])

        if test_data['name'] == 'VW Application Software Version Number':
            expected_data = [0x30, 0x31, 0x31, 0x31]  #
        else:
            expected_data = test_data['expected_response']

        # test step x.1
        testresult.append(["[+] '{}' auslesen: {}"
                          .format(test_data['name'], HexList(test_data['identifier'])),
                           ""])
        request = [0x22] + test_data['identifier']
        response, result = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

        # test step x.2
        testresult.append(["[.] Datenlänge überprüfen", ""])
        testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

        # test step x.3
        testresult.append(["[.] Inhalt auf Korrektheit überprüfen", ""])
        testresult.append(canape_diag.checkResponse(response[3:], expected_data))

        # silently go one chapter level up, add next parent chapter
        testresult.append(["[-0]", ""])

    # cleanup
    hil = None

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.shutdownECU()
    testenv.breakdown(ecu_shutdown=False)
    print('done')

