#******************************************************************************
# -*- coding: latin1 -*-
# File    : Fehlererkennung_Timeout_Kl15_AN.py
# Title   : Fehlererkennung Timeout KL15 AN
# Task    : Fehlererkennungund Behandlung bei KL15 Timeout
#
# Author  : Mohammed Abdul Karim
# Date    : 14.04.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 14.04.2021 | Abdul Karim  | initial
# 1.1  | 08.07.2021 | NeumannA     | cpmpletly reworked for automation
# 1.2  | 11.01.2022 | Mohammed     | Adapt the TestSpec
#******************************************************************************
# Imports #####################################################################
import time
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
from simplified_bus_tests import getMaxValidPeriod
from ttk_daq import eval_signal

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_108")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    kl15_period = hil.ClampControl_01__period
    cycle_time = kl15_period.value_lookup["an"]
    timeout_quali_min = getMaxValidPeriod(cycletime_ms=cycle_time)/1000.0
    timeout_quali_max = 10

    kl15_status_var = hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    wh_fahrstufe_fehlerwert = 15
    fehlerwert_timer_s = 0.2
    allowed_fahrstufe = [4, 5, 6, 7] # Nicht betigt, D, N, R

    meas_vars = [kl15_period, kl15_status_var, wh_fahrstufe]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    # canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Prüfe aktuelle Fahrstufe", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = allowed_fahrstufe,
            current_value= current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe korrekt ist"
        )
    )

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["\xa0Start DAQ Measurement für Timing-Verhalten der Fehlerreaktionen", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["[+] Prüfe aktuellen KL15 Status der NM_Waehlhebel Botschaft", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=kl15_status_var,
            nominal_status=1,
            descr="Prüfe, dass KL15 Status == 1 (an) ist"
        )
    )

    testresult.append(["[.] Schalte Senden von ClampControl_01 aus", ""])
    testresult.append(["Schalte Periode von ClampControl_01 auf 0", "INFO"])
    kl15_period.setState('aus')
    testresult.append(["Warte %ss (max. Timeoutqualifizierungszeit)"%timeout_quali_max, "INFO"])
    time.sleep(timeout_quali_max)

    testresult.append(["[.] Warte 2 Sekunde, bevor DAQ Messung beendet wird", ""])
    time.sleep(2)
    testresult.append(["Stopp DAQ Measurement", "INFO"])
    daq_data = daq.stopMeasurement()
    time.sleep(0.5)

    testresult.append(["\nStart Analyse of DAQ Measurement", ""])

    # Startzeitpunkt = ClampControl_01 Periode == 0
    period_data = daq_data[str(kl15_period)]
    analyse_period_data = eval_signal.EvalSignal(period_data)
    analyse_period_data.clearAll()

    time_zero = analyse_period_data.getTime()
    stop_period_time = analyse_period_data.find(operator="==", value=0)

    # Zeitpunkt Waehlhebel_04:WH_Fahrstufe = Fehlerwert
    wh_fahrstufe_data = daq_data[str(wh_fahrstufe)]
    analyse_wh_fahrstufe_data = eval_signal.EvalSignal(wh_fahrstufe_data)
    analyse_wh_fahrstufe_data.clearAll()

    fehlerwert_timestamp = analyse_wh_fahrstufe_data.find(operator="==", value=wh_fahrstufe_fehlerwert)

    # Zeitpunkt NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15 = 0 (aus) - Ersatzwert
    kl15_status_data = daq_data[str(kl15_status_var)]
    analyse_kl15_status_data = eval_signal.EvalSignal(kl15_status_data)
    analyse_kl15_status_data.clearAll()

    ersatzwert_timestamp = analyse_kl15_status_data.find(operator="==", value=0)

    testresult.append(["[.] Prüfe, dass Waehlhebel_04:WH_Fahrstufe nach max %ss Fehlerwert setzt"%fehlerwert_timer_s, ""])
    if fehlerwert_timestamp:
        testresult.append(
            basic_tests.checkRange(
                value=fehlerwert_timestamp-stop_period_time,
                min_value=0,
                max_value=fehlerwert_timer_s,
                descr="Prüfe, dass Fehlerwert in erwarteter Zeit gesetzt wird"
            )
        )
    else:
        testresult.append(["Prüfe Waehlhebel_04:WH_Fahrstufe wurde nicht auf den Fehlerwert %s nicht gesetzt"%wh_fahrstufe_fehlerwert, "PASSED"])

    testresult.append(["[.] Prüfe, dass NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15 nach frühestens %ss und max %ss Ersatzwert setzt"
                       %(timeout_quali_min, timeout_quali_max), ""])
    if ersatzwert_timestamp:
        testresult.append(
            basic_tests.checkRange(
                value=ersatzwert_timestamp-stop_period_time,
                min_value=timeout_quali_min,
                max_value=timeout_quali_max,
                descr="Prüfe, dass Ersatzwert in erwarteter Zeit gesetzt wird"
            )
        )
    else:
        testresult.append(["Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15 wurde nicht auf den Ersatzwert (0, aus) gesetzt", "FAILED"])

    testresult.append(["[.] Schalte Senden von ClampControl_01 wieder an", ""])
    testresult.append(["Schalte Periode von ClampControl_01 auf %sms"%cycle_time, "INFO"])
    kl15_period.setState('an')
    time.sleep(cycle_time/1000.0)

    testresult.append(["[.] Prüfe aktuellen KL15 Status der NM_Waehlhebel Botschaft", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=kl15_status_var,
            nominal_status=1,
            descr="Prüfe, dass KL15 Status == 1 (an) ist"
        )
    )

    testresult.append(["[.] Prüfe aktuellen Wert der Waehlhebel_04:WH_Fahrstufe", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=wh_fahrstufe,
            nominal_status=current_fahrstufe,
            descr="Prüfe, dass Waehlhebel_04:WH_Fahrstufe == %s ist"%current_fahrstufe
        )
    )

    # erzeuge Plot für Testreport (ohne KL15)
    plot_data = {}
    for mes in [kl15_status_var, wh_fahrstufe]:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(
        daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0]),
                          v_lines={1: {'x': stop_period_time - time_zero, 'label': "ClampControl_01 Periode = 0"},
                                   2: {'x': stop_period_time - time_zero+timeout_quali_min, 'label': "min. Timeoutqualifizierungszeit"},
                                   3: {'x': stop_period_time - time_zero+timeout_quali_max, 'label': "max. Timeoutqualifizierungszeit"},}
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
