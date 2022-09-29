# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : STANDALONE_ACTIVE_Mode_2.py
# Title   : flasing of software via Vflash
# Task    : Set KL30 overvoltage error 
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

import time
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
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################


    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_284")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    time.sleep(5)

    Physical_ID = 0x1C400253
    response_CAN_ID= 0x1C420253
    Functional_req_CAN_ID = 0x1C410200
    
    
    
    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])
    
    testresult.append(["SETTING IS Physical_ID = %s , response_CAN_ID = %s, Functional_req_CAN_ID = %s" %(Physical_ID,response_CAN_ID, Functional_req_CAN_ID), "INFO"])

    testresult.append(["[-] voltage check with DID F1F2 " , "INFO"])
    res, verdict = canape_diag.sendDiagRequest([0x22, 0xF1, 0xF2])
    testresult.append(["raw output from DID F1F2 %s -" % (res), "INFO"])
    testresult.append(["voltage = %s mV -" %(int(hex((res[3] << 8) | res[4]), 16)), "PASSED"])
    time.sleep(.05)
    
    request_Standalone_Modes_2 = [0x22, 0xC1, 0x11]
    testresult.append(["[-] read Standalone_Modes_2 " , "INFO"])
    response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_2)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_Standalone_Modes_2))
    
    testresult.append(["\x0a OTAMC_D_01 setze auf VPE_none", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    time.sleep(1)
    
    testresult.append(["[.] VDSO_Vx3d = 0 km/h" , ""])
    testresult.append(func_gs.setVelocity_kmph(0))
    time.sleep(2.1) 
   
    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(["[+0]", ""])
    testresult.append(canape_diag.resetEventMemory())
    testresult.append(canape_diag.checkEventMemoryEmpty())
    
    testresult.append(["\x0a ORU_CONTROL_A setze auf  RUNNING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(2)
    testresult.append(["\x0a ORU_CONTROL_D setze auf RUNNING ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(2)
    time.sleep(2)
    
    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))
    
    testresult.append(["\x0a PropulsionSystemActive_switch = 0", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    
    testresult.append(["\x0a set ClampControl_01__KST_KL_15__value 0 ", ""])
    hil.ClampControl_01__KST_KL_15__value.set(0)
    time.sleep(.05)
    
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    testresult.append(["[.] Security Access aktivieren", ""])

    testresult.append(["[+] Seed anfragen: 0x2711", ""])
    seed, result = canape_diag.requestSeed(special=True)
    testresult.extend(result)

    testresult.append(["[.] Key berechnen: <key 1>", ""])
    key, result = canape_diag.calculateKey(seed)
    testresult.extend(result)

    testresult.append(["[.] Key senden: 0x2712 + <key 1>", ""])
    verdict = canape_diag.sendKey(key)
    testresult.extend(verdict)
    
    write_standalone_modes_1 = [ 0x2E, 0xC1, 0x10, 0xBD, 0xDB, 0x6B, 0x3A]
    testresult.append(["[-] read Standalone_Modes_2 " , "INFO"])
    response, verdict = canape_diag.sendDiagRequest(write_standalone_modes_1)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, write_standalone_modes_1))
    
    testresult.append(["[.] Wechsel in default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))
    
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    request_programming = [0x10, 0x03]
    testresult.append(["\xa0Versuchen, in 'Extended session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_programming))
    
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x7E))
    
    write_standalone_modes_1 = [ 0x2E, 0xC1, 0x10, 0xBD, 0xDB, 0x6B, 0x3A]
    testresult.append(["[-] read Standalone_Modes_2 " , "INFO"])
    response, verdict = canape_diag.sendDiagRequest(write_standalone_modes_1)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, write_standalone_modes_1))
    
    write_standalone_modes_2 = [ 0x2E, 0xC1, 0x11, 0x42, 0x24, 0x94, 0xC5]
    testresult.append(["[-] read Standalone_Modes_2 " , "INFO"])
    response, verdict = canape_diag.sendDiagRequest(write_standalone_modes_1)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, write_standalone_modes_1))
    
    request_Standalone_Modes_2 = [0x22, 0xC1, 0x01]
    testresult.append(["[-] read Standalone-Mode Status " , "INFO"])
    response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_2)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_Standalone_Modes_2))

    request_Standalone_Modes_1 = [0x22, 0xC1, 0x10]
    testresult.append(["[-] read Standalone_Modes_1 " , "INFO"])
    response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_1)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_Standalone_Modes_1))
    
    request_Standalone_Modes_2 = [0x22, 0xC1, 0x11]
    testresult.append(["[-] read Standalone_Modes_2 " , "INFO"])
    response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_2)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_Standalone_Modes_2))
    
    testresult.append(["\x0a1.Flashing ist moglich", ""])
    
    testresult.append(["[.] Wechsel in default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))
    
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    request_programming = [0x10, 0x03]
    testresult.append(["\xa0Versuchen, in 'Extended session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_programming))
    
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_programming))

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