#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : canapeapi.py
# Package : ttk_tools.vector
# Task    : Wrapper for CANape Access via CANapeAPI
#           This serves as "interface" to the precompiled module in delivery 
#           to enable code-completion in PyDev
# Type    : Interface
# Python  : 2.5+
#
# Copyright 2012 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 24.06.2012 | J.Tremmel | initial
# 1.1  | 20.02.2013 | J.Tremmel | tweaked docstrings
# 1.2  | 09.08.2013 | J.Tremmel | imported CANape 9.0+ communication channel constants
# 1.3  | 25.07.2014 | J.Tremmel | fixed review findings (see Ticket #23)
# 1.4  | 07.07.2015 | J.Tremmel | added Tester Present methods to CANapeDiag,
#                               | added configurable error behavior for get/setECUVar
# 1.5  | 15.07.2015 | J.Tremmel | added CANapeDiag option to restore TP status
# 1.6  | 15.12.2015 | J.Tremmel | tweaks to harmonize base, interface and offline stub
# 1.7  | 08.04.2016 | J.Tremmel | moved to sub-package ttk_tools.vector
# 1.9  | 26.07.2016 | J.Tremmel | updated to match _canapeapi v5.1
# 1.10 | 28.09.2016 | J.Tremmel | removed obsolete features: zyklischMessen,
#                               | logError and wrappers for old interfaces.
# 1.11 | 26.07.2016 | J.Tremmel | updated to match _canapeapi v5.3
# 1.12 | 17.10.2016 | J.Tremmel | switched to canapeapi_common
# 1.13 | 16.11.2016 | J.Tremmel | added basic runScript method to device classes,
#                               | added manual exit/release methods to ASAP3 
#                               | and device classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2.0  | 13.10.2017 | J.Tremmel | CANapeDevice: added parameters connect and enable_cache,
#                               | removed obsolete parameter dummy_var_name,
#                               | updated interface to match _canapeapi v6.0
# 2.1  | 02.02.2017 | J.Tremmel | update sample code to use explicit calls to 
#                               | device.release()/asap3.exit() to mitigate
#                               | cleanup issues with Python 2.5. Hardened
#                               | release/exit wrappers to abort if parent
#                               | classes have already been garbage-collected.
# 2.2  | 02.05.2018 | J.Tremmel | added CANapeDiagTimeoutError
# 2.3  | 03.05.2018 | J.Tremmel | added CANapeDiag.sendHexRequestSym
# 2.4  | 08.06.2018 | J.Tremmel | added CANapeASAP3.getDebugWindowText
# 2.5  | 20.05.2020 | J.Tremmel | added Scripting interface
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3.0  | 17.06.2020 | J.Tremmel | removed non-essential imported constants from 
#                               | canapeapi_common, removed superfluous parameter
#                               | "representation" from getECUVarByAddress
#                               | removed convertMDF2MAT (deprecated since CANape 13)
#                               | added getAvailableConverters and convertData
#******************************************************************************
"""
@package ttk_tools.vector.canapeapi
Wrapper for Access to CANape devices via CANapeAPI.
This serves as "interface" to the precompiled module in delivery to enable 
code-completion in PyDev. 

See ttk_tools.vector._canapeapi for base implementation.
"""

# Error handling ##############################################################
from canapeapi_common import CANapeError, CANapeErrorString          # @UnusedImport
from canapeapi_common import CANapeAccessError, CANapeDaqError       # @UnusedImport
from canapeapi_common import CANapeDiagError, CANapeDiagTimeoutError # @UnusedImport
from canapeapi_common import CANapeScriptError                       # @UnusedImport

# Defines / Constants #########################################################
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

from ttk_base.baseutils import HexList          # @UnusedImport

