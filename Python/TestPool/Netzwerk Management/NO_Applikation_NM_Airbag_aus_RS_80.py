# ******************************************************************************
# -*- coding: latin1 -*-
# File    : NO_Applikation_NM_Airbag_aus_RS_80.py
# Title   : NO Applikation NM Airbag aus RS
# Task    : NO verursacht durch die Applikation (Empfang NM_Airbag Botschaft)
#           aus Ready Sleep-Mode (RM-NO-RS-NO)
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name     | Description
# ------------------------------------------------------------------------------
# 1.0  | 28.01.2021 | Abdul Karim  | initial
# 1.1  | 21.05.2021 | NeumannA     | reworked for updated spec
# 1.2  | 30.06.2021 | NeumannA     | update check of FCAB bit
# 1.3  | 04.08.2021 | Mohammed     | Waehlhebel_NM_State: replace 8 to 4
# 1.4  | 14.10.2021 | Mohammed     |Added Feher ID
# 1.5  | 15.11.2021 | Devangbhai   | Reworked
# 1.6  | 06.12.2021 | Mohammed     | Added NM_Waehlhebel_CBV_AWB:Passiver_WakeUp
# 1.7  | 21.12.2021 | Mohammed     | Added Fehler Id
# 1.8  | 07.01.2022 | Mohammed     | Added NM_Waehlhebel_NM_aktiv_KL15:Aktiv
# 1.9  | 08.03.2022 | Devangbhai   | Removed the unnecessory part from step 4.2
# 1.10  | 16.03.2022 | Devangbhai  | Reworked in test step 7


# ******************************************************************************

# Imports #####################################################################
import time
from _automation_wrapper_ import TestEnv
from ttk_daq import eval_signal
from ttk_checks import basic_tests
import functions_nm
import functions_gearselection
import copy
from functions_nm import _checkStatus

