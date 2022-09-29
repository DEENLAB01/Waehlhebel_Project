# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : DTC_Suppression_KL15.py
# Title   : DTC_Suppression_KL15
# Task    : set kl15 is on and off and read DTC
#
# Author  : M.A. Mushtaq
# Date    : 23.02.2022
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 23.02.2022 | M.A. Mushtaq | initial
# 1.1  | 17.08.2022 | Mohammed     | Added Fehler ID
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import functions_hil
from ttk_daq import eval_signal
import data_common as dc
import time

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    bus = testenv.getCanBus()
    daq = testenv.getGammaDAQ()
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])

    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()
    func_hil = functions_hil.FunctionsHil(testenv, hil)
    # Initialize variables ####################################################
    voltage_ov = dc.voltage_range['Overvoltage']
    set_voltage_invalid_ov = float(voltage_ov['voltage']) + float(voltage_ov['voltage']) * float(
        voltage_ov['tol_perc'] / 100.0) + float(voltage_ov['hil_tol_ma'])
    set_voltage_back_valid = float(dc.voltage_range['Normal']['voltage'])
    exp_dtc = [voltage_ov['DTCs'], 0x800100]  # voltage_ov['DTCs']
    failure_set_time = 0.100
    relay_debounce_time = 0.02  # do not know the exect time
    failure_reset_time = 0.500
    kl_15_values = [1, 0]
    sig1 = bus.DS_Waehlhebel__DS_Waehlhebel_MemSel10Changed__value
    sig2 = bus.DS_Waehlhebel__DS_Waehlhebel_MemSelChanged__value
    sig3 = bus.DS_Waehlhebel__DS_Waehlhebel_StMemChanged__value
    sig4 = bus.DS_Waehlhebel__DS_Waehlhebel_TestFailedChanged__value

    meas_vars = [sig1, sig2, sig3, sig4]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_372")

    # TEST PRE CONDITIONS #####################################################

    testresult.append(["[-] Test Vorbedingungen", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(["[+0]", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append([" set Systeminfo_01_SI_NWDF_30 =1  ",  "INFO"])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["\xa0Start DAQ Measurement für DS_Waehlhebel__DS signals Analyse", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    for i in range(1):
        testresult.append(["[.] Setze ClampControl_01::KST_KL_15 = %s" % (kl_15_values[i]), ""])
        bus.ClampControl_01__KST_KL_15__value.set(kl_15_values[i])

        testresult.append(["[.] Setze Spannung auf %sV (uberspannung)" % set_voltage_invalid_ov, ""])
        descr, verdict = func_hil.setVoltage(set_voltage_invalid_ov)
        testresult.append([descr, verdict])

        testresult.append(["Warte %ss - Fehlererkennungszeit" % (failure_set_time + relay_debounce_time), "INFO"])
        time.sleep(failure_set_time + relay_debounce_time)

        if i == 0:

            testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
            activ_dtcs1 = [(0x800100, 0x27)]
            testresult.append(canape_diag.checkEventMemory(activ_dtcs1, mode="ONE_OR_MORE"))
            time.sleep(1.5)
            #time.sleep(1)
            testresult.append(["[.] Stopp DAQ Measurement", ""])
            daq_data = daq.stopMeasurement()

            descr, verdict = func_hil.setVoltage(set_voltage_back_valid)
            testresult.append([descr, verdict])

            time.sleep(0.5)
            testresult.append(canape_diag.resetEventMemory(wait=True, ticket_id='Fehler Id:EGA-PRM-276'))
            testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-276'))
        else:
            testresult.append(["[.] Lese Fehlerspeicher (ADC-Plausibility-DTC aktiv und KL-30 uberspannung)", ""])
            testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["[+0]", ""])
    testresult.append(["[-] Setze Spannung zurück auf %s (gültiger Bereich)" % set_voltage_back_valid, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_back_valid)
    testresult.append([descr, verdict])

    testresult.append(["[+0]", ""])
    testresult.append(["[-] Lösche Fehlerspeicher", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True, ticket_id='Fehler Id:EGA-PRM-276'))
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-276'))

    testresult.append(["\nStart Analyse of DAQ Measurement", ""])

    for i in range(len(meas_vars)):
        sig_status_data = daq_data[str(meas_vars[i])]  # str(meas_vars[i])
        analyse_sig1_data = eval_signal.EvalSignal(sig_status_data)
        analyse_sig1_data.clearAll()
        time_1 = analyse_sig1_data.findChanged(forward=True, threshold=0.5)
        time_1 = analyse_sig1_data.findChanged(forward=True, threshold=0.5)

        if time_1:
            testresult.append([" %s::\nValue toggled from 0-->1-->0" % (meas_vars[i].alias), "PASSED"])
            time_1 = None
        else:
            testresult.append([" %s::\nValue did not toggled from 0-->1-->0 " % (meas_vars[i].alias), "FAILED"])
            sig_status_data = []

    #     only for debugging
    plot_data = {}
    for mes in meas_vars:
        plot_data[str(mes)] = daq_data[str(mes)]


    # testresult.append(
    #         daq.plotMultiShot(plot_data, "test_signal_multi_1"))
    # testresult.append(
    #      daq.plotSingleShot(daq_data=plot_data[str(mes)],
    #                        filename="test_signal1",
    #                         label_signal="test1"))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None
    bus = None
    daq = None
finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
