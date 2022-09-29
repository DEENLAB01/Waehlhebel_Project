#******************************************************************************
# -*- coding: latin1 -*-
# File    : Fehlererkennung_Timeout_Kl15_AN.py
# Title   : Fehlererkennung Timeout KL15 AN
# Task    : Fehlererkennungund Behandlung bei KL15 Timeout
#
# Author  : Mohammed Abdul Karim
# Date    : 27.01.2022
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 27.01.2022 | Mohammed | initial

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
    testresult.append(["[+] ECU einschalten: KL15 an", ""])
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

    testresult.append(["[+] Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15 == 1 (an)", ""])
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

    testresult.append(["[.] Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15 == 1 (an)", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=kl15_status_var,
            nominal_status=1,
            descr="Prüfe, dass KL15 Status == 1 (an) ist"
        )
    )

    testresult.append(["[.] Schalte Senden von ClampControl_01 wieder an", ""])
    testresult.append(["Schalte Periode von ClampControl_01 auf %sms"%cycle_time, "INFO"])
    kl15_period.setState('an')
    time.sleep(cycle_time/1000.0)

    testresult.append(["[.] Warte 200 ms ", ""])
    time.sleep(.200)

    testresult.append(["[.] Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15 == 1 (an)", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=kl15_status_var,
            nominal_status=1,
            descr="Prüfe, dass KL15 Status == 1 (an) ist"
        )
    )

    testresult.append(["[.] Prüfe Waehlhebel_04:WH_Fahrstufe == gespeicherter Wert (Vorbedingungen)", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=wh_fahrstufe,
            nominal_status=current_fahrstufe,
            descr="Prüfe, dass Waehlhebel_04:WH_Fahrstufe == %s ist"%current_fahrstufe
        )
    )

    testresult.append(["Stopp DAQ Measurement", "INFO"])
    daq_data = daq.stopMeasurement()
    time.sleep(.50)
    # erzeuge Plot für Testreport (ohne KL15)
    plot_data = {}
    for mes in [kl15_period, kl15_status_var, wh_fahrstufe]:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(
        daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))



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
