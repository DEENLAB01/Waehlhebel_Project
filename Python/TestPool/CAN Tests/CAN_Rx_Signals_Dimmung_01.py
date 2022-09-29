#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Rx_Signals_Dimmung_01.py
# Title   : CAN Rx Signals Dimmung 01
# Task    : Test of HIL-Tx => ECU-Rx Signals of CAN Message Dimmung_01
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
    setTestcaseId(testresult, 'Dimmung_01__DI_KL_58xd')
    testresult.append(["\nMessage/PDU: Dimmung_01:DI_KL_58xd", ""]) 

    # #########################################################################
    # Dimmung_01:DI_KL_58xd
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                8 bits
    # Lookup (raw):
    #   0xFE: Init
    #   0xFF: Fehler
    # Valid range (raw+phys):    [0x00..0xFD] 
    # Invalid range (raw+phys):  ]0xFD..0xFF] => [0xFE..0xFF]
    # Invalid states (raw+phys): [0xFE, 0xFF]
    # Total range (raw+phys):    [0x00..0xFF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.Dimmung_01__DI_KL_58xd__value,
        check_var    = cal.Dimmung_01__DI_KL_58xd, # TODO: Add correct cal-variable from .a2l
        set_values   = [0x00, 0x7F, 0xFD],
        check_values = [0x00, 0x7F, 0xFD],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Dimmung_01__DI_KL_58xt')
    testresult.append(["\nMessage/PDU: Dimmung_01:DI_KL_58xt", ""]) 

    # #########################################################################
    # Dimmung_01:DI_KL_58xt
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                7 bits
    # Lookup (raw):
    #   0x7E: Init
    #   0x7F: Fehler
    # Valid range (raw+phys):    [0x00..0x64] 
    # Invalid range (raw+phys):  ]0x64..0x7F] => [0x65..0x7F]
    # Invalid states (raw+phys): [0x7E, 0x7F]
    # Total range (raw+phys):    [0x00..0x7F]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.Dimmung_01__DI_KL_58xt__value,
        check_var    = cal.Dimmung_01__DI_KL_58xt, # TODO: Add correct cal-variable from .a2l
        set_values   = [0x00, 0x32, 0x64],
        check_values = [0x00, 0x32, 0x64],
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
