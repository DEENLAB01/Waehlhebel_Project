#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : xil_api_offline_stub.py
# Package : ttk_tools.dspace
# Task    : A dummy implementation of the default xil_api.py for debugging  
#           without available hardware or license keys.
# Type    : Interface
# Python  : 2.7 (but 2.5 compatible)
#
# Copyright 2016 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 15.04.2016 | J.Tremmel  | initial
# 1.1  | 15.04.2016 | J.Tremmel  | added sample code
# 1.2  | 26.04.2016 | J.Tremmel  | added stub info output during __init__
# 1.3  | 18.10.2016 | J.Tremmel  | moved shared error classes to xil_api_common
# 1.4  | 21.12.2016 | J.Tremmel  | split into interface and base implementation
# 1.5  | 28.09.2018 | J.Tremmel  | updated default task_name used for Capture 
# 1.6  | 17.10.2018 | J.Tremmel  | added import of stubbed TimeoutException
# 1.7  | 22.06.2020 | J.Tremmel  | updated sample code in __main__
#******************************************************************************
"""
@package ttk_tools.dspace.xil_api_offline_stub
Wrapper for a dummy/stub implementation of the default ttk_tools.dspace.xil_api 
for debugging without available hardware or license keys.

This serves as "interface" to the precompiled module in delivery to enable 
code-completion in PyDev.
"""
import _xil_api_offline_stub

# "enums" (to make them available w/o .NET/XIL libraries) # # # # # # # # # # #
# Note: those are normally imported from dSPACE's .NET implementation, 
#       here they are just stubbed equivalents
from _xil_api_offline_stub import DataType              # @UnusedImport
from _xil_api_offline_stub import InterpolationTypes    # @UnusedImport
from _xil_api_offline_stub import MAPortState           # @UnusedImport
from _xil_api_offline_stub import CaptureState          # @UnusedImport
from _xil_api_offline_stub import SignalGeneratorState  # @UnusedImport


# Exceptions # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# TTk Testbench Exceptions
# Hierarchy: 
# TTkException -> TestbenchError -> StimulusError
from xil_api_common import TestbenchError   # @UnusedImport
from xil_api_common import StimulusError    # @UnusedImport


# Exceptions from XIL-API Testbench layer (stubbed .NET exceptions).
# Normal, non-stubbed hierarchy: 
# Exception -> (.NET) System.Exception -> TestbenchPortException -> MAPortError
from _xil_api_offline_stub import DotNetException           # @UnusedImport
from _xil_api_offline_stub import TimeoutException          # @UnusedImport
from _xil_api_offline_stub import TestbenchPortException    # @UnusedImport
from _xil_api_offline_stub import MAPortError               # @UnusedImport


# utility function(s)
from xil_api_common import writeMAPortConfigXML         # @UnusedImport (just to make it available)


