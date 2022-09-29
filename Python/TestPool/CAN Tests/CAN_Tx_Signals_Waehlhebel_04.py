#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Tx_Signals_Waehlhebel_04.py
# Title   : CAN Tx Signals Waehlhebel 04
# Task    : Test of ECU-Tx => HIL-Rx Signals of CAN Message Waehlhebel_04
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
# 1.3  | 24.09.2021 | Mohammed | added correct cal-variable from .a2l
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
    setTestcaseId(testresult, 'Waehlhebel_04__Waehlhebel_04_CRC')
    testresult.append(["\nMessage/PDU: Waehlhebel_04:Waehlhebel_04_CRC", ""]) 

    # #########################################################################
    # Waehlhebel_04:Waehlhebel_04_CRC
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                8 bits
    # Valid range (raw+phys):    [0x00..0xFF] 
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x00..0xFF]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_GearProcessing_PIM_Waehlhebel_04_Waehlhebel_04_CRC, # Added correct cal-variable from .a2l
        check_sig    = can_bus.Waehlhebel_04__Waehlhebel_04_CRC__value,
        set_values   = [0x00, 0x80, 0xFF],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Waehlhebel_04__WH_Zustand_N_Haltephase_2')
    testresult.append(["\nMessage/PDU: Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""]) 

    # #########################################################################
    # Waehlhebel_04:WH_Zustand_N_Haltephase_2
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                3 bits
    # Lookup (raw):
    #   0x0: inaktiv
    #   0x1: aktiv_Timer_laeuft
    #   0x2: beendet_Timer_abgelaufen
    #   0x3: beendet_P_taste_betaetigt
    #   0x5: aktiv_Hinweismeldung
    # Valid range (raw+phys):    [0x0..0x7] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1, 0x2, 0x3, 0x5]
    # Total range (raw+phys):    [0x0..0x7]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_GearProcessing_PIM_Waehlhebel_04_WH_Zustand_N_Haltephase_2, # Added correct cal-variable from .a2l
        check_sig    = can_bus.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
        set_values   = [0x0, 0x1, 0x2, 0x3, 0x5],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Waehlhebel_04__Waehlhebel_04_BZ')
    testresult.append(["\nMessage/PDU: Waehlhebel_04:Waehlhebel_04_BZ", ""]) 

    # #########################################################################
    # Waehlhebel_04:Waehlhebel_04_BZ
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                4 bits
    # Valid range (raw+phys):    [0x0..0xF] 
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x0..0xF]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_GearProcessing_PIM_Waehlhebel_04_Waehlhebel_04_BZ, # Added correct cal-variable from .a2l
        check_sig    = can_bus.Waehlhebel_04__Waehlhebel_04_BZ__value,
        set_values   = [0x0, 0x8, 0xF],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Waehlhebel_04__WH_SensorPos_roh')
    testresult.append(["\nMessage/PDU: Waehlhebel_04:WH_SensorPos_roh", ""]) 

    # #########################################################################
    # Waehlhebel_04:WH_SensorPos_roh
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                4 bits
    # Lookup (raw):
    #   0x0: Init
    #   0x1: Pos_1
    #   0x2: Pos_2
    #   0x3: Pos_3
    #   0x4: Pos_4
    #   0x5: Pos_5
    #   0x6: Pos_6
    #   0x7: Pos_7
    #   0x8: Pos_8
    #   0x9: Pos_9
    #   0xA: Pos_10
    #   0xB: Pos_11
    #   0xC: Pos_12
    #   0xD: Pos_13
    #   0xE: Pos_14
    #   0xF: Fehler
    # Valid range (raw+phys):    [0x0..0xE] 
    # Invalid range (raw+phys):  ]0xE..0xF] => [0xF..0xF]
    # Valid states (raw+phys):   [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE]
    # Invalid states (raw+phys): [0xF]
    # Total range (raw+phys):    [0x0..0xF]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_GearProcessing_PIM_Waehlhebel_04_WH_SensorPos_roh, # Added correct cal-variable from .a2l
        check_sig    = can_bus.Waehlhebel_04__WH_SensorPos_roh__value,
        set_values   = [0x0, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xD, 0xE],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Waehlhebel_04__WH_Entsperrtaste_02')
    testresult.append(["\nMessage/PDU: Waehlhebel_04:WH_Entsperrtaste_02", ""]) 

    # #########################################################################
    # Waehlhebel_04:WH_Entsperrtaste_02
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                2 bits
    # Lookup (raw):
    #   0x0: Init_nicht_verbaut
    #   0x1: nicht_betaetigt
    #   0x2: betaetigt
    #   0x3: Fehler
    # Valid range (raw+phys):    [0x0..0x2] 
    # Invalid range (raw+phys):  ]0x2..0x3] => [0x3..0x3]
    # Valid states (raw+phys):   [0x0, 0x1, 0x2]
    # Invalid states (raw+phys): [0x3]
    # Total range (raw+phys):    [0x0..0x3]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_GearProcessing_PIM_Waehlhebel_04_WH_Entsperrtaste_02, # Added correct cal-variable from .a2l
        check_sig    = can_bus.Waehlhebel_04__WH_Entsperrtaste_02__value,
        set_values   = [0x0, 0x1, 0x2],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Waehlhebel_04__WH_Fahrstufe')
    testresult.append(["\nMessage/PDU: Waehlhebel_04:WH_Fahrstufe", ""]) 

    # #########################################################################
    # Waehlhebel_04:WH_Fahrstufe
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                4 bits
    # Lookup (raw):
    #   0x0: Init
    #   0x4: nicht_betaetigt
    #   0x5: D
    #   0x6: N
    #   0x7: R
    #   0x8: P
    #   0x9: N_ohne_Spotausleuchtung
    #   0xA: Tipp_Plus
    #   0xB: Tipp_Minus
    #   0xC: S
    #   0xE: Tipp_Gasse
    #   0xF: Fehler
    # Valid range (raw+phys):    [0x0..0xE] 
    # Invalid range (raw+phys):  ]0xE..0xF] => [0xF..0xF]
    # Valid states (raw+phys):   [0x0, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xE]
    # Invalid states (raw+phys): [0xF]
    # Total range (raw+phys):    [0x0..0xF]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_GearProcessing_PIM_Waehlhebel_04_WH_Fahrstufe, # Added correct cal-variable from .a2l
        check_sig    = can_bus.Waehlhebel_04__WH_Fahrstufe__value,
        set_values   = [0x0, 0x4, 0x5, 0x6, 0x7, 0x8, 0x9, 0xA, 0xB, 0xC, 0xE],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Waehlhebel_04__WH_P_Taste')
    testresult.append(["\nMessage/PDU: Waehlhebel_04:WH_P_Taste", ""]) 

    # #########################################################################
    # Waehlhebel_04:WH_P_Taste
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                2 bits
    # Lookup (raw):
    #   0x0: Init
    #   0x1: nicht_betaetigt
    #   0x2: betaetigt
    #   0x3: Fehler
    # Valid range (raw+phys):    [0x0..0x2] 
    # Invalid range (raw+phys):  ]0x2..0x3] => [0x3..0x3]
    # Valid states (raw+phys):   [0x0, 0x1, 0x2]
    # Invalid states (raw+phys): [0x3]
    # Total range (raw+phys):    [0x0..0x3]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_GearProcessing_PIM_Waehlhebel_04_WH_P_Taste, # Added correct cal-variable from .a2l
        check_sig    = can_bus.Waehlhebel_04__WH_P_Taste__value,
        set_values   = [0x0, 0x1, 0x2],
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
