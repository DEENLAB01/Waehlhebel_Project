#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : bus_signals_canmmbs.py
# Package : ttk_bus
# Task    : Wrapper classes for bus/interface signal descriptions.
#           Specific implementation for dSpace CAN Multi-Message blocksets 
#           (using "trc"-signals added to BusSystems)
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
# 1.0  | 26.08.2013 | J.Tremmel | initial
# 1.1  | 13.03.2015 | L.Morgus  | expanded descriptions and examples
# 1.2  | 11.12.2015 | J.Tremmel | some cleanup, update for _bus_signals_canmmbs 1.7
# 1.3  | 02.03.2016 | J.Tremmel | update for _bus_signals_canmmbs 1.9
# 1.4  | 11.03.2016 | J.Tremmel | update for _bus_signals_canmmbs 1.10, added CanBusSignalContainer
# 1.5  | 18.03.2016 | J.Tremmel | fixed missing parameter in _RxCanBusMessage call
#                               | and leftover (premature) switch_var assignment in AcCanBusSignal
# 1.6  | 25.11.2016 | J.Tremmel | updated interface methods
# 1.7  | 29.08.2017 | J.Tremmel | added interface descriptions for getStateDescription methods
# 1.8  | 15.07.2020 | J.Tremmel | removed obsolete signal parameters min/max_value
#******************************************************************************
"""
@package ttk_bus.bus_signals_canmmbs
Interface wrapper bus/interface signal classes in ttk_bus._bus_signals_canmmbs.
Specific implementation for dSpace CAN Multi-Message blocksets 
(using "trc"-signals added to BusSystems)

Convention:  
    Signal directions are relative to the DUT:
      * Tx - transmitted by ECU => received from HIL
      * Rx - received by ECU <= transmitted from HIL
    
"""
import _bus_signals_canmmbs

# #############################################################################
# Sample BusSystem structure:
#
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/ALIV_CLRC_SEG_00_LH_SIDE_RADA
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/CHL_CLRC_SEG_00_SIDE_LH_RADA
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/CLRC_CTY_00_SIDE_LH_RADA
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/CLRC_DIST_00_SIDE_LH_RADA
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/CLRC_SEG_00_SIDE_LH_RADA_CheckEnable
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/CLRC_SEG_00_SIDE_LH_RADA_CycleTime
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/CLRC_SEG_00_SIDE_LH_RADA_DelayTime
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/CLRC_SEG_00_SIDE_LH_RADA_Enable
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/CLRC_SEG_00_SIDE_LH_RADA_Kickout
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/CLRC_SEG_00_SIDE_LH_RADA_PeriodicalOn
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/CLRC_SEG_00_SIDE_LH_RADA_status
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/CLRC_SEG_ID_00_SIDE_LH_RADA
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/CRC_CLRC_SEG_00_SIDE_LH_RADA
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/SBS_PRO_CLRC_SEG_00_LH_SIDE_RADA
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/ST_CLRC_MEASMT_00_LH_SIDE_RADA
# masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/ST_CLRC_MOV_00_SIDE_LH_RADA
#
# #############################################################################