# #############################################################################
# Testbench
# #############################################################################
class XilTestbench(_xil_api_offline_stub.XilTestbench):
    """ XilTestbench access offline stub """
    ## vendor name for dSPACE's XIL testbench implementation. 
    # This should not really change (but neither should product name, which 
    # already changed between Releases 2014-B and 2015-A...)
    VENDOR_NAME = "dSPACE GmbH"
    
    # #########################################################################
    def __init__(self, 
                 config_file_path, 
                 force_config=False,
                 port_name="MAPort", 
                 product_name="XIL API", 
                 product_version="2017-B"):
        """ Setup a (stubbed) dSPACE XIL testbench along with a (stubbed) MAPort.
            
            Parameters:
                config_file_path - path to XML configuration file
                force_config     - if True, an already loaded application will 
                                   be replaced with the "new" configuration
                port_name        - name of MA Port (not really useful, though)
                product_name     - product name used in testbench factory
                product_version  - product version used in testbench factory.
                                   This usually matches the current release name.
        """
        
        
        ## [XIL-API] dSPACE-flavored testbench interface.
        # In a XilTestbench stub, this will only reference a minimal testbench 
        # stub containing members for VendorName, ProductName and ProductVersion.
        self.testbench = None 
        
        ## [XIL-API] model access port. 
        # In a XilTestbench stub, this will only reference a minimal MAPort
        # stub that reads/writes offline data (see ttk_tools.offline_data_provider) 
        self.ma_port = None
        
        _xil_api_offline_stub.XilTestbench.__init__(
            self, 
            config_file_path = config_file_path, 
            force_config     = force_config,
            port_name        = port_name, 
            product_name     = product_name, 
            product_version  = product_version
        )
    
    # #########################################################################
    def dispose(self):
        """ Dispose of resources allocated by this testbench instance.
            After this is called, the MAPort will no longer be available and
            further access will fail.
        """
        _xil_api_offline_stub.XilTestbench.dispose(self)
    
    # #########################################################################
    def read(self, model_path):
        """ Read a value from a variable.
            
            Parameters:
                model_path - path to variable, e.g. a Simulink-path
            
            Returns the current value of the variable
        """
        return _xil_api_offline_stub.XilTestbench.read(self, model_path)
        
    
    # #########################################################################
    def write(self, model_path, value):
        """ Write a value to a variable.
            
            Parameters:
                model_path - path to variable, e.g. a Simulink-path
                value      - value to write
            
            Returns the previous value before the write operation.
        """
        return _xil_api_offline_stub.XilTestbench.write(self, model_path, value)
    
    # #########################################################################
    def getCapture(self):
        """ Get a Capture instance configured to use this XilTestbench. """
        return _xil_api_offline_stub.XilTestbench.getCapture(self)
    
    # #########################################################################
    def getStimulus(self):
        """ Get a Stimulus instance configured to use this XilTestbench. """
        return _xil_api_offline_stub.XilTestbench.getStimulus(self)
        

# #############################################################################
# Capture / Data Acquisition
# #############################################################################
class Capture(_xil_api_offline_stub.Capture):
    """ Capture / Data Acquisition Offline Stub"""
    # #########################################################################
    def __init__(self, xil_testbench):
        """ Capture/DAQ stub.
            Parameters:
                xil_testbench - parent XilTestbench instance
        """
        ## reference to parent XilTestbench instance
        self.parent = xil_testbench
        
        ## reference to actual testbench api
        self.testbench = xil_testbench.testbench
        
        ## actual Capture instance, will be configured during setup()
        self.capture  = None
        
        ## list of variables / model_paths to capture 
        # (configured during setup())
        self.variables = []
        
        ## capture task name (configured during setup())
        self.task_name = u""
        
        ## file path to MDF-file in stream-to-disk mode 
        # (configured during setup())
        self.mdf_file_path = None
        
        _xil_api_offline_stub.Capture.__init__(self, xil_testbench)
        
    
    # #########################################################################
    def setup(self, variables, mdf_file_path=None, downsampling=None, 
              task_name="Periodic Task 1"):
        """ Setup data capture.
            
            Info: Task Name:
                Default capture/measurement task_name is 
                * "HostService" for PHS bus systems and 
                * "Periodic Task 1" for VEOS/SCALEXIO systems.
                
                See TRC file (`<model_name>.trc`) for available/configured tasks,
                e.g.  
                sampling_period[0]  
                {  
                    value:       0.001  
                    alias:       "HostService"  
                    increment:   0.001  
                    unit:        "s"  
                }  
            
            Parameters:
                variables     - list of variables/paths to capture
                mdf_file_path - path to MDF-file to use for stream-to-disk mode.  
                                None: keep captured data in memory.
                downsampling  - downsampling factor (1:n, one sample captured 
                                for every n capture cycles).  
                                Setting None uses the capture service's default 
                                setting (which should be 1:1).
                task_name     - name of capture task to use (see note)
            
        """
        _xil_api_offline_stub.Capture.setup(
            self, 
            variables      = variables, 
            mdf_file_path  = mdf_file_path, 
            downsampling   = downsampling, 
            task_name      = task_name
        )
    
    # #########################################################################
    def dispose(self):
        """ Dispose of resources allocated by this Capture instance.
            
            Note:
                After this has been called further access to capture data will 
                fail (... if not in the stub implementation).
        """
        _xil_api_offline_stub.Capture.dispose(self)
    
    # #########################################################################
    def start(self):
        """ Start capturing. 
            
            Note: stream-to-disk:
                start() will raise a (somewhat generic) `TestbenchPortException` 
                ("Could not start capturing.") if the configured MDF-file is 
                locked by another application.  
                The stub implementation will not really care about this, though.
        """
        _xil_api_offline_stub.Capture.start(self)
    
    # #########################################################################
    def stop(self):
        """ Stop capture process """
        _xil_api_offline_stub.Capture.stop(self)
    
    # #########################################################################
    def fetch(self):
        """ Fetch data while capture is running. Only works if data is written
            to memory (and specifically not in stream-to-disk mode).
            
            Only works in states `eACTIVATED`, `eRUNNING`, `eFINISHED` (and not 
            in `eCONFIGURED`, so it will not work once a capture has been stopped.)
            
            Returns data captured since the last call to fetch.
        """
        return _xil_api_offline_stub.Capture.fetch(self)
    
    # #########################################################################
    def getData(self, verbosity=1):
        """ Get a DAQ data structure containing the captured data 
            
            Example: DAQ data structure:
                daq_data = { 
                    "<signal name>": { 
                        "time": [ t1, t2, t3, ..., tn ], # timestamps
                        "data": [ d1, d2, d3, ..., dn ], # data points
                    }
                }
            
            Parameters:
                verbosity - 0: silent  
                            1: show MDF file info (only for stream-to-disk mode)
            
            Returns a dictionary with entries for each captured signal (see example)
        """
        return _xil_api_offline_stub.Capture.getData(self, verbosity)
        

