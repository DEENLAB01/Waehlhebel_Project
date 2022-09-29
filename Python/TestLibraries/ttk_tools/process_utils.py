#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : process_utils.py
# Task    : Utilities for handling win32 (and x64) processes.
#           Interface to _process_utils.
#
# Type    : Interface
# Python  : 2.5+
#
# Copyright 2009 - 2015 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0 | 05.02.2009 | J.Tremmel | initial
# 1.1 | 16.02.2009 | J.Tremmel | added further descriptions
# 1.2 | 28.07.2009 | J.Tremmel | added getCurrentProcessNames and isProcessActive
# 1.3 | 11.03.2010 | J.Tremmel | cleanup for static code analysis
# 1.4 | 30.07.2012 | J.Tremmel | Docstring cleanup
# 1.5 | 19.11.2014 | J.Tremmel | increased buffer for getCurrentPIDs()
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2.0 | 20.11.2014 | J.Tremmel | support for 64bit processes (and unicode process names)
# 2.1 | 18.12.2015 | J.Tremmel | split into interface and base implementation
#******************************************************************************
"""
@package ttk_tools.process_utils
Interface to utilities for handling win32 (and x64) processes in 
ttk_tools._process_utils.

It appears that "handling" processes mostly seems to boil down to "killing" 
them, though.
"""
__ALL__ = [
    "killProcess",
    "getCurrentPIDs",
    "getCurrentProcessNames",
    "getCurrentProcessPaths",
    "isProcessActive",
]
import _process_utils # base implementation


# #############################################################################
def killProcess(target_names, verbosity=1):
    """ Kill all processes that match the given target_name(s) (using kernel32).
        Note that target may be a single name or list of names.
        
        Parameters: 
            target_names  -  a single name or a list of names of processes
                             to be killed. If a process name contains unicode
                             characters, it should be supplied as unicode string.
            verbosity     -  verbosity of status output  
                             0: (mostly) silent  
                             1: show names/pids  of killed processes  
                             2: also show process access warnings
        
        Returns the number of killed processes.
    """
    return _process_utils.killProcess(
        target_names = target_names, 
        verbosity    = verbosity
    )


# #############################################################################
def getCurrentProcessNames(normalize_case=True):
    """ Get image names of currently active processes (that is, the executable 
        file names).
        
        Parameters: 
            normalize_case - cast process names to lowercase (as windows is
                             not case sensitive); defaults to True
        
        Returns a dictionary `{<process_name>: <number of active processes>, ...}`
    """
    return _process_utils.getCurrentProcessNames(
        normalize_case = normalize_case
    )
    

# #############################################################################
def getCurrentProcessPaths(normalize_case=True, file_names_only=False):
    """ Get image names/paths of currently active processes (that is, names
        or paths of the executable files).
        
        Info: Limitation: 
            The used `QueryFullProcessImageName` is only supported since 
            Windows Vista
        
        Parameters: 
            normalize_case  - cast process names/paths to lowercase (as windows
                              is not case sensitive); defaults to True
            file_names_only - True:  return only base names (e.g. "notepad.exe")  
                              False: return full file paths
        
        Returns a dictionary `{<process name or path>: <number of active processes>, ...}`
    """
    return _process_utils.getCurrentProcessPaths(
        normalize_case  = normalize_case, 
        file_names_only = file_names_only
    )
    

# #############################################################################
def isProcessActive(process_name, ignore_case=True):
    """ Check whether at least one process using the supplied executable name
        is currently running.
        
        Parameters: 
            process_name - name of process to check
            ignore_case  - True: ignore case of process_name
        
        Returns True if a matching process is running, otherwise False.
    """
    return _process_utils.isProcessActive(
        process_name = process_name, 
        ignore_case  = ignore_case
    )
    

# #############################################################################
def killProcess2(image_name):
    """ Kill all processes that match the given image_name using the windows
       "taskkill" command running in a sub process.
        
        Parameters: 
            image_name  -  the name of the process to be killed
        
    """
    _process_utils.killProcess2(image_name=image_name)


# #############################################################################
def getCurrentPIDs():
    """ Get a list of PIDs of running processes, similar to the output of
        win32process.EnumProcesses() (which is available in later Python versions).
        
        Returns a list of PID values.
    """
    return _process_utils.getCurrentPIDs()
    

# #############################################################################
def killByPID(pid):
    """ Kill the process with the supplied ID (as long as the user has 
        sufficient access rights).
        
        Parameters: 
            pid -  process ID of the process to be killed
        
        Returns the return status of `TerminateProcess` (non-zero on success)
    """
    return _process_utils.killByPID(pid = pid)
    

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    import time
    print("# Active Processes ###############################################")
    procs = getCurrentProcessNames()
    #procs = getCurrentProcessPaths()
    width = max(len(entry) for entry in procs.keys())
    for name, number in sorted(procs.iteritems()):
        print "  %-*s => %d instance%s active"%(width, name, number, ('s', '')[number == 1])
    print
     
    process_name = 'Calc.exe'
    #process_name = 'BäreGrëp.exe' # baregrep.exe renamed for checks with unicode names
    #process_name = 'baregrep.exe'
    print "isProcessActive:", process_name, "=>", isProcessActive(process_name)
    killProcess(process_name)
    # wait a bit for process to fully "die" (or it might still twitch a bit and appear as "active")
    time.sleep(.250)
    print "isProcessActive:", process_name, "=>", isProcessActive(process_name)
    
    
# @endcond DOXYGEN_IGNORE
# #############################################################################
