# ******************************************************************************
# -*- coding: latin1 -*-
# File    : WakeUp_Kl15_aus_PBSM_79.py
# Task    : A minimal "WakeUp_Kl15_aus_PBSM!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 21.01.2021 | Mohammed  | initial
# 1.1  | 26.05.2021 | StengerS     | reworked
# 1.2  | 30.06.2021 | NeumannA     | evaluation of FCAB Value updated
# 1.3  | 14.10.2021 | Mohammed     |Added Feher ID
# 1.4  | 12.11.2021 | Devangbhai   | Reworked
# 1.5  | 17.11.2021 | Devangbhai   | Reworked
# 1.6  | 24.11.2021 | Devangbhai   | changed waiting time from 500ms to 300ms
# 1.7  | 21.12.2021 | Mohammed     | Added Fehler Id
# 1.8  | 08.03.2022 | Devangbhai   | Removed 20ms cycle time
# 1.9  | 10.03.2022 | Devangbhai   | Changed the sleepnig time  in test step 7
# 1.10 | 21.03.2022 | Mohammed     | CSignal NM_Waehlhebel_NM_aktiv_Tmin korrigiert 0 nach 1

# ******************************************************************************
import time
from _automation_wrapper_ import TestEnv
from ttk_daq import eval_signal
from ttk_checks import basic_tests
import functions_nm
import functions_gearselection
import copy
from functions_nm import _checkStatus

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_79")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    applikationsbotschaften = [hil.Waehlhebel_04__timestamp,
                               hil.DS_Waehlhebel__timestamp,
                               hil.KN_Waehlhebel__timestamp, ]

    nm_botschaften = [hil.NM_Waehlhebel__timestamp]
    messages_cycle_times = {str(hil.Waehlhebel_04__timestamp): 10,
                            str(hil.DS_Waehlhebel__timestamp): 1000,
                            str(hil.KN_Waehlhebel__timestamp): 500,
                            str(hil.NM_Waehlhebel__timestamp): 200,
                            }
    tolerance_percent = 0.10
    cycletime_tol_perc = 0.10
    ttimeout = 1.0
    ttimeout_tol_perc = 0.05
    nm_stop_s = 0.4
    t_send_after_wakeup = 0.15  # to be clarified

    meas_vars = [hil.cl15_on__, hil.Waehlhebel_04__timestamp,
                 hil.DS_Waehlhebel__timestamp, hil.KN_Waehlhebel__timestamp,
                 hil.NM_Waehlhebel__timestamp]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten und 4 Sekunden warten (T_aktiv_min)", ""])
    testenv.startupECU()
    time.sleep(4)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+0]", ""])

    testresult.append(["Starte DAQ Messung für Applikations- und NM-Botschaften", "INFO"])
    testresult.append(["Folgende Signale werden mitgemessen:\n%s" % meas_vars, "INFO"])
    daq.startMeasurement(meas_vars)

    testresult.append(["\x0a1. Prüfe Werte der Botschaft NM_Waehlhebel", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 0,
                                descr="NM_Waehlhebel_CBV_AWB:Passiver_WakeUp"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value, 1,
                                descr="NM_Waehlhebel_CBV_CRI:NM_mit_Clusteranforderungen"),
        func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [12], [],
                                 descr="NM_Waehlhebel_FCAB:12_GearSelector"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_SNI_10__value, 83,
                                descr="NM_Waehlhebel_SNI_10:Waehlhebel_SNI"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value, 4 or 8,
                                descr="NM_Waehlhebel_NM_State:NM_NO_aus_RM oder NM_NO_aus_RS"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value, 1,
                                descr="NM_Waehlhebel_Wakeup_V12:Bus_Wakeup"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value, 1,
                                descr="NM_Waehlhebel_NM_aktiv_KL15:KL15_EIN"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value, 0,
                                descr="NM_Waehlhebel_NM_aktiv_Diag:Inaktiv"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 0,
                                descr="NM_Waehlhebel_NM_aktiv_Tmin:Inaktiv"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv")
    ]
    testresult.append(
        _checkStatus(current_status=hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value,
                     nominal_status=0,
                     descr="NM_Waehlhebel_UDS_CC:Inaktiv is",
                     ticket_id='FehlerId:EGA-PRM-13')
    )

    time.sleep(2)
    testresult.append(["Warte 2sec und Stoppe DAQ Messung", "INFO"])
    daq_data = daq.stopMeasurement()
    time.sleep(0.1)
    hcp1_mess = eval_signal.EvalSignal(daq_data[str(meas_vars[4])])
    hcp1_mess.clearAll()
    t_hcp1_sent = hcp1_mess.getTime()

    idx_hcp1_sent = hcp1_mess.cur_index

    daq_data_part1 = copy.deepcopy(daq_data)
    daq_data_part2 = copy.deepcopy(daq_data)
    for data1, data2 in zip(daq_data_part1, daq_data_part2):
        daq_data_part1[data1]['data'] = daq_data_part1[data1]['data'][:idx_hcp1_sent]
        daq_data_part1[data1]['time'] = daq_data_part1[data1]['time'][:idx_hcp1_sent]
        daq_data_part2[data2]['data'] = daq_data_part2[data2]['data'][idx_hcp1_sent:]
        daq_data_part2[data2]['time'] = daq_data_part2[data2]['time'][idx_hcp1_sent:]

    testresult.append(
        ["\x0a2. Prüfe Versenden (Timestamps/Zykluszeit) der gesendeten Applikations- und NM Botschaften:", ""])
    for var in meas_vars:
        if var != hil.cl15_on__:
            cycle_times, wakeup_time = func_nm.analyseCycleSleepTimes(start_time=t_hcp1_sent,
                                                                      daq_data=daq_data_part2[str(var)])

            if len(cycle_times) > 0:
                if var == hil.NM_Waehlhebel__timestamp:
                    testresult.append(["\xa0Prüfe, dass Zykluszeit von NM-Botschaft: NM_Waehlhebel korrekt ist", ""])
                    cycle_time = sum(cycle_times) / len(cycle_times)
                    testresult.append(
                        basic_tests.checkTolerance(current_value=cycle_time, rated_value=messages_cycle_times[str(var)],
                                                   rel_pos=cycletime_tol_perc, descr="Zykluszeit von %s" % str(var)))
                else:
                    testresult.append(["\xa0Prüfe, dass Zykluszeit von Applikationsbotschaften korrekt ist", ""])
                    cycle_time = sum(cycle_times) / len(cycle_times)
                    testresult.append(
                        basic_tests.checkTolerance(current_value=cycle_time, rated_value=messages_cycle_times[str(var)],
                                                   rel_pos=cycletime_tol_perc, descr="Zykluszeit von %s" % str(var)))
            else:
                testresult.append(["%s Botschaft beginnt sendet nicht" % str(var), "FAILED"])

    testresult.append(["Starte DAQ Messung für Applikations- und NM-Botschaften und warte 2s", "INFO"])
    testresult.append(["Folgende Signale werden mitgemessen:\n%s" % meas_vars, ""])
    daq.startMeasurement(meas_vars)
    time.sleep(4)

    testresult.append(["\x0a3. Schalte KL15 aus (=0), Schalte Restbussimulation aus, 150ms warten", ""])
    hil.cl15_on__.set(0)
    sleeping_t = 0.110
    time.sleep(sleeping_t)
    func_nm.hil_ecu_tx_off_state("aus")
    time.sleep(0.15 - sleeping_t)

    testresult.append(["\x0a5. Warte 1000ms (T Timeout)", "INFO"])
    time.sleep(1)

    testresult.append(["\x0a6. Warte 300ms (< T WaitBusSleep) ", "INFO"])
    time.sleep(0.1)

    # testresult.append(["Stoppe DAQ Messung", "INFO"])
    # daq_data1 = daq.stopMeasurement()
    # time.sleep(2)

    # plot_data = {}
    # for mes in applikationsbotschaften + nm_botschaften:
    #     plot_data[str(mes)] = daq_data1[str(mes)]
    # testresult.append(daq.plotMultiShot(plot_data, "WakeUp_Kl15_aus_PBSM_79_NACH_KL15_AUS"))
    #
    # testresult.append(["\xa0Werte KL15 Signal aus", "INFO"])
    # descr, plot, verdict = daq.plotSingleShot(
    #     daq_data=daq_data1[str(meas_vars[0])],
    #     filename="WakeUp_Kl15_aus_PBSM_79_NACH_KL15_AUSKL_15",
    #     label_signal="KL15_AUS")
    # testresult.append([descr, plot, verdict])
    #
    # cl15_data = daq_data1[str(hil.cl15_on__)]
    # cl_15 = eval_signal.EvalSignal(cl15_data)
    # cl_15.clearAll()
    # time_zero = cl_15.getTime()
    # # find timestamp when clamp 15 is switched off:
    # t_cl_15_off = cl_15.findNext("==", 0)
    # cl15_idx = cl_15.cur_index  # read index
    # testresult.append(["Ermittelter Zeitpunkt 'KL15 aus': %s" % (t_cl_15_off - time_zero), "INFO"])
    # test_start_time = cl15_data['time'][cl15_idx - 200]
    #
    # daq_data_part1 = copy.deepcopy(daq_data1)
    # daq_data_part2 = copy.deepcopy(daq_data1)
    # for data1, data2 in zip(daq_data_part1, daq_data_part2):
    #     daq_data_part1[data1]['data'] = daq_data_part1[data1]['data'][:cl15_idx]
    #     daq_data_part1[data1]['time'] = daq_data_part1[data1]['time'][:cl15_idx]
    #     daq_data_part2[data2]['data'] = daq_data_part2[data2]['data'][cl15_idx:]
    #     daq_data_part2[data2]['time'] = daq_data_part2[data2]['time'][cl15_idx:]
    #
    # testresult.append(["\x0a4. Prüfe Versenden (Timestamps/Zykluszeit) der gesendeten Applikations- und NM Botschaften:", ""])
    #
    # cycle_times = {}
    # sleep_times = {}
    # for var in meas_vars:
    #     if var != hil.cl15_on__:
    #         cycle_time, sleep_time = func_nm.analyseCycleSleepTimes(
    #             start_time=test_start_time,
    #             daq_data=daq_data_part2[str(var)])
    #         cycle_times[str(var)] = cycle_time
    #         sleep_times[str(var)] = sleep_time
    #
    # testresult.append(["\x0a4.1 Prüfe NM-Botschaften werden nicht gesendet: NM_Waehlhebel keine timestamps", ""])
    #
    # for var in nm_botschaften:
    #     st_nm = sleep_times[str(var)]
    #     if st_nm:
    #         testresult.append(
    #             basic_tests.compare(
    #                 left_value=st_nm,
    #                 operator="<=",
    #                 right_value=nm_stop_s,
    #                 descr="Vergleiche Stop NM Botschaft <= %ss" % nm_stop_s
    #             )
    #         )
    #     else:
    #         testresult.append(["Keine Einschlafzeit für NM-Botschaften gefunden", "FAILED"])
    #
    #     testresult.append( ["\x0a4.2 Applikationsbotschaften: Waehlhebel_04, KN_Waehlhebel, DS_Waehlhebel  werden gesendet", ""])
    #     for var in applikationsbotschaften:
    #         ct = cycle_times[str(var)]
    #         if len(ct) > 0:
    #             testresult.append(["\xa0Prüfe, dass Zykluszeit korrekt ist", ""])
    #             cycle_time = sum(ct) / len(ct)
    #             testresult.append(
    #                 basic_tests.checkTolerance(
    #                     current_value=cycle_time,
    #                     rated_value=messages_cycle_times[str(var)],
    #                     rel_pos=cycletime_tol_perc,
    #                     descr="Zykluszeit von %s" % str(var)))
    #
    #         else:
    #             testresult.append(
    #                 ["Nicht genug Zykluszeiten (%s) gemessen um Zeitpunkt zu analysieren" % str(var), "FAILED"])

    testresult.append(["\x0a7. Schalte KL15 und Restbussimulation an und 350ms warten", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_tx_off_state("an")
    time.sleep(0.350)

    testresult.append(["\x0a8. NM_Waehlhebel Botschaft auslesen", ""])
    # time.sleep(.200)
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 0, descr="NM_Waehlhebel_CBV_AWB:Passiver_WakeUp"))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value, 1, descr="NM_Waehlhebel_CBV_CRI:NM_mit_Clusteranforderungen"))
    #testresult.append(func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [12], [], descr="NM_Waehlhebel_FCAB:12_GearSelector"))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_SNI_10__value, 83, descr="NM_Waehlhebel_SNI_10:Waehlhebel_SNI"))
    #testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value, 0, descr="NM_Waehlhebel_UDS_CC:Inaktiv"))
    testresult.append(_checkStatus(current_status=hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value, nominal_status=0,descr="NM_Waehlhebel_UDS_CC:Inaktiv ist", ticket_id='Fehler Id:EGA-PRM-13'))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value, 1, descr="NM_Waehlhebel_Wakeup_V12:Bus_Wakeup"))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value, 0, descr="NM_Waehlhebel_NM_aktiv_Diag:Inaktiv"))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0, descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv"))
    testresult.append(_checkStatus( current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value, nominal_status=2, descr="NM_RM_aus_PBSM:NM_RM_aus_PBSM ist", ticket_id='Fehler Id:EGA-PRM-13' ))
    #testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value, 1, descr="NM_Waehlhebel_NM_aktiv_KL15:KL15_EIN"))
    testresult.append(func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [12], [],descr="NM_Waehlhebel_FCAB:12_GearSelector"))
    testresult.append(_checkStatus( current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, nominal_status=1, descr="NM_Waehlhebel_NM_aktiv_Tmin:Mindestaktivzeit ist", ticket_id='Fehler Id:EGA-PRM-13'))
    time.sleep(3)

    testresult.append(["\xa0 Stoppe DAQ Messung", "INFO"])
    daq_data3 = daq.stopMeasurement()
    time.sleep(0.1)

    # DAQ Analysis ################################################################
    testresult.append(["\xa0 Analysiere DAQ Messung", "INFO"])

    plot_data = {}
    for mes in applikationsbotschaften + nm_botschaften:
        plot_data[str(mes)] = daq_data3[str(mes)]
    testresult.append(
        daq.plotMultiShot(plot_data, "WakeUp_Kl15_an_PBSM_79")
    )

    testresult.append(["\xa0Werte KL15 Signal aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data3[str(meas_vars[0])],
        filename="WakeUp_Kl15_an_PBSM_79_KL_15",
        label_signal="KL15_AN"
    )
    testresult.append([descr, plot, verdict])
    testresult.append(["\xa0Werte NM Signal aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data3[str(meas_vars[4])],
        filename="WakeUp_Kl15_an_PBSM_79_NM",
        label_signal="KL15_AN"
    )
    testresult.append([descr, plot, verdict])

    #######################################################################################################################
    cl15_data = daq_data3[str(hil.cl15_on__)]
    cl_15_off = eval_signal.EvalSignal(cl15_data)
    cl_15_off.clearAll()
    time_zero = cl_15_off.getTime()

    t_cl_15_data = cl_15_off.findNext("==", 0)  # timestamp when clamp 15 is switched off:
    cl15_idx = cl_15_off.cur_index  # read index
    testresult.append(["Ermittelter Zeitpunkt 'KL15 aus': %s" % (t_cl_15_data - time_zero), "INFO"])
    test_start_time = cl15_data['time'][cl15_idx - 200]

    t_cl_15_on = cl_15_off.findNext("==", 1)
    if t_cl_15_on is not None:
        t_cl_15_on_t = cl_15_off.getTime()

    testresult.append(["Ermittelter Zeitpunkt 'KL15 an': %s" % (t_cl_15_on - time_zero), "INFO"])
    testresult.append(["Zeit zwichen KL15 aus eund KL15 Ein ist %s" %( (t_cl_15_on - time_zero)- (t_cl_15_data - time_zero)), "INFO"])

    # idx_cl15_on = cl_15.cur_index

    daq_data_part11 = copy.deepcopy(daq_data3)
    daq_data_part22 = copy.deepcopy(daq_data3)
    for data1, data2 in zip(daq_data_part11, daq_data_part22):
        daq_data_part11[data1]['data'] = daq_data_part11[data1]['data'][:cl15_idx]
        daq_data_part11[data1]['time'] = daq_data_part11[data1]['time'][:cl15_idx]
        daq_data_part22[data2]['data'] = daq_data_part22[data2]['data'][cl15_idx:]
        daq_data_part22[data2]['time'] = daq_data_part22[data2]['time'][cl15_idx:]

    testresult.append(
        ["\x0a4. Prüfe Versenden (Timestamps/Zykluszeit) der gesendeten Applikations- und NM Botschaften:", ""])

    cycle_times = {}
    sleep_times = {}
    for var in meas_vars:
        if var != hil.cl15_on__:
            cycle_time, sleep_time = func_nm.analyseCycleSleepTimes(
                start_time=test_start_time,
                daq_data=daq_data_part11[str(var)])
            cycle_times[str(var)] = cycle_time
            sleep_times[str(var)] = sleep_time

    testresult.append(["\x0a4.1 Prüfe NM-Botschaften werden nicht gesendet: NM_Waehlhebel keine timestamps", ""])

    for var in nm_botschaften:
        st_nm = sleep_times[str(var)]
        if st_nm:
            testresult.append(
                basic_tests.compare(
                    left_value=st_nm,
                    operator="<=",
                    right_value=nm_stop_s,
                    descr="Vergleiche Stop NM Botschaft <= %ss" % nm_stop_s
                )
            )
        else:
            testresult.append(["Keine Einschlafzeit für NM-Botschaften gefunden", "FAILED"])


    testresult.append(["\x0a4.2 Applikationsbotschaften: Waehlhebel_04, KN_Waehlhebel, DS_Waehlhebel  werden gesendet", ""])
    for var in meas_vars:
        if (var != hil.cl15_on__) and (var != hil.NM_Waehlhebel__timestamp):
            verdict, discription = func_nm.analysisApplicationMessageSent(start_time=t_cl_15_data, name=str(var),
                                                                          daq_data=daq_data3[str(var)],
                                                                          ApplicationsAreSending=True)
            testresult.append([discription, verdict])
            # ct = cycle_times[str(var)]
            # if len(ct) > 0:
            #     testresult.append(["\xa0Prüfe, dass Zykluszeit korrekt ist", ""])
            #     cycle_time = sum(ct) / len(ct)
            #     testresult.append(
            #         basic_tests.checkTolerance(
            #             current_value=cycle_time,
            #             rated_value=messages_cycle_times[str(var)],
            #             rel_pos=cycletime_tol_perc,
            #             descr="Zykluszeit von %s" % str(var)))
            #
            # else:
            #     testresult.append(
            #         ["Nicht genug Zykluszeiten (%s) gemessen um Zeitpunkt zu analysieren" % str(var), "FAILED"])
####################################################################################################################################


    # Check when messages start sending again #####################################
    testresult.append(["\x0a9.  Prüfe Versenden (Timestamps/Zykluszeit) der gesendeten Applikations- und NM Botschaften", ""])
    testresult.append(["\x0a9.1   Prüfe Versenden (Timestamps/Zykluszeit) der gesendeten Applikations- und NM Botschaften", ""])
    wakeup_times = {}
    for var in meas_vars:
        if var != hil.cl15_on__:
            cycle_times, wakeup_time = func_nm.analyseCycleWakeupTimes(
                start_time=t_cl_15_on,
                daq_data=daq_data_part22[str(var)])
            wakeup_times[str(var)] = wakeup_time

            if len(cycle_times) > 0:
                if var == hil.NM_Waehlhebel__timestamp:
                    if len(cycle_times) > 11:
                        testresult.append(["\xa0Prüfe, Zykluszeiten des Signals NM-Botschaft nach erneutem Senden korrekt sind", ""])
                        cycle_time = sum(cycle_times) / len(cycle_times)
                        testresult.append(basic_tests.checkTolerance(current_value=cycle_time, rated_value=messages_cycle_times[str(var)], rel_pos=cycletime_tol_perc, descr="Zykluszeit von %s" % str(var)))
                    else:
                        testresult.append( ["Nicht genug Zykluszeiten aufgezeichnet zum Auswerten", "FAILED"])
                else:
                    testresult.append(["\xa0Prüfe, dass Zykluszeit nach erneutem Senden korrekt ist", ""])
                    cycle_time = sum(cycle_times) / len(cycle_times)
                    testresult.append(basic_tests.checkTolerance( current_value=cycle_time, rated_value=messages_cycle_times[str(var)], rel_pos=cycletime_tol_perc, descr="Zykluszeit von %s" % str(var) ) )
            else:
                testresult.append(
                    ["%s Botschaft beginnt nicht wieder zu senden, nachdem NM_HCP1 wieder sendet" % str(var), "FAILED"])

    testresult.append(["\x0a9.2. Prüfe, dass NM-Botschaften vor der Applikationsbotschaft gesendet wird", ""])

    # Check that NM message is sent as first ##################################
    if ((wakeup_times[str(hil.NM_Waehlhebel__timestamp)] < wakeup_times[str(hil.Waehlhebel_04__timestamp)]) and
        (wakeup_times[str(hil.NM_Waehlhebel__timestamp)] <= wakeup_times[str(hil.DS_Waehlhebel__timestamp)]) and
        (wakeup_times[str(hil.NM_Waehlhebel__timestamp)] <= wakeup_times[str(hil.KN_Waehlhebel__timestamp)])):
        descr = "NM-Botschaft wird zuerst gesendet. \nNM NM_Waehlhebel__timestamp = %s, Waehlhebel_04__timestamp= %s, DS_Waehlhebel__timestamp= %s, KN_Waehlhebel__timestamp = %s" % (
            wakeup_times[str(hil.NM_Waehlhebel__timestamp)], wakeup_times[str(hil.Waehlhebel_04__timestamp)],
            wakeup_times[str(hil.DS_Waehlhebel__timestamp)], wakeup_times[str(hil.KN_Waehlhebel__timestamp)])
        verdict = "PASSED"
    else:
        descr = "NM-Botschaft wird NICHT zuerst gesendet. \nNM NM_Waehlhebel__timestamp = %s, Waehlhebel_04__timestamp= %s, DS_Waehlhebel__timestamp= %s, KN_Waehlhebel__timestamp = %s" % (
            wakeup_times[str(hil.NM_Waehlhebel__timestamp)], wakeup_times[str(hil.Waehlhebel_04__timestamp)],
            wakeup_times[str(hil.DS_Waehlhebel__timestamp)], wakeup_times[str(hil.KN_Waehlhebel__timestamp)])
        verdict = "FAILED"

    testresult.append([descr, verdict])
    testresult.append(["[-0]", ""])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################