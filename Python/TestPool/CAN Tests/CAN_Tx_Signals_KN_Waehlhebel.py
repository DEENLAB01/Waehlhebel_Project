#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Tx_Signals_KN_Waehlhebel.py
# Title   : CAN Tx Signals KN Waehlhebel
# Task    : Test of ECU-Tx => HIL-Rx Signals of CAN Message KN_Waehlhebel
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
    setTestcaseId(testresult, 'KN_Waehlhebel__Waehlhebel_Abschaltstufe')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:Waehlhebel_Abschaltstufe", ""]) 

    # #########################################################################
    # KN_Waehlhebel:Waehlhebel_Abschaltstufe
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: keine_Einschraenkung
    #   0x1: Funktionseinschraenkung
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testTxSigSeq(
        set_var      = cal.KN_Waehlhebel__Waehlhebel_Abschaltstufe, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__Waehlhebel_Abschaltstufe__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'KN_Waehlhebel__KN_Waehlhebel_BusKnockOut')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:KN_Waehlhebel_BusKnockOut", ""]) 

    # #########################################################################
    # KN_Waehlhebel:KN_Waehlhebel_BusKnockOut
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                2 bits
    # Lookup (raw):
    #   0x0: Funktion_nicht_ausgeloest
    #   0x1: Veto_aktiv
    #   0x2: Funktion_ausgeloest
    #   0x3: Funktion_deaktiviert
    # Valid range (raw+phys):    [0x0..0x3] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1, 0x2, 0x3]
    # Total range (raw+phys):    [0x0..0x3]
    testresult.append(testTxSigSeq(
        set_var      = cal.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value,
        set_values   = [0x0, 0x1, 0x2, 0x3],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer", ""]) 

    # #########################################################################
    # KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                6 bits
    # Lookup (raw):
    #   0x3F: ECUKnockOut_deaktiviert
    # Valid range (raw+phys):    [0x00..0x3E] 
    # Invalid range (raw+phys):  ]0x3E..0x3F] => [0x3F..0x3F]
    # Invalid states (raw+phys): [0x3F]
    # Total range (raw+phys):    [0x00..0x3F]
    testresult.append(testTxSigSeq(
        set_var      = cal.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value,
        set_values   = [0x00, 0x1F, 0x3E],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'KN_Waehlhebel__Waehlhebel_KD_Fehler')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:Waehlhebel_KD_Fehler", ""]) 

    # #########################################################################
    # KN_Waehlhebel:Waehlhebel_KD_Fehler
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: Kein KD_Fehler
    #   0x1: KD_Fehler
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testTxSigSeq(
        set_var      = cal.KN_Waehlhebel__Waehlhebel_KD_Fehler, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__Waehlhebel_KD_Fehler__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut", ""]) 

    # #########################################################################
    # KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                2 bits
    # Lookup (raw):
    #   0x0: Funktion_nicht_ausgeloest
    #   0x1: Veto_war_aktiv
    #   0x2: Funktion_ausgeloest
    #   0x3: Funktion_deaktiviert
    # Valid range (raw+phys):    [0x0..0x3] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1, 0x2, 0x3]
    # Total range (raw+phys):    [0x0..0x3]
    testresult.append(testTxSigSeq(
        set_var      = cal.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value,
        set_values   = [0x0, 0x1, 0x2, 0x3],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'KN_Waehlhebel__NM_Waehlhebel_FCIB')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:NM_Waehlhebel_FCIB", ""]) 

    # #########################################################################
    # KN_Waehlhebel:NM_Waehlhebel_FCIB
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                56 bits
    # Lookup (raw):
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
    #   0x00010000000801: InitValueFCIB
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
    # Valid states (raw+phys):   [0x00000000000001, 0x00000000000002, 0x00000000000004, 0x00000000000008, 0x00000000000010, 0x00000000000020, 0x00000000000040, 0x00000000000080, 0x00000000000100, 0x00000000000200, 0x00000000000400, 0x00000000000800, 0x00000000001000, 0x00000000002000, 0x00000000004000, 0x00000000008000, 0x00000000010000, 0x00000000020000, 0x00000000040000, 0x00000000080000, 0x00000000100000, 0x00000000200000, 0x00000000400000, 0x00000000800000, 0x00000001000000, 0x00000002000000, 0x00000004000000, 0x00000008000000, 0x00000010000000, 0x00000020000000, 0x00000040000000, 0x00000080000000, 0x00000100000000, 0x00000200000000, 0x00000400000000, 0x00000800000000, 0x00001000000000, 0x00008000000000, 0x00010000000000, 0x00010000000801, 0x00020000000000, 0x00040000000000, 0x00080000000000, 0x00100000000000, 0x00200000000000, 0x00400000000000, 0x00800000000000, 0x01000000000000, 0x10000000000000, 0x20000000000000, 0x40000000000000, 0x80000000000000]
    # Total range (raw+phys):    [0x00000000000000..0xFFFFFFFFFFFFFF]
    testresult.append(testTxSigSeq(
        set_var      = cal.KN_Waehlhebel__NM_Waehlhebel_FCIB, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__NM_Waehlhebel_FCIB__value,
        set_values   = [0x00000000000001, 0x00000000000002, 0x00000000000004, 0x00000000000008, 0x00000000000010, 0x00000000000020, 0x00000000000040, 0x00000000000080, 0x00000000000100, 0x00000000000200, 0x00000000000400, 0x00000000000800, 0x00000000001000, 0x00000000002000, 0x00000000004000, 0x00000000008000, 0x00000000010000, 0x00000000020000, 0x00000000040000, 0x00000000080000, 0x00000000100000, 0x00000000200000, 0x00000000400000, 0x00000000800000, 0x00000001000000, 0x00000002000000, 0x00000004000000, 0x00000008000000, 0x00000010000000, 0x00000020000000, 0x00000040000000, 0x00000080000000, 0x00000100000000, 0x00000200000000, 0x00000400000000, 0x00000800000000, 0x00001000000000, 0x00008000000000, 0x00010000000000, 0x00010000000801, 0x00020000000000, 0x00040000000000, 0x00080000000000, 0x00100000000000, 0x00200000000000, 0x00400000000000, 0x00800000000000, 0x01000000000000, 0x10000000000000, 0x20000000000000, 0x40000000000000, 0x80000000000000],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'KN_Waehlhebel__Waehlhebel_SNI_10')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:Waehlhebel_SNI_10", ""]) 

    # #########################################################################
    # KN_Waehlhebel:Waehlhebel_SNI_10
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                10 bits
    # Valid range (raw+phys):    [0x000..0x3FF] 
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x000..0x3FF]
    testresult.append(testTxSigSeq(
        set_var      = cal.KN_Waehlhebel__Waehlhebel_SNI_10, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__Waehlhebel_SNI_10__value,
        set_values   = [0x000, 0x200, 0x3FF],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'KN_Waehlhebel__NM_Waehlhebel_Subsystemaktiv')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:NM_Waehlhebel_Subsystemaktiv", ""]) 

    # #########################################################################
    # KN_Waehlhebel:NM_Waehlhebel_Subsystemaktiv
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
        set_var      = cal.KN_Waehlhebel__NM_Waehlhebel_Subsystemaktiv, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__NM_Waehlhebel_Subsystemaktiv__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'KN_Waehlhebel__Waehlhebel_Transport_Mode')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:Waehlhebel_Transport_Mode", ""]) 

    # #########################################################################
    # KN_Waehlhebel:Waehlhebel_Transport_Mode
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: keine_Einschraenkung
    #   0x1: Funktionseinschraenkung
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testTxSigSeq(
        set_var      = cal.KN_Waehlhebel__Waehlhebel_Transport_Mode, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__Waehlhebel_Transport_Mode__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'KN_Waehlhebel__NM_Waehlhebel_Lokalaktiv')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:NM_Waehlhebel_Lokalaktiv", ""]) 

    # #########################################################################
    # KN_Waehlhebel:NM_Waehlhebel_Lokalaktiv
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
        set_var      = cal.KN_Waehlhebel__NM_Waehlhebel_Lokalaktiv, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__NM_Waehlhebel_Lokalaktiv__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'KN_Waehlhebel__Waehlhebel_KompSchutz')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:Waehlhebel_KompSchutz", ""]) 

    # #########################################################################
    # KN_Waehlhebel:Waehlhebel_KompSchutz
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
        set_var      = cal.KN_Waehlhebel__Waehlhebel_KompSchutz, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__Waehlhebel_KompSchutz__value,
        set_values   = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'KN_Waehlhebel__Waehlhebel_Nachlauftyp')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:Waehlhebel_Nachlauftyp", ""]) 

    # #########################################################################
    # KN_Waehlhebel:Waehlhebel_Nachlauftyp
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                4 bits
    # Lookup (raw):
    #   0x0: Komm_bei_KL15_EIN
    #   0x1: Komm_nach_KL15_AUS
    #   0x2: Komm_bei_KL15_AUS
    # Valid range (raw+phys):    [0x0..0xF] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1, 0x2]
    # Total range (raw+phys):    [0x0..0xF]
    testresult.append(testTxSigSeq(
        set_var      = cal.KN_Waehlhebel__Waehlhebel_Nachlauftyp, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__Waehlhebel_Nachlauftyp__value,
        set_values   = [0x0, 0x1, 0x2],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer", ""]) 

    # #########################################################################
    # KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                8 bits
    # Lookup (raw):
    #   0xFF: BusKnockOut_deaktiviert
    # Valid range (raw+phys):    [0x00..0xFE] 
    # Invalid range (raw+phys):  ]0xFE..0xFF] => [0xFF..0xFF]
    # Invalid states (raw+phys): [0xFF]
    # Total range (raw+phys):    [0x00..0xFF]
    testresult.append(testTxSigSeq(
        set_var      = cal.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value,
        set_values   = [0x00, 0x7F, 0xFE],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())


    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'KN_Waehlhebel__KN_Waehlhebel_DiagPfad_V12')
    testresult.append(["\nMessage/PDU: KN_Waehlhebel:KN_Waehlhebel_DiagPfad_V12", ""]) 

    # #########################################################################
    # KN_Waehlhebel:KN_Waehlhebel_DiagPfad_V12
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: Aktiv
    #   0x1: inaktiv
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testTxSigSeq(
        set_var      = cal.KN_Waehlhebel__KN_Waehlhebel_DiagPfad_V12, # TODO: Add correct cal-variable from .a2l
        check_sig    = can_bus.KN_Waehlhebel__KN_Waehlhebel_DiagPfad_V12__value,
        set_values   = [0x0, 0x1],
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
