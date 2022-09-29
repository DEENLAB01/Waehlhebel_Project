# ******************************************************************************
# -*- coding: latin1 -*-
# File    : BSM_aus_NO_76.py
# Title   : BSM aus NO
# Task    : Wechsel in den Sleepmodus aus NO durch Wegfall der Kl15-Wachhaltebedingung
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name     | Description
# ------------------------------------------------------------------------------
# 1.0  | 20.01.2021 | Abdul Karim  | initial
# 1.1  | 13.04.2021 | Abdul Karim  | added Busruhe Signals
# 1.2  | 20.05.2021 | NeumannA | update Spec and script
# 1.3  | 30.06.2021 | NeumannA | update check of FCAB bit
# 1.4  | 09.09.2021 | Mohammed     | Added Fehler Id
# 1.5  | 24.11.2021 | Devangbhai   | Reworked
# 1.6  | 21.12.2021 | Mohammed     | Added Fehler Id
# 1.7  | 07.02.2022 | Mohammed     | Added Strommonitoring
# 1.8  | 14.03.2022 | Devangbhai   | Changed to check cycle time in test step 3 to check if the Alpplication messages are sending

# ******************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_daq import eval_signal
import functions_nm
import time
import functions_gearselection
from ttk_checks import basic_tests
from functions_nm import _checkStatus, _checkRange
import copy

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
                               hil.DS_Waehlhebel__timestamp,
                               hil.KN_Waehlhebel__timestamp,]

    nm_botschaften = [hil.NM_Waehlhebel__timestamp]
    messages_cycle_times = {str(hil.Waehlhebel_04__timestamp): 10,
                            str(hil.DS_Waehlhebel__timestamp): 1000,
                            str(hil.KN_Waehlhebel__timestamp): 500,
                            str(hil.NM_Waehlhebel__timestamp): 200,
                            }
    cycletime_tol_perc = 0.10
    ttimeout = 1.0
    ttimeout_tol_perc = 0.05
    nm_stop_s = 0.4

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_76")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte KL30 und KL15 an und Warte 4 Sekund ", ""])
    testenv.startupECU()
    time.sleep(4)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    meas_vars = applikationsbotschaften + nm_botschaften + [hil.cl15_on__]

    testresult.append(["\xa0Start DAQ Measurement für Zustandsanalyse", ""])
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
                                descr="NM_Waehlhebel_NM_State:NM_NO_aus_RM oder NM_NO_aus_RS"), # added
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value, 1,
                                descr="NM_Waehlhebel_Wakeup_V12:Bus_Wakeup"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value, 1,
                                descr="NM_Waehlhebel_NM_aktiv_KL15:KL15_EIN"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value, 0,
                                descr="NM_Waehlhebel_NM_aktiv_Diag_:Inaktiv"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 0,
                                descr="NM_Waehlhebel_NM_aktiv_Tmin:Inaktiv"),
    ]
    testresult.append( _checkStatus(current_status=hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value, nominal_status=0, descr="Prüfe NM_Waehlhebel:NM_Waehlhebel_UDS_CC = 0 (inaktiv) ist", ticket_id='FehlerId:EGA-PRM-148'))
    time.sleep(2)

    testresult.append(["Stoppe DAQ Messung", "INFO"])
    daq_data = daq.stopMeasurement()
    time.sleep(0.1)
    NM_mess = eval_signal.EvalSignal(daq_data[str(hil.NM_Waehlhebel__timestamp)])
    NM_mess.clearAll()
    t_hcp1_sent = NM_mess.getTime()

    idx_hcp1_sent = NM_mess.cur_index

    daq_data_part1 = copy.deepcopy(daq_data)
    daq_data_part2 = copy.deepcopy(daq_data)
    for data1, data2 in zip(daq_data_part1, daq_data_part2):
        daq_data_part1[data1]['data'] = daq_data_part1[data1]['data'][:idx_hcp1_sent]
        daq_data_part1[data1]['time'] = daq_data_part1[data1]['time'][:idx_hcp1_sent]
        daq_data_part2[data2]['data'] = daq_data_part2[data2]['data'][idx_hcp1_sent:]
        daq_data_part2[data2]['time'] = daq_data_part2[data2]['time'][idx_hcp1_sent:]

    testresult.append(
        ["\x0aPrüfe Versenden (Timestamps/Zykluszeit) der gesendeten Applikations- und NM Botschaften:", "INFO"])
    for var in meas_vars:
        if var != hil.cl15_on__:
            cycle_times, wakeup_time = func_nm.analyseCycleSleepTimes(start_time=t_hcp1_sent, daq_data=daq_data_part2[str(var)])
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

    testresult.append(["\xa0Start DAQ Measurement für Zustandsanalyse", ""])


    daq.startMeasurement(meas_vars)
    time.sleep(2)
    testresult.append(["\x0a2. Schalte KL15 und Restbussimulation aus", ""])
    hil.cl15_on__.set(0)
    time_sleep = 0.005
    time.sleep(time_sleep)
    func_nm.hil_ecu_tx_off_state("aus")
    # hil.can0_HIL__HIL_TX__enable.set(0)
    time.sleep(0.15 - time_sleep)

    testresult.append(["\x0a3. Timestamps/Zykluszeiten der gesendeten Applikations- und NM Botschaften auswerten", ""])
    testresult.append(["Siehe DAQ-Analyse", "INFO"])

    testresult.append(["\x0a4. Warte T Timeout: 1000ms", ""])
    time.sleep(1)

    testresult.append(["\x0a5. Warte T WaitBusSleep: 750ms", ""])
    time.sleep(0.75)

