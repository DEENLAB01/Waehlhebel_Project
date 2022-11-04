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
    testresult.setTestcaseId("TestSpec_380")

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
    testresult.append(["[-0]", ""])

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # test step 1
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186 ", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 2
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 3
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    # test step 4
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 5
    testresult.append(["[.] Security Access aktivieren", ""])

    # test step 5.1
    testresult.append(["[+]Seed anfragen: 0x2761", ""])
    seed, result = canape_diag.requestSeed()
    testresult.extend(result)

    # test step 5.2
    testresult.append(["[.] Key berechnen: <key 1>", ""])
    key, result = canape_diag.calculateKey(seed)
    testresult.extend(result)

    # test step 5.3
    testresult.append(["[.] Key senden: 0x2762 + <key 1>", ""])
    verdict = canape_diag.sendKey(key)
    testresult.extend(verdict)
    testresult.append(["[-0]", ""])

    # test step 6
    obd_driving_cycle = [0x00]
    request = [0x2E, 0x02, 0x61]
    testresult.append(["[.] Schreibe OBD_Driving_Cycle: 0x{} + 0x{}"
                      .format("".join("{:02X}".format(x) for x in request),
                              "".join("{:02X}".format(x) for x in obd_driving_cycle)),
                       ""])
    response, result = canape_diag.sendDiagRequest(request + obd_driving_cycle)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, ticket_id='FehlerId:EGA-PRM-236'))

    # test step 7
    testresult.append(["[.] Diagnose Request schicken: 0x220261", ""])
    testresult.append([" Prüfe Inhalt: 0x{}"
                      .format(" ".join("{:02X}".format(x) for x in obd_driving_cycle)),
                       ""])
    request = [0x22, 0x02, 0x61]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response[3:], obd_driving_cycle, ticket_id='FehlerId:EGA-PRM-236'))

    # test step 8
    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkResponse(response, [0x62, 0x02, 0x61, 0x00], ticket_id='FehlerId:EGA-PRM-236'))

    # test step 9
    testresult.append(["[.] Auslesen der Programmzugriffe: 0x220407 und abspeichern (vor dem Flashen)", ""])
    request = [0x22] + [0x04, 0x07]
    response2, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\x0a Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response2, request, ticket_id='FehlerId:EGA-PRM-236'))

    testresult.append(["\x0aAuslesen der Programmzugriffe: 0x220407 (nach dem Flashen)", ""])
    testresult.append(canape_diag.checkResponse(response2[0:6], [0x62, 0x04, 0x07, 0x00, 0x01, 0x00], ticket_id='FehlerId:EGA-PRM-236'))

    # test step 10 -10.3
    testresult.append(["[.] vFlash Software Pfade anrufen.", ""])
    flash_file_path = r"C:\Users\DEENLAB01\Desktop\Software_version\SW0112\Vflash_Project\Production_Key\ISO\Project1.vflash" ### must be vFlash path with ISO CAN ID
    vflash_dll_path = r'C:\Program Files (x86)\Vector vFlash 7\Bin\VFlashAutomation.dll'
    activate_network = False

    testresult.append(["[+] Setze Flash Timeout 2000 Sekunden", ""])
    flash_timeout = 2000
    vf = VFlashAPI(vflash_dll_path)

    print ("# vFlash Automation: ")
    print ("    vflash dll path: %s" % (vf.dll_path))
    print ("    flash file path: %s" % (flash_file_path))

    print ("# vFlash Automation: Flash Progress:")

    try:
        vf.flash(flash_file_path, testresult, activate_network, flash_timeout)
        testresult.append(["\x0aPrüfe Vflash: SW 0112 Flashen Erfolgerich", "PASSED"])
    except vflash_api.VFlashResultError, ex:
        testresult.append(["\x0a Vflash: SW 0112 Flashen Erfolgerich nicht Erfolgerich %s" % ex, "FAILED"])
    testresult.append(["[-0]", ""])

    # test step 11
    testresult.append(["[.] VW Application Software Version auslesen: 0x22F189", ""])
    request = [0x22] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step
    testresult.append(["\x0a Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, ticket_id='FehlerId:EGA-PRM-236'))

    # test step
    testresult.append(["\x0aInhalt der Response überprüfen: aktuelle SW Version> = <exp_version>", ""])
    testresult.append(canape_diag.checkResponse(response, [0x62, 0xF1, 0x89, 0x30, 0x31, 0x31, 0x32], ticket_id='FehlerId:EGA-PRM-236'))  ########### added

    # test step 12
    testresult.append(["[.] Auslesen der Programmzugriffe: 0x220407 und abspeichern (vor dem Flashen)", ""])
    request = [0x22] + [0x04, 0x07]
    response1, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\x0a Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response1, request))

    testresult.append(["\x0aAuslesen der Programmzugriffe: 0x220407 (nach dem Flashen)", ""])
    testresult.append(canape_diag.checkResponse(response1[0:6], [0x62, 0x04, 0x07, 0x00, 0x01, 0x00], ticket_id='FehlerId:EGA-PRM-236'))  ########### added

    # test step 13
    testresult.append(["[.] Vergleichen prg_counts und prg_counts_new (vor dem Flashen und nach dem Flashen) ", ""])
    if response1[0:5]==response2[0:5]:
        if response1[6] == response2[6]+1:
            testresult.append(["\xa0 Programmzugriff wurde um 1 erhöht nach dem erfolgreichen Flashvorgang", "PASSED"])
        else:
            testresult.append(["\xa0 Programmzugriff wurde um 1 erhöht nach dem erfolgreichen Flashvorgang", "FAILED"])
    else:
        testresult.append(["\xa0 failed because the first 5 bytes are not same", "FAILED"])
        testresult.append(["%s response 1, %s response in 2"%(response2[0:5], response1[0:5])])

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

