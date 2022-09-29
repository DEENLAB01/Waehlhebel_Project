#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_Rx_Signals_VDSO_05.py
# Title   : CAN Rx Signals VDSO 05
# Task    : Test of HIL-Tx => ECU-Rx Signals of CAN Message VDSO_05
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
# 1.5  | 14.02.2022 | Mohammed   | added DAQ Measurement
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
    VDSO_Vx3d = hil.VDSO_05__VDSO_Vx3d__value
    meas_vars = [VDSO_Vx3d]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[+] Kl30, Kl15 ein und Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    #testresult.append(canape_diag.checkEventMemoryEmpty())
    
    # TEST PROCESS ############################################################
    testresult.append(["\xa0 Start DAQ Measurement", ""])
    daq.startMeasurement(meas_vars)

    # set Testcase ID #########################################################
    setTestcaseId(testresult, 'VDSO_05__VDSO_Vx3d')
    testresult.append(["\nMessage/PDU: VDSO_05:VDSO_Vx3d", ""]) 

    # #########################################################################
    # VDSO_05:VDSO_Vx3d
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                16 bits
    # Lookup (raw):
    #   0xFFFE: Init
    #   0xFFFF: Fehler
    # Valid range (raw+phys):    [0x0000..0xFFFD] 
    # Invalid range (raw+phys):  ]0xFFFD..0xFFFF] => [0xFFFE..0xFFFF]
    # Invalid states (raw+phys): [0xFFFE, 0xFFFF]
    # Total range (raw+phys):    [0x0000..0xFFFF]
    testresult.append(testRxSigSeq(
        set_sig      = can_bus.VDSO_05__VDSO_Vx3d__value,
        check_var    = cal.Swc_GSL_Diag_RP_VDSO_Vx3d_VDSO_Vx3d, # Added correct cal-variable from .a2l
        set_values   = [0x0000, 0x7FFF, 0xFFFD], # 0x7FFF, 0xFFFD
        check_values = [0x0000, 0x7FFF, 0xFFFD], # 0x7FFF, 0xFFFD
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-151'))

    # test step
    testresult.append(["[.] Stoppe Measurement", ""])
    daq_data = daq.stopMeasurement()
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])

    plot_data = {}
    for mes in [VDSO_Vx3d]:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))

    # clear any currently used test case id ###################################
    testresult.clearTestcaseId()
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
