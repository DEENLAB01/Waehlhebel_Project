#******************************************************************************
# -*- coding: latin1 -*-
# File    : eval_signal_test.py
# Title   : EvalSignal Example
# Task    : Evaluating DAQ data with EvalSignal example
#
# Author  : J.Tremmel
# Date    : 02.07.2015
# Copyright 2015 - 2018 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 02.07.2015 | Tremmel  | initial    
# 1.1  | 03.07.2015 | Tremmel  | expanded example, added plot output
# 1.2  | 10.05.2016 | Tremmel  | added some TC-IDs
# 1.3  | 01.12.2017 | Tremmel  | seek() returns the associated data value since
#                              | TTk 2.0.0, check vs. None to see if seek failed
# 1.4  | 07.11.2018 | Tremmel  | use a static seed for analog "noise",
#                              | switched example from pylab to pyplot
#******************************************************************************
from _automation_wrapper_ import TestEnv
testenv = TestEnv()

import os
import random

from matplotlib import pyplot 
# older matplotlib versions:
# import pylab as pyplot # figure/show/close functions work the same

from ttk_daq.eval_signal import EvalSignal
from ttk_checks import basic_tests
from ttk_base.values_base import meta


# #############################################################################
def debugPlot(daq_data, title="data", output_path=None):
    """ Simple plotting of signals using matplotlib (for debug purposes).
        IF output_path was not specified, this will block until displayed plot 
        window gets closed.
        
        Parameters:
            daq_data    - data acquisition data structure containing data to display
            title       - title for plot/figure
            output_path - if specified, the plotted data will be stored to this 
                          path (and interactive plot display will not get shown)
    """
    fig = pyplot.figure(figsize=(12, 6)) 
    subplot = fig.add_subplot(111, title=title, xlabel="time [s]", ylabel="values")
    for sig_label, sig_data in sorted(daq_data.iteritems()):
        alias = getattr(sig_label, "alias", "%s"%(sig_label)) 
        subplot.plot(sig_data["time"], sig_data["data"], label=alias) # , marker="x"
        
    subplot.grid(True)
    subplot.legend()
    
    
    # pyplot.show()/pylab.show() opens a modal control, so it does not work that well 
    # during automatic tests (but it may be nice during debugging)
    if output_path:
        fig.savefig(output_path, bbox_inches="tight", dpi=90)
        # Note that in a "real life" test script, generated plot images should 
        # probably not be opened automatically as this delays test execution 
        # and might consume quite a bit of processing resources, depending on 
        # the associated image viewer
        os.startfile(os.path.normpath(output_path))
    else:
        print "Showing debug plot..."
        pyplot.show()
    
    
    # release figure memory (might not work as well in older pylab releases)
    fig.clear()
    pyplot.close() 
    
    
