# *******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Fehlererkennung_SiShift_01_Timeout.py
# Title   : Fehlererkennung_SiShift_01_Timeout
# Task    : Timeout test für SiShift_01 Message

# Author  : A.Neumann
# Date    : 28.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************** Version ***********************************
# ******************************************************************************
# Rev. | Date        | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 28.05.2021  | A. Neumann  | initial created Timeout Test
# 1.1  | 07.07.2021  | A. Neumann  | adapted for Waehlhebel_04 Errorreaction
# 1.2  | 27.07.2021 | Mohammed     | Added TestSpec_ID
# 1.3  | 22.11.2021 | Mohammed     | Rework
# 1.4  | 21.12.2021 | Mohammed     | Added Fehler Id
# 1.5  | 24.02.2022 | Mohammed     | Added NWDF_30 Signal
# 1.6  | 18.07.2022 | Mohammed     | Rework
# 1.7  | 20.07.2022 | Mohammed     | Added Fehler Id
# 1.8  | 21.07.2022 | Mohammed     | Added Korrektur gültige Zykluszeit aufgrund E2E-Implementierung
# 1.9  | 04.08.2022 | Mohammed     | Change TestSpec Name
# ******************************************************************************

from _automation_wrapper_ import TestEnv

testenv = TestEnv()

