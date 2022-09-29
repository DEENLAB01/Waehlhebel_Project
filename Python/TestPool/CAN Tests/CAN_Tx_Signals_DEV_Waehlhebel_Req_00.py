#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Tx_Signals_DEV_Waehlhebel_Req_00.py
# Title   : CAN Tx Signals DEV Waehlhebel Req 00
# Task    : Test of ECU-Tx => HIL-Rx Signals of CAN Message DEV_Waehlhebel_Req_00
#
# Author  : A. Neumann
# Date    : 07.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 07.05.2021 | A. Neumann | initial
# 1.1  | 26.05.2021 | A. Neumann | Generate signaltests for Eissmann
# 1.2  | 24.08.2021 | M. Mushtaq | change HIL var to Can bus var
#******************************************************************************
from _automation_wrapper_ import TestEnv
testenv = TestEnv()
# Imports #####################################################################
from simplified_bus_tests import testTxSigSeq, setTestcaseId
try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()
    
    # Initialize functions ####################################################
    hil = testenv.getHil()
    testenv.startupECU()  # startup before cal vars are called
    cal = testenv.getCal()
    can_bus = testenv.getCanBus()
    canape_diag = testenv.getCanapeDiagnostic()
    
    # TEST PRE CONDITIONS #####################################################
    testresult.append(canape_diag.checkEventMemoryEmpty())
    
    # TEST PROCESS ############################################################


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'DEV_Waehlhebel_Req_00__DEV_Waehlhebel_Req_00_Data')
    testresult.append(["\nMessage/PDU: DEV_Waehlhebel_Req_00:DEV_Waehlhebel_Req_00_Data", ""]) 

    # #########################################################################
    # DEV_Waehlhebel_Req_00:DEV_Waehlhebel_Req_00_Data
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                64 bits
    # Valid range (raw+phys):    [0x0000000000000000..0xFFFFFFFFFFFFFFFF] 
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x0000000000000000..0xFFFFFFFFFFFFFFFF]
    testresult.append(testTxSigSeq(
        set_var      = cal.DEV_Waehlhebel_Req_00__DEV_Waehlhebel_Req_00_Data, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.DEV_Waehlhebel_Req_00__DEV_Waehlhebel_Req_00_Data__value,
        set_values   = [0x0000000000000000, 0x8000000000000000, 0x10000000000000000],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())
    
    # clear any currently used test case id ###################################
    testresult.clearTestcaseId()
    
    # TEST POST CONDITIONS ####################################################
    testresult.append(["\nTest Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()
    
    # cleanup
    cal = None
    hil = None
    can_bus = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