try:
    # #########################################################################
    testenv.setup()    
    # #########################################################################
    testresult = testenv.getResults()
    
    # not needed in this offline-example:
    # hil = testenv.getHil()
    # testenv.startupECU()
    
    
    # #########################################################################
    # create some sample data
    # #########################################################################
    
    # time axis: 2s duration in 1ms steps 
    timestamps = [0.001 * t for t in range(2000)]
    
    # signal change 0 => 1 after 500ms, stay 1 until end of measurement
    source_data = [0.0] * 500 + [1.0] * 1500
    
    # signal change 0 => 1 after 800ms, 1 => 5 200ms later, stay 5 until end of measurement
    target_data = [0.0] * 800 + [1.0] * 200 + [5.0] * 1000
    
    # signal change: ramp from 0 .. 30 between 850ms and 1250ms, then stay at 30 
    analog_data = [0.0] * 850 + [0.1 * x for x in range(300)] 
    analog_data += [analog_data[-1]] * (2000 - 300 - 850)
    
    # since it is supposed to be an analog signal: add some "noise"
    # (use a static seed so result values can be more easily compared)
    random.seed(1234) 
    analog_data = [max(0.0, round(random.gauss(x, 0.01), 3)) for x in analog_data]
    
    assert len(timestamps) == len(source_data) == len(target_data) == len(analog_data)
    
    # Use identifiers with some additional meta info for nicer output
    #
    # Normal "variables" (CalVar, HilVar, ...) will also have attached meta 
    # info and use their "identifier" as representation
    source = meta("source", alias="source (switch)",     
                  lookup={0: "off", 1: "on"})
    target = meta("target", alias="target (pump control state)", 
                  lookup={0: "off", 1: "active", 5: "minimum pressure reached"})
    analog = meta("analog", alias="analog (pressure value)", unit="bar")
     
    daq_data = {
        source: {'data': source_data, 'time': timestamps},
        target: {'data': target_data, 'time': timestamps},
        analog: {'data': analog_data, 'time': timestamps},
    }
    
    
    print "# " * 60
    print "# Demo Data:"
    for sig, sig_data in sorted(daq_data.iteritems()):
        for entry, data in sorted(sig_data.iteritems()):
            print sig, 
            print "%s: %s"%(entry, ", ".join(["%4s"%(v) for v in data[:4] + ["..."] + data[-4:]]))
        print "# " + "-" * 58
    print "# " * 60
    
    
    
    # #########################################################################
    # plot sample data
    # #########################################################################
    
    plot_file_path = os.path.splitext(testenv.getResultsFilePath())[0] + ".png"
    
    if "SingleTestManual" in plot_file_path:
        # rather "hacky": run standalone, not as part of test series
        # => show interactive, modal plot
        debugPlot(daq_data, "source data")
    
    
    info = (
        # some additional explanations
        '"source": a switch state output,\n'
        '"target": a status value that reacts to "source" switch, '
                  'e.g. a pump motor control status\n'
        '"analog": an analog sensor value, e.g. a pressure rising '
                  'when "target" motor is running.'
    )
    
    debugPlot(daq_data, "example data", plot_file_path)
    
    # add a result with plotted image
    testresult.append([
        "Example Data for EvalSignal Demo", 
        info,
        "[[IMG]]" + str(plot_file_path), # add image to result entry
        "INFO"
    ])
    
    
    # #########################################################################
    # evaluate data
    # #########################################################################
    
    # prepare EvalSignal objects for all our signals
    source_sig = EvalSignal(daq_data[source])
    target_sig = EvalSignal(daq_data[target])
    analog_sig = EvalSignal(daq_data[analog])
    
    # #########################################################################
    # Check change in input / source signal  
    testresult.setTestcaseId("EVALSIG-01")
    testresult.append(["\nDetermining input/source signal change", ""])
    
    # find timestamp of first "0" status (should be initial state, but we 
    # cannot assume this with captured data, e.g. source could be stuck at 1)
    source_initial_ts = source_sig.findNext("==", 0) # default tolerance is 0.001
    
    # find following status change to "1"
    source_status_1_ts = source_sig.findNext("==", 1)
    
    verdict = "FAILED"
    if source_initial_ts is None:
        # if our detection of the initial status failed 
        # (no 0 found in captured data)
        descr = "Initial state 0 not found in source signal data"
        
    elif source_status_1_ts is None:
        # if timestamp is None, findNext did not find the specified value
        descr = "No state change from 0 => 1 found in source signal data"
        
    else:
        # found both states 0 and 1.
        # Realistically, we could also check if there are any other states 
        # between 0 and 1 (but lets treat this signal as a 1 bit switch)
        descr = "Source signal changed to 1 at %.3fs"%(source_status_1_ts)
        verdict = "PASSED"
    
    testresult.append([descr, verdict])
    
    
    # #########################################################################
    # Check change in target signal (that "reacts" to the source signal change)
    testresult.setTestcaseId("EVALSIG-02")
    testresult.append(["\nDetermining target signal change", ""])
    # move to time where source signal changes to 1
    target_sig.seek(source_status_1_ts)

    testresult.append(
        basic_tests.checkStatus(
            target_sig.getValue(), 0,
            descr="Target signal is inactive when source signal switches to 1"
        )
    )
    # find first occurrence of status 1
    target_status_1_ts = target_sig.findNext("==", 1)
    # find first occurrence of status 5    
    target_status_5_ts = target_sig.findNext("==", 5)
    
    target_status_5_until_end = (
        target_status_5_ts is not None and   # found status 5
        target_sig.findNext("!=", 5) is None # no other status until end of data
    )
    
    # Check that there is no other status between 1 and 5
    target_sig.setEvalRange(target_status_1_ts, target_status_5_ts)
    target_sig.seekEnd()
    # in this eval range: last entry should be the first status "5", 
    #                     all others before should be "1"s
    unexpected_target_states = target_sig.findPrev("!=", 1) is not None # default tolerance is still 0.001
    target_sig.clearAll() # best practice: clear evalRange when done with it (and current position) 
    
    verdict = "FAILED"
    if target_status_1_ts is None:
        descr = "No state change from 0 => 1 found in target signal data"
    elif target_status_5_ts is None:
        descr = (
            "Target signal changed to 1 at %.3fs, but no change to 5 "
            "found in target signal data"%(target_status_1_ts)
        )
    else:
        descr = "Target signal changed to 1 at %.3fs and to 5 at %.3fs"%(
            target_status_1_ts, target_status_5_ts
        )
        if not unexpected_target_states:
            descr += "\nNo invalid states detected between status 1 and 5"
            verdict = "PASSED"
        else:
            descr += "\n> Invalid states detected between status 1 and 5"
            
    testresult.append([descr, verdict])
    
    
    # ... or we could check delta time between status 1 and 5
    if None in (target_status_1_ts, target_status_5_ts) or unexpected_target_states:
        testresult.append(["Target signal did not contain a valid status change", "FAILED"])
    else:
        delta_ms = (target_status_5_ts - target_status_1_ts) * 1000
        testresult.append(
            basic_tests.checkTolerance(
                meta(delta_ms, unit="ms"),
                200, 
                abs_pos=5.0,
                descr="Delta time between status 1 and 5"
            )
        )
    
    # Another typical case: check delta time between changes in separate signals
    #
    # Real-world examples include reaction time checks, e.g.  
    #    error injection => error reaction
    # or signal propagation checks, e.g. 
    #    change on a bus signal => change to associated data element in DUT's SW
    #
    if None in (source_status_1_ts, target_status_1_ts):
        # Best practice: 
        #    Always include a consistency check and provide a sensible failure 
        #    description. This will greatly simplify debugging if problems turn 
        #    up later during regressions test.
        testresult.append([
            "Inconsistent data:\n"
            "Unable to evaluate delta time between source and target signal change", 
            "FAILED"
        ])
    else:
        delta_ms = (target_status_1_ts - source_status_1_ts) * 1000
        testresult.append(
            basic_tests.checkTolerance(
                meta(delta_ms, unit="ms", alias="delta time"),
                meta(300, unit="ms"), 
                abs_pos=5, 
                descr="Delta time between status change 0=>1 in source signal "
                      "and status change 0=>1 in target signal"
            )
        )
    
    # #########################################################################
    # Check change in analog signal (e.g. assume a pressure rising as reaction 
    # to target signal's switch to status 1)
    testresult.setTestcaseId("EVALSIG-03")
    testresult.append(["\nDetermining analog signal change", ""])
    analog_sig.seekStart() # should initially be at start of data, but anyway
    
    value = analog_sig.getData()
    testresult.append(
        basic_tests.checkTolerance(
            meta(value, unit=analog.unit),
            0,
            abs_pos=0.2,
            descr="Analog signal should start at 0"
        )
    )
    
    if analog_sig.seek(target_status_1_ts) is not None:
        value = analog_sig.getData()
        testresult.append(
            basic_tests.checkTolerance(
                meta(value, unit=analog.unit),
                0,
                abs_pos=0.2,
                descr="Analog signal should (still) be at 0 at point of activation"
            )
        )   
    else:
        testresult.append([
            "Failed to find target signal's activation point", 
            "FAILED"
        ])
    
    
    # Check time when analog signal has reached 20 "bar"
    desired_value = 20 
    reached_desired_value_ts = analog_sig.findNext(">=", desired_value)
     
    if reached_desired_value_ts is None:
        testresult.append([
            "Failed to reach desired analog value %.1f"%(desired_value), 
            "FAILED"
        ])
    
    else:
        delta_ms = (reached_desired_value_ts - target_status_1_ts) * 1000
        testresult.append(
            basic_tests.compare(
                meta(delta_ms, unit="ms", alias="time until desired value reached"),
                "<",
                meta(300, "ms", alias="upper boundary"),
                descr="Desired analog value should be reached before 300 ms have passed."
            )
        )
    
    # Check for value of target_signal, assuming in this example that target_sig 
    # should be at status 5 once the analog_sig has reached 20 "bar" 
    # (e.g. an internal status like "pressure is now high enough")
    if reached_desired_value_ts is None:
        # Best practice: 
        #     Keep number of test steps identical in all branches.
        #     Provide a sensible failure message
        testresult.append([
            "Unable to check target signal status "
            "(desired analog value not reached)", 
            "FAILED"
        ])
    else:
        target_sig.seek(reached_desired_value_ts)
        # Note that if, for some reason, target_sig cannot seek timestamp
        # reached_desired_value_ts, checkStatus will deal with the invalid 
        # data type (None if timestamp is invalid so no value exists for it) 
        # and enter an ERROR verdict
        testresult.append(
            basic_tests.checkStatus(
                target_sig.getValue(), 5,
                descr="Target signal should be in state 5 if analog signal "
                      "has reached %.1f [%s]"%(desired_value, analog.unit)
            )
        )
        
    
    # cleanup #################################################################
    testresult.clearTestcaseId()
    # hil = None # no HIL access used in this example
    
finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################
    
print "Done."
