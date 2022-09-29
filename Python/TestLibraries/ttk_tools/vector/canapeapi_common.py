#******************************************************************************
# -*- coding: latin-1 -*-
# File    : canapeapi_common.py
# Package : ttk_tools.vector
# Task    : Common utility functions and classes for CANape access
# Type    : Implementation
# Python  : 2.5+
# 
# Copyright 2010 - 2020 iSyst Intelligente Systeme GmbH
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev.| Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0 | 26.06.2010 | J.Tremmel  | initial
# 1.1 | 24.08.2011 | J.Tremmel  | renamed registry_utils => canape_utils,
#                                 moved other utility functions to here
# 1.2 | 30.07.2012 | J.Tremmel  | docstring cleanup
# 1.3 | 08.04.2016 | J.Tremmel  | moved to sub-package ttk_tools.vector,
#                               | refactored some functions to ttk_tools.win32_utils
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2.0 | 22.07.2016 | J.Tremmel  | moved base classes for CANape errors here so
#                               | they can be re-used in offline implementation
#                               | without triggering feature checks in main 
#                               | implementation. Also moved all "defines" to 
#                               | this module (for the same reason)
# 2.1 | 02.08.2016 | J.Tremmel  | removed import of win32_utils.waitPumpMessages
#                               | (now gets imported directly in _canapeapi).
#                               | Tweaked HexList repr to better handle negative 
#                               | values, added examples. 
# 2.2 | 09.08.2016 | J.Tremmel  | added new "defines" from CANape 14
# 2.3 | 17.10.2016 | J.Tremmel  | renamed to canapeapi_common
# 2.4 | 18.10.2016 | J.Tremmel  | switched to EnumInfo for enum-like value containers
# 2.5 | 21.09.2017 | J.Tremmel  | added api_msg and error_code members to CANapeError 
# 2.6 | 02.05.2018 | J.Tremmel  | added CANapeDiagTimeoutError
# 2.7 | 17.10.2018 | J.Tremmel  | added type for 2D value blocks
# 2.8 | 20.05.2020 | J.Tremmel  | added SCRIPT_STATUS and CANapeScriptError
# 2.9 | 17.06.2020 | J.Tremmel  | updated info_mappings
#******************************************************************************
""" 
@package ttk_tools.vector.canapeapi_common
Common utility functions and classes for CANape access (used in canapeapi.py).
"""
from ttk_base.errors    import TTkErrorString, TTkException
from ttk_base.baseutils import EnumInfo

# #############################################################################
# Defines / Constants 
# #############################################################################


# #############################################################################
class REPR(EnumInfo):
    """ Measurement data format representation constants from enum `TFormat` 
        (original constants have no specific prefix) 
    """
    ## ECU-internal data format
    HEX = ECU_INTERNAL = 0
    ## physical value representation
    PHYS = PHYSICAL_REPRESENTATION = 1
    
    __info_mapping__ = {
        HEX:  'HEX: ECU-internal data format',
        PHYS: 'PHYS: physical value representation',
    }
    

# #############################################################################
class VALUE_TYPE(EnumInfo): 
    """ Value type constants from enum `TValueType` (original constants have no 
        specific prefix) 
    """
    ## scalar value
    VALUE   = 0
    ## curve, 2D
    CURVE   = 1
    ## map, 3D
    MAP     = 2
    ## axis points
    AXIS    = 3
    ## string value
    ASCII   = 4 
    ## value block, 2D
    VAL_BLK = 5
    

# #############################################################################
class DATA_TYPE(EnumInfo): 
    """ Data type constants (`TYPE_*`) from enum `TAsap3DataType` """
    UNKNOWN  = 0
    INT      = 1
    FLOAT    = 2
    DOUBLE   = 3
    SIGNED   = 4
    UNSIGNED = 5
    STRING   = 6
    
    __info_mapping__ = {
        UNKNOWN:  'Unknown',
        INT:      'Int',
        FLOAT:    'Float',
        DOUBLE:   'Double',
        SIGNED:   'Signed',
        UNSIGNED: 'Unsigned',
        STRING:   'String', 
    }
    

