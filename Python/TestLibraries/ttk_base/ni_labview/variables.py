#******************************************************************************
# -*- coding: latin-1 -*-
# File    : variables.py
# Package : ttk_base.ni_labview
# Task    : Wrapper classes for hil variables using an interface to NI LabView 
# Type    : Interface
#
# Author  : J.Tremmel
# Date    : 18.12.2019
# Copyright 2019 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 18.12.2019 | J.Tremmel | initial
#******************************************************************************
"""
@package ttk_base.ni_labview.variables
Wrapper classes for hil variables using an interface to NI LabView to provide a
unified interface and containers to group variables into sets.

This serves as "interface" to the precompiled module in delivery to permit 
better code-analysis and code-completion in PyDev.
"""
from ttk_base.ni_labview import _variables


# #############################################################################
class Var(_variables.Var):
    """ Simple wrapper for NI LabView "HIL" variables/controls.  
        Uses a ttk_tools.ni.labview.LabView instance for variable access via COM.
    """
    # #########################################################################
    def __init__(self, context, identifier, unit="", alias="", descr="", 
                 lookup=None, default=None, resettable=True, fmt=None):
        """ Parameters:
                context     - parent context (here: a LabView instance) 
                identifier  - variable identifier: "vi_name.vi/variable_name"
                unit        - (optional) unit string for the variable
                alias       - (optional) alias name, defaults to last (non-
                              default) entry in the identifier model path
                descr       - description for the variable
                lookup      - lookup dictionary for states {value => "state name"}
                default     - manually defined default value for the variable.
                              Will be used as "reset" value instead of the 
                              original value before the first set operation 
                              if set to anything but None.
                resettable  - enable/disable reset() for this variable. If set
                              to False, a call to reset() will be ignored.
                fmt         - format string or keyword to use for value 
                              representation, e.g. "%.2f" or "hex"
        """
        _variables.Var.__init__(
            self, context, identifier, 
            unit=unit, alias=alias, descr=descr, 
            lookup=lookup, default=default, 
            resettable=resettable, fmt=fmt
        )
    
    # #########################################################################
    def get(self, *args, **kwargs):
        """ Get the current value of the VI control / variable.
            
            Returns the current value.
        """
        return _variables.Var.get(self, *args, **kwargs)
    
    # #########################################################################
    def set(self, value, *args, **kwargs):
        """ Set a value to the VI control / variable.
            
            Parameters:
                value - value to set
            
            Returns the original value before the set operation occurred.
        """
        return _variables.Var.set(self, value, *args, **kwargs)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the variable's current data. This uses 
            the lookup values supplied in constructor.
            
            Returns a textual state description (if available) or the unmapped 
            value (if no matching state was found).
        """
        return _variables.Var.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the variable. This uses the lookup values 
            supplied in constructor.
            Fallback (if no matching state text was found) will be the
            unmapped input state.
            
            Parameters:
                state - named state to set
            
            Returns the previously set state (if possible, otherwise the 
            previous unmapped value, see getState)
        """
        return _variables.Var.setState(self, state)
        
    # #########################################################################
    def reset(self, verbosity=1):
        """ Reset the variable to its initial value (default value specified
            in constructor or value before the first set() call).
            
            Parameters:
                verbosity - verbosity of log output.  
                            0: silent,   
                            1: show calls to non-resettable variables  
                            2: show all reset calls  
            
            Returns the original value (which may be None if the variable has
            not been set before)
        """
        return _variables.Var.reset(self, verbosity)
    
    # #########################################################################
    def info(self):
        """ Get an info string for this variable (alias and current value plus 
            unit and lookup value, if available). 
            
            Example:
                >>> print voltage_var.info()
                Var Name: 12 V
                >>> print status_var.info()
                Status Var Name: 1 (valid)
                
            Returns a formatted string.
        """
        return _variables.Var.info(self)


# #############################################################################
# Container
# #############################################################################
class VarContainer(_variables.VarContainer):
    """ Base class for LabView "HIL" variable containers. """
    
    # #########################################################################
    def __init__(self, lv):
        """ Parameters:
                lv  -  a ttk_tools.ni.labview.LabView instance connected
                       to a suitable COM server "LabView App"
        """
        _variables.VarContainer.__init__(self, lv)
    
    # #########################################################################
    def resetAll(self, verbosity=1, recursion_depth=4):
        """ Call reset() on all contained variables that support it. 
            
            Info:
                Variables will be reset in an arbitrary order (first found, 
                first reset).  
                It might therefore be preferable to mark all variables used in 
                DUT's startup/shutdown sequences (like power supply settings, 
                KL30, KL15, ...) as not "resettable" in order to get a more
                predictable behavior. 
            
            Parameters:
                verbosity       - verbosity of debug/log messages.  
                                    0: silent,  
                                    1: plain info,  
                                    2: +var names,  
                                    3: overkill
                    
                recursion_depth - how "deep" to recurse into lists/dictionary
                                  structures when looking for variables to 
                                  reset. 
        """
        _variables.VarContainer.resetAll(
            self, verbosity=verbosity, recursion_depth=recursion_depth
        )


# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    pass
# @endcond DOXYGEN_IGNORE #####################################################