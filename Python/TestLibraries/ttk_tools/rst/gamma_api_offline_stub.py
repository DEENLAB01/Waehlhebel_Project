#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : gamma_api_offline_stub.py
# Package : ttk_tools.rst
# Task    : Interface wrapper for a stub implementation of the default gamma_api, 
#           for debugging without installed GammaV middleware.
# Type    : Interface
# Python  : 2.7
#
# Copyright 2016 - 2018 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 21.12.2016 | JoTremmel  | initial
# 1.1  | 10.02.2017 | JoTremmel  | added stubs for GammaLogger/DAQ/"Capture"
# 1.2  | 03.03.2017 | JoTremmel  | added stub for Gamma.getPVs()
# 1.3  | 30.08.2018 | JoTremmel  | DAQ: updated PVs for GammaLogger v1.0
# 1.4  | 14.09.2018 | JoTremmel  | moved readDaqData to separate module idaq
# 1.5  | 09.09.2020 | JoTremmel  | default to keep_gamma_alive=True
#******************************************************************************
"""
@package ttk_tools.rst.gamma_api_offline_stub
Interface wrapper for a stub implementation of gamma_api in 
ttk_tools.rst._gamma_api_offline_stub.
for debugging without installed GammaV middleware.

This module serves as "interface" to the precompiled module in delivery to 
enable code-completion in PyDev.
"""
import _gamma_api_offline_stub

# Error handling ##############################################################
from gamma_api_common import GammaError             # @UnusedImport
from gamma_api_common import GammaDaqError          # @UnusedImport
from gamma_api_common import GammaDaqStateError     # @UnusedImport
from _gamma_api_offline_stub import GammaApiError   # @UnusedImport (internal error class)

# Defines / Constants / Defaults ##############################################
from gamma_api_common import LOG_LEVEL
from gamma_api_common import MESSAGE_MODE
from gamma_api_common import DEFAULT_LOGFILE_NAME   # @UnusedImport
from gamma_api_common import DEFAULT_LISTEN_PORT
from gamma_api_common import DEFAULT_ATTACH_TIMEOUT
from gamma_api_common import DaqMeasurementStatus   # @UnusedImport

from _gamma_api_offline_stub import is_win32, is_linux      # @UnusedImport - just to be thorough
from _gamma_api_offline_stub import GAMMA_PROCESS_NAME      # @UnusedImport
from _gamma_api_offline_stub import GAMMA_CMD_PROCESS_NAME  # @UnusedImport 


