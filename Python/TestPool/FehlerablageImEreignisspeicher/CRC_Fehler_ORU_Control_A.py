#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CRC_Fehler_ORU_Control_A.py
# Title   : CRC_Fehler_ORU_Control_A
# Task    : ORU_Control_A Fehlererkennung für CRC-Fehler und Ablage im Fehlerspeicher
#
# Author  : Mohammed Abdul Karim
# Date    : 13.05.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 13.05.2022  | Mohammed | initial
# 1.1  | 18.05.2022  | Mohammed | Rework
# 1.2  | 11.07.2022  | Mohammed | 3 OP-PowerCycle
# 1.3  | 14.07.2022  | Mohammed | Rework
# 1.4  | 27.07.2022  | Mohammed  | Added waiting time during ECU_Sleep
#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()

# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
from ttk_checks import basic_tests
import functions_gearselection
import time
from time import time as t
import functions_hil
from functions_diag import HexList  # @UnresolvedImport
import functions_nm

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
    func_hil = functions_hil.FunctionsHil(testenv, hil)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    period_var = hil.ORU_Control_A_01__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 15000  # CAN_3244
    active_dtcs = [(0xE0010D, 0x27)]
    passive_dtcs = [(0xE0010D, 0x24)]
    confirme_dtcs = [(0xE0010D, 0x2F)]
    curr_value = func_nm.low_current()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_192")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: LK30 und Kl15 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[.] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    # testresult.append(["[.] Raumtemperatur zwischen -40 to 90 Grad = %s degree" % (int(hex(res[3]), 16)), ""])
    # testresult.append(["[.] Auslesen DID: 0xF1F3 (Raumtemperatur zwischen -40 to 90 Grad)", ""])
    request = [0x22] + [0xF1, 0xF3]
    [response, result] = canape_diag.sendDiagRequest(request)
    # testresult.append(result)
    # testresult.append(["[.] Auf positive Response überprüfen", ""])
    # testresult.append(canape_diag.checkPositiveResponse(response, request))
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

    testresult.append(["[.] Prüfe Betriebsspannung : 6-16 V", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.vbat_cl30__V.get(),  # letzer Sendetimestamp
            min_value=6.0,
            max_value=16.0,
            descr="Check that value is in range"
        )
    )

    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    #testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Setze Zykluszeit der Botschaft ORU_Control_A_01 auf 500ms (gültig)", ""])
    testresult.append(["\xa0 Setze Zykluszeit auf %sms" % cycle_time, ""])
    period_var.set(cycle_time)

    # test step 2
    testresult.append(["[.] Warte 1500 ms", ""])
    time.sleep(1.50)

    # test step 3
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 4-4.2
    sec = 0.490
    timeout = sec + t()
    testresult.append(["[.] Sende erste CRC-Fehler für ORU_Control_A::ORU_Control_A_CRC", ""])
    while timeout > t():
        hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0)

    testresult.append(["[+] Warte für 220ms (FR=Fehlerreaktionszeit) + 10ms (Toleranz)", ""])
    time.sleep(0.230)

    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='FehlerId:EGA-PRM-250'))
    testresult.append(["[-0]", ""])

    # test step 5-5.2
    sec = 0.500
    timeout = sec + t()
    testresult.append(["[.] Sende zweite CRC-Fehler für ORU_Control_A::ORU_Control_A_CRC", ""])
    while timeout > t():
        hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0)

    testresult.append(["[+] Warte für 220ms (FR=Fehlerreaktionszeit) + 10ms Toleranz", ""])
    time.sleep(0.230)

    testresult.append(["[.] Lese Fehlerspeicher (0xE0010D DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='FehlerId:EGA-PRM-237'))
    testresult.append(["[-0]", ""])

    # test step 6-6.8
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

    # test step 7-7.2
    testresult.append(["[.] Sende keinen CRC-Fehler mehr für ORU_Control_A_01::ORU_Control_A_01_CRC ", ""])
    testresult.append(["[+] Warte Warte für 1100ms(2x tMSG_CYCLE + Toleranz)", ""])
    time.sleep(1.1)

    testresult.append(["[.] Lese Fehlerspeicher (0xE0010D DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(active_dtcs))
    testresult.append(["[-0]", ""])

    # test step 8-8.8
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

    # test step 9-9.6
    testresult.append(["\x0a Führe 3 OP-PowerCycle (ECU_Sleep (Ruhestrom auswerten) -> ECU_WakeUp) durch:", ""])
    testresult.append(["[.] Führe ersten OP-PowerCycle (ECU_Sleep  -> ECU_WakeUp) durch", ""])
    hil.cl15_on__.set(0)
    time.sleep(.200)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(20)
    testresult.append(["[+] Warte 20 Sekunde während ECU_Sleep und Prüfe Ruhestrom ", ""])
    testresult.append(basic_tests.checkRange(value=hil.cc_mon__A,
                                             min_value=0.0,  # 0mA
                                             max_value=0.006,  # 6mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt", ))

    testresult.append(["[.] Bus WakeUp und Warte 2 Sekunde  ", ""])
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(2)

    testresult.append(["[.] Lese Fehlerspeicher Passiv ", ""])
    testresult.append(canape_diag.checkEventMemory(passive_dtcs, mode="ONE_OR_MORE"))

    testresult.append(["[.] Sende zwei ORU_Control_A-CRC Fehler hintereinander", ""])
    sec = 1
    timeout = sec + t()
    while timeout > t():
        hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0)

    testresult.append(["[.] Warte für 220ms (FR=Fehlerreaktionszeit) + 10ms Toleranz", ""])
    time.sleep(0.230)

    testresult.append(["[.] Lese Fehlerspeicher (0xE0010D DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(active_dtcs, mode="ONE_OR_MORE"))
    testresult.append(["[-0]", ""])

    # test step 10-10.6
    testresult.append(["[.] Führe zweiten OP-PowerCycle (ECU_Sleep -> ECU_WakeUp)", ""])
    hil.cl15_on__.set(0)
    time.sleep(.200)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(20)
    testresult.append(["[+] Warte 20 Sekunde während ECU_Sleep und Prüfe Ruhestrom ", ""])
    testresult.append(basic_tests.checkRange(value=hil.cc_mon__A,
                                             min_value=0.0,  # 0mA
                                             max_value=0.006,  # 6mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt", ))

    testresult.append(["[.] Bus WakeUp und Warte 2 Sekunde  ", ""])
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(2)

    testresult.append(["[.] Lese Fehlerspeicher Passiv ", ""])
    testresult.append(canape_diag.checkEventMemory(passive_dtcs, mode="ONE_OR_MORE", ticket_id='FehlerId: EGA-PRM-237'))

    testresult.append(["[.] Sende zwei ORU_Control_A-CRC Fehler hintereinander", ""])
    sec = 1
    timeout = sec + t()
    while timeout > t():
        hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0)

    testresult.append(["[.] Warte für 220ms (FR=Fehlerreaktionszeit) + 10ms Toleranz", ""])
    time.sleep(0.230)
    testresult.append(["[.] Lese Fehlerspeicher (0xE0010D DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(active_dtcs, mode="ONE_OR_MORE"))
    testresult.append(["[-0]", ""])

    # test step 11-11.7
    testresult.append(["[.] Führe dritten OP-PowerCycle (ECU_Sleep -> ECU_WakeUp)", ""])
    hil.cl15_on__.set(0)
    time.sleep(.200)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(20)
    testresult.append(["[+] Warte 20 Sekunde während ECU_Sleep und Prüfe Ruhestrom ", ""])
    testresult.append(basic_tests.checkRange(value=hil.cc_mon__A,
                                             min_value=0.0,  # 0mA
                                             max_value=0.006,  # 6mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt", ))

    testresult.append(["[.] Bus WakeUp und Warte 2 Sekunde  ", ""])
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(2)

    testresult.append(["[.] Lese Fehlerspeicher Passiv ", ""])
    passive_dtcs = [(0xE0010D, 0x24)]
    testresult.append(canape_diag.checkEventMemory(passive_dtcs, mode="ONE_OR_MORE"))

    testresult.append(["[.] Sende zwei ORU_Control_A-CRC Fehler hintereinander", ""])
    sec = 1
    timeout = sec + t()
    while timeout > t():
        hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0)

    testresult.append(["[.] Warte für 220ms (FR=Fehlerreaktionszeit) + 10ms Toleranz", ""])
    time.sleep(0.230)

    testresult.append(["[.] Lese Fehlerspeicher (Aktiv und Confirme DTC )", ""])
    testresult.append(canape_diag.checkEventMemory(confirme_dtcs, mode="ONE_OR_MORE", ticket_id='FehlerId:EGA-PRM-247'))

    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1.0)
    testresult.append(["[-0]", ""])

    # test step 12
    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # test step 13
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1.0)

    # test step 14
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

