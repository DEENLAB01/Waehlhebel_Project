#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Tx_Signals_DS_Waehlhebel.py
# Title   : CAN Tx Signals DS Waehlhebel
# Task    : Test of ECU-Tx => HIL-Rx Signals of CAN Message DS_Waehlhebel
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
    setTestcaseId(testresult, 'DS_Waehlhebel__DS_Waehlhebel_StMemChanged')
    testresult.append(["\nMessage/PDU: DS_Waehlhebel:DS_Waehlhebel_StMemChanged", ""]) 

    # #########################################################################
    # DS_Waehlhebel:DS_Waehlhebel_StMemChanged
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
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_DS_Waehlhebel_StMemChanged_DS_Waehlhebel_StMemChanged, # Added correct cal-variable from .a2l
        check_sig    = can_bus.DS_Waehlhebel__DS_Waehlhebel_StMemChanged__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'DS_Waehlhebel__DS_Waehlhebel_Lokalaktiv')
    testresult.append(["\nMessage/PDU: DS_Waehlhebel:DS_Waehlhebel_Lokalaktiv", ""]) 

    # #########################################################################
    # DS_Waehlhebel:DS_Waehlhebel_Lokalaktiv
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: war_nicht_lokal_aktiv
    #   0x1: war_lokal_aktiv
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_Diag_NM_Waehlhebel_Lokalaktiv_NM_Waehlhebel_Lokalaktiv, # Added correct cal-variable from .a2l
        check_sig    = can_bus.DS_Waehlhebel__DS_Waehlhebel_Lokalaktiv__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'DS_Waehlhebel__DS_Waehlhebel_DiagAdr')
    testresult.append(["\nMessage/PDU: DS_Waehlhebel:DS_Waehlhebel_DiagAdr", ""]) 

    # #########################################################################
    # DS_Waehlhebel:DS_Waehlhebel_DiagAdr
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                16 bits
    # Valid range (raw+phys):    [0x0000..0xFFFF] 
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x0000..0xFFFF]
    '''
    testresult.append(testTxSigSeq(
        set_var      = cal.DS_Waehlhebel__DS_Waehlhebel_DiagAdr, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.DS_Waehlhebel__DS_Waehlhebel_DiagAdr__value,
        set_values   = [0x0000, 0x8000, 0xFFFF],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())
'''

    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'DS_Waehlhebel__DS_Waehlhebel_IdentValid')
    testresult.append(["\nMessage/PDU: DS_Waehlhebel:DS_Waehlhebel_IdentValid", ""]) 

    # #########################################################################
    # DS_Waehlhebel:DS_Waehlhebel_IdentValid
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: Ungueltig
    #   0x1: Gueltig
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_DS_Waehlhebel_IdentValid_DS_Waehlhebel_IdentValid, # Added correct cal-variable from .a2l
        check_sig    = can_bus.DS_Waehlhebel__DS_Waehlhebel_IdentValid__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'DS_Waehlhebel__DS_Waehlhebel_MemSelChanged')
    testresult.append(["\nMessage/PDU: DS_Waehlhebel:DS_Waehlhebel_MemSelChanged", ""]) 

    # #########################################################################
    # DS_Waehlhebel:DS_Waehlhebel_MemSelChanged
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
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_DS_Waehlhebel_MemSelChanged_DS_Waehlhebel_MemSelChanged, # Added correct cal-variable from .a2l
        check_sig    = can_bus.DS_Waehlhebel__DS_Waehlhebel_MemSelChanged__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'DS_Waehlhebel__DS_Waehlhebel_MemSel10Changed')
    testresult.append(["\nMessage/PDU: DS_Waehlhebel:DS_Waehlhebel_MemSel10Changed", ""]) 

    # #########################################################################
    # DS_Waehlhebel:DS_Waehlhebel_MemSel10Changed
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
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_DS_Waehlhebel_MemSel10Changed_DS_Waehlhebel_MemSel10Changed, # Added correct cal-variable from .a2l
        check_sig    = can_bus.DS_Waehlhebel__DS_Waehlhebel_MemSel10Changed__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'DS_Waehlhebel__DS_Waehlhebel_ConfDTCChanged')
    testresult.append(["\nMessage/PDU: DS_Waehlhebel:DS_Waehlhebel_ConfDTCChanged", ""]) 

    # #########################################################################
    # DS_Waehlhebel:DS_Waehlhebel_ConfDTCChanged
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
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_DS_Waehlhebel_ConfDTCChanged_DS_Waehlhebel_ConfDTCChanged, # Added correct cal-variable from .a2l
        check_sig    = can_bus.DS_Waehlhebel__DS_Waehlhebel_ConfDTCChanged__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'DS_Waehlhebel__DS_Waehlhebel_TestFailedChanged')
    testresult.append(["\nMessage/PDU: DS_Waehlhebel:DS_Waehlhebel_TestFailedChanged", ""]) 

    # #########################################################################
    # DS_Waehlhebel:DS_Waehlhebel_TestFailedChanged
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
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_DS_Waehlhebel_TestFailedChanged_DS_Waehlhebel_TestFailedChanged, # Added correct cal-variable from .a2l
        check_sig    = can_bus.DS_Waehlhebel__DS_Waehlhebel_TestFailedChanged__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'DS_Waehlhebel__DS_Waehlhebel_WIRChanged')
    testresult.append(["\nMessage/PDU: DS_Waehlhebel:DS_Waehlhebel_WIRChanged", ""]) 

    # #########################################################################
    # DS_Waehlhebel:DS_Waehlhebel_WIRChanged
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
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_DS_Waehlhebel_WIRChanged_DS_Waehlhebel_WIRChanged, # Added correct cal-variable from .a2l
        check_sig    = can_bus.DS_Waehlhebel__DS_Waehlhebel_WIRChanged__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'DS_Waehlhebel__DS_Waehlhebel_Subsystemaktiv')
    testresult.append(["\nMessage/PDU: DS_Waehlhebel:DS_Waehlhebel_Subsystemaktiv", ""]) 

    # #########################################################################
    # DS_Waehlhebel:DS_Waehlhebel_Subsystemaktiv
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: war_nicht_lokal_aktiv
    #   0x1: war_lokal_aktiv
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_DS_Waehlhebel_Subsystemaktiv_DS_Waehlhebel_Subsystemaktiv, # Added correct cal-variable from .a2l
        check_sig    = can_bus.DS_Waehlhebel__DS_Waehlhebel_Subsystemaktiv__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))
    
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
