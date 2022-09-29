# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Reflash_vFlash_PrecondCheck.py
# Title   : Flashen über vFlash Precondition Check
# Task    : Reflash_vFlash_PrecondCheck
#
# Author  : Mohammed Abdul Karim
# Date    : 29.03.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 29.03.2022 | Mohammed     | initial
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
    testenv.startupECU()  # startup before cal vars are called

    # Initialize variables ####################################################
    test_data = identifier_dict['VW Application Software Version Number']

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_378")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])
    time.sleep(1)
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])
    time.sleep(2)

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    testresult.append([" \x0aWarte 2 Sekunde", "INFO"])
    time.sleep(2)

    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\x0aStarte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # ******************************************************************************
    # -*- coding: latin-1 -*-
    #
    # File    : Flashen_vFlash_OBD_Drive_Cycle_NOT_SET.py
    # Title   : Flashen über vFlash OBD_Drive_Cycle NOT SET
    # Task    : Flashen_vFlash_OBD_Drive_Cycle_NOT_SET
    #
    # Author  : Mohammed Abdul Karim
    # Date    : 29.03.2022
    # Copyright 2021 Eissmann Automotive Deutschland GmbH
    #
    # ******************************************************************************
    # ********************************* Version ************************************
    # ******************************************************************************
    # Rev. | Date       | Name         | Description
    # ------------------------------------------------------------------------------
    # 1.0  | 29.03.2022 | Mohammed     | initial
    # 1.1  | 31.03.2022 | Mohammed     | Reworke afte TestSpec changed
    # ******************************************************************************
    #
    # Imports #####################################################################
    from _automation_wrapper_ import TestEnv
    import functions_hil
    from ttk_tools.vector.vflash_api import VFlashAPI
    import time
    import functions_gearselection
    import ttk_tools.vector.vflash_api as vflash_api
    from diag_identifier import identifier_dict
    from functions_diag import HexList  # @UnresolvedImport

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
        test_data = identifier_dict['VW Application Software Version Number']

        # set Testcase ID #########################################################
        testresult.setTestcaseId("TestSpec_380xx")

        # TEST PRE CONDITIONS #####################################################
        testresult.append(["[#0] Test Vorbedingungen: LK30 und Kl15 an", ""])
        testenv.startupECU()  # startup before cal vars are called
        testresult.append(["[+] Setze Waehlhebelposition P aktiviert", ""])
        descr, verdict = func_gs.changeDrivePosition('P')
        # testresult.append(["\xa0" + descr, verdict])
        # time.sleep(1)
        testresult.append(["[.] Setze VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
        descr, verdict = func_gs.setVelocity_kmph(0)
        testresult.append(["\xa0" + descr, verdict])

        testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
        hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

        testresult.append(["[.] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 0 (VPE_NONE)", ""])
        hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
        testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 4 (RUNNING)", ""])
        hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
        testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 4 (RUNNING)", ""])
        hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
        testresult.append(["[.] Warte 2 Sekunde", ""])
        time.sleep(2)
        canape_diag = testenv.getCanapeDiagnostic()
        testresult.append(["[.] Tester Present deaktivieren", ""])
        canape_diag.disableTesterPresent()
        testresult.append(["[-0]", ""])

        # TEST PROCESS ############################################################
        testresult.append(["\n Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
        testresult.append(["[-0]", ""])

        testresult.append(["[.] SW-Flashtool starten:  vFlash Software Pfade anrufen.", ""])
        flash_file_path = r"C:\Users\DEENLAB01\Desktop\SW0111\vFlash\Project1.vflash"
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
        hil.vbat_cl30__V.set(6.0)

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
        testenv.breakdown(ecu_shutdown=False)
        print('done')

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
    testenv.breakdown(ecu_shutdown=False)
    print('done')

