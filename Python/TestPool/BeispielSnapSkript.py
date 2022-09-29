# ******************************************************************************
# -*- coding: latin1 -*-
# File    : BeispielSnapSkript.py
# Title   : Gamma V Capture Example
# Task    : Gamma V "Capture" example
#
# Author  : M. Abdul Karim
# Date    : 29.03.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name     | Description
# ------------------------------------------------------------------------------
# 1.0  | 29.03.2021 | Abdul Karim  | initial

# ******************************************************************************
import os
import time
from ttk_daq import daq_utils
from ttk_daq import matfile  # @UnresolvedImport (pyc'd)
import plot_utils
from _automation_wrapper_ import TestEnv

testenv = TestEnv()
try:
    # #########################################################################
    testenv.setup()
    # #########################################################################
    testresult = testenv.getResults()
    hil = testenv.getHil()

    testenv.startupECU()
    hil.cl15_on__.set(0)
   # hil.motor_temp.set(20.21)  # just to get some non-zero values to "capture"

    measurement_lead_in_s = 0.5
    measurement_lead_out_s = 0.5

    measurement_duration_s = 2.0 + measurement_lead_in_s + measurement_lead_out_s

    capture_vars = [hil.vbat_cl30__V, hil.current_cl30__A, hil.supply_sense__, hil.cl15_on__]
    capture = testenv.gamma.Capture(capture_vars)
    capture.SetFrame(
        1,  # downsampling
        0,  # delay [s]
        int(measurement_duration_s)  # duration [s]
    )

    print "Capturing...",
    # measurement/capture
    capture.StartCapturing()

    # it is a good idea to wait a little after measurement has started to
    # get a few samples with initial data
    time.sleep(measurement_lead_in_s)

    # do stuff here...
    # (note that offline mode does not support dynamic data changes during
    #  capture, so "captured" data will not change)
    hil.vbat_cl30__V.set(15.0)
    time.sleep(1)
    print ".",

    hil.vbat_cl30__V.set(13.0)
    time.sleep(1)
    print ".",

    # a little lead-out delay
    time.sleep(measurement_lead_out_s)

    # #########################################################################
    # Get and save measurement data
    # #########################################################################
    # It is not necessary to wait until capture is done. As our measurement is
    # finished, we can just get all data captured so far.
    # Capture would be "done" once the remaining measurement buffer has been
    # filled.
    hil_data = capture.Fetch()

    print "...data captured."

    # transform capture data to our generic data acquisition data structure
    # (dict with {<label>: { "time": [0.0, 0.1, ...], "data": [1, 2, ...] }}
    daq_data = daq_utils.getDaqDataStruct(hil_data)

    # store plot to results folder (and base name on single test results name)
    plot_file_path = os.path.splitext(testenv.getResultsFilePath())[0] + ".png"

    plot_utils.plotSignals(
        daq_data, capture_vars, plot_file_path, title="Some Captured Data"
    )
    print "Data plotted to %s" % (plot_file_path)

    # add a result with plotted image
    testresult.append([
        "A result entry with a plotted figure",
        "[[IMG]] %s" % (plot_file_path),  # add image to result entry
        "INFO"
    ])

    # We might also want to store the "raw" measurement data, e.g. to a mat file
    # (Note that matlab import/export currently uses utility functions from
    #  dSPACE installation, so this will not work properly unless a dSPACE
    #  Release with Python test automation libs is installed)
    mat_file_path = os.path.splitext(testenv.getResultsFilePath())[0] + ".mat"
    matfile.exportToMat(daq_data, capture_vars, mat_file_path)

    # just for demo purposes: display figure/image with its associated program
    os.startfile(os.path.normpath(plot_file_path))
    # (this should normally not be included in "live" test scripts)

    # cleanup #################################################################
    hil = None


finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=True)
    # #########################################################################

print "Done."