# #############################################################################
class DRIVER(EnumInfo):
    """ Driver type constants (`ASAP3_DRIVER_*`) from enum `tDriverType`. """
    ## unknown driver type
    UNKNOWN        =     0
    ## CCP: CAN Calibration Protocol Driver
    CCP            =     1
    ## XCP: Universal Measurement and Calibration Protocol Driver
    XCP            =     2
    ## CAN: Controller Area Network Driver
    CAN            =    20
    ## Keyword protocol 2000 on CAN via ISO/TF2
    KWPCAN         =    30
    ## Pure offline driver
    HEXEDIT        =    40
    ## Analog measurement data (e.g. 'National Instruments' PCMCIA-card)
    ANALOG         =    50
    ## CANopen Driver
    CANOPEN        =    60
    ## CANdela Diagnostic Driver
    CANDELA        =    70
    ## Environment (access to global variables)
    ENVIRONMENT    =    80
    ## LIN: Local Interconnect Network
    LIN            =    90
    ## FlexRay Driver
    FLX            =   100
    ## Functional Diagnostic Driver
    FUNC           =   110
    ## NI DAQ Driver 'National Instruments'
    NIDAQMX        =   120
    ## XCP Driver for RAMscope
    XCP_RAMSCOPE   =   130
    ## System Driver
    SYSTEM         =   140
    ## Ethernet driver (CANape 14++)
    ETH            =   150
    ## DAIO system driver (CANape 14++)
    DAIO_SYSTEM    =   160
    ## Keyword protocol 2000 on K-Line
    KWP2000        =   255
    
    __info_mapping__ = {
        UNKNOWN:       "UNKNOWN",
        CCP:           "CCP",
        XCP:           "XCP",
        CAN:           "CAN",
        KWPCAN:        "KWP2000 on CAN",
        HEXEDIT:       "HEXEDIT",
        ANALOG:        "ANALOG",
        CANOPEN:       "CANopen",
        CANDELA:       "CANdela Diagnostic",
        ENVIRONMENT:   "Environment (access to global variables)",
        LIN:           "LIN",
        FLX:           "FlexRay",
        FUNC:          "Functional Diagnostic Driver",
        NIDAQMX:       "NI DAQ Driver",
        XCP_RAMSCOPE:  "XCP Driver for RAMscope",
        SYSTEM:        "System driver",
        ETH:           "Ethernet driver",
        DAIO_SYSTEM:   "DAIO system driver",
        KWP2000:       "KWP2000 on K-Line",
    }
    

# #############################################################################
class TYPE_SWITCH(EnumInfo):
    """ Device online switch state constants (`TYPE_SWITCH_*`) from enum 
        `TAsap3ECUState`. 
    """
    ONLINE  = 0
    OFFLINE = 1
    

# #############################################################################
class MEASUREMENT_STATE(EnumInfo): 
    """ Measurement state constants (`eT_MEASUREMENT_*`) from enum 
        `tMeasurementState` (new in CANape 9). 
    """
    ## no measurement active
    STOPPED             = 0
    ## measurement started, but measurement thread not yet running
    INIT                = 1
    ## measurement will be stopped via function in prStart
    STOP_ON_START       = 2
    ## measurement stop requested, but not yet stopped
    EXIT                = 3
    ## measurement started, measurement thread is running
    THREAD_RUNNING      = 4
    ## measurement loop is running
    RUNNING             = 5
    
    __info_mapping__ = {
        STOPPED:        "stopped, no measurement active",
        INIT:           "started, but measurement thread not yet running",
        STOP_ON_START:  "will be stopped via function in prStart", # ?
        EXIT:           "stop requested, but not yet stopped",
        THREAD_RUNNING: "started, measurement thread is running",
        RUNNING:        "loop is running",
    }
    

