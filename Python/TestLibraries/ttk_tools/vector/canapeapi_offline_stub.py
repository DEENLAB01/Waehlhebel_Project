#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : canapeapi_offline_stub.py
# Package : ttk_tools.vector
# Task    : Interface to a stub implementation of the default canapeapi.py for
#           debugging without vector hardware or license keys.
# Type    : Interface
# Python  : 2.5+
#
# Copyright 2009 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev  | Date       | Name    | Description
#------------------------------------------------------------------------------
# 1.0  | 22.06.2009 | Tremmel | initial
# 1.1  | 11.03.2010 | Tremmel | cleanup
# 2.0  | 05.06.2012 | Tremmel | renamed from canapeapi_dummy, moved to package 
#                             | ttk_tools, now uses OfflineDataProvider 
# 2.1  | 06.06.2012 | Tremmel | DataAcquisition now generates dummy data
# 2.2  | 24.07.2012 | Tremmel | fix for compatibility with Python 2.2.1
# 2.3  | 19.01.2015 | Tremmel | added polling_rate parameter to DataAcquisition.setup,
#                             | fixed timebase in generated "dummy" DAQ data
# 2.4  | 07.07.2015 | Tremmel | updated interface to match canapeapi.py 1.4
# 2.5  | 15.07.2015 | Tremmel | updated interface to match canapeapi.py 1.5
# 2.6  | 15.12.2015 | Tremmel | tweaks to harmonize base, interface and offline stub
# 2.7  | 08.04.2016 | Tremmel | moved to sub-package ttk_tools.vector
# 2.8  | 10.05.2016 | Tremmel | fixed [ms] => [s] conversion in getData
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3.0  | 22.07.2016 | Tremmel | removed imports from canapeapi/_canapeapi to 
#                             | keep feature check for offline implementation 
#                             | separate
# 3.1  | 28.07.2016 | Tremmel | removed obsolete features: zyklischMessen,
#                             | logError and wrappers for old interfaces
# 3.2  | 02.08.2016 | Tremmel | tweaked DAQ running/stopped status, added getStatus()
#                             | split into base implementation and interface
# 3.3  | 17.10.2016 | Tremmel | switched to canapeapi_common
# 3.4  | 21.11.2016 | Tremmel | updated to match _canapeapi_offline_stub 3.5
# 3.5  | 13.10.2017 | Tremmel | updated to match _canapeapi_offline_stub 4.0
# 3.6  | 02.05.2018 | Tremmel | added CANapeDiagTimeoutError
# 3.7  | 03.05.2018 | Tremmel | added CANapeDiag.sendHexRequestSym
# 3.8  | 08.06.2018 | Tremmel | added CANapeASAP3.getDebugWindowText
# 3.9  | 20.05.2020 | Tremmel | added Scripting stub
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 4.0  | 18.06.2020 | Tremmel | removed non-essential canapeapi_common constant imports,  
#                             | removed convertMDF2MAT (deprecated since CANape 13), 
#                             | added getAvailableConverters and convertData
#******************************************************************************
"""
@package ttk_tools.vector.canapeapi_offline_stub
Interface to a stub implementation of the default canapeapi.py for debugging 
without access to vector software, hardware or license keys.

See ttk_tools.vector._canapeapi_offline_stub for base implementation.
"""

# Error handling ##############################################################
# exception classes (just to make them available)
from canapeapi_common import CANapeError, CANapeErrorString          # @UnusedImport
from canapeapi_common import CANapeAccessError, CANapeDaqError       # @UnusedImport
from canapeapi_common import CANapeDiagError, CANapeDiagTimeoutError # @UnusedImport
from canapeapi_common import CANapeScriptError                       # @UnusedImport
from _canapeapi_offline_stub import CANapeOfflineStubNotSupported # @UnusedImport

# Defines / Constants #########################################################
# import all CANapAPI.h derived definitions so they are directly available here 
# Note that the offline stub will "use" almost none of those definitions
from canapeapi_common import DATA_TYPE          # @UnusedImport
from canapeapi_common import DEV                # 
from canapeapi_common import DIAG_PARAM_TYPE    # @UnusedImport
from canapeapi_common import DIAG_SERVICE       # @UnusedImport
from canapeapi_common import DRIVER             # 
from canapeapi_common import REPR               # 
from canapeapi_common import TYPE_SWITCH        # @UnusedImport
from canapeapi_common import VALUE_TYPE         # @UnusedImport
from canapeapi_common import MEASUREMENT_STATE  # @UnusedImport
from canapeapi_common import SCRIPT_STATUS      # @UnusedImport

# Diagnostic Utility Containers ###############################################
# => see sendSymbolicRequest
from canapeapi_common import DiagParameterName  # @UnusedImport 
from canapeapi_common import DiagParameterValue # @UnusedImport 

from ttk_base.baseutils import HexList

# CANape application and device classes #######################################
import _canapeapi_offline_stub 

# #############################################################################
# @cond DOXYGEN_IGNORE

# keep HEX/PHYS "constants" directly available, as it was before 
## HEX: ECU-internal data format.
HEX  = REPR.HEX
## PHYS: physical value representation.
PHYS = REPR.PHYS
# also keep ECU_INTERNAL/PHYSICAL_REPRESENTATION "constants" directly available
ECU_INTERNAL            = REPR.ECU_INTERNAL            # == REPR.HEX 
PHYSICAL_REPRESENTATION = REPR.PHYSICAL_REPRESENTATION # == REPR.PHYS

# @endcond DOXYGEN_IGNORE
# #############################################################################


