# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : RPC_PLUS_AfterSales_Flashing_vFlash.py
# Title   : Flasing of software via vFlash
# Task    : Automatic RPC PLUS AfterSales Flashing vFlash
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
import functions_gearselection


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
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

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
    testresult.setTestcaseId("TestSpec_291")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    #testenv.startupECU()
    hil.cl30_on__.set(1)
    hil.cl15_on__.set(0)
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present und Warte 100ms", ""])
    canape_diag.disableTesterPresent()
    time.sleep(.1)

    Physical_ID = 0x1C400253
    response_CAN_ID= 0x1C420253
    Functional_req_CAN_ID = 0x1C410200
    
    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["[.] Setze in Vflash: Physical_ID = 0x1C400253, response_CAN_ID = 0x1C420253 und Functional_req_CAN_ID = 0x1C410200 ",""])
    testresult.append(["SETTING IS Physical_ID = %s , response_CAN_ID = %s, Functional_req_CAN_ID = %s" % (Physical_ID, response_CAN_ID, Functional_req_CAN_ID), "INFO"])

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    #testresult.append(["[+0]", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["[.] Setze gulitige Precondition für RPCplus AfterSales Flashing", ""])
    testresult.append(["\x0a Setze Kein CRC und BZ Error", ""])
    testresult.append(["\x0a Setze Kein E2E Timeout", ""])
    testresult.append(["\x0a Setze VDSO_Vx3d auf (+/-5 km/h)", ""])
    testresult.append(func_gs.setVelocity_kmph(0))

    testresult.append(["\x0a Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))

    testresult.append(["\x0a PropulsionSystemActive_switch = 0", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append(["\x0a OTAMC_D_01 setze auf VPE_AfterSales", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(2)
    testresult.append(["\x0a ORU_CONTROL_A setze auf IDLE ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["\x0a ORU_CONTROL_D setze auf  IDLE ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)

    tMSG_CYCLE = 0.5  # sec
    testresult.append(["[.] Warte tMSG_CYCLE: 500ms ", ""])
    time.sleep(tMSG_CYCLE)

    testresult.append(["[.] Auslesen DID: 0xF1F2 (KL30 Signal Read)", ""])
    res, verdict = canape_diag.sendDiagRequest([0x22, 0xF1, 0xF2])
    testresult.append(["\xa0 raw output from DID F1F2 %s -" % (res), ""])
    testresult.append(["\xa0 voltage = %s mV -" % (int(hex((res[3] << 8) | res[4]), 16)), "PASSED"])

    testresult.append(["[.] Auslesen DID: 0xF1F3 (Temeprature Sensor Read) zwischen -40 to 90 Grad ", ""])
    res, verdict = canape_diag.sendDiagRequest([0x22, 0xF1, 0xF3])
    testresult.append(["\xa0 Prüfe Temeprature zwischen -40 to 90 Grad = %s degree" % (int(hex(res[3]), 16)), "INFO"])

    testresult.append(["[.] SW-Flashing starten", ""])
    print "# vFlash Automation: Flash Progress:"
    try:
        vf.flash(flash_file_path, testresult, activate_network, flash_timeout)
        testresult.append(["\x0a RPCplus AfterSales Flashing: SW0085 Erfolgreich", "PASSED"])
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