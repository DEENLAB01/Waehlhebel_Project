# #******************************************************************************
# # -*- coding: latin1 -*-
# # File    : WakeUp_Applikation_NM_Airbag_aus_PBSM_77.py
# # Title   : WakeUp Applikation NM_Airbag aus PBSM
# # Task    : A minimal "WakeUp_Applikation_NM_Airbag_aus_PBSM!" test script
# #
# # Copyright 2020 Eissmann Automotive Deutschland GmbH
# #
# #******************************************************************************
# #********************************* Version ************************************
# #******************************************************************************
# # Rev. | Date       | Name     | Description
# #------------------------------------------------------------------------------
# # 1.0  | 21.01.2021 | Mohammed     | initial
# # 1.1  | 02.06.2021 | StengerS     | reworked
# # 1.2  | 30.06.2021 | NeumannA     | evaluation of FCAB Value updated
# # 1.3  | 30.07.2021 | Mohammed     | Added 2.1 and 2.2 TestSteps
# # 1.4  | 09.09.2021 | Mohammed     | Added Fehler Id
# #******************************************************************************
#
# import time
# from _automation_wrapper_ import TestEnv
# from ttk_daq import eval_signal
# from ttk_checks import basic_tests
# import functions_nm
# import functions_gearselection
# import copy
# from time import time as t
# from functions_nm import _checkStatus
#
# # Instantiate test environment
# testenv = TestEnv()
#
#
# def check_cycletime(sec, application_msg=True, nm_msg=True, check_20_cycle_NM_WH=False):
#     Waehlhebel_04__timestamp_list = []
#     DS_Waehlhebel__timestamp_list = []
#     KN_Waehlhebel__timestamp_list = []
#     NM_Waehlhebel__timestamp_list = []
#     check_20_cycle_NM_WH_list = []
#
#     timeout = sec + t()
#
#     while timeout > t():
#         timestamp_Waehlhebel_04 = hil.Waehlhebel_04__timestamp.get()
#         timestamp_DS_Waehlhebel = hil.DS_Waehlhebel__timestamp.get()
#         timestamp_KN_Waehlhebel = hil.KN_Waehlhebel__timestamp.get()
#         timestamp_NM_Waehlhebel = hil.NM_Waehlhebel__timestamp.get()
#
#         if len(Waehlhebel_04__timestamp_list) == 0 or Waehlhebel_04__timestamp_list[-1] != timestamp_Waehlhebel_04:
#             Waehlhebel_04__timestamp_list.append(timestamp_Waehlhebel_04)
#
#         elif len(DS_Waehlhebel__timestamp_list) == 0 or DS_Waehlhebel__timestamp_list[-1] != timestamp_DS_Waehlhebel:
#             DS_Waehlhebel__timestamp_list.append(timestamp_DS_Waehlhebel)
#
#         elif len(KN_Waehlhebel__timestamp_list) == 0 or KN_Waehlhebel__timestamp_list[-1] != timestamp_KN_Waehlhebel:
#             KN_Waehlhebel__timestamp_list.append(timestamp_KN_Waehlhebel)
#
#         elif len(NM_Waehlhebel__timestamp_list) == 0 or NM_Waehlhebel__timestamp_list[-1] != timestamp_NM_Waehlhebel:
#             NM_Waehlhebel__timestamp_list.append(timestamp_NM_Waehlhebel)
#
#     new_sec = sec * 1000
#     Waehlhebel_04__timestamp = 10
#     DS_Waehlhebel__timestamp = 1000
#     KN_Waehlhebel__timestamp = 500
#     NM_Waehlhebel_timestamp = 200
#
#     testresult.append(basic_tests.checkRange((len(Waehlhebel_04__timestamp_list)) if application_msg else (len(Waehlhebel_04__timestamp_list) - 1),((new_sec / Waehlhebel_04__timestamp) - 5) if application_msg else 0,((new_sec / Waehlhebel_04__timestamp) + 5) if application_msg else 0,"Prüfen, ob die Applikation Botschaft Waehlhebel_04 mit dem Zeitzyklus von  %s ms in %s Sekunden %s mal gesendet wird." % (Waehlhebel_04__timestamp,sec,(new_sec / Waehlhebel_04__timestamp)) if application_msg else "Prüfen, ob die Applikation Botschaft Waehlhebel_04 nicht  gesendet wird."))
#     testresult.append(basic_tests.checkRange((len(DS_Waehlhebel__timestamp_list)) if application_msg else (len(DS_Waehlhebel__timestamp_list) - 1),((new_sec / DS_Waehlhebel__timestamp) - 2) if application_msg else 0,((new_sec / DS_Waehlhebel__timestamp) + 2) if application_msg else 0,"Prüfen, ob die Applikation Botschaft DS_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden %s mal gesendet wird." % (DS_Waehlhebel__timestamp,sec,(new_sec / DS_Waehlhebel__timestamp)) if application_msg else "Prüfen, ob die Applikation Botschaft DS_Waehlhebel nicht  gesendet wird."))
#     testresult.append(basic_tests.checkRange((len(KN_Waehlhebel__timestamp_list)) if application_msg else (len(KN_Waehlhebel__timestamp_list) - 1),((new_sec / KN_Waehlhebel__timestamp) - 2) if application_msg else 0,((new_sec / KN_Waehlhebel__timestamp) + 2) if application_msg else 0,"Prüfen, ob die Applikation Botschaft KN_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden  %s mal gesendet wird." % (KN_Waehlhebel__timestamp,sec,(new_sec / KN_Waehlhebel__timestamp)) if application_msg else "Prüfen, ob die Applikation Botschaft KN_Waehlhebel nicht  gesendet wird."))
#     testresult.append(basic_tests.checkRange( (len(NM_Waehlhebel__timestamp_list)) if nm_msg else (len(NM_Waehlhebel__timestamp_list) - 1), ((new_sec / NM_Waehlhebel_timestamp) - 2) if nm_msg else 0, ((new_sec / NM_Waehlhebel_timestamp) + 2) if nm_msg else 0, "Prüfen, ob die Applikation Botschaft NM_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden %s gesendet wird." % ( NM_Waehlhebel_timestamp, sec,(new_sec / NM_Waehlhebel_timestamp)) if nm_msg else "Prüfen, ob die Applikation Botschaft NM_Waehlhebel nicht  gesendet wird."))
#
#     if check_20_cycle_NM_WH:
#         count = new_sec/NM_Waehlhebel_timestamp
#         if len(NM_Waehlhebel__timestamp_list) > 10:
#             if ((len(NM_Waehlhebel__timestamp_list)-2) < count < (len(NM_Waehlhebel__timestamp_list)+2)):
#                 for i in NM_Waehlhebel__timestamp_list[0:10:1]:
#                     check_20_cycle_NM_WH_list.append(i)
#                 cycle_NM = sum(check_20_cycle_NM_WH_list) / len(check_20_cycle_NM_WH_list)
#                 testresult.append(basic_tests.checkRange(cycle_NM, 0.015, 0.025, descr="Prüf ob für Zycluszeit von NM_Waehlhebel für erste 1o Botschaft ist 20ms"))
#             else:
#                 testresult.append(["Zeitzyklus von NM_Waehlhebel für erste 1o Botschaft ist nicht 20ms", "FAILED"])
# try:
#     # #########################################################################
#     # Testenv #################################################################
#     testenv.setup()
#     testresult = testenv.getResults()
#
#     # set Testcase ID #########################################################
#     testresult.setTestcaseId("TestSpec_77")
#
#     # Initialize functions ####################################################
#     hil = testenv.getHil()
#     daq = testenv.getGammaDAQ()
#     func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
#     func_nm = functions_nm.FunctionsNM(testenv)
#
#     # Initialize variables ####################################################
#     applikationsbotschaften = [hil.Waehlhebel_04__timestamp,
#                                hil.DS_Waehlhebel__timestamp,
#                                hil.KN_Waehlhebel__timestamp, ]
#
#     nm_botschaften = [hil.NM_Waehlhebel__timestamp]
#     messages_cycle_times = {str(hil.Waehlhebel_04__timestamp): 10,
#                             str(hil.DS_Waehlhebel__timestamp): 1000,
#                             str(hil.KN_Waehlhebel__timestamp): 500,
#                             str(hil.NM_Waehlhebel__timestamp): 200,
#                             }
#     tolerance_percent = 0.10
#     cycletime_tol_perc = 0.10
#     ttimeout = 1.0
#     ttimeout_tol_perc = 0.05
#     nm_stop_s = 0.4
#     t_send_after_wakeup = 0.15  # to be clarified
#
#     meas_vars = [hil.cl15_on__, hil.Waehlhebel_04__timestamp,
#                  hil.DS_Waehlhebel__timestamp, hil.KN_Waehlhebel__timestamp,
#                  hil.NM_Waehlhebel__timestamp, hil.NM_Airbag__NM_Airbag_01_FCAB__value]
#
#     # TEST PRE CONDITIONS #####################################################
#     testresult.append(["[#0] Test Vorbedingungen", ""])
#     testresult.append(["[+] ECU einschalten und 4 Sekunden warten (T_aktiv_min)", ""])
#     testenv.startupECU()
#     time.sleep(4)
#
#     # TEST PROCESS ############################################################
#     testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
#     testresult.append(["[+0]", ""])
#
#     testresult.append(["[.] Prüfe Werte der Botschaft NM_Waehlhebel", ""])
#
#     testresult += [
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 0,
#                                 descr="NM_Waehlhebel_CBV_AWB:Passiver_WakeUp"),
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value, 1,
#                                 descr="NM_Waehlhebel_CBV_CRI:NM_mit_Clusteranforderungen"),
#         func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [12], [],
#                                  descr="NM_Waehlhebel_FCAB:12_GearSelector"),
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_SNI_10__value, 83,
#                                 descr="NM_Waehlhebel_SNI_10:Waehlhebel_SNI"),
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value, 4,
#                                 descr="NM_Waehlhebel_NM_State:NM_NO_aus_RM"),
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value, 0,
#                                 descr="NM_Waehlhebel_UDS_CC:Inaktiv"),
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value, 1,
#                                 descr="NM_Waehlhebel_Wakeup_V12:Bus_Wakeup"),
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value, 1,
#                                 descr="NM_Waehlhebel_NM_aktiv_KL15:KL15_EIN"),
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value, 0,
#                                 descr="NM_Waehlhebel_NM_aktiv_Diag:Inaktiv"),
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 0,
#                                 descr="NM_Waehlhebel_NM_aktiv_Tmin:Inaktiv")
#     ]
#
#     testresult.append(["[.] Prüfe Versenden (Timestamps/Zykluszeit) der gesendeten Applikations- und NM Botschaften", ""])
#     check_cycletime(2)
#
#     testresult.append(["[.] Schalte KL15 und Restbussimulation aus", ""])
#     testresult.append(["Setze KL15 auf 0", "INFO"])
#     hil.cl15_on__.set(0)
#     time.sleep(0.100)
#     testresult.append(["Schalte Senden von empfangenen Signalen aus (HiL -> ECU)", "INFO"])
#     descr, verdict = func_gs.switchAllRXMessagesOff()
#     testresult.append([descr, verdict])
#
#     testresult.append( ["[.] Prüfe Versenden (Timestamps/Zykluszeit) der gesendeten Applikations- und NM Botschaften", ""])
#     check_cycletime(1.002)
#
#
#     testresult.append(["[.] Warte 1000ms (T Timeout)", ""])
#     time.sleep(1)
#
#
#     testresult.append(["[.] Warte 500ms (< T WaitBusSleep)", ""])
#     time.sleep(0.5)
#
#
#     testresult.append(["[.] NM_Airbag_FCAB senden", ""])
#     hil.NM_Airbag__NM_Airbag_01_FCAB__value.set(2048)  # 12
#     hil.NM_Airbag__period.setState('an')
#
#
#     testresult.append(["[.] Prüfe erneut Werte der Botschaft NM_Waehlhebel", ""])
#
#     testresult += [
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value, 1,
#                                 descr="NM_Waehlhebel_CBV_CRI:NM_mit_Clusteranforderungen"),
#         func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [12], [],
#                                  descr="NM_Waehlhebel_FCAB:12_GearSelector"),
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_SNI_10__value, 83,
#                                 descr="NM_Waehlhebel_SNI_10:Waehlhebel_SNI"),
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value, 0,
#                                 descr="NM_Waehlhebel_UDS_CC:Inaktiv"),
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value, 1,
#                                 descr="NM_Waehlhebel_Wakeup_V12:Bus_Wakeup"),
#         basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value, 0,
#                                 descr="NM_Waehlhebel_NM_aktiv_Diag:Inaktiv"),
#
#     ]
#
#     testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Waehlhebel_CBV_AWB", ""])
#     testresult.append(
#         _checkStatus(
#             current_status=hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value,
#             nominal_status=1,
#             descr="NM_Waehlhebel_CBV_AWB:Aktiver_WakeU ist", ticket_id='Fehler Id:EGA-PRM-13'
#         )
#     )
#
#     testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_State", ""])
#     testresult.append(
#         _checkStatus(
#             current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value,
#             nominal_status=2,
#             descr="NM_RM_aus_PBSM:NM_RM_aus_PBSM ist", ticket_id='Fehler Id:EGA-PRM-13'
#         )
#     )
#     testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15", ""])
#     testresult.append(
#         _checkStatus(
#             current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value,
#             nominal_status=0,
#             descr="NM_Waehlhebel_NM_aktiv_KL15:Inaktiv ist", ticket_id='Fehler Id:EGA-PRM-13'
#         )
#     )
#     testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_aktiv_Tmin", ""])
#     testresult.append(
#         _checkStatus(
#             current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value,
#             nominal_status=1,
#             descr="NM_aktiv_Tmin:Mindestaktivzeit ist", ticket_id='Fehler Id:EGA-PRM-13'
#         )
#     )
#
#     testresult.append( ["[.] Prüfe Versenden (Timestamps/Zykluszeit) der gesendeten Applikations- und NM Botschaften", ""])
#     check_cycletime(2)
#
#
#     # time.sleep(3)
#     #
#     # testresult.append(["\xa0 Stoppe DAQ Messung", "INFO"])
#     # daq_data = daq.stopMeasurement()
#     # time.sleep(0.1)
#     #
#     # # DAQ Analysis ################################################################
#     # testresult.append(["[.] Analysiere DAQ Messung", ""])
#     #
#     # plot_data = {}
#     # for mes in applikationsbotschaften + nm_botschaften:
#     #     plot_data[str(mes)] = daq_data[str(mes)]
#     # testresult.append(
#     #     daq.plotMultiShot(plot_data, "WakeUp_Applikation_NM_Airbag_aus_PBSM_77")
#     # )
#     #
#     # testresult.append(["\xa0Werte KL15 Signal aus", "INFO"])
#     # descr, plot, verdict = daq.plotSingleShot(
#     #     daq_data=daq_data[str(meas_vars[0])],
#     #     filename="WakeUp_Applikation_NM_Airbag_aus_PBSM_77_KL_15",
#     #     label_signal="KL15"
#     # )
#     # testresult.append([descr, plot, verdict])
#     #
#     # cl15_data = daq_data[str(hil.cl15_on__)]
#     # cl_15 = eval_signal.EvalSignal(cl15_data)
#     # cl_15.clearAll()
#     # time_zero = cl_15.getTime()
#     # # find timestamp when clamp 15 is switched off:
#     # t_cl_15_off = cl_15.findNext("==", 0)
#     # cl15_idx = cl_15.cur_index  # read index
#     # testresult.append(["Ermittelter Zeitpunkt 'KL15 aus': %s" % (t_cl_15_off - time_zero), "INFO"])
#     # test_start_time = cl15_data['time'][cl15_idx - 200]  # go 200ms back (Zykluszeit NM)
#     # testresult.append(["Start-Zeitpunkt Analyse (200ms vorher): %ss" % (test_start_time - time_zero), "INFO"])
#     #
#     # testresult.append(["\xa0Werte NM_Airbag Signal aus", "INFO"])
#     # descr, plot, verdict = daq.plotSingleShot(
#     #     daq_data=daq_data[str(meas_vars[5])],
#     #     filename="WakeUp_Applikation_NM_Airbag_aus_PBSM_77_Airbag",
#     #     label_signal="NM_Airbag_FCAB"
#     # )
#     # testresult.append([descr, plot, verdict])
#     # airbag_mess = eval_signal.EvalSignal(daq_data[str(meas_vars[5])])
#     # airbag_mess.clearAll()
#     # time_zero = airbag_mess.getTime()
#     # # find timestamp when Airbag message is sent:
#     # t_airbag_sent = airbag_mess.findNext("==", 2048)
#     # testresult.append(["Ermittelter Zeitpunkt 'Senden der NM_Airbag Botschaft': %s" % (t_airbag_sent - time_zero), "INFO"])
#     #
#     # idx_airbag_sent = airbag_mess.cur_index  # index, when KL15 is switched on
#     # # prepare daq data for first analyse (behaviour till nm airbag will send)
#     # daq_data_part1 = copy.deepcopy(daq_data)
#     # daq_data_part2 = copy.deepcopy(daq_data)
#     # for data1, data2 in zip(daq_data_part1, daq_data_part2):
#     #     daq_data_part1[data1]['data'] = daq_data_part1[data1]['data'][:idx_airbag_sent]
#     #     daq_data_part1[data1]['time'] = daq_data_part1[data1]['time'][:idx_airbag_sent]
#     #     daq_data_part2[data2]['data'] = daq_data_part2[data2]['data'][idx_airbag_sent:]
#     #     daq_data_part2[data2]['time'] = daq_data_part2[data2]['time'][idx_airbag_sent:]
#     #
#     #
#     # # Check that messages stop sending correctly #####################################
#     # cycle_times = {}
#     # sleep_times = {}
#     # for var in meas_vars:
#     #     if (var != hil.cl15_on__) and (var != hil.NM_Airbag__NM_Airbag_01_FCAB__value):
#     #         cycle_time, sleep_time = func_nm.analyseCycleSleepTimes(
#     #             start_time=test_start_time,
#     #             daq_data=daq_data_part1[str(var)])
#     #         cycle_times[str(var)] = cycle_time
#     #         sleep_times[str(var)] = sleep_time
#     #
#     # testresult.append(["[+] Prüfe, dass NM-Botschaften %ss nach 'KL15 aus' nicht mehr gesendet werden"%nm_stop_s, ""])
#     # for var in nm_botschaften:
#     #     st_nm = sleep_times[str(var)]
#     #     if st_nm:
#     #         testresult.append(
#     #             basic_tests.compare(
#     #                 left_value=st_nm,
#     #                 operator="<=",
#     #                 right_value=nm_stop_s,
#     #                 descr = "Vergleiche Stop NM Botschaft <= %ss"%nm_stop_s
#     #             )
#     #         )
#     #     else:
#     #         testresult.append(["Keine Einschlafzeit für NM-Botschaften gefunden", "FAILED"])
#     #
#     #     testresult.append(["[.] Prüfe, dass Applikations-Botschaften %ss nach der letzten gesendeten NM-Botschaft"
#     #                        " nicht mehr gesendet werden" %(ttimeout), ""])
#     #     for var in applikationsbotschaften:
#     #         ct = cycle_times[str(var)]
#     #         if len(ct) > 0:
#     #             testresult.append(["\xa0Prüfe, dass Zykluszeit vor dem Einschlafen korrekt ist", ""])
#     #             cycle_time = sum(ct) / len(ct)
#     #             testresult.append(
#     #                 basic_tests.checkTolerance(
#     #                     current_value=cycle_time,
#     #                     rated_value=messages_cycle_times[str(var)],
#     #                     rel_pos=cycletime_tol_perc,
#     #                     descr="Zykluszeit von %s"%str(var)
#     #                 )
#     #             )
#     #             testresult.append(["\xa0Prüfe Einschlafzeit", ""])
#     #             st = sleep_times[str(var)]
#     #             if st and st_nm:
#     #                 testresult.append(
#     #                     basic_tests.checkRange(
#     #                         value=st-st_nm,
#     #                         min_value=ttimeout-(float(messages_cycle_times[str(var)])/1000),
#     #                         max_value = ttimeout + (ttimeout*ttimeout_tol_perc),
#     #                         descr = "Einschlafzeit von %s"%str(var),
#     #                     )
#     #                 )
#     #             else:
#     #                 testresult.append(["Es wurde keine Einschlafzeit für %s oder für die NM-Botschaft gefunden" % str(var), "FAILED"])
#     #         else:
#     #             testresult.append(["Nicht genug Zykluszeiten (%s) gemessen um Zeitpunkt zu analysieren"%str(var), "FAILED"])
#     #
#     #
#     # # Check when messages start sending again #####################################
#     # testresult.append(["[.] Prüfe, dass Botschaften %ss nach 'Senden der NM_Airbag Botschaft' wieder gesendet wird'"
#     #                    % t_send_after_wakeup, ""])
#     # wakeup_times = {}
#     # for var in meas_vars:
#     #     if (var != hil.cl15_on__) and (var != hil.NM_Airbag__NM_Airbag_01_FCAB__value):
#     #         cycle_times, wakeup_time = func_nm.analyseCycleWakeupTimes(
#     #             start_time=t_airbag_sent,
#     #             daq_data=daq_data_part2[str(var)])
#     #         wakeup_times[str(var)] = wakeup_time
#     #
#     #         if wakeup_time:
#     #             testresult.append(["\xa0Prüfe, dass Botschaft %s nach 'Senden der NM_Airbag Botschaft' wieder gesendet wird" % str(var), ""])
#     #             testresult.append(
#     #                 basic_tests.checkRange(
#     #                     value=wakeup_time,
#     #                     min_value=0,  # 0 means 'immediately'
#     #                     max_value=0 + t_send_after_wakeup,
#     #                     descr="Zeit von %s nach KL15 an" % str(var),
#     #                 )
#     #             )
#     #         else:
#     #             testresult.append(["%s beginnt nach 'Senden der NM_Airbag Botschaft' nicht wieder an zu senden" % str(var), "FAILED"])
#     #
#     #         if len(cycle_times) > 0:
#     #             if var == hil.NM_Waehlhebel__timestamp:
#     #                 if len(cycle_times) > 11:
#     #                     testresult.append(["\xa0Prüfe, dass erste 10 Zykluszeiten nach erneutem Senden korrekt sind", ""])
#     #                     cycle_times_first_10 = cycle_times[:10]
#     #                     cycle_time = sum(cycle_times_first_10) / len(cycle_times_first_10)
#     #                     testresult.append(
#     #                         basic_tests.checkTolerance(
#     #                             current_value=cycle_time,
#     #                             rated_value=messages_cycle_times[str(var)]/10,
#     #                             rel_pos=cycletime_tol_perc,
#     #                             descr="Zykluszeit von %s" % str(var)
#     #                             )
#     #                         )
#     #                     testresult.append(["\xa0Prüfe, dass anschließende Zykluszeiten korrekt sind", ""])
#     #                     cycle_times_next = cycle_times[10:]
#     #                     cycle_time = sum(cycle_times_next) / len(cycle_times_next)
#     #                     testresult.append(
#     #                         basic_tests.checkTolerance(
#     #                             current_value=cycle_time,
#     #                             rated_value=messages_cycle_times[str(var)],
#     #                             rel_pos=cycletime_tol_perc,
#     #                             descr="Zykluszeit von %s" % str(var)
#     #                             )
#     #                         )
#     #                 else:
#     #                     testresult.append(
#     #                         ["Nicht genug Zykluszeiten aufgezeichnet zum Auswerten (min. 11: 10 fast, 1 normal)",
#     #                          "FAILED"])
#     #             else:
#     #                 testresult.append(["\xa0Prüfe, dass Zykluszeit nach erneutem Senden korrekt ist", ""])
#     #                 cycle_time = sum(cycle_times) / len(cycle_times)
#     #                 testresult.append(
#     #                     basic_tests.checkTolerance(
#     #                         current_value=cycle_time,
#     #                         rated_value=messages_cycle_times[str(var)],
#     #                         rel_pos=cycletime_tol_perc,
#     #                         descr="Zykluszeit von %s" % str(var)
#     #                         )
#     #                     )
#     #         else:
#     #             testresult.append(["%s Botschaft beginnt nicht wieder zu senden, nachdem NM_Airbag wieder sendet"%str(var), "FAILED"])
#     #
#     #
#     # # Check that NM messages is sent first #####################################
#     # testresult.append(["[.] Prüfe, dass NM-Botschaften vor der Applikationsbotschaft gesendet wird", ""])
#     #
#     # # Check that NM message is sent as first ##################################
#     # if ((wakeup_times[str(hil.NM_Waehlhebel__timestamp)] < wakeup_times[str(hil.Waehlhebel_04__timestamp)]) and
#     #     (wakeup_times[str(hil.NM_Waehlhebel__timestamp)] < wakeup_times[str(hil.DS_Waehlhebel__timestamp)]) and
#     #     (wakeup_times[str(hil.NM_Waehlhebel__timestamp)] < wakeup_times[str(hil.KN_Waehlhebel__timestamp)])):
#     #     descr = "NM-Botschaft wird zuerst gesendet"
#     #     verdict = "PASSED"
#     # else:
#     #     descr = "NM-Botschaft wird NICHT zuerst gesendet"
#     #     verdict = "FAILED"
#     #
#     # testresult.append([descr, verdict])
#     # testresult.append(["[-0]", ""])
#
#     # TEST POST CONDITIONS ####################################################
#     testresult.append(["[-] Test Nachbedingungen", ""])
#     testresult.append(["Shutdown ECU", ""])
#     testenv.shutdownECU()
#
#     # cleanup
#     hil = None
#
# finally:
#     # #########################################################################
#     testenv.breakdown()
#     # #########################################################################