# #############################################################################
# CANape Application Connection 
# #############################################################################
class CANapeASAP3(_canapeapi_offline_stub.CANapeASAP3):
    """ CANape ASAP3-connection (application). """
    # #########################################################################
    def __init__(self, working_dir,
                       clear_device_list   = False,
                       debug_mode          = True,
                       keep_canape_alive   = False,
                       canape_path         = None, 
                       init_timeout        = 100000, # ms
                       init_retries        = 3 
                ):
        """ Initialize a CANape connection (that is, a connection to the base 
            application).
            
            Parameters:
                working_dir       - working directory containing `CANape.ini`
                clear_device_list - if device list gets __not__ cleared and later a module
                                    name matches a device in the list, the existing
                                    device (i.e. its settings) will be assigned.
                debug_mode        - if True, the CANape window will be visible
                                    to show debug messages (i.e. the "Write Window")
                keep_canape_alive - if True, the CANape instance will stay active between
                                    calls (thus drastically decreasing startup time)
                canape_path       - path to CANape installation directory, set to None
                                    to use the current path from registry (e.g. for 
                                    single CANape installations)
                init_timeout      - [ms] timeout for connection init and responses 
                                    (not too short, or timeout will occur while 
                                    device database(s) are being read)
                init_retries      - how often the ASAP3 connection init should be 
                                    retried in case of failure
        """
        _canapeapi_offline_stub.CANapeASAP3.__init__(
            self, working_dir,  clear_device_list, debug_mode, keep_canape_alive,
            canape_path, init_timeout, init_retries
        )
    
    # #########################################################################
    def exit(self, verbosity=2):
        """ Manually shut down ASAP3 connection to CANape. If keep_canape_alive 
            was set to False in constructor, the CANape application will 
            also be closed. 
            
            This will normally be called during the destructor call, but 
            it might sometimes be advantageous to exit the connection at a 
            defined time (and not just implicitly when the destructor gets 
            called eventually).
            
            Parameters:
                verbosity - verbosity of stdout/log output:  
                           -1: do not show anything if handle is already gone 
                               (for calls in CANapeASAP3.__del__)  
                            0: errors only  
                            1: Asap3Exit status output  
                            2: also show "nothing to do" notice if handle is already gone  
            
            Returns True if successful (or already closed), otherwise False
        """
        try:
            return _canapeapi_offline_stub.CANapeASAP3.exit(self, verbosity=verbosity)
        except AttributeError:
            pass # may already be gone (if called from destructor)
    
    # #########################################################################
    def getVersion(self, verbose=False):
        """ Get the current CANape/API version.
            
            Parameters:
                verbose - if True, version info will also be printed to stdout
            
            Returns a dictionary with version information.
        """
        return _canapeapi_offline_stub.CANapeASAP3.getVersion(self, verbose)
    
    # #########################################################################
    def getDebugWindowText(self):
        """ Get current contents of CANape's write/debug window. 
            Returns a contents as a string. If access to debug window contents 
            failed, returned string will contain an error message.
        """
        return _canapeapi_offline_stub.CANapeASAP3.getDebugWindowText(self)
    
    # #########################################################################
    def getLastError(self, also_return_code=False):
        """ Get an error text/description for the most recent CANape error.
            
            Parameters: 
                also_return_code  -  if True, the CANape error code will also
                                     be returned
            
            Returns the string "No Error" if, well, no error occurred, 
            otherwise an error description supplied by CANape.
            
            If parameter `also_return_code` is set, the result will be a tuple 
            containing the error info: (<description>, <code>)
        """
        return _canapeapi_offline_stub.CANapeASAP3.getLastError(self, also_return_code)
    
    # #########################################################################
    def getAvailableConverters(self, verbosity=0):
        """ Get available options for data file conversion.
            
            Note:
                Support for Asap3MDFConverterInfo was added in CANape 13.
            
            Parameters:
                verbosity  - 0: silent, 1: log converters to stdout
            
            Returns a dictionary with entries for each converter option:  
                <converter id> : {  
                    'id"'       <converter id>,  
                    'name':     <converter name>,  
                    'comment':  <converter comment>,  
                }  
            or None if API does not support this feature (available starting
            with CANape 13).
        """
        return _canapeapi_offline_stub.CANapeASAP3.getAvailableConverters(self, verbosity)
    
    # #########################################################################
    def convertData(self, converter_id, source_file_name, dest_file_name=None, overwrite=True):
        """ Convert data between different formats.
            
            Note:
                Support for Asap3MDFConvert was added in CANape 13.
            
            Parameters:
                converter_id     - id/name of converter to use, e.g. "MDF2MAT".  
                                   See getAvailableConverters() for, well, 
                                   available converters. 
                source_file_name - name/path of input/source file
                dest_file_name   - name/path of output/destination file  
                                   None: CANape will choose name of output file, 
                                         which typically means same path but a 
                                         different file extension.
                overwrite        - True: overwrite existing files,  
                                   False: do not overwrite existing files
                                          (may raise a CANapeError)
            
        """
        _canapeapi_offline_stub.CANapeASAP3.convertData(
            self, 
            converter_id=converter_id, 
            source_file_name=source_file_name, 
            dest_file_name=dest_file_name, 
            overwrite=overwrite
        )
    

# #############################################################################
# Data Acquisition / Recording
# #############################################################################
class DataAcquisition(_canapeapi_offline_stub.DataAcquisition):
    """ Data acquisition (stub) for multiple CANape devices. Normally, data 
        will be stored as MDF files ("streamed to disk") and later read back 
        after the measurement is completed.
        
        This stub will currently only provide generated dummy data for the 
        measured time range (current value of measured stub variable * 
        (time range / step size) values).  
        See also DataAcquisition.polling_rate
        
        Note: 
           In some CANape versions, CANape will retain a file lock on the 
           current MDF-file after a measurement has been run (and stopped).  
           So multiple start() / stop() cycles after a single setup() may not 
           work in all releases. 
           
           Workaround:  
               Explicitly perform another DAQ setup before each new 
               measurement (works even with the same mdf file path).
        ## 
        
        Note:
           In some versions (probably starting with CANape 13), CANape seems to 
           continue writing to the MDF-file for some time after data acquisition 
           has been successfully stopped.  
           This may cause the current MDF-data to be interpreted as "unsorted"
           but the call to `mdfSort` will fail with an undocumented error code 
           (1022). As this appears to be a race condition, the actual error 
           symptoms might vary.
           
           Workaround:  
               see DataAcquisition.extra_delay_before_mdf_read  
               see DataAcquisition.read_data_attempts_timeout  
               see DataAcquisition.read_data_attempts_delay  
    """
    # #########################################################################
    def __init__(self, canape_asap3, *devices):
        """ Setup data acquisition devices.
            
            Parameters: 
                canape_asap3 - ASAP3-handle to main application server
                *devices     - CANape devices from which to acquire data [1..n].  
                               See CANapeDevice
            
            Usage:
                # with two CANapeDevice instances, one for XCP and one for CAN:
                daq = DataAcquisition(asap3, canape_xcp, canape_can)
            
        """
        
        # Note: members will be overridden/updated in base class' __init__
        #       (just here for documentation)
        
        ## file path of current mdf file. This value will be set during setup().
        self.mdf_file_path = None
        
        ## default file name for MDF files ("daq.mdf") [unused in stub].
        #  This will be used if no explicit mdf_file_path will be supplied 
        #  during setup().
        self.default_mdf_filename = "daq.mdf"
        
        ## default output folder for MDF files [unused in stub]. 
        #  Defaults to the current CANape working folder.
        self.default_mdf_folder = None
        
        ## default/fallback polling-rate in [ms] when using DAQ with polling
        #  (which is a rather unusual thing to do).
        #  This value will be updated during calls to setup().  
        #
        #  Note:
        #    This stub implementation will use the `polling_rate` value as 
        #    step size for generating dummy measurement data (as any actual 
        #    measurement task information is unavailable in stub)
        #
        self.polling_rate = 10
        
        
        ## [s] extra delay before MDF file is read [unused in stub].
        #  This might be useful for some CANape releases (e.g. at least some 
        #  builds of CANNpe13), where the MDF fill is still being processed
        #  when stop() returns.
        self.extra_delay_before_mdf_read = 0.250
        
        ## [s] timeout value for MDF-read attempts [unused in stub]
        # If a MDF file is not yet completely written, mdfLib will raise errors
        # that will "go away" once the file is finished/consistent.
        self.read_data_attempts_timeout  = 15
        
        ## [s] delay between MDF-read attempts [unused in stub]
        # See DataAcquisition.read_data_attempts_timeout
        self.read_data_attempts_delay = 0.500
        
        _canapeapi_offline_stub.DataAcquisition.__init__(
            self, canape_asap3, *devices
        )
    
    # #########################################################################
    def setup(self, measurement_vars, mdf_file_path=None, polling_rate=20):
        """ Setup data acquisition.
            
            Parameters:
                measurement_vars - list of variables to measure. 
                
                mdf_file_path    - path to mdf-file into which to store results.  
                                   If left empty, a default "daq.mdf" file will 
                                   be used/created in the CANape working directory.  
                                   See DataAcquisition.default_mdf_filename.
                
                polling_rate     - [ms] polling rate to use for task-type
                                   "polling".  
                                   Use polling only as fallback if there are no
                                   other/better measurement tasks available.
            
            Info: Format of measurement_vars:
                `measurement_vars` with list entries:  
                `[[var, task, device, repr], ...]` 
                
                `measurement_vars` with dictionary entries:  
                `[{"var": cal.nii, "task": "10ms", "device": "ECU", "repr": REPR.PHY}, ...]`
                    
                Available entries
                * `var`  -   name/identifier of variable (this can simply be
                             a "CalVar" instance, as VarBase-derived variables
                             have their identifier as default representation) 
                             
                * `task` -   name of DAQ-task, see CANapeDevice.getECUTasks() 
                             for available tasks.
                             
                * `device` - index of device (order as supplied during 
                             DataAcquisition.__init__), defaults to first 
                             device (device index 0)  
                             OR  
                             device/module name as supplied during device's
                             constructor call.
                             
                * `repr`   - data representation to use for measured variable, 
                             REPR.HEX or REPR.PHYS (defaults to PHYS).
                             See canapeapi_common.REPR
                    
                Note that at least `var` and `task` entries have to be present,
                `device` and `repr` are optional.
                
            Example: DAQ setup and execution
                meas_vars = [
                    # <variable/identifier>, <measurement task>, <device index>
                    [cal.emotor_temp,       "10ms", 0],
                    [cal.emotor_n_ist,      "10ms", 0],
                    [cal.speicherdruck,     "10ms", 0],
                    ["GE_Oiltemp",          "CAN",  1],
                ]
                    
                daq.setup(meas_vars)
                    
                # start measurement/recorder
                daq.start()
                    
                # do stuff here... 
                    
                # stop measurement/recorder
                daq.stop()
                    
                # get measured data
                daq_data = daq.getData()
            
        """
        return _canapeapi_offline_stub.DataAcquisition.setup(
            self, 
            measurement_vars=measurement_vars,
            mdf_file_path=mdf_file_path,
            polling_rate=polling_rate,
        )
    
    # #########################################################################
    def start(self):
        """ Start the currently configured data acquisition.
            
            Returns True if data acquisition has been started or is already 
            running.
        """
        return _canapeapi_offline_stub.DataAcquisition.start(self)
    
    # #########################################################################
    def stop(self):
        """ Stop a currently running data acquisition.
            
            Returns True if data acquisition has been stopped or was not 
            running to begin with.
        """
        return _canapeapi_offline_stub.DataAcquisition.stop(self)
    
    # #########################################################################
    def getData(self, verbosity=0):
        """ Get data of the last measurement from the measurement data file. 
            
            Parameters:
                verbosity - verbosity level of mdflib status messages.  
                            0: off. See mdflib.readMdf() for more details.
            
            Example: Basic Data Structure:
                daq_data[<canape var name>] = {
                    'data':    <list of data values>,
                    'time':    <list of corresponding time stamps>,
                }
            
            Returns a data dictionary with entries for each recorded variable.
            See basic example, above. See mdflib.readMdf() for a more detailed 
            description.
        """
        return _canapeapi_offline_stub.DataAcquisition.getData(self, verbosity)
        
    
    # #########################################################################
    def getStatus(self, verbosity=1):
        """ Get status of current DAQ/measurement, 
            see canapeapi_common.MEASUREMENT_STATE.
            
            Parameters:
                verbosity -  > 0: status text will be printed to stdout
            
            Returns an numeric status value or None if status is not available 
            (function was added in CANape 9).
        """
        return _canapeapi_offline_stub.DataAcquisition.getStatus(self, verbosity)
        

