# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Standalone_Flashing_Auto.py
# Title   : Automatic Standalone Flashing vFlash
# Task    : Automatic Standalone Flashing vFlash
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


from _automation_wrapper_ import TestEnv  # @UnresolvedImport
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
    flash_file_path = r"C:\Users\DEENLAB01\Desktop\SW1X86\OTA\MP_EGA_PM_SCHALTBETAETIGUNG.vflash"
    vflash_dll_path = r'C:\Program Files (x86)\Vector vFlash 7\Bin\VFlashAutomation.dll'
    activate_network = False
    flash_timeout = 2000
    vf = VFlashAPI(vflash_dll_path)

    request_defined_1 = [0x2E, 0xC1, 0x10, 0xBD, 0xDB, 0x6B, 0x3A]
    res_defined_1 = [0x62, 0xC1, 0x10, 0xBD, 0xDB, 0x6B, 0x3A]
    request_defined_2 = [0x2E, 0xC1, 0x11, 0x42, 0x24, 0x94, 0xC5]
    res_defined_2 = [0x62, 0xC1, 0x11, 0x42, 0x24, 0x94, 0xC5]
    request_undefined_1 = [0x62, 0xC1, 0x10, 0x00, 0x00, 0x00, 0x00]
    request_undefined_2 = [0x62, 0xC1, 0x11, 0x00, 0x00, 0x00, 0x00]
    expected_response_1 = [0x6E, 0xC1, 0x10]
    expected_response_2 = [0x6E, 0xC1, 0x11]
    request_Standalone_Modes_status_1 = [0x22, 0xC1, 0x10]
    request_Standalone_Modes_status_2 = [0x22, 0xC1, 0x11]
    request_Standalone_Modes_status = [0x22, 0xC1, 0x01]
    expected_Standalone_Modes_status = [0x62, 0xC1, 0x01, 0x01]

    print "# vFlash Automation: "
    print "    vflash dll path: %s" % (vf.dll_path)
    print "    flash file path: %s" % (flash_file_path)
    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_XXy")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    time.sleep(.1)

    Physical_ID = 0x1C400253
    response_CAN_ID = 0x1C420253
    Functional_req_CAN_ID = 0x1C410200

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(["[+0]", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["\x0a1. Setze Precondition", ""])
    testresult.append(["\x0a Set all E2E Messages Timeout", ""])
    hil.SiShift_01__period.setState("aus")
    hil.ORU_Control_A_01__period.setState("aus")
    hil.ORU_Control_D_01__period.setState("aus")
    hil.ORU_01__period.setState("aus")
    hil.OTAMC_D_01__period.setState("aus")
    hil.VDSO_05__period.setState("aus")
    time.sleep(5.1)

    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    testresult.append(["[.] Security Access aktivieren", ""])

    testresult.append(["[+] Seed anfragen: 0x2711", ""])
    seed, result = canape_diag.requestSeed()
    testresult.extend(result)

    testresult.append(["[.] Key berechnen: <key 1>", ""])
    key, result = canape_diag.calculateKey(seed)
    testresult.extend(result)

    testresult.append(["[.] Key senden: 0x2712 + <key 1>", ""])
    verdict = canape_diag.sendKey(key)
    testresult.extend(verdict)
    testresult.append(["[-0]", ""])

    testresult.append(["[.] write Standalone_Modes_1: %s " % request_defined_1, ""])
    response, verdict = canape_diag.sendDiagRequest(request_defined_1)
    testresult.append(verdict)
    testresult.append(canape_diag.checkResponse(response, expected_response_1))

    testresult.append(["[.] read Standalone_Modes_1 Status ", ""])
    response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_status_1)
    testresult.append(verdict)
    testresult.append(canape_diag.checkResponse(response, res_defined_1))

    testresult.append(["[.] write Standalone_Modes_2: %s " % request_defined_2, ""])
    response, verdict = canape_diag.sendDiagRequest(request_defined_2)
    testresult.append(verdict)
    testresult.append(canape_diag.checkResponse(response, expected_response_2))

    testresult.append(["[.] read Standalone_Modes Status ", ""])
    response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_status)
    testresult.append(verdict)
    testresult.append(canape_diag.checkResponse(response, expected_Standalone_Modes_status))
    testresult.append(verdict)

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