# #############################################################################
class DIAG_SERVICE(EnumInfo):
    """ Diagnostic service states (`DIAG_SERVICE_*`) from enum `eServiceStates`.
        
        Note:
            Service states have explicitly been defined in ascending order:  
            `CREATED` => `RUNNING` => `FINISHED` => `TIMEOUT`
    """
    ## Diagnostic Service created but not yet sent
    CREATED  = 10
    ## Diagnostic Service created and sent, currently running 
    #  -> no response received 
    RUNNING  = 20 # CREATED  + 10
    ## Diagnostic Service finished running 
    #  -> response received
    FINISHED = 30 # RUNNING  + 10
    ## Diagnostic Service was created and sent,
    # but a timeout occurred while CANape was waiting for response
    TIMEOUT  = 40 # FINISHED + 10
    
    __info_mapping__ = {
        CREATED:  "Service created (but not yet sent)",
        RUNNING:  "Service running, response not yet received",
        FINISHED: "Service finished, response received",
        TIMEOUT:  "A timeout occurred while waiting for response",
    }
    

# #############################################################################
class DIAG_PARAM_TYPE(EnumInfo):
    """ Diagnostic response parameter types (`Param*`) from enum `EnParamType`.
    """
    SIGNED     = 1
    DOUBLE     = 2
    BCD        = 3
    UNSIGNED   = 4
    FLOAT      = 5
    AUTODETECT = 6
    
    __info_mapping__ = {
        SIGNED:     "Signed",
        DOUBLE:     "Double",
        BCD:        "BCD",
        UNSIGNED:   "Unsigned",
        FLOAT:      "Float",
        AUTODETECT: "Autodetect",
    }
    

# #############################################################################
# Device channels defined in CANapAPI.h  (v6.5, v7):
#     1..8: DEV_CAN1..DEV_CAN8
#      255: DEV_TCP
#      256: DEV_UDP
#      261: DEV_USERDEFINED
#
# Comment in CANapAPI.h (until CANape 12):
#    channelNo - Logical communication channel to be used
#    (like CCP:1-4 = CAN1-CAN4, 5 = TCP/IP, 6 = UDP, 261 = userdefined (only for XCP))
#
# since CANape 13 this now reads:
#    channelNo - Logical communication channel to be used 
#    (like CCP:1-4 = CAN1-CAN4, 255 = TCP/IP, 256 = UDP))
#
# #############################################################################
class DEV(EnumInfo):
    """ Device channel constants (DEV_*) from CANapAPI.h """
    # CAN #########################################

    CAN1 =      1 # CAN 1
    CAN2 =      2 # CAN 2
    CAN3 =      3 # CAN 3
    CAN4 =      4 # CAN 4
    CAN5 =      5 # CAN 5
    CAN6 =      6 # CAN 6
    CAN7 =      7 # CAN 7
    CAN8 =      8 # CAN 8
    # Note: CAN 9..19 not defined in CANapAPI.h (last checked w/ CANape 14SP3)
    CAN20 =    20 # CAN 20  (CANape 9.0+)

    CANFD1 = 121  # CANFD 121
    CANFD2 = 122  # CANFD 122
    CANFD3 = 123  # CANFD 123
    CANFD4 = 124  # CANFD 124
    CANFD5 = 125  # CANFD 125
    CANFD6 = 126  # CANFD 126
    CANFD7 = 127  # CANFD 127
    CANFD8 = 128  # CANFD 128
    CANFD9 = 129  # CANFD 129
    # FlexRay (CANape 9.0+) #######################
    FLX1 =     31 # FLX 1
    FLX2 =     32 # FLX 2
    FLX3 =     33 # FLX 3
    FLX4 =     34 # FLX 4
    FLX5 =     35 # FLX 5
    FLX6 =     36 # FLX 6
    FLX7 =     37 # FLX 7
    FLX8 =     38 # FLX 8
    
    # LIN (CANape 9.0+) ###########################
    LIN1 =     61 # LIN 1
    LIN2 =     62 # LIN 2
    LIN3 =     63 # LIN 3
    LIN4 =     64 # LIN 4
    LIN5 =     65 # LIN 5
    LIN6 =     66 # LIN 6
    LIN7 =     67 # LIN 7
    LIN8 =     68 # LIN 8
    
    # VX-Box (CANape 9.0+) ########################
    # CAN on VX 1-4
    VX_CAN1 =  81 # VX CAN 1
    VX_CAN2 =  82 # VX CAN 2
    VX_CAN3 =  83 # VX CAN 3
    VX_CAN4 =  84 # VX CAN 4
    # TCP on VX
    VX_TCP  =  85 # VX TCP
    VX_UDP  =  86 # VX UDP
    
    # SXI (CANape 9.0+) ###########################
    SXI1 =     91 # SXI 1
    SXI2 =     92 # SXI 2
    SXI3 =     93 # SXI 3
    SXI4 =     94 # SXI 4
    SXI5 =     95 # SXI 5
    SXI6 =     96 # SXI 6
    SXI7 =     97 # SXI 7
    SXI8 =     98 # SXI 8
    
    # misc ########################################
    USB =     110 # USB
    TCP =     255 # TCP
    UDP =     256 # UDP
    
    ## "User Defined Interface"
    # (gets used for FlexRay connections in CANape releases pre-9.0 )
    USERDEFINED  = 261
    
    # User Ethernet Interface (CANape 14++) #######
    VX_ETHERNET1 = 271
    VX_ETHERNET2 = 272
    DAIO_DLL     = 280
    

