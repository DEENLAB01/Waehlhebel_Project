#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : vflash_api_common.py
# Package : ttk_tools.vector
# Task    : Common definitions, utility functions and classes for vFlash API access. 
# Type    : Implementation
# Python  : 2.5+
#
# Copyright 2017 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 05.05.2017 | P. Wunner  | initial
# 1.1  | 02.05.2018 | J.Tremmel  | VFlashResultError now derived from VFlashError
# 1.2  | 09.05.2018 | J.Tremmel  | refactoring and cleanup, added a few more
#                                | status values from VFlashAutomationTypes.h
# 1.3  | 20.04.2020 | J.Tremmel  | status now gets decoded in VFlashResultError,
#                                | not in VFlashError; removed MAX_LEN_ERROR_TEXT
#******************************************************************************
""" 
@package ttk_tools.vector.vflash_api_common
Common definitions, utility functions and classes for vFlash API access. 
"""
from ttk_base.errors    import TTkException
from ttk_base.baseutils import EnumInfo


# #############################################################################
# Error handling 
# #############################################################################
class VFlashError(TTkException):
    """ Base Error for vFlash API """
    

class VFlashDLLError(VFlashError):
    """ DLL access failed """
    

class VFlashResultError(VFlashError):
    """ Flashing ended with an error state """ 
    def __init__(self, flash_result, last_error):
        VFlashError.__init__(
            self, 
            "vFlash: Error - aborting (Code %i, %s)\n"
            "        vFlash error message: %s"%(
                flash_result, 
                VFlashResult.getInfo(flash_result),
                last_error
        ))

# TODO:  Maybe add a VFlashStatusError, just for symmetry? -JT 2018-05-07


# #############################################################################
# Defines / Constants / Defaults
# #############################################################################

## timeout for flash process in [s]
FLASH_TIMEOUT = 2000


# #############################################################################
class VFlashStatus(EnumInfo):
    """ Flash programming status values. """
    FS_SUCCESS =                                     0
    FS_LICENSE_IS_NOT_AVAILABLE =                    9
    
    FS_ABORTED =                                    10
    FS_UNKNOWN_ERROR =                              11
    FS_PROCESSING_FLASHWARE_FAILED =                15
    FS_INITIALIZING_COMMUNICATION_FAILED =          16
    FS_STOP_REPROGRAMMING_FAILED =                  17
    FS_PROJECT_DATA_INVALID =                       18
    FS_INITIALIZING_FLASH_LIBRARY_FAILED =          19
    FS_SCRIPT_VERSION_MISMATCH =                    20
    FS_LOADING_PROJECT_FAILED =                     21
    FS_FLASHWARE_CHANGED =                          22
    FS_READING_EXPECTED_IDENTS_FAILED =             23
    FS_FORCE_BOOT_MODE_FAILED =                     24
    FS_SWITCH_BAUD_RATE_FAILED =                    25
    FS_SEND_WAKEUP_PATTERN_FAILED =                 26
    
    FS_GENERAL_SCRIPT_FAILURE =                     40
    FS_SEED_KEY_HANDLING_FAILED =                   41
    FS_SECURITY_ACCESS_FAILED =                     42
    FS_COMMUNICATION_FAILED =                       43
    FS_DIAGNOSTIC_TRANSACTION_FAILED =              44
    FS_SOFTWARE_INTEGRITY_CHECK_FAILED =            45
    FS_NEGATIVE_RESPONSE_RECEIVED =                 46
    FS_ERASE_MEMORY_FAILED =                        47
    FS_SOFTWARE_AUTHENTICITY_CHECK_FAILED =         48
    FS_SOFTWARE_COMPATIBILITY_CHECK_FAILED =        49
    FS_FINGERPRINT_CHECK_FAILED =                   50
    FS_HARDWARE_COMPATIBILITY_CHECK_FAILED =        51
    FS_PROGRAMMING_PRECONDITIONS_CHECK_FAILED =     52
    FS_INVALID_PARAMETER_DETECTED =                 53
    
    FS_GENERAL_CUSTOM_ACTION_FAILURE =              60
    FS_CUSTOM_ACTION_ATTRIBUTE_CONVERSION_FAILED =  61
    
    __info_mapping__ = {
        FS_SUCCESS:                                "FS_Success, reprogramming successful",
        FS_LICENSE_IS_NOT_AVAILABLE:               "License is not available",
        FS_ABORTED:                                "FS_Aborted",
        FS_UNKNOWN_ERROR:                          "FS_UnknownError",
        FS_PROCESSING_FLASHWARE_FAILED:            "FS_ProcessingFlashwareFailed, Intel-hex, Motorola-S files cannot be processed",
        FS_INITIALIZING_COMMUNICATION_FAILED:      "FS_InitializingCommunicationFailed",
        FS_STOP_REPROGRAMMING_FAILED:              "FS_StopReprogrammingFailed",
        FS_PROJECT_DATA_INVALID:                   "FS_ProjectDataInvalid",
        FS_INITIALIZING_FLASH_LIBRARY_FAILED:      "FS_InitializingFlashLibraryFailed",
        FS_SCRIPT_VERSION_MISMATCH:                "FS_ScriptVersionMismatch",
        FS_LOADING_PROJECT_FAILED:                 "FS_LoadingProjectFailed",
        FS_FLASHWARE_CHANGED:                      "FS_FlashwareChanged",
        FS_READING_EXPECTED_IDENTS_FAILED:         "FS_ReadingExpectedIdentsFailed",
        FS_FORCE_BOOT_MODE_FAILED:                 "FS_ForceBootModeFailed",
        FS_SWITCH_BAUD_RATE_FAILED:                "FS_SwitchBaudrateFailed",
        FS_SEND_WAKEUP_PATTERN_FAILED:             "FS_SendWakeUpPatternFailed",
        FS_GENERAL_SCRIPT_FAILURE:                 "FS_GeneralScriptFailure",
        FS_SEED_KEY_HANDLING_FAILED:               "FS_SeedKeyHandlingFailed",
        FS_SECURITY_ACCESS_FAILED:                 "FS_SecurityAccessFailed",
        FS_COMMUNICATION_FAILED:                   "FS_CommunicationFailed",
        FS_DIAGNOSTIC_TRANSACTION_FAILED:          "FS_DiagnosticTransactionFailed",
        FS_SOFTWARE_INTEGRITY_CHECK_FAILED:        "FS_SoftwareIntegrityCheckFailed",
        FS_NEGATIVE_RESPONSE_RECEIVED:             "FS_NegativeResponseReceived",
        FS_ERASE_MEMORY_FAILED:                    "FS_EraseMemoryFailed",
        FS_SOFTWARE_AUTHENTICITY_CHECK_FAILED:     "FS_SoftwareAuthenticityCheckFailed",
        FS_SOFTWARE_COMPATIBILITY_CHECK_FAILED:    "FS_SoftwareCompatibilityCheckFailed",
        FS_FINGERPRINT_CHECK_FAILED:               "FS_FingerprintCheckFailed",
        FS_HARDWARE_COMPATIBILITY_CHECK_FAILED:    "FS_HardwareCompatibilityCheckFailed",
        # Preconditions are not fulfilled, e.g. user tried to reprogram an engine ECU while the engine is running 
        FS_PROGRAMMING_PRECONDITIONS_CHECK_FAILED: "FS_ProgrammingPreconditionsCheckFailed",
        # Value of a FlashAttribute is missing or invalid 
        FS_INVALID_PARAMETER_DETECTED:             "FS_InvalidParameterDetected",
        
        FS_GENERAL_CUSTOM_ACTION_FAILURE:             "FS_GeneralCustomActionFailure",
        FS_CUSTOM_ACTION_ATTRIBUTE_CONVERSION_FAILED: "FS_CustomActionAttributeConversionFailed",
        
    }


