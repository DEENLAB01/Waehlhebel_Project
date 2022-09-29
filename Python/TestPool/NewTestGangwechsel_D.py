# ******************************************************************************
# -*- coding: latin1 -*-
# File    : WakeUp_Applikation_NM_HCP1.py
# Title   : WakeUp Applikation NM_HCP1 erst mit gültigem FCAB
# Task    : A minimal "WakeUp_Applikation_NM_HCP1!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name     | Description
# ------------------------------------------------------------------------------
# 1.0  | 15.07.2021 | M. Abdul Karim  | initial
# 1.0  | 28.07.2021 | M. Abdul Karim  | Rework
# ******************************************************************************

import time
from _automation_wrapper_ import TestEnv
from ttk_daq import eval_signal
from ttk_checks import basic_tests
import functions_nm
import functions_gearselection
import copy

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
    tolerance_percent = 0.10
    cycletime_tol_perc = 0.10
    ttimeout = 1.0
    ttimeout_tol_perc = 0.05
    nm_stop_s = 0.4
    t_send_after_wakeup = 0.15  # to be clarified

    meas_vars = [hil.cl15_on__, hil.Waehlhebel_04__timestamp,
                 hil.DS_Waehlhebel__timestamp, hil.KN_Waehlhebel__timestamp,
                 hil.NM_Waehlhebel__timestamp, hil.NM_HCP1__NM_HCP1_FCAB__value]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte KL30 ein (KL15 aus), ", ""])
    hil.cl30_on__.set(1)
    hil.cl15_on__.set(0)

    testresult.append(["Schalte Senden von empfangenen Signalen aus (HiL -> ECU)", "INFO"])
    hil.can0_HIL__HIL_TX__enable.set(0)
    time.sleep(30)

    testresult.append(["[.] Prüfe Busruhe", ""])
    descr, verdict = func_gs.checkBusruhe(daq)
    testresult.append([descr, verdict])

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+0]", ""])

    testresult.append(["[.] Schalte 10xZzykulszeit Senden von NM_HCP1 an", ""])
    testresult.append(["[.] NM_HCP1_01_FCAB senden", ""])
    hil.NM_HCP1__NM_HCP1_FCAB__value.set(1024)  # 11
    testresult.append(["[.] NM_HCP1_01_CBV_CRI senden", ""])
    hil.NM_HCP1__NM_HCP1_CBV_CRI__value.set(1)  # 1
    testresult.append(["Setze NM_Airbag:NM_HCP1__period auf 'an'", "INFO"])
    hil.NM_HCP1__period.setState('an')
    testresult.append(["[.] Warte 10xZzykulszeit (10x200ms=2000ms)", ""])
    time.sleep(2)

    testresult.append(["Setze NM_Airbag:NM_HCP1__period auf 'aus'", "INFO"])
    hil.NM_HCP1__period.setState('aus')

    ## Busruhe  (0mA<I<2mA) prüfen
    testresult.append(["[.] Prüfe, dass nach Busruhe ist", ""])
    time.sleep(.150)
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.0,  # 0mA
            max_value=0.002,  # 2mA
            descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt"
        )
    )

    testresult.append(["[.] Schalte 10xZzykulszeit Senden von NM_HCP1 an", ""])
    testresult.append(["[.] NM_HCP1_01_FCAB senden", ""])
    hil.NM_HCP1__NM_HCP1_FCAB__value.set(2048)  # 12

    testresult.append(["[.] NM_HCP1_01_CBV_CRI senden", ""])
    hil.NM_HCP1__NM_HCP1_CBV_CRI__value.set(1)  # 1
    testresult.append(["Setze NM_HCP1:NM_HCP1__period auf 'an'", "INFO"])
    testresult.append(["[.] Warte 10xZzykulszeit (10x200ms=2000ms)", ""])
    hil.NM_Airbag__period.setState('an')
    time.sleep(2)

    testresult.append(["Setze NM_HCP1:NM_HCP1__period auf 'aus'", "INFO"])
    hil.NM_HCP1__period.setState('aus')

    testresult.append(["[.] Prüfe Werte der Botschaft NM_Waehlhebel", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 0,
                                descr="NM_Waehlhebel_CBV_AWB:Passiver_WakeUp"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value, 1,
                                descr="NM_Waehlhebel_CBV_CRI:NM_mit_Clusteranforderungen"),
        func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [12], [],
                                 descr="NM_Waehlhebel_FCAB:12_GearSelector"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_SNI_10__value, 83,
                                descr="NM_Waehlhebel_SNI_10:Waehlhebel_SNI"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value, 4,
                                descr="NM_Waehlhebel_NM_State:NM_NO_aus_RM"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value, 0,
                                descr="NM_Waehlhebel_UDS_CC:Inaktiv"),
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

    testresult.append(["Zykluszeit messen", ""])
    testresult.append(["\xa0 Stoppe DAQ Messung", "INFO"])
    daq_data = daq.stopMeasurement()
    time.sleep(0.1)

    # DAQ Analysis ################################################################
    testresult.append(["[.] Analysiere DAQ Messung", ""])

    plot_data = {}
    for mes in applikationsbotschaften + nm_botschaften:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(
        daq.plotMultiShot(plot_data, "WakeUp_Applikation_NM_HCP1")
    )

    testresult.append(["\xa0Werte KL15 Signal aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data[str(meas_vars[0])],
        filename="WakeUp_Applikation_NM_HCP1_KL_15",
        label_signal="KL15"
    )
    testresult.append([descr, plot, verdict])

    cl15_data = daq_data[str(hil.cl15_on__)]
    cl_15 = eval_signal.EvalSignal(cl15_data)
    cl_15.clearAll()
    time_zero = cl_15.getTime()
    # find timestamp when clamp 15 is switched off:
    t_cl_15_off = cl_15.findNext("==", 0)
    cl15_idx = cl_15.cur_index  # read index
    testresult.append(["Ermittelter Zeitpunkt 'KL15 aus': %s" % (t_cl_15_off - time_zero), "INFO"])
    test_start_time = cl15_data['time'][cl15_idx - 200]  # go 200ms back (Zykluszeit NM)
    testresult.append(["Start-Zeitpunkt Analyse (200ms vorher): %ss" % (test_start_time - time_zero), "INFO"])

    testresult.append(["\xa0Werte NM_HCP1 Signal aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data[str(meas_vars[5])],
        filename="WakeUp_Applikation_NM_HCP1",
        label_signal="NM_HCP1_FCAB"
    )
    testresult.append([descr, plot, verdict])
    hcp1_mess = eval_signal.EvalSignal(daq_data[str(meas_vars[5])])
    hcp1_mess.clearAll()
    time_zero = hcp1_mess.getTime()
    # find timestamp when HCP1 message is sent:
    t_hcp1_sent = hcp1_mess.findNext("==", 2048)
    testresult.append(["Ermittelter Zeitpunkt 'Senden der NM_HCP1 Botschaft': %s" % (t_hcp1_sent - time_zero), "INFO"])

    idx_hcp1_sent = hcp1_mess.cur_index  # index, when KL15 is switched on
    # prepare daq data for first analyse (behaviour till nm airbag will send)
    daq_data_part1 = copy.deepcopy(daq_data)
    daq_data_part2 = copy.deepcopy(daq_data)
    for data1, data2 in zip(daq_data_part1, daq_data_part2):
        daq_data_part1[data1]['data'] = daq_data_part1[data1]['data'][:idx_hcp1_sent]
        daq_data_part1[data1]['time'] = daq_data_part1[data1]['time'][:idx_hcp1_sent]
        daq_data_part2[data2]['data'] = daq_data_part2[data2]['data'][idx_hcp1_sent:]
        daq_data_part2[data2]['time'] = daq_data_part2[data2]['time'][idx_hcp1_sent:]


    # Check that messages stop sending correctly #####################################
    cycle_times = {}
    sleep_times = {}
    for var in meas_vars:
        if (var != hil.cl15_on__) and (var != hil.NM_HCP1__NM_HCP1_FCAB__value):
            cycle_time, sleep_time = func_nm.analyseCycleSleepTimes(
                start_time=test_start_time,
                daq_data=daq_data_part1[str(var)])
            cycle_times[str(var)] = cycle_time
            sleep_times[str(var)] = sleep_time

    testresult.append(["[+] Prüfe, dass NM-Botschaften %ss nach 'KL15 aus' nicht mehr gesendet werden"%nm_stop_s, ""])
    for var in nm_botschaften:
        st_nm = sleep_times[str(var)]
        if st_nm:
            testresult.append(
                basic_tests.compare(
                    left_value=st_nm,
                    operator="<=",
                    right_value=nm_stop_s,
                    descr = "Vergleiche Stop NM Botschaft <= %ss"%nm_stop_s
                )
            )
        else:
            testresult.append(["Keine Einschlafzeit für NM-Botschaften gefunden", "FAILED"])

        testresult.append(["[.] Prüfe, dass Applikations-Botschaften %ss nach der letzten gesendeten NM-Botschaft"
                           " nicht mehr gesendet werden" %(ttimeout), ""])
        for var in applikationsbotschaften:
            ct = cycle_times[str(var)]
            if len(ct) > 0:
                testresult.append(["\xa0Prüfe, dass Zykluszeit vor dem Einschlafen korrekt ist", ""])
                cycle_time = sum(ct) / len(ct)
                testresult.append(
                    basic_tests.checkTolerance(
                        current_value=cycle_time,
                        rated_value=messages_cycle_times[str(var)],
                        rel_pos=cycletime_tol_perc,
                        descr="Zykluszeit von %s"%str(var)
                    )
                )
                testresult.append(["\xa0Prüfe Einschlafzeit", ""])
                st = sleep_times[str(var)]
                if st and st_nm:
                    testresult.append(
                        basic_tests.checkRange(
                            value=st-st_nm,
                            min_value=ttimeout-(float(messages_cycle_times[str(var)])/1000),
                            max_value = ttimeout + (ttimeout*ttimeout_tol_perc),
                            descr = "Einschlafzeit von %s"%str(var),
                        )
                    )
                else:
                    testresult.append(
                        ["Es wurde keine Einschlafzeit für %s oder für die NM-Botschaft gefunden" % str(var), "FAILED"])
            else:
                testresult.append(["Nicht genug Zykluszeiten (%s) gemessen um Zeitpunkt zu analysieren"%str(var), "FAILED"])

    ## Busruhe  (0mA<I<2mA) prüfen
    testresult.append(["[.] Prüfe, dass nach Busruhe ist", ""])
    time.sleep(.150)
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.0,  # 0mA
            max_value=0.002,  # 2mA
            descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt"
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
    testenv.breakdown()
    # #########################################################################