# Instantiate test environmentimport time
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
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    applikationsbotschaften = [hil.Waehlhebel_04__timestamp,
                               hil.DS_Waehlhebel__timestamp, # zykluszeit zu groß für den Test
                               hil.KN_Waehlhebel__timestamp, ]
    nm_botschaften = [hil.NM_Waehlhebel__timestamp]
    nm_airbag = [hil.NM_Airbag__timestamp]
    messages_cycle_times = {str(hil.Waehlhebel_04__timestamp): 10,
                            str(hil.DS_Waehlhebel__timestamp): 1000,
                            str(hil.KN_Waehlhebel__timestamp): 500,
                            str(hil.NM_Waehlhebel__timestamp): 200,
                            str(hil.NM_Airbag__timestamp): 200,
                            }
    cycletime_tol_perc = 0.10
    nm_botschaft_cycle = 200
    nm_botschaft_fast_cycle = 10
    nm_stop_s = 0.4
    ttimeout = 1.0

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_80")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte KL30 an (KL15 aus)", ""])
    testenv.startupECU()
    testresult.append(["Warte 4s (Taktiv_min)", "INFO"])
    time.sleep(4)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    meas_vars = [hil.cl15_on__, hil.Waehlhebel_04__timestamp,
                 hil.DS_Waehlhebel__timestamp, hil.KN_Waehlhebel__timestamp,
                 hil.NM_Waehlhebel__timestamp]

    testresult.append(["Starte DAQ Messung für Applikations- und NM-Botschaften", "INFO"])
    testresult.append(["Folgende Signale werden mitgemessen:\n%s" % meas_vars, "INFO"])
    daq.startMeasurement(meas_vars)
    time.sleep(2)

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
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value, 4,
                                descr="NM_Waehlhebel_NM_State:NM_NO_aus_RM"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value, 1,
                                descr="NM_Waehlhebel_Wakeup_V1:Bus_Wakeup"),
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

    testresult.append(["Stoppe DAQ Messung", "INFO"])
    daq_data1 = daq.stopMeasurement()
    time.sleep(0.1)
    hcp1_mess = eval_signal.EvalSignal(daq_data1[str(meas_vars[4])])
    hcp1_mess.clearAll()
    t_hcp1_sent = hcp1_mess.getTime()

    idx_hcp1_sent = hcp1_mess.cur_index

    daq_data_part1 = copy.deepcopy(daq_data1)
    daq_data_part2 = copy.deepcopy(daq_data1)
    for data1, data2 in zip(daq_data_part1, daq_data_part2):
        daq_data_part1[data1]['data'] = daq_data_part1[data1]['data'][:idx_hcp1_sent]
        daq_data_part1[data1]['time'] = daq_data_part1[data1]['time'][:idx_hcp1_sent]
        daq_data_part2[data2]['data'] = daq_data_part2[data2]['data'][idx_hcp1_sent:]
        daq_data_part2[data2]['time'] = daq_data_part2[data2]['time'][idx_hcp1_sent:]

    testresult.append(
        ["\x0a2. Prüfe Versenden (Timestamps/Zykluszeit) der gesendeten Applikations- und NM Botschaften:", ""])
    for var in meas_vars:
        if (var != hil.cl15_on__):
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


    testresult.append(["Start DAQ Measurement für Zustandsanalyse", "INFO"])
    meas_vars = applikationsbotschaften + nm_botschaften + [hil.cl15_on__, hil.NM_Airbag__period]+ nm_airbag
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["\x0a3. Schalte KL15 und Restbussimulation aus", ""])
    hil.cl15_on__.set(0)
    sleep_time= 0.100
    time.sleep(sleep_time)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(0.150 - sleep_time)
    testresult.append(["\x0a4.  Prüfe Versenden (Timestamps/Zykluszeit) der gesendeten Applikations- und NM Botschaften", ""])
    testresult.append(["Siehe DAQ-Analyse", "INFO"])
    testresult.append(["\x0a5. Warte 500ms", ""])
    time.sleep(0.5)

    testresult.append(["\x0a6.  Setze NM_Airbag_01_FCAB = 2048 (12_GearSelector), starte"
                       "zyklisches Senden der NM_Airbag Botschaft und warte 400ms (2*Zykluszeit)", ""])
    
    hil.NM_Airbag__NM_Airbag_01_FCAB__value.set(2048)
    hil.NM_Airbag__period.setState('an')
    time.sleep(.400)
    testresult.append( ["\x0a 7. Prüfe Versenden (Timestamps/Zykluszeit) der gesendeten Applikations- und NM Botschaften:", ""])
    testresult.append(["Siehe DAQ-Analyse", "INFO"])

    testresult.append(["Warte weitere 2000ms für die DAQ Messung", "INFO"])
    time.sleep(2)
    testresult.append(["Stop DAQ Measurement", ""])
    daq_data = daq.stopMeasurement()
    time.sleep(0.5)

    testresult.append(["\nStart Analyse of DAQ Measurement", ""])

    # search for time, where KL15 switched off (from 1 -> 0)
    cl15_data = daq_data[str(hil.cl15_on__)]
    analyse_cl15_data = eval_signal.EvalSignal(cl15_data)
    analyse_cl15_data.clearAll()
    
    time_zero = analyse_cl15_data.getTime() # start time of measurment
    cl15_off_time = analyse_cl15_data.find(operator="==", value=0) 
    cl15_idx = analyse_cl15_data.cur_index # read index
    test_start_time = cl15_data['time'][cl15_idx-200] # go 200ms back (Zykluszeit NM)
    testresult.append(["KL15 aus Zeitpunkt: %ss" % (cl15_off_time - time_zero), "INFO"])
    testresult.append(["Start-Zeitpunkt Analyse: %ss" % (test_start_time - time_zero), "INFO"])

    # search for end of 1. analyse: NM_Airbag__period set from 0 -> 200
    nm_airbag_data = daq_data[str(hil.NM_Airbag__period)]
    analyse_nm_airbag_data = eval_signal.EvalSignal(nm_airbag_data)
    analyse_nm_airbag_data.clearAll()
    analyse_nm_airbag_data.find(operator="==", value=0)  # change from 200 -> 0
    time_period_on = analyse_nm_airbag_data.findNext(operator="==", value=200)  # change from 0 -> 200
    testresult.append(["Start-Zeitpunkt NM_Airbag sendet wieder: %ss" % (time_period_on - time_zero), "INFO"])

    plot_data = {}
    for mes in applikationsbotschaften + nm_botschaften + nm_airbag:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(
        daq.plotMultiShot(plot_data, "NO_Applikation_NM_Airbag_aus_RS_80", v_lines={1:{'x':cl15_off_time-time_zero, 'label': 'KL15 off'},
                                                                                    2:{'x':test_start_time-time_zero, 'label': 'KL15 off - NM Zykluszeit'},
                                                                                    3:{'x':time_period_on-time_zero, 'label': 'NM Airbag sendet wieder'}})
    )
    # descr, plot, verdict = daq.plotSingleShot(
    #     daq_data=daq_data[str(hil.NM_Airbag__period)],
    #     filename="NM_Airbag__period_80_",
    #     label_signal="NM_Airbag__period_80")
    # testresult.append([descr, plot, verdict])

    if cl15_off_time and time_period_on:
        idx_end = analyse_nm_airbag_data.cur_index
        # prepare daq data for first analyse (behaviour till nm airbag will send)
        daq_data_part1 = copy.deepcopy(daq_data)
        daq_data_part2 = copy.deepcopy(daq_data)
        for data1, data2 in zip(daq_data_part1, daq_data_part2):
            # part 1 for analyse of change from NO into RS
            daq_data_part1[data1]['data'] = daq_data_part1[data1]['data'][:idx_end]
            daq_data_part1[data1]['time'] = daq_data_part1[data1]['time'][:idx_end]
            # part 2 for analyse of change from RS back to NO
            daq_data_part2[data2]['data'] = daq_data_part2[data2]['data'][idx_end:]
            daq_data_part2[data2]['time'] = daq_data_part2[data2]['time'][idx_end:]

        # START ANALYSE PART 1 ################################################
        cycle_times = {}
        sleep_times = {}
        for var in meas_vars:
            if var not in [hil.cl15_on__, hil.NM_Airbag__period]:
                cycle_time, sleep_time = func_nm.analyseCycleSleepTimes(
                    start_time=test_start_time,
                    daq_data=daq_data_part1[str(var)])
                cycle_times[str(var)] = cycle_time
                sleep_times[str(var)] = sleep_time

        testresult.append(["\x0a4.1 Prüfe, dass NM-Botschaften %ss nach KL15 aus "
                           "nicht mehr gesendet werden" % nm_stop_s, ""])
        for var in nm_botschaften:
            st_nm = sleep_times[str(var)]
            if st_nm:
                testresult.append(
                    basic_tests.compare(
                        left_value=st_nm,
                        operator="<=",
                        right_value=nm_stop_s,
                        descr="Vergleiche Stop NM Botschaft (%s) <= %ss" %(str(var), nm_stop_s)
                    )
                )
            else:
                testresult.append(["Keine Einschlafzeit für NM-Botschaft (%s) gefunden"%str(var), "FAILED"])

        testresult.append(["\x0a4.2 Prüfe, dass Applikations-Botschaften noch gesendet werden", ""])
        testresult.append(["[+0]", ""])
        for var in applikationsbotschaften:
           testresult.append(["\xa0 Botschaft %s"%str(var), ""])
           ct = cycle_times[str(var)]
           testresult.append(["\xa0Prüfe, dass Zykluszeit korrekt ist", ""])
           if var == hil.DS_Waehlhebel__timestamp:
               verdict, discription = func_nm.analysisApplicationMessageSent(start_time=test_start_time, name=str(var),
                                                                    daq_data=daq_data_part1[str(var)], ApplicationsAreSending=True)
               testresult.append([discription, verdict])

           else:
               if len(ct) > 0:
                   cycle_time = sum(ct) / len(ct)
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
                       ["Nicht genug Zykluszeiten (%s) gemessen um Zeitpunkt zu analysieren" % str(var), "FAILED"])

        # START ANALYSE PART 2 ################################################
        testresult.append(["\x0a 7.1 Applikationsbotschaften: Waehlhebel_04, KN_Waehlhebel, DS_Waehlhebel (wird versendet)", ""])
        signal_data = daq_data_part2[str(hil.NM_Waehlhebel__timestamp)]
        analyse_signal_data = eval_signal.EvalSignal(signal_data)
        analyse_signal_data.clearAll()

        timestamp = analyse_signal_data.getData()  # timestamp at the beginning of measurement

        for var in meas_vars:
            if var == hil.NM_Waehlhebel__timestamp:
                verdict, discription = func_nm.analysisNmMessageSent(start_time=cl15_off_time, name=str(var),
                                                                     daq_data=daq_data[str(var)], NMAreSending=False)
                testresult.append([discription, verdict])
        testresult.append(["\x0a 7.2 NM-Botschaft: NM_Waehlhebel (wird nicht versendet)", ""])
        for var in applikationsbotschaften:
            verdict, discription = func_nm.analysisApplicationMessageSent(start_time=cl15_off_time, name=str(var),
                                                                          daq_data=daq_data[str(var)],
                                                                          ApplicationsAreSending=True)
            testresult.append([discription, verdict])
        # if timestamp:
        #     cycletimes = []
        #     while timestamp:
        #         t = analyse_signal_data.findNext(">", timestamp)
        #         if t:
        #             next_timestamp = analyse_signal_data.getData()
        #             cycletimes.append((next_timestamp - timestamp))
        #             timestamp = next_timestamp
        #         else:
        #             break
        #     if len(cycletimes) > 3:
        #         testresult.append(["NM-Botschaften werden gesendet: NM_Waehlhebel", "FAILED"])
        #
        #     if len(cycletimes) == 0:
        #         testresult.append(
        #             ["NM-Botschaften werden nicht gesendet: NM_Waehlhebel", "PASSED"])
        #     else:
        #         testresult.append(
        #             ["Nicht genug Zykluszeiten aufgezeichnet zum Auswerten (min. 12 - 10 fast, 2 normal)", "FAILED"])
        # else:
        #     testresult.append(
        #         ["Keine Auswertung der Zykluszeiten möglich, da keine DAQ Daten vorhanden sind", "FAILED"])
    else:
        descr = ""
        if cl15_off_time is None:
            descr += ">> Zeitpunkt, an dem KL15 auf 0 wechselt wurde nicht gefunden\n"
        if time_period_on is None:
            descr += ">> Zeitpunkt, an dem NM_Airbag wieder sendet wurde nicht gefunden"
        testresult.append([descr, "FAILED"])

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