# #############################################################################
# Connection to Gamma Service
# #############################################################################
class Gamma(_gamma_api_offline_stub.Gamma):
    """ GammaService-connection (application) stub. """
    # #########################################################################
    def __init__(self, 
                 system_file,
                 config_file,
                 system_name_local  = None,
                 system_name_remote = None, 
                 io_load            = False,
                 message_mode       = MESSAGE_MODE.CONSOLE,
                 log_level          = LOG_LEVEL.ERROR,
                 log_file_path      = "",
                 keep_gamma_alive   = True,
                 port               = DEFAULT_LISTEN_PORT, 
                 timeout_ms         = DEFAULT_ATTACH_TIMEOUT
                ):
        """ Initialize a GammaV connection.
            
            Parameters:
                system_file        - system configuration file
                config_file        - service configuration file
                system_name_local  - system name for the local system 
                                     (optional - only needed if system_file is not used)
                system_name_remote - system name for a remote system 
                                     (optional - needed if an already started gamma service should be checked and used)
                io_load            - True: load IO Plugins + IO mapping
                message_mode       -  0: console (default)  
                                      1: file  
                                      2: syslog  
                                      3: console and file  
                                      4: console and syslog  
                                      See gamma_api_common.MESSAGE_MODE  
                log_level          -  1: error (default)  
                                      2: warn  
                                      3: info  
                                      See gamma_api_common.LOG_LEVEL  
                log_file_path      - path to write the log file of the gamma service to
                                     (an empty path deactivates file logging) 
                keep_gamma_alive   - leave the gamma service alive on shutdown
                port               - Listen port of the gamma service (see gamma service configuration file)
                timeout_ms         - Timeout to wait for the gamma service during attach
                
            Example:
                gamma_instance = Gamma(
                    system_file = r'D:\Projekte\Gamma\Datenmodelle\Projekte\Kartentester\system.xml',
                    config_file = r'D:\Projekte\Gamma\Datenmodelle\Projekte\Kartentester\config_local.xml', 
                    system_name_local = 'iSyTester',
                    keep_gamma_alive = False,
                    message_mode = MESSAGE_MODE.CONSOLE, 
                    log_level = LOG_LEVEL.ERROR,
                    io_load = False
                )
        """
        _gamma_api_offline_stub.Gamma.__init__(
            self, 
            system_file        = system_file,
            config_file        = config_file,
            system_name_local  = system_name_local,
            system_name_remote = system_name_remote, 
            io_load            = io_load,
            message_mode       = message_mode,
            log_level          = log_level,
            log_file_path      = log_file_path,
            keep_gamma_alive   = keep_gamma_alive,
            port               = port, 
            timeout_ms         = timeout_ms
        )
    
    # #########################################################################
    def getGammaVersioninfo(self):
        """ Get version info of current Gamma-V-Service.
            Returns a version info string or None if access failed.
        """
        return _gamma_api_offline_stub.Gamma.getGammaVersioninfo(self)
    
    # #########################################################################
    def getReference(self):
        """ Get a gaapi reference for variable access.
            Returns a reference to the current gaapi module.
        """
        return _gamma_api_offline_stub.Gamma.getReference(self)
    
    # #########################################################################
    def isGammaServiceAlive(self):
        """ Check if GammaV-Service is alive.
            Returns True if service is alive, otherwise False.
        """
        return _gamma_api_offline_stub.Gamma.isGammaServiceAlive(self)
    
    # #########################################################################
    def detachFromService(self):
        """ Detach from GammaV-service. """
        return _gamma_api_offline_stub.Gamma.detachFromService(self)
    
    # #########################################################################
    def attachToService(self, port=None, timeout_ms=None):
        """ Attach to GammaV-Service. If no parameters are set, default settings 
            (as supplied in constructor) will be used.
            
            Parameters:
                port        - override for Listen port of the gamma service
                timeout_ms  - override for timeout to wait for attach
        """
        return _gamma_api_offline_stub.Gamma.attachToService(
            self, port=port, timeout_ms=timeout_ms
        )
    
    # #########################################################################
    def startScheduler(self, scheduler):
        """ Start a specific scheduler.
            
            Parameters:
                scheduler - id/address of scheduler to start, either as 
                            "name" or "index". Has to be supplied as string, 
                            as both variants may contain a system name 
                            separated by a colon and a assortment of dots.  
                            Compare Gamma V Specification and Overview, 
                            Chapter 10.2 Structure and Naming Conventions
            
            Usage:
                result = gamma_instance.startScheduler(':SchedulerMatlab')
                # or 'SchedulerMatlab'       # a missing system name will be added as default system
                # or 'iSyst:SchedulerMatlab' # w/ explicit system name
                # or ':0'                    # default system, first scheduler
                # or '0:0'                   # first system, first scheduler
                print result
                
            Returns status string of gacmd executable (which is probably empty 
            in this use-case), None if gacmd was not available or a numeric 
            (non-zero) exit code if the gacmd call failed. 
        """
        return _gamma_api_offline_stub.Gamma.startScheduler(self, scheduler)
    
    # #########################################################################
    def stopScheduler(self, scheduler):
        """ Stop a scheduler.
            
            Parameters:
                scheduler  - id/address of scheduler to stop, either as 
                             "name" or "index". See startScheduler()
            Usage:
                result = gamma_instance.stopScheduler('SchedulerMatlab')
                print result
                  
            Returns status string of gacmd executable (which is probably empty 
            in this use-case), None if gacmd was not available or a numeric 
            (non-zero) exit code if the gacmd call failed. 
        """
        return _gamma_api_offline_stub.Gamma.stopScheduler(self, scheduler)
    
    # #########################################################################
    def infoScheduler(self, scheduler):
        """ Get info about a specific scheduler.
            
            Parameters:
                scheduler  - id/address of scheduler to get info on, either as
                             "name" or "index". See startScheduler()
            Usage:
                result = gamma_instance.infoScheduler('SchedulerMatlab')
                print result
                
            Returns status string of gacmd executable, None if gacmd was not 
            available or a numeric (non-zero) exit code if the gacmd call failed.
        """
        return _gamma_api_offline_stub.Gamma.infoScheduler(self, scheduler)
        
    # #########################################################################
    def statSchedulerSlot(self, slot):
        """ Get timing info about a scheduler slot.
            
            Parameters:
                slot     -   id/address of scheduler slot, either as
                             "name" or "index". See startScheduler
            
            Returns status string of gacmd executable, None if gacmd was not 
            available or a numeric (non-zero) exit code if the gacmd call failed.
        """
        return _gamma_api_offline_stub.Gamma.statSchedulerSlot(self, slot)
    
    # #########################################################################
    @staticmethod
    def getPVs():
        """ Get PV addresses available on the currently connected system(s).
            
            Example: PV info dicts
                # Each info dict contains entries similar to this:
                pv_info = {
                    "address":     'iSyst:DAQ.Memory.Group.DIO_IN_00', # full PV address as string (again)
                    "name":        'DIO_IN_00',          # just the PV (array) name
                    "data_type":   'UINT_8',             # data type as string, see gacommon.DataType
                    "num_elements": 1,                   # number of elements of the PV (array)
                    "l5_address":  (0, 13, 0, 0, 0),     # Level-5 address as tuple of indices
                }
                
            Note: 
                For data type BLOB there will be an additional entry 
                "length" that contains the BLOB's length.
                
                The PV (or actually: PV-Array) name will be the unique 
                name below the "group" level (i.e. address level 4), 
                and may still contain further dots for sub-structured PVs
            
            Returns a dict with { <pv_address>: {pv info} } mappings.
        """
        return _gamma_api_offline_stub.Gamma.getPVs()
    
    # #########################################################################
    def getDAQ(self):
        """ Get a DAQ/"Capture" instance configured for this Gamma connection.
        """
        return _gamma_api_offline_stub.Gamma.getDAQ(self)
        