# #############################################################################
# 
# #############################################################################
class StimulusSignalDescription(_xil_api_offline_stub.StimulusSignalDescription):
    """ Stub for signal value description for stimulus / signal generator.
        Describes signal value changes over time.
    """
    # #########################################################################
    def __init__(self, xil_testbench, name, model_path):
        """ Stimulus signal description stub.
            
            Parameters:
                xil_testbench - parent XilTestbench instance
                name          - `sig_descr` description name/label/alias
                model_path    - path to signal to be stimulated
            
        """
        ## reference to testbench api
        self.testbench   = None
        
        ## [XIL-API] SegmentSignalDescription.
        # A SegmentSignalDescription is used to define a signal waveform based 
        # on a chronologically ordered sequence of different segments. 
        self.sig_descr = None
        
        ## Model Path for this signal
        self.model_path = None
        
        _xil_api_offline_stub.StimulusSignalDescription.__init__(
            self, xil_testbench, name, model_path
        )
    
    # #########################################################################
    def addConstSegment(self, duration, value):
        """ Add a `ConstSegment`, a segment with, well, a constant value. 
            
            Info:
                f(t) = value
            
            Parameters:
                duration - duration of segment in [s]
                value    - `sig_descr` value/amplitude
        """
        _xil_api_offline_stub.StimulusSignalDescription.addConstSegment(
            self, duration, value
        )
    
    # #########################################################################
    def addRampSegment(self, duration, start_value, stop_value):
        """ Add a `RampSegment`, a segment with a linear ramp moving from start 
            to stop value during the specified time.
            
            Info:
                f(t) = (stop_value - start_value) / duration * t + start_value
            
            Parameters:
                duration    -  duration of segment in [s]
                start_value -  `sig_descr` value at beginning of ramp
                stop_value  -  `sig_descr` value at end of ramp
        """
        _xil_api_offline_stub.StimulusSignalDescription.addRampSegment(
            self, duration, start_value, stop_value
        )
    
    # #########################################################################
    def addIdleSegment(self, duration):
        """ Add an `IdleSegment`. This sets `sig_descr` generation into idle-mode 
            for the given  duration. During idle time, the `sig_descr` generator 
            will not write to the corresponding model variable.
            
            Parameters:
                duration - duration of segment in [s]
        """
        _xil_api_offline_stub.StimulusSignalDescription.addIdleSegment(
            self, duration
        )
    
    # #########################################################################
    def addNoiseSegment(self, duration, mean, sigma, seed=None):
        """ Add a `NoiseSegment`, a segment with noise having a Gaussian/normal 
            distribution.
            
            Parameters:
                duration - duration of segment in [s]
                mean     - mean value of Gaussian noise
                sigma    - standard deviation of amplitude against mean value 
                seed     - seed/start value for random number generator.  
                           None: uses current time (epoch) as seed value
        """
        _xil_api_offline_stub.StimulusSignalDescription.addNoiseSegment(
            self, duration, mean, sigma, seed
        )
    
    # #########################################################################
    def addRampSlopeSegment(self, duration, offset, slope):
        """ Add a `RampSlopeSegment`, a segment with a ramp according to a 
            linear equation.
            
            Info:
                f(t) = slope * t + offset
            
            Parameters:
                duration    -  duration of segment in [s]
                offset      -  offset value of ramp
                slope       -  slope of ramp
            
        """
        _xil_api_offline_stub.StimulusSignalDescription.addRampSlopeSegment(
            self, duration, offset, slope
        )
    
    # #########################################################################
    def addSineSegment(self, duration, offset, amplitude, period, phase=0):
        """ Add a `SineSegment`, a segment with a sine waveform.
            
            Parameters:
                duration    -  duration of segment in [s]
                offset      -  offset value of the sine waveform
                amplitude   -  amplitude of sine waveform,  
                               maximum value = offset + amplitude,  
                               minimum value = offset - amplitude
                period      -  cycle time of the sine waveform in [s]
                phase       -  initial phase shift as positive or negative 
                               factor of the period [-1.0 <= phase <= +1.0]  
                               e.g. 0.25 equals a 90° phase shift,  
                               -0.33 equals a -120° phase shift
            
        """
        _xil_api_offline_stub.StimulusSignalDescription.addSineSegment(
            self, duration, offset, amplitude, period, phase
        )
    
    # #########################################################################
    def addSawSegment(self, duration, offset, amplitude, period, phase=0, duty_cycle=0.5):
        """ Add a `SawSegment`, a segment of the `sig_descr` with a saw tooth 
            (or triangle) wave form.
            
            Parameters:
                duration    -  duration of segment in [s]
                offset      -  offset value of saw tooth waveform 
                amplitude   -  amplitude of saw tooth waveform  
                               maximum value = offset + amplitude,  
                               minimum value = offset 
                period      -  cycle time of the waveform in [s]
                phase       -  initial phase shift as positive or negative
                               factor of the period [-1.0 <= phase <= +1.0]  
                               e.g. 0.25 equals a 90° phase shift,  
                               -0.33 equals a -120° phase shift
                duty_cycle  -  ratio of raise time to period as a positive factor 
                               [0.0 <= duty_cycle <= 1.0], use factor 0.5 to 
                               get a triangle wave form.
            
        """
        _xil_api_offline_stub.StimulusSignalDescription.addSawSegment(
            self, duration, offset, amplitude, period, phase, duty_cycle
        )
        
    
    # #########################################################################
    def addPulseSegment(self, duration, offset, amplitude, period, phase=0, duty_cycle=0.5):
        """ Add a `PulseSegment`, a segment with periodic rectangular pulses 
            (that is, a PWM `sig_descr` with a fixed duty cycle).
            
            Parameters:
                duration    -  duration of segment in [s]
                offset      -  offset value of waveform 
                amplitude   -  amplitude of waveform,  
                               maximum value = offset + amplitude,  
                               minimum value = offset 
                period      -  cycle time of the waveform in [s]
                phase       -  initial phase shift as positive or negative 
                               factor of the period [-1.0 <= phase <= +1.0]  
                               e.g. 0.25 equals a 90° phase shift,  
                               -0.33 equals a -120° phase shift
                duty_cycle  -  ratio of high time to period as a positive factor 
                               [0.0 <= duty_cycle <= 1.0],  
                               DC 0.0: constant value (low @ offset)  
                               DC 0.5: symmetric rectangular `sig_descr`  
                               DC 1.0: constant value (high @ offset + amplitude)
            
        """
        _xil_api_offline_stub.StimulusSignalDescription.addPulseSegment(
            self, duration, offset, amplitude, period, phase, duty_cycle
        )
    
    # #########################################################################
    def addExpSegment(self, duration, start_value, stop_value, tau):
        """ Add an `ExpSegment`, a segment following an exponential curve.
            
            Info:
                f(t) = amplitude * (1 - e**(t/tau)) + offset  
                with  
                    offset    = start_value  
                    amplitude = stop_value - start_value  
            
            Parameters:
                duration    -  duration of segment in [s]
                start_value -  start value (offset of `sig_descr`)
                stop_value  -  stop value
                tau         -  time constant of exponential curve in [s]
            
        """
        _xil_api_offline_stub.StimulusSignalDescription.addExpSegment(
            self, duration, start_value, stop_value, tau
        )
    
    # #########################################################################
    def addSignalValueSegment(self, time_values, data_values, interpolation="backward"):
        """ Add a `SignalValueSegment`, a segment which directly uses numerical 
            data. The amplitude results from data points in numerical data and 
            the given interpolation type.  
            Duration of the segment is implicitly derived from the time vector.
            
            Note:
                Normally this segment is used to replay measured data.
            
            Info: Limitations:
                dSPACE XIL API Implementation Guide May 2015:  
                The `eFORWARD` and the `eLINEAR` interpolation types are not
                supported by the `SignalValueSegment` and the `DataFileSegment`.  
                All methods which access the InterpolationType property 
                implicitly use `eBACKWARD`. An exception is not thrown.
                
                The `SignalValueSegment` only supports values of `FloatVectorValue`
                data type.
            
            Parameters:
                time_values   - a list of time stamps
                data_values   - a list of data points
                interpolation - interpolation method:
                                * "backward": current data point will be used 
                                              until next data point (staircase backward) 
                                * "linear":   Linear interpolation between data points
                                * "forward":  next data point will be used immediately 
                                              (staircase forward)
        """
        _xil_api_offline_stub.StimulusSignalDescription.addSignalValueSegment(
            self, time_values, data_values, interpolation
        )
    
    # #########################################################################
    def addDataFileSegment(self, file_path, 
                           data_label, time_label=None,
                           start_time=None, duration=None,
                           interpolation="backward"):
        """ Add a `DataFileSegment`, a segment which uses numerical data stored 
            in a file. 
            
            The data file is typically a measurement data file which contains
            some measured signals and one or more time axes. The `DataFileSegment`
            holds a link to the data file and does not store or serialize the 
            used numerical data. 
            
            Info: Limitations:
                dSPACE XIL API Implementation Guide May 2015:  
                The `eFORWARD` and the `eLINEAR` interpolation types are not
                supported by the `SignalValueSegment` and the `DataFileSegment`. 
                All methods which access the `InterpolationType` property 
                implicitly use `eBACKWARD`. An exception is not thrown.
                
                If you use a `DataFileSegment`, only the following file formats
                are supported:
                * MAT file level 5
                * MDF 4.x
                
                To create a level 5 MAT file in MATLAB use -v6 as input 
                argument of MATLAB's save function. 
            
            Parameters:
                file_path     - path to data file in one of the supported formats
                data_label    - name/label of data vector/sig_descr to use 
                time_label    - name/label of time vector/raster to use 
                                (not needed for MDF files, leave as None)
                
                start_time    - start time stamp in [s]  
                                None: start at beginning of available data 
                duration      - maximum duration the segment in [s]  
                                None: run until end of file
                interpolation - interpolation method
                                * "backward": current data point will be used
                                              until next data point (staircase backward) 
                                * "linear":   Linear interpolation between data points
                                * "forward":  next data point will be used immediately 
                                              (staircase forward)
            
        """
        _xil_api_offline_stub.StimulusSignalDescription.addDataFileSegment(
            self, file_path, 
            data_label, time_label, 
            start_time, duration, 
            interpolation
        )
        

