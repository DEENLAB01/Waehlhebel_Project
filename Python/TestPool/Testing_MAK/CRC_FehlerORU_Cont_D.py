#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CRC_Fehler_ORU_Control_D.py
# Title   : CRC_Fehler_ORU_Control_D
# Task    : ORU_Control_D Fehlererkennung für CRC-Fehler und Ablage im Fehlerspeicher
#
# Author  : Mohammed Abdul Karim
# Date    : 19.05.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 19.05.2022  | Mohammed | initial
# 1.1  | 12.07.2022  | Mohammed | 3 OP-PowerCycle
#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()

# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
from ttk_checks import basic_tests
import functions_gearselection
import time
from time import time as t

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    period_var = hil.ORU_Control_D_01__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 15000  # CAN_3244

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_193")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: LK30 und Kl15 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[.] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["[.] Auslesen Raumtemperatur DID: 0xF1F3 (Temeprature Sensor Read)", ""])
    res, verdict = canape_diag.sendDiagRequest([0x22, 0xF1, 0xF3])
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Raumtemperatur zwischen -40 to 90 Grad = %s degree" % (int(hex(res[3]), 16)), ""])
    testresult.append(["[.] Prüfe Betriebsspannung : 6-16 V", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.vbat_cl30__V.get(),  # letzer Sendetimestamp
            min_value=6.0,
            max_value=16.0,
            descr="Check that value is in range"
        )
    )
    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    #testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Setze Zykluszeit der Botschaft ORU_Control_D_01 auf 320ms (gültig)", ""])
    #period_var.set(max_valid_cycletime)

    # test step 2
    testresult.append(["[.] Warte 1000 ms", ""])
    time.sleep(1.0)

    # test step 3
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 4
    testresult.append(["[.] Sende CRC-Fehler für ORU_Control_D_01::ORU_Control_D_01_CRC", ""])
    sec = 0.320
    timeout = sec + t()
    while timeout > t():
        hil.ORU_Control_D_01__ORU_Control_D_01_CRC__value.set(1)

    # test step 5
    testresult.append(["[.] Warte 3190ms ms (tMSG_CYCLE + Toleranz)", ""])
    time.sleep(3.190)

    # test step 6
    testresult.append(["[.] Lese Fehlerspeicher (0xE0010E DTC aktiv)", ""])
    active_dtcs = [(0xE0010E, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs))

    # test step 7-7.8
    testresult.append(["[.] Initiiere OTA-ORUnext-Flashprozess", ""])
    testresult.append(["[+] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 0 (VPE_none)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 4 (RUNNING)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 4 (RUNNING)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    tMSG_CYCLE = 0.5  # sec
    testresult.append(["[.] Warte tMSG_CYCLE: 500ms ", ""])
    time.sleep(tMSG_CYCLE)

    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)

    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))
    testresult.append(["[-0]", ""])

    # test step 8
    testresult.append(["[.] Nimm CRC-Fehler zurück für ORU_Control_D_01::ORU_Control_D_01_CRC ", ""])

    # test step 9
    testresult.append(["[.] Warte 1000 ms (2x tMSG_CYCLE + Toleranz)", ""])
    time.sleep(1.0)

    # test step 10
    testresult.append(["[.] Lese Fehlerspeicher (0xE0010D DTC aktiv)", ""])
    active_dtcs = [(0xE0010E, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs))

    # test step 11-11.8
    testresult.append(["[.] Initiiere OTA-ORUnext-Flashprozess", ""])
    testresult.append(["[+] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 0 (VPE_none)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 4 (RUNNING)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 4 (RUNNING)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    tMSG_CYCLE = 0.5  # sec
    testresult.append(["[.] Warte tMSG_CYCLE: 500ms ", ""])
    time.sleep(tMSG_CYCLE)

    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)

    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))
    testresult.append(["[-0]", ""])

    # test step 12
    testresult.append(["[.] Setze Kl30 aus und warte 500 ms", ""])
    hil.cl30_on__.set(0)
    # hil.cl15_on__.set(0)
    time.sleep(0.500)

    testresult.append(["[.] Setze Kl30 ein und warte 500 ms", ""])
    hil.cl30_on__.set(1)
    # hil.cl15_on__.set(1)
    time.sleep(0.500)

    # test step 13
    testresult.append(["[.] Lese Fehlerspeicher (0xE0010D DTC passiv)", ""])
    passiv_dtcs = [(0xE0010E, 0x26)]
    testresult.append(canape_diag.checkEventMemory(passiv_dtcs, ticket_id='FehlerId:EGA-PRM-248'))

    # test step 14
    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # test step 15
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1)

    # test step 16
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[.] Bus Reset", ""])
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(0.5)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    cal = None
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()

