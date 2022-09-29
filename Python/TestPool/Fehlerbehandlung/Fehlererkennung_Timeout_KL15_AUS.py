#******************************************************************************
# -*- coding: latin1 -*-
# File    : Fehlererkennung_Timeout_Kl15_AUS.py
# Title   : Fehlererkennung Timeout KL15 AUS
# Task    : Fehlererkennungund Behandlung bei KL15 Timeout
#
# Author  : A. Neumann
# Date    : 08.07.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 08.07.2021 | NeumannA     | initial
# 1.1  | 27.07.2021 | Mohammed     | Added TestSpec_ID
# 1.2  | 21.12.2021 | Mohammed     | Added Fehler Id#
# 1.3  | 14.02.2022 | Mohammed     | Added Warte Zeit
# 1.4  | 16.02.2022 | Mohammed     | Added Kl15 = 0
#******************************************************************************
# Imports #####################################################################
import time
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
from simplified_bus_tests import getMaxValidPeriod
from ttk_daq import eval_signal
from functions_nm import _checkStatus

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_199")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    kl15_period = hil.ClampControl_01__period
    cycle_time = kl15_period.value_lookup["an"]
    timeout_quali_max = 10

    kl15_status_var = hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    wh_fahrstufe_fehlerwert = 15

    meas_vars = [kl15_period, kl15_status_var, wh_fahrstufe]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte KL30 an (KL15 aus)", ""])
    testenv.startupECU()

    hil.cl30_on__.set(1)
    hil.cl15_on__.set(0)
    # canape_diag = testenv.getCanapeDiagnostic()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # test step 1
    testresult.append(["\xa01 Start DAQ Measurement für Timing-Verhalten der Fehlerreaktionen", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["\xa02 Prüfe aktuellen KL15 Status der NM_Waehlhebel Botschaft", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=kl15_status_var,
            nominal_status=0,
            descr="Prüfe, dass KL15 Status == 0 (aus) ist"
        )
    )

    testresult.append(["\xa03  Schalte Senden von ClampControl_01 aus", ""])
    testresult.append(["Schalte Periode von ClampControl_01 auf 0", "INFO"])
    kl15_period.setState('aus')
    testresult.append(["\xa04 Warte %ss (max. Timeoutqualifizierungszeit)"%timeout_quali_max, "INFO"])
    time.sleep(timeout_quali_max)

    testresult.append(["\xa05 Warte 2 Sekunde, bevor DAQ Messung beendet wird", ""])
    time.sleep(2)
    testresult.append(["\xa06 Stopp DAQ Measurement", "INFO"])
    daq_data = daq.stopMeasurement()
    time.sleep(0.5)

    testresult.append(["\nStart Analyse of DAQ Measurement", ""])
    testresult.append(["\xa07 Prüfe Wert NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15 nachdem ClampControl_01 Periode = 0", ""])
    # Startzeitpunkt = ClampControl_01 Periode == 0
    period_data = daq_data[str(kl15_period)]
    analyse_period_data = eval_signal.EvalSignal(period_data)
    analyse_period_data.clearAll()

    time_zero = analyse_period_data.getTime()
    stop_period_time = analyse_period_data.find(operator="==", value=0)
    stop_period_time_idx = analyse_period_data.cur_index

    # Prüfe alle Werte der MEssung, nachdem Period = 0
    wh_fahrstufe_data = daq_data[str(wh_fahrstufe)]['data'][stop_period_time_idx:]
    verdict = 'PASSED'
    for value in wh_fahrstufe_data:
        failure_count = 0
        if value == wh_fahrstufe_fehlerwert:
            failure_count += 1
            verdict = 'FAILED'
    if verdict == 'FAILED':
        descr = "Fehlerwert wurde gesetzt, nachdem ClampControl_01 Periode auf 0 gesetzt wurde (%s Messwerte)"%failure_count
    else:
        descr = "Fehlerwert wurde nicht gesetzt, nachdem ClampControl_01 Periode auf 0 gesetzt wurde"
    testresult.append([descr, verdict])


    # Prüfe alle Werte der MEssung, nachdem Period = 0
    kl15_status_data = daq_data[str(kl15_status_var)]['data'][stop_period_time_idx:]
    verdict = 'PASSED'
    for value in kl15_status_data:
        failure_count = 0
        if value != 0:
            failure_count += 1
            verdict = 'FAILED'
    if verdict == 'FAILED':
        descr = "KL15 Status wurde geändert, nachdem ClampControl_01 Periode auf 0 gesetzt wurde (%s Messwerte)" % failure_count
    else:
        descr = "KL15 Status wurde nicht geändert, nachdem ClampControl_01 Periode auf 0 gesetzt wurde"
    testresult.append([descr, verdict])

    testresult.append(["\xa08 Schalte Periode von ClampControl_01 an %sms"%cycle_time, "und warte 200 ms", "INFO"])
    kl15_period.setState('an')
    time.sleep(cycle_time/1000.0)
    time.sleep(.200)

    testresult.append(["\xa09 Prüfe aktuellen KL15 Status der NM_Waehlhebel Botschaft", ""])
    testresult.append(
        _checkStatus(current_status=kl15_status_var, nominal_status=0,
                     descr="Prüfe, dass KL15 Status == 0 (aus) ist",
                     ticket_id='FehlerId:EGA-PRM-147'))

    # erzeuge Plot für Testreport (ohne KL15)
    plot_data = {}
    for mes in [kl15_status_var, wh_fahrstufe]:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(
        daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0]),
                          v_lines={1: {'x': stop_period_time - time_zero, 'label': "ClampControl_01 Periode = 0"},}
                          )
            )

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    ## Cleanup
    hil=None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################
