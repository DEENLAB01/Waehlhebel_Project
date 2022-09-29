# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : ORUnext_Flashing_vFlash.py
# Title   : ORUnext_Flashing_vFlash
# Task    : ORUnext Flashing mit vFlash Tools
#
# Author  : Mohammed Abdul Karim
# Date    : 25.04.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 23.02.2022 | Mohammed | initial
# 1.2  | 12.05.2022 | Mohammed  | Added Testschritte
# 1.3  | 22.07.2022 | Mohammed  | Added Raumtemperatur zwischen -40 to 90 Grad
# ******************************************************************************

# ******************************************************************************


from _automation_wrapper_ import TestEnv  # @UnresolvedImport
from ttk_tools.vector.vflash_api import VFlashAPI
import ttk_tools.vector.vflash_api as vflash_api
import time
from ttk_checks import basic_tests
import functions_gearselection
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
    flash_file_path = r"C:\Users\DEENLAB01\Desktop\SW0111\OTA_Prod\Project1.vflash" # must be OTA CANID via vFlash
    vflash_dll_path = r'C:\Program Files (x86)\Vector vFlash 7\Bin\VFlashAutomation.dll'
    activate_network = False
    flash_timeout = 2000
    vf = VFlashAPI(vflash_dll_path)

    print "# vFlash Automation: "
    print "    vflash dll path: %s" % (vf.dll_path)
    print "    flash file path: %s" % (flash_file_path)

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_307")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    #hil.cl30_on__.set(1)
    #hil.cl15_on__.set(0)
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present und Warte 100ms", ""])
    canape_diag.disableTesterPresent()
    time.sleep(.1)

    Physical_ID = 0x1C400253
    response_CAN_ID = 0x1C420253
    Functional_req_CAN_ID = 0x1C410200

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Setze in Vflash: Physical_ID = 0x1C400253, Response_CAN_ID = 0x1C420253 und Functional_req_CAN_ID = 0x1C410200 ", ""])
    testresult.append(["Setze vFlash Tool --> Configure --> Communication: Physical CAN ID = %s , Response CAN ID = %s, Functional Request CAN ID = %s" %(Physical_ID,response_CAN_ID, Functional_req_CAN_ID), "INFO"])

    # test step 2
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    #testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 3
    testresult.append(["[.] Setze OBD_Driving_Cycle auf 1", ""])
    hil.OBD_03__OBD_Driving_Cycle__value.set(1)

    # test step 4-4.5
    testresult.append(["[.] Setze gulitige Precondition für ORUnext Flashing", ""])
    testresult.append(["[+] Setze Kein CRC und BZ Error", ""])
    testresult.append(["[.] Setze Kein E2E Timeout", ""])
    testresult.append(["[.] Setze VDSO_Vx3d auf (+/-5 km/h)", ""])
    testresult.append(func_gs.setVelocity_kmph(0))
    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))
    testresult.append(["[.] Setze PropulsionSystemActive_switch = 0", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append(["[.] Setze OTAMC_D_01 auf VPE_None", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze ORU_CONTROL_A auf RUNNING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_CONTROL_D auf  RUNNING ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    testresult.append(["[-0]", ""])

    # test step 5
    tMSG_CYCLE = 0.5  # sec
    testresult.append(["[.] Warte tMSG_CYCLE: 500ms ", ""])
    time.sleep(tMSG_CYCLE)

    # test step 6-6.2
    testresult.append(["[.] Auslesen DID: 0xF1F2 (KL30 Signal Read)", ""])
    request = [0x22] + [0xF1, 0xF2]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["[+] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Prüfe Voltage : 13-16 V", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.vbat_cl30__V.get(),  # letzer Sendetimestamp
            min_value=6.0,
            max_value=16.0,
            descr="Check that value is in range"
        )
    )
    testresult.append(["[-0]", ""])

    # test step 7-7.2
    testresult.append(["[.] Auslesen DID: 0xF1F3 (Temeprature Sensor Read)", ""])
    request = [0x22] + [0xF1, 0xF3]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["[+] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Prüfe Raumtemperatur zwischen -40 to 90 Grad", ""])
    if len(response) > 3:
        data = response[3:]  # just take data of complete response
        temp_value_dec = 0
        i = len(response) - 3 - 1
        for temp_value in data:
            temp_value_dec += temp_value << (i * 8)  # set all bytes together
            i -= 1

        testresult.append(["Empfangene Daten (Rohwert): {}\nEntspricht dem Temeprature Sensor Wert : {} Grad"
                          .format(str(HexList(data)), temp_value_dec),
                           "INFO"])
        testresult.append(basic_tests.checkRange(temp_value_dec, 0, 0x5A))

    else:
        testresult.append(["Keine Auswertung möglich, da falsche oder keine Response empfangen wurde!", "FAILED"])
    testresult.append(["[-0]", ""])

    # test step 8-8.3
    testresult.append(["[.] SW-Flashing starten:vFlash Software Pfade anrufen.", ""])
    try:
        vf.flash(flash_file_path, testresult, activate_network, flash_timeout)
        testresult.append(["\x0a ORUnext Flashing: SW0111 Erfolgreich", "PASSED"])
    except vflash_api.VFlashResultError, ex:
        testresult.append(["ORUnext Flashing: SW0111 nicht Erfolgreich %s" % ex, "FAILED"])

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