# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : RPC_PLUS_Production_Flashing.py
# Title   : OTA RPC_PLUS Flasing Production
# Task    : RPC PLUS Production Flashing via vFlash
#
# Author  : Mohammed Abdul Karim
# Date    : 12.04.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 12.04.2022 | Mohammed | initial
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
    flash_file_path = r"C:\Users\DEENLAB01\Desktop\SW0085\OTA\MP_EGA_PM_SCHALTBETAETIGUNG.vflash"
    vflash_dll_path = r'C:\Program Files (x86)\Vector vFlash 7\Bin\VFlashAutomation.dll'
    activate_network = False
    flash_timeout = 2000
    vf = VFlashAPI(vflash_dll_path)

    print "# vFlash Automation: "
    print "    vflash dll path: %s" % (vf.dll_path)
    print "    flash file path: %s" % (flash_file_path)

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_XXL")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: Kl30 ein", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    time.sleep(.1)
    testresult.append(["[.] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    testresult.append(["\x0a vFlash Aufbau:Physical_ID = 0x1C400253, response_CAN_ID = 0x1C420253 und Functional_req_CAN_ID = 0x1C410200 ", ""])
    Physical_ID = 0x1C400253
    response_CAN_ID = 0x1C420253
    Functional_req_CAN_ID = 0x1C410200

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    # Test step 1
    testresult.append(["\x0a Prüfe Spannungsbereich 6V- 16V ", ""])
    testresult.append(["Supply Voltage = %s " % hil.cv_mon__V.get(), "INFO"])

    # Test step 2, 2.1
    testresult.append(["\x0a Prüfe Temeprature zwischen -40 to 90 Grad ", ""])
    res, verdict = canape_diag.sendDiagRequest([0x22, 0xF1, 0xF3])
    testresult.append(["Current Temperature = %s degree" % (int(hex(res[3]), 16)), "INFO"])

    # Test step 3, 3.1, 3.2, 3.3
    testresult.append(["[-] Setze Kein CRC, BZ und Timeout Error", ""])
    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(["[+0]", ""])

    # Test step 4, 4.1
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # Test step 5
    testresult.append(["\x0a5. Gültige Signal for Production Flashen:", ""])
    testresult.append(["\x0a OTAMC_D_01 setze auf VPE_PRODUCTION", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["\x0a ORU_CONTROL_A setze auf IDLE ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["\x0a ORU_CONTROL_D setze auf  IDLE ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)
    time.sleep(2)

    testresult.append(["\x0a OBD_03::OBD_Driving_Cycle_set_once = 1 senden", ""])
    hil.OBD_03__OBD_Driving_Cycle__value.set(1)

    # Test step 6
    obd_cycle= [0x01]
    request = [0x22, 0x02, 0x61]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response[3:], obd_cycle ))

    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # Test step 7,
    print "# vFlash Automation: Flash Progress:"
    try:
        vf.flash(flash_file_path, testresult, activate_network, flash_timeout)
        testresult.append(["\x0aVflash: SW0085 is sucessful", "PASSED"])
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