# #############################################################################
# Standard CANape device class for CCP and XCP
# #############################################################################
class CANapeDevice(_canapeapi_offline_stub.CANapeDevice):
    """ CANape device class (ASAP3-devices: CCP, XCP).
        Also supports Bus-devices (like CAN/FlexRay), although getECUVar() will 
        not return correct values, as those devices do not support polling. 
        DAQ will work just fine, though.
    """
    # #########################################################################
    def __init__(self, canape_asap3,
                       db_filename          = "hil.a2l",
                       comm_channel         = DEV.CAN1,   # DEV.FLX1 
                       driver_type          = DRIVER.XCP, # DRIVER.CCP,
                       module_name          = "ECU",
                       connect              = True,
                       enable_cache         = None,
                       obj_access_retries   = 4,
                       raise_get_exceptions = True, 
                       raise_set_exceptions = True,
                ):
        """ Initializes a standard CANape device (XCP, CAN, ...) connection.
            
            Parameters:
                canape_asap3         - a CANapeASAP3 instance (application interface)
                db_filename          - filename of .a2l database (or .dbc for CAN, 
                                       fibex/.xml for FlexRay, ...)
                comm_channel         - communication channel (see canapeapi_common.DEV constants)
                driver_type          - driver type (see canapeapi_common.DRIVER constants)
                module_name          - name of device/module in CANape
                
                connect              - Device connection behavior:  
                                       True:  immediately connect DUT after device has been 
                                              created. Device will start in state "online"  
                                       False: create device but remain in state "offline" 
                                              if DUT cannot be connected at this time.
                
                enable_cache         - None:  ignore parameter, use default  
                                       True:  enable caching  
                                       False: disable caching  
                                       Available since CANape 10, see Asap3CreateModule3  
                
                obj_access_retries   - number of retries to perform when object 
                                       access fails
                
                raise_get_exceptions - Error handling for get/read access (see getECUVar()):  
                                         True:  Raise exceptions  
                                         False: Return error strings (classic behavior)  
                raise_set_exceptions - Error handling for set/write access (see setECUVar()):  
                                         True:  Raise exceptions  
                                         False: Return error strings (classic behavior)  
            
            Note: Parameter `connect`
                Setting `connect` to False permits attaching/creating a device 
                that is currently not active (e.g. DUT is still shut down), 
                that is, the device-init will not fail right away with error 
                message "No response from ECU (attach Asap2 failed)".
                
                An **inactive** DUT can be successfully attached and start out 
                in state "offline". See isOnline() and goOnline().  
                However, if the DUT is **active** after all, the device's online
                state may end up in state "online" even if `connect` has been 
                set to False.
            
        """
        _canapeapi_offline_stub.CANapeDevice.__init__(
            self, canape_asap3,
            db_filename, comm_channel, driver_type, module_name,
            connect              = connect,
            enable_cache         = enable_cache,
            obj_access_retries   = obj_access_retries,
            raise_get_exceptions = raise_get_exceptions,
            raise_set_exceptions = raise_set_exceptions,
        )
        
    
    # #########################################################################
    def getECUVar(self, varname, representation=REPR.PHYS, extended_mode=False, 
                        silent=False):
        """ Get the current value of a single ECU variable (single read access 
            via polling).
            
            Parameters:
               varname         -  name of variable (signal/measurement/calibration)
               representation  -  data representation, can be either REPR.HEX 
                                  (ecu internal value) or REPR.PHYS (physical 
                                  representation of data).  
                                  See canapeapi_common.REPR.
               extended_mode   -  if True, existing axis data for `CURVE` and
                                  `MAP` objects will also be returned.  
                                  See canapeapi_common.VALUE_TYPE
               silent          -  True: suppress debug error messages
            
            Example: Data format in "simple mode" depending on value types
                VALUE:     a float value
                CURVE:     [values]         # a list of n float values
                MAP:       [values]         # a list of x*y float values
                AXIS_PTS:  [values]         # a list of n float values
                ASCII:     a string 
            
            Example: Data format in "extended mode" depending on value types
                VALUE:     a float value
                CURVE:     ([axis values], [data values])
                MAP:       ([x-axis values], [y-axis values], [data values])
                AXIS_PTS:  [values]
                ASCII:     a string
                
                # Note: If a CURVE or MAP entry has no assigned axis/axes 
                #       (i.e. it has no referenced AXIS_PTS entries), 
                #       CANape will return all axis values as 0.0
            
            Returns the current data found for the variable (calibration 
            object). 
            
            In case of access errors, either a CANapeErrorString will be returned 
            or a CANapeAccessError will be raised, depending on the setting of
            raise_get_exceptions, see CANapeDevice.__init__.
            
            For other error cases (e.g. an invalid data type was encountered),
            a CANapeError will be raised (or CANapeErrorString returned; again, 
            see raise_get_exceptions)
        """
        return _canapeapi_offline_stub.CANapeDevice.getECUVar(
            self, varname, representation, extended_mode, silent
        )
    
    # #########################################################################
    def setECUVar(self, varname, data, representation=REPR.PHYS, 
                        extended_mode=False, return_original=True):
        """ Set data of a single ECU variable.
            
            Parameters:
                varname         -  name of variable (signal/measurement/calibration)
                data            -  data to set (either a scalar value or
                                   a list of values)
                representation  -  data representation, can be either REPR.HEX
                                   (ecu internal value) or REPR.PHYS (physical
                                   representation of data).  
                                   See canapeapi_common.REPR
                extended_mode   -  see description and examples at getECUVar()
                return_original -  True:  return original value before "set"  
                                   False: return current value after "set"  
            
            Returns the previous/original value if `return_original` is True 
            (useful to reset changes later), otherwise the current value (as 
            read back from ECU, useful to check if the new value has been
            successfully set)
            
            In case of errors, either a CANapeErrorString will be returned or 
            a CANapeAccessError will be raised, depending on the setting of
            raise_set_exceptions, see CANapeDevice.__init__.
            
        """
        return _canapeapi_offline_stub.CANapeDevice.setECUVar(
            self, varname, data, representation, extended_mode, return_original
        )
    # #########################################################################################
    # Calibration Object Information 
    # #########################################################################################
    
    # #########################################################################
    def getECUVarInfoBasic(self, varname, representation=REPR.PHYS):
        """ Get information about an ECU var/object 
            
            Parameters:
                varname        - name of variable
                representation - data representation, can be either REPR.HEX 
                                 (ecu internal value) or REPR.PHYS (physical 
                                 representation of data).  
                                 See canapeapi_common.REPR
            
            Returns a dict with some basic variable information:  
                'type':       data type (see canapeapi_common.DATA_TYPE)  
                'address':    memory address  
                'minimum':    minimum value  
                'maximum':    maximum value  
                'increment':  increment value  
        """
        return _canapeapi_offline_stub.CANapeDevice.getECUVarInfoBasic(
            self, varname=varname, representation=representation
        )
    
    # #########################################################################
    def getECUVarByAddress(self, varname, length):
        """ Read `length` bytes from beginning at the address of an object 
            defined by a given name.
            
            Parameters:
                varname         - name of variable at the start address
                length          - number of bytes to read
            
            Returns a raw bytes string.
        """
        return _canapeapi_offline_stub.CANapeDevice.getECUVarByAddress(
            self, varname=varname, length=length
        )
    
    # #########################################################################
    def readBytes(self, address, length, addr_ext=0, verbosity=1):
        """ Read `length` bytes, starting at the supplied address.
            
            Parameters:
                address   - start address in ECU to read from (preferably
                            already a `c_ulong`)
                length    - number of bytes to read
                addr_ext  - address extension, only used with some special 
                            multiprocessor ECUs (leave at 0 if not required)
                verbosity - verbosity of log output  
                            0: only errors  
                            1: status info  
            
            Example:
                buf = canape.readBytes(0x123456, 16)
                print [ord(b) for b in buf] # list of bytes (as int values)
                print HexList(buf)          # list of bytes with "nicer" hex display
                print binascii.hexlify(buf) # hex string
            
            Returns a raw bytes string.
        """
        return _canapeapi_offline_stub.CANapeDevice.readBytes(
            self, address=address, length=length, 
            addr_ext=addr_ext, verbosity=verbosity
        )
    
    # #########################################################################
    def writeBytes(self, address, data, addr_ext=0, verbosity=1):
        """ Write the supplied bytes to ECU, starting at address.
            
            Parameters:
                address   - start address in ECU to read from (preferably
                            already a `c_ulong`)
                data      - an already initialized ctypes string buffer  OR  
                            a list of byte values to write   OR  
                            a hex-string (a leading "0x" will be ignored)  
                            Note that a missing nibble in the hex string will 
                            be zero-padded to get a full byte
                addr_ext  - address extension, only used with some special 
                            multiprocessor ECUs (leave at 0 if not required)
                verbosity - verbosity of log output  
                            0: only errors  
                            1: status info  
            
            Examples:
                canape.writeBytes(0x123456, "0xAABBCC")
                canape.writeBytes(0x123456, "AA BB CC")
                canape.writeBytes(0x123456, "ABBCC") # will be padded to 0ABBCC
                canape.writeBytes(0x123456, [0xAA, 0xBB, 0xCC])
                canape.writeBytes(0x123456, [170, 187, 204])
            
            Returns the write status from low-level API (i.e. 0 on success)
        """
        return _canapeapi_offline_stub.CANapeDevice.writeBytes(
            self, address=address, data=data,
            addr_ext=addr_ext, verbosity=verbosity
        )
    
    # #########################################################################
    # Inherited from BaseCANapeDevice
    # #########################################################################
    
    # #########################################################################
    def release(self, verbosity=2):
        """ Manually release the module/device handle in CANape.
            
            This will normally be called during __del__, but sometimes it might
            be advantageous to release the handle a defined time (and not just 
            implicitly when the destructor gets called eventually).
            
            Parameters:
                verbosity - verbosity of stdout/log output:  
                           -1: do not show anything if handle is already gone (for calls in __del__)  
                            0: errors only  
                            1: Asap3Exit status output  
                            2: also show "nothing to do" notice if handle is already gone  
            
            Returns True if successful (or already released), otherwise False.
        """
        if getattr(_canapeapi_offline_stub.CANapeDevice, "release", None):
            return _canapeapi_offline_stub.CANapeDevice.release(self, verbosity=verbosity)
    
    # #########################################################################
    def runScript(self, script_command, is_file_name=False):
        """ Execute a CAPL script or script command via CANapeAPI.
            
            Note:
                This uses the "classic" `Asap3ExecuteScript` API function which 
                does not provide any script status or return values.
                
                New extended script functions are available since CANape 
                version 9. The classic approach is sufficient for simple cases, 
                though.
            
            Parameters:
                script_command - CAPL command or name of CAPL script file to 
                                 execute. A CAPL command can also be the name
                                 of a custom "project function" that has been
                                 defined in the current workspace.
                is_file_name   - True if `script_command` contains the name of 
                                 a script file to be run,  
                                 False if it directly contains a CAPL command.
            
            Example:
                # multiple commands can be added in sequence
                device.runScript('Speak("Hello World"); Write("Done.");')
                
                # some CAPL commands/methods have to be called on an existing
                # device object
                device.runScript('%s.SaveDatabase(0);'%(device.getModuleName())
                
                # default location of script files is the folder of the current 
                # CANape workspace
                device.runScript('capl_script.scr', is_file_name=True)
            
            Note:
                The executed script or script command might still be running 
                when this function returns.
            
            Returns True if script execution was successful (though not 
            necessarily completed), otherwise False.
        """
        return _canapeapi_offline_stub.CANapeDevice.runScript(
            self, 
            script_command=script_command, 
            is_file_name=is_file_name
        )
    
    # #########################################################################
    def isOnline(self):
        """ Get online state of current device.
            Returns True if the device is online, otherwise False.
        """
        return _canapeapi_offline_stub.CANapeDevice.isOnline(self)
    
    # #########################################################################
    def goOnline(self, retry_timeout=10000):
        """ Switch the CANape device connection to online mode.
            Parameters: 
                retry_timeout - [ms], if > 0, repeated attempts to set the 
                                ECU state will be made until timeout occurs
            Returns a list of testresult entries containing info about retried
            attempts
        """
        return _canapeapi_offline_stub.CANapeDevice.goOnline(self, retry_timeout)
    
    # #########################################################################
    def goOffline(self, retry_timeout=10000):
        """ Switch the CANape device connection to offline mode.
            Parameters: 
                retry_timeout - [ms], if > 0, repeated attempts to set the 
                                ecu state will be made until timeout occurs
            Returns a list of testresult entries containing info about retried
            attempts.
        """
        return _canapeapi_offline_stub.CANapeDevice.goOffline(self, retry_timeout)
    
    # #########################################################################
    def getECUTasks(self):
        """ Get a dictionary containing available measurement tasks 
            (as defined in the ECU)
            
            Returns a task dictionary with entries like:  
                <task name/descr.>: {  
                    "id":         <internal task id>,  
                    "cycle_time": <cycle time in ms, 0 if n/a>  
                }  
        """
        return _canapeapi_offline_stub.CANapeDevice.getECUTasks(self)
        

