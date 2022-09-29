#******************************************************************************
# -*- coding: latin-1 -*-
# File    : data_sync.py
# Package : ttk_daq
# Task    : Examples/utilities for daq data synchronization. 
#           
#           As synchronization requirements vary with available HW and SW 
#           features, the provided functions are intended as a starting point 
#           for developing individual sync functions suitable for specific 
#           project needs.
# 
# Python  : 2.5+
#
# Copyright 2011 - 2020 iSyst GmbH
#******************************************************************************
# Rev. | Date       | Name    | Description
#------------------------------------------------------------------------------
# 1.0  | 17.10.2011 | Tremmel | initial
# 1.1  | 11.11.2011 | Tremmel | added twoStepSynch
# 1.9  | 19.02.2013 | Tremmel | added getToggleEdgeNearestSync to twoStepSync()
#                             | which might give better sync results
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2.0  | 13.02.2015 | Tremmel | refactored from daq_utils
# 2.1  | 31.08.2017 | Tremmel | updated synchronize example with code from TTk
#                             | advanced training (now supports interpolation)
# 2.2  | 24.06.2020 | Tremmel | added basic usage example to __main__
#******************************************************************************
"""
@package ttk_daq.data_sync
Examples/utilities for daq data synchronization. 

Note:
    As synchronization requirements vary with available HW and SW features, 
    the provided functions are intended as a starting point for developing 
    individual sync functions suitable for specific project needs.
    
"""

# FIXME: sync functions are pre-EvalSignal and might be simplified by changing
#        search code to use EvalSignal instances. 
# TODO:  nomenclature consistency: cal_data is called daq_data in refactored 
#        modules (but cal_data might be clearer here)


# #############################################################################
def synchronize(hil_data, hil_sync_signal, hil_sync_value,
                cal_data, cal_sync_signal, cal_sync_value,
                interpolate = True,
                offset = 0,
                ):
    """ Synchronize CANape measurements and dSpace capture data.
        
        Parameters:
            hil_data        - capture data structure as provided by
                              capture.Fetch() (on single processor systems)
            hil_sync_signal - name of sync signal in hil_data
            hil_sync_value  - sync edge found if value first time >= this value
            
            cal_data        - measurement data structure as provided by
                              DataAcquisition.getData() (compare mdflib.readMdf())  
            cal_sync_signal - name of sync signal in cal_data
            cal_sync_value  - sync edge found if value first time >= this value
            
            interpolate     - True: interpolate time of sync edge between the 
                                    first matching and the previous data point 
                                    (might be helpful for analog values and 
                                     slower measurements)  
                              False: use timestamp of first match
            
            offset          - additional time axis offset [s] hil vs. cal.  
                              Set to a positive value to offset processing 
                              and/or filter time in ECU (e.g. 2.5ms delay due to 
                              low pass filter on ADC input plus 5ms cycle time
                              of ADC read task)
        
        Note: Current limitations:
           * capture data of multi-processor systems not yet supported
             in this example (they use a modified data structure)
        
        Example:
            # given RTP capture data in `hil_data` and CANape daq data in `daq_data`
            # as well als `hil` and `cal` variable containers:
            synchronize(
                # hil capture
                hil_data        = hil_data, 
                hil_sync_signal = hil.vbat, 
                hil_sync_value  = 11.5, 
                
                # daq measurement
                cal_data        = daq_data, 
                cal_sync_signal = cal.adc_vbat, 
                cal_sync_value  = 11.5, 
                
                interpolate     = True,
                # 5ms offset to compensate e.g. for input filters and (worst-case) task timing
                offset          = 0.005 
            )
            # merge synchronized data
            synched = {}
            synched.update(daq_data)
            synched.update(daq_utils.getDaqDataStruct(hil_data))
            
            # trim off excess data points to get a cleaner area if you want to create a plot 
            daq_utils.trimDaqData(synched)
            
        
        Returns True if synchronization was successful, otherwise False.  
        Time axis of `hil_data` will be modified and synch'ed to the axis of
        `cal_data`.
    """
    print("Synchronizing time axis...")
    # for this measurement:
    # o all cal values are recorded in the same task, so the time axis
    #   of all cal/ccp signals will be identical (the can sync signal
    #   will have its own time axis, though it will be in sync with the
    #   ccp signals)
    #   
    # o all hil values are recorded in the main model task, so they
    #   have the same time axis
    
    cal_time_axis = cal_data[cal_sync_signal].get("time", [])
    hil_time_axis = hil_data["xAxis"] # capture data contains only one time axis
    
    # Note that time axis of cal signals are just referenced, so if we 
    # change one axis, we will change the axis of all connected signals.
    # In measurement data, the time axis of can and cal (ccp/xcp) signals
    # are synchronized (they use the same reference time base)
    
    # find sync edge timestamps:
    hil_sync_data = hil_data[hil_sync_signal]         # from capture data
    cal_sync_data = cal_data[cal_sync_signal]["data"] # from measurement/mdf data
    
    def getSyncEdgeTime(data_axis, time_axis, threshold, fallback=-1.0):
        """ closure; detect timestamp where data first reaches threshold value """
        sync_time = fallback
        for index in xrange(len(data_axis)):
            if data_axis[index] >= threshold:
                sync_time = time_axis[index]
                if interpolate and index > 0:
                    # linear interpolate between the data point that is 
                    # above the threshold value and its predecessor
                    delta_thresh = threshold        - data_axis[index - 1]
                    delta_data   = data_axis[index] - data_axis[index - 1]
                    delta_time   = time_axis[index] - time_axis[index - 1]
                    sync_time = delta_time / float(delta_data) * delta_thresh \
                              + time_axis[index - 1] 
                break
        return sync_time
        
    
    # seek sync edges
    sync_time_hil = getSyncEdgeTime(hil_sync_data, hil_time_axis, hil_sync_value)
    sync_time_cal = getSyncEdgeTime(cal_sync_data, cal_time_axis, cal_sync_value)
    
    print "# sync-time HIL: %.4f s"%(sync_time_hil)
    print "# sync-time CAL: %.4f s"%(sync_time_cal)
    
    if (sync_time_hil > 0 and sync_time_cal > 0):
        print "--> detected sync edges."
        delta = sync_time_cal - sync_time_hil
        print "   delta to hil time axis: %.1f ms"%(delta * 1000)
        if offset:
            delta -= offset 
            print "   including man. offset:  %.1f ms"%(delta * 1000)
            
        # modify capture time axis (for simplicity's sake)
        for index in xrange(len(hil_time_axis)):
            hil_time_axis[index] += delta
        print "--> time axis synchronized.\n"
        return True
    else:
        print "> failed to detect sync edges."
        print "Signals will remain unsynchronized.\n"
    return False
    

