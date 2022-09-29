# ******************************************************************************
# -*- coding: latin1 -*-
# File    : WakeUp_Applikation_NM_HCP1.py
# Title   : WakeUp Applikation NM_HCP1 erst mit gültigem FCAB
# Task    : WakeUp durch die Applikation (Empfang NM_HCP1 Botschaft) erst mit gültigem FCAB
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name     | Description
# ------------------------------------------------------------------------------
# 1.0  | 15.07.2021 | Mohammed   | initial
# 1.0  | 28.07.2021 | Mohammed   | Rework
# 1.1  | 13.09.2021 | Devangbhai Patel | Rework line 124
# 1.2  | 07.10.2021 | Mohammed     | Added Fehler Id
# 1.3  | 09.11.2021 | Devangbhai   | Reworked
# 1.4  | 18.11.2021 | Devangbhai   | Reworked
# 1.5  | 10.12.2021 | Devangbhai   | Reworked
# 1.6  | 21.12.2021 | Mohammed     | Added Fehler Id
# 1.7  | 08.03.2022 | Devangbhai   | Removed 20ms cycle time
# 1.8  | 28.03.2022 | Mohammed     | Added FCAB Fehler Id
# 1.9  | 27.07.2022 | Mohammed     | Added FCAB New Value
# ******************************************************************************

