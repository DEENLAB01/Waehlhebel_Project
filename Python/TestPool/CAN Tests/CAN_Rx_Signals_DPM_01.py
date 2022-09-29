#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Rx_Signals_DPM_01.py
# Title   : CAN Rx Signals DPM 01
# Task    : Test of HIL-Tx => ECU-Rx Signals of CAN Message DPM_01
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
    setTestcaseId(testresult, 'DPM_01__DPM_01_CRC')
    testresult.append(["\nMessage/PDU: DPM_01:DPM_01_CRC", ""]) 

    # #########################################################################
    # DPM_01:DPM_01_CRC
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                8 bits
    # Valid range (raw+phys):    [0x00..0xFF] 
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x00..0xFF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.DPM_01__DPM_01_CRC__value,
        check_var    = cal.DPM_01__DPM_01_CRC, # TODO: Add correct cal-variable from .a2l
        set_values   = [0x00, 0x80, 0xFF],
        check_values = [0x00, 0x80, 0xFF],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'DPM_01__DPM_FlgStrtNeutHldPha')
    testresult.append(["\nMessage/PDU: DPM_01:DPM_FlgStrtNeutHldPha", ""]) 

    # #########################################################################
    # DPM_01:DPM_FlgStrtNeutHldPha
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: NoRequest
    #   0x1: StartNeutralHoldPhase
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.DPM_01__DPM_FlgStrtNeutHldPha__value,
        check_var    = cal.DPM_01__DPM_FlgStrtNeutHldPha, # TODO: Add correct cal-variable from .a2l
        set_values   = [0x0, 0x1],
        check_values = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'DPM_01__DPM_01_BZ')
    testresult.append(["\nMessage/PDU: DPM_01:DPM_01_BZ", ""]) 

    # #########################################################################
    # DPM_01:DPM_01_BZ
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                4 bits
    # Valid range (raw+phys):    [0x0..0xF] 
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x0..0xF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.DPM_01__DPM_01_BZ__value,
        check_var    = cal.DPM_01__DPM_01_BZ, # TODO: Add correct cal-variable from .a2l
        set_values   = [0x0, 0x8, 0xF],
        check_values = [0x0, 0x8, 0xF],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'DPM_01__DPM_StLghtDrvPosn')
    testresult.append(["\nMessage/PDU: DPM_01:DPM_StLghtDrvPosn", ""]) 

    # #########################################################################
    # DPM_01:DPM_StLghtDrvPosn
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                4 bits
    # Lookup (raw):
    #   0x0: Init
    #   0x5: D
    #   0x6: N
    #   0x7: R
    #   0x8: P
    #   0xC: S
    #   0xF: Fehler
    # Valid range (raw+phys):    [0x0..0xE] 
    # Invalid range (raw+phys):  ]0xE..0xF] => [0xF..0xF]
    # Valid states (raw+phys):   [0x0, 0x5, 0x6, 0x7, 0x8, 0xC]
    # Invalid states (raw+phys): [0xF]
    # Total range (raw+phys):    [0x0..0xF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.DPM_01__DPM_StLghtDrvPosn__value,
        check_var    = cal.DPM_01__DPM_StLghtDrvPosn, # TODO: Add correct cal-variable from .a2l
        set_values   = [0x0, 0x5, 0x6, 0x7, 0x8, 0xC],
        check_values = [0x0, 0x5, 0x6, 0x7, 0x8, 0xC],
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
