# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : flashing_via_vflash.py
# Task    : flasing of software via Vflash
#
# Author  : Mohammed Abdul Karim
# Date    : 24.11.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 20.11.2021 | Mohammed  | initial

# ******************************************************************************

from _automation_wrapper_ import TestEnv
import time
from ttk_tools.vector.vflash_api import VFlashAPI
import ttk_tools.vector.vflash_api as vflash_api


import functions_nm
import functions_gearselection

# Instantiate test environment
testenv = TestEnv()
odx_file_path    = r'C:\Users\DEENLAB01\Desktop\SW 0064\OTA\FL_95C713041_0064_H02WAEHLHEBEL_V001_E.pdx'
flash_file_path = r"C:\Users\DEENLAB01\Desktop\SW 0064\OTA\MP_EGA_PM_SCHALTBETAETIGUNG.vflash"
vflash_dll_path  = r'C:\Program Files (x86)\Vector vFlash 7\Bin\VFlashAutomation.dll'

try:
    # #########################################################################

    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    vf = VFlashAPI(vflash_dll_path)

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_282")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    time.sleep(5)

    Physical_ID = 0x1C400253
    response_CAN_ID= 0x1C420253
    Functional_req_CAN_ID = 0x1C410200

    testresult.append(["SETTING IS Physical_ID = %s , response_CAN_ID = %s, Functional_req_CAN_ID = %s" %(Physical_ID,response_CAN_ID, Functional_req_CAN_ID), "INFO"])

    testresult.append(["\x0a Setze die Precondition", ""])
    testresult.append(["\x0a Schalte KL15 aus (=0)", ""])
    #
    hil.cl15_on__.set(0)
    # testresult.append(["\x0a Waehlhebelposition P aktiviert", ""])
    # descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\x0a OTAMC_D_01 setze auf VPE_PRODUCTION", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["\x0a ORU_CONTROL_A setze auf  RUNNING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlOldA__value.set(2)
    testresult.append(["\x0a ORU_CONTROL_D setze auf RUNNING ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlOldD__value.set(2)
    time.sleep(2)

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


finally:
    # #########################################################################
    testenv.shutdownECU()
    testenv.breakdown()
    # #########################################################################