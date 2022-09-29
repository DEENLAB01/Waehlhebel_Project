#******************************************************************************
# -*- coding: latin-1 -*-
# File    : win32_utils.py
# Task    : Utility functions for use on Windows systems (interface to _win32_utils)
# 
# Type    : Interface
# Python  : 2.5+
# 
# Copyright 2010 - 2018  iSyst Intelligente Systeme GmbH
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev.| Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0 | 26.06.2010 | J.Tremmel | initial
# 1.1 | 24.08.2011 | J.Tremmel | renamed registry_utils => canape_utils,
#                              | moved other utility functions to here
# 1.2 | 30.07.2012 | J.Tremmel | docstring cleanup
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2.0 | 08.04.2016 | J.Tremmel | refactored from canape_utils v1.2, moved 
#                              | generic functions to this module
# 2.1 | 11.04.2016 | J.Tremmel | tweaked docstrings and samples in __main__
# 2.2 | 02.08.2016 | J.Tremmel | split into base and interface implementations
# 2.3 | 29.08.2017 | J.Tremmel | added disableAppCrashDialog
# 2.4 | 14.08.2018 | J.Tremmel | added support for alternate registry views (32/64-bits)
#******************************************************************************
""" 
@package ttk_tools.win32_utils
Interface wrapper for Windows systems utility functions, see ttk_tools._win32_utils.
"""
import _win32_utils


# #############################################################################
def disableAppCrashDialog():
    """ Disable displaying of application/program crash dialog for the current
        process ("XYZ has stopped working" / "XYZ funktioniert nicht mehr").
        
        This tells Windows Error Reporting to skip displaying the dialog.
        See `SEM_NOGPFAULTERRORBOX`.
    """
    # see "Disabling the program crash dialog"
    # https://blogs.msdn.microsoft.com/oldnewthing/20040727-00/?p=38323/
    _win32_utils.disableAppCrashDialog()
    

# ############################################################################
def waitPumpMessages(delay):
    """ Wait for (approximately) delay [s] and pump windows messages/events  
        while waiting, which is a "good thing" to do if a COM connection is 
        active in the current process/thread.
        
        Note:
            The wait time is rather approximate, and may be quite a bit longer
            (like about +500ms on occasion) if the system is busy and lots of 
            events are fired.  
            The usable resolution appears to be about 200ms.
        
        Parameters:
            delay   -   wait delay in seconds
        
    """
    _win32_utils.waitPumpMessages(delay)
    

# #############################################################################
def getRegPath(path, name, wow64_32_key=None, verbosity=1):
    """ Get a value from an entry in the windows registry.
        
        Parameters: 
            path         - a registry path starting with one of the HKEY entries, e.g.  
                           "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft" or  
                           "HKLM\SOFTWARE\Microsoft" 
            
            name         - name of entry below path
            
            wow64_32_key - None:  use default key view depending on current bitness  
                           True:  access 32-bit keys from 32-bit and 64-bit applications  
                           False: access 64-bit keys from 32-bit and 64-bit applications  
            
            verbosity    - verbosity of error messages  
                           0: silent,  
                           1: print error to stdout,  
                           2: also print exception info  
        
        Note:
            Registry paths may start with both full or abbreviated HKEY values,
            e.g. 
                * `HKEY_LOCAL_MACHINE\...` or abbreviated `HKLM\...`
                * `HKEY_CLASSES_ROOT\... ` or abbreviated `HKCR\...`
                * `HKEY_CURRENT_USER\... ` or abbreviated `HKCU\...`
        
        Returns the contents of the specified key/name or None if access failed.
    """
    return _win32_utils.getRegPath(
        path = path, 
        name = name,
        wow64_32_key = wow64_32_key,
        verbosity = verbosity
    )
    

# #############################################################################
def setRegPath(path, name, value, value_type=None, wow64_32_key=None, verbosity=1):
    """ Set a value to an entry in the windows registry.
        
        Parameters: 
            path         - a registry path starting with one of the HKEY entries,
                           e.g. "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft" or  
                           "HKLM\SOFTWARE\Microsoft". See note at getRegPath().
            name         - name of entry below path
            value        - value to set
            value_type   - type of value to set, should be one of the defined
                           `_winreg.REG_*` values or None to "auto detect": 
                           * string values  => `REG_SZ`  
                           * integer values => `REG_DWORD` (note: max 32 bit)  
                           * float values   => `REG_DWORD` (will be rounded towards the nearest integer)  
            
            wow64_32_key - None:  use default key view depending on current bitness  
                           True:  access 32-bit keys from 32-bit and 64-bit applications  
                           False: access 64-bit keys from 32-bit and 64-bit applications  
            
            verbosity    - verbosity of error messages  
                           0: silent,  
                           1: print error to stdout,  
                           2: also print exception info
        
        Returns True if value was set, otherwise False.
    """
    return _win32_utils.setRegPath(
        path  = path, 
        name  = name,
        value = value,
        value_type   = value_type, 
        wow64_32_key = wow64_32_key,
        verbosity    = verbosity
    )
    

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    
    print "# waitPumpMessages ################################################"
    print "Waiting (while pumping messages)...",
    waitPumpMessages(0.5)
    print "...done."
    
    print
    print "# getRegPath ######################################################"
    path = r"HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\iTestStudio TA" 
    name = "DisplayName"
    
    print "# iTS (32-bit registry view)"
    print "%s: %s"%(name, getRegPath(path, name, wow64_32_key=True))
    print "# iTS (64-bit registry view)"
    print "%s: %s"%(name, getRegPath(path, name, wow64_32_key=False))
    print "# iTS (auto)"
    print "%s: %s"%(name, getRegPath(path, name))
    
    print
    print "# setRegPath ######################################################"
    path = r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Taskband" 
    # "Taskband" info is in a shared registry key (same for both 32-bit and 64-bit registry views)
    name = "NumThumbnails"
    print "Taskband %s: %s"%(name, getRegPath(path, name))
    prev_value = getRegPath(path, name)
    if prev_value is not None:
        print "changing value..."
        setRegPath(path, name, 6)
        print "Taskband %s: %s"%(name, getRegPath(path, name))
        print "resetting value..."
        setRegPath(path, name, prev_value)
        print "Taskband %s: %s"%(name, getRegPath(path, name))
        
    
    print "# getRegPath ######################################################"
    CANAPE_REG_KEY = r"HKEY_LOCAL_MACHINE\SOFTWARE\VECTOR\CANape"
    name = "Path160"
    print "# default"
    print getRegPath(CANAPE_REG_KEY, name, wow64_32_key=None, verbosity=1)
    print "# 64"
    print getRegPath(CANAPE_REG_KEY, name, wow64_32_key=False, verbosity=1)
    print "# 32"
    print getRegPath(CANAPE_REG_KEY, name, wow64_32_key=True, verbosity=1)
    
    
    
# @endcond DOXYGEN_IGNORE
# #############################################################################
