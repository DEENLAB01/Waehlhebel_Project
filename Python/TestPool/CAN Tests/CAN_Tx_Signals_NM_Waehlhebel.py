#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Tx_Signals_NM_Waehlhebel.py
# Title   : CAN Tx Signals NM Waehlhebel
# Task    : Test of ECU-Tx => HIL-Rx Signals of CAN Message NM_Waehlhebel
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
# 1.3  | 02.09.2021 | Mohammed | added correct cal-variable from .a2l
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

    '''
    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'NM_Waehlhebel__NM_Waehlhebel_FCAB')
    testresult.append(["\nMessage/PDU: NM_Waehlhebel:NM_Waehlhebel_FCAB", ""]) 

    # #########################################################################
    # NM_Waehlhebel:NM_Waehlhebel_FCAB
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                56 bits
    # Lookup (raw):
    #   0x00000000000000: Init
    #   0x00000000000001: 01_CarWakeUp
    #   0x00000000000002: 02_Basefunction_Powertrain
    #   0x00000000000004: 03_Basefunction_Chassis
    #   0x00000000000008: 04_Basefunction_DrivingAssistance
    #   0x00000000000010: 05_Basefunction_Infotainment
    #   0x00000000000020: 06_Basefunction_ComfortLight
    #   0x00000000000040: 07_Basefunction_CrossSection
    #   0x00000000000080: 08_Basefunction_Connectivity
    #   0x00000000000100: 09_<reserved>
    #   0x00000000000200: 10_Powertrain
    #   0x00000000000400: 11_Chassis
    #   0x00000000000800: 12_GearSelector
    #   0x00000000001000: 13_Airbag
    #   0x00000000002000: 14_InfotainmentExtensions
    #   0x00000000004000: 15_InstrumentclusterDisplay
    #   0x00000000008000: 16_InfotainmentDisplay
    #   0x00000000010000: 17_Audio
    #   0x00000000020000: 18_VirtualSideMirrors
    #   0x00000000040000: 19_Doors_Hatches
    #   0x00000000080000: 20_OptionalComfort
    #   0x00000000100000: 21_AirSuspension
    #   0x00000000200000: 22_ExteriorLights
    #   0x00000000400000: 23_Climate
    #   0x00000000800000: 24_ThermoManagement
    #   0x00000001000000: 25_AccessSystemSensors
    #   0x00000002000000: 26_HighVoltage_Charging
    #   0x00000004000000: 27_Timemaster_Timer
    #   0x00000008000000: 28_OnboardTester_DataCollector
    #   0x00000010000000: 29_SteeringColumnLock
    #   0x00000020000000: 30_EnergyManagement
    #   0x00000040000000: 31_MultifunctionalSteeringWheel
    #   0x00000080000000: 32_OnlineAccess
    #   0x00000100000000: 33_ExternalWirelessCommunication
    #   0x00000200000000: 34_GPS_Localization
    #   0x00000400000000: 35_ExteriorSound
    #   0x00000800000000: 36_Preheater
    #   0x00001000000000: 37_HighVoltage_WirelessChargingStation
    #   0x00008000000000: 40_Diagnosis_Energy
    #   0x00010000000000: 41_Diagnosis_Powertrain
    #   0x00020000000000: 42_Diagnosis_FlexRay
    #   0x00040000000000: 43_Diagnosis_DrivingAssistance
    #   0x00080000000000: 44_Diagnosis_Infotainment
    #   0x00100000000000: 45_Diagnosis_Comfort
    #   0x00200000000000: 46_Diagnosis_Light
    #   0x00400000000000: 47_Diagnosis_ComfortLINs
    #   0x00800000000000: 48_Diagnosis_ClimateTmeLINs
    #   0x01000000000000: 49_<reserved>
    #   0x10000000000000: 53_Lock_Unlock
    #   0x20000000000000: 54_<reserved>
    #   0x40000000000000: 55_Dimming
    #   0x80000000000000: 56_ChargingStatus
    # Valid range (raw+phys):    [0x00000000000000..0xFFFFFFFFFFFFFF] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x00000000000000, 0x00000000000001, 0x00000000000002, 0x00000000000004, 0x00000000000008, 0x00000000000010, 0x00000000000020, 0x00000000000040, 0x00000000000080, 0x00000000000100, 0x00000000000200, 0x00000000000400, 0x00000000000800, 0x00000000001000, 0x00000000002000, 0x00000000004000, 0x00000000008000, 0x00000000010000, 0x00000000020000, 0x00000000040000, 0x00000000080000, 0x00000000100000, 0x00000000200000, 0x00000000400000, 0x00000000800000, 0x00000001000000, 0x00000002000000, 0x00000004000000, 0x00000008000000, 0x00000010000000, 0x00000020000000, 0x00000040000000, 0x00000080000000, 0x00000100000000, 0x00000200000000, 0x00000400000000, 0x00000800000000, 0x00001000000000, 0x00008000000000, 0x00010000000000, 0x00020000000000, 0x00040000000000, 0x00080000000000, 0x00100000000000, 0x00200000000000, 0x00400000000000, 0x00800000000000, 0x01000000000000, 0x10000000000000, 0x20000000000000, 0x40000000000000, 0x80000000000000]
    # Total range (raw+phys):    [0x00000000000000..0xFFFFFFFFFFFFFF]
    testresult.append(testTxSigSeq(
        set_var      = cal.NM_Waehlhebel__NM_Waehlhebel_FCAB, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.NM_Waehlhebel__NM_Waehlhebel_FCAB__value,
        set_values   = [0x00000000000000, 0x00000000000001, 0x00000000000002, 0x00000000000004, 0x00000000000008, 0x00000000000010, 0x00000000000020, 0x00000000000040, 0x00000000000080, 0x00000000000100, 0x00000000000200, 0x00000000000400, 0x00000000000800, 0x00000000001000, 0x00000000002000, 0x00000000004000, 0x00000000008000, 0x00000000010000, 0x00000000020000, 0x00000000040000, 0x00000000080000, 0x00000000100000, 0x00000000200000, 0x00000000400000, 0x00000000800000, 0x00000001000000, 0x00000002000000, 0x00000004000000, 0x00000008000000, 0x00000010000000, 0x00000020000000, 0x00000040000000, 0x00000080000000, 0x00000100000000, 0x00000200000000, 0x00000400000000, 0x00000800000000, 0x00001000000000, 0x00008000000000, 0x00010000000000, 0x00020000000000, 0x00040000000000, 0x00080000000000, 0x00100000000000, 0x00200000000000, 0x00400000000000, 0x00800000000000, 0x01000000000000, 0x10000000000000, 0x20000000000000, 0x40000000000000, 0x80000000000000],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())
    '''
    '''
    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'NM_Waehlhebel__NM_Waehlhebel_UDS_CC')
    testresult.append(["\nMessage/PDU: NM_Waehlhebel:NM_Waehlhebel_UDS_CC", ""]) 

    # #########################################################################
    # NM_Waehlhebel:NM_Waehlhebel_UDS_CC
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: Inaktiv
    #   0x1: CC_aktiv
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    
    testresult.append(testTxSigSeq(
        set_var      = cal.NM_Waehlhebel__NM_Waehlhebel_UDS_CC, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())
    '''

    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen')
    testresult.append(["\nMessage/PDU: NM_Waehlhebel:NM_Aktiv_N_Haltephase_abgelaufen", ""]) 

    # #########################################################################
    # NM_Waehlhebel:NM_Aktiv_N_Haltephase_abgelaufen
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: Inaktiv
    #   0x1: Aktiv
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
  
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_GearProcessing_Run_GP_Main10ms_PP_NM_Aktiv_N_Haltephase_abgelaufen_NM_Aktiv_N_Haltephase_abgelaufen,
        check_sig    = can_bus.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))

    '''
    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'NM_Waehlhebel__NM_Waehlhebel_NM_State')
    testresult.append(["\nMessage/PDU: NM_Waehlhebel:NM_Waehlhebel_NM_State", ""]) 

    # #########################################################################
    # NM_Waehlhebel:NM_Waehlhebel_NM_State
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                6 bits
    # Lookup (raw):
    #   0x00: Init
    #   0x01: NM_RM_aus_BSM
    #   0x02: NM_RM_aus_PBSM
    #   0x04: NM_NO_aus_RM
    #   0x08: NM_NO_aus_RS
    #   0x10: reserved
    #   0x20: reserved
    # Valid range (raw+phys):    [0x00..0x3F] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20]
    # Total range (raw+phys):    [0x00..0x3F]
     
    testresult.append(testTxSigSeq(
        set_var      = cal.NM_Waehlhebel__NM_Waehlhebel_NM_State, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.NM_Waehlhebel__NM_Waehlhebel_NM_State__value,
        set_values   = [0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    '''
    '''
    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'NM_Waehlhebel__NM_Waehlhebel_SNI_10')
    testresult.append(["\nMessage/PDU: NM_Waehlhebel:NM_Waehlhebel_SNI_10", ""]) 

    # #########################################################################
    # NM_Waehlhebel:NM_Waehlhebel_SNI_10
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                10 bits
    # Lookup (raw):
    #   0x053: Waehlhebel_SNI
    # Valid range (raw+phys):    [0x000..0x3FF] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x053]
    # Total range (raw+phys):    [0x000..0x3FF]
    testresult.append(testTxSigSeq(
        set_var      = cal.NM_Waehlhebel__NM_Waehlhebel_SNI_10, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.NM_Waehlhebel__NM_Waehlhebel_SNI_10__value,
        set_values   = [0x000, 0x053, 0x200, 0x3FF],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    '''
    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin')
    testresult.append(["\nMessage/PDU: NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Tmin", ""]) 

    # #########################################################################
    # NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Tmin
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: Inaktiv
    #   0x1: Mindestaktivzeit
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_GearProcessing_Run_GP_Main10ms_PP_NM_Waehlhebel_NM_aktiv_Tmin_NM_Waehlhebel_NM_aktiv_Tmin, # Added correct cal-variable from .a2l
        check_sig    = can_bus.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value,
        #check_sig= hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12')
    testresult.append(["\nMessage/PDU: NM_Waehlhebel:NM_Waehlhebel_Wakeup_V12", ""]) 

    # #########################################################################
    # NM_Waehlhebel:NM_Waehlhebel_Wakeup_V12
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                8 bits
    # Lookup (raw):
    #   0x00: Peripherie_Wakeup_Ursache_nicht_bekannt
    #   0x01: Bus_Wakeup
    #   0x02: KL15_HW
    #   0x80: N_Haltephase_abgelaufen
    # Valid range (raw+phys):    [0x00..0xFF] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x00, 0x01, 0x02, 0x80]
    # Total range (raw+phys):    [0x00..0xFF]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_GearProcessing_Run_GP_Main10ms_PP_NM_Waehlhebel_Wakeup_V12_NM_Waehlhebel_Wakeup_V12, # Added correct cal-variable from .a2l
        check_sig    = can_bus.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value,
        set_values   = [0x00, 0x01, 0x02, 0x80],
    ))

    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15')
    testresult.append(["\nMessage/PDU: NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15", ""]) 

    # #########################################################################
    # NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: Inaktiv
    #   0x1: KL15_EIN
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_GearProcessing_Run_GP_Main10ms_PP_NM_Waehlhebel_NM_aktiv_KL15_NM_Waehlhebel_NM_aktiv_KL15, # Added correct cal-variable from .a2l
        check_sig    = can_bus.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value,
        set_values   = [0x0, 0x1],
    ))

    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))

    '''
    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'NM_Waehlhebel__NM_Waehlhebel_CBV_CRI')
    testresult.append(["\nMessage/PDU: NM_Waehlhebel:NM_Waehlhebel_CBV_CRI", ""]) 

    # #########################################################################
    # NM_Waehlhebel:NM_Waehlhebel_CBV_CRI
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: NM_ohne_Clusteranforderungen
    #   0x1: NM_mit_Clusteranforderungen
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testTxSigSeq(
        set_var      = cal.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    '''
    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'NM_Waehlhebel__NM_Waehlhebel_CBV_AWB')
    testresult.append(["\nMessage/PDU: NM_Waehlhebel:NM_Waehlhebel_CBV_AWB", ""]) 

    # #########################################################################
    # NM_Waehlhebel:NM_Waehlhebel_CBV_AWB
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: Passiver_WakeUp
    #   0x1: Aktiver_WakeUp
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_GearProcessing_Run_GP_Main10ms_PP_NM_Waehlhebel_CBV_AWB_NM_Waehlhebel_CBV_AWB, # Added correct cal-variable from .a2l
        check_sig    = can_bus.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value,
        set_values   = [0x0, 0x1],
    ))

    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-2'))


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag')
    testresult.append(["\nMessage/PDU: NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", ""]) 

    # #########################################################################
    # NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: Inaktiv
    #   0x1: Diagnose_aktiv
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testTxSigSeq(
        set_var      = cal.Swc_GSL_GearProcessing_PP_NM_Waehlhebel_NM_aktiv_Diag_NM_Waehlhebel_NM_aktiv_Diag, # Added correct cal-variable from .a2l
        check_sig    = can_bus.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
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
