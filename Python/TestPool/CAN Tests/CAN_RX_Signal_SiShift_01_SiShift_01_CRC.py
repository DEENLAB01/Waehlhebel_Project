# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_RX_Signal_SiShift_01_SiShift_01_CRC.py
# Title   : CAN Rx Signals SiShift 01 CRC
# Task    : Test of HIL-Tx => ECU-Rx Signals of CAN Message SiShift_01_CRC
#
# Author  : Mohammed Abdul Karim
# Date    : 15.02.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 15.02.2022 | Mohammed | initial

# ******************************************************************************
from _automation_wrapper_ import TestEnv

testenv = TestEnv()
# Imports #####################################################################
from simplified_bus_tests import testRxSigSeq, setTestcaseId

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("CAN_125")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    testenv.startupECU()  # startup before cal vars are called
    cal = testenv.getCal()
    can_bus = testenv.getCanBus()
    canape_diag = testenv.getCanapeDiagnostic()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    SiShift_01_CRC = hil.SiShift_01__SiShift_01_20ms_CRC__value
    meas_vars = [SiShift_01_CRC]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[+] Kl30, Kl15 ein und Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # TEST PROCESS ############################################################
    testresult.append(["\xa0 Start DAQ Measurement", ""])
    daq.startMeasurement(meas_vars)

    # #########################################################################
    # SiShift_01:SiShift_01_CRC
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                8 bits
    # Valid range (raw+phys):    [0x00..0xFF]
    # Invalid range (raw+phys):  n/a
    # Total range (raw+phys):    [0x00..0xFF]
    testresult.append(testRxSigSeq(
        set_sig=can_bus.SiShift_01__SiShift_01_20ms_CRC__value,
        check_var=cal.Swc_GSL_GearDetection_PIM_SG_SiShift_01_SiShift_01_CRC,
        # Added correct cal-variable from .a2l
        set_values=[0x00, 0x80, 0xFF],
        check_values=[0x00, 0x80, 0xFF],
    ))

    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    #testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step
    testresult.append(["[.] Stoppe Measurement", ""])
    daq_data = daq.stopMeasurement()
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])
    testresult.append(["[.] Setze values in CAN-Bus: [0x00, 0x80, 0xFF]", ""])
    plot_data = {}
    for mes in meas_vars:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))

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