# #############################################################################
class SCRIPT_STATUS(EnumInfo):
    """ Script execution status values from enum `TScriptStatus`. 
        (added in CANape 9). 
    """
    Ready           =  1 # Initial status after creation of the task
    Starting        =  2 # Waiting in the list for execution
    Running         =  3 # Status if task was not finished in one Eval step
    Sleeping        =  4 # Function contained Sleep function
    Suspended       =  5 # Suspended by user
    Terminated      =  6 # Terminated by user
    FinishedReturn  =  7 # Successful finish, Return value available
    FinishedCancel  =  8 # Successful finish, No Return value
    Failure         =  9 # Failure
    Timeout         = 10 # Terminated due to timeout
    
    __info_mapping__ = {
        Ready:          "Initial status after creation of the task",
        Starting:       "Waiting in list for execution",
        Running:        "Task not yet finished",
        Sleeping:       "Function contained Sleep function",
        Suspended:      "Suspended by user",
        Terminated:     "Terminated by user",
        FinishedReturn: "Successful finish, return value available",
        FinishedCancel: "Successful finish, no return value",
        Failure:        "Failure",
        Timeout:        "Terminated due to timeout",
    }


# #############################################################################
# Error / Exception classes
# #############################################################################

# #############################################################################
class CANapeError(TTkException):
    """ Base error for CANape connection """ 
    def __init__(self, msg='', log_msg=True, api_msg=None, error_code=None):
        """ Parameters:
                msg        - error message
                log_msg    - True:  log message to stdout,  
                             False: no log output
                api_msg    - CANape-provided "last error" message, if available
                error_code - error code from CANapeAPI, if available.
        """
        msg = "%s"%(msg)
        if api_msg:
            msg = "%s: %s"%(msg, api_msg) if msg else "%s"%(api_msg)
        
        if error_code:
            msg = "%s [%s]"%(msg, error_code)
        
        if log_msg and msg:
            print '> %s'%(msg.replace('\n', '\n> '))
            
        ## error code from API function call, if available
        self.error_code = error_code
        ## error description from APU ("last error"), if available
        self.api_msg    = api_msg
        TTkException.__init__(self, msg)
        

# #############################################################################
class CANapeAccessError(CANapeError):
    """ Cal-object access errors for CANape connection """
    def __init__(self, varname='', msg='', log_msg=False, api_msg=None, error_code=None):
        if varname:
            msg = 'Access to "%s" failed%s'%(
                varname, " (%s)"%(msg) if msg else ""
            )
        CANapeError.__init__(self, msg, log_msg, api_msg, error_code)
        

# #############################################################################
class CANapeDaqError(CANapeError):
    """ Data Acquisition errors for CANape connection. """
    def __init__(self, msg='', log_msg=False, api_msg=None, error_code=None):
        CANapeError.__init__(
            self, 'Data Acquisition: %s'%(msg), log_msg, api_msg, error_code
        )
        

