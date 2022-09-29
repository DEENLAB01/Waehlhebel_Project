# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : KL30_plausibility_check_DTC_after_3 ocy.py
# Title   : KL30_plausibility_check_DTC_after_3 ocy
# Task    : check KL30 plausibility DTC confirmed after 3 OCY
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
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import functions_hil
from ttk_checks import basic_tests
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

    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])

    testenv.startupECU()  # startup before cal vars are called

    canape_diag = testenv.getCanapeDiagnostic()
    func_hil = functions_hil.FunctionsHil(testenv, hil)
    # Initialize variables ####################################################
    voltage_uv = dc.voltage_range['Undervoltage']
    # set_voltage_invalid_uv = float(voltage_uv['voltage']) + float(voltage_uv['voltage']) * float(
    #     voltage_uv['tol_perc'] / 100.0) + float(voltage_uv['hil_tol_ma'])
    set_voltage_invalid_uv = 5.5
    set_voltage_back_valid = float(dc.voltage_range['Normal']['voltage'])
    exp_dtc = 0x800100  # voltage_uv['DTCs']
    failure_set_time = 0.1
    relay_debounce_time = 0.3 # do not know the exect time
    failure_reset_time = 0.1

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_NA")

    # TEST PRE CONDITIONS #####################################################

    testresult.append(["[-] Test Vorbedingungen", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(["[+0]", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["[.] Setze Spannung auf %sV (unterspannung)" % set_voltage_invalid_uv, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_invalid_uv)
    testresult.append([descr, verdict])

    testresult.append(["Warte %ss - Fehlererkennungszeit" % (failure_set_time + relay_debounce_time), "INFO"])
    time.sleep(failure_set_time + relay_debounce_time)
    testresult.append(["[.] Lese Fehlerspeicher (ADC-Plausibility-DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory([(0x800100, 0x27)]))

    testresult.append(["[+0]", ""])
    testresult.append(["[-] perform 3 OCY", ""])
    func_hil.perform3OYC()
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Setze Spannung zurück auf %s (gültiger Bereich)" % set_voltage_back_valid, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_back_valid)
    testresult.append([descr, verdict])

    testresult.append(["Warte %ss - Fehlererkennungszeit" % (failure_set_time + relay_debounce_time), "INFO"])
    time.sleep(failure_set_time + relay_debounce_time)
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Lese Fehlerspeicher (Überspannungs-DTC Pasiv)", ""])
    pasiv_dtcs1 = [(exp_dtc, 0x65), (0x800101, 0x65)]
    testresult.append(canape_diag.checkEventMemory(pasiv_dtcs1, mode="ONE_OR_MORE"))

    testresult.append(["[+0]", ""])
    testresult.append(["[-] Lösche Fehlerspeicher", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
