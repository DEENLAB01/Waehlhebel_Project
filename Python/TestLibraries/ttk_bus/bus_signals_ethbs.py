#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : _bus_signals_ethbs.py
# Package : ttk_bus
# Task    : Wrapper classes for bus/interface signal descriptions.
#           Specific implementation for dSPACE Ethernet blocksets 
# Python  : 2.5+
# Type    : Interface
#
# Copyright 2013 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Author    | Description
#------------------------------------------------------------------------------
# 1.0  | 13.02.2015 | L.Morgus  | initial
# 1.1  | 13.03.2015 | L.Morgus  | expanded descriptions and examples
# 1.2  | 27.03.2015 | L.Morgus  | RxEthEvent / TxEthEvent
# 1.3  | 28.04.2016 | Tremmel   | added EthSignalContainer
# 1.4  | 01.12.2016 | J.Tremmel | updated interface methods
# 1.5  | 31.07.2017 | J.Tremmel | CrcEthStatus: added explicit get/getState wrappers
# 1.6  | 30.08.2017 | J.Tremmel | added interface descriptions for getStateDescr methods
# 2.5  | 02.07.2020 | J.Tremmel | removed obsolete signal parameters min/max_value
#******************************************************************************
"""
@package ttk_bus.bus_signals_ethbs
Interface wrapper for "bus"/interface signal classes in ttk_bus._bus_signals_ethbs.
Specific implementation for dSpace Ethernet blocksets ("Ethernet Configuration 
Package") using ModelRoot-signals and (for E2E) BusSystems-signals)

Convention:
    Signal directions are relative to the DUT:
       * Tx - transmitted by ECU => received from HIL
       * Rx - received by ECU <= transmitted from HIL
       
       * PSI - provider, Tx
       * CSI - consumer, Rx
    
"""
import _bus_signals_ethbs

# #############################################################################
# NOTE: Model Root-based implementations ---
# Some functionality (Subscriber States, ...) is only available in Model Root,
# while other (E2E, ..) can only be found in BusSystems.
#
# Furthermore, using variables below ModelRoot allows us to skip handling of 
# Source Switches.
# #############################################################################


# #############################################################################
# [Model Root] Ethernet Events (and Fields, HIL => ECU)
# #############################################################################
class RxEthEvent(_bus_signals_ethbs.RxEthEvent):
    """ Ethernet-Event-specific data and methods - Rx (HIL-Tx => ECU-Rx).
        Extends EthEvent with methods for enableHilTx/disableHilTx and kickout 
        (trigger).
        
        Note: This class expects a "Model Root/" path structure.
        
        Also note that BusSystems-based implementations (see below) may use
        Model-Root-based EthEvents without problems.
    """
    # #########################################################################
    def __init__(self, context, enable_path, trigger_path, 
                 cycle_time=0, debounce_time=0,
                 alias='', descr='',
                 change_delay=None, timeout=None, recovery_time=None):
        """ Ethernet Rx-Event (or field) data.
            
            Parameters:
                context       - parent context (an RTE application or XilTestbench 
                                instance to resolve signal/variable paths)
                enable_path   - model path to tx enable switch (if available)
                trigger_path  - model path to tx trigger (if available)
                
                cycle_time    - cycle time in [ms]. On-demand events have a cycle 
                                time of 0 (similar to fibex value)
                debounce_time - minimum debounce delay time between events in [ms]
                
                alias         - Event alias/name
                descr         - (opt) Event description (may be used in report entries)
                
                change_delay  - (opt) delay to wait after a value change [ms], 
                                      defaults to 2x max(cycle_time, debounce_time)
                timeout       - (opt) detection time for timeout errors [ms], 
                                      defaults to 2x max(cycle_time, debounce_time)
                recovery_time - (opt) time for recovery/"wiedergut" checks [ms]
                                      defaults to 2x max(cycle_time, debounce_time)
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so auto-complete may find them even 
        #       if the base class code cannot be analyzed.
        
        ## HIL-Tx enable/disable variable (a "HilVar" instance)
        self.enable_var = None
        ## HIL-Tx kickout/trigger variable (a "HilVar" instance)
        self.kickout_var = None
        
        # Members inherited from CanBusMessage (see Note above) ###############
        ## parent context (an RTE application instance to resolve signal/variable paths)
        self.context = None
        ## alias name of event
        self.alias = None
        ## description text of event 
        self.descr = None
        
        ## model path to tx enable switch (if available).
        # Other relevant entries will be derived from this 
        # path (e.g. kickout, status, ...)
        self.enable_path = enable_path
        
        # timings #############################################################
        ## cycle time of event in [ms]
        self.cycle_time = None
        ## minimum debounce delay for triggered events in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        _bus_signals_ethbs.RxEthEvent.__init__(
            self, context=context, 
            enable_path=enable_path, trigger_path=trigger_path, 
            cycle_time=cycle_time, debounce_time=debounce_time, 
            alias=alias, descr=descr, change_delay=change_delay, 
            timeout=timeout, recovery_time=recovery_time
        )
        
    
    # #########################################################################
    def enableHilTx(self):
        """ (Re-)enable sending of Event. """
        _bus_signals_ethbs.RxEthEvent.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable sending of Event. """
        _bus_signals_ethbs.RxEthEvent.disableHilTx(self)
    
    # #########################################################################
    def kickout(self, delay_ms=None):
        """ Trigger sending of the Ethernet Event / Field. 
            
            Parameters: 
                delay_ms - [ms] Delay to wait before clearing kickout/trigger 
                           variable again (it _should_ auto-reset, but anyway).  
                           Defaults to self.debounce_time (if explicitly set)
                           or alternatively to self.change_delay
        """
        _bus_signals_ethbs.RxEthEvent.kickout(self, delay_ms=delay_ms)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs): 
        """ Call reset() on all contained variables/signals that support it.
            Simple, non-recursive approach.
        """
        _bus_signals_ethbs.RxEthEvent.reset(self, *args, **kwargs)
        

