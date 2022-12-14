#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Bz_Fehler_ORU_Control_A.py
# Title   : Bz_Fehler_ORU_Control_A
# Task    : Fehlererkennung f?r BZ-Fehler ORU_Control_A und Ablage im Fehlerspeicher

# Author  : Mohammed Abdul Karim
# Date    : 16.05.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 16.05.2022 | Mohammed | initial created Timeout Test
# 1.1  | 19.05.2022 | Mohammed | Rework
# 1.2  | 10.06.2022 | Mohammed | TestSpec Aktualisiert
# 1.3  | 29.06.2022 | Mohammed | tMSG_Botschaftsz?hlers Aktualisiert
# 1.4  | 28.07.2022 | Mohammed | Added TestStep 11.9 and 11.10
# 1.5  | 15.08.2022 | Mohammed | Added Tollerenz
# 1.6  | 02.11.2022 | Devangbhai | Added 3 cycle wait in test step 9

#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()
import functions_gearselection
# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
from ttk_checks import basic_tests
from functions_diag import HexList  # @UnresolvedImport
import time

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()

    # Initialize variables ####################################################
    period_var = hil.ORU_Control_A_01__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 1500
    activ_dtcs = [(0xE0010A, 0x27)]
    passive_dtcs = [(0xE0010A, 0x26)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_228")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: LK30 und Kl15 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[.] Pr?fe, dass Fehler l?schbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[.] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["[.] Pr?fe Raumtemperatur zwischen -40 to 90 Grad", ""])
    request = [0x22] + [0xF1, 0xF3]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    # testresult.append(["[+] Auf positive Response ?berpr?fen", ""])
    # testresult.append(canape_diag.checkPositiveResponse(response, request))
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
        testresult.append(["Keine Auswertung m?glich, da falsche oder keine Response empfangen wurde!", "FAILED"])

    testresult.append(["[.] Pr?fe Betriebsspannung : 6-16 V", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.vbat_cl30__V.get(),  # letzer Sendetimestamp
            min_value=6.0,
            max_value=16.0,
            descr="Check that value is in range"
        )
    )

    testresult.append(["[.] Waehlhebelposition P aktiviert ", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze PropulsionSystemActive_switch = 0", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    # test step 1
    testresult.append(["[.] Setze Zykluszeit der Botschaft ORU_Control_A_01 auf 500ms " ""])
    testresult.append(["\xa0 Setze Zykluszeit auf %sms" % cycle_time, ""])
    period_var.set(cycle_time)

    # test step 2
    testresult.append(["[.] Warte 1500 ms", ""])
    time.sleep(1.50)

    # test step 3
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 4
    testresult.append(["[.] Halte ORU_Control_A_01:ORU_Control_A_01_BZ an (Setze Inkrementierung des Botschaftsz?hlers aus)", ""])
    hil.ORU_Control_A_01__ORU_Control_A_01_BZ__switch.set(1)

    # test step 5
    testresult.append(["[.] Warte 4500 ms (tMSG_Timeout: n-q+1, n=10, q=2) + 420ms (Tollerenz)", ""])
    time.sleep(4.92)

    # test step 6
    testresult.append(["[.] Lese Fehlerspeicher (0xE0010A DTC activ)", ""])
    testresult.append(canape_diag.checkEventMemory(activ_dtcs, ticket_id='FehlerId:EGA-PRM-234'))

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

    testresult.append(["\xa0Auf negative Response ?berpr?fen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))
    testresult.append(["[-0]", ""])

    # test step 8
    testresult.append(["[.] Setze ORU_Control_A_01:ORU_Control_A_01_BZ wieder fort)", ""])
    hil.ORU_Control_A_01__ORU_Control_A_01_BZ__switch.set(0)

    # test step 9
    testresult.append(["[.] Warte 4000 ms (tMSG_Timeout: 3+n/2, n=10, q=2) + 500ms (Tollerenz)", ""])
    time.sleep(4 + 0.420)

    # test step 10
    testresult.append(["[.] Lese Fehlerspeicher (0xE0010A DTC passiv)", ""])
    testresult.append(canape_diag.checkEventMemory(passive_dtcs))

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
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1)

    testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))

    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    testresult.append(["[.] Wechsel in Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))
    testresult.append(["[-0]", ""])

    # test step 12
    testresult.append(["[.] Fehlerspeicher l?schen", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # test step 13
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1)

    # test step 14
    testresult.append(["[.] Pr?fe, dass Fehler l?schbar ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] Bus Reset", ""])
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

