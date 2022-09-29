# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : ORUnext_Flashing_vFlash.py
# Title   : Automatic ORUnext Flashing vFlash
# Task    : Automatic ORUnext Flashing vFlash
#           
# Author  : M.A. Mushtaq
# Date    : 23.02.2022
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 23.02.2022 | M.A. Mushtaq | initial
# ******************************************************************************

# ******************************************************************************


from _automation_wrapper_ import TestEnv # @UnresolvedImport
from ttk_tools.vector.vflash_api import VFlashAPI
import ttk_tools.vector.vflash_api as vflash_api
import time


# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################

    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    flash_file_path = r"C:\Users\DEENLAB01\Desktop\SW0085\OTA\MP_EGA_PM_SCHALTBETAETIGUNG.vflash"
    vflash_dll_path = r'C:\Program Files (x86)\Vector vFlash 7\Bin\VFlashAutomation.dll'
    activate_network = False
    flash_timeout = 2000
    vf = VFlashAPI(vflash_dll_path)

    print "# vFlash Automation: "
    print "    vflash dll path: %s" % (vf.dll_path)
    print "    flash file path: %s" % (flash_file_path)
    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_XXz")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    time.sleep(.1)

    Physical_ID = 0x1C400253
    response_CAN_ID= 0x1C420253
    Functional_req_CAN_ID = 0x1C410200
    
    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(["[+0]", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["\x0a1. Setze Precondition", ""])

    testresult.append(["\x0a OTAMC_D_01 setze auf VPE_none", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    #testresult.append(["\x0a ORU_CONTROL_A setze auf  PREPARATION ", ""])
    #hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(2)
    #hil.ORU_Control_A_01__OnlineRemoteUpdateControlOldA__value.set(2)
    #testresult.append(["\x0a ORU_CONTROL_D setze auf PREPARATION ", ""])
    #hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(2)
    #hil.ORU_Control_D_01__OnlineRemoteUpdateControlOldD__value.set(2)
    #time.sleep(2)
    testresult.append(["\x0a ORU_CONTROL_A setze auf  RUNNING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlOldA__value.set(4)
    testresult.append(["\x0a ORU_CONTROL_D setze auf RUNNING ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlOldD__value.set(4)
    time.sleep(0.50)

    print "# vFlash Automation: Flash Progress:"
    try:
        vf.flash(flash_file_path, testresult, activate_network, flash_timeout)
        testresult.append(["Vflash: SW0080 is sucessful", "PASSED"])
    except vflash_api.VFlashResultError, ex:
        testresult.append(["Vflash Result: %s" % ex, "FAILED"])
    
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