# #############################################################################
# [Model Root] Ethernet Events (and Fields, ECU => HIL)
# #############################################################################
class TxEthEvent(_bus_signals_ethbs.TxEthEvent):
    """ Ethernet-Event-specific data and methods - Tx (ECU-Tx => HIL-Rx).
        
        Note:
            This is currently just a container for meta entries, 
            as there are (so far) no HIL variables needed for Tx events.
        
    """
    # #########################################################################
    def __init__(self, context, 
                 cycle_time=0, debounce_time=0,
                 alias="", descr="", 
                 change_delay=None, timeout=None, recovery_time=None,
                 ):
        """ Ethernet Tx-Event (or field) data.
            
            Note:
                This is currently just a container for meta entries, 
                as there are (so far) no HIL variable needed for Tx events.
            
            Parameters:
                context       - parent context, an RTE application or XilTestbench 
                                instance to resolve variable paths (if any)
                cycle_time    - (opt) cycle time in [ms]
                debounce_time - (opt) minimum debounce delay time between events in [ms]
                
                alias         - (opt) event alias/name
                descr         - (opt) event description (e.g. used in report entries)
                
                change_delay  - (opt) delay to wait after a value change [ms], 
                                      defaults to 2x max(cycle_time, debounce_time)
                timeout       - (opt) detection time for timeout errors [ms], 
                                      defaults to 2x max(cycle_time, debounce_time)
                recovery_time - (opt) time for recovery/"wiedergut" checks [ms]
                                      defaults to 2x max(cycle_time, debounce_time)
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so auto-complete may find them even
        #       if the base class code cannot be analyzed.
        
        # Members inherited from EthEvent (see Note above) ####################
        ## parent context (an RTE application instance to resolve signal/variable paths)
        self.context = None
        ## event alias name
        self.alias = None
        ## event description text
        self.descr = None
        
        # timings #############################################################
        ## cycle time of signal in [ms]
        self.cycle_time = None
        ## minimum debounce delay for triggered signals in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        _bus_signals_ethbs.TxEthEvent.__init__(
            self, context, 
            cycle_time=cycle_time, debounce_time=debounce_time,
            alias=alias, descr=descr,
            change_delay=change_delay, timeout=timeout, recovery_time=recovery_time,
        )
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs): 
        """ Call reset() on all contained variables/signals that support it.
            Simple, non-recursive approach.
        """
        _bus_signals_ethbs.TxEthEvent.reset(self, *args, **kwargs)
        

# #############################################################################
# [Model Root] Ethernet Event Signal (HIL => ECU)
# #############################################################################
class RxEthSignal(_bus_signals_ethbs.RxEthSignal):
    """ An Ethernet event signal/parameter/sub-parameter sent from test system 
        to DUT (ECU CSI Rx <= HIL PSI Tx). 
        
        Note: This class expects a "Model Root/" path structure.
    """
    # #########################################################################
    def __init__(self, context, signal_path, 
                 event=None, cycle_time=None, debounce_time=None,
                 unit="", alias="", descr="", lookup=None,
                 change_delay=None, timeout=None, recovery_time=None,
                 **kwargs):
        """ Ethernet Rx signal initialization ("Model Root/"-path flavour).
            
            Parameters:
                context       - parent context (an RTE application or XilTestbench 
                                instance to resolve signal/variable paths)
                signal_path   - signal path below ModelRoot
                event         - reference to associated EthEvent instance
                cycle_time    - (opt) cycle time in [ms], overrides settings in EthEvent
                debounce_time - (opt) minimum debounce delay time between events in [ms],
                                      overrides settings in EthEvent
                unit          - (opt) unit of physical signal value (as string,
                                      mainly used for report entries)
                alias         - (opt) bus signal alias/name, defaults to the 
                                      last (non-default) entry in identifier
                                      (i.e. signal model path)
                
                descr         - (opt) signal description (e.g. used in report entries)
                lookup        - (opt) a lookup-table for mapping discrete signal 
                                      states to textual descriptions
                
                change_delay  - (opt) delay to wait after a value change [ms],  
                                      defaults to 2x max(cycle_time, debounce_time)
                timeout       - (opt) detection time for timeout errors [ms],  
                                      defaults to 2x max(cycle_time, debounce_time)
                recovery_time - (opt) time for recovery/"wiedergut" checks [ms],  
                                      defaults to 2x max(cycle_time, debounce_time)
        """
        
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so auto-complete may find them even 
        #       if the base class code cannot be analyzed.
        
        # Members inherited from BusSignal (see Note above) ###################
        ## parent context (an RTE application instance to resolve signal/variable paths)
        self.context = None
        ## Base path to signal below BusSystems
        self.signal_path = None
        ## reference to associated EthEvent instance
        self.event = None
        
        ## unit of physical signal value (as string, mainly used for report entries)
        self.unit = None
        ## bus signal alias name
        self.alias = None
        ## signal description text
        self.descr = None
        
        # timings #############################################################
        ## cycle time of signal in [ms]
        self.cycle_time = None
        ## minimum debounce delay for triggered signals in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        # #####################################################################
        _bus_signals_ethbs.RxEthSignal.__init__(
            self, context=context, 
            signal_path=signal_path, 
            event=event, cycle_time=cycle_time, 
            debounce_time=debounce_time, 
            unit=unit, alias=alias, 
            descr=descr, lookup=lookup, 
            change_delay=change_delay, 
            timeout=timeout, 
            recovery_time=recovery_time, 
            **kwargs
        )
    
    # #########################################################################
    def enableHilTx(self):
        """ Enable transmission of signal HIL => DUT (if the assigned EthEvent
            supports it). 
            
            Note: This enables transmission of all signals in the parent Event.
        """
        _bus_signals_ethbs.RxEthSignal.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable transmission of signal HIL => DUT (if the assigned EthEvent
            supports it).
            
            Note: This disables transmission of all signals in the parent Event.
        """
        _bus_signals_ethbs.RxEthSignal.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger sending of the Ethernet Event / Field. """ 
        _bus_signals_ethbs.RxEthSignal.kickout(self)
        
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/RxBusSignal
    # #########################################################################
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable
            (typically not that useful for ECU-Rx/HIL-Tx signals, though).
            
            Returns the current value from signal_var.
         """
        return _bus_signals_ethbs.RxEthSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable. 
            
            Parameters:
                value - value to set
            
            Returns the previous value from signal_var.
        """
        
        return _bus_signals_ethbs.RxEthSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data. 
            (typically not that useful for ECU-Rx/HIL-Tx signals, though).
            This uses the lookup values supplied in constructor.
            
            Returns the current state representation from signal_var.
        """
        return _bus_signals_ethbs.RxEthSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor.
            
            Parameters:
                state - named state to set
            
            Returns the previous value representation from signal_var.
        """
        return _bus_signals_ethbs.RxEthSignal.setState(self, state)
    
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
        return _bus_signals_ethbs.RxEthSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. 
            Returns an info string.
        """
        return _bus_signals_ethbs.RxEthSignal.info(self)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_ethbs.RxEthSignal.reset(self, *args, **kwargs)
        