# #############################################################################
def twoStepSynch(hil_data, hil_sync_edge, hil_sync_toggle,
                 cal_data, cal_sync_edge, cal_sync_toggle,
                 toggle_dt=10):
    """ Synchronize CANape measurements and dSpace capture data.
        
        Note: Trigger sources:
            1. CAN message/signal sent from HIL to ECU, 
               measured on HIL and via CAN-Device in CANape
            2. HW-pin toggling every toggle_dt [ms],
               measured on HIL (digital in) and via its corresponding 
               status variable via XCP/CCP in CANape
        
        Parameters:
            hil_data        - capture data structure as provided by
                              capture.Fetch() (on single processor systems)
            hil_sync_edge   - name of (can rx) sync signal in hil_data
                              (set on HIL, captured from CAN-transceiver
                              in rtp)
            hil_sync_toggle - digital measurement of a hw pin that toggles
                              with a defined T
            
            cal_data        - measurement data structure as provided by
                              DataAcquisition.getData() 
            cal_sync_edge   - name of (can rx) sync signal in cal_data
                              (measured from a CAN-device in CANape)
            cal_sync_toggle - digital measurement of the source value for
                              a toggling pin measured with hil_sync_toggle
            
            toggle_dt       - [ms] toggle time for hw pin
        
        Note: Current limitations:
           * capture data must use only a single task for all signals
           * capture data of multi-processor systems not yet supported
             (they use a modified data structure)
           * sync signal should change 0 => >0 within measurement time
        
        Returns True if synchronization was successful, otherwise False.
        Time axis of hil_data will be modified and synched to the axis of
        cal_data.
    """
    print("Synchronizing time axis...")
    
    def getRisingToggleEdgeBeforeSync(sync_data, time_axis, edge_sync_time):
        """ Get a rising edge from sync data that is directly before
            the timestamp edge_sync_time.
            
            Seek the rising edge of the toggle signal that appears directly
            before the edge signal.
            As long as the transmission delay from hil-can => cal-can is
            shorter than 2 * toggle_dt, detection should work fine.
        """
        last_rising_edge_time = None
        last_state            = int(round(sync_data[0])) # initial state: initial value
        
        for index in range(len(sync_data)):
            # round value to avoid float issues from measurement data,
            # the sync signal should be digital, though
            curr_state = int(round(sync_data[index])) 
            curr_time  = time_axis[index]
            
            if last_state < curr_state:
                # edge detected
                last_rising_edge_time = time_axis[index]
            last_state = curr_state
            
            if curr_time >= edge_sync_time:
                # reached the sync edge, last_rising_edge_time
                # contains the time of the (toggle signal) edge
                # directly before the sync edge
                break
        else:
            # for some reason we did not reach the edge sync time
            print "> Failed to reach edge sync time while looking for "\
                  "secondary sync signal."
            return  None
        
        if last_rising_edge_time is None:
            print "> Failed to detect an edge while looking for "\
                  "secondary sync signal. "
            return  None
        
        delta = edge_sync_time - last_rising_edge_time
        if delta > 2 * toggle_dt:
            print "> Warning: Implausible delay between primary and secondary"\
                  " sync edges (%.4fs instead of < %.4fs)"%(
                      delta,
                      2 * toggle_dt
                  )
            # print "> Using time of primary sync edge as fallback."
            # # fallback to initial sync edge
            # last_rising_edge_time = edge_sync_time
            
        
        return last_rising_edge_time
    
    def getToggleEdgeNearestSync(sync_data, time_axis, edge_sync_time):
        """ Get a rising edge from sync data that is closest to the timestamp 
            edge_sync_time.
            
            As long as the transmission delay from hil-can => cal-can is
            shorter than 2 * toggle_dt, detection should work fine.
        """
        last_rising_edge_time = None
        current_rising_edge_time = None
        last_state            = int(round(sync_data[0])) # initial state: initial value
        
        edge_time_before = None
        edge_time_after  = None
        
        for index in range(len(sync_data)):
            # round value to avoid float issues from measurement data,
            # the sync signal should be digital, though
            curr_state = int(round(sync_data[index])) 
            curr_time  = time_axis[index]
            
            if last_state < curr_state:
                # rising edge detected
                current_rising_edge_time = curr_time
            last_state = curr_state
            
            
            if curr_time >= edge_sync_time:
                # by now we have reaced our primary sync time. The currently
                # detected edge might actually come _after_ edge_sync_time if
                # the sync_data time axis is coarse enough.
                # So:
                if edge_time_before is None:
                    # reached the sync edge, determine time of (toggle signal) 
                    # edge directly before the sync edge
                    
                    if current_rising_edge_time <= edge_sync_time:
                        # current_rising_edge_time might be before edge_sync_time
                        edge_time_before = current_rising_edge_time
                    
                    else:
                        # last_rising_edge_time has to be <= edge_sync_time
                        edge_time_before = last_rising_edge_time
                
                if (edge_time_before is not None and 
                    edge_time_before < current_rising_edge_time):
                    # found the next rising edge _after_ the edge_sync_time
                    edge_time_after = current_rising_edge_time
                    break
            
            last_rising_edge_time = current_rising_edge_time
        
        else:
            # for some reason we did not reach the edge sync time
            print("> Failed to reach edge sync time while looking for "
                  "secondary sync signal.")
            return  None
            
        
        if edge_time_before is None and edge_time_after is None:
            print("> Failed to detect sync edges while looking for "
                  "secondary sync signal. ")
            return None
        
        if edge_time_before is not None and edge_time_after is None:
            print("> Found only a sync edge right before the primary sync "
                  " edge (and no following edge)")
            return edge_time_before
            
        
        delta_before = abs(edge_time_before - edge_sync_time) * 1000 # [ms]
        delta_after  = abs(edge_sync_time - edge_time_after)  * 1000 # [ms] 
        print "-> edge before:   %5.3fs"%(edge_time_before)
        print "-> can sync edge: %5.3fs"%(edge_sync_time)
        print "-> edge after:    %5.3fs"%(edge_time_after)
        if (edge_time_before <= edge_sync_time < edge_time_after):
            print "  OK  -  order of detected edges valid  "
        else:
            print "  WARNING  -  detected edges in wrong order"
        
        if delta_before <= delta_after:
            print "--> leading toggle sync edge is closer (%.1fms vs. %.1fms)"%(
                delta_before, delta_after
            )
            closest_edge_time = edge_time_before
        else:
            print "--> trailing toggle sync edge is closer (%.1fms vs. %.1fms)"%(
                delta_after, delta_before
            )
            closest_edge_time = edge_time_after
        print "---> delta between leading and trailing edge: %.1fms"%(
            (edge_time_after - edge_time_before) * 1000
        )
        delta = abs(edge_sync_time - closest_edge_time)
        if delta > 2 * toggle_dt:
            print("> Warning: Implausible delay between primary and secondary"
                  " sync edges (%.4fs instead of <= %.4fs)"%(delta, 2 * toggle_dt))
        elif delta > toggle_dt:
            print("> Warning: high delay (above toggle delta) between primary "
                  " and secondary sync edges (%.4fs instead of <= %.4fs)"%(delta, toggle_dt))
        
        return closest_edge_time
        
    
    # for this measurement:
    # o all cal values are recorded in the same task, so the time axis
    #   of all cal/ccp signals will be identical (the can sync signal
    #   will have its own time axis, though it will be in sync with the
    #   ccp signals)
    #   
    # o all hil values are recorded in the main model task, so they
    #   have the same time axis
    
    can_time_axis = cal_data[cal_sync_edge].get("time", [])
    hil_time_axis = hil_data["xAxis"] # capture data contains only one time axis
    
    # Note that time axis of cal signals are just referenced, so if we 
    # change one axis, we will change the axis of all connected signals.
    # In measurement data, the time axis of can and cal (ccp/xcp) signals
    # are synchronized (they use the same reference time base)
    
    # find sync edge timestamps:
    hil_sync_data = hil_data[hil_sync_edge]            # from capture data
    can_sync_data = cal_data[cal_sync_edge]["data"]    # from measurement/mdf data
    
    
    # seek sync edges
    # FIXME: for now we've hardcoded a jump from 0 => something > 0
    #        maybe we better detect an actual change from the initial value?
    sync_time_hil = -1.0
    sync_time_can = -1.0
    for index in range(len(hil_sync_data)):
        if hil_sync_data[index] > 0:
            sync_time_hil = hil_time_axis[index]
            break
    
    for index in range(len(can_sync_data)):
        if can_sync_data[index] > 0:
            sync_time_can = can_time_axis[index]
            break
    
    print "  sync_time_hil: %.4f s"%(sync_time_hil)
    print "  sync_time_can: %.4f s"%(sync_time_can)
    
    
    if (sync_time_hil > 0 and sync_time_can > 0):
        
        edge_sync_time_hil = sync_time_hil
        edge_sync_time_can = sync_time_can
        
        print "-> found sync edges."
        delta1 = sync_time_can - sync_time_hil
        print "   delta to hil time axis: %.1f ms"%(delta1 * 1000)
        
        # secondary sync:
        # seek rising edge of toggling signal closest to the
        # respective devices' sync times
        # This should help to get a somewhat more precise sync time
        
        
        # As the edge of the can sync signal is transmitted from HIL to ECU,
        # the cal_sync_edge should appear with a short transmission delay
        # hil_sync_edge => cal_sync_edge
        
        
        # NOTE: We'll traverse over the whole measurement again to determine
        #       the correct "toggle signal edge", which is not terribly
        #       efficient, but spares us handling of a few edge cases
        # TODO: If this is really too slow, we'll have to rewrite it
        #       (seek index of sync_edge, go back 2 * toggle_dt, seek rising
        #        toggle edge...)
        
        print("getting sync time for hil measurements...")
        toggle_sync_time_hil = getToggleEdgeNearestSync(
            sync_data = hil_data[hil_sync_toggle],
            time_axis = hil_data["xAxis"],
            edge_sync_time = edge_sync_time_hil
        )
        print("getting sync time for cal measurements...")
        toggle_sync_time_cal = getToggleEdgeNearestSync(
            sync_data = cal_data[cal_sync_toggle]["data"],
            time_axis = cal_data[cal_sync_toggle]["time"],
            edge_sync_time = edge_sync_time_can
        )
        
        if (toggle_sync_time_hil is None or 
            toggle_sync_time_cal is None    ):
            print ">> secondary sync failed, no edge found",
            
            if toggle_sync_time_hil is None and toggle_sync_time_cal is None:
                print("in both HIL and CAL toggle sync signals.")
            elif toggle_sync_time_hil is None:
                print("in HIL toggle sync signal.")
            else:
                print("in CAL toggle sync signal.")
            
            print(">> using delta of primary sync")
            print("delta1: %.4fs (sync edge)"%(delta1))
            delta = delta1 # using primary sync delta
        
        else:
            print("-> secondary sync.")
            delta2 = toggle_sync_time_cal - toggle_sync_time_hil
            print "   refined delta to hil time axis: %.1f ms"%(delta2 * 1000)
            
            print "delta1: %.1fms (can sync edge)"%( delta1 * 1000)
            print "delta2: %.1fms (hw toggle edge)"%(delta2 * 1000)
            diff = abs(delta1 - delta2)
            print "-> delta difference: %.1fms"%(diff * 1000)
            
            delta = delta2
            if diff > 0.02:
                print "> Warning: High sync delays (using primary sync edge time instead)"
                delta = delta1
            elif diff > 0.01:
                print "> Note: rather high differences between primary and secondary sync." 
        
        # TODO: maybe use numpy vectors for easier numeric access
        # modify capture time axis (for simplicity's sake)
        for index in range(len(hil_time_axis)):
            hil_time_axis[index] = hil_time_axis[index] + delta
        #hil_data["xAxis_before_sync"] = hil_data["xAxis"] # debug 
        hil_data["xAxis"] = hil_time_axis
        print("Time axis synchronized.\n")
        return True
    else:
        print("> failed to detect synch edges. Signals will remain unsynchronized.\n")
    return False
    

