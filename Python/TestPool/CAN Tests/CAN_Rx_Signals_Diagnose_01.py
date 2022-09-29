#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Rx_Signals_Diagnose_01.py
# Title   : CAN Rx Signals Diagnose 01
# Task    : Test of HIL-Tx => ECU-Rx Signals of CAN Message Diagnose_01
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
    testresult.append(["\x0a Kl30, Kl15 ein und Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    #testresult.append(canape_diag.checkEventMemoryEmpty())
    
    # TEST PROCESS ############################################################

    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Diagnose_01__UH_Monat')
    testresult.append(["\nMessage/PDU: Diagnose_01:UH_Monat", ""]) 

    # #########################################################################
    # Diagnose_01:UH_Monat
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                4 bits
    # Lookup (raw):
    #   0x0: Init
    #   0xE: Relatives_Datum
    #   0xF: Fehler
    # Valid range (raw+phys):    [0x1..0xC] 
    # Invalid range (raw+phys):  [0x0..0x1[ => [0x0..0x0]
    # Invalid range (raw+phys):  ]0xC..0xF] => [0xD..0xF]
    # Invalid states (raw+phys): [0x0, 0xE, 0xF]
    # Total range (raw+phys):    [0x0..0xF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.Diagnose_01__UH_Monat__value,
        check_var    = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_UH_Monat_UH_Monat, # Added correct cal-variable from .a2l
        set_values   = [0x1, 0x7, 0xC],
        check_values = [0x1, 0x7, 0xC],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Diagnose_01__UH_Tag')
    testresult.append(["\nMessage/PDU: Diagnose_01:UH_Tag", ""])

    # #########################################################################
    # Diagnose_01:UH_Tag
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                5 bits
    # Lookup (raw):
    #   0x00: Init
    # Valid range (raw+phys):    [0x01..0x1F] 
    # Invalid range (raw+phys):  [0x00..0x01[ => [0x00..0x00]
    # Invalid states (raw+phys): [0x00]
    # Total range (raw+phys):    [0x00..0x1F]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.Diagnose_01__UH_Tag__value,
        check_var    = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_UH_Tag_UH_Tag, # Added correct cal-variable from .a2l
        set_values   = [0x01, 0x10, 0x1F],
        check_values = [0x01, 0x10, 0x1F],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Diagnose_01__DW_Kilometerstand')
    testresult.append(["\nMessage/PDU: Diagnose_01:DW_Kilometerstand", ""])

    # #########################################################################
    # Diagnose_01:DW_Kilometerstand
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                20 bits
    # Lookup (raw):
    #   0xFFFFE: Init
    #   0xFFFFF: Fehler
    # Valid range (raw+phys):    [0x00000..0xFFFFD] 
    # Invalid range (raw+phys):  ]0xFFFFD..0xFFFFF] => [0xFFFFE..0xFFFFF]
    # Invalid states (raw+phys): [0xFFFFE, 0xFFFFF]
    # Total range (raw+phys):    [0x00000..0xFFFFF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.Diagnose_01__DW_Kilometerstand__value,
        check_var    = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_DW_Kilometerstand_DW_Kilometerstand, # Added correct cal-variable from .a2l
        set_values   = [0x00000, 0x7FFFF, 0xFFFFD],
        check_values = [0x00000, 0x7FFFF, 0xFFFFD],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Diagnose_01__UH_Stunde')
    testresult.append(["\nMessage/PDU: Diagnose_01:UH_Stunde", ""])

    # #########################################################################
    # Diagnose_01:UH_Stunde
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                5 bits
    # Valid range (raw+phys):    [0x00..0x17] 
    # Invalid range (raw+phys):  ]0x17..0x1F] => [0x18..0x1F]
    # Total range (raw+phys):    [0x00..0x1F]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.Diagnose_01__UH_Stunde__value,
        check_var    = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_UH_Stunde_UH_Stunde, # Added correct cal-variable from .a2l
        set_values   = [0x00, 0x0C, 0x17],
        check_values = [0x00, 0x0C, 0x17],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Diagnose_01__UH_Minute')
    testresult.append(["\nMessage/PDU: Diagnose_01:UH_Minute", ""])

    # #########################################################################
    # Diagnose_01:UH_Minute
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                6 bits
    # Valid range (raw+phys):    [0x00..0x3B] 
    # Invalid range (raw+phys):  ]0x3B..0x3F] => [0x3C..0x3F]
    # Total range (raw+phys):    [0x00..0x3F]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.Diagnose_01__UH_Minute__value,
        check_var    = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_UH_Minute_UH_Minute, #  Added correct cal-variable from .a2l
        set_values   = [0x00, 0x1E, 0x3B],
        check_values = [0x00, 0x1E, 0x3B],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Diagnose_01__UH_Jahr')
    testresult.append(["\nMessage/PDU: Diagnose_01:UH_Jahr", ""])

    # #########################################################################
    # Diagnose_01:UH_Jahr
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                7 bits
    # Valid range (raw+phys):    [0x00..0x7F] 
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x00..0x7F]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.Diagnose_01__UH_Jahr__value,
        check_var    = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_UH_Jahr_UH_Jahr, # Added correct cal-variable from .a2l
        set_values   = [0x00, 0x40, 0x7F],
        check_values = [0x00, 0x40, 0x7F],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-127'))

    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'Diagnose_01__UH_Sekunde')
    testresult.append(["\nMessage/PDU: Diagnose_01:UH_Sekunde", ""])

    # #########################################################################
    # Diagnose_01:UH_Sekunde
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                6 bits
    # Valid range (raw+phys):    [0x00..0x3B] 
    # Invalid range (raw+phys):  ]0x3B..0x3F] => [0x3C..0x3F]
    # Total range (raw+phys):    [0x00..0x3F]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.Diagnose_01__UH_Sekunde__value,
        check_var    = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_UH_Sekunde_UH_Sekunde, # Added correct cal-variable from .a2l
        set_values   = [0x00, 0x1E, 0x3B],
        check_values = [0x00, 0x1E, 0x3B],
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
