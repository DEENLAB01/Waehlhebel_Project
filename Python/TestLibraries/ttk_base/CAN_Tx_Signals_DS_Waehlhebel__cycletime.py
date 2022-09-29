#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Tx_Signals_DS_Waehlhebel__cycletime.py
# Title   : CAN Tx Signals DS Waehlhebel__cycletime
# Task    : Test of Cycle time ECU-Tx => HIL-Rx Signals of CAN Message DS_Waehlhebel
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
    cal = testenv.getCal()
    
    # Initialize variables ####################################################
    cycle_time_ms       = 1000
    inhibitzeit_ms      = 80
    tolerance_percent   = 10
    
    # set Testcase ID #########################################################
    #testenv.setTCID(mdd=None, mdp=None, cabin=None, private=None)
    
    # TEST PRE CONDITIONS #####################################################
    testenv.startupECU()  
    
    # TEST PROCESS ############################################################
    testresult.append(['Check the cycle time of the message DS_Waehlhebel.','INFO'])
    testresult.append(
        simplified_bus_tests.checkTiming(
            time_stamp_variable=hil.DS_Waehlhebel__timestamp, 
            cycle_time_value_ms=1000,
            message_name="DS_Waehlhebel",
            tol_perc=tolerance_percent,
            operator = "==")
            )

    # Anna Neumann: aktuell noch nicht testbar
    # testresult.append(['Check the inhibit cycle time of the message DS_Waehlhebel.','INFO'])
    # testresult.append(
    #     simplified_bus_tests.checkInhibitTiming(
    #         time_stamp_variable=hil.DS_Waehlhebel__timestamp,
    #         set_variable = hil.DS_Waehlhebel__DS_Waehlhebel_ConfDTCChanged__value,
    #         set_values = [0x0, 0x1],
    #         cycle_time_value_ms = 1000,
    #         message_name="DS_Waehlhebel",
    #         inhibit_time_ms = 80,
    #         tol_perc=tolerance_percent,
    #         )
    #     )
    
    # TEST POST CONDITIONS ####################################################
    testenv.shutdownECU()
    
    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