##################### Measurement of the Current
    # hil.error_type.set(5)
    # time.sleep(2)
    # hil.N1SRC_ReqData__trigger.set(0)
    # hil.N1SRC_ReqData__trigger.set(1)
    # time.sleep(.100)
    # temp_value = hil.N1SRC_Measurement_Low__CurrentLow__value.get()*(0.00847711)
    temp_value = func_nm.low_current()
    testresult.append(["\x0a6. Botschaftsein- und ausgänge prüfen", ""])
    time.sleep(5)
    testresult.append(_checkRange( value= temp_value/1000,
            min_value=0.0,  # 0mA
            max_value=0.002,  # 2mA
            descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt",
                                   ticket_id="Fehler Id:EGA-PRM-237"))
    # hil.error_type.set(0)

    ##################### End of the Measurement of Current

    # testresult.append(["\x0a6. Botschaftsein- und ausgänge prüfen", ""])
    # testresult.append(basic_tests.checkRange( value= hil.cc_mon__A.get(),
    #         min_value=0.0,  # 0mA
    #         max_value=0.002,  # 2mA
    #         descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt" ))

    testresult.append(["Siehe DAQ-Analyse für Busruhe", "INFO"])
    time.sleep(1) # TODO why sleep time #

    testresult.append(["Stopp DAQ Measurement", ""])
    daq_data = daq.stopMeasurement()
    time.sleep(0.5)

    testresult.append(["\nStart Analyse of DAQ Measurement", ""])
    plot_data = {}
    for mes in applikationsbotschaften+nm_botschaften:
        plot_data[str(mes)] = daq_data[str(mes)]

    cl15_data = daq_data[str(hil.cl15_on__)]
    analyse_cl15_data = eval_signal.EvalSignal(cl15_data)
    analyse_cl15_data.clearAll()
    time_zero = analyse_cl15_data.getTime()
    cl15_off_time = analyse_cl15_data.find(operator="==", value=0)
    testresult.append(["KL15 aus Zeitpunkt: %ss"%(cl15_off_time-time_zero), "INFO"])

    testresult.append(
        daq.plotMultiShot(plot_data, "BSM_aus_NO_76", v_lines={1: {'x': cl15_off_time-time_zero, 'label': 'KL15 off'}})
    )

    cycle_times = {}
    sleep_times = {}
    for var in meas_vars:
        if var != hil.cl15_on__:
            cycle_time, sleep_time = func_nm.analyseCycleSleepTimes(
                start_time=cl15_off_time,
                daq_data=daq_data[str(var)])
            cycle_times[str(var)] = cycle_time
            sleep_times[str(var)] = sleep_time

    testresult.append(["\x0a3. Timestamps/Zykluszeiten der gesendeten Applikations- und NM Botschaften auswerten", ""])
    for var in meas_vars:
        if var == hil.NM_Waehlhebel__timestamp:
            verdict, discription = func_nm.analysisNmMessageSent(start_time=cl15_off_time, name=str(var),
                                                                 daq_data=daq_data[str(var)], NMAreSending=False)
            testresult.append([discription, verdict])

        elif (var != hil.cl15_on__) and (
                var != hil.NM_Waehlhebel__timestamp):
            verdict, discription = func_nm.analysisApplicationMessageSent(start_time=cl15_off_time, name=str(var),
                                                                          daq_data=daq_data[str(var)],
                                                                          ApplicationsAreSending=True)
            testresult.append([discription, verdict])

    # for var in nm_botschaften:
    #     st_nm = sleep_times[str(var)]
    #     # if st_nm:
    #     #     testresult.append(
    #     #         basic_tests.compare(
    #     #             left_value=st_nm,
    #     #             operator="<=",
    #     #             right_value=nm_stop_s,
    #     #             descr = "Vergleiche Stop NM Botschaft <= %ss"%nm_stop_s
    #     #         )
    #     #     )
    #     # else:
    #     #     testresult.append(["Keine Einschlafzeit für NM-Botschaften gefunden", "FAILED"])
    #
    #     testresult.append(["\x0a3. Prüfe, dass Applikations-Botschaften %ss nach der letzten gesendeten NM-Botschaft"
    #                        " nicht mehr gesendet werden" %(ttimeout), ""])
    #     for var in applikationsbotschaften:
    #         ct = cycle_times[str(var)]
    #         if len(ct) > 0:
    #             testresult.append(["\xa0Prüfe, dass Zykluszeit vor dem Einschlafen korrekt waren", ""])
    #             cycle_time = sum(ct) / len(ct)
    #             testresult.append(
    #                 basic_tests.checkTolerance(
    #                     current_value=cycle_time,
    #                     rated_value=messages_cycle_times[str(var)],
    #                     rel_pos=cycletime_tol_perc,
    #                     descr="Zykluszeit von %s"%str(var)
    #                 )
    #             )
    #             testresult.append(["\xa0Prüfe Einschlafzeit", ""])
    #             st = sleep_times[str(var)]
    #             # if st_nm:
    #             if st:
    #                 testresult.append(
    #                     basic_tests.checkRange(
    #                         value=st,
    #                         min_value=ttimeout-(float(messages_cycle_times[str(var)])/1000),
    #                         max_value = ttimeout + (ttimeout*ttimeout_tol_perc),
    #                         descr = "Einschlafzeit von %s"%str(var),
    #                     )
    #                 )
    #             else:
    #                 testresult.append(["Keine Einschlafzeit der Applikationsbotschaft gefunden", "FAILED"])
    #             # else:
    #             #     testresult.append(["Keine Einschlafzeit für NM-Botschaften gefunden", "FAILED"])
    #         else:
    #             testresult.append(["Nicht genug Zykluszeiten (%s) gemessen um Zeitpunkt zu analysieren"%str(var), "FAILED"])

    testresult.append(["\x0a6. Botschaftsein- und ausgänge prüfen", ""])
    for var in meas_vars:
        if var == hil.NM_Waehlhebel__timestamp:
            verdict, discription = func_nm.analysisNmMessageSent(start_time=cl15_off_time + 1.9, name=str(var),
                                                                 daq_data=daq_data[str(var)], NMAreSending=False)
            testresult.append([discription, verdict])

        elif (var != hil.cl15_on__) and (
                var != hil.NM_Waehlhebel__timestamp):
            verdict, discription = func_nm.analysisApplicationMessageSent(start_time=cl15_off_time + 1.9, name=str(var),
                                                                          daq_data=daq_data[str(var)],
                                                                          ApplicationsAreSending=False)
            testresult.append([discription, verdict])

    # testresult.append(["[.] Prüfe Busruhe", ""])
    # descr, verdict = func_gs.checkBusruhe(daq)
    # testresult.append([descr, verdict])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])

    func_nm.hil_ecu_tx_off_state("an")
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

