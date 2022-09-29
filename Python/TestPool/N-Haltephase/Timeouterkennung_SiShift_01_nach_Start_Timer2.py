#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Timeouterkennung_SiShift_01_nach_Start_Timer2.py
# Title   : Timeouterkennung SiShift nach Start Timer2
# Task    : Timeouterkennung der SiShift Start Timer2
#
# Author  : Mohammed Abdul Karim
# Date    : 04.11.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 04.11.2021 | Mohammed | initial
# 1.1  | 13.12.2021 | Devangbhai  | Rework

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
from functions_nm import _checkStatus, _checkRange
from time import time as t

# Instantiate test environment
testenv = TestEnv()

def check_cycletime(sec, application_msg=True, nm_msg=True):
    Waehlhebel_04__timestamp_list = []
    DS_Waehlhebel__timestamp_list = []
    KN_Waehlhebel__timestamp_list = []
    NM_Waehlhebel__timestamp_list = []

    timeout = sec + t()

    while timeout > t():
        timestamp_Waehlhebel_04 = hil.Waehlhebel_04__timestamp.get()
        timestamp_DS_Waehlhebel = hil.DS_Waehlhebel__timestamp.get()
        timestamp_KN_Waehlhebel = hil.KN_Waehlhebel__timestamp.get()
        timestamp_NM_Waehlhebel = hil.NM_Waehlhebel__timestamp.get()

        if len(Waehlhebel_04__timestamp_list) == 0 or Waehlhebel_04__timestamp_list[-1] != timestamp_Waehlhebel_04:
            Waehlhebel_04__timestamp_list.append(timestamp_Waehlhebel_04)

        elif len(DS_Waehlhebel__timestamp_list) == 0 or DS_Waehlhebel__timestamp_list[-1] != timestamp_DS_Waehlhebel:
            DS_Waehlhebel__timestamp_list.append(timestamp_DS_Waehlhebel)

        elif len(KN_Waehlhebel__timestamp_list) == 0 or KN_Waehlhebel__timestamp_list[-1] != timestamp_KN_Waehlhebel:
            KN_Waehlhebel__timestamp_list.append(timestamp_KN_Waehlhebel)

        elif len(NM_Waehlhebel__timestamp_list) == 0 or NM_Waehlhebel__timestamp_list[-1] != timestamp_NM_Waehlhebel:
            NM_Waehlhebel__timestamp_list.append(timestamp_NM_Waehlhebel)

    new_sec = sec * 1000
    Waehlhebel_04__timestamp = 10
    DS_Waehlhebel__timestamp = 1000
    KN_Waehlhebel__timestamp = 500
    NM_Waehlhebel_timestamp = 200

    testresult.append(basic_tests.checkRange((len(Waehlhebel_04__timestamp_list)) if application_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / Waehlhebel_04__timestamp) - 5) if application_msg else 0, ((new_sec / Waehlhebel_04__timestamp) + 5) if application_msg else 0, "Prüfen, ob die Applikation Botschaft Waehlhebel_04 mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (Waehlhebel_04__timestamp, sec)))
    testresult.append(basic_tests.checkRange((len(DS_Waehlhebel__timestamp_list)) if application_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / DS_Waehlhebel__timestamp) - 2) if application_msg else 0, ((new_sec / DS_Waehlhebel__timestamp) + 2) if application_msg else 0, "Prüfen, ob die Applikation Botschaft DS_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % ( DS_Waehlhebel__timestamp, sec)))
    testresult.append(basic_tests.checkRange((len(KN_Waehlhebel__timestamp_list)) if application_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / KN_Waehlhebel__timestamp) - 2) if application_msg else 0,((new_sec / KN_Waehlhebel__timestamp) + 2) if application_msg else 0, "Prüfen, ob die Applikation Botschaft KN_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % ( KN_Waehlhebel__timestamp, sec)))
    testresult.append(basic_tests.checkRange((len(NM_Waehlhebel__timestamp_list)) if nm_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / NM_Waehlhebel_timestamp) - 2) if nm_msg else 0, ((new_sec / NM_Waehlhebel_timestamp) + 2) if nm_msg else 0, "Prüfen, ob die Applikation Botschaft NM_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (NM_Waehlhebel_timestamp, sec)))


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
    #test_variable.alias = "Waehlhebel_04:WH_Zustand_N_Haltephase_2"
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    SiShift_period = hil.SiShift_01__period
    allowed_fahrstufe = [4, 5, 6, 7, 8]  # nicht_betaetigt, D, N, R, P,
    exp_dtc = 0X200101

    meas_vars = [hil.cl15_on__, hil.Waehlhebel_04__timestamp,
                 hil.DS_Waehlhebel__timestamp, hil.KN_Waehlhebel__timestamp,
                 hil.NM_Waehlhebel__timestamp, hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_180")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[.] Prüfe Waehlhebel_04:WH_Fahrstufe != 15", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = allowed_fahrstufe,
            current_value= current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe: WH_Fahrstufe != 15 ist"
        )
    )

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["Starte DAQ Messung für Applikations- und NM-Botschaften", "INFO"])
    testresult.append(["Folgende Signale werden mitgemessen:\n%s" % meas_vars, ""])
    daq.startMeasurement(meas_vars)

