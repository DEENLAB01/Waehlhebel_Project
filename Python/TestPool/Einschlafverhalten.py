# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Einschlafverhalten.py
# Title   : Einschlafverhalten
# Task    : Test Einschlafverhalten
#
# Author  : A. Neumann
# Date    : 20.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 20.05.2021 | A. Neumann | initial
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_daq import eval_signal
from ttk_tools.rst import gamma_api #@UnresolvedImport
import time
import functions_common
import os
import pylab

# Instantiate test environment
testenv = TestEnv()


try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    fc = functions_common.FunctionsCommon(testenv)

    # variables ###############################################################
    measurement_duration_s = 1*6

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["\xa0Starte DAQ Messung (Strommessung)", ""])

    meas_var = [hil.cc_mon__A]


    testresult.append(["Starte DAQ Messung", "INFO"])
    daq.startMeasurement(meas_var)
    time.sleep(0.1)
    testresult.append(["Setze KL15 auf 0 (inactive)", "INFO"])
    hil.cl15_on__.set(0)
    testresult.append(["Schalte Senden von empfangenen Signalen aus (HiL -> ECU)", "INFO"])
    hil.can0_HIL__HIL_TX__enable.set(0)
    testresult.append(["Warte %s Sekunden"%measurement_duration_s,"INFO"])
    fc.waitSecondsWithResponse(measurement_duration_s, 10)
    testresult.append(["Stoppe DAQ Messung", "INFO"])
    daq_data = daq.stopMeasurement()

    signal_data = daq_data[str(meas_var[0])]
    analyse_signal_data = eval_signal.EvalSignal(signal_data)
    analyse_signal_data.clearAll()

    start_time = analyse_signal_data.getTime()
    time_off = analyse_signal_data.findNext(operator="<=", value= 0.01)

    if time_off:
        descr = "ECU wechselte nach %sms in the Ruhestrom"%(round(time_off -start_time,4)*1000)
        verdict = "PASSED"
    else:
        descr = "ECU wechselte während der Messung nicht in den Ruhestrom"
        verdict = "FAILED"

    save_path = r"D:\HIL-Projekte\Eissmann_HIL_Waehlhebel\Waehlhebel"
    testresult.append(
        daq.plotSingleShot(daq_data = signal_data,
                           filename="Einschlafverhalten",
                           label_signal="CC_MON_A")
    )

    testresult.append([descr, verdict])


    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU (KL15 aus, KL30 aus)", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