# #############################################################################
class VFlashResult(EnumInfo):
    """ Flash programming result values. """
    FR_SUCCESS =                       0
    
    FR_INITIALIZATION_ERROR =         10
    FR_DEINITIALIZATION_ERROR =       11
    FR_INVALID_PROJECT_HANDLE =       12
    FR_INVALID_LICENSE =              13
    
    FR_STOP_FAILED =                  20
    FR_PROJECT_IN_PROCESSING =        21
    
    FR_NO_PROJECT_LOADED =            30
    FR_PROJECT_PATH_INVALID =         31
    FR_INCONSISTENT_PROJECT =         32
    FR_INVALID_CALLBACKS =            33
    FR_PROCESSING_FLASHWARE_ERROR =   34
    FR_CHANNEL_ALREADY_IN_USE =       35
    FR_NETWORK_ACTIVATION_FAILED =    36
    
    FR_NO_CAN_DRIVER_AVAILABLE =      40
    
    FR_INVALID_COMMAND_ORDER =        50
    FR_FILE_NOT_FOUND =               51
    FR_PROJECT_LOAD_FAILED =          52
    FR_PROJECT_UNLOAD_FAILED =        53
    FR_MAX_PROJECT_NUMBER_EXCEEDED =  54
    
    FR_UNKNOWN_ERROR =               100
    
    __info_mapping__ = {
        FR_SUCCESS:                     "FR_Success",
        
        FR_INITIALIZATION_ERROR:        "FR_InitializationError",
        FR_DEINITIALIZATION_ERROR:      "FR_DeinitializationError",
        FR_INVALID_PROJECT_HANDLE:      "FR_InvalidProjectHandle",
        FR_INVALID_LICENSE:             "FR_InvalidLicense",
        FR_STOP_FAILED:                 "FR_StopFailed",
        FR_PROJECT_IN_PROCESSING:       "FR_ProjectInProcessing",
        FR_NO_PROJECT_LOADED:           "FR_NoProjectLoaded",
        FR_PROJECT_PATH_INVALID:        "FR_ProjectPathInvalid",
        FR_INCONSISTENT_PROJECT:        "FR_InconsistentProject",
        FR_INVALID_CALLBACKS:           "FR_InvalidCallbacks",
        FR_PROCESSING_FLASHWARE_ERROR:  "FR_ProcessingFlashwareError",
        FR_CHANNEL_ALREADY_IN_USE:      "FR_ChannelAlreadyInUse",
        FR_NETWORK_ACTIVATION_FAILED:   "FR_NetworkActivationFailed",
        FR_NO_CAN_DRIVER_AVAILABLE:     "FR_NoCanDriverAvailable",
        FR_INVALID_COMMAND_ORDER:       "FR_InvalidCommandOrder",
        FR_FILE_NOT_FOUND:              "FR_FileNotFound",
        FR_PROJECT_LOAD_FAILED:         "FR_ProjectLoadFailed",
        FR_PROJECT_UNLOAD_FAILED:       "FR_ProjectUnloadFailed",
        FR_MAX_PROJECT_NUMBER_EXCEEDED: "FR_MaxProjectNumberExceeded",
        FR_UNKNOWN_ERROR:               "FR_UnknownError",
    }


# #############################################################################
# @cond DOXYGEN_IGNORE 
# #############################################################################
if __name__ == '__main__':  # pragma: no cover (contains only sample code)
    
    VFlashStatus.printDefinedValues()  
    VFlashResult.printDefinedValues()
    
# @endcond DOXYGEN_IGNORE
# #############################################################################