#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Rx_Signals_OTAMC_D_01.py
# Title   : CAN Rx Signals OTAMC D 01
# Task    : Test of HIL-Tx => ECU-Rx Signals of CAN Message OTAMC_D_01
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
    #testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST PROCESS ############################################################

    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'OTAMC_D_01__VehicleProtectedEnvironment_D')
    testresult.append(["\nMessage/PDU: OTAMC_D_01:VehicleProtectedEnvironment_D", ""]) 

    # #########################################################################
    # OTAMC_D_01:VehicleProtectedEnvironment_D
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                2 bits
    # Lookup (raw):
    #   0x0: VPE_none
    #   0x1: VPE_production
    #   0x2: VPE_aftersales
    # Valid range (raw+phys):    [0x0..0x3] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1, 0x2]
    # Total range (raw+phys):    [0x0..0x3]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.OTAMC_D_01__VehicleProtectedEnvironment_D__value,
        check_var    = cal.Sw_GSL_OTA_PIM_SG_OTAMC_D_01_VehicleProtectedEnvironment_D, # Added correct cal-variable from .a2l
        set_values   = [0x0, 0x1, 0x2],
        check_values = [0x0, 0x1, 0x2],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'OTAMC_D_01__OTAMC_D_01_CRC')
    testresult.append(["\nMessage/PDU: OTAMC_D_01:OTAMC_D_01_CRC", ""]) 

    # #########################################################################
    # OTAMC_D_01:OTAMC_D_01_CRC
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                8 bits
    # Valid range (raw+phys):    [0x00..0xFF] 
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x00..0xFF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.OTAMC_D_01__OTAMC_D_01_CRC__value,
        check_var    = cal.Sw_GSL_OTA_PIM_SG_OTAMC_D_01_OTAMC_D_01_CRC, # Added correct cal-variable from .a2l
        set_values   = [0x00, 0x80, 0xFF],
        check_values = [0x00, 0x80, 0xFF],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'OTAMC_D_01__OTAMC_D_01_BZ')
    testresult.append(["\nMessage/PDU: OTAMC_D_01:OTAMC_D_01_BZ", ""]) 

    # #########################################################################
    # OTAMC_D_01:OTAMC_D_01_BZ
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                4 bits
    # Valid range (raw+phys):    [0x0..0xF] 
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x0..0xF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.OTAMC_D_01__OTAMC_D_01_BZ__value,
        check_var    = cal.Sw_GSL_OTA_PIM_SG_OTAMC_D_01_OTAMC_D_01_BZ, # Added correct cal-variable from .a2l
        set_values   = [0x0, 0x8, 0xF],
        check_values = [0x0, 0x8, 0xF],
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
