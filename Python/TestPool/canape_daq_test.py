# ******************************************************************************
# -*- coding: utf-8 -*-
# -*- coding: latin1 -*-
# File    : canape_daq_test.py
# Title   : CANape Data Acquisition Example
# Task    : Data acquisition with Vector CANape example
#
# Author  : J.Tremmel
# Date    : 10.05.2016
# Copyright 2016 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name     | Description
# ------------------------------------------------------------------------------
# 1.0  | 10.05.2016 | Tremmel  | initial
# 1.2  | 31.05.2016 | Tremmel  | moved plot function to module plot_utils
# ******************************************************************************
from _automation_wrapper_ import TestEnv

testenv = TestEnv()
import os
import time
import matplotlib
#import plot_utils

try:
    # #########################################################################
    testenv.setup()
    # #########################################################################
    testresult = testenv.getResults()
    hil = testenv.getHil()

    testenv.startupECU()

    cal = testenv.getCal()
    daq = testenv.getCanapeDAQ()

    Swc_GSL_IOHardwareAbstraction = 0.5
    Swc_GSL_IOHardwareAbstraction = 0.5

    # just to get somewhat sensible values
    #cal.emotor_n_ist.set(10)
    #cal.speicherdruck.set(1.2)

    meas_vars = [
        # <variable/identifier>, <measurement task>, <device index>
        [cal.Swc_GSL_IOHardwareAbstraction, "10ms", 0],
        [cal.Swc_GSL_IOHardwareAbstraction, "10ms", 0],
        ["GE_Oiltemp", "CAN", 1]
    ]

    daq.setup(meas_vars)

    print "Data Acquisition...",
    # start measurement/recorder
    daq.start()

    # it is a good idea to wait a little after measurement has started to
    # get a few samples with initial data
    #time.sleep(measurement_lead_in_s)

    # do stuff here...
    # (note that offline mode does not support dynamic data changes during
    #  capture, so "captured" data will not change)
    #hil.motor_temp.set(24.0)
    time.sleep(1)
    print ".",

    #hil.motor_temp.set(18.0)
    time.sleep(1)
    print ".",

    # a little lead-out delay
    #time.sleep(measurement_lead_out_s)

    daq.stop()

    # #########################################################################
    # Get and save measurement data
    # #########################################################################
    # Note: Writing/processing of MDF data may take some additional time after
    #       data acquisition has been stopped (since CANape 12)
    #       Trying to getData (which reads data from the stored MDF file) might
    #       report errors ("unsorted data" or some undocumented error number).
    #       Waiting a bit before reading data will solve this issue.
    #       Setting extra_delay_before_mdf_read to a DataAquisition instance
    #       (usually right in getCanapeDAQ()) in can add an additional wait
    #       time for all acquisitions
    daq.extra_delay_before_mdf_read = 1.0  # [s]

    daq_data = daq.getData()

    print "...data acquired."

    # store plot to results folder (and base name on single test results name)
    plot_file_path = os.path.splitext(testenv.getResultsFilePath())[0] + ".png"

    var_names = [element[0] for element in meas_vars]  # just get identifiers
    matplotlib.plotSignals(
        daq_data, var_names, plot_file_path, title="Some DAQ Data"
    )
    print "Data plotted to %s" % (plot_file_path)

    # add a result with plotted image
    testresult.append([
        "A result entry with a plotted figure",
        "[[IMG]] %s" % (plot_file_path),  # add image to result entry
        "INFO"
    ])

    # just for demo purposes: display figure/image with its associated program
    os.startfile(os.path.normpath(plot_file_path))

    # cleanup #################################################################
    hil = None
    daq = None
    cal = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=True)
    # #########################################################################

print "Done."