# #############################################################################
# 
# #############################################################################
class Stimulus(_xil_api_offline_stub.Stimulus):
    """ Offline stub for Stimulus / Signal Generator """
    
    # #########################################################################
    def __init__(self, xil_testbench, appl_name=None):
        """ Stimulus / Signal Generator stub.
            
            Parameters:
                xil_testbench - parent XilTestbench instance
                appl_name     - target application name for multi core systems
                                (e.g. "masterAppl"), None for single core setups.
            
        """
        ## reference to parent testbench
        self.parent   = xil_testbench
        
        ## reference to testbench api
        self.testbench = self.parent.testbench
        
        ## [XIL-API] SignalGenerator instance
        self.signal_generator = None
        
        _xil_api_offline_stub.Stimulus.__init__(self, xil_testbench, appl_name)
        
    
    # #########################################################################
    def loadStimulusFile(self, file_path, assignments=None):
        """ Load signal generator settings from an STI or STZ file.
            
            Note:
                The STI/STZ file might not contain signal mappings, 
                so signals may still have to be assigned manually.
            
            Note:
                If you add signal descriptions via addSignalDescription(), 
                they will replace/overwrite the loaded stimulus.
            
            Parameters:
                file_path   - path to STI/STZ file
                assignments - optional dictionary with <name>: <signal path> 
                              assignments.
            
        """
        _xil_api_offline_stub.Stimulus.loadStimulusFile(
            self, file_path, assignments
        )
    
    # ########################################################################
    def addSignalDescription(self, stim_sig_descr):
        """ Add a `StimulusSignalDescription` instance to this Stimulus. 
            
            Parameters:
                stim_sig_descr - StimulusSignalDescription instance to add
            
        """
        _xil_api_offline_stub.Stimulus.addSignalDescription(
            self, stim_sig_descr
        )
    
    # #########################################################################
    def loadToTarget(self):
        """ Load stimulus to target application """
        _xil_api_offline_stub.Stimulus.loadToTarget(self)
    
    # #########################################################################
    def destroyOnTarget(self):
        """ Destroy (well, unload) a currently loaded stimulus on/from target 
            application.
        """
        _xil_api_offline_stub.Stimulus.destroyOnTarget(self)
    
    # #########################################################################
    def start(self):
        """ Start a loaded stimulus. """
        _xil_api_offline_stub.Stimulus.start(self)
    
    # #########################################################################
    def pause(self):
        """ Pause a running stimulus. """
        _xil_api_offline_stub.Stimulus.pause(self)
    
    # #########################################################################
    def stop(self):
        """ Stop a running (or paused) stimulus. """
        _xil_api_offline_stub.Stimulus.stop(self)
    
    # #########################################################################
    def getState(self, verbosity=1):
        """ Get a numeric representation of the current stimulus state.
            
            Parameters:
                verbosity - 0: silent,  
                            1: print current state as info to log console
            
            Returns a numeric value. See `SignalGeneratorState` enum.
        """
        return _xil_api_offline_stub.Stimulus.getState(self, verbosity)
    
    # #########################################################################
    def getStateText(self, state=None):
        """ Get a string description for a numeric stimulus state.
            
            Parameters:
                state - numeric state to get a description for  
                        None: use current state
            
            Returns a string.
        """
        return _xil_api_offline_stub.Stimulus.getStateText(self, state)
    
    # #########################################################################
    def isRunning(self):
        """ Return True if signal generation is currently running. """
        return _xil_api_offline_stub.Stimulus.isRunning(self)
    
    # #########################################################################
    def isDone(self):
        """ Return True if signal generation is done (finished or stopped)."""
        return _xil_api_offline_stub.Stimulus.isDone(self)
    
    # #########################################################################
    def getElapsedTime(self):
        """ Get elapsed time in seconds. """
        return _xil_api_offline_stub.Stimulus.getElapsedTime(self)
    
    # #########################################################################
    def waitUntilDone(self, timeout, step_size=0.500, auto_destroy=True, verbosity=2):
        """ Wait until a running stimulus is done (that is, has reached states
            `eSTOPPED` or `eFINISHED`, see isDone()).
            
            Parameters:
                timeout      - timeout in [s]; stimulus will be stopped after 
                               timeout has been reached.
                step_size    - step_size in [s] to wait between state checks
                auto_destroy - automatically unload stimulus from target
                               after it is done. See destroyOnTarget()
                verbosity    - verbosity of status messages:  
                                0: (mostly) silent  
                                1: waiting ... done messages
                                   plus verbose exception info  
                                2: + stimulus running / unloading / done info
        """
        _xil_api_offline_stub.Stimulus.waitUntilDone(
            self, timeout, step_size, auto_destroy, verbosity
        )
        