# Imports #####################################################################
from ttk_checks import basic_tests
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
import time
import data_common as dc
from ttk_daq import eval_signal

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

    # Initialize variables ####################################################
    period_var = hil.SiShift_01__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 280  # CAN_3244
    ftti_ms = 50
    tMSG_CYCLE_FTTI = 240
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    wh_fahrstufe_fehlerwert = 15
    allowed_fahrstufe = [4, 5, 6, 7]  # Nicht betigt, D, N, R
    failure_reac_var = hil.Waehlhebel_04__WH_Fahrstufe__value
    fehlerwert = 15
    meas_vars = [failure_reac_var, hil.SiShift_01__period]
    active_dtcs = [(0xE00101, 0x27)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_61")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: KL30 und KL15 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[-] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["\xa0Start DAQ Measurement für Kommunikationsanalyse", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    # Test step 1
    testresult.append(["[.] Setze Zykluszeit der Botschaft SiShift_01 auf 20ms (gültig)", ""])
    # testresult.append(["[+] Ändere Zykluszeit und prüfe Fehlerspeicher", ""])
    testresult.append(["\xa0 Setze Zykluszeit auf %sms" % cycle_time, ""])
    period_var.set(cycle_time)

    # Test step 2
    testresult.append(["[.] Warte 1 Sekunde", ""])
    time.sleep(1)

    # Test step 3
    testresult.append(["[.] Lese Botschaft Waehlhebel_04:WH_Fahrstufe", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = allowed_fahrstufe,
            current_value= current_fahrstufe,
            descr="Prüfe WH_Fahrstufe !=15 ist"
        )
    )

    # Test step 4
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # Test step 5
    testresult.append(["[.] Setze Zykluszeit der Botschaft SiShift_01 auf 240ms (gültig <(n-q+1))", ""])
    testresult.append(["Setze Zykluszeit auf %sms" % max_valid_cycletime, "INFO"])
    period_var.set(max_valid_cycletime)

    # Test step 6
    testresult.append(["[.] Lese Botschaft Waehlhebel_04:WH_Fahrstufe", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = allowed_fahrstufe,
            current_value= current_fahrstufe,
            descr="Prüfe WH_Fahrstufe = 4 ist"
        )
    )

    # Test step 7
    testresult.append(["[.] Warte maximum tMSG_CYCLE-FTTI (%sms)" % (tMSG_CYCLE_FTTI), ""])
    time.sleep(float(tMSG_CYCLE_FTTI) / 1000)

    # Test step 8
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='FehlerId:EGA-PRM-258'))

    # Test step 9
    testresult.append(["[.] Setze Zykluszeit der Botschaft SiShift_01 auf 0ms (ungültig)", ""])
    period_var.set(0)

    # Test step 10
    testresult.append(["[.] Warte 260 ms (n-q+1)+ 20 ms (Toleranz) (%sms)" % (wait_time), ""])
    time.sleep(float(wait_time) / 1000)

    # Test step 11
    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='FehlerId:EGA-PRM-144'))

    # Test step 12
    testresult.append(["[.] Setze Zykluszeit der Botschaft SiShift_01 auf 20ms (original)", ""])
    #testresult.append(["\xa0 Prüfe, dass Fehler zurückgesetzt wird bei erneutem richtigen Empfangen", ""])
    testresult.append(["\xa0 Setze Zykluszeit auf %sms" % cycle_time, ""])
    period_var.set(cycle_time)

    # Test step 13
    testresult.append(["[.] Warte 140ms  (tMSG_Timeoutn: n/2, n=14) + 10ms (Toleranz)", ""])
    time.sleep(.150)
    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC passiv)", ""])

    # Test step 14
    passive_dtcs = [(0xE00101, 0x26)]
    testresult.append(canape_diag.checkEventMemory(passive_dtcs, ticket_id='FehlerId:EGA-PRM-144'))

    # Test step 15
    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(["\xa0 Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    #testresult.append(["[.] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    #time.sleep(float(wait_time) / 1000)
    # Test step 15
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1)
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["Stopp DAQ Measurement", ""])
    daq_data = daq.stopMeasurement()
    time.sleep(0.5)

    testresult.append(["\nStart Analyse of DAQ Measurement", ""])
    plot_data = {}
    plot_data[str(failure_reac_var)] = daq_data[str(failure_reac_var)]
    v_lines = {}

    # search failure time --> SiShift period = max_valid_cycletime
    sishift_data = daq_data[str(hil.SiShift_01__period)]
    analyse_sishift_data = eval_signal.EvalSignal(sishift_data)
    analyse_sishift_data.clearAll()

    time_zero = analyse_sishift_data.getTime()

    time_period_stopp = analyse_sishift_data.find(operator="==", value=max_valid_cycletime)
    v_lines[1] = {'x': time_period_stopp - time_zero, 'label': 'SiShift Period == %s'%max_valid_cycletime}
    v_lines[2] = {'x': time_period_stopp - time_zero + (ftti_ms/1000.0), 'label': 'FTTI Ende (nach %sms)' %ftti_ms}

    # search changetime waehlhebel_04:wh_fahrstufe = Fehlerwert
    fahrstufe_data = daq_data[str(failure_reac_var)]
    analyse_fahrstufe_data = eval_signal.EvalSignal(fahrstufe_data)
    analyse_fahrstufe_data.clearAll()

    start_value = analyse_fahrstufe_data.getData()

    failure_timestamp = analyse_fahrstufe_data.find(operator="==", value=fehlerwert)

    if failure_timestamp:
        curr_ftti = failure_timestamp - time_period_stopp

        if curr_ftti >= 0:
            if curr_ftti <= (ftti_ms / 1000.0):
                descr = "Fehlerwert wurde  zu spät gesetzt (nach %sms)" % (curr_ftti * 1000)
                verdict = "FAILED"
            else:
                descr = "Fehlerwert wurde korrekt gesetzt (erst nach %sms)" % (curr_ftti * 1000)
                verdict = "PASSED"
        else:
            descr = "Fehlerwert wurde gesetzt, bevor Timeout erkannt werden soll"
            verdict = "FAILED"
    else:
        descr = "Waehlhebel_04:WH_Fahrstufe wurde nicht auf Fehlerwert %s gesetzt" % fehlerwert
        verdict = "FAILED"

    testresult.append(["[.] Prüfe, dass Fehlerwert (Waehlhebel_04:WH_Fahrstufe) gesetzt wurde", ""])
    testresult.append([descr, verdict])

    testresult.append(
        daq.plotMultiShot(plot_data, testenv.script_name.split(".py")[0], v_lines=v_lines)
    )

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

