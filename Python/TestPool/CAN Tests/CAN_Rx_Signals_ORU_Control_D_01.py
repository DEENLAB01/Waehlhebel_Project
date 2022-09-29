#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Rx_Signals_ORU_Control_D_01.py
# Title   : CAN Rx Signals ORU Control D 01
# Task    : Test of HIL-Tx => ECU-Rx Signals of CAN Message ORU_Control_D_01
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
# 1.3  | 24.08.2021 | Mohammed   | Reworked after new a2L file
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

    '''
    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'ORU_Control_D_01__ORU_Control_D_01_BZ')
    testresult.append(["\nMessage/PDU: ORU_Control_D_01:ORU_Control_D_01_BZ", ""]) 

    # #########################################################################
    # ORU_Control_D_01:ORU_Control_D_01_BZ
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                4 bits
    # Valid range (raw+phys):    [0x0..0xF] 
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x0..0xF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.ORU_Control_D_01__ORU_Control_D_01_BZ__value,
        check_var    = cal.Sw_GSL_OTA_PIM_SG_ORU_Control_D_01_ORU_Control_D_01_BZ, # Added correct cal-variable from .a2l
        set_values   = [0x0, 0x8, 0xF],
        check_values = [0x0, 0x8, 0xF],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

'''
    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'ORU_Control_D_01__OnlineRemoteUpdateControlD')
    testresult.append(["\nMessage/PDU: ORU_Control_D_01:OnlineRemoteUpdateControlD", ""]) 

    # #########################################################################
    # ORU_Control_D_01:OnlineRemoteUpdateControlD
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                4 bits
    # Lookup (raw):
    #   0x0: IDLE
    #   0x1: PENDING
    #   0x2: PREPARATION
    #   0x3: PREPARATION_HV
    #   0x4: RUNNING
    #   0x5: RUNNING_HV
    #   0x6: PENDING_NOTREADY
    #   0x7: OTA_FAILURE_POWERTRAIN_DISABLED
    #   0x8: FUNCTIONAL_SAFETY_RELEASE
    #   0x9: PREPARATION_SG
    #   0xF: Fehler
    # Valid range (raw+phys):    [0x0..0xE] 
    # Invalid range (raw+phys):  ]0xE..0xF] => [0xF..0xF]
    # Valid states (raw+phys):   [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9]
    # Invalid states (raw+phys): [0xF]
    # Total range (raw+phys):    [0x0..0xF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.ORU_Control_D_01__OnlineRemoteUpdateControlD__value,
        check_var    = cal.Sw_GSL_OTA_PIM_SG_ORU_Control_D_01_OnlineRemoteUpdateControlD, # Added correct cal-variable from .a2l
        set_values   = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9],
        check_values = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    '''
    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'ORU_Control_D_01__ORU_Control_D_01_CRC')
    testresult.append(["\nMessage/PDU: ORU_Control_D_01:ORU_Control_D_01_CRC", ""]) 

    # #########################################################################
    # ORU_Control_D_01:ORU_Control_D_01_CRC
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                8 bits
    # Valid range (raw+phys):    [0x00..0xFF] 
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x00..0xFF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.ORU_Control_D_01__ORU_Control_D_01_CRC__value,
        check_var    = cal.Sw_GSL_OTA_PIM_SG_ORU_Control_D_01_ORU_Control_D_01_CRC, # Added correct cal-variable from .a2l
        set_values   = [0x00, 0x80, 0xFF],
        check_values = [0x00, 0x80, 0xFF],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'ORU_Control_D_01__OnlineRemoteUpdateControlOldD')
    testresult.append(["\nMessage/PDU: ORU_Control_D_01:OnlineRemoteUpdateControlOldD", ""]) 

    # #########################################################################
    # ORU_Control_D_01:OnlineRemoteUpdateControlOldD
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                4 bits
    # Lookup (raw):
    #   0x0: IDLE
    #   0x1: PENDING
    #   0x2: PREPARATION
    #   0x3: PREPARATION_HV
    #   0x4: RUNNING
    #   0x5: RUNNING_HV
    #   0x6: PENDING_NOTREADY
    #   0x7: OTA_FAILURE_POWERTRAIN_DISABLED
    #   0x8: FUNCTIONAL_SAFETY_RELEASE
    #   0x9: PREPARATION_SG
    #   0xF: Fehler
    # Valid range (raw+phys):    [0x0..0xE] 
    # Invalid range (raw+phys):  ]0xE..0xF] => [0xF..0xF]
    # Valid states (raw+phys):   [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9]
    # Invalid states (raw+phys): [0xF]
    # Total range (raw+phys):    [0x0..0xF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.ORU_Control_D_01__OnlineRemoteUpdateControlOldD__value,
        check_var    = cal.Sw_GSL_OTA_PIM_SG_ORU_Control_D_01_OnlineRemoteUpdateControlOldD, # Added correct cal-variable from .a2l
        set_values   = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9],
        check_values = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())
    '''
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
