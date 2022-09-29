# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Verlaengerung_N_Haltephase_Timer2.py
# Title   : Verlaengerung N Haltephase Timer2
# Task    : Test Verlaengerung der N-Haltephase Timer2
#
# Author  : Mohammed Abdul Karim
# Date    : 12.05.2021
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 29.10.2021 | Mohammed   | initial
# 1.1  | 29.10.2021 | Mohammed   | initial
# 1.2  | 10.12.2021 | Mohammed   | Added Fehler Id
# 1.3  | 15.12.2021 | Devangbhai | Chanded the velocity timer from 0.04ms to infinite, adjusted the timing
# 1.4  | 15.12.2021 | Mohammed   | Corrected NM_aktiv_Tmin and NM_Aktiv_N_Haltephase_abgelaufen value
# 1.5  | 14.06.2022 | Devangbhai | Added Ticket ID 232
# 1.6  | 26.07.2022 | Mohammed   | test step 5 und 7 Testschritte aktualisiert
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
from functions_nm import _checkStatus
import functions_common
import functions_nm
import time
from time import time as t

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
    func_com = functions_common.FunctionsCommon(testenv)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    test_variable = hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value
    test_variable.alias = "Waehlhebel_04:WH_Zustand_N_Haltephase_2"

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_116")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    testresult.append(["[.]Initialisierungsphase abgeschlossen und Waehlhebelposition D aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('D')
    testresult.append(["\xa0" + descr, verdict])

    # TEST PROCESS ############################################################
    testresult.append([" Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # test step 1
    testresult.append(["\x0a1. Lese Signal Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append([" Prüfe WH_Zustand_N_Haltephase_2 = 0", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    # test step 2
    testresult.append(["\x0a2 Setze SiShift_FlgStrtNeutHldPha = 1,VDSO_Vx3d = 32766 (0 km/h),SIShift_StLghtDrvPosn = 6, und Kl15 aus ", ""])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(1)

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["Setze KL15 auf 0 (inactive) und 150ms warten", "INFO"])
    hil.cl15_on__.set(0)
    time.sleep(0.15)

    testresult.append(["\x0a2.1 Schalte Senden von RX Signalen (HiL --> ECU) aus", ""])
    func_nm.hil_ecu_tx_off_state("aus")

    testresult.append(["\x0aPrüfe WH_Zustand_N_Haltephase_2 = 1 ", "INFO"])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )

    # test step 3
    testresult.append(["\x0a3.1 min warten...nach 1 min CAN-Trace auswerten", ""])
    time.sleep(60)
    testresult.append(["\x0aPrüfe, Kein Senden und Empfangen von Botschaften (WH im lokalen Nachlauf", ""])
    time_1 = time.time()
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    testresult.append([descr, verdict])

    time_2 = time.time()
    time_difference = time_2 - time_1

    testresult.append(["Prüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    # test step 4
    testresult.append(["\x0a4. 23 min warten...nach 24 min CAN-Trace auswerten", ""])
    time.sleep(1380 - time_difference)
    testresult.append(["\x0a Prüfe, Kein Senden und Empfangen von Botschaften (WH im lokalen Nachlauf)", ""])
    time_5 = time.time()
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    time_6 = time.time()
    time_difference3 = time_6 - time_5
    testresult.append([descr, verdict])
    testresult.append(
        basic_tests.checkRange(value=hil.cc_mon__A.get(),min_value=0.002, max_value=0.100,
                               descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"))
    # storing the last time stamp
    nm_timestamp = hil.NM_Waehlhebel__timestamp
    start_timestamp = nm_timestamp.get()


    # test step 5
    testresult.append(["\x0a5. 1 min warten...nach 25 min CAN-Trace auswerten", ""])
    wait_time= 61- time_difference3 + 2

    t_out = wait_time + t()
    WH_Sends_data = False
    while t_out > t():
        curr_timestamp = nm_timestamp.get()
        if start_timestamp != curr_timestamp:
            testresult.append(
                ["\xa0 WH starts sending the message after %sec" % (curr_timestamp - start_timestamp), "PASSED"])
            WH_Sends_data = True
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 WH not sending the message ", "FAILED"])
            break

    if WH_Sends_data == False:
        testresult.append(["\xa0 WH sendet keine Botschaften nach 25 min ", "FAILED"])

    testresult.append(["\x0aPrüfe folgende Signale werden vom Wählhebel nach Ablauf Timer1 gesendet", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="NM_Waehlhebel_CBV_AWB: Aktiver_WakeUp"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1,
                                descr="WH_Zustand_N_Haltephase_2: aktiv_Timer_laeuft"),
        # func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [1], [],
        #                          descr="NM_Waehlhebel_FCAB:12_GearSelector"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1,
                                descr="NM_Waehlhebel_NM_aktiv_Tmin:Mindestaktivzeit"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv")
    ]

    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    # test step 6
    testresult.append(["\x0a6. Schalte Senden von RX Signalen (HiL -->ECU) und Sende VDSO_Vx3d = 32838  (1,008 km/h)", ""])
    func_nm.hil_ecu_tx_off_state("an")
    descr, verdict = func_gs.setVelocity_kmph(1.008, True)    # changed the velocity timer from 0.04ms to forever
    testresult.append([descr, verdict])

    # test step 7
    testresult.append(["\x0a7. 1 min warten...nach 26 min CAN-Trace auswerten", ""])
    time.sleep(60)
    testresult.append(["\x0aPrüfe folgende Signale werden vom Wählhebel nach Ablauf Timer2 gesendet", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="NM_Waehlhebel_CBV_AWB: Aktiver_WakeUp"),
        # func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [1], [],
        #                          descr="NM_Waehlhebel_FCAB:12_GearSelector"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1,
                                descr="WH_Zustand_N_Haltephase_2: aktiv_Timer_laeuft"),
        _checkStatus(current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, nominal_status=0,
                     descr="NM_Waehlhebel_NM_aktiv_Tmin:inaktiv", ticket_id='Fehler Id:EGA-PRM-15'),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv")
    ]

    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    # test step 8
    testresult.append(["\x0a8. VDSO_Vx3d = 32766 senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])
    time.sleep(0.025)

    # test step 9
    testresult.append(["\x0a9. 1 min warten...nach 27 min CAN-Trace auswerten", ""])
    time.sleep(60)
    testresult.append(["\x0aPrüfe folgende Signale werden vom Wählhebel nach Ablauf Timer2 gesendet", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1, descr="NM_Waehlhebel_CBV_AWB: Aktiver_WakeUp"),
        # basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value, 0, descr="NM_Waehlhebel_FCAB: Init"),
        func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [], [1], descr="NM_Waehlhebel_FCAB:CAR wakeup = 0", ticket_id='Fehler-Id: EGA-PRM-232'),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1, descr="WH_Zustand_N_Haltephase_2: aktiv_Timer_laeuft"),
        _checkStatus(current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, nominal_status=0, descr="NM_Waehlhebel_NM_aktiv_Tmin:inaktiv", ticket_id='Fehler Id:EGA-PRM-15'),
        _checkStatus(current_status=hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, nominal_status=0, descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv ist", ticket_id='Fehler Id:EGA-PRM-15')
    ]

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup #################################################################
    # hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