# CANape application and device classes #######################################
import _canapeapi

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
class CANapeASAP3(_canapeapi.CANapeASAP3):
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
        _canapeapi.CANapeASAP3.__init__(
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
        if getattr(getattr(_canapeapi, "CANapeASAP3", None), "exit", None):
            # parent class might already be gone (if called from destructor)
            return _canapeapi.CANapeASAP3.exit(self, verbosity=verbosity)

    # #########################################################################
    def getVersion(self, verbose=False):
        """ Get the current CANape/API version.
            
            Parameters:
                verbose - if True, version info will also be printed to stdout
            
            Returns a dictionary with version information.
        """
        return _canapeapi.CANapeASAP3.getVersion(self, verbose)
    
    # #########################################################################
    def getDebugWindowText(self):
        """ Get current contents of CANape's write/debug window. 
            Returns a contents as a string. If access to debug window contents 
            failed, returned string will contain an error message.
        """
        return _canapeapi.CANapeASAP3.getDebugWindowText(self)
    
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
        return _canapeapi.CANapeASAP3.getLastError(self, also_return_code)
        
    
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
        return _canapeapi.CANapeASAP3.getAvailableConverters(self, verbosity)
    
    
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
        return _canapeapi.CANapeASAP3.convertData(
            self, 
            converter_id=converter_id, 
            source_file_name=source_file_name,
            dest_file_name=dest_file_name, 
            overwrite=overwrite
        )
        

# #############################################################################
# Data Acquisition / Recording
# #############################################################################
class DataAcquisition(_canapeapi.DataAcquisition):
    """ Data acquisition for multiple CANape devices. Data will be stored as
        MDF files ("streamed to disk") and later read back after the 
        measurement is completed.
        
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
        
        ## [s] extra delay before MDF file is read.
        #  This might be useful for some CANape releases (e.g. at least some 
        #  builds of CANNpe13), where the MDF fill is still being processed
        #  when stop() returns
        self.extra_delay_before_mdf_read = 0.250
        
        ## [s] timeout value for MDF-read attempts
        # If a MDF file is not yet completely written, mdfLib will raise errors
        # that will "go away" once the file is finished/consistent.
        self.read_data_attempts_timeout  = 15
        
        ## [s] delay between MDF-read attempts [unused in stub]
        # See read_data_attempts_timeout
        self.read_data_attempts_delay = 0.500
        
        _canapeapi.DataAcquisition.__init__(self, canape_asap3, *devices)
    
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
        return _canapeapi.DataAcquisition.setup(
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
        return _canapeapi.DataAcquisition.start(self)
    
    # #########################################################################
    def stop(self):
        """ Stop a currently running data acquisition.
            
            Returns True if data acquisition has been stopped or was not 
            running to begin with.
        """
        return _canapeapi.DataAcquisition.stop(self)
    
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
        return _canapeapi.DataAcquisition.getData(self, verbosity)
        
    
    # #########################################################################
    def getStatus(self, verbosity=1):
        """ Get status of current DAQ/measurement, 
            see canapeapi_common.MEASUREMENT_STATE.
            
            Parameters:
                verbosity -  > 0: status text will be printed to stdout
            
            Returns an numeric status value or None if status is not available 
            (function was added in CANape 9).
        """
        return _canapeapi.DataAcquisition.getStatus(self, verbosity)
        

# #############################################################################
# Standard CANape device class for CCP and XCP
# #############################################################################
class CANapeDevice(_canapeapi.CANapeDevice):
    """ CANape device class (ASAP3-devices: CCP, XCP).
        Also supports Bus-devices (like CAN/FlexRay), although getECUVar() will 
        not return correct values, as those devices do not support polling. 
        DAQ will work just fine, though.
    """
    # #########################################################################
    def __init__(self, canape_asap3,
                       db_filename          = "hil.a2l", ### .a2l to arxml
                       comm_channel         = DEV.CAN1,   # DEV.FLX1
                       driver_type          = DRIVER.XCP, # DRIVER.CCP
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
        _canapeapi.CANapeDevice.__init__(
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
        return _canapeapi.CANapeDevice.getECUVar(
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
        return _canapeapi.CANapeDevice.setECUVar(
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
        return _canapeapi.CANapeDevice.getECUVarInfoBasic(
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
        return _canapeapi.CANapeDevice.getECUVarByAddress(
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
        return _canapeapi.CANapeDevice.readBytes(
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
        return _canapeapi.CANapeDevice.writeBytes(
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
        if getattr(getattr(_canapeapi, "CANapeDevice", None), "release", None):
            # parent class might already be gone (if called from destructor)
            return _canapeapi.CANapeDevice.release(self, verbosity=verbosity)
    
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
        return _canapeapi.CANapeDevice.runScript(
            self, 
            script_command=script_command, 
            is_file_name=is_file_name
        )
    
    # #########################################################################
    def isOnline(self):
        """ Get online state of current device.
            Returns True if the device is online, otherwise False.
        """
        return _canapeapi.CANapeDevice.isOnline(self)
    
    # #########################################################################
    def goOnline(self, retry_timeout=10000):
        """ Switch the CANape device connection to online mode.
            Parameters: 
                retry_timeout - [ms], if > 0, repeated attempts to set the 
                                ECU state will be made until timeout occurs
            Returns a list of testresult entries containing info about retried
            attempts
        """
        return _canapeapi.CANapeDevice.goOnline(self, retry_timeout)
    
    # #########################################################################
    def goOffline(self, retry_timeout=10000):
        """ Switch the CANape device connection to offline mode.
            Parameters: 
                retry_timeout - [ms], if > 0, repeated attempts to set the 
                                ecu state will be made until timeout occurs
            Returns a list of testresult entries containing info about retried
            attempts.
        """
        return _canapeapi.CANapeDevice.goOffline(self, retry_timeout)
    
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
        return _canapeapi.CANapeDevice.getECUTasks(self)
        

# #############################################################################
# Diagnostic device class (UDS, ...)
# #############################################################################
class CANapeDiag(_canapeapi.CANapeDiag):
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
        _canapeapi.CANapeDiag.__init__(
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
        return _canapeapi.CANapeDiag.isTesterPresentEnabled(
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
        _canapeapi.CANapeDiag.enableTesterPresent(self, verbosity=verbosity)
    
    # #########################################################################
    def disableTesterPresent(self, verbosity=1):
        """ Disable automatic sending of Tester Present (TP) service. 
            Note:
                Available since CANape 11.
            
            Parameters:
                verbosity - 0: silent  
                            1: log current TP status
        """
        _canapeapi.CANapeDiag.disableTesterPresent(self, verbosity=verbosity)
        
    
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
        if getattr(getattr(_canapeapi, "CANapeDiag", None), "release", None):
            # parent class might already be gone (if called from destructor)
            return _canapeapi.CANapeDiag.release(self, verbosity=verbosity)
    
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
        return _canapeapi.CANapeDiag.runScript(
            self, 
            script_command=script_command, 
            is_file_name=is_file_name
        )
    
    # #########################################################################
    def isOnline(self):
        """ Get online state of current device.
            
            Returns True if the device is online, otherwise False.
        """
        return _canapeapi.CANapeDiag.isOnline(self)
    
    # #########################################################################
    def goOnline(self, retry_timeout=10000):
        """ Switch the CANape diag device connection to online mode.
            
            Parameters: 
                retry_timeout - [ms], if > 0, repeated attempts to set the 
                                ECU state will be made until timeout occurs
            
            Returns a list of testresult entries containing info about retried
            attempts.
        """
        return _canapeapi.CANapeDiag.goOnline(self, retry_timeout)
    
    # #########################################################################
    def goOffline(self, retry_timeout=10000):
        """ Switch the CANape diag device connection to offline mode.
            
            Parameters: 
                retry_timeout - [ms], if > 0, repeated attempts to set the 
                                ECU state will be made until timeout occurs.
            
            Returns a list of testresult entries containing info about retried
            attempts.
        """
        return _canapeapi.CANapeDiag.goOffline(self, retry_timeout)
        
    
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
        return _canapeapi.CANapeDiag.sendHexRequest(self, request)
    
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
        return _canapeapi.CANapeDiag.sendSymbolicRequest(
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
        return _canapeapi.CANapeDiag.sendHexRequestSym(
            self, 
            request = request, 
            response_params = response_params 
        )
        

# #############################################################################
class Scripting(_canapeapi.Scripting):
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
        _canapeapi.Scripting.__init__(self, device, verbosity)
    
    # #########################################################################
    def getStatus(self):
        """ Get execution status for the currently defined script/command.
            Returns a SCRIPT_STATUS value or None if API access failed.
        """
        return _canapeapi.Scripting.getStatus(self)
    
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
        _canapeapi.Scripting.create(
            self, script_command=script_command, is_file_name=is_file_name
        )
    
    # #########################################################################
    def start(self, command_line=None):
        """ Start execution of a currently defined script.
            Parameters:
                command_line - optional "command line" string to hand to Asap3StartScript.
        """
        _canapeapi.Scripting.start(self, command_line)
    
    # #########################################################################
    def stop(self):
        """ Stop a currently running script.
            Returns True if script was stopped, False if stop failed and None
            if there was no current script handle to stop.
        """
        return _canapeapi.Scripting.stop(self)
    
    # #########################################################################
    def getReturnValue(self):
        """ Get return value of finished script (set via "return 4711;" in script).
            Returns a float (double) value or None if no script was available.
            Value may be NaN if no return value has been provided.
        """
        return _canapeapi.Scripting.getReturnValue(self)
    
    # #########################################################################
    def getResult(self):
        """ Get string result value of finished script.
            Note: 
                To get a result here, the function "SetScriptResult" 
                has to be called in the executed script.
            
            Returns a string or None if no script was available.
        """
        return _canapeapi.Scripting.getResult(self)
    
    # #########################################################################
    def release(self):
        """ Release a currently defined script """
        _canapeapi.Scripting.release(self)
    
    # #########################################################################
    def waitUntilFinished(self, timeout_s=10):
        """ Wait until a currently running script is finished. 
            Parameters:
                timeout_s - timeout in [s] before script will be stopped.
        """
        _canapeapi.Scripting.waitUntilFinished(self, timeout_s)
    
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
        return _canapeapi.Scripting.run(
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
    print("== Active CANape installation path: %s =="%(_canapeapi._getCanapeRegPath()))
    
    # NOTE: Tests have been moved to canapeapi_test.py
    
    print("Done.")
# @endcond DOXYGEN_IGNORE
# #############################################################################