# #############################################################################
# @cond DOXYGEN_IGNORE  
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    # See daq_sync_example.py in HIL-Demo-Project
    from copy import deepcopy
    from ttk_daq import daq_utils
    from ttk_daq._daq_utils import _printDataInfo
    
    capture_data_sc = { # single core, rtplib-capture structure
        "foo":      [0.00, 0.00, 0.00, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90], 
        # sync edge at index 3
        "hil_sync": [0.00, 0.02, 0.01, 1.10, 1.12, 1.09, 1.10, 1.11, 1.11, 1.10, 1.10, 1.10], 
        'xAxis':    [1.1 + 0.001 * t for t in range(12)]
    }
    daq_data = {
        "bar": {
            'data': [0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.4, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0, 0.0, 0.0, 0.0], 
            'time': [0.8 + 0.001 * t for t in range(16)]
        }, 
        "cal_sync": { # sync edge at index 5
            'data': [0.0, 0.1, 0.0, 0.0, 0.0, 5.1, 4.9, 5.0, 4.9, 5.0, 5.0, 5.1, 5.0, 5.0, 4.9, 5.0], 
            'time': [0.8 + 0.001 * t for t in range(16)]
        }, 
        "baz": { # synchronous to bar and sync, but uses a different time axis step size
            'data': [0.0, 0.0, 1.0, 0.0, 2.0, 0.0, 4.0, 0.0, 5.0], 
            'time': [0.8 + 0.002 * t for t in range(9)]
        },
    }
    
    
    unsynched = {}
    unsynched.update(deepcopy(daq_data))
    unsynched.update(daq_utils.getDaqDataStruct(deepcopy(capture_data_sc)))
    
    synchronize(
        # hil capture
        hil_data        = capture_data_sc, 
        hil_sync_signal = "hil_sync", 
        hil_sync_value  = 0.9, 
        
        # daq measurement
        cal_data        = daq_data, 
        cal_sync_signal = "cal_sync", 
        cal_sync_value  = 4.8, 
        
        interpolate     = True,
    )
    
    synched = {}
    synched.update(daq_data)
    synched.update(daq_utils.getDaqDataStruct(capture_data_sc))
    # let time axes start at 0
    synched = daq_utils.getNormalizedDaqData(synched)
    
    print("# Before: #########################################################")
    _printDataInfo(unsynched, outer_n=6)
    print("# After Sync: #####################################################")
    _printDataInfo(synched, outer_n=6)
    
    # sync edges: 4th entry of hil_sync 
    #             6th entry of cal_sync 
    # => both should now be at the same time value
    assert abs(round(synched["hil_sync"]["time"][3] - synched["cal_sync"]["time"][5], 3)) <= 0
    
    # and before they were quite different:
    assert abs(unsynched["hil_sync"]["time"][3] - unsynched["cal_sync"]["time"][5]) > 0.200
    
    
    print("Done.")

# @endcond DOXYGEN_IGNORE
# #############################################################################

