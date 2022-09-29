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
# 1.2  | 28.10.2021  | Mohammed | Rework
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
    exp_dtc = []

    failure_set_time = 5.0 # Todo
    failure_reset_time = 1.0 # Todo

    active_dtcs1 = []
    passive_dtcs = []
    for dtc in exp_dtc:
        active_dtcs.append((dtc, dc.DTCactive))
        passive_dtcs.append((dtc, dc.DTCpassive))

    send_messages = func_gs.getAllTimestamps("TX", 'cycletime')
    meas_vars = send_messages + [hil.vbat_cl30__V]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_281")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["\xa0Start DAQ Measurement für Kommunikationsanalyse", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["[+0]", ""])
    if voltage_ov['voltage'] < voltage_can['voltage']:
        testresult.append(["\nOberspannung ist niedriger als Spannung des max. Funktionsbereiches\n"
                           "Es wird erst geprüft, dass der UV DTC eingetragen wird", ""])
        testresult.append(["[.] Setze Spannung auf %sV (Überspannung), overvoltage 1"%set_voltage_invalid_ov, ""])
        descr, verdict = func_hil.setVoltage(set_voltage_invalid_ov, 0.1, 0.02)
        testresult.append([descr, verdict])

        testresult.append(["Warte %ss - Fehlererkennungszeit"%failure_set_time, "INFO"])
        time.sleep(failure_set_time)

        testresult.append(["[.] Lese Fehlerspeicher (Überspannungs-DTC aktiv)", ""])
        active_dtcs1 = [(0x800100, 0x27), (0x800101, 0x27), (0xE00106, 0x27)]
        testresult.append(canape_diag.checkEventMemory(active_dtcs, mode="ALL"))
    else:
        testresult.append(["\nÜberspannung ist höher als Spannung des max. Funktionsbereiches\n"
                           "Es wird kein UV DTC erwartet", ""])

    testresult.append(["[.] Setze Spannung auf %sV (max. Funktionsbereich)OVERVOLTAGE 2 "%set_voltage_can_valid_max, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_can_valid_max, 0.1, 0.02)
    testresult.append([descr, verdict])

    testresult.append(["Warte %ss - Fehlererkennungszeit"%failure_set_time, "INFO"])
    time.sleep(failure_set_time)

    if exp_dtc:
        testresult.append(["[.] Lese Fehlerspeicher (Überspannungs-DTC aktiv) OVERVOLTAGE 3 ", ""])
        testresult.append(canape_diag.checkEventMemory(active_dtcs))

    testresult.append(["[.] Setze Spannung zurück auf %s (gültiger Bereich) OVERVOLTAGE 4" % set_voltage_back_valid, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_back_valid, 0.1, 0.05)
    testresult.append([descr, verdict])

    testresult.append(["Warte %ss - Fehlerrücksetzzeit"%failure_reset_time, "INFO"])
    time.sleep(failure_reset_time)

    if exp_dtc:
        testresult.append(["[.] Lese Fehlerspeicher (Überspannungs-DTC passiv)", ""])
        testresult.append(canape_diag.checkEventMemory(passive_dtcs))

        testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
        testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["Stopp DAQ Measurement", ""])
    daq_data = daq.stopMeasurement()


    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    cal = None
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()

