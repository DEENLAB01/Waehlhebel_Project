#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Rx_Signals_ClampControl_01.py
# Title   : CAN Rx Signals ClampControl 01
# Task    : Test of HIL-Tx => ECU-Rx Signals of CAN Message ClampControl_01
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
# 1.4  | 24.09.2021 | Mohammed   | added correct cal-variable from .a2l
# 1.5  | 14.02.2022 | Mohammed   | added DAQ Measurement
#******************************************************************************
from _automation_wrapper_ import TestEnv
testenv = TestEnv()
# Imports #####################################################################
from simplified_bus_tests import testRxSigSeq, setTestcaseId
import time
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
    KST_KL_15 = hil.ClampControl_01__KST_KL_15__value
    meas_vars = [KST_KL_15]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[+] Kl30, Kl15 ein und Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    
    # TEST PROCESS ############################################################
    testresult.append(["\xa0 Start DAQ Measurement", ""])
    daq.startMeasurement(meas_vars)

    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'ClampControl_01__KST_KL_15')
    testresult.append(["\nMessage/PDU: ClampControl_01:KST_KL_15", ""]) 

    # #########################################################################
    # ClampControl_01:KST_KL_15
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: aus
    #   0x1: ein
    # Valid range (raw+phys):    [0x0..0x1] 
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.ClampControl_01__KST_KL_15__value,
        check_var    = cal.Swc_GSL_GearProcessing_Run_GP_Main10ms_RP_GSL_KST_KL_15_KST_KL_15, # Added correct cal-variable from .a2l
        set_values   = [0x0, 0x1],
        check_values = [0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-152'))

    # test step
    testresult.append(["[.] Stoppe Measurement", ""])
    daq_data = daq.stopMeasurement()
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])
    testresult.append(["[.] Setze values in CAN-Bus: [0x0, 0x1]", ""])

    plot_data = {}
    for mes in [KST_KL_15]:
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