# #############################################################################
# Diagnostic device class (UDS, ...)
# #############################################################################
class CANapeDiag(_canapeapi_offline_stub.CANapeDiag):
    """ Diagnostics device class (UDS, ...). """
    # #########################################################################
    def __init__(self, canape_asap3,
                       db_filename     = "hil.cdd",
                       comm_channel    = DEV.CAN1, 
                       driver_type     = DRIVER.CANDELA, 
                       module_name     = "DIAG",
                       connect         = True,
                       enable_cache    = None,
                       request_timeout = 30000, # ms
                       enable_tp       = None,
                       restore_tp      = True,
                ):
        """ Initialize a CANape Diagnostics Device connection.
            
            Parameters:
                canape_asap3    - a CANapeASAP3 instance (application interface)
                
                db_filename     - filename of .cdd/.odx database (or similar)
                
                comm_channel    - communication channel (see canapeapi_common.DEV constants)
                
                driver_type     - driver type (see canapeapi_common.DRIVER constants)
                
                module_name     - name of device/module in CANape
                
                connect         - Device connection behavior:  
                                  True:  immediately connect DUT after device has been 
                                         created. Device will start in state "online"  
                                  False: create device but remain in state "offline"
                                         if DUT cannot be connected at this time.
                
                enable_cache    - None:  ignore parameter, use default  
                                  True:  enable caching  
                                  False: disable caching  
                                  Available since CANape 10, see Asap3CreateModule3
                
                request_timeout - timeout for diag requests [ms]
                
                enable_tp       - auto-set Tester Present status:  
                                  None:  leave as configured in workspace  
                                  True:  Enable automatic sending  
                                  False: Disable automatic sending  
                
                restore_tp      - TesterPresent status after going online (again):  
                                  True:  Restore TP status, so it will be the same as 
                                         before going offline.  
                                  False: Do nothing, TP status after going online 
                                         will depend on current CANape configuration.
        """
        _canapeapi_offline_stub.CANapeDiag.__init__(
            self, 
            canape_asap3, 
            db_filename, 
            comm_channel, 
            driver_type, 
            module_name,
            connect         = connect,
            enable_cache    = enable_cache,
            request_timeout = request_timeout,
            enable_tp       = enable_tp,
            restore_tp      = restore_tp,
        )
    
    # #########################################################################
    def isTesterPresentEnabled(self, ignore_errors=True, verbosity=1):
        """ Get current state of automatic sending of Tester Present (TP).
            Note:
                Available since CANape 11.
            
            Parameters:
                ignore_errors - if True, access errors will be ignored and
                                return value will be None.
                verbosity     - 0: silent  
                                1: log current TP status
            
            Returns True if Tester Present sending is currently active,  
            False if TP sending is inactive or (if ignore_errors is set)  
            None if API function access failed (e.g. older CANape releases).
        """
        return _canapeapi_offline_stub.CANapeDiag.isTesterPresentEnabled(
            self, ignore_errors=ignore_errors, verbosity=verbosity
        )
    
    # #########################################################################
    def enableTesterPresent(self, verbosity=1):
        """ Enable automatic sending of Tester Present (TP) service. 
            Note:
                Available since CANape 11.
            
            Parameters:
                verbosity - 0: silent  
                            1: log current TP status
        """
        _canapeapi_offline_stub.CANapeDiag.enableTesterPresent(self, verbosity=verbosity)
    
    # #########################################################################
    def disableTesterPresent(self, verbosity=1):
        """ Disable automatic sending of Tester Present (TP) service. 
            Note:
                Available since CANape 11.
            
            Parameters:
                verbosity - 0: silent  
                            1: log current TP status
        """
        _canapeapi_offline_stub.CANapeDiag.disableTesterPresent(self, verbosity=verbosity)
        
    
    # #########################################################################
    # Inherited from BaseCANapeDevice
    # #########################################################################
    
    # #########################################################################
    def release(self, verbosity=2):
        """ Manually release the module/device handle in CANape.
            
            This will normally be called during __del__, but sometimes it might
            be advantageous to release the handle a defined time (and not just 
            implicitly when the destructor gets called eventually).
            
            Parameters:
                verbosity - verbosity of stdout/log output:
                           -1: do not show anything if handle is already gone (for calls in __del__)
                            0: errors only
                            1: Asap3Exit status output
                            2: also show "nothing to do" notice if handle is already gone
            
            Returns True if successful (or already released), otherwise False.
        """
        if getattr(_canapeapi_offline_stub.CANapeDiag, "release", None):
            # parent class might already be gone (if called from destructor)
            return _canapeapi_offline_stub.CANapeDiag.release(self, verbosity=verbosity)
    
    # #########################################################################
    def runScript(self, script_command, is_file_name=False):
        """ Execute a CAPL script or script command via CANapeAPI.
            
            Note:
                This uses the "classic" `Asap3ExecuteScript` API function which 
                does not provide any script status or return values.
                
                New extended script functions are available since CANape 
                version 9. The classic approach is sufficient for simple cases, 
                though.
            
            Parameters:
                script_command - CAPL command or name of CAPL script file to 
                                 execute. A CAPL command can also be the name
                                 of a custom "project function" that has been
                                 defined in the current workspace.
                is_file_name   - True if `script_command` contains the name of 
                                 a script file to be run,  
                                 False if it directly contains a CAPL command.
            
            Example:
                # multiple commands can be added in sequence
                device.runScript('Speak("Hello World"); Write("Done.");')
                
                # some CAPL commands/methods have to be called on an existing
                # device object
                device.runScript('%s.SaveDatabase(0);'%(device.getModuleName())
                
                # default location of script files is the folder of the current 
                # CANape workspace
                device.runScript('capl_script.scr', is_file_name=True)
            
            Note:
                The executed script or script command might still be running 
                when this function returns.
            
            Returns True if script execution was successful (though not 
            necessarily completed), otherwise False.  
        """
        return _canapeapi_offline_stub.CANapeDiag.runScript(
            self, 
            script_command=script_command, 
            is_file_name=is_file_name
        )
    
    # #########################################################################
    def isOnline(self):
        """ Get online state of current device.
            
            Returns True if the device is online, otherwise False.
        """
        return _canapeapi_offline_stub.CANapeDiag.isOnline(self)
    
    # #########################################################################
    def goOnline(self, retry_timeout=10000):
        """ Switch the CANape diag device connection to online mode.
            
            Parameters: 
                retry_timeout - [ms], if > 0, repeated attempts to set the 
                                ECU state will be made until timeout occurs
            
            Returns a list of testresult entries containing info about retried
            attempts.
        """
        return _canapeapi_offline_stub.CANapeDiag.goOnline(self, retry_timeout)
    
    # #########################################################################
    def goOffline(self, retry_timeout=10000):
        """ Switch the CANape diag device connection to offline mode.
            
            Parameters: 
                retry_timeout - [ms], if > 0, repeated attempts to set the 
                                ECU state will be made until timeout occurs.
            
            Returns a list of testresult entries containing info about retried
            attempts.
        """
        return _canapeapi_offline_stub.CANapeDiag.goOffline(self, retry_timeout)
        
    
    # #########################################################################
    # Diag Methods
    # #########################################################################
    
    # #########################################################################
    def sendHexRequest(self, request):
        """ Send a raw service request as a series of bytes (usually as hex).
            
            Parameters:
                request - a request as list of bytes
            
            Example:
                asap3 = CANapeASAP3(working_dir=r"path/to/canape_working_dir")
                diag  = CANapeDiag(asap3, module_name="device_name")
                diag.goOnline()
                response = diag.sendHexRequest([0x10, 0x03])
                print "response:", response
                diag.goOffline()
            
            Info: Tester Present issues: 
                In order to get diagnostics via CANapeAPI to work, 
                cyclic sending of "Tester Present" may have to be deactivated 
                in CANape config (no, really).
                
                Device Configuration -> [Diagnostics device] -> Tab Communication 
                -> uncheck "Send Tester Present" -> Save 
                
                See also disableTesterPresent() for CANape 11 or later.
            
            Returns a list of responses [[response 1], [response 2], ...].
            Typically, there will only be a single response, though.
        """
        return _canapeapi_offline_stub.CANapeDiag.sendHexRequest(self, request)
    
    # #########################################################################
    def sendSymbolicRequest(self, request, 
                            request_params=None, 
                            response_params=None, 
                            skip_empty_iterations=False):
        """ Send a symbolic service request (name/path as defined in CDD/ODX-file).
            
            Parameters:
                request          - a request as service name/path (from CDD/ODX) 
                request_params   - dict with parameters for the request
                response_params  - list of parameters that should be extracted
                                   from the response
                skip_empty_iterations - for complex parameters: skip iterations
                                   if they contain no data at all
            
            Example:
                response = diag.sendSymbolicRequest(
                    'RoutineCtrl/SR015_Idle_Speed_Modification/Start', 
                    {'engine_speed_request': 1200}
                )
                print response[0]['pos_response']
                
                response = diag.sendSymbolicRequest(
                    'DS019/Read_Discrete_Signal',
                    None,
                    ['safety_status'],
                )
                print response[0]['pos_response']
                print response[0]['response_params']['safety_status']
            
            Note:
                For complex response parameters, supply appropriate instances 
                of `DiagParameterName` (with set sub-parameter names) as entries 
                in `response_params` in order to extract/access the complex 
                sub-responses.  
                See canapeapi_common.DiagParameterName, 
                    canapeapi_common.DiagParameterValue
            
            Returns a list of response dicts [{response 1}, {response 2}, ...] 
            i.e. one dict per response (which usually means just one).  
            
            Each response dict contains:
                'raw_response': raw response as a list of bytes  
                'pos_response': True if response was positive, otherwise False  
                'params':       a dictionary with name: value entries for each 
                                parameter name from the `response_params` list.  
            
        """
        return _canapeapi_offline_stub.CANapeDiag.sendSymbolicRequest(
            self, request, 
            request_params, 
            response_params, 
            skip_empty_iterations
        )
    
    # #########################################################################
    def sendHexRequestSym(self, request, response_params=None):
        """ Send a raw service request as a series of bytes (usually as hex),
            but attempt to decode the response using parameter names/qualifiers
            of the matching symbolic request.
            
            Parameters:
                request         - a request as list of bytes
                response_params - a list of parameter names/qualifiers to
                                  decode, compare sendSymbolicRequest
            
            Example:
                # using a symbolic request
                responses = canape_diag.sendSymbolicRequest(
                    request = "EcuIdentification_Read",
                    request_params  = None,
                    response_params = ["RecordDataIdentifier", "Part_Number"],
                )
                # dto. using a raw request
                responses = canape_diag.sendHexRequestSym(
                    request = [0x22, 0x00, 0x9F],
                    response_params = ["RecordDataIdentifier", "Part_Number"],
                )
                
            
            Returns a list of response dicts [{response 1}, {response 2}, ...] 
            i.e. one dict per response (which usually means just one).  
            
            Each response dict contains:
                'raw_response': raw response as a list of bytes  
                'pos_response': True if response was positive, otherwise False  
                'params':       a dictionary with name: value entries for each 
                                parameter name from the `response_params` list.  
            
            If a parameter name for `response_params` could not be decoded, 
            its value will be set to None.
        """
        return _canapeapi_offline_stub.CANapeDiag.sendHexRequestSym(
            self, 
            request = request, 
            response_params = response_params 
        )
        