# #############################################################################
# @cond DOXYGEN_IGNORE 
# #############################################################################
if __name__ == '__main__':  # pragma: no cover (contains only sample code)
    import time
    start_time = time.time()
    print "instantiating testbench...",
    tb = XilTestbench(
        config_file_path = r"D:\Python\MAPortConfiguration.xml",
        product_name    = "XIL", 
        product_version = "2.0.0",
    )
    print "...testbench instantiated in %.2fs"%(time.time() - start_time)
    
    print "Testbench: %s, %s, v%s"%(
        tb.testbench.VendorName,
        tb.testbench.ProductName,
        tb.testbench.ProductVersion,
    )
    
    def header(text):
        print("\n" + "#" * 80)
        print("# %s"%(text))
        
    # #########################################################################
    # MAPort read/write access
    # #########################################################################
    header("double scalar")
    p = 'Platform()://Model Root/IOUserInterface/IO_PAR/Konstanter/CV prog/Value' # double scalar
    print "# %s"%(p)
    print tb.read(p)
    print tb.write(p, 12)
    print tb.read(p)
    print tb.write(p, 48)
    print tb.read(p)
    
    # #########################################################################
    header("1x6 utint16 vector")
    p = 'Platform()://Model Root/IO/Protocols/RTICANMM\nControllerSetup/RTICANMMCHANNEL_TLC/P6' 
    print "# %s"%(p)
    orig = tb.read(p)
    print orig
    print tb.write(p, [117L, 110L, 117L, 115L, 101L, 10])
    print tb.read(p)
    print tb.write(p, orig)
    print tb.read(p)
    
    # #########################################################################
    header("2x3 double matrix")
    p = 'Platform()://Model Root/MDL/Motormodell/BLDC_Motor_HIL/magnetic/abc->dq/Constant1/Value'
    p = p.replace("Platform()://", "") # not really needed
    print "# %s"%(p)
    orig = tb.read(p)
    print orig
    print tb.write(p, [[1, 2, 3], [0.1, 0.2, -0.3]])
    print tb.read(p)
    print tb.write(p, orig)
    print tb.read(p)
     
    # #########################################################################
    header("3x2 double matrix")
    p = 'Platform()://Model Root/MDL/Motormodell/BLDC_Motor_HIL/magnetic/dq->abc/Constant2/Value'
    p = p.replace("Platform()://", "") # not really needed
    print "# %s"%(p)
    orig = tb.read(p)
    print orig
    print tb.write(p, [[11, 12], [0.21, 0.22], [0.31, 0.32]])
    print tb.read(p)
    print tb.write(p, orig)
    print tb.read(p)
    
    
    # #############################################################################
    # Capture
    # #############################################################################
    capture_vars = [
        'Model Root/IOUserInterface/IO_PAR/Konstanter/CV prog/Value',
        'Model Root/IOUserInterface/IO_DISP/Actors/<V - mon>'
    ]
    
    def printDaqSummary(daq_data):
        for label, sig_data in sorted(daq_data.iteritems()):
            print "--> %s  (%d data points)"%(label, len(sig_data.get("time", [])))
            for key, entries in sorted(sig_data.iteritems()):
                print "    %-4s: [%s]"%(
                    key,
                    ", ".join([
                        d if isinstance(d, str) else "%6.3f"%(d) 
                        for d in entries[:3] + ["..."] + entries[-3:]
                    ]),
                )
    
    # #############################################################################
    header("Data Capture (capture to memory)")
    capture = Capture(tb)
    
    capture.setup(capture_vars)
    print "# starting capture..."
    capture.start()
    
    p = capture_vars[0]
    steps = 8
    for _i in range(steps):
        if _i == steps // 2:
            print "\n[modify] %s"%(p)
            print tb.write(p, 40), "-->", tb.read(p)
        time.sleep(.1)
        print ".",
    print
    
    print "# stopping capture..."
    capture.stop()
    
    # reset value
    tb.write(p, 48)
    
    print "# getting data:"
    daq_data = capture.getData()
    
    printDaqSummary(daq_data)
    
    
    # #########################################################################
    # Stimulus
    # #########################################################################
    header("Stimulus")
    stimulus = Stimulus(tb)
    ssd = StimulusSignalDescription(
        tb, 
        name       = "Drehzahl",
        model_path = 'Platform()://Model Root/IOUserInterface/IO_PAR/Sensors/Drehzahl/Value'
    )
    ssd.addConstSegment(duration=0.5, value=100)
    ssd.addNoiseSegment(duration=0.5, mean=100, sigma=10)
    ssd.addPulseSegment(
        duration=1.0, 
        offset=100, amplitude=20, period=0.200, duty_cycle=.5
    )
    ssd.addRampSegment(duration=1.0, start_value=100, stop_value=200)
    ssd.addRampSlopeSegment(duration=1, offset=200, slope=-100)
    ssd.addIdleSegment(duration=0.5)
    ssd.addExpSegment(duration=.5, start_value=100, stop_value=120, tau=.2)
    ssd.addSawSegment(duration=1.0, offset=100, amplitude=20, period=.200, duty_cycle=0.5)
    ssd.addSineSegment(duration=1.0, offset=100, amplitude=20, period=.200)
    
    stimulus.addSignalDescription(ssd)
    
    print "# uploading stimulus to target..."
    stimulus.loadToTarget()
    print "# starting stimulus..."
    stimulus.start()
    stimulus.waitUntilDone(timeout=10, auto_destroy=False)
    
    print "# starting stimulus (again, but now with a timeout)..."
    stimulus.start()
    stimulus.waitUntilDone(timeout=3, auto_destroy=True)
    
    # #############################################################################
    header("More Stimulus (SignalValueSegment)")
    stimulus = Stimulus(tb)
    ssd = StimulusSignalDescription(
        tb, 
        name       = "Drehzahl",
        model_path = 'Platform()://Model Root/IOUserInterface/IO_PAR/Sensors/Drehzahl/Value'
    )
    
    time_values = [0.002 * i for i in range(1000)]
    data_values = range(0, 250) + range(250, -250, -1) + range(-250, 0) 
    assert len(time_values) == len(data_values)
    ssd.addSignalValueSegment(time_values, data_values)
    
    #ssd.addDataFileSegment(file_path, data_label, time_label, start_time, duration, interpolation)
    
    stimulus.addSignalDescription(ssd)
    
    print("# uploading stimulus to target...")
    stimulus.loadToTarget()
    print("# starting stimulus...")
    stimulus.start()
    stimulus.waitUntilDone(timeout=10, auto_destroy=True)
    
    # #############################################################################
    header("More Stimulus (DataFileSegment)")
    stimulus = Stimulus(tb)
    ssd = StimulusSignalDescription(
        tb, 
        name       = "Drehzahl",
        model_path = 'Platform()://Model Root/IOUserInterface/IO_PAR/Sensors/Drehzahl/Value'
    )
    ssd.addDataFileSegment(
        file_path  = r"D:\Python\stimulus-test.mdf",
        data_label = 'Platform()://Model Root/IOUserInterface/IO_PAR/Sensors/Drehzahl/Value', 
        time_label = None, # not needed for mdf files, time axis is implicit
        start_time = 0, # start at data start
        duration   = 4, # None: run all available data
    #    interpolation
    )
    stimulus.addSignalDescription(ssd)
    
    print("# uploading stimulus to target...")
    stimulus.loadToTarget()
    print("# starting stimulus...")
    stimulus.start()
    stimulus.waitUntilDone(timeout=10, auto_destroy=True)
    
    print("Done.")
# @endcond DOXYGEN_IGNORE
# #############################################################################
