#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Timeouterkennung_VDSO_05.py
# Title   : Timeouterkennung VDSO_05
# Task    : Timeouterkennung der N-Haltephase durch VDSO_05-Timeout
#
# Author  : Mohammed Abdul Karim
# Date    : 22.07.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 22.07.2021 | Mohammed    | initial
# 1.1  | 16.12.2021 | Devangbhai  | Added DAQ evaluation / Rework
# 1.2  | 26.01.2022 | Mohammed    | Corrected DTC and added reset event memory
# 1.3  | 07.02.2022 | Mohammed    | Added Strommonitoring
# 1.4  | 17.02.2022 | Mohammed    | Rework
# 1.5  | 24.02.2022 | Mohammed    | Added NWDF_30 Signal
# 1.6  | 25.03.2022 | Mohammed    | Added Fehler ID
# 1.7  | 20.04.2022 | Devangbhai   | Corrected the evaluation method
# 1.8  | 26.07.2022 | Mohammed    | test step 3,7 und 10 Testschritte aktualisiert
#******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
import functions_common
import functions_nm
import time
import functions_hil
import data_common as dc
from ttk_daq import eval_signal
from time import time as t

# Instantiate test environment
testenv = TestEnv()


def check_cycletime(sec, nm_msg=True):
    NM_Waehlhebel__timestamp_list = []

    timeout = sec + t()

    while timeout > t():
        timestamp_NM_Waehlhebel = hil.NM_Waehlhebel__timestamp.get()
        if len(NM_Waehlhebel__timestamp_list) == 0 or NM_Waehlhebel__timestamp_list[-1] != timestamp_NM_Waehlhebel:
            NM_Waehlhebel__timestamp_list.append(timestamp_NM_Waehlhebel)

    new_sec = sec * 1000

    NM_Waehlhebel_timestamp = 20

    testresult.append(basic_tests.checkRange((len(NM_Waehlhebel__timestamp_list)) if nm_msg else (len(NM_Waehlhebel__timestamp_list) - 1), ((new_sec / NM_Waehlhebel_timestamp) - 2) if nm_msg else 0, ((new_sec / NM_Waehlhebel_timestamp) + 2) if nm_msg else 0, "Prüfen, ob die Applikation Botschaft NM_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (NM_Waehlhebel_timestamp, sec)))



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
    func_hil = functions_hil.FunctionsHil(testenv, hil)

    # Initialize variables ####################################################
    test_variable = hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value
    test_variable.alias = "Waehlhebel_04:WH_Zustand_N_Haltephase_2"
    VDSO_05__period_period = hil.VDSO_05__period
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    allowed_fahrstufe = [4, 5, 6, 7, 8 ]  # nicht_betaetigt, D, N, R, P,
    wh_fahrstufe_fehlerwert = 15 # 'Fehler
    failure_reset_time = 1.0

    meas_vars = [hil.cl15_on__, hil.Waehlhebel_04__timestamp,
                 hil.DS_Waehlhebel__timestamp, hil.KN_Waehlhebel__timestamp,
                 hil.NM_Waehlhebel__timestamp, hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value]


    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_184")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[-] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["[.] Prüfe Waehlhebel_04:WH_Fahrstufe != 15", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = allowed_fahrstufe,
            current_value= current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe: WH_Fahrstufe != 15 ist"
        )
    )

    testresult.append(["[.] Tester Present disabled", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+] Prüfe, dass %s zum Teststart wie erwartet gesetzt ist (=0)" % test_variable.alias, ""])

    testresult.append(["Starte DAQ Messung für Applikations- und NM-Botschaften und warte 1 sekund", "INFO"])
    testresult.append(["Folgende Signale werden mitgemessen:\n%s" % meas_vars, ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["\x0a1. Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    testresult.append(["\x0a2. Setze SiShift_FlgStrtNeutHldPha = 1, VDSO_Vx3d  = 32766, SIShift_StLghtDrvPosn  = 6 und KL15 aus -  Prüfe, dass %s auf 1 wechselt" % test_variable.alias, ""])
    testresult.append(["\xa0Setze SiShift FlgStrtNeutHldPha auf 1 (StartNeutralHoldPhase)", ""])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(1)

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["\xa0Setze KL15 auf 0 (inactive)", ""])
    hil.cl15_on__.set(0)
    testresult.append(["\xa0 Warte 150ms", ""])
    time.sleep(0.15)

    testresult.append(["\x0a2.1 Schalte Senden von RX Signalen (HiL --> ECU) aus", ""])
    func_nm.hil_ecu_tx_off_state("aus")

    testresult.append(["\x0a2.2 Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )


    testresult.append(["\x0a3. 25 min warten...auf empfangene Botschaften prüfen", ""])
    wait_time = 24 * 60

    time.sleep(65)
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(0)    # making the Nhaltphase flake inactive
    nm_timestamp = hil.NM_Waehlhebel__timestamp
    start_timestamp = nm_timestamp.get()

    t_out = wait_time + t()
    while t_out > t():
        curr_timestamp = nm_timestamp.get()
        if start_timestamp != curr_timestamp:
            testresult.append(
                ["\xa0 WH starts sending the message after %s microsec" % (curr_timestamp - start_timestamp), "PASSED"])
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 WH not sending the message ", "FAILED"])
            break

    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1,
                                descr="Prüf dass NM_aktiv_Tmin = 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="Prüf dass NM_Waehlhebel_CBV_AWB= 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="Prüf dass NM_Aktiv_N_Haltephase_abgelaufen= 0"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1,
                                descr="Prüf dass WH_Zustand_N_Haltephase_2 = 1")
    ]

    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    # check_cycletime(sec=0.180, nm_msg=True)

    testresult.append(["\x0a4. Setze Zykluszeit der Botschaft VDSO_05 auf 0ms und schalte Senden von RX Signalen (HiL -->ECU) ein", ""])
    hil.VDSO_05__period.setState("aus")  # VDSO STATE IS AUS
    hil.Diagnose_01__period.setState("an")
    hil.ClampControl_01__period.setState("an")
    hil.NVEM_12__period.setState("an")
    hil.Dimmung_01__period.setState("an")
    hil.NM_Airbag__period.setState("an")
    hil.OBD_03__period.setState("an")
    hil.OBD_04__period.setState("an")
    hil.ORU_Control_A_01__period.setState("an")
    hil.ORU_Control_D_01__period.setState("an")
    hil.OTAMC_D_01__period.setState("an")
    hil.Systeminfo_01__period.setState("an")
    hil.NM_HCP1__period.setState("an")
    hil.SiShift_01__period.setState("an")

    testresult.append(["\x0a4.1. Warte 5000ms (tMSG_CYCLE)", ""])
    time1 = time.time()
    time.sleep(5)

    testresult.append(["\x0a4.2. Lese Fehlerspeicher aus (0xE00104 -DTC aktiv)", ""])
    #testresult.append(canape_diag.checkEventMemory([[exp_dtc, dc.DTCactive]]))
    active_dtcs = [(0xE00104, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs))

    testresult.append(["\x0a Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2 !=0", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0, equal=False,
            descr="Prüfe, dass Wert !=0 ist",
        )
    )
    testresult.append(["\x0a4.3. Setze Zykluszeit der Botschaft VDSO_05 auf 5ms", ""])
    hil.VDSO_05__period.set(5)

    testresult.append(["\x0a4.4. Lösche Fehlerspeicher", ""])
    testresult.append(canape_diag.resetEventMemory())

    testresult.append(["\x0a4.5. 1000ms warten...Fehlerspeicher erneut auslesen", ""])
    time.sleep(1)

    testresult.append(["\xa0 Fehlerspeicher erneut auslesen: Fehlerspeicher leer", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())
    time2 = time.time()
    time_diff= time2-time1

    testresult.append(["\x0a5. 1 min warten...nach 26 min auf empfangene Botschaften prüfen", ""])
    if time_diff > 60:
        time.sleep(0.0001)
    else:
        time.sleep(60- time_diff + 1)

    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 0,
                                descr="Prüf dass NM_aktiv_Tmin = 0"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value, 0,
                                descr="Prüf dass NM_Waehlhebel_FCAB= 0"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="Prüf dass NM_Waehlhebel_CBV_AWB= 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="Prüf dass NM_Aktiv_N_Haltephase_abgelaufen= 0"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1,
                                descr="Prüf dass WH_Zustand_N_Haltephase_2 = 1")]

    testresult.append(["\x0a6.  Schalte Senden von RX Signalen (HiL --> ECU) aus", ""])
    func_nm.hil_ecu_tx_off_state("aus")

    testresult.append(["\x0a7. 3 min warten...nach 29 min auf empfangene Botschaften prüfen", ""])
    time.sleep(63)
    nm_timestamp = hil.NM_Waehlhebel__timestamp
    start_timestamp = nm_timestamp.get()
    WH_Sends_data = False
    wait_time = 120
    t_out = wait_time + t()
    while t_out > t():
        curr_timestamp = nm_timestamp.get()
        if start_timestamp != curr_timestamp:
            testresult.append(
                ["\xa0 WH starts sending the message after %s microsec" % (curr_timestamp - start_timestamp), "PASSED"])
            WH_Sends_data = True
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 WH not sending the message ", "FAILED"])
            break
    if WH_Sends_data == False:
        testresult.append(["\xa0 WH sendet keine Botschaften nach 29 min ", "FAILED"])

    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1,
                                descr="Prüf dass NM_aktiv_Tmin = 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="Prüf dass NM_Waehlhebel_CBV_AWB= 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="Prüf dass NM_Aktiv_N_Haltephase_abgelaufen= 0"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 5,
                                descr="Prüf dass WH_Zustand_N_Haltephase_2 = 5")
    ]

    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    testresult.append(["\x0a8. Setze Zykluszeit der Botschaft VDSO_05 auf 0ms und schalte Senden von RX Signalen (HiL -->ECU) ein",""])
    hil.VDSO_05__period.setState("aus")  # VDSO STATE IS AUS
    hil.Diagnose_01__period.setState("an")
    hil.ClampControl_01__period.setState("an")
    hil.NVEM_12__period.setState("an")
    hil.Dimmung_01__period.setState("an")
    hil.NM_Airbag__period.setState("an")
    hil.OBD_03__period.setState("an")
    hil.OBD_04__period.setState("an")
    hil.ORU_Control_A_01__period.setState("an")
    hil.ORU_Control_D_01__period.setState("an")
    hil.OTAMC_D_01__period.setState("an")
    hil.Systeminfo_01__period.setState("an")
    hil.NM_HCP1__period.setState("an")
    hil.SiShift_01__period.setState("an")

    testresult.append(["\x0a9.1. Warte 5000ms (tMSG_CYCLE)", ""])
    time.sleep(5)
    testresult.append(["\x0a9.2. Lese Fehlerspeicher aus (0x200104 -DTC aktiv)", ""])  ###
    active_dtcs = [(0xE00104, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='Fehler Id:EGA-PRM-186'))

    testresult.append(["\x0a9.3. Setze Zykluszeit der Botschaft VDSO_05 auf 5ms", ""])
    hil.VDSO_05__period.set(5)
    time.sleep(0.030)

    testresult.append(["\x0a9.4. Lösche Fehlerspeicher", ""])
    testresult.append(canape_diag.resetEventMemory(ticket_id='Fehler Id:EGA-PRM-186'))

    testresult.append(["\x0a9.5. 1000ms warten...Fehlerspeicher erneut auslesen", ""])
    time.sleep(1)
    testresult.append(["\xa0Prüfe, dass Fehlerspeicher leer", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-186'))

    testresult.append(["\x0a10. 1 min warten...nach 30 min auf empfangene Botschaften prüfen", ""])
    time.sleep(60-5-1)
    testresult.append(["\x0aPrüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 0,
                                descr="Prüf dass NM_aktiv_Tmin =1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="Prüf dass NM_Waehlhebel_CBV_AWB= 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 1,
                                descr="Prüf dass NM_Aktiv_N_Haltephase_abgelaufen= 1"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 2,
                                descr="Prüf dass WH_Zustand_N_Haltephase_2 = 2")]
    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]
    
    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
