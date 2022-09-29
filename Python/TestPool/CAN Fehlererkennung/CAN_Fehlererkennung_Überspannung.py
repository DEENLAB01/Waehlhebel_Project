#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Fehlererkennung_Überspannung.py
# Task    : Kommunikationsprüfung im oberen Spannungsbereich (bis 13V - 17V)

# Author  : A.Neumann
# Date    : 05.07.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.1  | 01.07.2021  | A. Neumann | initial
# 1.2  | 28.10.2021  | Mohammed   | Rework
# 1.2  | 28.10.2021  | Mohammed   | Added Fehler Id
# 1.3  | 24.02.2022  | Mohammed   | Updated Passiv DTC
# 1.4  | 17.08.2022  | Mohammed   | Added new Fehler Id
#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()

# Imports #####################################################################
import time
import functions_hil
import functions_gearselection
import functions_nm
import data_common as dc
from ttk_daq import eval_signal
from ttk_checks import basic_tests

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()
    daq = testenv.getGammaDAQ()
    func_hil = functions_hil.FunctionsHil(testenv, hil)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    voltage_ov = dc.voltage_range['Overvoltage']
    set_voltage_invalid_ov = float(voltage_ov['voltage']) + float(voltage_ov['voltage']) * float(voltage_ov['tol_perc'] / 100.0) + float(voltage_ov['hil_tol_ma'])

    voltage_can = dc.voltage_range['Overvoltage Functions']
    set_voltage_can_valid_max = float(voltage_can['voltage']) - float(voltage_can['voltage']) * float(voltage_can['tol_perc'] / 100.0) - float(voltage_can['hil_tol_ma'])

    set_voltage_back_valid = float(dc.voltage_range['Normal']['voltage'])

    exp_dtc = voltage_ov['DTCs'] if voltage_ov['voltage'] < voltage_can['voltage'] else voltage_can['DTCs']
    failure_set_time = 5.0
    failure_reset_time = 1

    send_messages = func_gs.getAllTimestamps("TX", 'cycletime')
    meas_vars = send_messages + [hil.vbat_cl30__V]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_281")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[-] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["\xa0Start DAQ Measurement für Kommunikationsanalyse", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["[+0]", ""])
    if voltage_ov['voltage'] < voltage_can['voltage']:
        testresult.append(["\nOberspannung ist niedriger als Spannung des max. Funktionsbereiches\n"
                           "Es wird erst geprüft, dass der UV DTC eingetragen wird", ""])
        testresult.append(["[.] Setze Spannung auf %sV (Überspannung)"%set_voltage_invalid_ov, ""])
        descr, verdict = func_hil.setVoltage(set_voltage_invalid_ov, 0.1, 0.02)
        testresult.append([descr, verdict])

        testresult.append(["[.] Warte %ss - Fehlererkennungszeit"%failure_set_time, ""])
        time.sleep(failure_set_time)

        testresult.append(["[.] Lese Fehlerspeicher (Überspannungs-DTC aktiv)", ""])
        active_dtcs1 = [(0x800100, 0x27), (0x800101, 0x27)]
        testresult.append(canape_diag.checkEventMemory(active_dtcs1, mode="ONE_OR_MORE", ticket_id='Fehler Id:EGA-PRM-276'))
    else:
        testresult.append(["\nÜberspannung ist höher als Spannung des max. Funktionsbereiches\n"
                           "Es wird kein UV DTC erwartet", ""])

    testresult.append(["[.] Setze Spannung auf %sV (max. Funktionsbereich)"%set_voltage_can_valid_max, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_can_valid_max, 0.1, 0.02)
    testresult.append([descr, verdict])

    testresult.append(["[.] Warte %ss - Fehlererkennungszeit"%failure_set_time, ""])
    time.sleep(failure_set_time)

    if exp_dtc:
        testresult.append(["[.] Lese Fehlerspeicher (Überspannungs-DTC aktiv)", ""])
        testresult.append(canape_diag.checkEventMemory(active_dtcs1, ticket_id='Fehler Id:EGA-PRM-276'))

    testresult.append(["[.] Setze Spannung zurück auf %s (gültiger Bereich)" % set_voltage_back_valid, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_back_valid, 0.1, 0.05)
    testresult.append([descr, verdict])

    testresult.append(["[.] Warte %ss - Fehlerrücksetzzeit"%failure_reset_time, ""])
    time.sleep(failure_reset_time)

    testresult.append(["[.] Lese Fehlerspeicher (Überspannungs-DTC passiv)", ""])
    testresult.append(canape_diag.checkEventMemory([(0x800101, 0x26), (0x800100, 0x26)], ticket_id='Fehler Id:EGA-PRM-276'))
    #if exp_dtc:
        #testresult.append(["[.] Lese Fehlerspeicher (Überspannungs-DTC passiv)", ""])
        #testresult.append(canape_diag.checkEventMemory([(0x800101, 0x27), (0x800100, 0x27)], ticket_id='Fehler-Id:120'))

        ####
        #testresult.append(["[.] Setze Spannung zurück auf %s (gültiger Bereich)" % set_voltage_back_valid, ""])
       # descr, verdict = func_hil.setVoltage(set_voltage_back_valid, 0.1, 0.05)
       # testresult.append([descr, verdict])
        #testresult.append(canape_diag.checkEventMemory([(0x800101, 0x27), (0x800100, 0x27)], ticket_id='Fehler-Id:120'))

        ###
        #testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
        #testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-276'))

    testresult.append(["Stopp DAQ Measurement", ""])
    daq_data = daq.stopMeasurement()
    time.sleep(0.5)

   # print active_dtcs, passive_dtcs, "+++++THIS IS ACTIVE AND PASSIVE DTC++++++"
    testresult.append(["[.] Prüfe CAN Kommunikation ", ""])
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])
    plot_data = {}
    for mes in send_messages:
        plot_data[str(mes)] = daq_data[str(mes)]

    # search for voltage settings (only for plot)
    cl30_data = daq_data[str(hil.vbat_cl30__V)]
    analyse_cl15_data = eval_signal.EvalSignal(cl30_data)
    analyse_cl15_data.clearAll()
    time_zero = analyse_cl15_data.getTime()
    cl30_valid = analyse_cl15_data.find(operator=">=", value=set_voltage_invalid_ov)
    cl30_invalid = analyse_cl15_data.findNext(operator=">=", value=set_voltage_can_valid_max)
    cl30_valid_back = analyse_cl15_data.findNext(operator="<=", value=set_voltage_back_valid)

    testresult.append(
        daq.plotMultiShot(plot_data, "CAN_EI_CAN_Overvoltage",
                          v_lines={1: {'x': cl30_valid-time_zero, 'label': 'KL30 %sV'%set_voltage_invalid_ov},
                                   2: {'x': cl30_invalid-time_zero, 'label': 'KL30 %sV'%set_voltage_can_valid_max},
                                   3: {'x': cl30_valid_back-time_zero, 'label': 'KL30 %sV'%set_voltage_back_valid},})
    )

    # check that communication always run
    for mes in send_messages:
        data = daq_data[str(mes)]
        last_timestamp = data['time'][-1]
        cycle_time = func_gs.messages_tx_cycletimes["self.hil." + mes.split('.')[-2]]
        _, sleep_time = func_nm.analyseCycleSleepTimes(start_time=time_zero, daq_data=data)

        testresult.append(
            basic_tests.compare(
                left_value=round(sleep_time,2),
                operator=">=",
                right_value=round(last_timestamp-time_zero-(cycle_time/1000.0),2),
                descr="Prüfe, dass Botschaft %s bis zum Ende der Messung gesendet wurde (Letzter Messpunkt - Zykluszeit)"%mes.split('.')[-2]
            )
        )

    testresult.append(["[.] Lösche Fehlerspeicher", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-276'))

    testresult.append(["[.] Warte 1s", ""])
    time.sleep(1)

    testresult.append(["[.] Lese Fehlerspeicher", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-276'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    cal = None
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()