# #############################################################################
class CANapeDiagError(CANapeError):
    """ Errors for CANape diagnostic connections. """ 
    def __init__(self, msg='', log_msg=False, api_msg=None, error_code=None):
        CANapeError.__init__(
            self, 'Diagnostics: %s'%(msg), log_msg, api_msg, error_code
        )
        

# #############################################################################
class CANapeDiagTimeoutError(CANapeDiagError):
    """ Timeout occurred during a diag request """
    

# #############################################################################
class CANapeScriptError(CANapeError):
    """ Errors during script execution """
    

# #############################################################################
class CANapeErrorString(TTkErrorString):
    """ A wrapper for error message strings so they can be distinguished
        from "normal" string values (like contents of ASCII-type variables). 
    """
    

# #############################################################################
# Diag: Parameter Value Container
# #############################################################################
class DiagParameterValue(str):
    """ Container for diagnostic response values that may have multiple value
        representations.
        
        Base representation is a "string", others might be "raw", "numeric"
        and "complex parameters" that contain a list of sub-parameters as 
        before:
            DiagParameterValue         - value as basic string representation 
                                         (which should always be available)
            DiagParameterValue.raw     - raw value representation
            DiagParameterValue.numeric - numeric value representation
            DiagParameterValue.complex - complex value representation (a list 
                                         of sub-responses with sub-value dicts)
    """
    # #########################################################################
    def __new__(cls, value, *args, **kwargs): # @UnusedVariable *args, **kwargs (see __init__)
        """ Create a custom instance of the immutable str type.
            Parameters:
                value - value as string representation, see __init__
        """
        return str.__new__(cls, value)
    
    # #########################################################################
    def __init__(self, value, # @UnusedVariable value (see __new__)
                 raw_val=None, numeric_val=None, complex_val=None): 
        """ Create a new diagnostics parameter value. 
            
            It should normally not be necessary to create those values directly.
            However, instances of DiagParameterValue will be returned by 
            diagnostic requests to give access to all available value 
            representations.
            
            Parameters: 
                value       - value as string representation
                raw_val     - raw value representation (e.g. bytes)
                numeric_val - numeric value representation
                complex_val - a list of sub-responses containing a dictionary
                              with entries for each requested sub-parameter
        """
        ## raw value representation
        self.raw     = raw_val
        ## numeric value representation
        self.numeric = numeric_val
        ## complex value (list of sub-responses)
        self.complex = complex_val
        

# #############################################################################
# Diag: Parameter Name Container
# #############################################################################
class DiagParameterName(str):
    """ Container for diagnostic response name that may contain sub-parameter
        names for "complex parameters"
    """
    # #########################################################################
    def __new__(cls, name, *args, **kwargs): # @UnusedVariable *args, **kwargs (see __init__)
        """ Create a custom instance of the immutable str type.
            Parameters:
                name - name of parameter, see __init__
        """
        return str.__new__(cls, name)
    
    # #########################################################################
    def __init__(self, name, sub_names=None): # @UnusedVariable name (see __new__)
        """ Create a new diagnostics parameter name that may have sub-parameter
            names. See CANapeDiag.sendSymbolicRequest.
            
            Note. 
                For "normal" (non-complex) parameters, a name as string 
                will usually suffice.
            
            Parameters: 
                name      - name of the parameter
                sub_names - for complex parameters: a list of sub-parameter
                            names (i.e. for sub-parameters contained in this 
                            complex parameter)
            
            Example:
                param = DiagParameterName(
                    name      = "main_parameter_name",
                    sub_names = ["sub_param_name_1", "sub_param_name_2"]
                )
        """
        if sub_names is None:
            sub_names = []
        ## list of sub-parameter names
        self.sub_names = sub_names
        

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    
    print "# CANapeError #####################################################"
    e = CANapeError("fnord")
    print "direct: ", e
    print "repr:   ", repr(e)
    print "str:    ", str(e)
    print "message:", e.message
    
    for container in (DEV, REPR, VALUE_TYPE, DATA_TYPE, DRIVER, TYPE_SWITCH,
                      MEASUREMENT_STATE, DIAG_SERVICE, DIAG_PARAM_TYPE):
        container.printDefinedValues()
    
# @endcond DOXYGEN_IGNORE
# #############################################################################
