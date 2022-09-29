#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Rx_Signals_NVEM_12.py
# Title   : CAN Rx Signals NVEM 12
# Task    : Test of HIL-Tx => ECU-Rx Signals of CAN Message NVEM_12
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
# 1.3  | 02.11.2021 | Mohammed | added correct cal-variable from .a2l
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
    testresult.append(["[+] Kl30, Kl15 ein und Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())
    
    # TEST PROCESS ############################################################


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'NVEM_12__NVEM_Abschaltstufe')
    testresult.append(["\nMessage/PDU: NVEM_12:NVEM_Abschaltstufe", ""]) 

    # #########################################################################
    # NVEM_12:NVEM_Abschaltstufe
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                2 bits
    # Lookup (raw):
    #   0x0: Stufe_0_keine_Einschraenkung
    #   0x1: Stufe_1
    #   0x2: Stufe_2
    #   0x3: Stufe_3
    # Valid range (raw+phys):    [0x0..0x3] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1, 0x2, 0x3]
    # Total range (raw+phys):    [0x0..0x3]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.NVEM_12__NVEM_Abschaltstufe__value,
        check_var    = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_NVEM_Abschaltstufe_NVEM_Abschaltstufe, # Added correct cal-variable from .a2l
        set_values   = [0x0, 0x1, 0x2, 0x3],
        check_values = [0x0, 0x1, 0x2, 0x3],
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
