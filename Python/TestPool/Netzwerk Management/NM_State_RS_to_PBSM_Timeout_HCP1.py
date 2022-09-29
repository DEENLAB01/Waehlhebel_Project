# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : NM_State_RS_to_PBSM_Timeout_HCP1.py
# Task    : check that no Wakeup of Application from RS Mode if message too short
#
# Author  : An3Neumann
# Date    : 15.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 15.06.2021 | An3Neumann | initial  
# ******************************************************************************
from _automation_wrapper_ import TestEnv

testenv = TestEnv()

import functions_gearselection
import functions_common
import functions_nm
from ttk_checks import basic_tests
import time
from ttk_daq import eval_signal
from result_list import ResultList  # @UnresolvedImport (in .pyz)

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
    func_nm = functions_nm.FunctionsNM(testenv, hil)

    # Initialize variables ####################################################
    t_aktiv_min_s = 4
    t_timeout_s = 1
    nm_cycletime_s = 0.200
    nm_sending_message = hil.NM_Waehlhebel__timestamp
    nm_receiving_message = hil.NM_HCP1__timestamp
    applikationsbotschaften = [hil.Waehlhebel_04__timestamp,
                               hil.DS_Waehlhebel__timestamp,
                               hil.KN_Waehlhebel__timestamp, ]

    nm_botschaften = [nm_sending_message,
                      nm_receiving_message]

    botschaften_cycletimes = {str(hil.Waehlhebel_04__timestamp): 10,
                              str(hil.DS_Waehlhebel__timestamp): 1000,
                              str(hil.KN_Waehlhebel__timestamp): 500,
                              str(hil.NM_Waehlhebel__timestamp): 200
                              }

    # set Testcase ID #########################################################
    testresult.setTestcaseId('TestSpec_53')

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte KL30 an (KL15 aus), warte 150ms", ""])
    testresult.append(["Setze KL30 auf 1", "INFO"])
    hil.cl30_on__.set(1)
    testresult.append(["Warte 150ms", "INFO"])
    time.sleep(0.15)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["\xa0Start DAQ Measurement für Zustandsanalyse (Ready Sleep Mode)", ""])
    meas_vars = applikationsbotschaften + nm_botschaften + [hil.cl15_on__]
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["[+] Schalte KL15 an, warte 150ms", ""])
    testresult.append(["Setze KL15 auf 1", "INFO"])
    hil.cl15_on__.set(1)
    testresult.append(["Warte 150ms", "INFO"])
    time.sleep(0.15)

    testresult.append(["[.] Warte %sms (Taktiv_min)" % (t_aktiv_min_s * 1000), ""])
    func_com.waitSecondsWithResponse(t_aktiv_min_s)

    testresult.append(["[.] Prüfe Signal NM_Waehlhebel:NM_Waehlhebel_NM_State", ""])
    descr, verdict = basic_tests.checkStatus(
        current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value,
        nominal_status=4,
        descr="Prüfe, dass Wert 4 (NM_NO_aus_RM) gesetzt ist"
    )
    testresult.append([descr, verdict])

    testresult.append(["[.] Schalte KL15 aus, warte 150ms", ""])
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    testresult.append(["Setze KL15 auf 0", "INFO"])
    hil.cl15_on__.set(0)
    testresult.append(["Warte bis in den Ready Sleep Mode gewechselt wurde (kein Senden von NM Botschaften)", "INFO"])
    func_nm.waitTillChangeIntoRS()

    testresult.append(["[.] Prüfe, dass in Ready Sleep Mode gewechselt wurde", ""])
    testresult.append(["Wird mit DAQ Messung ausgewertet, siehe DAQ Analyse", "INFO"])
    rs_change_chapter = '.'.join(map(str, testresult.current_chapter._indexes))

    testresult.append(["[.] Schalte zyklisches Senden von NM_HCP1 an", ""])
    testresult.append(["Setze NM_HCP1:NM_HCP1__period auf 'an'", "INFO"])
    hil.NM_HCP1__period.setState('an')

    testresult.append(["[.] Warte %sms + 100ms (T Timeout)" % (t_timeout_s * 1000), ""])
    func_com.waitSecondsWithResponse(t_timeout_s * 1.05 + 0.1)

    testresult.append(["[.] Prüfe, dass in ECU weiterhin im Ready Sleep Mode ist", ""])
    testresult.append(["Wird mit DAQ Messung ausgewertet, siehe DAQ Analyse", "INFO"])
    rs_stay_chapter = '.'.join(map(str, testresult.current_chapter._indexes))

    testresult.append(["[.] Schalte zyklisches Senden von NM_HCP1 aus", ""])
    testresult.append(["Setze NM_HCP1:NM_HCP1__period auf 'aus'", "INFO"])
    hil.NM_HCP1__period.setState('aus')

    testresult.append(["[.] Warte %sms (T Timeout)" % (t_timeout_s * 1000), ""])
    func_com.waitSecondsWithResponse(t_timeout_s * 1.05)

    testresult.append(["[.] Prüfe, dass in Prepare Bus-Sleep Mode gewechselt wurde", ""])
    testresult.append(["Wird mit DAQ Messung ausgewertet, siehe DAQ Analyse", "INFO"])
    pbsm_change_chapter = '.'.join(map(str, testresult.current_chapter._indexes))

    testresult.append(["[.] Prüfe Signal NM_Waehlhebel:NM_Waehlhebel_FCAB", ""])
    verdict = func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [1], [], "Prüfe, dass Wert 1 (CarWakeUp) gesetzt ist")
    testresult.append(verdict)

    testresult.append(["Warte eine weitere Sekunde, bevor DAQ Messung beendet wird", "INFO"])
    time.sleep(1)
    testresult.append(["Stopp DAQ Measurement", "INFO"])
    daq_data = daq.stopMeasurement()
    time.sleep(0.5)

    testresult.append(["\nStart Analyse of DAQ Measurement", ""])

    # Prüfe, dass in den Ready Sleep Mode gewechselt wird
    # Startzeitpunkt = KL15 wechselt von 1 auf 0
    cl15_data = daq_data[str(hil.cl15_on__)]
    analyse_cl15_data = eval_signal.EvalSignal(cl15_data)
    analyse_cl15_data.clearAll()
    time_zero = analyse_cl15_data.getTime()
    analyse_cl15_data.find(operator="==", value=1)  # KL15 an
    cl15_off_time = analyse_cl15_data.find(operator="==", value=0)  # KL15 von 1 -> 0
    cl15_off_idx = analyse_cl15_data.cur_index
    testresult.append(["KL15 aus Zeitpunkt: %ss" % (round(cl15_off_time - time_zero, 4)), "INFO"])

    # #########################################################################
    # Kapitel 6.2/9.2/12.2 (Spec) - Prüfe dass in Ready Sleep Mode gewechselt wurde
    # #########################################################################
    testresult.append([
                          "\n%s.2/%s.2/%s.2: NM Botschaften wird nach Wechsel in den Ready Sleep Mode nicht mehr gesendet" % (
                          rs_change_chapter, rs_stay_chapter, pbsm_change_chapter), ""])
    nm = nm_botschaften[0]
    ct = botschaften_cycletimes[str(nm)]
    nm_data = daq_data[str(nm)]
    _, sleep_time = func_nm.analyseCycleSleepTimes(start_time=cl15_off_time, daq_data=nm_data)

    if sleep_time:
        # rs_change_time - Senden von NM Botschaften stoppen
        rs_change_time = sleep_time + cl15_off_time -time_zero
        # prüfzeiten ####
        rs_stay_time = rs_change_time + t_timeout_s * 1.05 + 0.1

        # get index of times and exp value for NM Message
        nm_data = daq_data[str(nm_sending_message)]
        analyse_nm_data = eval_signal.EvalSignal(nm_data)
        analyse_nm_data.clearAll()
        rs_change_daq_time = analyse_nm_data.seek(rs_change_time + time_zero)
        rs_change_idx = analyse_nm_data.cur_index

        descr, verdict = daq.checkDataIsEqual(daq_data=nm_data['data'][rs_change_idx:], exp_value= rs_change_daq_time)
        testresult.append([descr, verdict])

        # Define Time of Prepare Bus-Sleep Mode (NM-HCP1 wird nicht mehr gesendet)
        nm_hcp1_data = daq_data[str(nm_receiving_message)]
        analyse_nm_hcp1_data = eval_signal.EvalSignal(nm_hcp1_data)
        analyse_nm_hcp1_data.clearAll()
        # go to es-change time and search start time of sending
        analyse_nm_hcp1_data.seek(nm_hcp1_data['time'][rs_change_idx])
        nm_hcp1_start_sending = analyse_nm_hcp1_data.findNextChanged()
        # search time, were sending stops
        _, sleep_time = func_nm.analyseCycleSleepTimes(start_time=nm_hcp1_start_sending, daq_data=nm_hcp1_data)

        t_timeout_start = sleep_time + nm_hcp1_start_sending - time_zero
        pbsm_change_time = t_timeout_start + t_timeout_s * 1.05

        # #########################################################################
        # Kapitel 6.1/9.1/12.1 (Spec) - Prüfe dass in Ready Sleep Mode gewechselt wurde
        # #########################################################################
        testresult.append(["\nTestergebnisse zum Kapitel %s, %s und %s: Wechsel in den Ready Sleep Mode" % (
        rs_change_chapter, rs_stay_chapter, pbsm_change_chapter), ""])
        testresult.append([
                              "\n%s.1/%s.1/%s.1: Applikationsbotschaften werden gesendet bis in den Prepare Bus-Sleep Mode gewechselt wird" % (
                              rs_change_chapter, rs_stay_chapter, pbsm_change_chapter), ""])
        subresult = ResultList()
        subresult.enableEcho(False)  # no need to echo results twice
        for app in applikationsbotschaften:
            ct = float(botschaften_cycletimes[str(app)])
            app_data = daq_data[str(app)]
            cycle_times, sleep_time = func_nm.analyseCycleSleepTimes(start_time=cl15_off_time, daq_data=app_data)
            sleep_time = sleep_time + cl15_off_time - time_zero if sleep_time else app_data['time'][-1] # wenn kein Einschlafen, dann nimm letzten Timestamp
            last_sending_timestamp = pbsm_change_time

            subresult.append(
                basic_tests.checkRange(
                    value=round(sleep_time, 4),  # letzer Sendetimestamp
                    min_value=round((last_sending_timestamp - ( ct / 1000) - ( t_timeout_s*0.05) ), 4),
                    max_value=round((last_sending_timestamp + ( ct / 1000) + ( t_timeout_s*0.05) ), 4),
                    descr="Prüfe, dass Applikationsbotschaft %s bis zum Wechsel in den Prepare Bus-Sleep Mode (Zeitpunkt: %ss +- %ss Zykluszeit [+- 5%%Toleranz Timeout]) noch gesendet wird" % (
                    str(app), round(last_sending_timestamp, 4), ct/1000)
                )
            )
        testresult.append(subresult.getCombinedResult())

        # erzeuge Plot für Testreport (ohne KL15)
        plot_data = {}
        for mes in applikationsbotschaften + nm_botschaften:
            plot_data[str(mes)] = daq_data[str(mes)]
        testresult.append(
            daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0]),
                              v_lines={1: {'x': cl15_off_time - time_zero, 'label': "KL15 aus"},
                                       2: {'x': rs_change_time, 'label': "Wechsel in Ready Sleep Mode"},
                                       3: {'x': rs_stay_time, 'label': "Bleibt in Ready Sleep Mode"},
                                       4: {'x': t_timeout_start, 'label': 'T Timeout timer starts'},
                                       5: {'x': pbsm_change_time, 'label': "Wechsel in Prepare Bus-Sleep Mode"}}
                              )
        )
    else:
        testresult.append(["Keine Einschlafzeit für NM-Botschaften gefunden (Kein Wechsel in Ready Sleep Mode)", "FAILED"])
        # erzeuge Plot für Testreport (ohne KL15)
        plot_data = {}
        for mes in applikationsbotschaften + nm_botschaften:
            plot_data[str(mes)] = daq_data[str(mes)]
        testresult.append(
            daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0]), v_lines={1: {'x': cl15_off_time - time_zero, 'label': "KL15 aus"}}))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup #################################################################
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

print "Done."
