#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : bus_signals_base.py
# Package : ttk_bus
# Task    : Wrapper classes for bus/interface signal descriptions.
#           This serves as "interface" to the precompiled module in delivery 
#           to enable code-completion in PyDev
# Python  : 2.5+
# Type    : Interface
#
# Copyright 2012 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Author    | Description
#------------------------------------------------------------------------------
# 1.0  | 19.07.2012 | J.Tremmel | initial
# 1.1  | 29.08.2012 | J.Tremmel | added get/set to BusSignal, some cleanup for doxygen 
# 1.2  | 05.10.2012 | J.Tremmel | added getState/setState to wrapper
# 1.3  | 03.05.2013 | J.Tremmel | added CRC/AC signal classes
# 1.4  | 12.07.2013 | J.Tremmel | added CrcBusSignalIOUserCustom
# 1.5  | 21.10.2014 | J.Tremmel | cleanup, removed obsolete bindings
# 1.6  | 16.12.2015 | J.Tremmel | tweaks for consistency with _bus_signals_base v1.10
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2.0  | 26.04.2016 | J.Tremmel | added support for different "HilVar" flavors,
#                               | removed obsolete CrcBusSignalIOUserCustom
# 2.1  | 25.11.2016 | J.Tremmel | updated interface methods, removed workaround 
#                               | for old "verbose" parameter in BusSignalContainer
# 2.2  | 29.08.2017 | J.Tremmel | added interface description for getStateDescr
# 2.3  | 28.02.2019 | J.Tremmel | updated for _bus_signals_base v2.8
# 2.4  | 13.03.2020 | J.Tremmel | updated for _bus_signals_base v2.9
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 3.0  | 15.07.2020 | J.Tremmel | removed obsolete signal parameters min/max_value
#******************************************************************************
"""
@package ttk_bus.bus_signals_base
Interface wrapper for bus/interface signal classes in ttk_bus._bus_signals_base.
This serves as "interface" to the precompiled module in delivery to enable 
code-completion in PyDev.

Convention:
    Signal directions are relative to the DUT:  
      * Tx - transmitted by ECU => received from HIL  
      * Rx - received by ECU <= transmitted from HIL  
    
"""
import _bus_signals_base
from _bus_signals_base import BusSignal # (base class, just for completeness)


