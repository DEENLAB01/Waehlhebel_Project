#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Timeouterkennung_SiShift_01_nach_Start_Timer4.py
# Title   : Timeouterkennung N-Haltephase SiShift Timer4 Start
# Task    : Timeouterkennung der N-Haltephase SiShift nach Timer4 Start
#
# Author  : Mohammed Abdul Karim
# Date    : 23.07.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 23.07.2021 | Mohammed     | initial
# 1.1  | 30.07.2021 | Mohammed     | Rework
# 1.2  | 13.12.2021 | Devangbhai   | Rework
# 1.3  | 14.12.2021 | Devangbhai   | Added DAQ evaluation
# 1.4  | 26.01.2022 | Mohammed     | Corrected DTC and added event memory
# 1.5  | 07.02.2022 | Mohammed     | Added Strommonitoring
# 1.6  | 17.02.2022 | Mohammed    | Added NWDF_30 Signal
# 1.7  | 24.03.2022 | Devangbhai  | Test step 4 --> set the N hold phase to 0

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
import copy

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
    func_hil = functions_hil.FunctionsHil(testenv, hil)

    # Initialize variables ####################################################
    test_variable = hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value
    test_variable.alias = "Waehlhebel_04:WH_Zustand_N_Haltephase_2"
    SiShift_period = hil.SiShift_01__period
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    SiShift_period = hil.SiShift_01__period
    allowed_fahrstufe = [4, 5, 6, 7, 8]  # nicht_betaetigt, D, N, R, P,
    wh_fahrstufe_fehlerwert = 15  # 'Fehler'

    meas_vars = [hil.cl15_on__, hil.Waehlhebel_04__timestamp,
                 hil.DS_Waehlhebel__timestamp, hil.KN_Waehlhebel__timestamp,
                 hil.NM_Waehlhebel__timestamp, hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value]
    period_var = hil.SiShift_01__period  ### Added

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_181")

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
    testresult.append(["[-] Testep Present disabled", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+] Prüfe, dass %s zum Teststart wie erwartet gesetzt ist (=0)" % test_variable.alias, ""])

    testresult.append(["Starte DAQ Messung für Applikations- und NM-Botschaften und warte 1 sekund", "INFO"])
    testresult.append(["Folgende Signale werden mitgemessen:\n%s" % meas_vars, ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    # test test 1
    testresult.append(["\x0a1. Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    # test test 2
    testresult.append(["\x0a2.Setze SiShift_FlgStrtNeutHldPha = 1, VDSO_Vx3d  = 32766, SIShift_StLghtDrvPosn  = 6 und KL15 aus -  Prüfe, dass %s auf 1 wechselt" % test_variable.alias, ""])
    testresult.append(["\xa0Setze SiShift FlgStrtNeutHldPha auf 1 (StartNeutralHoldPhase)", ""])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(1)

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["\xa0Setze KL15 auf 0 (inactive)", ""])
    time1 = time.time()
    hil.cl15_on__.set(0)
    testresult.append(["\xa0 Warte 150ms", ""])
    time.sleep(0.15)

    # test test 2.1
    testresult.append(["\x0a2.1 Schalte Senden von RX Signalen (HiL --> ECU) aus", ""])
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])

    # test test 2.2
    testresult.append(["\x0a2.2 Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )

    """
    # removed this part as not requitred
    # for time_sleep in [60, 60*24]:
    #     testresult.append(["[.] Prüfe nach %s Minute Busruhe und Strommonitoring" % (time_sleep / 60), ""])
    #     func_com.waitSecondsWithResponse(time_sleep)
    #     descr, verdict = func_gs.checkBusruhe(daq, 1)
    """

    # test test 3
    testresult.append(["\x0a3. 25 min warten...auf empfangene Botschaften prüfen", ""])
    descr, verdict = func_nm.waitTillTimerEnds(timer=1)
    testresult.append([descr, verdict])

    # test test 4
    testresult.append(["\x0a4. Schalte Senden von RX Signalen (HiL --> ECU) ein", ""])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(0)
    func_nm.hil_ecu_tx_off_state("an")

    # test test 5
    testresult.append(["\x0a5.  1 min warten...nach 26 min auf empfangene Botschaften prüfen ", ""])
    # descr, verdict = func_nm.waitTillTimerEnds(timer=2, switch_rx_signals=False)
    # testresult.append([descr, verdict])
    time.sleep(1 * 60)
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 0, descr="Prüf dass NM_aktiv_Tmin = 0"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value, 0, descr="Prüf dass NM_Waehlhebel_FCAB= 0"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1, descr="Prüf dass NM_Waehlhebel_CBV_AWB= 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0, descr="Prüf dass NM_Aktiv_N_Haltephase_abgelaufen= 0"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1, descr="Prüf dass WH_Zustand_N_Haltephase_2 = 1")
    ]

    # test test 6
    testresult.append(["\x0a6 Schalte Senden von RX Signalen (HiL --> ECU) aus", "INFO"])
    func_nm.hil_ecu_tx_off_state("aus")

    # test test 7
    testresult.append(["\x0a7.  3 min warten...nach 29 min auf empfangene Botschaften prüfen ", ""])
    time.sleep(3 * 60)
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1, descr="Prüf dass NM_aktiv_Tmin = 1"),
        func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [1], [], descr="Prüf dass NM_Waehlhebel_FCAB = mindestens 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1, descr="Prüf dass NM_Waehlhebel_CBV_AWB= 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0, descr="Prüf dass NM_Aktiv_N_Haltephase_abgelaufen= 0"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 5, descr="Prüf dass WH_Zustand_N_Haltephase_2 = 5")
    ]

    # test test 8
    testresult.append(["\x0a8 Setze Zykluszeit der Botschaft SiShift_01 auf 0ms  und schalte Senden von RX Signalen (HiL -->ECU) ein", ""])
   # hil.SiShift_01__period.setState('aus')  # changed to aus

    # hil.OTAMC_01__period.setState('an')
    hil.VDSO_05__period.setState('an')
    hil.Diagnose_01__period.setState('an')
    hil.ClampControl_01__period.setState('an')
    hil.NVEM_12__period.setState('an')
    hil.Dimmung_01__period.setState('an')
    hil.NM_Airbag__period.setState('an')
    hil.OBDC_Funktionaler_Req_All_FD__period.setState('an')
    hil.OBD_03__period.setState('an')
    hil.OBD_04__period.setState('an')
    hil.ORU_Control_A_01__period.setState('an')
    hil.ORU_Control_D_01__period.setState('an')
    hil.OTAMC_D_01__period.setState('an')
    hil.Systeminfo_01__period.setState('an')
    hil.NM_HCP1__period.setState('an')
    hil.ORU_01__period.setState('an')

    testresult.append(["Setze  Zykluszeit der Botschaft SiShift_01 auf 0ms", "INFO"])
    period_var.set(0)

    # test test 9
    testresult.append(["\x0a9. Warte 4950ms (tMSG_CYCLE)", ""])
    time.sleep(4.95)

    # test test 10
    testresult.append(["\x0a10.  Lese Fehlerspeicher aus (0xE00101 -DTC aktiv)", ""]) ###
    active_dtcs = [(0xE00101, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='Fehler Id:18'))

    testresult.append(["\x0a Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2 !=0", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0, equal=False,
            descr="Prüfe, dass Wert !=0 ist",
        )
    )

    # test test 11
    testresult.append(["\x0a11. Schalte Senden von RX Signalen (HiL --> ECU) aus", ""])
    func_nm.hil_ecu_tx_off_state("aus")
    time2 = time.time()

    # test test 12
    testresult.append(["\x0a12. Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append( basic_tests.checkStatus(current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, nominal_status=0, descr="Prüfe, dass Wert 0 ist",))
    testresult.append(["\xa0 Prüfe, es werden keine NM-Botschaften gesendet, aber es werden Applikationsbotschaften gesendet:", ""])
    time3 = time2 - time1
    testresult.append(["\xa0 Siehe DAQ Analysis", "INFO"])

    # test test 13
    testresult.append(["\x0a13. Warte TTimeout 1000 ms (RS-->PBSM)", "INFO"])
    # testresult.append(["[.] Prüfe, dass in Ready Sleep Mode gewechselt wurde", ""])
    # t_timeout_s = 1
    # testresult.append(["[.] Warte %sms + 1000ms (T Timeout)" % (t_timeout_s * 1000), ""])
    # func_com.waitSecondsWithResponse(t_timeout_s * 1.05 + 0.1)
    time.sleep(1)

    # test test 14
    testresult.append(["\x0a14. Warte TWaitBusSleep 750 ms (PBSM-->BSM)", ""])
    # testresult.append(["[.] Prüfe, dass in Prepare Bus-Sleep Mode gewechselt wurde", ""])
    # t_timeout_s = 1
    # testresult.append(["[.] Warte %sms + 750ms (T Timeout)" % (t_timeout_s * 750), ""])
    # func_com.waitSecondsWithResponse(t_timeout_s * 1.05 + 0.1)
    time.sleep(0.750)
    time4 = time.time()
    time5 = time4 - time2

    # test test 15
    testresult.append(["\xa0 15 Warte 60 Sekunde und Prüfe  Busruhe (0mA<I<2mA)", ""])
    time.sleep(60)
    testresult.append(["Prüfe, Es werden keine Botschaften versendet oder empfangen", ""])
    temp_value = func_nm.low_current()
    testresult.append(basic_tests.checkRange(value=temp_value / 1000,
                                             min_value=0.0,  # 0mA
                                             max_value=0.002,  # 2mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt"))

    testresult.append(["\xa0 Siehe DAQ Analysis", "INFO"])

    testresult.append(["2 sekund warten und Stoppe DAQ Messung", "INFO"])
    time.sleep(2)
    daq_data = daq.stopMeasurement()
    time.sleep(0.1)

    testresult.append(["\xa0Werte Waehlhebel_04__WH_Zustand_N_Haltephase_2 Signal aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data[str(meas_vars[5])],
        filename="Timeouterkennung_SiShift_01_nach_Start_Timer4",
        label_signal="WH_Zustand_N_Haltephase_2_Testspec_181")
    testresult.append([descr, plot, verdict])
    cl15_data = daq_data[str(hil.cl15_on__)]
    analyse_cl15_data = eval_signal.EvalSignal(cl15_data)
    analyse_cl15_data.clearAll()
    time_zero = analyse_cl15_data.getTime()
    cl15_off_time = analyse_cl15_data.find(operator="==", value=0)  # KL15 aus
    cl15_off_idx = analyse_cl15_data.cur_index
    if cl15_off_time is not None:
        testresult.append(["KL15 aus Zeitpunkt: %ss" % (round(cl15_off_time - time_zero, 4)), "INFO"])

        testresult.append(
            ["\x0a12 Es werden nur Applikation Botschaften versendet. NM Botschaften sendet nicht mehr.", ""])
        testresult.append(["Prüf nach %s, dass kein NM Botschaften gesendet. Nur Applikation Botschaften versendet " % (
                    (cl15_off_time - time_zero) + time3), "INFO"])
        for var in meas_vars:
            if var == hil.NM_Waehlhebel__timestamp:
                verdict, discription = func_nm.analysisNmMessageSent(start_time=cl15_off_time + time3, name=str(var),
                                                                     daq_data=daq_data[str(var)], NMAreSending=False)
                testresult.append([discription, verdict])

            elif (var != hil.cl15_on__) and (var != hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value) and (
                    var != hil.NM_Waehlhebel__timestamp):
                verdict, discription = func_nm.analysisApplicationMessageSent(start_time=cl15_off_time + time3,
                                                                              name=str(var),
                                                                              daq_data=daq_data[str(var)],
                                                                              ApplicationsAreSending=True)
                testresult.append([discription, verdict])

        testresult.append(["\x0a14 Busruhe: Es werden keine Botschaften versendet oder empfangen (0mA<I<2mA)", ""])
        testresult.append(["Prüf nach %s, dass kein Botschaften gesendet oder empfangen"
                           ". " % ((cl15_off_time - time_zero) + time3 + time5), "INFO"])

        for var in meas_vars:
            if var == hil.NM_Waehlhebel__timestamp:
                verdict, discription = func_nm.analysisNmMessageSent(start_time=cl15_off_time + time3 + time5,
                                                                     name=str(var),
                                                                     daq_data=daq_data[str(var)], NMAreSending=False)
                testresult.append([discription, verdict])

            elif (var != hil.cl15_on__) and (var != hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value) and (
                    var != hil.NM_Waehlhebel__timestamp):
                verdict, discription = func_nm.analysisApplicationMessageSent(start_time=cl15_off_time + time3 + time5,
                                                                              name=str(var),
                                                                              daq_data=daq_data[str(var)],
                                                                              ApplicationsAreSending=False)
                testresult.append([discription, verdict])

    else:
        testresult.append(["KL15 aus Zeitpunkt nicht gefunden", "FAILED"])


    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