# #############################################################################
#
# #############################################################################
class DataAcquisition(_gamma_api_offline_stub.DataAcquisition):
    """ Data Acquisition with GammaV Logger Task"""
    
    ## Default PV addresses for access/utility variables
    pvaddr_capture_config_flag = "iSyRTA.measurement.config.CaptureConfigFlag"
    pvaddr_capture_run_flag    = "iSyRTA.measurement.config.CaptureRunFlag"
    pvaddr_capture_config_vars = "iSyRTA.measurement.config.ConfigVars"
    
    pvaddr_retval              = "iSyRTA.measurement.config.GL_CommandRetVal"
    pvaddr_retval_descr        = "iSyRTA.measurement.config.GL_RetValDescription"
    pvaddr_file_name           = "iSyRTA.measurement.config.GL_FileName"
    pvaddr_system_ip           = "iSyRTA.measurement.config.GL_IPAddress"
    pvaddr_system_free_space   = "iSyRTA.measurement.config.GL_HDDSpace"
    
    pvaddr_logger_status       = "iSyRTA.measurement.config.GL_LoggerStatus"
    pvaddr_logger_status_code  = "iSyRTA.measurement.config.GL_LoggerStatusID"
    pvaddr_task_status         = "iSyRTA.measurement.config.GL_TaskStatus"
    
    # ########################################################################
    def __init__(self, gamma, system_name="iSyst", ftp_host=None):
        """ GammaV Data Acquisition stub. 
            Parameters:
                gamma       - context for accessing PVs (i.e. a reference to 
                              gaapi for Gamma PVs, see Gamma.getReference())
                system_name - name of remote Gamma system to access
                ftp_host    - host name / ip of remote system to retrieve
                              captured data from.  
                              None: automatically retrieve setting from a support PV
        """
        _gamma_api_offline_stub.DataAcquisition.__init__(
            self, 
            gamma       = gamma, 
            system_name = system_name,
            ftp_host    = ftp_host,
        )
       
    # #########################################################################
    def setup(self, variables):
        """ Setup data acquisition (configure what variables to measure).
            
            Note:
                setup() may only be performed while data acquisition 
                is not already running.
            
            Parameters:
                variables - list/iterable of gamma variables to measure
           
            Usage:
                # direct setup with PV addresses/identifiers:
                daq.setup([
                    "iSyst:Data1.Data1.Data1.Data1", 
                    "iSyst:Data2.Data2.Data2.Data2"
                ])
                # or, when using a VarContainer:
                daq.setup([hil.some_var, hil.some_other_var])
           
        """
        _gamma_api_offline_stub.DataAcquisition.setup(self, variables)
        
    # #########################################################################
    def start(self):
        """ Start a configured data acquisition. """
        _gamma_api_offline_stub.DataAcquisition.start(self)
   
    # #########################################################################
    def stop(self):
        """ Stop a currently running data acquisition. """
        _gamma_api_offline_stub.DataAcquisition.stop(self)
        
    # #########################################################################
    def getData(self):
        """ Get data from last measurement run. Data acquisition should 
            be stopped before retrieving data (and should have been started
            at least once before).
            
            Returns a daq data structure with {  
                <label>: {  
                    "time": [<time_s>, <time_s>, ...],  
                    "data": [<value>,  <value>,  ...],  
                    "type": "<datatype-string>"  
                },  
            } entries.
        """
        return _gamma_api_offline_stub.DataAcquisition.getData(self)
        
    # #########################################################################
    def getRemoteDataFilePath(self):
        """ Get the current data file name (and relative path) to file on 
            remote Gamma system's FTP server.
        """
        return _gamma_api_offline_stub.DataAcquisition.getRemoteDataFilePath(self)
    
    # #########################################################################
    def getDaqDataFile(self, file_path):
        """ Retrieve contents of remote data file.
            
            Parameters:
                file_path - name of file to retrieve from Gamma server
                
            Returns an open file handle in mode r+b, file pointer position will
            be at last written position.
        """
        return _gamma_api_offline_stub.DataAcquisition.getDaqDataFile(
            self, file_path
        )
    
    # #########################################################################
    def setDataStorageFolder(self, folder_path=None):
        """ Set a storage folder for retrieved *.idaq files will to store 
            there. If set to None, a disposable temporary file will be used 
            for data exchange.
            
            Parameters:
                folder_path - path to a folder or None to use temp files
        """
        _gamma_api_offline_stub.DataAcquisition.setDataStorageFolder(
            self, folder_path
        )