# #############################################################################
class TxCanBusMessage(_bus_signals_canmmbs.TxCanBusMessage):
    """ CAN Message/PDU ECU-Tx (ECU-Tx => HIL-Rx).
        Extends the basic CanBusMessage with access to time_var (rx time of 
        message) and deltatime_var (rx delta time of message)
    """
    # #########################################################################
    def __init__(self, context, bus_systems_path=None, 
                 cycle_time=0, debounce_time=0,
                 alias="", descr='',
                 change_delay=None, timeout=None, recovery_time=None):
        """ Tx CAN Message data (ECU-Tx => HIL-Rx).
            
            Parameters:
                context           - parent context (an RTE application instance to 
                                    resolve signal/variable paths)
                
                bus_systems_path  - base path to PDU/message below BusSystems,
                                    use `BusSystems/CAN/<CAN_NAME>/<MSG_NAME>/RX/<MSG_NAME>`  
                                    Helper entries will be derived from this path,
                                    e.g. kickout or status variables (though this is more 
                                    relevant to messages sent to DUT, see RxCanBusMessage)
                
                cycle_time        - cycle time in [ms]. Event-triggered messages 
                                    have a cycle time of 0 (similar to DBC value)
                debounce_time     - minimum debounce delay between events in [ms]
                alias             - Message alias/name
                descr             - (opt) Message description (may be used in report entries)
                
                change_delay      - (opt) delay to wait after a value change [ms],  
                                          defaults to 2x max(cycle_time, debounce_time)
                timeout           - (opt) detection time for timeout errors [ms],  
                                          defaults to 2x max(cycle_time, debounce_time)
                recovery_time     - (opt) time for recovery/"wiedergut" checks [ms],  
                                          defaults to 2x max(cycle_time, debounce_time)
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class code cannot be analyzed.
        
        ## Message Rx delta time variable.
        # Time between current and previous received message in seconds
        # (a HilVar instance)
        self.deltatime_var = None
        
        ## Message Rx time variable (in seconds)
        # (a HilVar instance)
        self.time_var = None
        
        # Members inherited from CanBusMessage (see Note above) ###############
        ## HIL-Rx-status variable
        # (a HilVar instance)
        self.status_var = None
        
        ## Parent context (an RTE application instance to resolve signal/variable paths)
        self.context = None
        ## Message alias name
        self.alias = None
        ## Message description text
        self.descr = None
        
        ## Base BusSystems path to Message/PDU helper variables below BusSystems
        #  e.g. "BusSystems/CAN/<CAN_NAME>/<MSG_NAME>/RX/<MSG_NAME>"
        self.bus_systems_path = None
        
        # timings #############################################################
        ## cycle time of Message/PDU in [ms]
        self.cycle_time = None
        ## minimum debounce delay for event-triggered Messages/PDUs in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        # #####################################################################
        _bus_signals_canmmbs.TxCanBusMessage.__init__(
            self, context=context, 
            bus_systems_path=bus_systems_path, 
            
            cycle_time=cycle_time, debounce_time=debounce_time, 
            
            alias=alias, descr=descr, 
            
            change_delay=change_delay, 
            timeout=timeout, 
            recovery_time=recovery_time
        )
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs): # @UnusedVariable *args, **kwargs (just to tolerate optional parameters)
        """ Call reset() on all contained variables/signals that support it.
            Simple, non-recursive approach.
        """
        _bus_signals_canmmbs.TxCanBusMessage.reset(self)
        

# #############################################################################
class RxCanBusMessage(_bus_signals_canmmbs.RxCanBusMessage):
    """ CAN Message/PDU ECU-Rx (HIL-Tx => ECU-Rx).
        Extends the basic CanBusMessage with methods for enableHilTx/disableHilTx 
        and message kickout (trigger).
    """
    
    ## Configuration setting for new instances:  
    # Custom "hard" default values to use for internal real time system 
    # variables, so a reset() will always reset those variables to defined 
    # values (and not just those variables that were set/accessed). 
    #
    # This might be helpful if "other" tests fail to properly clean up the
    # test environment after they are done.
    # 
    # Mapping: <variable name as string>: <default value>
    #
    # A value of None (or a missing variable name) enables normal/automatic 
    # reset behavior.
    #
    # Typical default values:
    # - Enable variables are usually default to "enabled"
    #    * 0: disabled
    #    * 1: enabled
    # - Message/PDU (Hil-TX) cycle time access:  
    #   Default value depends on configured cycle time (in [s]).  
    #   Override standard behavior only if absolutely necessary.
    # - Kickout/trigger variables:  
    #   Triggers below BusSystems should auto-reset to 0 once the PDU has been 
    #   triggered. 0 is a safe default.
    cfg_custom_defaults = {
        "enable_var":       None,
        "kickout_var":      None,
        "cycle_time_var":   None,
    }
    
    # #########################################################################
    def __init__(self, context, enable_path=None, bus_systems_path=None, 
                 cycle_time=0, debounce_time=0,
                 alias="", descr='',
                 change_delay=None, timeout=None, recovery_time=None):
        """ Rx CAN Message/PDU data (HIL-Tx => ECU-Rx).
            
            Parameters:
                context           - parent context (an RTE application instance 
                                    to resolve signal/variable paths)
                enable_path       - manual path to a tx enable switch. Keep at None
                                    to use default enable switch below BusSystems
                                    (see parameter bus_systems_path).
                                    The enable variable will later be set to 1 
                                    to enable or to 0 to disable message 
                                    transmission.
                
                bus_systems_path  - base path to PDU/message below BusSystems,  
                                    use "BusSystems/CAN/<CAN_NAME>/<MSG_NAME>/TX/<MSG_NAME>"  
                                    or  "BusSystems/CAN/<CAN_NAME>/<MSG_NAME>/TX/<MSG_NAME>_Enable"  
                                    Helper entries will be derived from this path,
                                    e.g. kickout or status variables.
                
                cycle_time        - cycle time in [ms]. Event-triggered messages 
                                    have a cycle time of 0 (similar to DBC value)
                debounce_time     - minimum debounce delay between events in [ms]
                alias             - Message alias/name
                descr             - (opt) Message description (may be used in report entries)
                
                change_delay      - (opt) delay to wait after a value change [ms],  
                                          defaults to 2x max(cycle_time, debounce_time)
                timeout           - (opt) detection time for timeout errors [ms],  
                                          defaults to 2x max(cycle_time, debounce_time)
                recovery_time     - (opt) time for recovery/"wiedergut" checks [ms],  
                                          defaults to 2x max(cycle_time, debounce_time)
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class code cannot be analyzed.
        
        ## HIL-Tx-enable/disable variable
        # (a HilVar instance)
        self.enable_var = None
        
        ## HIL-Tx-kickout variable
        # (a HilVar instance)
        self.kickout_var = None
        
        ## HIL-Tx-cycle_time variable (currently active cycle time in [s])
        # (a HilVar instance)
        self.cycle_time_var = None
        
        # Members inherited from CanBusMessage (see Note above) ###############
        ## HIL-Tx-status variable
        # (a HilVar instance)
        self.status_var = None
        
        ## Parent context (an RTE application instance to resolve signal/variable paths)
        self.context = None
        ## Message alias name
        self.alias = None
        ## Message description text
        self.descr = None
        
        ## Base BusSystems path to Message/PDU helper variables below BusSystems
        #  e.g. "BusSystems/CAN/<CAN_NAME>/<MSG_NAME>/TX/<MSG_NAME>"
        self.bus_systems_path = None
        
        # timings #############################################################
        ## cycle time of Message/PDU in [ms]
        self.cycle_time = None
        ## minimum debounce delay for event-triggered Messages/PDUs in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        # #####################################################################
        _bus_signals_canmmbs.RxCanBusMessage.__init__(
            self, context=context, 
            enable_path=enable_path, bus_systems_path=bus_systems_path,
            
            cycle_time=cycle_time, debounce_time=debounce_time, 
            
            alias=alias, descr=descr, 
            
            change_delay=change_delay, 
            timeout=timeout, 
            recovery_time=recovery_time
        )
    
    # #########################################################################
    def enableHilTx(self):
        """ (Re-)enable sending of this Message/PDU. """
        _bus_signals_canmmbs.RxCanBusMessage.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable sending of this Message/PDU. """
        _bus_signals_canmmbs.RxCanBusMessage.disableHilTx(self)
    
    # #########################################################################
    def kickout(self, delay_ms=None):
        """ Trigger sending of this CAN-Message/PDU. 
            
            Parameters: 
                delay_ms - [ms] Delay to wait before clearing kickout/trigger 
                           variable again (it _should_ auto-reset if trigger 
                           variable is located below BusSystems, but anyway).
            
            Info: Default Delay:
               Delay defaults to 1/2 self.debounce_time (if explicitly set) 
               or alternatively to 1/2 self.change_delay.  
               Default delay will never be shorter than 5 ms.
        """
        _bus_signals_canmmbs.RxCanBusMessage.kickout(self, delay_ms=delay_ms)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs): 
        """ Call reset() on all contained variables/signals that support it.
            Simple, non-recursive approach.
        """
        _bus_signals_canmmbs.RxCanBusMessage.reset(self, *args, **kwargs)
        

# #############################################################################
class TxCanBusSignal(_bus_signals_canmmbs.TxCanBusSignal):
    """ A CAN signal sent from the DUT to the test system (ECU Tx => HIL Rx). 
        See _bus_signals_canmmbs.CanBusSignal.
    """
    # #########################################################################
    def __init__(self, context, signal_path, 
                 message=None, cycle_time=None, debounce_time=None,
                 unit="", alias="", descr="", lookup=None,
                 change_delay=None, timeout=None, recovery_time=None):
        """ Tx bus signal initialization.
            
            Parameters:
                context       - parent context (an RTE application instance to 
                                resolve signal/variable paths)
                signal_path   - base path to signal value below BusSystems
                message       - reference to associated CanBusMessage instance
                cycle_time    - (opt) cycle time in [ms], overrides settings in Message
                debounce_time - (opt) minimum debounce delay between events in [ms],
                                      overrides settings in Message
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
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class' code cannot be analyzed.
        
        
        # Members inherited from CanBusSignal (see Note above) ################
        
        ## Signal model path as base path for deriving sub-element paths.
        # For CANMM signals, related variables follow the form 
        # <path_to_signal>_suffix
        self.base_path = None
        ## reference to associated (Tx-)CanBusMessage instance
        self.message = None
        
        # Members inherited from BusSignal (see Note above) ###################
        
        ## signal value variable. get/info methods of this TxCanBusSignal
        # will access this variable.
        # (a HilVar instance)
        self.signal_var = None
        ## parent context (an RTE application instance to resolve signal/variable paths)
        self.context = None
        
        ## unit of physical signal value (as string, mainly used for report entries)
        self.unit  = None
        ## bus signal alias name
        self.alias = None
        ## bus signal description text
        self.descr = None
        
        # timings #############################################################
        ## cycle time of Message/PDU in [ms]
        self.cycle_time = None
        ## minimum debounce delay for event-triggered Messages/PDUs in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        # #####################################################################
        _bus_signals_canmmbs.TxCanBusSignal.__init__(
            self, context=context, 
            signal_path=signal_path, message=message,
            
            cycle_time=cycle_time, debounce_time=debounce_time,
            unit=unit, alias=alias, descr=descr, lookup=lookup,
            change_delay=change_delay, timeout=timeout, 
            recovery_time=recovery_time,
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable, 
            see signal_var
            Returns the current info string from signal_var.
        """
        return _bus_signals_canmmbs.TxCanBusSignal.info(self)
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable, see signal_var 
            Returns the current value from signal_var.
        """
        return _bus_signals_canmmbs.TxCanBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable, see signal_var
            
            Attention:
                For TxCanBusSignals this will only overwrite the current 
                contents of the HIl receive buffer of the signal
                (which is typically not too useful).
            
            Parameters:
                value - value to set
            
            Returns the previous value from signal_var.
        """
        return _bus_signals_canmmbs.TxCanBusSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data, 
            see signal_var. This uses the lookup values supplied in constructor.
            Fallback (if no matching state was found) will be the unmapped 
            numeric value.
            
            Returns the current state representation from signal_var.
        """
        return _bus_signals_canmmbs.TxCanBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable, see signal_var.
            This uses the lookup values supplied in constructor.
            
            Attention:
                For TxFrBusSignals this will only overwrite the current 
                contents of the HIl receive buffer of the signal 
                (which typically is not too useful).
            
            Parameters:
                state - named state to set
            
            Returns the previous state representation from signal_var.
        """
        return _bus_signals_canmmbs.TxCanBusSignal.setState(self, state)
    
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
        return _bus_signals_canmmbs.TxCanBusSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_canmmbs.TxCanBusSignal.reset(self, *args, **kwargs)
        

# #############################################################################
class RxCanBusSignal(_bus_signals_canmmbs.RxCanBusSignal):
    """ A CAN signal sent from the test system to the DUT (ECU Rx <= HIL Tx). 
        
        Note:
            RxCanBusSignal requires at least an available input manipulation 
            via TRC/BusSystems (which is the default setting in CANMM, but can 
            be disabled).
        
        See _bus_signals_canmmbs.CanBusSignal.
    """
    
    ## Configuration setting for new instances:  
    # Try to initialize (additional) variables that are only available if 
    # "dynamic values" input manipulation has been selected during RTICANMM 
    # configuration for a signal. 
    #
    # Additional variables:
    #  * dyncount_var
    #  * dynvalue_var
    #
    cfg_init_signal_manipulation = False
    
    ## Configuration setting for new instances:  
    # Custom "hard" default value(s) to use for internal real time system 
    # variables (e.g. switch settings), so a reset() will always reset those 
    # variables to defined values (and not just those variables that have 
    # actually been accessed).  
    # This might be helpful if "other" tests fail to properly clean up the
    # test environment after they are done.
    # 
    # Mapping: <variable name as string>: <default value>
    #
    # A value of None (or a missing variable name) enables normal/automatic 
    # reset behavior.
    #
    # Typical default values:
    # - Switch variable (signal manipulation)
    #   * 0: model input (if configured/available)
    #   * 1: constant from Trc/BusSystems 
    #   * 2: counter running (for counter signals, default switch setting for enabled counters)
    #   * 3: constant + counter (for counter signals)
    #   * 4: toggle value  (for toggle signals)
    #   * 5: parity value  (for parity signals)
    #   * 6: ~parity value (for parity signals)
    #   * 7: error value   (if an error value is configured)
    #   * 8: dynamic value (if dynamic value manipulation is configured) 
    # - Dynamic Countdown Value: Auto-decrements until 0 is reached if 
    #   signal manipulation switch is set to 8  
    #   => 0 would be a safe default value
    # - Dynamic Value: value that is active while dyncount_var decrements.
    #
    cfg_custom_defaults = {
        "switch_var":   None,
        "dyncount_var": None,
        "dynvalue_var": None,
    }
    
    
    # #########################################################################
    def __init__(self, context, signal_path, 
                 message=None, cycle_time=None, debounce_time=None,
                 unit="", alias="", descr="", lookup=None,
                 change_delay=None, timeout=None, recovery_time=None):
        """ Rx bus signal initialization.
            
            Parameters:
                context       - parent context (an RTE application instance to 
                                resolve signal/variable paths)
                signal_path   - base path to signal value below BusSystems
                message       - reference to associated CanBusMessage instance
                cycle_time    - (opt) cycle time in [ms], overrides settings in Message
                debounce_time - (opt) minimum debounce delay between events in [ms],
                                      overrides settings in Message
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
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class' code cannot be analyzed.
        
        ## Switch variable for signal manipulation. 
        # Only available if more than one signal manipulation option is 
        # configured in CANMM.
        #
        # Values:
        #  * 0: model input (if configured/available)
        #  * 1: constant from Trc/BusSystems 
        #  * 2: counter running (for counter signals, default switch setting for enabled counters)
        #  * 3: constant + counter (for counter signals)
        #  * 4: toggle value  (for toggle signals)
        #  * 5: parity value  (for parity signals)
        #  * 6: ~parity value (for parity signals)
        #  * 7: error value   (if an error value is configured)
        #  * 8: dynamic value (if dynamic value manipulation is configured)
        #
        self.switch_var = None
        
        ## Dynamic Countdown Value.
        # Only available if signal manipulation is configured in CANMM and 
        # enabled in class config.  
        # See self.cfg_init_signal_manipulation 
        self.dyncount_var = None
        
        ## Dynamic Value: value that is active while dyncount_var decrements.
        # Only available if signal manipulation is configured in CANMM and 
        # enabled in class config.  
        # See self.cfg_init_signal_manipulation 
        self.dynvalue_var = None
        
        # Members inherited from CanBusSignal (see Note above) ################
        
        ## Signal model path as base path for deriving sub-element paths.
        # For CANMM signals, related variables follow the form 
        # <path_to_signal>_suffix
        self.base_path = None
        ## reference to associated (Rx-)CanBusMessage instance
        self.message = None
        
        # Members inherited from BusSignal (see Note above) ###################
        
        ## signal value variable. get/info methods of this RxCanBusSignal
        # will access this variable.
        # (a HilVar instance)
        self.signal_var = None
        ## parent context (an RTE application instance to resolve signal/variable paths)
        self.context = None
        
        ## unit of physical signal value (as string, mainly used for report entries)
        self.unit  = None
        ## bus signal alias/name
        self.alias = None
        ## bus signal description text
        self.descr = None
        
        # timings #############################################################
        ## cycle time of Message/PDU in [ms]
        self.cycle_time = None
        ## minimum debounce delay for event-triggered Messages/PDUs in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        # #####################################################################
        _bus_signals_canmmbs.RxCanBusSignal.__init__(
            self, context=context, 
            signal_path=signal_path, message=message, 
            cycle_time=cycle_time, debounce_time=debounce_time, 
            unit=unit, alias=alias, descr=descr, lookup=lookup, 
            change_delay=change_delay, timeout=timeout, 
            recovery_time=recovery_time, 
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable, 
            see signal_var
            
            Attention:
                For RxCanBusSignals, this will show info on the contents 
                of the HIL-send-buffer (below BusSystems), not the value from
                Model/Simulink source nor the last seen signal value on CAN bus.
            
            Returns the current info string from signal_var.
        """
        return _bus_signals_canmmbs.RxCanBusSignal.info(self)
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable, see signal_var. 
            
            Attention:
                For RxCanBusSignals, this will get the current value of the 
                HIL-send-buffer (below BusSystems), not the last seen signal 
                value on CAN bus.
            
            Returns the current value from signal_var.
        """
        return _bus_signals_canmmbs.RxCanBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable below BusSystems
            (and switch the signal source to "BusSystems" if necessary).
            
            Parameters:
                value - new value to set
            
            Returns the previous value from signal_var.
        """
        _bus_signals_canmmbs.RxCanBusSignal.set(self, value=value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data, 
            see signal_var. This uses the lookup values supplied in constructor.
            Fallback (if no matching state was found) will be the unmapped 
            numeric value.
            
            Attention:
                For RxCanBusSignals, this will get the current value of the 
                HIL-send-buffer (below BusSystems), not the last seen signal 
                value on CAN bus.
            
            Returns the current state representation from signal_var.
        """
        return _bus_signals_canmmbs.RxCanBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable below BusSystems
            (and switches the signal source to "BusSystems" if necessary). 
            This uses the lookup values supplied in constructor.
            
            Parameters:
                state - named state to set
            
            Returns the previous value representation from signal_var.
        """
        return _bus_signals_canmmbs.RxCanBusSignal.setState(self, state=state)
    
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
        return _bus_signals_canmmbs.RxCanBusSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def enableHilTx(self):
        """ Enable transmission of signal HIL => DUT (if the assigned 
            CAN-Message/PDU supports it).
            
            Note:
                This will enable transmission of _all_ signals of the parent 
                Message/PDU.
        """
        return _bus_signals_canmmbs.RxCanBusSignal.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable transmission of signal HIL => DUT (if the assigned 
            CAN-Message/PDU supports it).
            
            Note:
                This will disable transmission of _all_ signals of the parent 
                Message/PDU.
        """
        return _bus_signals_canmmbs.RxCanBusSignal.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger transmission ("kickout") of signal HIL => DUT (by 
            triggering the parent CAN-Message/PDU). 
            
            Note:
                All other signals of the parent Message/PDU will also be sent.
        """
        return _bus_signals_canmmbs.RxCanBusSignal.kickout(self)
        
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. Note that this
            will also switch the variable source switch back to its original 
            setting.
        """
        # Note: inherited from ResettableContainer
        _bus_signals_canmmbs.RxCanBusSignal.reset(self, *args, **kwargs)
        

# #############################################################################
class CrcCanBusSignal(_bus_signals_canmmbs.CrcCanBusSignal):
    """ A CRC RX bus signal derived from RxCanBusSignal (HIL-Tx => ECU-Rx) 
        for use with dSPACE CAN Multi-Message blockset.
        See RxCanBusSignal for inherited methods.
    """
    
    ## Configuration setting for new instances:  
    #  CRC type for "correct" CRC algorithm (normal mode)
    cfg_crc_normal_type = 1
    
    ## Configuration setting for new instances:  
    # CRC type for "incorrect" CRC algorithm (for error injection, for example
    # calculated CRC + 1).  
    #
    # Note: 
    #    Simply switching CRC calculation off (e.g. CRC = 0x00) may lead to 
    #    detection failures, as a static CRC value might actually be correct 
    #    for the current data.  
    #
    cfg_crc_error_type  = 2
    
    ## Configuration setting for new instances:  
    # Try to initialize (additional) variables that are only available if 
    # "dynamic crc" manipulation has been selected during RTICANMM 
    # configuration for a signal.
    #
    # Additional variables:
    #  * .crc_dyntype_var
    #  * .crc_dyncount_var
    #
    cfg_init_crc_dynamic_manipulation = False
    
    ## Configuration setting for new instances:  
    # Custom "hard" default value(s) to use for internal real time system 
    # variables.
    # 
    # Mapping: <variable name as string>: <default value>
    #
    # A value of None (or a missing variable name) enables normal/automatic 
    # reset behavior.  
    # See RxCanBusSignal for further details.
    #
    # Typical default values:
    # - CRC enable (automatic CRC calculation) usually defaults to "enabled"
    #    * 0: CRC calculation disabled
    #    * 1: CRC calculation enabled
    # - CRC type (active CRC algorithm) should default to "correct CRC" 
    #   (which is typically algorithm 1)
    #
    cfg_custom_defaults = {
        "crc_enable_var": None,
        "crc_type_var":   None,
        
        "switch_var":     None,   # for parent RxCanBusSignal
        "dyncount_var":   None,   # for parent RxCanBusSignal
        "dynvalue_var":   None,   # for parent RxCanBusSignal
    }
    
    # #########################################################################
    def __init__(self, context, signal_path, 
                 message=None, cycle_time=None, debounce_time=None,
                 alias="", descr="", lookup=None,
                 error_delay=None, change_delay=None, timeout=None, 
                 recovery_time=None
                 ):
        """ CRC bus signal (HIL-Tx => ECU-Rx) initialization for dSPACE CAN 
            Multi-Message blockset.
            
            Example: CRC Signal Path Structure:
                # (static) crc signal value
                BusSystems/CAN/FOO_CAN/QUX_MESSAGE/TX/CRC_QUX_MESSAGE
                # crc calculation enable
                BusSystems/CAN/FOO_CAN/QUX_MESSAGE/TX/QUX_MESSAGE_crc
                # selected crc algorithm
                BusSystems/CAN/FOO_CAN/QUX_MESSAGE/TX/QUX_MESSAGE_crc_algorithm
                # variables for dynamic crc manipulation
                BusSystems/CAN/FOO_CAN/QUX_MESSAGE/TX/QUX_MESSAGE_dyn_algorithm
                BusSystems/CAN/FOO_CAN/QUX_MESSAGE/TX/QUX_MESSAGE_dyn_countdown
            
            Parameters:
                context         - rtplib application instance
                signal_path     - base path to signal below BusSystems
                                  (`BusSystems/.../<message>/TX/<signal>`)
                message         - reference to associated RxCanBusMessage instance
                cycle_time      - (opt) cycle time in [ms], overrides settings in Message
                debounce_time   - (opt) minimum debounce delay between events in [ms],
                                        overrides settings in Message
                alias           - (opt) bus signal alias/name
                descr           - (opt) signal description
                lookup          - (opt) lookup table for values, see VarBase
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
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class' code cannot be analyzed.
        
        ## CRC type for "correct" CRC algorithm (normal mode)
        self.crc_normal_type = self.cfg_crc_normal_type # (copy from class attribute)
        ## CRC type for "incorrect" CRC algorithm (for error injection)
        self.crc_error_type  = self.cfg_crc_error_type  # (copy from class attribute)
        
        ## delay [ms] to wait until a basic CRC error (like "CRC invalid")
        #  should be detected. This will be used in test functions.
        self.error_delay = None
        
        ## CRC Type variable, selects active CRC algorithm 
        # (a "HilVar" instance)
        self.crc_type_var   = None
        
        ## CRC Enable variable, enables/disables automatic CRC calculation 
        # (a "HilVar" instance)
        # * 0: CRC calculation disabled
        # * 1: CRC calculation enabled
        self.crc_enable_var = None
        
        ## CRC Dynamic Type variable, selects active CRC algorithm 
        # (a "HilVar" instance), only available if configured in CANMM and 
        # enabled in class config.  
        # See cfg_init_crc_dynamic_manipulation 
        self.crc_dyntype_var   = None
        
        ## CRC Dynamic Countdown variable, enables dynamic CRC type while 
        # counting down to 0 at each message transmission (a "HilVar" instance), 
        # only available if configured in CANMM and enabled with in class config.  
        # See cfg_init_crc_dynamic_manipulation
        self.crc_dyncount_var = None
        
        
        # Members inherited from RxCanBusSignal (see Note above) ##############
        
        ## Switch variable for signal manipulation. Only available if more than 
        # one signal manipulation option is configured in CANMM.
        #
        # Values:
        #  * 0: model input (if configured/available)
        #  * 1: constant from Trc/BusSystems 
        #  * 2: counter running (for counter signals, default switch setting for enabled counters)
        #  * 3: constant + counter (for counter signals)
        #  * 4: toggle value  (for toggle signals)
        #  * 5: parity value  (for parity signals)
        #  * 6: ~parity value (for parity signals)
        #  * 7: error value   (if an error value is configured)
        #  * 8: dynamic value (if dynamic value manipulation is configured)
        #
        self.switch_var = None
        
        ## Dynamic Countdown Value. Only available if signal manipulation is 
        # configured in CANMM and enabled in class config.  
        # See self.cfg_init_signal_manipulation 
        self.dyncount_var = None
        
        ## Dynamic Value: value that is active while dyncount_var decrements.
        # Only available if signal manipulation is configured in CANMM and 
        # enabled in class config.  
        # See self.cfg_init_signal_manipulation 
        self.dynvalue_var = None
        
        
        # Members inherited from CanBusSignal (see Note above) ################
        
        ## Signal model path as base path for deriving sub-element paths.
        # For CANMM signals, related variables follow the form 
        # <path_to_signal>_suffix
        self.base_path = None
        ## reference to associated (Rx-)CanBusMessage instance
        self.message = None
        
        
        # Members inherited from BusSignal (see Note above) ###################
        
        ## Signal value variable. get/info methods of this CanBusSignal
        # will access this variable (a HilVar instance).
        self.signal_var = None
        ## parent context (an RTE application instance to resolve signal/variable paths)
        self.context = None
        
        ## unit of physical signal value (as string, mainly used for report entries)
        self.unit  = None
        ## bus signal alias name
        self.alias = None
        ## bus signal description text
        self.descr = None
        
        # timings #############################################################
        ## cycle time of Message/PDU in [ms]
        self.cycle_time = None
        ## minimum debounce delay for event-triggered Messages/PDUs in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        ## delay to wait after a "basic" CRC error injection [ms] 
        self.error_delay = None
        
        # #####################################################################
        _bus_signals_canmmbs.CrcCanBusSignal.__init__(
            self, context=context, 
            signal_path=signal_path, message=message, 
            cycle_time=cycle_time, debounce_time=debounce_time, 
            alias=alias, descr=descr, lookup=lookup, 
            error_delay=error_delay, change_delay=change_delay, 
            timeout=timeout, recovery_time=recovery_time
        )
    
    # #########################################################################
    def setBasicCrcError(self):
        """ Switch CRC calculation to an algorithm producing incorrect CRCs.
            See CrcCanBusSignal.crc_error_type.
        """
        # Example/Default:
        #     Algorithm 1: Correct CRC
        #     Algorithm 2: Incorrect CRC (correct CRC XOR 0xFF)
        return _bus_signals_canmmbs.CrcCanBusSignal.setBasicCrcError(self)
    
    # #########################################################################
    def clearBasicCrcError(self):
        """ Switch CRC calculation back to an algorithm producing correct CRCs.
            See CrcCanBusSignal.crc_normal_type.
        """
        return _bus_signals_canmmbs.CrcCanBusSignal.clearBasicCrcError(self)
        
    
    # #########################################################################
    # Methods inherited from  RxCanBusSignal
    # #########################################################################
    def enableHilTx(self):
        """ Enable transmission of signal HIL => DUT (if the assigned 
            CAN-Message/PDU supports it).
            
            Note:
                This will enable transmission of _all_ signals of the parent 
                Message/PDU.
        
        """
        return _bus_signals_canmmbs.CrcCanBusSignal.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable transmission of signal HIL => DUT (if the assigned 
            CAN-Message/PDU supports it). 
            
            Note:
                This will disable transmission of _all_ signals of the parent 
                Message/PDU.
        
        """
        return _bus_signals_canmmbs.CrcCanBusSignal.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger transmission ("kickout") of signal HIL => DUT (by 
            triggering the parent CAN-Message/PDU).
            
            Note:
                All other signals of the parent Message/PDU will also be sent.
        
        """
        return _bus_signals_canmmbs.CrcCanBusSignal.kickout(self)
        
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/RxBusSignal
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable
            (typically not that useful for ECU-Rx/HIL-Tx CRC-Signals, though).
         """
        return _bus_signals_canmmbs.CrcCanBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable. 
            
            Parameters:
                value - value to set
            
            Returns the previous value from signal_var.
        """
        return _bus_signals_canmmbs.CrcCanBusSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data 
            (typically not that useful for ECU-Rx/HIL-Tx CRC-Signals, though).
            Returns the current state's description from signal_var.
        """
        return _bus_signals_canmmbs.CrcCanBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor.
            
            Parameters:
                state - named state to set
            
            Returns the previous state's description.
        """
        return _bus_signals_canmmbs.CrcCanBusSignal.setState(self, state)
    
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
        return _bus_signals_canmmbs.CrcCanBusSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. 
            Returns an info string.
        """
        return _bus_signals_canmmbs.CrcCanBusSignal.info(self)
        
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_canmmbs.CrcCanBusSignal.reset(self, *args, **kwargs)
        

# #############################################################################
class AcCanBusSignal(_bus_signals_canmmbs.AcCanBusSignal):
    """ Alive counter bus signal derived from RxCanBusSignal (HIL-Tx => ECU-Rx) 
        for use with dSPACE CAN Multi-Message blockset data structures.  
        See RxCanBusSignal for inherited methods.
    """
    
    ## Configuration settings for new instances:  
    # Temporary step length used to "freeze" counter in setBasicAcError
    # (arbitrary value, but should be selected large enough to hold counter
    #  for a full check duration, typically > error_delay)
    cfg_basic_error_tmpsteplen = 2000
    
    ## Configuration settings for new instances:  
    # Custom "hard" default value(s) to use for internal real time system 
    # variables. See RxFrBusSignal for further details.
    #
    # Mapping: <variable name as string>: <default value>
    #
    # Typical default values:
    # - source switches for alive counters usually default to "running counter"
    #   See RxFrBusSignal for further details.
    # - Temporary Step Length: auto-resets to default step length, which is
    #   usually 1
    # - Counter Offset, additive offset to counter value defaults to 0 
    #
    cfg_custom_defaults = {
        "ac_tmpsteplen_var": None, #
        "ac_offset_var":     None, #
        
        "switch_var":        None, # ac_switch_var is just an alias for switch_var
        "dyncount_var":      None, # for parent RxCanBusSignal
        "dynvalue_var":      None, # for parent RxCanBusSignal
    }
    
    
    # #########################################################################
    def __init__(self, context, signal_path, 
                 message=None, cycle_time=None, debounce_time=None,
                 alias="", descr="", lookup=None,
                 error_delay=None, change_delay=None, timeout=None, 
                 recovery_time=None
                 ):
        """ Alive counter bus signal (HIL-Tx => ECU-Rx) initialization for 
            dSPACE CAN Multi-Message blockset.
            
            Parameters:
                context         - rtplib application instance
                signal_path     - base path to signal below BusSystems
                                  (`BusSystems/.../<message>/TX/<signal>`)
                message         - reference to associated RxCanBusMessage instance
                cycle_time      - (opt) cycle time in [ms], overrides settings in Message
                debounce_time   - (opt) minimum debounce delay between events in [ms],
                                        overrides settings in Message  
                alias           - (opt) bus signal alias/name
                descr           - (opt) signal description  
                lookup          - (opt) lookup table for values, see VarBase
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
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class' code cannot be analyzed.
        
        ## delay to wait after a "simple" ac error injection [ms] 
        self.error_delay = None
        
        ## HilVar for additional alive counter offset
        # (offset will simply be added to current counter value)
        self.ac_offset_var = None
        
        ## HilVar for "temporary step length", holds counter for n * cycle time 
        # (will reset automatically to default step length)
        self.ac_tmpsteplen_var = None
        
        ## Alive Counter mode switch (uses same switch as other
        # input manipulation options). See self.switch_var
        self.ac_switch_var = None # will be a reference to self.switch_var later
        
        
        # Members inherited from CanBusSignal (see Note above) ################
        
        ## Signal model path as base path for deriving sub-element paths.
        # For CANMM signals, related variables follow the form 
        # <path_to_signal>_suffix
        self.base_path = None
        ## reference to associated (Rx-)CanBusMessage instance
        self.message = None
        
        
        # Members inherited from BusSignal (see Note above) ###################
        
        ## signal value variable, get/info methods of this TxCanBusSignal
        # will access this variable (a HilVar instance).
        self.signal_var = None
        ## parent context (an RTE application instance to resolve signal/variable paths)
        self.context = None
        
        ## unit of physical signal value (as string, mainly used for report entries)
        self.unit  = None
        ## bus signal alias name
        self.alias = None
        ## bus signal description text
        self.descr = None
        
        # timings #############################################################
        ## cycle time of Message/PDU in [ms]
        self.cycle_time = None
        ## minimum debounce delay for event-triggered Messages/PDUs in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        ## delay to wait after a "basic" AC error injection [ms] 
        self.error_delay = None
        
        
        # #####################################################################
        _bus_signals_canmmbs.AcCanBusSignal.__init__(
            self, context=context, 
            signal_path=signal_path, message=message, 
            cycle_time=cycle_time, 
            debounce_time=debounce_time, alias=alias, 
            descr=descr, lookup=lookup, 
            error_delay=error_delay, 
            change_delay=change_delay, 
            timeout=timeout, recovery_time=recovery_time
        )
        
    
    # #########################################################################
    def setBasicAcError(self):
        """ Stop and hold Alive Counter at the current count. """
        _bus_signals_canmmbs.AcCanBusSignal.setBasicAcError(self)
    
    # #########################################################################
    def clearBasicAcError(self):
        """ (Re-)enable normal Alive Counter behaviour (i.e. continue counting)."""
        _bus_signals_canmmbs.AcCanBusSignal.clearBasicAcError(self)
        
    
    # #########################################################################
    # Methods inherited from  RxCanBusSignal
    # #########################################################################
    def enableHilTx(self):
        """ Enable transmission of signal HIL => DUT (if the assigned 
            CAN-Message/PDU supports it).
            
            Note:
                This will enable transmission of _all_ signals of the parent 
                Message/PDU.
        """
        return _bus_signals_canmmbs.AcCanBusSignal.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable transmission of signal HIL => DUT (if the assigned 
            CAN-Message/PDU supports it).
            
            Note:
                This will disable transmission of _all_ signals of the parent 
                Message/PDU.
        
        """
        return _bus_signals_canmmbs.AcCanBusSignal.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger transmission ("kickout") of signal HIL => DUT (by 
            triggering the parent CAN-Message/PDU).
            
            Note:
                All other signals of the parent Message/PDU will also be sent.
        """
        return _bus_signals_canmmbs.AcCanBusSignal.kickout(self)
        
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/RxBusSignal
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable
            (typically not that useful for ECU-Rx/HIL-Tx AC-signals, though).
            Returns the current value from signal_var.
         """
        return _bus_signals_canmmbs.AcCanBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable. 
            Parameters:
                value - value to set
            Returns the previous value from signal_var.
        """
        return _bus_signals_canmmbs.AcCanBusSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data
            (typically not that useful for ECU-Rx/HIL-Tx AC-signals, though).
            Returns the current state's description.
        """
        return _bus_signals_canmmbs.AcCanBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor.
            Parameters:
                state - named state to set
            Returns the previous state's description.
        """
        return _bus_signals_canmmbs.AcCanBusSignal.setState(self, state)
    
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
        return _bus_signals_canmmbs.AcCanBusSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. 
            Returns an info string.
        """
        return _bus_signals_canmmbs.AcCanBusSignal.info(self)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_canmmbs.AcCanBusSignal.reset(self, *args, **kwargs)
        

# #############################################################################
# Signal Container
# #############################################################################
class CanBusSignalContainer(_bus_signals_canmmbs.CanBusSignalContainer):
    """ A BusSignalContainer for CAN Bus Signals """
    
    # #########################################################################
    def __init__(self, context):
        """ Override to add signals.
            
            Parameters:
                context - context used for contained BusSignals
        """
        _bus_signals_canmmbs.CanBusSignalContainer.__init__(self, context)
    
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
        _bus_signals_canmmbs.CanBusSignalContainer.resetAll(
            self, 
            verbosity=verbosity, 
            recursion_depth=recursion_depth
        )
    
    # #########################################################################
    def iterSignals(self, msg):
        """ Iterate over all signals that reference the specified CAN message/PDU.
            
            Parameters:
                msg - a CAN message/pdu instance
            
            Usage:
                for sig in bus.iterSignals(bus.tx_msg_FNORD):
                    print sig
            
            Returns an iterator object.
        """
        return _bus_signals_canmmbs.CanBusSignalContainer.iterSignals(
            self, msg=msg
        )
    

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################   
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    import time
    if True:
        import ttk_tools.dspace.rtplib_offline_stub as rtplib
        context = rtplib.Appl("foo.sdf", "ds1006", "Offline")
        
    else:
        import ttk_tools.dspace.xil_api_offline_stub as xil_api 
        context = xil_api.XilTestbench(
            config_file_path = r"D:\Python\MAPortConfiguration.xml",
            product_name    = "XIL API", 
            product_version = "2018-B",
        )
    
    
    rx_sig = RxCanBusSignal(context, 'masterappl/BusSystems/CAN/FASL_CAN/CLRC_SEG_00_SIDE_LH_RADA/TX/CLRC_SEG_00_SIDE_LH_RADA_Enable', cycle_time=10)
    
    print rx_sig.signal_var.info()
    rx_sig.signal_var.set(123)
    print rx_sig.info()
    print rx_sig.signal_var.info()
    rx_sig.reset()
    print rx_sig.signal_var.info()
    
    tx_sig = RxCanBusSignal(context, 'BusSystems/CAN/FnordSG/FooBarMsg/RX/Kl_15', cycle_time=10)
    print tx_sig.info()
    print tx_sig.signal_var.info()
    
    
    # #########################################################################
    class BusSignals(CanBusSignalContainer):
        def __init__(self, context):
            self.tx_msg = TxCanBusMessage(context, bus_systems_path="BusSystems/CAN/SomeECU/MessageB/RX/MessageB", 
                                          cycle_time=100, debounce_time=10, alias="MessageB")
            
            self.rx_msg2 = RxCanBusMessage(context, cycle_time=50, debounce_time=10, alias="OBJ_00_EXT_SIDE_LH_RADA",
                                           bus_systems_path="masterAppl/BusSystems/CAN/FASL_CAN/OBJ_00_EXT_SIDE_LH_RADA/TX/OBJ_00_EXT_SIDE_LH_RADA_Enable" )
                                           
            
            self.BarBazSig  = TxCanBusSignal(context, "BusSystems/CAN/SomeECU/MessageB/RX/SignalName3", self.tx_msg)
            
            self.rx_msg = RxCanBusMessage(context, bus_systems_path="BusSystems/CAN/SomeECU/MessageA/TX/MessageA", 
                                          cycle_time=100, debounce_time=10, alias="MessageA")
            self.FooBarSig  = RxCanBusSignal(context, "BusSystems/CAN/SomeECU/MessageA/TX/SignalName1", self.rx_msg)
            self.BazQuuxSig = RxCanBusSignal(context, "BusSystems/CAN/SomeECU/MessageA/TX/SignalName2", self.rx_msg)
            
            self.crc_signal = CrcCanBusSignal(context, "BusSystems/CAN/SomeECU/MessageA/TX/CRC_SignalName", self.rx_msg2)
            self.ac_signal  = AcCanBusSignal(context,  "BusSystems/CAN/SomeECU/MessageA/TX/AC_SignalName", self.rx_msg2)
            
            
            
            
            self.AnotherSig = RxCanBusSignal(context, "BusSystems/CAN/SomeECU/MessageA/TX/AnotherSignal", 
                alias="Another Bus Signal", descr="Another Signal to test", unit="rpm", 
                message=self.rx_msg, 
                change_delay=250, timeout=500, recovery_time=500,
            )
            
            
    
    bus_signals = BusSignals(context)
    
    print "# initial:"
    print bus_signals.FooBarSig.info()
    print bus_signals.BazQuuxSig.info()
    print bus_signals.AnotherSig.info()
    bus_signals.FooBarSig.set(1234)
    bus_signals.AnotherSig.set(1000)
    time.sleep(bus_signals.AnotherSig.cycle_time / 1000.0)
    
    print "# changed:"
    print bus_signals.FooBarSig.info()
    print bus_signals.BazQuuxSig.info()
    print bus_signals.AnotherSig.info()
    
    print
    bus_signals.resetAll()
    print "# reset:"
    print bus_signals.FooBarSig.info()
    print bus_signals.BazQuuxSig.info()
    print bus_signals.AnotherSig.info()
    
    
    print 
    print "# iterSignals:"
    print 'Signals in rx_msg ("%s"):'%(bus_signals.rx_msg.alias)
    for sig in bus_signals.iterSignals(bus_signals.rx_msg):
        print " ->", sig
    print 'Signals in tx_msg ("%s"):'%(bus_signals.tx_msg.alias)
    for sig in bus_signals.iterSignals(bus_signals.tx_msg):
        print " ->", sig
    
    print "#" * 80
    
    def pv(obj, name):
        var = getattr(obj, name, None)
        print "%-24s->\t %s\t %s"%(name, type(var), var)
    
    pv(bus_signals.ac_signal.message, "cycle_time_var")
    pv(bus_signals.ac_signal.message, "kickout_var")
    pv(bus_signals.ac_signal, "switch_var")
    pv(bus_signals.ac_signal, "ac_offset_var")
    print("------")
    pv(bus_signals.FooBarSig.message, "cycle_time_var")
    pv(bus_signals.FooBarSig.message, "kickout_var")
    pv(bus_signals.FooBarSig, "switch_var")
    print("------")
    pv(bus_signals.rx_msg, "cycle_time_var")
    pv(bus_signals.rx_msg, "kickout_var")
    pv(bus_signals.rx_msg2, "cycle_time_var")
    pv(bus_signals.rx_msg2, "kickout_var")
    
    
    print("\nDone.")
# @endcond DOXYGEN_IGNORE
# #############################################################################

