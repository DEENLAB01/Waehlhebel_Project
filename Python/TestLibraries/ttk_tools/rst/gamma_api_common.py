#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : gamma_api_common.py
# Package : ttk_tools.rst
# Task    : Common shared definitions and error classes for gamma_api
# Type    : Implementation
# Python  : 2.7
#
# Author  : J.Tremmel
# Date    : 15.08.2016
# Copyright 2016 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 15.08.2016 | J.Tremmel | initial, moved "constants" and error classes
#                               | to a separate module
# 1.1  | 18.10.2016 | J.Tremmel | switched to EnumInfo for enum-like value containers
# 1.2  | 10.02.2017 | J.Tremmel | added DAQ exceptions and state machine states
#******************************************************************************
"""
@package ttk_tools.rst.gamma_api_common
Common shared definitions and error classes for gamma_api.
"""
from ttk_base.errors    import TTkException
from ttk_base.baseutils import EnumInfo


# #############################################################################
# Error handling 
# #############################################################################
class GammaError(TTkException):
    """ Base Error for GammaV connection """ 


class GammaDaqError(GammaError):
    """ Base Error for GammaV DAQ / data logger functionality """ 


class GammaDaqStateError(GammaDaqError):
    """ Gamma V DAQ state machine did not reach the expected state """ 


# #############################################################################
# Defines / Constants / Defaults
# #############################################################################

## default name for log files
DEFAULT_LOGFILE_NAME = "Gamma_Logfile.txt"

## default listen port of the gamma service (see gamma service configuration file)
DEFAULT_LISTEN_PORT = 0

## default timeout in [ms] to wait for the gamma service during attach
DEFAULT_ATTACH_TIMEOUT = 5000


# #############################################################################
class MESSAGE_MODE(EnumInfo):
    """ Message modes """
    CONSOLE        = 0
    FILE           = 1
    SYSLOG         = 2
    CONSOLE_FILE   = 3
    CONSOLE_SYSLOG = 4
    
    __info_mapping__ = {
        CONSOLE:        'console',
        FILE:           'file',
        SYSLOG:         'syslog',
        CONSOLE_FILE:   'console and file',
        CONSOLE_SYSLOG: 'console and syslog',
    }


# #############################################################################
class LOG_LEVEL(EnumInfo):
    """ Log levels """
    ERROR = 1
    WARN  = 2
    INFO  = 3
    
    __info_mapping__ = {
        ERROR:  'error',
        WARN:   'warning',
        INFO:   'info',
    }


# #############################################################################
class DaqMeasurementStatus(EnumInfo):
    """ State machine states for daq task """
    M_INIT                          = 0  # --
    M_WAITING_FOR_CONFIG            = 1  # Loggerstatus: M_WAITING_FOR_CONFIG
    M_CREATE_THREAD_GET_CONFIG      = 2  # Loggerstatus: M_CREATE_THREAD_GET_CONFIG
    M_WAITING_FOR_CONFIGDATA        = 3  # Loggerstatus: M_WAITING_FOR_CONFIGDATA
    M_CREATE_THREAD_VALIDATE_CONFIG = 4  # Loggerstatus: M_CREATE_THREAD_VALIDATE_CONFIG
    M_SETUP_CONFIGURATION           = 5  # Loggerstatus: M_SETUP_CONFIGURATION
    M_WAITING_FOR_RUN_INFO          = 6  # --
    M_WAITING_FOR_RUN               = 7  # Loggerstatus: M_WAITING_FOR_RUN
    M_RUNNING_INFO                  = 8  # --
    M_RUNNING                       = 9  # Loggerstatus: M_RUNNING
    M_RUNNING_STOPPED_INFO          = 10 # --
    M_RUNNING_STOPPED               = 11 # Loggerstatus: M_RUNNING_STOPPED
    M_DEINIT                        = 12 # Loggerstatus: M_DEINIT


# #############################################################################
# @cond DOXYGEN_IGNORE 
# #############################################################################
if __name__ == '__main__':  # pragma: no cover (contains only sample code)
    
    MESSAGE_MODE.printDefinedValues()  
    LOG_LEVEL.printDefinedValues()
    
    DaqMeasurementStatus.printDefinedValues()
    
# @endcond DOXYGEN_IGNORE
# #############################################################################
