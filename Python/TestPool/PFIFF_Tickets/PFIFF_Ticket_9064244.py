# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : PFIFF_Ticket_9064244.py
# Title   : CAN Tx Signals NM Waehlhebel cycletime
# Task    : Test of Cycle time ECU-Tx => HIL-Rx Signals of CAN Message NM_Waehlhebel
#
# Author  : Mohammed Abdul Karim
# Date    : 10.08.2022
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 10.08.2022 | Mohammed   | initial
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import simplified_bus_tests

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    # cal = testenv.getCal()

    # Initialize variables ####################################################
    cycle_time_ms = 200
    inhibitzeit_ms = 10
    tolerance_percent = 0.10

    # set Testcase ID #########################################################
    # testenv.setTCID(mdd=None, mdp=None, cabin=None, private=None)
    testresult.setTestcaseId("PFIFF_9064244")

    # TEST PRE CONDITIONS #####################################################
    testresult.append([" \x0aKl30 und Kl15 ein ", ""])
    testenv.startupECU()
    testresult.append([" \x0aLese Fehlerspeicher (muss leer sein)", ""])
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST PROCESS ############################################################
    testresult.append(['Check the cycle time of the message NM_Waehlhebel.', 'INFO'])
    testresult.append(
        simplified_bus_tests.checkTiming(
            time_stamp_variable=hil.NM_Waehlhebel__timestamp,
            cycle_time_value_ms=cycle_time_ms,
            message_name="NM_Waehlhebel",
            tol_perc=tolerance_percent,
            operator="==")
    )

    # TEST POST CONDITIONS ####################################################
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