## 1
    testresult.append(["\x0a1. Lese Signal Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 (inaktiv) ist",
        )
    )
## 2
    testresult.append(["\xa02 Setze SiShift_FlgStrtNeutHldPha = 1,VDSO_Vx3d = 32766 (0 km/h),SIShift_StLghtDrvPosn = 6 und KL15 aus, ", "INFO"])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(1)

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["\Setze KL15 auf 0 (inactive) und 150ms warten", "INFO"])
    hil.cl15_on__.set(0)
    time.sleep(0.15)

    testresult.append(["\x0a2.1 Schalte Senden von RX Signalen (HiL --> ECU) aus", "INFO"])
    func_nm.hil_ecu_tx_off_state("aus")

    testresult.append(["\x0aPrüfe WH_Zustand_N_Haltephase_2 = 1 ", "INFO"])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 (aktiv_Timer_laeuft) ist",
        )
    )
    #3
    testresult.append(["\x0a3. nach 25 min CAN-Trace auswerten und auf empfangene Botschaften prüfen (Signale auswerten)", "INFO"])
    time.sleep(1500)
    # for time_sleep in [60, ((60 * 23.367)-time_difference)]:
    #    testresult.append(["\x0aPrüfe nach %s Minute Busruhe und Strommonitoring" % (time_sleep / 60), ""])
    #    func_com.waitSecondsWithResponse(time_sleep)

    testresult.append(["\x0a Prüfe NM_Waehlhebel Signals ", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="NM_Waehlhebel_CBV_AWB: Aktiver_WakeUp"),
        func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [1], [],
                                 descr="NM_Waehlhebel_FCAB:12_GearSelector"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1,
                                descr="WH_Zustand_N_Haltephase_2: aktiv_Timer_laeuft"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1,
                                descr="NM_Waehlhebel_NM_aktiv_Tmin:Mindestaktivzeit"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv")
    ]

    testresult.append(["\x0a4. Setze  Zykluszeit der Botschaft SiShift_01 auf 0ms und schalte Senden von RX Signalen (HiL -->ECU) ein", "INFO"])
    testresult.append(["Schalte Senden von empfangenen Signalen ein (HiL -> ECU)", "INFO"])
    func_nm.hil_ecu_tx_off_state("an")
    hil.SiShift_01__period.setState('aus')

    testresult.append(["\x0a5. Warte 4950ms (tMSG_CYCLE)", ""])
    time.sleep(4.95)
## 6
    testresult.append(["\x0aPrüfe DTC Nummer 0x200101 aktiv im Fehlerspeicher ist", ""])
    testresult.append(canape_diag.checkEventMemory([[exp_dtc, dc.DTCactive]]))
##7
    testresult.append(["\x0a7. Schalte Senden von RX Signalen (HiL --> ECU) aus", ""])
    func_nm.hil_ecu_tx_off_state("aus")

    testresult.append(["\x0a7.1 Lese Signal Waehlhebel_04:WH_Zustand_N_Haltephase_2, prüfe Timestamps", ""])

    # check if Application messages and NM messages are getting send ##todo
    check_cycletime(20)

    testresult.append(["\x0a8.Warte TTimeout 1000 ms (RS-->PBSM)", "INFO"])
    # t_timeout_s = 1
    # testresult.append(["\x0aWarte %sms + 1000ms (T Timeout)" % (t_timeout_s * 1000), ""])
    # func_com.waitSecondsWithResponse(t_timeout_s * 1.05 + 0.1)
    time.sleep(1)

    ##
    testresult.append(["\x0a9.Warte TWaitBusSleep 750 ms (PBSM-->BSM)", "INFO"])
    # t_timeout_s = 1
    # testresult.append(["Warte %sms + 750ms (T Timeout)" % (t_timeout_s * 750), ""])
    # func_com.waitSecondsWithResponse(t_timeout_s * 1.05 + 0.1)
    time.sleep(0.750)

    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    testresult.append(["Stoppe DAQ Messung", "INFO"])
    daq_data = daq.stopMeasurement()
    time.sleep(0.1)

    testresult.append(["\xa0Werte Waehlhebel_04__WH_Zustand_N_Haltephase_2 Signal aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data[str(meas_vars[5])],
        filename="Timeouterkennung_SiShift_01_nach_Start_Timer2",
        label_signal="WH_Zustand_N_Haltephase_2")
    testresult.append([descr, plot, verdict])

    testresult.append(["\x0aPrüfe, Kein Senden und Empfangen von Botschaften (WH im lokalen Nachlauf)", ""])
    time_5 = time.time()
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    time_6 = time.time()
    time_difference3 = time_6 - time_5
    testresult.append([descr, verdict])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
