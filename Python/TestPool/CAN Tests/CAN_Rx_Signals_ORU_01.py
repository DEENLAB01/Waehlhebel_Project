#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Rx_Signals_ORU_01.py
# Title   : CAN Rx Signals ORU 01
# Task    : Test of HIL-Tx => ECU-Rx Signals of CAN Message ORU_01
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
from simplified_bus_tests import testRxSigSeq, setTestcaseId
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
    setTestcaseId(testresult, 'ORU_01__ORU_Status')
    testresult.append(["\nMessage/PDU: ORU_01:ORU_Status", ""]) 

    # #########################################################################
    # ORU_01:ORU_Status
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                3 bits
    # Lookup (raw):
    #   0x0: IDLE
    #   0x1: PENDING
    #   0x2: PREPARATION
    #   0x3: PREPARATION_HV
    #   0x4: RUNNING
    #   0x5: RUNNING_HV
    #   0x6: PENDING_NOTREADY
    #   0x7: FAILURE_POWERTRAIN_DISABLED
    # Valid range (raw+phys):    [0x0..0x7] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7]
    # Total range (raw+phys):    [0x0..0x7]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.ORU_01__ORU_Status__value,
        check_var    = cal.ORU_01__ORU_Status, # TODO: Add correct cal-variable from .a2l
        set_values   = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7],
        check_values = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7],
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