import time
from _automation_wrapper_ import TestEnv
from ttk_daq import eval_signal
from ttk_checks import basic_tests
import functions_nm
import functions_gearselection
import copy
from time import time as t
from functions_nm import _checkStatus

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_113")

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
    tolerance_percent = 0.15
    cycletime_tol_perc = 0.15
    ttimeout = 1.0
    ttimeout_tol_perc = 0.08
    nm_stop_s = 0.4
    t_send_after_wakeup = 0.17 + 0.13 # TODO added the 0.13 sec for the possibility check

    meas_vars = [hil.cl15_on__, hil.Waehlhebel_04__timestamp,
                 hil.DS_Waehlhebel__timestamp, hil.KN_Waehlhebel__timestamp,
                 hil.NM_Waehlhebel__timestamp, hil.NM_HCP1__NM_HCP1_FCAB__value]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte KL30 ein (KL15 aus), ", ""])
    hil.cl30_on__.set(1)
    hil.cl15_on__.set(0)
    hil.can0_HIL__HIL_TX__enable.set(1)
    testresult.append(["Schalte Senden von empfangenen Signalen aus (HiL -> ECU)", "INFO"])
    func_nm.hil_ecu_tx_off_state("aus")
    time.sleep(10)



    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+0]", ""])

    testresult.append(["\x0a1. Prüfe Busruhe", ""])
    descr, verdict = func_gs.checkBusruhe(daq, meas_time=2)
    testresult.append([descr, verdict])

    testresult.append(["\xa0Starte DAQ Messung für Applikations- und NM-Botschaften", "INFO"])
    testresult.append(["Folgende Signale werden mitgemessen:\n%s" % meas_vars, ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(
        ["\x0a2. NM_HCP1-Botschaft mit Signal NM_HCP1_01_CBV_CRI = 1 und NM_HCP1_01_FCAB = 11_Chassis 10x senden", ""])
    time_to_check = 1.9
    t_out = time_to_check + t()
    timestamp = []

    hil.NM_HCP1__NM_HCP1_FCAB__value.set(1024)
    hil.NM_HCP1__NM_HCP1_CBV_CRI__value.set(1)
    hil.NM_HCP1__period.setState('an')
    hil.NM_HCP1__NM_HCP1_FCAB__value.set(1024)
    hil.NM_HCP1__NM_HCP1_CBV_CRI__value.set(1)

    while t_out > t():
        d = hil.NM_HCP1__timestamp.get()
        if len(timestamp) == 0 or timestamp[-1] != d:
            timestamp.append(d)
    hil.NM_HCP1__period.setState("aus")

    # testresult.append(["Prüfe, dass nach Busruhe ist", "INFO"])
    # testresult.append(basic_tests.checkRange(value=hil.cc_mon__A.get(), min_value=0.0, max_value=0.002,
    #                                          descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt"))
    #
    # testresult.append(["Prüfe keine Botschaften werden gesendet", "INFO"])
    # descr, verdict = func_gs.checkBusruhe(daq, meas_time=1)
    # testresult.append([descr, verdict])
    #
    # testresult.append([
    #                       "\x0a2.1 NM_HCP1-Botschaft mit Signal NM_HCP1_01_CBV_CRI = 1 und NM_HCP1_01_FCAB = 12_GearSelector 10x senden, CAN-Traceverlauf auswerten",
    #                       ""])
    # time_to_check = 1.9
    # t_out = time_to_check + t()
    # timestamp = []
    #
    # testresult.append(["Starte DAQ Messung für Applikations- und NM-Botschaften", ""])
    # testresult.append(["Folgende Signale werden mitgemessen:\n%s" % meas_vars, ""])
    # daq.startMeasurement(meas_vars)
    #
    # hil.NM_HCP1__NM_HCP1_FCAB__value.set(2048)
    # hil.NM_HCP1__NM_HCP1_CBV_CRI__value.set(1)
    # hil.NM_HCP1__period.setState('an')
    # hil.NM_HCP1__NM_HCP1_FCAB__value.set(2048)
    # hil.NM_HCP1__NM_HCP1_CBV_CRI__value.set(1)
    #
    # while t_out > t():
    #     d = hil.NM_HCP1__timestamp.get()
    #     if len(timestamp) == 0 or timestamp[-1] != d:
    #         timestamp.append(d)
    # hil.NM_HCP1__period.setState("aus")
    #
    testresult.append(["Prüfe Werte der Botschaft NM_Waehlhebel", "INFO"])
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 0,
                                              descr="NM_Waehlhebel_CBV_AWB:Passiver_WakeUp"))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value, 1,
                                              descr="NM_Waehlhebel_CBV_CRI:NM_mit_Clusteranforderungen"))
    # testresult.append(func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [12], [],
    #                                            descr="NM_Waehlhebel_FCAB:12_GearSelector", ticket_id='Fehler-Id: EGA-PRM-19'))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value, 0,
                                              descr="NM_Waehlhebel_FCAB:Inaktiv"))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_SNI_10__value, 83,
                                              descr="NM_Waehlhebel_SNI_10:Waehlhebel_SNI"))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value, 1,
                                              descr="NM_Waehlhebel_NM_State:NM_RM_aus_BSM"))
    #testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value, 0,
     #                                         descr="NM_Waehlhebel_UDS_CC:Inaktiv"))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value, 1,
                                              descr="NM_Waehlhebel_Wakeup_V12:Bus_Wakeup"))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value, 0,
                                              descr="NM_Waehlhebel_NM_aktiv_KL15:Inaktiv"))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value, 0,
                                              descr="NM_Waehlhebel_NM_aktiv_Diag:Inaktiv"))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1,
                                              descr="NM_Waehlhebel_NM_aktiv_Tmin:Mindestaktivzeit"))
    testresult.append(basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                              descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv"))
    testresult.append(_checkStatus(current_status=hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value, nominal_status=0,
                                   descr="Prüfe NM_Waehlhebel:NM_Waehlhebel_UDS_CC = 0 (inaktiv) ist",
                                   ticket_id='FehlerId:EGA-PRM-19'))

    testresult.append(["Zykluszeit messen", "INFO"])
    testresult.append(["Warte 4000ms", "INFO"])
    time.sleep(4)

    testresult.append(["Warte 1000ms", "INFO"])
    time.sleep(1)

    testresult.append(["Warte 750ms", "INFO"])
    time.sleep(0.75)

    testresult.append(["Prüfe, dass nach Busruhe ist", "INFO"])
    temp_value = func_nm.low_current()

    testresult.append(["Stoppe DAQ Messung", "INFO"])
    daq_data = daq.stopMeasurement()
    time.sleep(0.1)

    plot_data = {}
    for mes in applikationsbotschaften + nm_botschaften:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(daq.plotMultiShot(plot_data, "WakeUp_Applikation_NM_HCP1_113"))

    nm_data = {}
    for mes in nm_botschaften:
        nm_data[str(mes)] = daq_data[str(mes)]
    testresult.append(daq.plotMultiShot(nm_data, "NM_Waehlhebel__timestamp_113"))


    hcp1_mess = eval_signal.EvalSignal(daq_data[str(meas_vars[5])])
    hcp1_mess.clearAll()
    time_zero = hcp1_mess.getTime()
    # find timestamp when HCP1 message is sent:
    t_hcp1_sent = hcp1_mess.findNext("==", 1024)

    testresult.append(["Ermittelter Zeitpunkt 'Senden der NM_HCP1 Botschaft': %s" % (t_hcp1_sent - time_zero), "INFO"])

    idx_hcp1_sent = hcp1_mess.cur_index

    daq_data_part1 = copy.deepcopy(daq_data)
    daq_data_part2 = copy.deepcopy(daq_data)
    for data1, data2 in zip(daq_data_part1, daq_data_part2):
        daq_data_part1[data1]['data'] = daq_data_part1[data1]['data'][:idx_hcp1_sent]
        daq_data_part1[data1]['time'] = daq_data_part1[data1]['time'][:idx_hcp1_sent]
        daq_data_part2[data2]['data'] = daq_data_part2[data2]['data'][idx_hcp1_sent:]
        daq_data_part2[data2]['time'] = daq_data_part2[data2]['time'][idx_hcp1_sent:]

    testresult.append(["\x0a2.2 Zykluszeit messen", ""])
    wakeup_times = {}
    for var in meas_vars:
        if (var != hil.cl15_on__) and (var != hil.NM_HCP1__NM_HCP1_FCAB__value):
            cycle_times, wakeup_time = func_nm.analyseCycleWakeupTimes(
                start_time=t_hcp1_sent,
                daq_data=daq_data_part2[str(var)])
            wakeup_times[str(var)] = wakeup_time

            # if wakeup_time:
            #     testresult.append(
            #         ["\xa0Prüfe, dass Botschaft %s nach 'Senden der NM_HCP1 Botschaft' gesendet wird" % str(var),
            #          ""])
            #     testresult.append(
            #         basic_tests.checkRange(
            #             value=wakeup_time,
            #             min_value=0,  # 0 means 'immediately'
            #             max_value=0 + t_send_after_wakeup,
            #             descr="Zeit von %s senden " % str(var),
            #         )
            #     )
            # else:
            #     testresult.append(
            #         ["%s beginnt nach 'Senden der NM_HCP1 Botschaft' nicht wieder an zu senden" % str(var), "FAILED"])

            if len(cycle_times) > 0:
                if var == hil.NM_Waehlhebel__timestamp:
                    if len(cycle_times) > 11:
                        # testresult.append(
                        #     ["\xa0Prüfe, dass erste 10 Zykluszeiten nach erneutem Senden korrekt sind", ""])
                        # cycle_times_first_10 = cycle_times[:10]
                        # cycle_time = sum(cycle_times_first_10) / len(cycle_times_first_10)
                        # testresult.append(
                        #     basic_tests.checkTolerance(
                        #         current_value=cycle_time,
                        #         rated_value=messages_cycle_times[str(var)] / 10,
                        #         rel_pos=cycletime_tol_perc,
                        #         descr="Zykluszeit von %s" % str(var)
                        #     )
                        # )
                        testresult.append(["\xa0Prüfe, dass Zykluszeiten korrekt sind", ""])
                        # cycle_times_next = cycle_times[10:]
                        cycle_time = sum(cycle_times) / len(cycle_times)
                        testresult.append(
                            basic_tests.checkTolerance(
                                current_value=cycle_time,
                                rated_value=messages_cycle_times[str(var)],
                                rel_pos=cycletime_tol_perc,
                                descr="Zykluszeit von %s" % str(var)
                            )
                        )
                    else:
                        testresult.append(
                            ["Nicht genug Zykluszeiten aufgezeichnet zum Auswerten",
                             "FAILED"])
                else:
                    testresult.append(["\xa0Prüfe, dass Zykluszeit nach erneutem Senden korrekt ist", ""])
                    cycle_time = sum(cycle_times) / len(cycle_times)
                    testresult.append(
                        basic_tests.checkTolerance(
                            current_value=cycle_time,
                            rated_value=messages_cycle_times[str(var)],
                            rel_pos=cycletime_tol_perc,
                            descr="Zykluszeit von %s" % str(var)
                        )
                    )
            else:
                testresult.append(
                    ["%s Botschaft beginnt nicht wieder zu senden, nachdem NM_HCP1 wieder sendet" % str(var), "FAILED"])

    testresult.append(["\xa0Prüfe, dass NM-Botschaften vor der Applikationsbotschaft gesendet wird", "INFO"])

    # Check that NM message is sent as first ##################################
    if ((wakeup_times[str(hil.NM_Waehlhebel__timestamp)] < wakeup_times[str(hil.Waehlhebel_04__timestamp)]) and
            (wakeup_times[str(hil.NM_Waehlhebel__timestamp)] <= wakeup_times[str(hil.DS_Waehlhebel__timestamp)]) and
            (wakeup_times[str(hil.NM_Waehlhebel__timestamp)] <= wakeup_times[str(hil.KN_Waehlhebel__timestamp)])):
        ddescr = "NM-Botschaft wird zuerst gesendet:.\nNM NM_Waehlhebel__timestamp = %s, Waehlhebel_04__timestamp= %s, DS_Waehlhebel__timestamp= %s, KN_Waehlhebel__timestamp = %s" % (wakeup_times[str(hil.NM_Waehlhebel__timestamp)], wakeup_times[str(hil.Waehlhebel_04__timestamp)],wakeup_times[str(hil.DS_Waehlhebel__timestamp)], wakeup_times[str(hil.KN_Waehlhebel__timestamp)])
        verdict = "PASSED"
    else:
        descr = "NM-Botschaft wird NICHT zuerst gesendet. \nNM NM_Waehlhebel__timestamp = %s, Waehlhebel_04__timestamp= %s, DS_Waehlhebel__timestamp= %s, KN_Waehlhebel__timestamp = %s" % (
        wakeup_times[str(hil.NM_Waehlhebel__timestamp)], wakeup_times[str(hil.Waehlhebel_04__timestamp)],
        wakeup_times[str(hil.DS_Waehlhebel__timestamp)], wakeup_times[str(hil.KN_Waehlhebel__timestamp)])
        verdict = "FAILED"
    testresult.append([descr, verdict])

    testresult.append(["\x0a2.3 Warte 4000ms", ""])
    testresult.append(["\x0a3.1 CAN-Traceverlauf erneut auswerten", ""])

    for var in meas_vars:
        if var == hil.NM_Waehlhebel__timestamp:
            verdict, discription = func_nm.analysisNmMessageSent(start_time=t_hcp1_sent + 4, name=str(var),
                                                                 daq_data=daq_data_part2[str(var)], NMAreSending=False)
            testresult.append([discription, verdict])

        elif (var != hil.cl15_on__) and (var != hil.NM_HCP1__NM_HCP1_FCAB__value) and (
                var != hil.NM_Waehlhebel__timestamp):
            verdict, discription = func_nm.analysisApplicationMessageSent(start_time=t_hcp1_sent + 4, name=str(var),
                                                                          daq_data=daq_data_part2[str(var)],
                                                                          ApplicationsAreSending=True)
            testresult.append([discription, verdict])

    testresult.append(["\x0a3.2 Warte 1000ms", ""])
    testresult.append(["\x0a4.1 CAN-Traceverlauf erneut auswerten", ""])
    for var in meas_vars:
        if var == hil.NM_Waehlhebel__timestamp:
            verdict, discription = func_nm.analysisNmMessageSent(start_time=t_hcp1_sent + 4 + 1, name=str(var),
                                                                 daq_data=daq_data_part2[str(var)], NMAreSending=False)
            testresult.append([discription, verdict])

        elif (var != hil.cl15_on__) and (var != hil.NM_HCP1__NM_HCP1_FCAB__value) and (
                var != hil.NM_Waehlhebel__timestamp):
            verdict, discription = func_nm.analysisApplicationMessageSent(start_time=t_hcp1_sent + 4 + 1, name=str(var),
                                                                          daq_data=daq_data_part2[str(var)],
                                                                          ApplicationsAreSending=False)
            testresult.append([discription, verdict])

    testresult.append(["\x0a4.2 Warte 750ms", ""])
    testresult.append(["\x0a5 CAN-Traceverlauf erneut auswerten", ""])
    for var in meas_vars:
        if var == hil.NM_Waehlhebel__timestamp:
            verdict, discription = func_nm.analysisNmMessageSent(start_time=t_hcp1_sent + 4 + 1 + 0.750, name=str(var),
                                                                 daq_data=daq_data_part2[str(var)], NMAreSending=False)
            testresult.append([discription, verdict])

        elif (var != hil.cl15_on__) and (var != hil.NM_HCP1__NM_HCP1_FCAB__value) and (
                var != hil.NM_Waehlhebel__timestamp):
            verdict, discription = func_nm.analysisApplicationMessageSent(start_time=t_hcp1_sent + 4 + 1+ 0.750, name=str(var),
                                                                          daq_data=daq_data_part2[str(var)],
                                                                          ApplicationsAreSending=False)
            testresult.append([discription, verdict])
    testresult.append(["\xa0 Prüfe, dass Strom zwischen 0mA und 2mA liegt", ""])
    testresult.append(basic_tests.checkRange(value=temp_value / 1000,
                                             min_value=0.0,  # 0mA
                                             max_value=0.002,  # 2mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt"))


    #testresult.append(busruhe_after)

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=False, all_other_send=False)

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################
