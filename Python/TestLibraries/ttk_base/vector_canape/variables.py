#******************************************************************************
# -*- coding: latin-1 -*-
# File    : variables.py
# Package : ttk_base.vector_canape
# Task    : Wrapper classes for cal variables using Vector CANape.
#           This serves as "interface" to precompiled modules in delivery 
#           to enable code-completion in PyDev.
# Type    : Interface
#
# Author  : J.Tremmel 
# Date    : 14.01.2016
# Copyright 2016 iSyst Intelligente Systeme GmbH
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Author    | Description
#------------------------------------------------------------------------------
# 1.0  | 14.01.2016 | J.Tremmel | initial, refactored from variables_base v1.8
# 1.1  | 29.09.2016 | J.Tremmel | support for custom value representations
#******************************************************************************
"""
@package ttk_base.vector_canape.variables
Wrapper classes for Vector CANape cal variables to provide a unified 
interface and containers to group variables into sets.

This serves as "interface" to the precompiled module in delivery to permit 
better code-analysis and code-completion in PyDev.
"""
import _variables


# #############################################################################
# CANape-Var ("CalVar") - Calibration Variables (and parameters)
# #############################################################################
class Var(_variables.Var):
    """ Simple wrapper for Vector CANape calibration variables. 
        Uses ttk_tools.vector_canape.canapeapi for accessing CANape application.
    """
    # #########################################################################
    def __init__(self, context, identifier, unit="", alias="", descr="", 
                 lookup=None, default=None, resettable=True, fmt=None, raw_mode=False):
        """ CANape-CAL-Variable initialization.
            
            Parameters:
                context     - parent context that handles tool references
                              This is usually a reference to a variables container
                              for CANape "Cal"-Vars
                              See ttk_base.vector_canape.variables.VarContainer
                identifier  - variable identifier/name in the calibration tool
                unit        - (optional) unit string for the variable
                alias       - (optional) alias name, defaults to varname
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
                raw_mode    - True:  use raw/internal representation of values
                              False: use physical representation of values (default)
        """
        _variables.Var.__init__(
            self, context, identifier, 
            unit=unit, alias=alias, descr=descr, 
            lookup=lookup, default=default, 
            resettable=resettable, fmt=fmt,
            raw_mode=raw_mode
        )
    
    # #########################################################################
    def get(self, *args, **kwargs):
        """ Get the current value of the calibration variable. 
            
            Note: 
                Any specified parameters will be handed on to the underlying 
                 "read" operation, which may or may not be able to handle 
                 them. Use with care and only in very special cases.
                 
            Returns the current value.
        """
        return _variables.Var.get(self, *args, **kwargs)
    
    # #########################################################################
    def set(self, value, *args, **kwargs):
        """ Set a value to the calibration variable. 
            
            Parameters:
                value - value to set
            
            Note: Any additional parameters will be handed on to the underlying 
                  cal-tool "write" operation, which may or may not be able to 
                  handle them. Use with care and only in very special cases.
            
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
            supplied in constructor. Fallback (if no matching state text was 
            found) will be the unmapped input state.
            
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
                verbosity - verbosity of log output,   
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
                Cal-Var Name: 12 V
                >>> print status_var.info()
                Status Var Name: 1 (valid)
                
            Returns a formatted string.
        """
        return _variables.Var.info(self)


# #############################################################################
# Container
# #############################################################################
class VarContainer(_variables.VarContainer):
    """ Base class for CalVar containers. """
    # #########################################################################
    def __init__(self, tool_ref=None):
        """ Parameters:
                tool_ref  -  calibration tool reference, see setToolRef
        """
        _variables.VarContainer.__init__(self, tool_ref)
        
    # #########################################################################
    def setToolRef(self, tool_ref):
        """ Set a calibration tool reference for cal var access."""
        return _variables.VarContainer.setToolRef(self, tool_ref)
    
    # #########################################################################   
    def resetAll(self, verbosity=1, recursion_depth=4):
        """ Call reset() on all contained variables that support it. 
            
            Info:
                Variables will be reset in an arbitrary order (first found, 
                first reset).
            
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