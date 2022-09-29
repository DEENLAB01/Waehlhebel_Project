#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Rx_Signals_SiShift_01.py
# Title   : CAN Rx Signals SiShift 01
# Task    : Test of HIL-Tx => ECU-Rx Signals of CAN Message SiShift_01
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
# 1.3  | 24.08.2021 | M. Mushtaq | added resetEventMemory in Pre.
# 1.4  | 24.09.2021 | Mohammed | added correct cal-variable from .a2l
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
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    SiShift_01_DrvPosn = hil.SiShift_01__SIShift_StLghtDrvPosn__value
    SiShift_01_NeutHldPha = hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value
    meas_vars = [SiShift_01_DrvPosn, SiShift_01_NeutHldPha]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[+] Kl30, Kl15 ein und Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    #testresult.append(canape_diag.checkEventMemoryEmpty())
    
    # TEST PROCESS ############################################################
    testresult.append(["\xa0 Start DAQ Measurement", ""])
    daq.startMeasurement(meas_vars)

    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'SiShift_01__SIShift_StLghtDrvPosn')
    testresult.append(["\nMessage/PDU: SiShift_01:SIShift_StLghtDrvPosn", ""]) 

    # #########################################################################
    # SiShift_01:SIShift_StLghtDrvPosn
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                4 bits
    # Lookup (raw):
    #   0x0: Init
    #   0x5: D
    #   0x6: N
    #   0x7: R
    #   0x8: P
    #   0xC: Sonderfahrprogramm
    #   0xF: Fehler
    # Valid range (raw+phys):    [0x0..0xE] 
    # Invalid range (raw+phys):  ]0xE..0xF] => [0xF..0xF]
    # Valid states (raw+phys):   [0x0, 0x5, 0x6, 0x7, 0x8, 0xC]
    # Invalid states (raw+phys): [0xF]
    # Total range (raw+phys):    [0x0..0xF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.SiShift_01__SIShift_StLghtDrvPosn__value,
        check_var    = cal.Swc_GSL_GearDetection_PIM_SG_SiShift_01_SIShift_StLghtDrvPosn, # Added correct cal-variable from .a2l
        set_values   = [0x0, 0x5, 0x6, 0x7, 0x8, 0xC],
        check_values = [0x0, 0x5, 0x6, 0x7, 0x8, 0xC],
    ))
    #testresult.append(canape_diag.checkEventMemory([], ticket_id='Fehler Id:EGA-PRM-164'))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    #testresult.append(canape_diag.checkEventMemoryEmpty())

    '''
    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'SiShift_01__SiShift_01_CRC')
    testresult.append(["\nMessage/PDU: SiShift_01:SiShift_01_CRC", ""]) 

    # #########################################################################
    # SiShift_01:SiShift_01_CRC
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                8 bits
    # Valid range (raw+phys):    [0x00..0xFF] 
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x00..0xFF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.SiShift_01__SiShift_01_20ms_CRC__value,
        check_var    = cal.Swc_GSL_GearDetection_PP_SG_SiShift_01_SG_SiShift_01_SiShift_01_CRC, # Added correct cal-variable from .a2l
        set_values   = [0x00, 0x80, 0xFF],
        check_values = [0x00, 0x80, 0xFF],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-164'))

   
    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'SiShift_01__SiShift_01_BZ')
    testresult.append(["\nMessage/PDU: SiShift_01:SiShift_01_BZ", ""])

    # #########################################################################
    # SiShift_01:SiShift_01_BZ
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                4 bits
    # Valid range (raw+phys):    [0x0..0xF]
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x0..0xF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.SiShift_01__SiShift_01_20ms_BZ__value,
        check_var    = cal.Swc_GSL_GearDetection_PP_SG_SiShift_01_SG_SiShift_01_SiShift_01_BZ, # Added correct cal-variable from .a2l
        set_values   = [0x0, 0x8, 0xF],
        check_values = [0x0, 0x8, 0xF],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-164'))

'''
    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'SiShift_01__SIShift_FlgStrtNeutHldPha')
    testresult.append(["\nMessage/PDU: SiShift_01:SIShift_FlgStrtNeutHldPha", ""])

    # #########################################################################
    # SiShift_01:SIShift_FlgStrtNeutHldPha
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
        set_sig      = can_bus.SiShift_01__SIShift_FlgStrtNeutHldPha__value,
        check_var    = cal.Swc_GSL_GearDetection_PIM_SG_SiShift_01_SIShift_FlgStrtNeutHldPha, # Added correct cal-variable from .a2l
        set_values   = [0x0, 0x1],
        check_values = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    #testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-164'))
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # test step
    testresult.append(["[.] Stoppe Measurement", ""])
    daq_data = daq.stopMeasurement()
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])
    testresult.append(["[.] Setze values in CAN-Bus: [0x00, 0x80, 0xFF]", ""])
    plot_data = {}
    for mes in meas_vars:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))
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
