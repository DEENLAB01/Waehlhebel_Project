# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Verlaengerung_N_Haltephase_Timer4.py
# Title   : Verlaengerung N Haltephase Timer4
# Task    : Test Verlaengerung der N-Haltephase Timer4
#
# Author  : Mohammed Abdul Karim
# Date    : 03.11.2021
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       |  Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 03.11.2021  | Mohammed   | initial
# 1.1  | 03.11.2021  | Mohammed   | initial
# 1.2  | 15.12.2021  | Devangbhai | Chanded the velocity timer from 0.04ms to infinite, adjusted the timing
# 1.3  | 18.01.2022  | Mohammed   | Rework after TestSpec Updated
# 1.4  | 07.02.2022  | Mohammed   | Added Strommonitoring
# 1.5  | 01.04.2022  | Devangbhai | Corrected the method to add the test result for FCAB value
# 1.6  | 20.04.2022  | Devangbhai | Corrected the evaluation method.Added checking of fast NM cycle method
# 1.7  | 02.05.2022  | Devangbhai | Rework according to the test specification
# 1.8  | 04.05.2022  | Devangbhai | Added grapf of Waehlhebel_04__WH_Zustand_N_Haltephase_2
# 1.9  | 06.05.2022  | Devangbhai | removed grapf of Waehlhebel_04__WH_Zustand_N_Haltephase_2, changed the calue acording to new test spec, info from test spec 115
# 1.10 | 14.06.2022  | Devangbhai | changed the value of the signals according to the specification update
# 1.11 | 26.07.2022  | Mohammed   | test step 4.2, 7.2, 8.3, 9.3 und 10.3 Testschritte aktualisiert

# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
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

    meas_vars = [hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, hil.cl15_on__, ]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_117")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    testresult.append(["[.]Initialisierungsphase abgeschlossen und Waehlhebelposition D aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('D')
    testresult.append(["\xa0" + descr, verdict])

    # TEST PROCESS ############################################################
    testresult.append([" Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["Starte DAQ Messung für Applikations- und NM-Botschaften und warte 1 sekund", "INFO"])
    testresult.append(["Folgende Signale werden mitgemessen:\n%s" % meas_vars, ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)


    # test step 1
    testresult.append(["\x0a 1. Lese Signal Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(["Prüfe WH_Zustand_N_Haltephase_2 = 0", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 (inaktiv) ist",
        )
    )

    # test step 2
    testresult.append(["\x0a 2.  Setze SiShift_FlgStrtNeutHldPha = 1, VDSO_Vx3d = 32766 (0 km/h) und SIShift_StLghtDrvPosn = 6","INFO"])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(1)

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["Kl.15 = 0 senden, warte 150ms", "INFO"])
    hil.cl15_on__.set(0)
    time.sleep(0.15)

    # test step 2.1
    testresult.append(["\x0a 2.1 Schalte Senden von RX Signalen (HiL --> ECU) aus", "INFO"])
    func_nm.hil_ecu_tx_off_state("aus")

    testresult.append(["\x0a 2.2 Lese Signal Waehlhebel_04:WH_Zustand_N_Haltephase_2 = 1 ", "INFO"])
    testresult.append(["Prüfe WH_Zustand_N_Haltephase_2 = 1 ", "INFO"])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 (aktiv_Timer_laeuft) ist",
        )
    )

    # test step 3
    testresult.append(["\x0a3. Warte 1 Minute und Prüfe Kommunikation", ""])

    # test step 3.1
    testresult.append(["\x0a3.1 Warte bis 1 Minute bevor Timer 1 (25 min) abläuft und Prüfe erneut Kommunikation", ""])
    testresult.append(["Prüfe, Kein Senden und Empfangen von Botschaften (WH im lokalen Nachlauf", ""])
    time.sleep(60)

    # test step 3.2
    testresult.append(["\x0a3.2 Prüfe Strommonitoring", ""])
    testresult.append(["Prüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    # test step 3.3
    testresult.append(["\x0a3.3 Warte 23 min (p_t_NHalte_Dauer - 1 min (von Schritt 5.1) - 1 min)", ""])
    time.sleep(23*60)
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(0)


    # test step 3.4
    testresult.append(["\x0a3.4 Prüfe, Kein Senden und Empfangen von Botschaften (WH im lokalen Nachlauf)", ""])
    time_5 = time.time()
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    time_6 = time.time()
    time_difference3 = time_6 - time_5
    testresult.append([descr, verdict])

    # test step 3.5
    testresult.append(["\x0a3.5 Prüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    # storing the last time stamp
    nm_timestamp = hil.NM_Waehlhebel__timestamp
    start_timestamp = nm_timestamp.get()

    # test step 4, 4.1
    testresult.append(["\x0a4. Warte bis Timer 1 abgelaufen ist (und Timer 2 startet) und prüfe Signale:", ""])

    # test step 4.1
    testresult.append(["\x0a4.1 Warte 1 Min", ""])
    wait_time = 60 - time_difference3 + 3  # added 3 sec extra to check if the WH starts sending 1st NM message
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
        testresult.append(
            ["\xa0 WH sendet keine Botschaften nach 25 min ", "FAILED"])

    # test step 4.2
    testresult.append(["\x0a4.2 Prüfe, dass NM_Waehlhebel Botschaft empfangen wurde", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="NM_Waehlhebel_CBV_AWB: Aktiver_WakeUp"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1,
                                descr="WH_Zustand_N_Haltephase_2: aktiv_Timer_laeuft"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1,
                                descr="NM_Waehlhebel_NM_aktiv_Tmin: 1 ist")
    ]
    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    # test step 4.3
    testresult.append(["\x0a4.3. Schalte Senden von RX Signalen (HiL --> ECU) an ", ""])
    func_nm.hil_ecu_tx_off_state("an")

    # test step 5
    testresult.append(["\x0a5. Warte bis Timer 2 abgelaufen ist (und Timer 3 startet) und prüfe Signale", ""])

    # test step 5.1
    testresult.append(["\x0a5.1 Warte 1 min (p_t_NHalte_v_Check)", ""])
    time.sleep(60)

    testresult.append(["\x0a5.2 Prüfe WH_Zustand_N_Haltephase_2 = 1 ", "INFO"])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 (aktiv_Timer_laeuft) ist",
        )
    )

    # test step 5.3
    testresult.append(["\x0a5.3 Schalte Senden von RX Signalen (HiL --> ECU) aus", "INFO"])
    func_nm.hil_ecu_tx_off_state("aus")

    # test step 6
    testresult.append(["\x0a6. Warte bis 1 Minute bevor Timer 3 (3 min) abläuft und Prüfe Kommunikation", "INFO"])

    # test step 6.1
    testresult.append(["\x0a6.1 Warte 1 min (p_t_NHalte_verl - 2 min)", ""])
    time.sleep(60)

    testresult.append(["\x0aPrüfe WH_Zustand_N_Haltephase_2 = 1 ", "INFO"])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )

    testresult.append(["\x0a6.2 Prüfe, Kein Senden und Empfangen von Botschaften (WH im lokalen Nachlauf", ""])
    time_6 = time.time()
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    time_7 = time.time()
    testresult.append([descr, verdict])
    time_difference4 = time_7 - time_6

    # test step 6.3
    testresult.append(["\x0a6.3 Prüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(basic_tests.checkRange(value=hil.cc_mon__A.get(), min_value=0.002,
                                             max_value=0.100, descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"))

    # test step 7
    testresult.append(["\x0a7. Warte bis Timer 3 abgelaufen ist (und Timer 4 startet) und prüfe Signale:", ""])

    # test step 7.1
    testresult.append(["\x0a7.1 2 Warte 2 min ", ""])
    wait_time = 120- time_difference4 + 3
    t_out = wait_time + t()
    nm_timestamp = hil.NM_Waehlhebel__timestamp
    start_timestamp = nm_timestamp.get()
    WH_Sends_data_2 = False
    while t_out > t():
        curr_timestamp = nm_timestamp.get()
        if start_timestamp != curr_timestamp:
            testresult.append( ["\xa0 WH starts sending the message after %s microsec" % (curr_timestamp - start_timestamp), "PASSED"])
            WH_Sends_data_2 = True
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 WH not sending the message ", "FAILED"])
            break

    if WH_Sends_data_2 == False:
        testresult.append(
            ["\xa0 WH sendet keine Botschaften nach 29 min (nach timert3 abgelaufen ist)", "FAILED"])

    # test step 7.2
    testresult.append(["\x0a7.2 Prüfe, dass NM_Waehlhebel Botschaft empfangen wurde", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="01_CarWakeUp: 1"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 5,
                                descr="WH_Zustand_N_Haltephase_2: 5"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1,
                                descr="NM_Waehlhebel_NM_aktiv_Tmin:Mindestaktivzeit"),
    ]
    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    # test step 7.3
    testresult.append(["\x0a7.3 Schalte Senden von RX Signalen (HiL --> ECU) an", ""])
    func_nm.hil_ecu_tx_off_state("an")

    # test step 8
    testresult.append(["\x0a8. N-Haltephase Timer 4 wird verlängert", ""])

    # test step 8.1
    testresult.append(["\x0a8.1 Warte 500ms", ""])
    time.sleep(.500)

    # test step 8.2
    testresult.append(["\x0a8.2 Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=5,
            descr="Prüfe, dass Wert 5 ist",))

    # test step 8.3
    testresult.append(["\x0a8.3 Prüfe NM_Waehlhebel:NM_Waehlhebel_FCAB ", ""])
    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    # test step 9, 9.1
    testresult.append(["\x0a9. VDSO_05:VDSO_Vx3d = 32838 (1,008 km/h) senden ", ""])
    descr, verdict = func_gs.setVelocity_kmph(1.008, True)
    testresult.append([descr, verdict])

    # test step 9.1
    testresult.append(["\x0a9.1 Warte 1 min ", ""])
    time.sleep(60)

    # test step 9.2
    testresult.append(["\x0a9.2 Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )

    # test step 9.3
    testresult.append(["\x0a9.3 Prüfe NM_Waehlhebel:NM_Waehlhebel_FCAB ", ""])
    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    # test step 10
    testresult.append(["\x0a10 VDSO_05:VDSO_Vx3d = 32766 (0 km/h) senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(0, True)
    testresult.append([descr, verdict])

    # test step 10.1
    testresult.append(["\x0a10.1 Warte 20ms (2*Zykluszeit VDSO_05))", ""])
    time.sleep(0.020)

    # test step 10.2
    testresult.append(["\x0a10.2 Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1",))

    # test step 10.3
    testresult.append(["\x0a10.3 Prüfe NM_Waehlhebel:NM_Waehlhebel_FCAB ", ""])
    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]
    # test step 10.4
    testresult.append(["\x0a10.4 Warte 1 min (p_t_NHalte_v_Check)", ""])
    time.sleep(60)

    # test step 11, 11.1
    testresult.append(["\x0a11. Prüfe, dass Timer 4 verlassen wurde und N-Haltephase beendet wird", ""])

    # test step 11.1
    testresult.append(["\x0a11.1 Setze SiShiftStLghtDrvPosn = 'P', und Warte 1 Sekunde", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    time.sleep(1)
    testresult.append(["\xa0" + descr, verdict])

    # test step 11.2
    testresult.append(["\x0a11.2 Prüfe NM_Waehlhebel:NM_Waehlhebel_FCAB ", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value,
            nominal_status=0,
            descr="Prüfe, dass Wert Bit 1 (01_CarWakeUp) == 0",
        )
    )

    # test step 11.3
    testresult.append(["\x0a11.3 Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 (inaktiv) ist",))

    # test step 11.4
    testresult.append(["\x0a11.4 Schalte Senden von empfangenen Signalen aus (HiL -> ECU)", "INFO"])
    func_nm.hil_ecu_tx_off_state("aus")

    # test step 11.5
    testresult.append(["\x0a11.5 Warte 1 Minute", "INFO"])
    time.sleep(60)

    # test step 11.6
    testresult.append(["\x0a11.6 Prüfe Busruhe (0<I<2mA)", ""])
    temp_value = func_nm.low_current()
    testresult.append(basic_tests.checkRange(value=temp_value / 1000,
                                             min_value=0.0,  # 0mA
                                             max_value=0.002,  # 2mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt"))

    testresult.append(["2 sekund warten und Stoppe DAQ Messung", "INFO"])
    time.sleep(2)
    daq_data = daq.stopMeasurement()
    time.sleep(0.1)


    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    func_nm.hil_ecu_tx_off_state("an")
    time.sleep(3)
    testenv.shutdownECU()

    # cleanup #################################################################
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