# #############################################################################
class TxBusSignal(_bus_signals_base.TxBusSignal):
    """ A signal sent from the DUT to the test system (ECU Tx => HIL Rx). """
    
    # #########################################################################
    def __init__(self, context, identifier, 
                 cycle_time=0, debounce_time=0,
                 signal_var=None,
                 unit="", alias="", descr="", lookup=None,
                 change_delay=None, timeout=None, recovery_time=None):
        """ Bus signal initialization.
            
            Parameters:
                context       - parent context for instantiating HIL variables.
                                This gets mainly used in derived classes
                identifier    - base signal identifier/name/path in the HIL model
                                (typically this is read-only for Tx-signals and 
                                writable for Rx-signals).  
                                Derived classes typically use this identifier
                                as starting point for deriving additional helper
                                variables.
                
                cycle_time    - cycle time in [ms], 0 if event-triggered
                debounce_time - minimum debounce delay time between events in [ms]
                
                signal_var    - (opt) an already initialized instance of Var 
                                      (or most likely one of its derived classes) 
                                      for the main signal value.  
                                      If not supplied, a DummyVar will be used/
                                      created as fall back
                
                unit          - (opt) unit of physical signal value (as string,
                                      mainly used for report entries), 
                                      defaults to signal_var.unit.
                alias         - (opt) bus signal alias/name,  
                                      defaults to signal_var.unit.
                descr         - (opt) signal description (e.g. used in report entries)
                lookup        - (opt) a lookup-table for mapping discrete signal 
                                      states to textual descriptions,  
                                      defaults to signal_var.unit.
                
                change_delay  - (opt) delay to wait after a value change [ms], 
                                      defaults to 2x max(cycle_time, debounce_time)
                timeout       - (opt) detection time for timeout errors [ms], 
                                      defaults to 2x max(cycle_time, debounce_time)
                recovery_time - (opt) time for recovery/"wiedergut" checks [ms], 
                                      defaults to 2x max(cycle_time, debounce_time)
                
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class code cannot be analyzed.
        
        ## context for "HilVar" variables
        self.context = None
        ## Main bus signal variable on HIL-side.
        self.signal_var = None
        
        # #####################################################################
        _bus_signals_base.TxBusSignal.__init__(
            self, context, identifier, 
            cycle_time=cycle_time, debounce_time=debounce_time,
            unit=unit, alias=alias, descr=descr, lookup=lookup,
            signal_var=signal_var,
            change_delay=change_delay, timeout=timeout, 
            recovery_time=recovery_time
        )
    
    # #########################################################################
    # Basic methods inherited from  BusSignal
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. """
        return _bus_signals_base.TxBusSignal.info()
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable. 
            Returns the current value.
        """
        return _bus_signals_base.TxBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable. 
            Parameters:
                value - new value to set
            Returns the previous value.
        """
        return _bus_signals_base.TxBusSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data. 
            This uses the lookup values supplied in constructor.
            Fallback (if no matching state was found) will be the unmapped 
            numeric value.
            
            Returns the current state's description. 
        """
        return _bus_signals_base.TxBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor.
            
            Parameters:
                state - named state to set
            
            Returns the previous state's description.
        """
        return _bus_signals_base.TxBusSignal.setState(self, state)
    
    # #########################################################################
    def hasStateLookup(self):
        """ Return True if a state/value lookup table is defined for the HIL 
            signal variable. 
        """
        return _bus_signals_base.TxBusSignal.hasStateLookup(self)
    
    # #########################################################################
    def getStateDescr(self, value=None, fallback=None):
        """ Get a state description text for the given value from the HIL 
            signal variable's defined lookup table (if any).
            
            Parameters:
                value     - value for which to get a state description. 
                            If None, the last read value will be used instead.
                fallback  - fallback value to return if no match was found.
                            Default: None
            
            Returns the state text if a match was found, otherwise the specified
            fallback value.
        """
        return _bus_signals_base.TxBusSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def hasFormattedRepr(self):
        """ Return True if a formatting for value representation is defined
            for the HIL signal variable.
        """
        return _bus_signals_base.TxBusSignal.hasFormattedRepr(self)
    
    # #########################################################################
    def getFormattedValue(self, value=None):
        """ Get a formatted representation for the given value using the defined 
            format string of the the HIL signal variable. 
            An empty (or non-defined) format string will use the value's 
            default string representation.
            
            Parameters:
                value     - value for which to get a string representation.  
                            If None, the last value (read or written) will be 
                            used instead.
            
            Returns a formatted string representation. 
        """
        return _bus_signals_base.TxBusSignal.hasFormattedRepr(self, value)
    
    # #########################################################################
    def reset(self, *args, **kwargs): # @UnusedVariable *args, **kwargs (just to tolerate optional parameters)
        """ Call reset() on all contained variables/signals that support it."""
        _bus_signals_base.TxBusSignal.reset(self)
        