# #############################################################################
def loadDaqDataFile(file_path):
    """ Read DAQ data from a file in "idaq" format. 
        Convenience function. See idaq.readDataData().
        
        Parameters:
            file_path - path to DAQ data file
            
        Returns a daq data structure with {  
            <label>: {  
                "time": [<time_s>, <time_s>, ...],  
                "data": [<value>,  <value>,  ...],  
                "type": "<datatype-string>"  
            },  
        } entries.
    """
    return _gamma_api_offline_stub.loadDaqDataFile(file_path)
    

# #############################################################################
# @cond DOXYGEN_IGNORE 
# #############################################################################
if __name__ == '__main__':  # pragma: no cover (contains only sample code)
    import os
    from ttk_base import baseutils
    
    # local offline test -> no IOs loaded, no keep alive
    base_path = r"D:\HIL_Projekte\Kartentester\Datenmodell"
    gamma_instance = Gamma(
        system_file       = os.path.join(base_path, "system.xml"),
        config_file       = os.path.join(base_path, "config_local.xml"), 
        system_name_local = 'iSyTester',
        keep_gamma_alive  = True,
        message_mode      = MESSAGE_MODE.CONSOLE, 
        log_level         = LOG_LEVEL.ERROR,
        io_load           = False,
    )
    
    baseutils.sleepWithFeedback(1000)
    
    print "\n== get gamma version information ================================"
    print gamma_instance.getGammaVersioninfo()
    
    print "gaapi (ref) version:", gamma_instance.getReference().getVersion()
    
    print "# GammaService Status:"
    
    print "\n== get information about a scheduler ============================"
    print gamma_instance.infoScheduler('SchedulerMatlab')
    
    baseutils.sleepWithFeedback(1000)
    
    print "\n== start a scheduler ============================================"
    print gamma_instance.startScheduler('SchedulerMatlab')
    
    print "\n== check if the gamma service instance is alive ================="
    print "# GammaService Alive:"
    print gamma_instance.isGammaServiceAlive()
    
    baseutils.sleepWithFeedback(1000, comment="  Wait after alive check...")
    
    print "\n==  get information about the running scheduler ================="
    print "# Scheduler Statistics:"
    print gamma_instance.infoScheduler('SchedulerMatlab')
    
    baseutils.sleepWithFeedback(1000)
    
    print "# Slot Statistics:"
    print "# Indexed Slot 0.0:"
    print gamma_instance.statSchedulerSlot("0.0")
    print "# Indexed Slot 0.1:"
    print gamma_instance.statSchedulerSlot("0.1")
    print "# Named Slot SchedulerMatlab.Slot_IO:"
    print gamma_instance.statSchedulerSlot("SchedulerMatlab.Slot_IO")
    
    
    print "\n== stop scheduler ==============================================="
    print gamma_instance.stopScheduler('SchedulerMatlab')
    
    baseutils.sleepWithFeedback(1000)
    
    print "\n== get information about the stopped scheduler =================="
    print gamma_instance.infoScheduler('SchedulerMatlab')
    
    print "\n== get currently available process variables (addresses) ========"
    pvs = gamma_instance.getPVs()
    for pv, pv_info in sorted(pvs.iteritems()):
        print "%-10s %s"%("[%(data_type)s]"%pv_info, pv)
    
    print "# found %d PVs"%(len(pvs))
    
    
    print "\n== detach from gamma service ===================================="
    print gamma_instance.detachFromService()
    
    baseutils.sleepWithFeedback(1000)
    del gamma_instance
    
# @endcond DOXYGEN_IGNORE
# #############################################################################
