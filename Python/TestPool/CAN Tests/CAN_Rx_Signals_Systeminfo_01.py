#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Rx_Signals_Systeminfo_01.py
# Title   : CAN Rx Signals Systeminfo 01
# Task    : Test of HIL-Tx => ECU-Rx Signals of CAN Message Systeminfo_01
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
    setTestcaseId(testresult, 'Systeminfo_01__SI_P_Mode_gueltig')
    testresult.append(["\nMessage/PDU: Systeminfo_01:SI_P_Mode_gueltig", ""]) 

    # #########################################################################
    # Systeminfo_01:SI_P_Mode_gueltig
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: dezentraler_Produktionsmode
    #   0x1: zentraler_Produktionsmode
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.Systeminfo_01__SI_P_Mode_gueltig__value,
        check_var    = cal.Systeminfo_01__SI_P_Mode_gueltig, # TODO: Add correct cal-variable from .a2l
        set_values   = [0x0, 0x1],
        check_values = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Systeminfo_01__SI_P_Mode')
    testresult.append(["\nMessage/PDU: Systeminfo_01:SI_P_Mode", ""]) 

    # #########################################################################
    # Systeminfo_01:SI_P_Mode
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: inaktiv
    #   0x1: aktiv
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.Systeminfo_01__SI_P_Mode__value,
        check_var    = cal.Systeminfo_01__SI_P_Mode, # TODO: Add correct cal-variable from .a2l
        set_values   = [0x0, 0x1],
        check_values = [0x0, 0x1],
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