# #############################################################################
class RxBusSignal(_bus_signals_base.RxBusSignal):
    """ A signal sent from the test system to the DUT (ECU Rx <= HIL Tx). """
    
    # #########################################################################
    def __init__(self, context, identifier, 
                 cycle_time=0, debounce_time=0,
                 signal_var=None,
                 unit="", alias="", descr="", lookup=None,
                 change_delay=None, timeout=None, recovery_time=None):
        """ Bus signal initialization.
            
            Parameters:
                context       - parent context for instantiating HIL variables.
                                This gets mainly used in derived classes
                identifier    - base signal identifier/name/path in the HIL model
                                (typically this is read-only for Tx-signals and 
                                writable for Rx-signals).  
                                Derived classes typically use this identifier
                                as starting point for deriving additional helper
                                variables.
                
                cycle_time    - cycle time in [ms], 0 if event-triggered
                debounce_time - minimum debounce delay time between events in [ms]
                
                signal_var    - (opt) an already initialized instance of Var 
                                      (or most likely one of its derived classes) 
                                      for the main signal value.  
                                      If not supplied, a DummyVar will be used/
                                      created as fall back
                
                unit          - (opt) unit of physical signal value (as string,
                                      mainly used for report entries)
                alias         - (opt) bus signal alias/name, defaults to the 
                                      last (non-default) entry in identifier (i.e. 
                                      signal model path)
                
                descr         - (opt) signal description (e.g. used in report entries)
                lookup        - (opt) a lookup-table for mapping discrete signal 
                                      states to textual descriptions,  
                                      defaults to signal_var.unit.  
                
                change_delay  - (opt) delay to wait after a value change [ms], 
                                      defaults to 2x max(cycle_time, debounce_time)
                timeout       - (opt) detection time for timeout errors [ms], 
                                      defaults to 2x max(cycle_time, debounce_time)
                recovery_time - (opt) time for recovery/"wiedergut" checks [ms], 
                                      defaults to 2x max(cycle_time, debounce_time)
                
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class code cannot be analyzed.
        
        ## context for "HilVar" variables
        self.context = None
        ## Main bus signal variable on HIL-side.
        self.signal_var = None
        
        # #####################################################################
        _bus_signals_base.RxBusSignal.__init__(
            self, context, identifier, 
            cycle_time=cycle_time, debounce_time=debounce_time,
            signal_var=signal_var, 
            unit=unit, alias=alias, descr=descr, lookup=lookup,
            change_delay=change_delay, timeout=timeout, 
            recovery_time=recovery_time,
        )
    
    # #########################################################################
    # Basic methods inherited from  BusSignal
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable.
            Returns an info string.
         """
        return _bus_signals_base.RxBusSignal.info(self)
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable. 
            Returns the current value.
        """
        return _bus_signals_base.RxBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable.
            Parameters:
                value - new value to be set
            Returns the original value before the set operation occurred. 
        """
        return _bus_signals_base.RxBusSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data. 
            This uses the lookup values supplied in constructor.
            Fallback (if no matching state was found) will be the unmapped 
            numeric value.
            Returns current state's description.
        """
        return _bus_signals_base.RxBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor.
            
            Parameters:
                state - named state to set
            
            Returns the previous state's description.
        """
        return _bus_signals_base.RxBusSignal.setState(self, state)
    
    # #########################################################################
    def hasStateLookup(self):
        """ Return True if a state/value lookup table is defined for the HIL 
            signal variable. 
        """
        return _bus_signals_base.RxBusSignal.hasStateLookup(self)
    
    # #########################################################################
    def getStateDescr(self, value=None, fallback=None):
        """ Get a state description text for the given value from the HIL 
            signal variable's defined lookup table (if any).
            
            Parameters:
                value     - value for which to get a state description. 
                            If None, the last read value will be used instead.
                fallback  - fallback value to return if no match was found.
                            Default: None
            
            Returns the state text if a match was found, otherwise the specified
            fallback value.
        """
        return _bus_signals_base.RxBusSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def hasFormattedRepr(self):
        """ Return True if a formatting for value representation is defined
            for the HIL signal variable.
        """
        return _bus_signals_base.RxBusSignal.hasFormattedRepr(self)
    
    # #########################################################################
    def getFormattedValue(self, value=None):
        """ Get a formatted representation for the given value using the defined 
            format string of the the HIL signal variable. 
            An empty (or non-defined) format string will use the value's 
            default string representation.
            
            Parameters:
                value     - value for which to get a string representation.  
                            If None, the last value (read or written) will be 
                            used instead.
            
            Returns a formatted string representation. 
        """
        return _bus_signals_base.RxBusSignal.hasFormattedRepr(self, value)
    
    # #########################################################################
    def reset(self, *args, **kwargs): # @UnusedVariable *args, **kwargs (just to tolerate optional parameters)
        """ Call reset() on all contained variables/signals that support it."""
        _bus_signals_base.RxBusSignal.reset(self)
        

