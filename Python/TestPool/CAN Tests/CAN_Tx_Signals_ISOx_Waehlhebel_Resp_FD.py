# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Tx_Signals_ISOx_Waehlhebel_Resp_FD.py.py
# Title   : CAN RX Signals ISOx_Waehlhebel_Resp_FD cycletime
# Task    : Test Cycletime of ECU-Tx => HIL-Rx Signals of CAN Message ISOx_Waehlhebel_Resp_FD
#
# Author  : Mohammed Abdul Karim
# Date    : 24.01.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 24.01.2022 | Mohammed | initial
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import simplified_bus_tests
import time
from ttk_daq import eval_signal
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

    # Initialize variables ####################################################
    cycle_time_ms = 2000
    tolerance_percent = 0.10

    # set Testcase ID #########################################################
    # testenv.setTCID(mdd=None, mdp=None, cabin=None, private=None)
    testresult.setTestcaseId("CAN_57")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[+] Kl30, Kl15 ein und Lese Fehlerspeicher (muss leer sein)", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST PROCESS ############################################################
    testresult.append(["[.] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    testresult.append(["\x0a Check the cycle time of the message ISOx_Waehlhebel_Resp_FD:Zykluszeit von 2s + +/-10ms gesendet ", "INFO"])
    testresult.append(
        simplified_bus_tests.checkTiming(
            time_stamp_variable=hil.ISOx_Waehlhebel_Resp_FD__timestamp,
            cycle_time_value_ms=cycle_time_ms,
            message_name="ISOx_Waehlhebel_Resp_FD",
            tol_perc=tolerance_percent,
            operator="==")
    )

    testresult.append(["[.] Tester Present deaktivieren", ""])
    testresult.append(["\x0a Check the cycle time of the message ISOx_Waehlhebel_Resp_FD:nicht mehr gesendet", "INFO"])
    canape_diag.disableTesterPresent()

    testresult.append(
        simplified_bus_tests.checkNoTiming(
            time_stamp_variable=hil.ISOx_Waehlhebel_Resp_FD__timestamp,
            cycle_time_value_ms=cycle_time_ms,
            message_name="ISOx_Waehlhebel_Resp_FD",
        )
    )

    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST POST CONDITIONS ####################################################
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
