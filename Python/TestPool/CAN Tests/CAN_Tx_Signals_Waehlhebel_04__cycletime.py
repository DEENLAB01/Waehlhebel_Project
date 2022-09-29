#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Tx_Signals_Waehlhebel_04__cycletime.py
# Title   : CAN Tx Signals Waehlhebel 04 cycletime
# Task    : Test Cycletime of ECU-Tx => HIL-Rx Signals of CAN Message DS_Waehlhebel
#
# Author  : A. Neumann
# Date    : 11.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 11.05.2021 | A. Neumann | initial
# 1.1  | 24.01.2022 | Mohammed   | Reworked
#******************************************************************************
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

    # Initialize variables ####################################################
    cycle_time_ms       = 10
    tolerance_percent   = 0.10
    
    # set Testcase ID #########################################################
    #testenv.setTCID(mdd=None, mdp=None, cabin=None, private=None)
    testresult.setTestcaseId("CAN_142")
    
    # TEST PRE CONDITIONS #####################################################
    testresult.append([" \x0aKl30 und Kl15 ein ", ""])
    testenv.startupECU()
    testresult.append([" \x0aLese Fehlerspeicher (muss leer sein)", ""])
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())
    
    # TEST PROCESS ############################################################
    testresult.append(['Check the cycle time of the message Waehlhebel_04.','INFO'])
    testresult.append(
        simplified_bus_tests.checkTiming(
            time_stamp_variable=hil.Waehlhebel_04__timestamp,
            cycle_time_value_ms=cycle_time_ms,
            message_name="Waehlhebel_04",
            tol_perc = tolerance_percent,
            operator = "==")
            )
    
    
    # TEST POST CONDITIONS ####################################################
    testenv.shutdownECU()
    
    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