# #############################################################################
class CrcBusSignal(_bus_signals_base.CrcBusSignal):
    """ A RX bus signal (HIL => ECU) that models a CRC value with additional 
        error injections. This is the generic base class for CRC signals, 
        blockset/implementation specific CRC signal classes will inherit from 
        this.
        
        Attention:
            This is just a base class, using it directly will not accomplish much.
            At the very least, setBasicCrcError and clearBasicCrcError need to be 
            overridden depending on the target interface.  
        
        See bus_signals_frbs or bus_signals_canmmbs for existing implementations.
    """
    # #########################################################################
    def __init__(self, context, identifier, 
                 cycle_time=0, debounce_time=0, 
                 signal_var=None, 
                 alias="", descr="",
                 error_delay=None, change_delay=None, 
                 timeout=None, recovery_time=None):
        """ CRC bus signal initialization. 
            
            Parameters:
                context       - parent context for instantiating HIL variables.
                                This gets mainly used in derived classes
                identifier    - base signal identifier/name/path in the HIL 
                                model pointing to the CRC signal value.  
                                Derived classes typically use this identifier
                                as starting point for locating additional helper
                                variables.
                
                cycle_time    - cycle time in [ms]
                debounce_time - minimum debounce delay between events in [ms]
                
                signal_var    - (opt) an already initialized instance of Var 
                                      (or most likely one of its derived classes) 
                                      for the main signal value.
                
                alias         - (opt) bus signal alias/name,
                                      defaults to signal_var.alias.
                descr         - (opt) signal description (e.g. may get used in 
                                      report entries)
                
                error_delay   - (opt) delay to wait until a basic CRC error 
                                      injection should be detected [ms],
                                      defaults to 10x max(cycle_time, debounce_time)
                change_delay  - (opt) delay to wait after a value change [ms],
                                      defaults to 2x max(cycle_time, debounce_time)
                timeout       - (opt) detection time for timeout errors [ms],
                                      defaults to 2x max(cycle_time, debounce_time)
                recovery_time - (opt) time for recovery/"wiedergut" checks [ms],
                                      defaults to 2x max(cycle_time, debounce_time)
            
            Note:
                The parameters `change_delay`, `timeout` and `recovery_time` 
                are just here for completeness' sake, only `cycle_time` and 
                `error_delay` are used during typical CRC checks.
        
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class code cannot be analyzed.
        
        ## delay to wait after a "basic" crc error injection[ms] 
        self.error_delay = None
        
        _bus_signals_base.CrcBusSignal.__init__(
            self, context, identifier, 
            cycle_time=cycle_time, debounce_time=debounce_time,
            signal_var=signal_var,
            alias=alias, descr=descr, 
            error_delay=error_delay, change_delay=change_delay, 
            timeout=timeout, recovery_time=recovery_time
        )
    
    # #########################################################################
    def setBasicCrcError(self):
        """ Switch to basic CRC error state. """
        _bus_signals_base.CrcBusSignal.setBasicCrcError(self)
    
    # #########################################################################
    def clearBasicCrcError(self):
        """ Resume normal CRC calculation. """
        _bus_signals_base.CrcBusSignal.clearBasicCrcError(self) 
        
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/RxBusSignal
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. """
        return _bus_signals_base.CrcBusSignal.info(self)
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable
            (typically not that useful for ECU-Rx/HIL-Tx CRC-signals, though).
         """
        return _bus_signals_base.CrcBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable.
            Parameters:
                value - new value to set
            Returns the previous value.
        """
        return _bus_signals_base.CrcBusSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data. 
            (typically not that useful for ECU-Rx/HIL-Tx CRC-signals, though)."""
        return _bus_signals_base.CrcBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor.
            Parameters:
                state - named state to set
        """
        return _bus_signals_base.CrcBusSignal.setState(self, state)
    
    # #########################################################################
    def hasStateLookup(self):
        """ Return True if a state/value lookup table is defined for the HIL 
            signal variable. 
        """
        return _bus_signals_base.CrcBusSignal.hasStateLookup(self)
    
    # #########################################################################
    def getStateDescr(self, value=None, fallback=None):
        """ Get a state description text for the given value from the HIL 
            signal variable's defined lookup table (if any).
            
            Parameters:
                value     - value for which to get a state description. 
                            If None, the last read value will be used instead.
                fallback  - fallback value to return if no match was found.
                            Default: None
            
            Returns the state text if a match was found, otherwise the specified
            fallback value.
        """
        return _bus_signals_base.CrcBusSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def hasFormattedRepr(self):
        """ Return True if a formatting for value representation is defined
            for the HIL signal variable.
        """
        return _bus_signals_base.CrcBusSignal.hasFormattedRepr(self)
    
    # #########################################################################
    def getFormattedValue(self, value=None):
        """ Get a formatted representation for the given value using the defined 
            format string of the the HIL signal variable. 
            An empty (or non-defined) format string will use the value's 
            default string representation.
            
            Parameters:
                value     - value for which to get a string representation.  
                            If None, the last value (read or written) will be 
                            used instead.
            
            Returns a formatted string representation. 
        """
        return _bus_signals_base.CrcBusSignal.hasFormattedRepr(self, value)
    
    # #########################################################################
    def reset(self, *args, **kwargs): # @UnusedVariable *args, **kwargs (just to tolerate optional parameters)
        """ Call reset() on all contained variables/signals that support it. """
        _bus_signals_base.CrcBusSignal.reset(self)
        