# #############################################################################
class Scripting(_canapeapi_offline_stub.Scripting):
    """ Access to extended scripting functions added in CANape 9.
        
        Example:
            # separate calls
            scripting = Scripting(cal_device)
            scripting.create('Write("Log output"); SetScriptResult("Foobar Baz"); return 1234;')
            scripting.start()
            scripting.waitUntilFinished()
            result = scripting.getResult()
            retval = scripting.getReturnValue()
            scripting.release()
            
            assert result == "Foobar Baz"
            assert retval == 1234.0
        
        Example:
            # single call, similar to classic runScript 
            # (but method blocks until script is finished)
            retval = scripting.run('Write("Log output, again"); return 1234;')
            assert retval == 1234.0
        
    """
    # #########################################################################
    def __init__(self, device, verbosity=2):
        """ Parameters:
                device     - CANape device/module (BaseDevice or child instances)
                verbosity  - verbosity of messages logged to console:  
                               0: only errors  
                               1: + status info  
        """
        _canapeapi_offline_stub.Scripting.__init__(self, device, verbosity)
    
    # #########################################################################
    def getStatus(self):
        """ Get execution status for the currently defined script/command.
            Returns a SCRIPT_STATUS value or None if API access failed.
        """
        return _canapeapi_offline_stub.Scripting.getStatus(self)
    
    # #########################################################################
    def create(self, script_command, is_file_name=False):
        """ Create a new script handle for a CAPL script or script command 
            via CANapeAPI.
            
            Parameters:
                script_command - CAPL command or name of CAPL script file to 
                                 execute. A CAPL command can also be the name
                                 of a custom "project function" that has been
                                 defined in the current workspace.
                is_file_name   - True if `script_command` contains the name of 
                                 a script file to be run,  
                                 False if it directly contains a CAPL command.
        
        """
        _canapeapi_offline_stub.Scripting.create(
            self, script_command=script_command, is_file_name=is_file_name
        )
    
    # #########################################################################
    def start(self, command_line=None):
        """ Start execution of a currently defined script.
            Parameters:
                command_line - optional "command line" string to hand to Asap3StartScript.
        """
        _canapeapi_offline_stub.Scripting.start(self, command_line=command_line)
    
    # #########################################################################
    def stop(self):
        """ Stop a currently running script.
            Returns True if script was stopped, False if stop failed and None
            if there was no current script handle to stop.
        """
        return _canapeapi_offline_stub.Scripting.stop(self)
    
    # #########################################################################
    def getReturnValue(self):
        """ Get return value of finished script (set via "return 4711;" in script).
            Returns a float (double) value or None if no script was available.
            Value may be NaN if no return value has been provided.
        """
        return _canapeapi_offline_stub.Scripting.getReturnValue(self)
    
    # #########################################################################
    def getResult(self):
        """ Get string result value of finished script.
            Note: 
                To get a result here, the function "SetScriptResult" 
                has to be called in the executed script.
            
            Returns a string or None if no script was available.
        """
        return _canapeapi_offline_stub.Scripting.getResult(self)
    
    # #########################################################################
    def release(self):
        """ Release a currently defined script """
        _canapeapi_offline_stub.Scripting.release(self)
    
    # #########################################################################
    def waitUntilFinished(self, timeout_s=10):
        """ Wait until a currently running script is finished. 
            Parameters:
                timeout_s - timeout in [s] before script will be stopped.
        """
        _canapeapi_offline_stub.Scripting.waitUntilFinished(self, timeout_s)
    
    # #########################################################################
    def run(self, script_command, is_file_name=False, command_line=None, timeout_s=10):
        """ Run a script command (or CAPL script) via CANapeAPI.
            Essentially just calls 
                * create  
                * start  
                * waitUntilFinished  
                * getReturnValue and  
                * release  
            in sequence.
            
            Parameters:
                script_command - CAPL command or name of CAPL script file to 
                                 execute. A CAPL command can also be the name
                                 of a custom "project function" that has been
                                 defined in the current workspace.
                is_file_name   - True if `script_command` contains the name of 
                                 a script file to be run,  
                                 False if it directly contains a CAPL command.
                command_line   - optional "command line" string to hand to start()
                timeout_s      - seconds to wait for script execution to finish
            
            Example:
                # multiple commands can be added in sequence
                scripting.run('Speak("Hello World"); Write("Done."); return 123;'
            
            Returns the script's return value (see getReturnValue)
        """
        return _canapeapi_offline_stub.Scripting.run(
            self, 
            script_command=script_command, 
            is_file_name=is_file_name, 
            command_line=command_line,
            timeout_s=timeout_s
        )
        

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == '__main__': # pragma: no cover (main contains only sample code)
    import sys
    import time
    
    asap3       = None
    canape_cal  = None
    canape_diag = None
    canape_can  = None
    daq         = None
    
    # #########################################################################
    # device configs for test
    # #########################################################################
    asap3_params = {
        "working_dir":       r"D:\Tools\CANape_Simulators\_workspaces\XCPDemo",
        "clear_device_list": True,  #
        "debug_mode":        True,  # show debug window
        "keep_canape_alive": False, # do not leave CANape main application opened
        "init_timeout":      5000
    }
    cal_params = {
        "db_filename":      "XCPsim.a2l",
        "comm_channel":     DEV.CAN1, 
        "driver_type":      DRIVER.XCP,
        "module_name":      "XCPsim",
    }
    can_params = {
        "db_filename":      "communication.dbc",
        "comm_channel":     DEV.CAN1, 
        "driver_type":      DRIVER.CAN,
        "module_name":      "can",
    }
    diag_params = {
        "db_filename":      "UDS-ExampleEcu.cdd",
        "comm_channel":     DEV.CAN1, 
        "driver_type":      DRIVER.CANDELA,
        "module_name":      "UDS-ExampleEcu",
    }
    # #########################################################################
    
    
    def printDaqEntry(label, values, n_entries=3, skip_aliased=True):
        """ Print a (somewhat formatted) summary for a DAQ entry:
            Parameters:
                label         - label of entry to print
                values        - time/data values for the entry
                n_entries     - number of first/last n entries to print
                skip_aliased  - if True, entry-aliases with context prefix
                                will be skipped (those are only relevant
                                if entries in different contexts have
                                the same label)
        """
        def summary(key, data, n=n_entries):
            d = data.get(key, [])
            n = max(1, min(abs(n), len(d) // 2))
            return "%6s: %s (%d entries)"%(
                key, 
                ", ".join(["%s"%(e) for e in d[:n] + ["..."] + d[-n:]]),
                len(d)
            )
        context = values.get("context")
        if skip_aliased and context and label.startswith(context):
            return 
        print "# %s:"%(label)
        print summary("time", values)
        print summary("data", values)
        
    
    try:
        start_time = time.time()
        
        
        print "# Initialization ######################################################################"
        
        print "\n## ASAP3 ######################################"
        asap3 = CANapeASAP3(**asap3_params)
        
        print "\n## Calibration CCP/XCP ########################"
        canape_cal = CANapeDevice(asap3, connect=True, **cal_params)
        
        print "--> isOnline: ", canape_cal.isOnline()
        print "--> goOffline:", canape_cal.goOffline()
        print "--> isOnline: ", canape_cal.isOnline()
        print "--> goOnline: ", canape_cal.goOnline()
        print "--> isOnline: ", canape_cal.isOnline()
        print "--> goOnline: ", canape_cal.goOnline()
        print "--> isOnline: ", canape_cal.isOnline()
        
        
        print "\n## CAN ########################################"
        canape_can = CANapeDevice(asap3, **can_params)
        
        print "\n## Diag #######################################"
        canape_diag  = CANapeDiag(asap3, **diag_params)
        
        print "CANapeAPI init took %0.3f seconds"%(time.time() - start_time)
        print "#######################################################################################\n"
        time.sleep(0.500)
        print "\n\n"
        
        
        print "# Basics ##############################################################################"
        if canape_cal:
            measurements = [
                "testbit0",     # MEASUREMENT / UBYTE
                "testubyte0",   # MEASUREMENT / UBYTE
                "testudword0",  # MEASUREMENT / ULONG
                "testuword0",   # MEASUREMENT / UWORD
                "testword0",    # MEASUREMENT / SWORD
                "channel_d",    # MEASUREMENT / FLOAT64_IEEE
            ]
            parameters = [
                "ampl_d",       # CHARACTERISTIC / VALUE, double
                "curve_kl2",    # CHARACTERISTIC / CURVE, 8 bytes
                "map1_8_8_uc",  # CHARACTERISTIC / MAP,   8x8 bytes
                
                "Curve1",       # AXIS_PTS "Curve used as axis"
                "Curve2",       # AXIS_PTS "Curve used as axis"
                "KL1",          # CHARACTERISTIC / VAL_BLK (AXIS) "16 BYTE curve"
                "KL2",          # CHARACTERISTIC / CURVE   "8 BYTE shared axis Curve2"
                "KF1",          # CHARACTERISTIC / MAP     "8*8 BYTE no axis"
                "KF2",          # CHARACTERISTIC / MAP     "8*8 BYTE shared axis Curve1/Curve1"
                
                "testString",  # CHARACTERISTIC / ASCII
                "testByte000", # CHARACTERISTIC / VALUE
            ]
            
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            print "\n" + "# " * 40
            print "# default mode (just data content)"
            for name in measurements + parameters:
                try:
                    value = canape_cal.getECUVar(name)
                except CANapeError, ex:
                    print "> %s: %s"%(type(ex).__name__, ex)
                    value = ex
                print "%-12s => %s"%(name, value)
            
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            print "\n" + "# " * 40
            print "# extended mode (adds referenced axes to curve/map entries)"
            for name in measurements + parameters:
                try:
                    value = canape_cal.getECUVar(name, extended_mode=True)
                except CANapeError, ex:
                    print "> %s: %s"%(type(ex).__name__, ex)
                    value = ex
                print "%-12s => %s"%(name, value)
            
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            print "\n" + "# " * 40
            print "# set access"
            for name in parameters:
                try:
                    before = canape_cal.setECUVar(name, 1.638)
                    after  = canape_cal.getECUVar(name)
                    # Note: setting a float value to a int variable will
                    #       cut off any decimal places 
                    canape_cal.setECUVar(name, before)
                    reset  = canape_cal.getECUVar(name)
                except CANapeError, ex:
                    print "> %s: %s"%(type(ex).__name__, ex)
                else:
                    print "%-12s => (before) %s"%(name, before)
                    print "%-12s    (after)  %s"%("", after)
                    print "%-12s    (reset)  %s"%("", reset)
            
            # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
            print "\n" + "# " * 40
            print "# set access for ASCII-type"
            
            def setTest(varname, value):
                def sp(*args):
                    for s in args:
                        if isinstance(s, unicode):
                            s = s.encode(sys.stdout.encoding or "latin-1", "replace") 
                        print s,
                    print
                print
                sp('# set "%s" to "%s"...'%(varname, value))
                sp("[before]", canape_cal.getECUVar(varname))
                canape_cal.setECUVar(varname, value)
                sp("[after] ", canape_cal.getECUVar(varname))
            
            setTest("testString",  "testString")
            setTest("testString",  "shorter")
            setTest("testString",  "somewhat longer")
            setTest("testString",  "b-spécîäl°")
            setTest("testString", u"u-spécîäl°")
            setTest("testString",  "testString")
            
            
        
        if canape_can:
            print("# can #################################################################################")
            pass
            # getECUVar won't work for CAN devices, as CAN signals cannot be polled
            #print 'ECM_A1.EngOilTemp',         canape_can.getECUVar('ECM_A1.EngOilTemp')
            #print 'SyncHilCal.Byte0',          canape_can.getECUVar('SyncHilCal.Byte0')
            #print 'EM2_Temp', canape_can.getECUVar('EM2_Temp') 
        
        if canape_diag:
            print("# diag ################################################################################")
            
            canape_diag.disableTesterPresent()
           
            try:
                request = [0x10, 0x03]
                print "sendHexRequest: %s"%(HexList(request)) 
                response = canape_diag.sendHexRequest(request)
                print "      response: %s"%(response)
            except Exception, ex:
                print "> %s: %s"%(type(ex).__name__, ex)
                
            try:
                request = "EcuIdentification_Read" # Qualifier
                print "sendSymbolicRequest: %s"%(request) 
                responses = canape_diag.sendSymbolicRequest(
                    request,
                    request_params  = None,
                    response_params = ["SID_PR", "RecordDataIdentifier", "Part_Number", "Non-Existing Parameter"], 
                )
                # Note: enumerate supports no "start" parameter before Python 2.6
                for i, response in enumerate(responses):
                    print "      response %d of %d:"%(i + 1, len(responses))
                    for key, value in response.iteritems():
                        print "        %-12s: %r"%(key, value)
                    
            except Exception, ex:
                print "> %s: %s"%(type(ex).__name__, ex)
                import traceback
                traceback.print_exc()
            
            canape_diag.enableTesterPresent()
            print
        print("#######################################################################################\n")
        
        
        
        print("# task info ###########################################################################")
        for device in [canape_cal, canape_can, canape_diag]:
            if not device: 
                continue
            ecu_tasks = device.getECUTasks()
            print "# %s Measurement Tasks:"%(device._module_name)
            if ecu_tasks:
                width = max([len(name) for name in ecu_tasks])
                for task, task_info in ecu_tasks.iteritems():
                    print "  %-*s -> id: %2d"%(width + 2, '"%s"'%(task), task_info['id']),
                    if task_info['cycle_time']:
                        print "(%d ms cycle time)"%(task_info['cycle_time']),
                    print
            else:
                print "  n/a"
            print
            
        # only cyclic tasks:
        # Dictionary and set comprehensions were added/back-ported in Python 2.7...
        # https://docs.python.org/2.7/whatsnew/2.7.html#python-3-1-features
        # cyclic_tasks = {task: data for task, data in ecu_tasks.iteritems() if data['cycle_time']}
        
        # Python 2.5 compatible "dict"-comprehension:
        cyclic_tasks = dict(( (k, v) for k, v in ecu_tasks.iteritems() if v['cycle_time']))
        
        if cyclic_tasks:
            print "Quickest cyclic task:", 
            task, data = sorted(cyclic_tasks.iteritems(), key=lambda e: e[1]['cycle_time'])[0]
            print '"%s" => id: %d @ %d ms'%(task, data["id"], data["cycle_time"])
        
        print("#######################################################################################\n")
        
        
        
        print("# Data Acquisition ####################################################################")
        if canape_cal and canape_can:
            # mixed daq xcp + can
            daq = DataAcquisition(asap3, canape_cal, canape_can)
            meas_vars = [
                ['ECUM_eSystemState',     "DAQ100ms",   0],
                ['s16TemperatureMotorLp', "DAQ1ms",     0],
                ['EM2_Temp',              "can",        1]
            ]
            daq.setup(meas_vars)
            daq.start()
            time.sleep(1)
            daq.stop()
            data = daq.getData()
            for entry, values in data.iteritems():
                printDaqEntry(entry, values)
        
        # ###########################################
        elif canape_cal:
            daq = DataAcquisition(asap3, canape_cal)
            
            # NOTE: DAQ in XCPDemo-Project (and demo mode) is limited to 16kB
            meas_vars = [
                ['PWM',             "1ms"],     # Pulse width signal from PWM_level and Triangle
                ['PWMFiltered',     "1ms"],     # Low pass filtered PWM signal
                ['Triangle',        "1ms"],     # Triangle test signal used for PWM output PWM
                ['bit12Counter',    "1ms"],     # Demo signal (12 bit, incrementing)
                
                ['channel1',        "1ms"],     # FLOAT demo signal (sine wave)
                ['channel2',        "10 ms"],   # FLOAT demo signal (sine wave)
                ['channel3',        "100ms"],   # FLOAT demo signal (sine wave)
                ['ampl',            "1ms"],     # Amplitude of channel 1-3  (Parameter)
            ]
            daq.setup(meas_vars)
            
            print "before start()", 
            daq.getStatus(verbosity=1)
            daq.start()
            print "after start()", 
            daq.getStatus(verbosity=1)
            
            print "Waiting...",
            for i in range(4 * 4):
                #daq.getStatus(verbosity=1)
                time.sleep(.100)
                print ".",
            print "...done"
            
            print "before stop()",
            daq.getStatus(verbosity=1)
            daq.stop()
            print "after stop() ",
            daq.getStatus(verbosity=1)
            
            data = daq.getData()
            
            for entry, values in data.iteritems():
                printDaqEntry(entry, values)
        
        print("#######################################################################################")
        
        print
        print("# runScript ###########################################################################")
        script_command = 'Speak("Hello World from %s");'%(canape_cal.getModuleName())
        script_command += " %s.SaveDatabase(0);"%(canape_cal.getModuleName())
        script_command += ' Write("done");'
        canape_cal.runScript(script_command, is_file_name=False)
        print("#######################################################################################")
        
        print
        print "# Write/Debug-Window Contents: ########################################################"
        print asap3.getDebugWindowText()
        print("#######################################################################################")
        
        print
        print("# set/get #############################################################################")
        print 'set egr_direct_enable_1m (prev value returned):',  canape_cal.setECUVar('egr_direct_enable_1m', 1)
        print 'get egr_direct_enable_1m (curr value returned):',  canape_cal.getECUVar('egr_direct_enable_1m')
        
        print 'set isp_t_coolant_out_2m (prev value returned):',  canape_cal.setECUVar('isp_t_coolant_out_2m', [1, 2, 3, 4])
        print 'set isp_t_coolant_out_2m (prev value returned):',  canape_cal.setECUVar('isp_t_coolant_out_2m', 123)
        print 'get isp_t_coolant_out_2m (curr value returned):',  canape_cal.getECUVar('isp_t_coolant_out_2m')
        
        old = canape_cal.getECUVar('ghc_preheat_dur_ht_3m')
        print "original:", old
        print "test1:   ", canape_cal.setECUVar('ghc_preheat_dur_ht_3m',  42, return_original = False)
        print "test2:   ", canape_cal.setECUVar('ghc_preheat_dur_ht_3m', 128, return_original = False)
        print "restored:", canape_cal.setECUVar('ghc_preheat_dur_ht_3m', old, return_original = False)
        print "#######################################################################################\n"
        
        
        print("# getECUVarInfo #######################################################################")
        prev_verbose = canape_cal.verbose
        canape_cal.verbose = True
        canape_cal.getECUVarInfo("egr_direct_enable_1m")
        canape_cal.getECUVarInfo("is4_t_coolant_out")
        canape_cal.getECUVarInfo("is4_t_coolant_out_2m")
        canape_cal.verbose = prev_verbose
        print("#######################################################################################\n")
        
        
    
    # #########################################################################
    finally:
        print("[cleanup]")
        daq = None
        
        print("\n# canape_diag:")
        print(canape_diag)
        print("\n# canape_can:")
        print(canape_can)
        print("\n# canape_cal:")
        print(canape_cal)
        print("\n# asap3:")
        print(asap3)
        
        # Best practice: Explicitly release devices and shut down ASAP3 handle.
        # Otherwise this would happen during destructor calls, but those might
        # be delayed, happen out-of-order or at a time where other script parts 
        # (like parent classes) have already been garbage-collected and are 
        # no longer available.
        if canape_cal:  canape_cal.release()  # noqa E701
        if canape_can:  canape_can.release()  # noqa E701
        if canape_diag: canape_diag.release() # noqa E701
        asap3.exit()
        
        print("-" * 80)
        canape_diag = None
        canape_can  = None
        canape_cal  = None
        
        asap3       = None
        
        print("Done.")
# @endcond DOXYGEN_IGNORE
# #############################################################################