# #############################################################################
# [Model Root] Ethernet Event Signal (ECU => HIL)
# #############################################################################
class TxEthSignal(_bus_signals_ethbs.TxEthSignal):
    """ An Ethernet event signal/parameter/sub-parameter sent from DUT to 
        test system (ECU PSI Tx => HIL CSI Rx). 
        
        Note: This class expects a "Model Root/" path structure.
    """
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/TxBusSignal
    # #########################################################################
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable.
            
            Returns the current value from signal_var. 
        """
        return _bus_signals_ethbs.TxEthSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable 
            (typically not that useful for ECU-Tx/HIL-Rx signals, though).
            
            Parameters:
                value - value to set
            
            Returns the previous value from signal_var.
        """
        return _bus_signals_ethbs.TxEthSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data.
            Returns the current state representation from signal_var.
        """
        return _bus_signals_ethbs.TxEthSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor (typically not that useful 
            for ECU-Tx/HIL-Rx signals, though).
            
            Parameters:
                state - named state to set
            
            Returns the previous value representation from signal_var.
        """
        return _bus_signals_ethbs.TxEthSignal.setState(self, state)
    
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
        return _bus_signals_ethbs.TxEthSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. 
            Returns an info string.
        """
        return _bus_signals_ethbs.TxEthSignal.info(self)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_ethbs.TxEthSignal.reset(self, *args, **kwargs)
        
# #############################################################################
# NOTE: BusSystems-based implementations ---
# Alas, some functionality (E2E, ...) is only available below BusSystems,
# while other functionality (Service Discovery, ...) can only be found 
# in elements below Model Root.
# #############################################################################


# #############################################################################
# [BusSystems] Ethernet Event Signal (HIL => ECU)
# #############################################################################
class RxEthBusSysSignal(_bus_signals_ethbs.RxEthBusSysSignal):
    """ An Ethernet event signal/parameter/sub-parameter sent from test system 
        to DUT (HIL PSI Tx => ECU CSI Rx). 
        
        Note: This class expects a BusSystems path structure.
    """
    
    # #########################################################################
    def __init__(self, context, base_path,
                 event=None, cycle_time=None, debounce_time=None,
                 unit="", alias="", descr="", lookup=None,
                 change_delay=None, timeout=None, recovery_time=None,
                 ):
        """ Ethernet Rx signal initialization (BusSystems flavour).
            
            Parameters:
                context       - parent context (an RTE application or XilTestbench 
                                instance to resolve signal/variable paths)
                base_path     - signal path below BusSystems (typically: use .../foobar/Value)
                event         - reference to associated EthEvent instance
                cycle_time    - (opt) cycle time in [ms], overrides settings in EthEvent
                debounce_time - (opt) minimum debounce delay time between events in [ms],
                                      overrides settings in EthEvent
                unit          - (opt) unit of physical signal value (as string,
                                      mainly used for report entries)
                alias         - (opt) bus signal alias/name, defaults to the 
                                      last (non-default) entry in identifier
                                      (i.e. signal model path)
                
                descr         - (opt) signal description (e.g. used in report entries)
                lookup        - (opt) a lookup-table for mapping discrete signal 
                                      states to textual descriptions
                
                change_delay  - (opt) delay to wait after a value change [ms], 
                                      defaults to 2x cycle_time
                timeout       - (opt) detection time for timeout errors [ms], 
                                      defaults to 2x cycle_time
                recovery_time - (opt) time for recovery/"wiedergut" checks [ms]
                                      defaults to 2x cycle_time
        """
        
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so autocomplete may find them even 
        #       if the base class code cannot be analyzed.
        
        ## Source Switch path (a "HilVar" instance)
        self.switch_path = None
        ## Source Switch variable (a HilVar instance)
        # * 0: value source is Simulink Model 
        # * 1: value source is BusSystems
        self.switch_var = None
        
        # Members inherited from BusSignal (see Note above) ###################
        ## parent context (an RTE application instance to resolve signal/variable paths)
        self.context = None
        ## base path to signal below BusSystems
        self.signal_path = None
        ## reference to associated EthEvent instance
        self.event = None
        
        ## unit of physical signal value (as string, mainly used for report entries)
        self.unit = None
        ## bus signal alias name
        self.alias = None
        ## signal description text
        self.descr = None
        
        # timings #############################################################
        ## cycle time of signal in [ms]
        self.cycle_time = None
        ## minimum debounce delay for triggered signals in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        # #####################################################################
        
        _bus_signals_ethbs.RxEthBusSysSignal.__init__(
            self, context=context, 
            base_path=base_path, event=event, 
            cycle_time=cycle_time, 
            debounce_time=debounce_time, 
            unit=unit, alias=alias, 
            descr=descr, lookup=lookup, 
            change_delay=change_delay, 
            timeout=timeout, recovery_time=recovery_time
        )
    
    # #########################################################################
    def switchToBusSystemsSource(self, bus_systems=True):
        """ Switch signal source to variables below "BusSystems". 
            This is mainly intended for internal use.
            
            Parameters:
                bus_systems - True:  use "BusSystems" paths as source  
                              False: use "Model Root" paths as source
        """
        _bus_signals_ethbs.RxEthBusSysSignal.switchToBusSystemsSource(
            self, bus_systems=bus_systems
        )
    
    # #########################################################################
    def enableHilTx(self):
        """ Enable transmission of signal HIL => DUT (if the assigned EthEvent
            supports it). 
            
            Note: This enables transmission of all signals in the parent Event.
        """
        _bus_signals_ethbs.RxEthBusSysSignal.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable transmission of signal HIL => DUT (if the assigned EthEvent
            supports it). 
            
            Note: This disables transmission of all signals in the parent Event.
        """
        _bus_signals_ethbs.RxEthBusSysSignal.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger transmission ("kickout") of signal HIL => DUT 
            (by triggering the parent EthEvent).
            
            Note: All other signals of the parent EthEvent also will be sent.
        """
        _bus_signals_ethbs.RxEthBusSysSignal.kickout(self)
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/RxBusSignal
    # #########################################################################
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable
            (typically not that useful for ECU-Rx/HIL-Tx signals, though).
            
            Returns the current value from signal_var. 
         """
        return _bus_signals_ethbs.RxEthBusSysSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable.
            Parameters:
                value - value to be set
            Returns the original value before the set operation occurred. 
        """
        return _bus_signals_ethbs.RxEthBusSysSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data
            (typically not that useful for ECU-Rx/HIL-Tx signals, though).
            
            Returns the current state's description.
        """
        return _bus_signals_ethbs.RxEthBusSysSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor.
            
            Parameters:
                state - named state to set
            
            Returns the previous state's description.
        """
        return _bus_signals_ethbs.RxEthBusSysSignal.setState(self, state)
    
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
        return _bus_signals_ethbs.RxEthBusSysSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. 
            Returns an info string.
        """
        return _bus_signals_ethbs.RxEthBusSysSignal.info(self)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_ethbs.RxEthBusSysSignal.reset(self, *args, **kwargs)
        