# #############################################################################
class AcBusSignal(_bus_signals_base.AcBusSignal):
    """ A RX bus signal (HIL => ECU) that models an alive counter value with 
        additional error injections. This is the generic base class for AC
        signals, blockset/implementation specific AC signal classes will 
        inherit from this.
        
        Attention:
            This is just a base class, using it directly will not accomplish much.
            At the very least, setBasicAcError and clearBasicAcError need to be 
            overridden depending on the target interface.
        
        See bus_signals_frbs or bus_signals_canmmbs for existing implementations.
    """
    # #########################################################################
    def __init__(self, context, identifier, cycle_time=0, debounce_time=0, 
                 signal_var=None,
                 alias="", descr="",
                 error_delay=None, change_delay=None, 
                 timeout=None, recovery_time=None):
        """ Alive counter bus signal initialization.
            
            Parameters:
                context       - parent context for instantiating HIL variables.
                                This gets mainly used in derived classes
                identifier    - base signal identifier/name/path in the HIL 
                                model pointing to the alive counter signal value.  
                                Derived classes typically use this identifier
                                as starting point for locating additional helper
                                variables.
                
                cycle_time    - cycle time in [ms]
                debounce_time - minimum debounce delay between events in [ms]
                
                signal_var    - (opt) an already initialized instance of Var 
                                      (or most likely one of its derived classes) 
                                      for the main signal value.
                
                alias         - (opt) bus signal alias/name,
                                      defaults to signal_var.alias.
                descr         - (opt) signal description (e.g. may get used in 
                                      report entries)
                
                error_delay   - (opt) delay to wait until a basic alive counter error 
                                      injection should be detected [ms],
                                      defaults to 10x max(cycle_time, debounce_time)
                change_delay  - (opt) delay to wait after a value change [ms],
                                      defaults to 2x max(cycle_time, debounce_time)
                timeout       - (opt) detection time for timeout errors [ms],
                                      defaults to 2x max(cycle_time, debounce_time)
                recovery_time - (opt) time for recovery/"wiedergut" checks [ms],
                                      defaults to 2x max(cycle_time, debounce_time)
            
            Note:
                The parameters `change_delay`, `timeout` and `recovery_time` 
                are just here for completeness' sake, only `cycle_time` and 
                `error_delay` are used during typical Alive Counter checks.
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class code cannot be analyzed.
        
        ## delay to wait after a "basic" crc error injection[ms] 
        self.error_delay = None
        
        _bus_signals_base.AcBusSignal.__init__(
            self, context, identifier,
            cycle_time=cycle_time, debounce_time=debounce_time,
            signal_var=signal_var,
            alias=alias, descr=descr, 
            error_delay=error_delay, change_delay=change_delay, 
            timeout=timeout, recovery_time=recovery_time
        )
    
    # #########################################################################
    def setBasicAcError(self):
        """ Switch to basic alive counter error state (which is usually "counter 
            stopped") 
        """
        _bus_signals_base.AcBusSignal.setBasicAcError(self)
    
    # #########################################################################
    def clearBasicAcError(self):
        """ Resume normal alive counter operation (which is typically "continue 
            counting").
        """
        _bus_signals_base.AcBusSignal.clearBasicAcError(self) 
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/RxBusSignal
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. 
            Returns an info string.
        """
        return _bus_signals_base.AcBusSignal.info(self)
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable
            (typically not that useful for ECU-Rx/HIL-Tx AC-signals, though).
            Returns current value.
         """
        return _bus_signals_base.AcBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable. 
            Parameters:
                value - new value to set
            Returns the previous value.
        """
        return _bus_signals_base.AcBusSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data. 
            (typically not that useful for ECU-Rx/HIL-Tx AC-signals, though).
            Returns the current state's description
        """
        return _bus_signals_base.AcBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor.
            Parameters:
                state - named state to set
            Returns the previous state's description
        """
        return _bus_signals_base.AcBusSignal.setState(self, state)
    
    # #########################################################################
    def hasStateLookup(self):
        """ Return True if a state/value lookup table is defined for the HIL 
            signal variable. 
        """
        return _bus_signals_base.AcBusSignal.hasStateLookup(self)
    
    # #########################################################################
    def getStateDescr(self, value=None, fallback=None):
        """ Get a state description text for the given value from the HIL 
            signal variable's defined lookup table (if any).
            
            Parameters:
                value     - value for which to get a state description. 
                            If None, the last read value will be used instead.
                fallback  - fallback value to return if no match was found.
                            Default: None
            
            Returns the state text if a match was found, otherwise the specified
            fallback value.
        """
        return _bus_signals_base.AcBusSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def hasFormattedRepr(self):
        """ Return True if a formatting for value representation is defined
            for the HIL signal variable.
        """
        return _bus_signals_base.AcBusSignal.hasFormattedRepr(self)
    
    # #########################################################################
    def getFormattedValue(self, value=None):
        """ Get a formatted representation for the given value using the defined 
            format string of the the HIL signal variable. 
            An empty (or non-defined) format string will use the value's 
            default string representation.
            
            Parameters:
                value     - value for which to get a string representation.  
                            If None, the last value (read or written) will be 
                            used instead.
            
            Returns a formatted string representation. 
        """
        return _bus_signals_base.AcBusSignal.hasFormattedRepr(self, value)
    
    # #########################################################################
    def reset(self, *args, **kwargs): # @UnusedVariable *args, **kwargs (just to tolerate optional parameters)
        """ Call reset() on all contained variables/signals that support it. """
        _bus_signals_base.AcBusSignal.reset(self)
        

# #############################################################################
# Signal Container
# #############################################################################
class BusSignalContainer(_bus_signals_base.BusSignalContainer):
    """ Base class for BusSignal containers. """
    
    # #########################################################################
    def __init__(self, context):
        """ Override to add signals.
            Parameter:
                context - context used for contained BusSignals
        """
        _bus_signals_base.BusSignalContainer.__init__(self, context)
    
    # #########################################################################
    def resetAll(self, verbosity=1, recursion_depth=4):
        """ Call reset() on all contained BusSignals that support it. 
            Parameters:
                verbosity       - verbosity of log output:
                                   0: silent except for errors
                                   1: only minimal status info (begin/end)
                                   2: also show processed variable names
                recursion_depth - how "deep" to recurse into lists/dictionary
                                  structures when looking for variables to 
                                  reset.
        """
        _bus_signals_base.BusSignalContainer.resetAll(
            self, 
            verbosity=verbosity, 
            recursion_depth=recursion_depth
        )
        

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    import time
    
    if True:
        # HilVar via rtplib 
        import ttk_tools.dspace.rtplib_offline_stub as rtplib
        context = rtplib.Appl("foo.sdf", "bar1005", "Offline")
    else:
        #
        # HilVar via XIL API
        import ttk_tools.dspace.xil_api_offline_stub as xil_api
        context = xil_api.XilTestbench(
            config_file_path = r"D:\Python\MAPortConfiguration.xml",
            product_name    = "XIL API", 
            product_version = "2.0.0",
        )
    
    
    sig = BusSignal(context, "Model Root/CAN/FooBarSig/Value", 10)
    
    print "signal_var: %-36s | sig: %s"%(sig.signal_var.info(), sig.info())
    sig.signal_var.set(123)
    print "signal_var: %-36s | sig: %s"%(sig.signal_var.info(), sig.info())
    sig.reset()
    print "signal_var: %-36s | sig: %s"%(sig.signal_var.info(), sig.info())
    
    
    # #########################################################################
    class BusSignals(BusSignalContainer):
        def __init__(self, context):
            self.FooBarSig  = BusSignal(context, "Model Root/CAN/FooBarSig/Value", 10)
            self.BazQuuxSig = BusSignal(context, "Model Root/CAN/BazQuuxSig/Out1", 100)
            self.AnotherSig = BusSignal(context, "Model Root/CAN/Another Signal/Value", 
                alias="Another Bus Signal", descr="Another Signal to test", unit="rpm", 
                cycle_time=100, 
                change_delay=250, timeout=500, recovery_time=500,
            )
    
    bus_signals = BusSignals(context)
    
    print "# initial:"
    print bus_signals.FooBarSig.signal_var.info()
    print bus_signals.BazQuuxSig.signal_var.info()
    print bus_signals.AnotherSig.signal_var.info()
    bus_signals.FooBarSig.set(1234)
    bus_signals.AnotherSig.set(1000)
    time.sleep(bus_signals.AnotherSig.cycle_time / 1000.0)
    
    print "# changed:"
    print bus_signals.FooBarSig.signal_var.info()
    print bus_signals.BazQuuxSig.signal_var.info()
    print bus_signals.AnotherSig.signal_var.info()
    
    print
    bus_signals.resetAll()
    print "# reset:"
    print bus_signals.FooBarSig.signal_var.info()
    print bus_signals.BazQuuxSig.signal_var.info()
    print bus_signals.AnotherSig.signal_var.info()
    

# @endcond DOXYGEN_IGNORE
# #############################################################################