# #############################################################################
# [BusSystems] Ethernet Event Signal (ECU => HIL)
# #############################################################################
class TxEthBusSysSignal(_bus_signals_ethbs.TxEthBusSysSignal):
    """ An Ethernet event signal/parameter/sub-parameter sent from DUT to 
        test system (ECU PSI Tx => HIL CSI Rx). 
        
        Note: This class expects a BusSystems path structure.
    """
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/TxBusSignal
    # #########################################################################
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable. 
            
            Returns the current value from signal_var. 
        """
        return _bus_signals_ethbs.TxEthBusSysSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable
            (typically not that useful for ECU-Tx/HIL-Rx signals, though).
            Parameters:
                value - value to set
            Returns the previous value from signal_var.
        """
        return _bus_signals_ethbs.TxEthBusSysSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data.
            Returns the current state's description. 
        """
        return _bus_signals_ethbs.TxEthBusSysSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor (typically not that useful 
            for ECU-Tx/HIL-Rx signals, though).
            Parameters:
                state - named state to set
          Returns the previous state's description.
        """
        return _bus_signals_ethbs.TxEthBusSysSignal.setState(self, state)
    
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
        return _bus_signals_ethbs.TxEthBusSysSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. 
            Returns an info string.
        """
        return _bus_signals_ethbs.TxEthBusSysSignal.info(self)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_ethbs.TxEthBusSysSignal.reset(self, *args, **kwargs)
        

# #############################################################################
# [BusSystems] CRC Validity Status (for ECU => HIL)
# #############################################################################
class CrcEthStatus(_bus_signals_ethbs.CrcEthStatus):
    """ CRC Tx-Event/Signal status (ECU PSI Tx => HIL CSI Rx) and associated 
        switch variables for dSPACE Ethernet blockset.
        
        Note: This class expects a BusSystems path structure.
        
        Note: This behaves essentially as a basic "HilVar" containing 
        the CRC status plus additional sub-variables.
    """
    # #########################################################################
    def __init__(self, context, crc_data_path, alias="", descr=""):
        """ HIL-Rx CRC-check status variables.
            
            Info: CRC check status values:
                * 0: CRC valid
                * 1: CRC invalid
                * 2: CRC check is disabled
            
            Example: BusSystems Path Structure
                # CRC enable variable:
                BusSystems/Ethernet/FRR/CSIs/ACME.ENVIRONMENTALMODEL/RoadDescription_3/Events/RoadForesight/E2E Protection/cRC/CRC/Enable
                # CRC status variable:
                BusSystems/Ethernet/FRR/CSIs/ACME.ENVIRONMENTALMODEL/RoadDescription_3/Events/RoadForesight/E2E Protection/cRC/CRC/Status
                # CRC type variable:
                BusSystems/Ethernet/FRR/CSIs/ACME.ENVIRONMENTALMODEL/RoadDescription_3/Events/RoadForesight/E2E Protection/cRC/CRC/Type
                # CRC signal variable:
                BusSystems/Ethernet/FRR/CSIs/ACME.ENVIRONMENTALMODEL/RoadDescription_3/Events/RoadForesight/E2E Protection/cRC/Value 
            
            Parameters:
                context       - parent context (an RTE application or XilTestbench 
                                instance to resolve signal/variable paths)
                crc_data_path - model path to /CRC/Enable branch of the event group
                                (or directly to the /CRC/Status variable)
                alias         - (opt) CRC signal alias/name
                descr         - (opt) CRC signal description
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so auto-complete may find them even 
        #       if the base class code cannot be analyzed.
        
        
        ## CRC calculation/check enable variable ("CRC Enable"):
        # * 0: calculation/check disabled
        # * 1: calculation/check enabled
        self.enable_var = None
        
        ## Source Switch variable for CRC check enable:
        # * 0: Simulink Model 
        # * 1: BusSystems
        #
        # This is unused for CRC-Enable (but kept for consistency with FR & CAN equivalents).
        # => ECP E2E BuySystems structure does not use/have a switch var 
        #    (as E2E info is n/a in SL/Model)
        self.switch_var = None
        
        # CRC check status values:
        # * 0: valid
        # * 1: invalid
        # * 2: disabled
        _bus_signals_ethbs.CrcEthStatus.__init__(
            self, context=context, 
            crc_data_path=crc_data_path, 
            alias=alias, descr=descr
        )
    
    # #########################################################################
    def enableCrcCalc(self):
        """ Enable CRC calculation/evaluation regardless of setting in model. """
        _bus_signals_ethbs.CrcEthStatus.enableCrcCalc(self)
    
    # #########################################################################
    def get(self):
        """ Get current CRC status value. 
            
            Possible values are
              * 0: CRC value is valid
              * 1: CRC value is invalid
              * 2: CRC check is disabled
            
            Returns the current status value.
        """
        return _bus_signals_ethbs.CrcEthStatus.get(self)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state description for the current CRC status value.
            Returns the current state representation.
        """
        return _bus_signals_ethbs.CrcEthStatus.getState(self)
    
    # #########################################################################
    def reset(self):
        """ Reset CRC calculation settings (switch back to calculation settings
            from "model"). 
        """
        _bus_signals_ethbs.CrcEthStatus.reset(self)
        

# #############################################################################
# [BusSystems] CRC Signal (HIL => ECU)
# #############################################################################
class CrcEthSignal(_bus_signals_ethbs.CrcEthSignal):
    """ A CRC RX Ethernet event signal/parameter (HIL-Tx => ECU-Rx) 
        for use with dSPACE Ethernet blockset.
        
        Note: This class expects a BusSystems path structure.
    """
    # #########################################################################
    def __init__(self, context, base_path, 
                 event=None, cycle_time=None, debounce_time=None,
                 alias="", descr="",
                 error_delay=None, change_delay=None, timeout=None, 
                 recovery_time=None,
                 **kwargs):
        """ CRC Ethernet signal initialization (with error injection, via BusSystems)
            for dSPACE Ethernet blockset.
            
            Example: BusSystems CRC Signal Path Structure
                BusSystems/Ethernet/FRR/PSIs/ACME.ENVIRONMENTALMODEL/BrakeAssistFrontRadar_1/Events/BrakeAssistFrontRadar/E2E Protection/cRC/CRC/Enable
                BusSystems/Ethernet/FRR/PSIs/ACME.ENVIRONMENTALMODEL/BrakeAssistFrontRadar_1/Events/BrakeAssistFrontRadar/E2E Protection/cRC/CRC/Type
                BusSystems/Ethernet/FRR/PSIs/ACME.ENVIRONMENTALMODEL/BrakeAssistFrontRadar_1/Events/BrakeAssistFrontRadar/E2E Protection/cRC/Source Switch
                BusSystems/Ethernet/FRR/PSIs/ACME.ENVIRONMENTALMODEL/BrakeAssistFrontRadar_1/Events/BrakeAssistFrontRadar/E2E Protection/cRC/Value
            
            Info: Suitable base_paths / examples:
                BusSystems/Ethernet/FRR/PSIs/ACME.ENVMDL/BrakeAssistFR/Events/BrakeAssistFR/E2E Protection/cRC/CRC/Enable  
                BusSystems/Ethernet/FRR/PSIs/ACME.ENVMDL/BrakeAssistFR/Events/BrakeAssistFR/E2E Protection/cRC/Value  
                => anything below .../CRC/* or the .../Value entry
            
            Parameters:
                context         - parent context (an RTE application or XilTestbench 
                                  instance to resolve signal/variable paths)
                base_path       - base model path below BusSystems from which 
                                  all required paths will be derived 
                                  (use /CRC/Enable of actual crc signal)
                event           - reference to associated EthEvent instance
                cycle_time      - (opt) cycle time in [ms], overrides settings in EthEvent
                debounce_time   - (opt) minimum debounce delay time between events in [ms],
                                        overrides settings in EthEvent
                alias           - (opt) bus signal alias/name
                descr           - (opt) signal description
                error_delay     - (opt) delay to wait until a simple crc error 
                                        should be detected [ms],
                                        defaults to 10x cycle time
                change_delay    - (opt) delay to wait after a value change [ms], 
                                        defaults to 2x cycle_time
                timeout         - (opt) detection time for timeout errors [ms], 
                                        defaults to 2x cycle_time
                recovery_time   - (opt) time for recovery/"wiedergut" checks [ms],
                                        defaults to 2x cycle_time
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so auto-complete may find them even 
        #       if the base class code cannot be analyzed.
        
        ## CRC type for "correct" CRC algorithm (normal mode)
        self.crc_normal_type = 1 # default 
        ## CRC type for "incorrect" CRC algorithm (for error injection)
        self.crc_error_type  = 2 # default
        
        ## delay [ms] to wait until a basic CRC error (like "CRC invalid")
        #  should be detected. This will be used in test functions.
        self.error_delay = None
        
        ## CRC Type variable, selects active CRC algorithm (a "HilVar" instance)
        self.crc_type_var   = None
        
        ## CRC Enable variable, enables/disables automatic CRC calculation (a "HilVar" instance)
        # * 0: CRC calculation disabled
        # * 1: CRC calculation enabled
        self.crc_enable_var = None
        
        # Members inherited from BusSignal (see Note above) ###################
        ## parent context (an RTE application instance to resolve signal/variable paths)
        self.context = None
        ## base path to signal below BusSystems
        self.signal_path = None
        ## reference to associated EthEvent instance
        self.event = None
        
        ## unit of physical signal value (as string, mainly used for report entries)
        self.unit = None
        ## bus signal alias name
        self.alias = None
        ## signal description text
        self.descr = None
        ## lookup-table for mapping discrete signal states to textual descriptions
        self.lookup = None
        
        
        # timings #############################################################
        ## cycle time of signal in [ms]
        self.cycle_time = None
        ## minimum debounce delay for triggered signals in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        # #####################################################################
        _bus_signals_ethbs.CrcEthSignal.__init__(
            self, context=context, 
            base_path=base_path, event=event, 
            cycle_time=cycle_time, debounce_time=debounce_time, 
            alias=alias, descr=descr, 
            error_delay=error_delay, change_delay=change_delay, 
            timeout=timeout, recovery_time=recovery_time,
            **kwargs
        ) 
    
    # #########################################################################
    def setBasicCrcError(self):
        """ Switch CRC calculation to an algorithm producing incorrect CRCs. """
        _bus_signals_ethbs.CrcEthSignal.setBasicCrcError(self)
    
    # #########################################################################
    def clearBasicCrcError(self):
        """ Clear a currently active CRC error injection """
        _bus_signals_ethbs.CrcEthSignal.clearBasicCrcError(self)
        
    
    # #########################################################################
    # Methods inherited from RxEthSignal
    # #########################################################################
    def enableHilTx(self):
        """ Enable transmission of signal HIL => DUT (if the assigned EthEvent
            supports it).
            
            Note: This enables transmission of all signals in the parent Event.
        """
        _bus_signals_ethbs.CrcEthSignal.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable transmission of signal HIL => DUT (if the assigned EthEvent
            supports it). 
            
            Note: This disables transmission of all signals in the parent Event.
        """
        _bus_signals_ethbs.CrcEthSignal.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger sending of the Ethernet Event / Field. 
            Note: All other signals of the parent EthEvent also will be sent.
        """
        _bus_signals_ethbs.CrcEthSignal.kickout(self)
        
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/RxBusSignal
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable
            (typically not that useful for ECU-Rx/HIL-Tx AC-signals, though).
            
            Returns the current value from signal_var.
         """
        return _bus_signals_ethbs.CrcEthSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable. 
            Parameters:
                value - value to set
            Returns the previous value from signal_var.  
        """
        return _bus_signals_ethbs.CrcEthSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data. 
            (typically not that useful for ECU-Rx/HIL-Tx AC-signals, though).
            Returns the current state's description.
        """
        return _bus_signals_ethbs.CrcEthSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor.
            Parameters:
                state - named state to set
            Returns the previous state's description.
        """
        return _bus_signals_ethbs.CrcEthSignal.setState(self, state)
    
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
        return _bus_signals_ethbs.CrcEthSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. 
            Returns an info string.
        """
        return _bus_signals_ethbs.CrcEthSignal.info(self)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_ethbs.CrcEthSignal.reset(self, *args, **kwargs)
        

# #############################################################################
# [BusSystems] Alive Counter Signal (HIL => ECU)
# #############################################################################
class AcEthSignal(_bus_signals_ethbs.AcEthSignal):
    """ An alive counter Rx Ethernet signal/parameter (HIL PSI => ECU CSI) 
        for use with dSPACE Ethernet blockset.
        
        Note: This class expects a BusSystems path structure.
    """
    
    # #########################################################################
    def __init__(self, context, base_path, 
                 event=None, cycle_time=None, debounce_time=None,
                 alias="", descr="",
                 error_delay=None, change_delay=None, timeout=None, 
                 recovery_time=None,
                 **kwargs):
        """ Alive counter signal initialization for dSPACE Ethernet blockset.
            
            Example: Alive Counter Signal Path Structure:
                BusSystems/Ethernet/FRR/PSIs/ACME.ENVIRONMENTALMODEL/ObjectFusionFront_1/Events/ObjectPosition/E2E Protection/counter/Counter/Calculated Value
                BusSystems/Ethernet/FRR/PSIs/ACME.ENVIRONMENTALMODEL/ObjectFusionFront_1/Events/ObjectPosition/E2E Protection/counter/Counter/Enable
                BusSystems/Ethernet/FRR/PSIs/ACME.ENVIRONMENTALMODEL/ObjectFusionFront_1/Events/ObjectPosition/E2E Protection/counter/Counter/Offset
                BusSystems/Ethernet/FRR/PSIs/ACME.ENVIRONMENTALMODEL/ObjectFusionFront_1/Events/ObjectPosition/E2E Protection/counter/Counter/Runtime Behavior
                BusSystems/Ethernet/FRR/PSIs/ACME.ENVIRONMENTALMODEL/ObjectFusionFront_1/Events/ObjectPosition/E2E Protection/counter/Source Switch
                BusSystems/Ethernet/FRR/PSIs/ACME.ENVIRONMENTALMODEL/ObjectFusionFront_1/Events/ObjectPosition/E2E Protection/counter/Value
                # or
                BusSystems/Ethernet/FRR/PSIs/ACME.DASS/RadarData_1/Events/LaneInfo/E2E Protection/counter/Counter/Calculated Value
                BusSystems/Ethernet/FRR/PSIs/ACME.DASS/RadarData_1/Events/LaneInfo/E2E Protection/counter/Counter/Enable
                BusSystems/Ethernet/FRR/PSIs/ACME.DASS/RadarData_1/Events/LaneInfo/E2E Protection/counter/Counter/Offset
                BusSystems/Ethernet/FRR/PSIs/ACME.DASS/RadarData_1/Events/LaneInfo/E2E Protection/counter/Counter/Runtime Behavior
                BusSystems/Ethernet/FRR/PSIs/ACME.DASS/RadarData_1/Events/LaneInfo/E2E Protection/counter/Source Switch
                BusSystems/Ethernet/FRR/PSIs/ACME.DASS/RadarData_1/Events/LaneInfo/E2E Protection/counter/Tx Inspect/Available SL Value
                BusSystems/Ethernet/FRR/PSIs/ACME.DASS/RadarData_1/Events/LaneInfo/E2E Protection/counter/Tx Inspect/Tx Value
                BusSystems/Ethernet/FRR/PSIs/ACME.DASS/RadarData_1/Events/LaneInfo/E2E Protection/counter/Value
            
            Info: Suitable base_paths / examples:
                BusSystems/Ethernet/FRR/PSIs/ACME.DASS/RadarData/Events/LaneInfo/E2E Protection/counter/Counter/Enable
                BusSystems/Ethernet/FRR/PSIs/ACME.DASS/RadarData/Events/LaneInfo/E2E Protection/counter/Value
                => anything below .../Counter/* or the .../Value entry
            
            Parameters:
                context         - rtplib Application or XilTestbench instance
                base_path       - base model path (below BusSystems) from which 
                                  all required paths will be derived.
                event           - reference to associated EthEvent instance
                cycle_time      - (opt) cycle time in [ms], overrides settings in EthEvent
                debounce_time   - (opt) minimum debounce delay time between events in [ms],
                                        overrides settings in EthEvent
                alias           - (opt) bus signal alias/name
                descr           - (opt) signal description
                error_delay     - (opt) delay to wait until a simple alive counter
                                        error should be detected [ms],
                                        defaults to 10x cycle time
                change_delay    - (opt) delay to wait after a value change [ms], 
                                        defaults to 2x cycle_time
                timeout         - (opt) detection time for timeout errors [ms], 
                                        defaults to 2x cycle_time
                recovery_time   - (opt) time for recovery/"wiedergut" checks [ms],
                                        defaults to 2x cycle_time
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so auto-complete may find them even 
        #       if the base class code cannot be analyzed.
        
        ## delay [ms] to wait until a basic Alive Counter error (like "AC stopped")
        #  should be detected. This will be used in test functions.
        self.error_delay = None
        
        ## Counter Runtime Behavior variable (a HilVar instance)
        # * 0: "The alive counter runs independently of the selected source 
        #       for the signal (see switch_var)"
        # * 1: counter running  
        #      "The alive counter runs only if its value is really sent 
        #       (Switch is 2 or 12). If it is switched to another source than 
        #       the alive counter, for example, a value from the Simulink 
        #       model, the alive counter stops."
        # * 2: counter stopped (at current value)  
        #      "The alive counter stops at the current value."
        self.ac_runtime_behavior_var = None
        
        ## Counter Offset variable.
        # Permits to add an offset to the value of the alive counter at run time.
        self.ac_offset_var = None
        
        ## ac_switch_var is only defined for backwards-compatibility to CANMMBS variant
        # Runtime Behavior entry is used as AC enable/disable switch
        self.ac_switch_var = None
        
        # Members inherited from BusSignal (see Note above) ###################
        ## parent context (an RTE application instance to resolve signal/variable paths)
        self.context = None
        ## base path to signal below BusSystems
        self.signal_path = None
        ## reference to associated EthEvent instance
        self.event = None
        
        ## unit of physical signal value (as string, mainly used for report entries)
        self.unit = None
        ## bus signal alias name
        self.alias = None
        ## signal description text
        self.descr = None
        ## lookup-table for mapping discrete signal states to textual descriptions
        self.lookup = None
        
        
        # timings #############################################################
        ## cycle time of signal in [ms]
        self.cycle_time = None
        ## minimum debounce delay for triggered signals in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        # #####################################################################
        _bus_signals_ethbs.AcEthSignal.__init__(self, context=context, 
            base_path=base_path, event=event, 
            cycle_time=cycle_time, debounce_time=debounce_time, 
            alias=alias, descr=descr, 
            error_delay=error_delay, change_delay=change_delay, 
            timeout=timeout, recovery_time=recovery_time,
            **kwargs
        )
    
    # #########################################################################
    def setBasicAcError(self):
        """ Stop and hold Alive Counter at the current count. """
        _bus_signals_ethbs.AcEthSignal.setBasicAcError(self)
    
    # #########################################################################
    def clearBasicAcError(self):
        """ (Re-)enable normal Alive Counter behaviour (continue counting)."""
        _bus_signals_ethbs.AcEthSignal.clearBasicAcError(self)
        
    
    # #########################################################################
    # Methods inherited from RxEthSignal
    # #########################################################################
    def enableHilTx(self):
        """ Enable transmission of signal HIL => DUT (if the assigned EthEvent
            supports it). 
            
            Note: This enables transmission of all signals in the parent Event.
        """
        _bus_signals_ethbs.AcEthSignal.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable transmission of signal HIL => DUT (if the assigned EthEvent
            supports it). 
            Note: This disables transmission of all signals in the parent Event.
        """
        _bus_signals_ethbs.AcEthSignal.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger sending of the Ethernet Event / Field. 
            Note: All other signals of the parent EthEvent also will be sent.
        """
        _bus_signals_ethbs.AcEthSignal.kickout(self)
        
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/RxBusSignal
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable
            (typically not that useful for ECU-Rx/HIL-Tx AC-signals, though).
            
            Returns the current value from signal_var.
         """
        return _bus_signals_ethbs.AcEthSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable. 
            Parameters:
                value - value to be set
            Returns the original value before the set operation occurred. 
        """
        return _bus_signals_ethbs.AcEthSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data. 
            (typically not that useful for ECU-Rx/HIL-Tx AC-signals, though).
            Returns the current state's description.
        """
        return _bus_signals_ethbs.AcEthSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. 
            This uses the lookup values supplied in constructor.
            Parameters:
                state - named state to set
            Returns the previous state's description.
        """
        return _bus_signals_ethbs.AcEthSignal.setState(self, state)
    
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
        return _bus_signals_ethbs.AcEthSignal.getStateDescr(self, value=value, fallback=fallback)
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. 
            Returns an info string.
        """
        return _bus_signals_ethbs.AcEthSignal.info(self)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_ethbs.AcEthSignal.reset(self, *args, **kwargs)
        

# #############################################################################
# Signal Container
# #############################################################################
class EthSignalContainer(_bus_signals_ethbs.EthSignalContainer):
    """ A container for Ethernet Signals """
    
    # #########################################################################
    def __init__(self, context):
        """ Override to add signals.
            
            Parameters:
                context - context used for contained BusSignals
        """
        _bus_signals_ethbs.EthSignalContainer.__init__(self, context)
    
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
        _bus_signals_ethbs.EthSignalContainer.resetAll(
            self, 
            verbosity=verbosity, 
            recursion_depth=recursion_depth
        )
    
    # #########################################################################
    def iterSignals(self, event):
        """ Iterate over all signals that reference the specified EthEvent.
            
            Parameters:
                event - an EthEvent instance
            
            Usage:
                for sig in eth.iterSignals(eth.evt_FRR_ACME_DASS_AWA_ESAssist)
                    print sig
            
            Returns an iterator object.
        """
        return _bus_signals_ethbs.EthSignalContainer.iterSignals(self, event)
        

# #############################################################################
# Alias(es) for previous (and incorrect) nomenclature for backwards compatibility
# @cond DOXYGEN_IGNORE 
EthEventGroup = RxEthEvent
# @endcond DOXYGEN_IGNORE


# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    import time
    if False:
        import ttk_tools.dspace.rtplib_offline_stub as rtplib
        ctx = rtplib.Appl("foo.sdf", "ds1701", "Offline")
    else:
        import ttk_tools.dspace.xil_api_offline_stub as xil_api
        ctx = xil_api.XilTestbench("fnord.xml", product_version="1895-B")
        
    
    # #########################################################################
    class EthSignals(EthSignalContainer):
        def __init__(self, context):
            ctx = context
            # Ethernet Events (ECU => HIL)
            self.evt_FRR_ACME_DASS_RadarControl_1_CtrlWarnPointIbrake            = TxEthEvent(ctx, cycle_time=100, debounce_time=20)
            
            # Ethernet Events (HIL => ECU) ###################################################################################
            self.evt_FRR_ACME_DASS_AWA_1_EmergencySteerAssist                    = RxEthEvent(ctx, "Model Root/ETH/IO/Protocols/ETHERNET/RTIETHERNETCONFIG\nECU Services/FRR/FRR_ACME_DASS_AWA_1_PSI/FRR_ACME_DASS_AWA_1_EmergencySteerAssist_TX_Event_MAPPING/TxEnable/Value",                                          "Model Root/ETH/IO/Protocols/ETHERNET/RTIETHERNETCONFIG\nECU Services/FRR/FRR_ACME_DASS_AWA_1_PSI/FRR_ACME_DASS_AWA_1_EmergencySteerAssist_TX_Event_MAPPING/TxTrigger/Value",                                       cycle_time=0, debounce_time=55, alias="Event FRR_ACME_DASS_AWA_1_EmergencySteerAssist") # noqa 501
            self.evt_FRR_ACME_DASS_BrakeAssistFrontRadar_1_BrakeAssistFrontRadar = RxEthEvent(ctx, "Model Root/ETH/IO/Protocols/ETHERNET/RTIETHERNETCONFIG\nECU Services/FRR/FRR_ACME_DASS_BrakeAssistFrontRadar_1_PSI/FRR_ACME_DASS_BrakeAssistFrontRadar_1_BrakeAssistFrontRadar_TX_Event_MAPPING/TxEnable/Value",     "Model Root/ETH/IO/Protocols/ETHERNET/RTIETHERNETCONFIG\nECU Services/FRR/FRR_ACME_DASS_BrakeAssistFrontRadar_1_PSI/FRR_ACME_DASS_BrakeAssistFrontRadar_1_BrakeAssistFrontRadar_TX_Event_MAPPING/TxTrigger/Value",  cycle_time=0, debounce_time=40, alias="Event FRR_ACME_DASS_BrakeAssistFrontRadar_1_BrakeAssistFrontRadar") # noqa 501
            self.evt_FRR_ACME_DASS_RadarData_1_LaneInfo                          = RxEthEvent(ctx, "Model Root/ETH/IO/Protocols/ETHERNET/RTIETHERNETCONFIG\nECU Services/FRR/FRR_ACME_DASS_RadarData_1_PSI/FRR_ACME_DASS_RadarData_1_LaneInfo_TX_Event_MAPPING/TxEnable/Value",                                          "Model Root/ETH/IO/Protocols/ETHERNET/RTIETHERNETCONFIG\nECU Services/FRR/FRR_ACME_DASS_RadarData_1_PSI/FRR_ACME_DASS_RadarData_1_LaneInfo_TX_Event_MAPPING/TxTrigger/Value",                                       cycle_time=0, debounce_time=45, alias="Event FRR_ACME_DASS_RadarData_1_LaneInfo") # noqa 501
            
            # Ethernet Signals/Parameters (HIL => ECU) #######################################################################
            self.BrakeAssistFrontRadar_activeFunction = RxEthSignal(ctx, "Model Root/ETH/IO/Protocols/ETHERNET/RTIETHERNETCONFIG\nECU Services/FRR/FRR_ACME_DASS_BrakeAssistFrontRadar_1_PSI/FRR_ACME_DASS_BrakeAssistFrontRadar_1_BrakeAssistFrontRadar_TX_Params_MAPPING/activeFunction/activeFunction_Value/Value", event=self.evt_FRR_ACME_DASS_BrakeAssistFrontRadar_1_BrakeAssistFrontRadar, alias="BrakeAssistFrontRadar_activeFunction") # noqa 501
            self.BrakeAssistFrontRadar_counter        = RxEthSignal(ctx, "Model Root/ETH/IO/Protocols/ETHERNET/RTIETHERNETCONFIG\nECU Services/FRR/FRR_ACME_DASS_BrakeAssistFrontRadar_1_PSI/FRR_ACME_DASS_BrakeAssistFrontRadar_1_BrakeAssistFrontRadar_TX_Params_MAPPING/counter/counter_Value/Value",               event=self.evt_FRR_ACME_DASS_BrakeAssistFrontRadar_1_BrakeAssistFrontRadar, alias="BrakeAssistFrontRadar_counter")        # noqa 501
            self.BrakeAssistFrontRadar_cRC            = RxEthSignal(ctx, "Model Root/ETH/IO/Protocols/ETHERNET/RTIETHERNETCONFIG\nECU Services/FRR/FRR_ACME_DASS_BrakeAssistFrontRadar_1_PSI/FRR_ACME_DASS_BrakeAssistFrontRadar_1_BrakeAssistFrontRadar_TX_Params_MAPPING/cRC/cRC_Value/Value",                       event=self.evt_FRR_ACME_DASS_BrakeAssistFrontRadar_1_BrakeAssistFrontRadar, alias="BrakeAssistFrontRadar_cRC")            # noqa 501
            
            # Ethernet Signals/Parameters (ECU => HIL) #######################################################################
            self.FRR_CtrlWarnPointIbrake_EvasionMvmntLeft  = TxEthSignal(ctx, "Model Root/ETH/IO/Protocols/Ethernet/RTIETHERNETCONFIG\nECU Services/FRR/FRR_ACME_DASS_RadarControl_1_CSI/FRR_ACME_DASS_RadarControl_1_CtrlWarnPointIbrake_RX_Params_MAPPING/EvasionMvmntLeft/EvasionMvmntLeft_Value/Out1",      cycle_time=100, alias="FRR_CtrlWarnPointIbrake_EvasionMvmntLeft")                                                                # noqa 501
            self.FRR_CtrlWarnPointIbrake_EvasionMvmntRight = TxEthSignal(ctx, "Model Root/ETH/IO/Protocols/Ethernet/RTIETHERNETCONFIG\nECU Services/FRR/FRR_ACME_DASS_RadarControl_1_CSI/FRR_ACME_DASS_RadarControl_1_CtrlWarnPointIbrake_RX_Params_MAPPING/EvasionMvmntRight/EvasionMvmntRight_Value/Out1",    event=self.evt_FRR_ACME_DASS_RadarControl_1_CtrlWarnPointIbrake, alias="FRR_CtrlWarnPointIbrake_EvasionMvmntRight")              # noqa 501
            
            # E2E CRC Status (ECU => HIL) ####################################################################################
            self.e2e_RadarControl1_crc_status         = CrcEthStatus(ctx, "BusSystems/Ethernet/FRR/CSIs/ACME.DASS/RadarControl_1/Events/RadarControl1/E2E Protection/cRC/Value", alias="e2e_RadarControl1_crc_status", descr="E2E CRC status for RadarControl1")      # noqa 501
            self.e2e_RadarControl2_crc_status         = CrcEthStatus(ctx, "BusSystems/Ethernet/FRR/CSIs/ACME.DASS/RadarControl_1/Events/RadarControl2/E2E Protection/cRC/CRC/Status", alias="e2e_RadarControl2_crc_status", descr="E2E CRC status for RadarControl2") # noqa 501
            
            # E2E CRC Signals (HIL => ECU) ###################################################################################
            self.e2e_BrakeAssistFrontRadar_crc        = CrcEthSignal(ctx, "BusSystems/Ethernet/FRR/PSIs/ACME.DASS/BrakeAssistFrontRadar_1/Events/BrakeAssistFrontRadar/E2E Protection/cRC/CRC/Enable",        event=self.evt_FRR_ACME_DASS_BrakeAssistFrontRadar_1_BrakeAssistFrontRadar,  alias="e2e_BrakeAssistFrontRadar_crc", descr="E2E CRC for BrakeAssistFrontRadar")    # noqa 501
            self.e2e_LaneInfo_crc                     = CrcEthSignal(ctx, "BusSystems/Ethernet/FRR/PSIs/ACME.DASS/RadarData_1/Events/LaneInfo/E2E Protection/cRC/CRC/Enable",                                 event=self.evt_FRR_ACME_DASS_RadarData_1_LaneInfo,                           alias="e2e_LaneInfo_crc",              descr="E2E CRC for LaneInfo")                 # noqa 501
            
            # E2E Alive Counter Signals (HIL => ECU) #########################################################################
            self.e2e_BrakeAssistFrontRadar_counter    = AcEthSignal(ctx,  "BusSystems/Ethernet/FRR/PSIs/ACME.DASS/BrakeAssistFrontRadar_1/Events/BrakeAssistFrontRadar/E2E Protection/counter/Counter/Enable", event=self.evt_FRR_ACME_DASS_BrakeAssistFrontRadar_1_BrakeAssistFrontRadar, alias="e2e_BrakeAssistFrontRadar_counter", descr="E2E AC for BrakeAssistFrontRadar") # noqa 501
            self.e2e_LaneInfo_counter                 = AcEthSignal(ctx,  "BusSystems/Ethernet/FRR/PSIs/ACME.DASS/RadarData_1/Events/LaneInfo/E2E Protection/counter/Counter/Enable",                          event=self.evt_FRR_ACME_DASS_RadarData_1_LaneInfo,                          alias="e2e_LaneInfo_counter",              descr="E2E AC for LaneInfo")              # noqa 501
            
    
    print "== EthSignalContainer with signals ================================"
    eth = EthSignals(ctx)
    
    print "# initial values:"
    print eth.BrakeAssistFrontRadar_activeFunction.info()
    print eth.BrakeAssistFrontRadar_counter.info()
    print eth.BrakeAssistFrontRadar_cRC.info()
    
    print eth.e2e_BrakeAssistFrontRadar_crc.info()
    print eth.e2e_BrakeAssistFrontRadar_counter.info()
    
    eth.BrakeAssistFrontRadar_activeFunction.set(1234)
    eth.BrakeAssistFrontRadar_counter.set(1000)
    eth.BrakeAssistFrontRadar_cRC.set(0xAABBCCDD)
    eth.e2e_BrakeAssistFrontRadar_crc.setBasicCrcError() # not that it makes any difference while offline
    eth.e2e_BrakeAssistFrontRadar_counter.setBasicAcError()
    
    time.sleep(eth.BrakeAssistFrontRadar_activeFunction.cycle_time / 1000.0)
    
    
    print "# changed values:"
    print eth.BrakeAssistFrontRadar_activeFunction.info()
    print eth.BrakeAssistFrontRadar_counter.info()
    print eth.BrakeAssistFrontRadar_cRC.info()
    
    print eth.e2e_BrakeAssistFrontRadar_crc.info()
    print eth.e2e_BrakeAssistFrontRadar_counter.info()
    
    print "# resetting container:"
    eth.resetAll(verbosity=2)
    
    print "# after reset:"
    print eth.BrakeAssistFrontRadar_activeFunction.info()
    print eth.BrakeAssistFrontRadar_counter.info()
    print eth.BrakeAssistFrontRadar_cRC.info()
    
    print eth.e2e_BrakeAssistFrontRadar_crc.info()
    print eth.e2e_BrakeAssistFrontRadar_counter.info()
    
    eth.e2e_BrakeAssistFrontRadar_crc.clearBasicCrcError() 
    eth.e2e_BrakeAssistFrontRadar_counter.clearBasicAcError()
    
    
    print
    print "== iterSignals ===================================================="
    evt = eth.evt_FRR_ACME_DASS_RadarData_1_LaneInfo
    print '# Signals in event ("%s"):'%(evt)
    for sig in eth.iterSignals(evt):
        print sig
    
    print "\nDone."

# @endcond DOXYGEN_IGNORE
# #############################################################################