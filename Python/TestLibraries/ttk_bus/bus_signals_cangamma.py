#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : bus_signals_cangamma.py
# Package : ttk_bus
# Task    : Wrapper classes for bus/interface signal descriptions.
#           Specific implementation for Gamma-V-based CAN blocksets
# Type    : Interface
# Python  : 2.7
#
# Copyright 2016 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Author    | Description
#------------------------------------------------------------------------------
# 1.0  | 01.03.2019 | J.Tremmel | initial, interface to _bus_signals_cangamma v1.8
# 1.1  | 11.06.2019 | J.Tremmel | updated to _bus_signals_cangamma v1.9 / 
#                               | "Schnittstellenbeschreibung 1.0.0"
# 1.2  | 29.04.2020 | J.Tremmel | updated to _bus_signals_cangamma v1.10.
#                               | Added basic bus signals, removed obsolete 
#                               | min/max_values from signal inits
#******************************************************************************
"""
@package ttk_bus.bus_signals_cangamma
Interface wrapper bus/interface signal classes in ttk_bus._bus_signals_cangamma.
Specific implementation for Gamma-V-based CAN blocksets 

Convention:
    Signal directions are relative to the DUT:
      * Tx - transmitted by ECU => received from HIL
      * Rx - received by ECU <= transmitted from HIL
    
"""
import _bus_signals_cangamma


# #############################################################################
# hil-tx message
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.cycle_counter
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.cycle_factor                          [internal use only]
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.cycle_time                            unused? => use period instead
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.length
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.min_delay
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.payload                               [internal use only]
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.period                                [current cycle time]
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.timestamp
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.transmission_mode                     [only for FlexRay, unused in CAN)
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.trigger

# NOTE: there is no "enable" switch on a per-message level, set period to 0 instead

# hil-tx signals
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.ac_case           [internal-use-only, AC signals]
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.algo              [only used for CRC signals]
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.algo_value        [internal use only]
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.dyn_value_phy     [was just dyn_value before 1.0.0]
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.offset            [only used for AC signals]
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.dyn_algo          [only used for CRC signals] 
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.dyn_count
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.dyn_pattern
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.mode
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.static_value_phy  (new 2019-02-20)
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.static_value_raw
# BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.value             [internal use, raw value sent to CAN plugin]

# #############################################################################
# hil-rx message
# BusSystems.can3_iFIU_iSRC.HIL_RX.N0FIU_Status_Card19.length
# BusSystems.can3_iFIU_iSRC.HIL_RX.N0FIU_Status_Card19.payload                                [internal use only]
# BusSystems.can3_iFIU_iSRC.HIL_RX.N0FIU_Status_Card19.timestamp

# hil-rx signals
# BusSystems.can3_iFIU_iSRC.HIL_RX.N0FIU_Status_Card19.signals.State_Path_3_break.algo        [only used for CRC signals] 
# BusSystems.can3_iFIU_iSRC.HIL_RX.N0FIU_Status_Card19.signals.State_Path_3_break.crc_valid   [only used for CRC signals] 
# BusSystems.can3_iFIU_iSRC.HIL_RX.N0FIU_Status_Card19.signals.State_Path_3_break.value       [internal use, raw value from CAN plugin] 
# BusSystems.can3_iFIU_iSRC.HIL_RX.N0FIU_Status_Card19.signals.State_Path_3_break.value_raw
# BusSystems.can3_iFIU_iSRC.HIL_RX.N0FIU_Status_Card19.signals.State_Path_3_break.value_phy   (new 2019-02-20)


# #############################################################################
class TxCanBusMessage(_bus_signals_cangamma.TxCanBusMessage):
    """ CAN Message/PDU ECU-Tx (ECU-Tx => HIL-Rx). """
    # #########################################################################
    def __init__(self, context, base_identifier=None, 
                 cycle_time=0, debounce_time=0,
                 alias="", descr='',
                 change_delay=None, timeout=None, recovery_time=None):
        """ Tx CAN Message data (ECU-Tx => HIL-Rx).
            
            Parameters:
                context          - parent gamma_api context 
                
                base_identifier  - base identifier to PDU/message.  
                                   Helper entries will be derived from this, 
                                   e.g. kickout or status variables (though this is mostly 
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
                recovery_time     - (opt) time for recovery/"wiedergut" checks [ms]
                                          defaults to 2x max(cycle_time, debounce_time)
        """
        
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class code cannot be analyzed.
        
        ## Message Rx time variable (in seconds)
        self.time_var = None
        
        ## Message payload data length
        self.length_var = None
        
        # Members inherited from CanBusMessage ################################
        # (see Note above)
        
        ## Parent context (a gaapi reference to resolve signal/variable paths)
        self.context = None
        ## Message alias name
        self.alias = None
        ## Message description text
        self.descr = None
        
        ## Base BusSystems path to Message/PDU helper variables 
        #  e.g. "BusSystems.<CAN_NAME>.HIL_RX.<MSG_NAME>"
        self.base_identifier = None
        
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
        _bus_signals_cangamma.TxCanBusMessage.__init__(
            self, context=context, 
            base_identifier=base_identifier,
            
            cycle_time=cycle_time, debounce_time=debounce_time, 
            
            alias=alias, descr=descr, 
            
            change_delay=change_delay, timeout=timeout,
            recovery_time=recovery_time
        )
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs): # @UnusedVariable *args, **kwargs (just to tolerate optional parameters)
        """ Call reset() on all contained variables/signals that support it.
            Simple, non-recursive approach.
        """
        _bus_signals_cangamma.TxCanBusMessage.reset(self)
        

# #############################################################################
class RxCanBusMessage(_bus_signals_cangamma.RxCanBusMessage):
    """ CAN Message/PDU ECU-Rx (HIL-Tx => ECU-Rx).
        
        Extends the basic CanBusMessage with methods for 
        enableHilTx/disableHilTx and message kickout (trigger).
    """
    
    ## Configuration setting for new instances: 
    # Custom "hard" default values to use for internal real time system 
    # variables, so a reset() will always reset those variables to defined 
    # values (and not just those variables that were set/accessed). 
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
    # - Message/PDU (Hil-TX) cycle time access: Default value depends on 
    #   configured cycle time (in [s]). Override standard behavior only if 
    #   absolutely necessary.
    # - Kickout/trigger variables: Triggers should auto-reset to 0 once the 
    #   PDU has been triggered. 0 is a safe default.
    cfg_custom_defaults = {
        "manual_enable_var":    None,
        "kickout_var":          None,
    }
    
    ## True: automatically initialize message's cycle time from the configured
    # cycle_time value (sets self.cycle_time_var to self.cycle_time during init)
    cfg_init_cycle_time = True
    
    
    # #########################################################################
    def __init__(self, context, enable_identifier=None, base_identifier=None, 
                 cycle_time=0, debounce_time=0,
                 alias="", descr='',
                 change_delay=None, timeout=None, recovery_time=None):
        """ Rx CAN Message/PDU data (HIL-Tx => ECU-Rx).
            
            Parameters:
                context           - parent gamma_api context 
                
                enable_identifier - identifier of a custom/manual tx enable switch PV.
                                    Keep at None to use default "enable" behavior.  
                                    If defined, the enable variable will later 
                                    be set to 1 to enable or to 0 to disable 
                                    message transmission.
                
                base_identifier   - base identifier to PDU/message.  
                                    Helper entries will be derived from this,
                                    e.g. kickout or status variables (though this is mostly 
                                    relevant to messages sent to DUT, see RxCanBusMessage)
                
                cycle_time        - cycle time in [ms]. Value will be used to 
                                    enable/disable sending of cyclic messages, 
                                    see cycle_time_var.  
                                    Event-triggered messages have a cycle time 
                                    of 0 (similar to DBC value)
                
                debounce_time     - minimum debounce delay between events in [ms]
                alias             - Message alias/name
                descr             - (opt) Message description (may be used in report entries)
                
                change_delay      - (opt) delay to wait after a value change [ms], 
                                          defaults to 2x max(cycle_time, debounce_time)
                timeout           - (opt) detection time for timeout errors [ms], 
                                          defaults to 2x max(cycle_time, debounce_time)
                recovery_time     - (opt) time for recovery/"wiedergut" checks [ms]
                                          defaults to 2x max(cycle_time, debounce_time)
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class code cannot be analyzed.
        
        ## HIL-Tx-enable/disable variable (only if set via enable_identifier)
        self.enable_var = None
        
        ## HIL-Tx-kickout/trigger variable
        self.kickout_var = None
        
        ## Message/PDU (Hil-Tx) cycle time access. Cycle time in [ms].
        # Note: This maps to the .period element of the current message
        self.cycle_time_var = None
        
        ##
        self.cycle_counter_var = None
        
        ## minimum delay between triggered messages in [ms], 
        # compare debounce delay in .debounce_time
        self.min_delay_var = None
        
        # Members inherited from CanBusMessage ################################
        # (see Note above)
        
        ## Parent context (a gaapi reference to resolve signal/variable paths)
        self.context = None
        ## Message alias name
        self.alias = None
        ## Message description text
        self.descr = None
        
        ## Base BusSystems path to Message/PDU helper variables below BusSystems
        #  e.g. "BusSystems.<CAN_NAME>.HIL_TX.<MSG_NAME>"
        self.base_identifier = None
        
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
        _bus_signals_cangamma.RxCanBusMessage.__init__(
            self, context, 
            enable_identifier=enable_identifier,    # custom enable switch
            base_identifier=base_identifier,        # base PV address/ident
            
            cycle_time=cycle_time, debounce_time=debounce_time, 
            alias=alias, descr=descr, 
            
            change_delay=change_delay, timeout=timeout,
            recovery_time=recovery_time
        )
    
    # #########################################################################
    def enableHilTx(self):
        """ (Re-)enable sending of this Message/PDU. """
        _bus_signals_cangamma.RxCanBusMessage.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable (cyclic) sending of this Message/PDU. """
        _bus_signals_cangamma.RxCanBusMessage.disableHilTx(self)
    
    # #########################################################################
    def kickout(self, delay_ms=None):
        """ Trigger sending of this CAN-Message/PDU. 
            
            Parameters: 
                delay_ms - [ms] Delay to wait before clearing kickout/trigger 
                           variable again.
            
            Info: Default Delay:
               Delay defaults to 1/2 self.debounce_time (if explicitly set) 
               or alternatively to 1/2 self.change_delay.  
               Default delay will never be shorter than 5 ms.
        """
        _bus_signals_cangamma.RxCanBusMessage.kickout(self, delay_ms=delay_ms)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs): 
        """ Call reset() on all contained variables/signals that support it.
            Simple, non-recursive approach.
        """
        _bus_signals_cangamma.RxCanBusMessage.reset(self, *args, **kwargs)
        

# #############################################################################
class TxCanBusSignalBasic(_bus_signals_cangamma.TxCanBusSignalBasic):
    """ A basic CAN signal sent from the DUT to the test system (ECU Tx => HIL Rx). 
        
        Basic implementation, directly accesses raw value as-is from CAN, 
        without a converted physical value or error injections.
        
        Use this for signal entries generated with iSyDBC mode "minimal" .
    """
    # #########################################################################
    def __init__(self, context, signal_identifier, 
                 message=None, cycle_time=None, debounce_time=None,
                 unit="", alias="", descr="", lookup=None,
                 change_delay=None, timeout=None, recovery_time=None,
                 ):
        """ Basic Tx bus signal initialization (ECU Tx => HIL Rx).
            
            Parameters:
                context            -  parent gamma_api context 
                signal_identifier  -  identifier for signal value PV. Use `.value` entry, e.g. 
                                      `"BusSystems.can.HIL_TX.MessageName.signals.SignalName.value"`
                message            -  reference to associated TxCanBusMessage instance
                
                cycle_time    - (opt) cycle time in [ms], overrides settings in message
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
                recovery_time - (opt) time for recovery/"wiedergut" checks [ms]
                                      defaults to 2x max(cycle_time, debounce_time)
            
            Info: Minimal/Basic Signals:
                ECU-Tx/HIL-Rx Signals generated by iSyDBC in minimal/basic mode 
                will only contain PVs for:
                * `<SignalName>.value`     - raw value as received from CAN-Plugin
                * `<SignalName>.timestamp` - Rx time stamp
                * `<SignalName>.length`    - message length
        
        """
        
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class' code cannot be analyzed.
        
        
        # Members inherited from CanBusSignal #################################
        # (see Note above)
        
        ## Signal PV address/identifier as base identifier for deriving sub-elements.
        # For CAN/Gamma signals, related variables follow the form 
        # `<base_identifier>.<suffix>`
        self.base_identifier = None
        ## reference to associated (Tx-)CanBusMessage instance
        self.message = None
        
        # Members inherited from BusSignal ####################################
        # (see Note above) 
        
        ## parent context (a gaapi reference to resolve signal/variable paths)
        self.context = None
        
        ## Signal value variable, default representation. get/info methods of 
        # this TxCanBusSignal will access this variable.  
        # Note that the default self.signal_var usually maps to member "value_phy", 
        # (depending on supplied signal_identifier).
        self.signal_var = None
        
        ## unit of physical signal value (as string, mainly used for report entries)
        self.unit = None
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
        
        
        _bus_signals_cangamma.TxCanBusSignalBasic.__init__(
            self, context, signal_identifier, 
            message=message, cycle_time=cycle_time, debounce_time=debounce_time,
            unit=unit, alias=alias, descr=descr, lookup=lookup,
            change_delay=change_delay, timeout=timeout, recovery_time=recovery_time,
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable, 
            see `signal_var`
            Returns the current info string from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignalBasic.info(self)
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable, see `signal_var` 
            Returns the current value from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignalBasic.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable, see `signal_var`
            
            Attention:
                For TxCanBusSignals, this will only overwrite the current 
                contents of the HIl receive buffer of the signal (which is 
                typically not too useful as it will be overwritten on next 
                update with data from CAN plugin)
            
            Parameters:
                value - value to set
            
            Returns the previous value from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignalBasic.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data, 
            see `signal_var`. This uses the lookup values supplied in constructor.
            Fallback (if no matching state was found) will be the unmapped 
            numeric value.
            
            Returns the current state representation from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignalBasic.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable, see `signal_var`.
            This uses the lookup values supplied in constructor.
            
            Attention:
                For TxFrBusSignals this will only overwrite the current 
                contents of the HIl receive buffer of the signal 
                (which typically is not too useful).
            
            Parameters:
                state - named state to set
            
            Returns the previous state representation from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignalBasic.setState(self, state)
    
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
        return _bus_signals_cangamma.TxCanBusSignalBasic.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_cangamma.TxCanBusSignalBasic.reset(self, *args, **kwargs)
        

# #############################################################################
class TxCanBusSignal(_bus_signals_cangamma.TxCanBusSignal):
    """ A CAN signal sent from the DUT to the test system (ECU Tx => HIL Rx). 
        
        Standard implementation, accesses converted physical or raw values. 
        
        Use this for signal entries generated with iSyDBC mode "standard" .
    """
    # #########################################################################
    def __init__(self, context, signal_identifier, 
                 message=None, cycle_time=None, debounce_time=None,
                 unit="", alias="", descr="", lookup=None,
                 change_delay=None, timeout=None, recovery_time=None,
                 ):
        """ Tx bus signal initialization (ECU Tx => HIL Rx).
            
            Parameters:
                context            -  parent gamma_api context 
                signal_identifier  -  identifier for signal value PV
                message            -  reference to associated TxCanBusMessage instance
                
                cycle_time    - (opt) cycle time in [ms], overrides settings in message
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
                recovery_time - (opt) time for recovery/"wiedergut" checks [ms]
                                      defaults to 2x max(cycle_time, debounce_time)
            
            Info: signal_identifier:
                HIL-Rx/ECU-Tx signals will have the following "value" PV elements:
                * `.value_phy` - physical representation of value
                * `.value_raw` - raw representation of value
                * `.value`     - value as received from CAN-Plugin (typically "raw")
                
                Usually, the "phy" variant will be used, e.g. something like
                `signal_identifier="BusSystems.can.HIL_TX.MessageName.signals.SignalName.value_phy"`
            
        """
        
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class' code cannot be analyzed.
        
        
        # Members inherited from CanBusSignal #################################
        # (see Note above) 
        
        ## Signal PV address/identifier as base identifier for deriving sub-elements.
        # For CAN/Gamma signals, related variables follow the form 
        # `<base_identifier>.<suffix>`
        self.base_identifier = None
        ## reference to associated (Tx-)CanBusMessage instance
        self.message = None
        
        # Members inherited from BusSignal ####################################
        # (see Note above) 
        
        ## parent context (a gaapi reference to resolve signal/variable paths)
        self.context = None
        
        ## Signal value variable, default representation. get/info methods of 
        # this TxCanBusSignal will access this variable.  
        # Note that the default self.signal_var usually maps to member "value_phy", 
        # (depending on supplied signal_identifier).
        self.signal_var = None
        
        ## Raw signal value variable.
        self.signal_raw_var = None
        
        ## Physical signal value variable.
        self.signal_phy_var = None
        
        
        ## unit of physical signal value (as string, mainly used for report entries)
        self.unit = None
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
        _bus_signals_cangamma.TxCanBusSignal.__init__(
            self, context, signal_identifier, 
            message=message, cycle_time=cycle_time, debounce_time=debounce_time,
            unit=unit, alias=alias, descr=descr, lookup=lookup,
            change_delay=change_delay, timeout=timeout, recovery_time=recovery_time,
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable, 
            see `signal_var`
            Returns the current info string from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignal.info(self)
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable, see `signal_var` 
            Returns the current value from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable, see `signal_var`
            
            Attention:
                For TxCanBusSignals, this will only overwrite the current 
                contents of the HIl receive buffer of the signal (which is 
                typically not too useful as it will be overwritten on next 
                update with data from CAN plugin)
            
            Parameters:
                value - value to set
            
            Returns the previous value from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data, 
            see `signal_var`. This uses the lookup values supplied in constructor.
            Fallback (if no matching state was found) will be the unmapped 
            numeric value.
            
            Returns the current state representation from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable, see `signal_var`.
            This uses the lookup values supplied in constructor.
            
            Attention:
                For TxFrBusSignals this will only overwrite the current 
                contents of the HIl receive buffer of the signal 
                (which typically is not too useful).
            
            Parameters:
                state - named state to set
            
            Returns the previous state representation from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignal.setState(self, state)
    
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
        return _bus_signals_cangamma.TxCanBusSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_cangamma.TxCanBusSignal.reset(self, *args, **kwargs)
        

# #############################################################################
class RxCanBusSignalBasic(_bus_signals_cangamma.RxCanBusSignalBasic):
    """ A basic CAN signal sent from the test system to the DUT (ECU Rx <= HIL Tx). 
        
        Basic implementation, directly accesses raw value as-is from CAN, 
        without a converted physical value or error injections.
        
        Use this for signal entries generated with iSyDBC mode "minimal" .
    """
    # #########################################################################
    def __init__(self, context, signal_identifier, 
                 message=None, cycle_time=None, debounce_time=None,
                 unit="", alias="", descr="", lookup=None,
                 change_delay=None, timeout=None, recovery_time=None,
                 ):
        """ Basic Rx bus signal initialization (ECU Rx <= HIL Tx).
            
            Parameters:
                context            -  parent gamma_api context 
                signal_identifier  -  identifier for signal value PV. Use `.value` entry, e.g. 
                                      `"BusSystems.can.HIL_TX.MessageName.signals.SignalName.value"`
                message            -  reference to associated CanBusMessage instance
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
                recovery_time - (opt) time for recovery/"wiedergut" checks [ms]
                                      defaults to 2x max(cycle_time, debounce_time)
            
            Info: Minimal/Basic Signals:
                ECU-Rx/HIL-Tx Signals generated by iSyDBC in minimal/basic mode 
                will only contain PVs for:
                * `<SignalName>.value`     - raw value as sent to CAN-Plugin
                * `<SignalName>.period`    - tx cycle time / period in ms.
                * `<SignalName>.timestamp` - Tx time stamp
                * `<SignalName>.length`    - message length
            
        """
        _bus_signals_cangamma.RxCanBusSignalBasic.__init__(
            self, context, signal_identifier, 
            
            message=message, cycle_time=cycle_time, debounce_time=debounce_time,
            unit=unit, alias=alias, descr=descr, lookup=lookup,
            change_delay=change_delay, timeout=timeout, recovery_time=recovery_time,
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable, 
            see `signal_var`
            
            Attention:
                For RxCanBusSignals, this will show info on the contents 
                of the HIL-send-buffer, not the value from Model/Simulink 
                source nor the last seen signal value on CAN bus.
            
            Returns the current info string from `signal_var`.
        """
        return _bus_signals_cangamma.RxCanBusSignalBasic.info(self)
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable, see `signal_var`. 
            
            Attention:
                For RxCanBusSignals, this will get the current (raw) value 
                of the HIL-send-buffer, not the last seen signal value on CAN 
                bus.
            
            Returns the current value from `signal_var`.
        """
        return _bus_signals_cangamma.RxCanBusSignalBasic.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable (`.signal_var`).
            
            Parameters:
                value - value to set (physical)
            
            Returns the previous value from `signal_var`.
        """
        return _bus_signals_cangamma.RxCanBusSignalBasic.set(self, value=value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data, 
            see `value_var`. This uses the lookup values supplied in constructor.
            Fallback (if no matching state was found) will be the unmapped 
            numeric value.
            
            Attention:
                For RxCanBusSignals, this will get the current (raw) value 
                of the HIL-send-buffer, not the last seen signal value on 
                CAN bus.
            
            Returns the current state representation from `signal_var`.
        """
        return _bus_signals_cangamma.RxCanBusSignalBasic.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable (`.signal_var`). 
            This uses the lookup values supplied in constructor.
            
            Parameters:
                state - named state to set
            
            Returns the previous value from `signal_var`.
        """
        return _bus_signals_cangamma.RxCanBusSignalBasic.setState(self, state=state)
    
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
        return _bus_signals_cangamma.RxCanBusSignalBasic.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def enableHilTx(self):
        """ Enable transmission of signal HIL => DUT (if the assigned 
            CAN-Message/PDU  supports it).
            
            Note:
                This will enable transmission of _all_ signals of the parent 
                Message/PDU.
        """
        return _bus_signals_cangamma.RxCanBusSignalBasic.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable transmission of signal HIL => DUT (if the assigned 
            CAN-Message/PDU supports it). 
            
            Note:
                This will disable transmission of _all_ signals of the parent 
                Message/PDU.
        """
        return _bus_signals_cangamma.RxCanBusSignalBasic.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger transmission ("kickout") of signal HIL => DUT (by 
            triggering the parent CAN-Message/PDU). 
            
            Note:
                All other signals of the parent Message/PDU will also be sent.
        """
        return _bus_signals_cangamma.RxCanBusSignalBasic.kickout(self)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. Note that this
            will also switch the variable source switch back to its original 
            setting.
        """
        _bus_signals_cangamma.RxCanBusSignalBasic.reset(self, *args, **kwargs)
        

# #############################################################################
class RxCanBusSignal(_bus_signals_cangamma.RxCanBusSignal):
    """ A CAN signal sent from the test system to the DUT (ECU Rx <= HIL Tx). 
        
        Standard implementation, accesses converted physical or raw values 
        and provides options for error injections.
        
        Use this for signal entries generated with iSyDBC mode "standard" .
        See _bus_signals_cangamma.RxCanBusSignalBasic.
    """
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
    #       0: default value from model input, see .mode_var for details.
    # - Dynamic Countdown Value: 
    #       auto-decrements until 0 is reached if a dynamic mode is active
    # - Dynamic Value: 
    #        value that is active while dyn_count_var decrements.
    cfg_custom_defaults = {
        "mode_var":          None,
        "dyn_count_var":     None,
        "dyn_value_phy_var": None,
    }
    
    ## [temporary] set True to also write to `.signal_var` (and not just
    # `.static_value_phy_var`) as a workaround for missing raw/phys conversion 
    # in realtime model
    cfg_value_workaround = False
    
    # #########################################################################
    def __init__(self, context, signal_identifier, 
                 message=None, cycle_time=None, debounce_time=None,
                 unit="", alias="", descr="", lookup=None,
                 change_delay=None, timeout=None, recovery_time=None,
                 ):
        """ Rx bus signal initialization (ECU Rx <= HIL Tx).
            
            Parameters:
                context            -  parent gamma_api context 
                signal_identifier  -  identifier for signal value PV
                message            -  reference to associated CanBusMessage instance
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
                recovery_time - (opt) time for recovery/"wiedergut" checks [ms]
                                      defaults to 2x max(cycle_time, debounce_time)
            
            Info: signal_identifier
                HIL-Tx/ECU-Rx signals will have a PV element `.value` which 
                contains the value as sent to CAN-plugin (typically in "raw" 
                format).  
                For signal manipulation the PV elements `.static_value_phy` or
                `.static_value_raw` (and an appropriate mode setting) will be
                used.
            
            Attention:
                When using the default PV `signal_identifier` ending in `.value`,
                reading the signal value via `.get()` will return the most 
                recently written value in *raw* format
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class' code cannot be analyzed.
        
        
        ## Mode switch variable for signal manipulation.  
        # * 0x00: simulink model inport value
        # * 0x01: `<signal>.static_value_phy` (manual override w/ physical value)
        # * 0x02: `<signal>.static_value_raw` (manual override w/ raw value)
        # * 0x03: `<signal>.dyn_value_phy`, while `<signal>.dyn_count` decrements down to 0, 
        #         then model value (mode 0x00)
        # * 0x04: `<signal>.dyn_value_phy`, while `<signal>.dyn_count` decrements down to 0, 
        #         then `<signal>.static_value_phy` (mode 0x01)
        # * 0x05: `<signal>.dyn_value_phy`, while `<signal>.dyn_count` decrements down to 0, 
        #         then `<signal>.static_value_raw` (mode 0x02)
        #
        # For alive counter signals (see dedicated sub-class):
        # * 0x10: alive-counter, running/counting
        # * 0x11: alive-counter, stopped (static value)
        # * 0x12: alive-counter, stopped while `<signal>.dyn_count` decrements, 
        #         then continues counting/running from last count (mode 0x10)
        # * 0x13: alive-counter, stopped while `<signal>.dyn_count` decrements 
        #         but continues counting in background (then mode 0x10)
        # * 0x14: alive-counter, add `.offset` to value,
        # * 0x15: alive-counter stopped/started according to `.dyn_pattern`
        # * 0x16: alive-counter stopped/started according to `.dyn_pattern`
        #         (continues counting while stopped)
        #
        # For CRC signals (see dedicated sub-class):
        # * 0x20: CRC calculated with default/correct algorithm (`.algo`)
        # * 0x21: CRC calculated with algorithm set in `.dyn_algo`
        # * 0x22: CRC calculated with algorithm from `.dyn_algo` while `.dyn_count` decrements, then mode 0x20
        # * 0x23: CRC calculated with `.algo`/`.dyn_algo` according to `.dyn_pattern`
        #
        self.mode_var = None
        
        ## Dynamic Countdown Value, see modes 0x03 and beyond
        self.dyn_count_var = None
        ## Dynamic Value: value that is active while dyn_count_var decrements.
        self.dyn_value_phy_var = None
        ## Dynamic Pattern Value, see modes 0x15/0x16/0x23
        self.dyn_pattern_var = None
        ## physical static override value (for mode 0x01)
        self.static_value_phy_var = None
        ## raw static override value (for mode 0x02)
        self.static_value_raw_var = None
        
        # Members inherited from CanBusSignal #################################
        # (see Note above) 
        
        ## Signal PV address/identifier as base identifier for deriving sub-elements.
        # For CAN/Gamma signals, related variables follow the form 
        # `<base_identifier>.<suffix>`
        self.base_identifier = None
        
        ## reference to associated (Rx-)CanBusMessage instance
        self.message = None
        
        # Members inherited from BusSignal ####################################
        # (see Note above) 
        
        ## parent context (a gaapi reference to resolve signal/variable PVs)
        self.context = None
        
        ## signal value variable. get/info methods of this RxCanBusSignal
        # will access this variable.
        self.signal_var = None
        
        ## unit of physical signal value (as string, mainly used for report entries)
        self.unit = None
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
        _bus_signals_cangamma.RxCanBusSignal.__init__(
            self, context=context, 
            signal_identifier=signal_identifier, message=message, 
            
            cycle_time=cycle_time, debounce_time=debounce_time,
            unit=unit, alias=alias, descr=descr, lookup=lookup,
            change_delay=change_delay, timeout=timeout, recovery_time=recovery_time,
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable, 
            see `signal_var`.
            Attention:
                For RxCanBusSignals, this will show info on the contents 
                of the HIL-send-buffer, not the value from Model/Simulink 
                source nor the last seen signal value on CAN bus.
            
            Returns the current info string from `signal_var`.
        """
        return _bus_signals_cangamma.RxCanBusSignal.info(self)
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable, see `signal_var`. 
            
            Attention:
                For RxCanBusSignals, this will get the current (raw) value 
                of the HIL-send-buffer, not the last seen signal value on CAN 
                bus.
            
            Returns the current value from `signal_var`.
        """
        return _bus_signals_cangamma.RxCanBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the static override variable  (`.static_value_phy_var`)
            and switch mode to use this value (mode 0x01).
            Use `.reset()` to clear override (or manually clear the mode setting).
            
            Parameters:
                value - value to set (physical)
            
            Returns the previous value from static_value_phy.
        """
        return _bus_signals_cangamma.RxCanBusSignal.set(self, value=value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data, 
            see `signal_var`. This uses the lookup values supplied in constructor.
            Fallback (if no matching state was found) will be the unmapped 
            numeric value.
            
            Attention:
                For RxCanBusSignals, this will get the current (raw) value 
                of the HIL-send-buffer, not the last seen signal value on 
                CAN bus.
            
            Returns the current state representation from `signal_var`.
        """
        return _bus_signals_cangamma.RxCanBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the static override variable 
            (`.static_value_phy_var`) and switch to use this value (mode 0x01).
            This uses the lookup values supplied in constructor.
            
            Parameters:
                state - named state to set
            
            Returns the previous value from static_value_phy.
        """
        return _bus_signals_cangamma.RxCanBusSignal.setState(self, state=state)
    
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
        return _bus_signals_cangamma.RxCanBusSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    # Inherited from RxCanBusSignalBasic
    # #########################################################################
    def enableHilTx(self):
        """ Enable transmission of signal HIL => DUT (if the assigned 
            CAN-Message/PDU supports it).
            
            Note:
                This will enable transmission of _all_ signals of the parent 
                Message/PDU.
        """
        return _bus_signals_cangamma.RxCanBusSignal.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable transmission of signal HIL => DUT (if the assigned 
            CAN-Message/PDU supports it). 
            
            Note:
                This will disable transmission of _all_ signals of the parent 
                Message/PDU.
        """
        return _bus_signals_cangamma.RxCanBusSignal.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger transmission ("kickout") of signal HIL => DUT (by 
            triggering the parent CAN-Message/PDU). 
            
            Note:
                All other signals of the parent Message/PDU will also be sent.
        """
        return _bus_signals_cangamma.RxCanBusSignal.kickout(self)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. Note that this
            will also switch the variable source switch back to its original 
            setting.
        """
        _bus_signals_cangamma.RxCanBusSignal.reset(self, *args, **kwargs)
        

# #############################################################################
class CrcRxCanBusSignal(_bus_signals_cangamma.CrcRxCanBusSignal):
    """ A CRC RX bus signal (HIL-Tx => ECU-Rx) """
    
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
    # - mode_var usually defaults to "CRC calculation active/enabled"
    #    * 0x22: CRC calculation enabled
    # - algo_var: CRC type (active CRC algorithm) should default to 
    #    "correct CRC" (which is typically algorithm 1)
    # - dyn_algo_var: dynamic algorithm override
    cfg_custom_defaults = {
        "algo_var":          None,   #
        "dyn_algo_var":      None,   #
        "mode_var":          None,   # for parent RxCanBusSignal
        "dyn_count_var":     None,   # for parent RxCanBusSignal
        "dyn_value_phy_var": None,   # for parent RxCanBusSignal
    }
    
    # #########################################################################
    def __init__(self, context, signal_identifier, 
                 message=None, cycle_time=None, debounce_time=None,
                 alias="", descr="", lookup=None,
                 error_delay=None, change_delay=None, timeout=None, 
                 recovery_time=None
                 ):
        """ CRC bus signal (HIL-Tx => ECU-Rx) initialization for Gamma-V based
            CAN signal manipulation options
            
            Parameters:
                context             -   parent gaapi context 
                signal_identifier   -   identifier for signal PV
                message             -   reference to parent RxCanBusMessage instance
                
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
        
        ## CRC algorithm type for "correct" CRC (normal mode)
        self.crc_normal_type = self.cfg_crc_normal_type # (copy from class attribute)
        ## CRC algorithm type for "incorrect" CRC (for error injection)
        self.crc_error_type  = self.cfg_crc_error_type  # (copy from class attribute)
        
        ## CRC algorithm type variable, selects active/default CRC algorithm.
        self.algo_var = None
        ## CRC dynamic algorithm type variable, selects active CRC algorithm
        # during dynamic error injection
        self.dyn_algo_var = None
        
        # Members inherited from RxCanBusSignal ###############################
        # (see Note above) 
        
        ## Dynamic Countdown value. 
        self.dyn_count_var = None
        ## Dynamic Value: value that is active while dyn_count_var decrements.
        self.dyn_value_var = None
        ## Dynamic Pattern value.
        self.dyn_pattern_var = None
        
        ## Physical static override value (for mode 0x01)
        self.static_value_phy_var = None
        ## Raw static override value (for mode 0x02)
        self.static_value_raw_var = None
        
        ## Mode switch variable for signal manipulation.  
        # (see RxCanBusSignal for full details)
        # 
        # For CRC signals:
        # * 0x20: CRC calculated with default/correct algorithm (.algo)
        # * 0x21: CRC calculated with algorithm set in .dyn_algo
        # * 0x22: CRC calculated with algorithm from .dyn_algo while .dyn_count decrements, then mode 0x20
        # * 0x23: CRC calculated with .algo/.dyn_algo according to .dyn_pattern
        self.mode_var = None
        
        # Members inherited from CanBusSignal #################################
        # (see Note above)
        
        ## Signal PV address/identifier as base identifier for deriving sub-elements.
        # For CAN/Gamma signals, related variables follow the form 
        # `<base_identifier>.<suffix>`
        self.base_identifier = None
        ## reference to associated (Rx-)CanBusMessage instance
        self.message = None
        
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
        _bus_signals_cangamma.CrcRxCanBusSignal.__init__(
            self, context=context, 
            signal_identifier=signal_identifier, message=message, 
            cycle_time=cycle_time, debounce_time=debounce_time, 
            alias=alias, descr=descr, lookup=lookup, 
            error_delay=error_delay, change_delay=change_delay, 
            timeout=timeout, recovery_time=recovery_time
        )
    
    # #########################################################################
    def setBasicCrcError(self):
        """ Switch CRC calculation to an algorithm producing incorrect CRCs.
            See CrcRxCanBusSignal.crc_error_type. 
        """
        # Example/Default:
        #     Algorithm 1: Correct CRC
        #     Algorithm 2: Incorrect CRC (correct CRC XOR 0xFF)
        return _bus_signals_cangamma.CrcRxCanBusSignal.setBasicCrcError(self)
    
    # #########################################################################
    def clearBasicCrcError(self):
        """ Switch CRC calculation back to an algorithm producing correct CRCs.
            See CrcRxCanBusSignal.crc_normal_type.
        """
        return _bus_signals_cangamma.CrcRxCanBusSignal.clearBasicCrcError(self)
        
    
    # #########################################################################
    # Methods inherited from RxCanBusSignal
    # #########################################################################
    def enableHilTx(self):
        """ Enable transmission of signal HIL => DUT.
            Note:
                This will enable transmission of _all_ signals of the parent 
                Message/PDU.
        """
        return _bus_signals_cangamma.CrcRxCanBusSignal.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable transmission of signal HIL => DUT.
            Note:
                This will disable transmission of _all_ signals of the parent 
                Message/PDU.
        """
        return _bus_signals_cangamma.CrcRxCanBusSignal.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger transmission ("kickout") of signal HIL => DUT (by 
            triggering the parent CAN-Message/PDU).
            Note:
                All other signals of the parent Message/PDU will also be sent.
        """
        return _bus_signals_cangamma.CrcRxCanBusSignal.kickout(self)
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/RxBusSignal
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable
            (typically not that useful for ECU-Rx/HIL-Tx CRC-Signals, though).
         """
        return _bus_signals_cangamma.CrcRxCanBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable. 
            Parameters:
                value - value to set
            Returns the previous value from `signal_var`.
        """
        return _bus_signals_cangamma.CrcRxCanBusSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data 
            (typically not that useful for ECU-Rx/HIL-Tx CRC-Signals, though).
            Returns the current state's description from `signal_var`.
        """
        return _bus_signals_cangamma.CrcRxCanBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor.
            Parameters:
                state - named state to set
            Returns the previous state's description.
        """
        return _bus_signals_cangamma.CrcRxCanBusSignal.setState(self, state)
    
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
        return _bus_signals_cangamma.CrcRxCanBusSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. 
            Returns an info string.
        """
        return _bus_signals_cangamma.CrcRxCanBusSignal.info(self)
        
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_cangamma.CrcRxCanBusSignal.reset(self, *args, **kwargs)
        

# #############################################################################
class CrcTxCanBusSignal(_bus_signals_cangamma.CrcTxCanBusSignal):
    """ A CRC TX bus signal (ECU-Tx => HIL-Rx), adds CRC validity info."""
    
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
    # - algo_var: CRC type (active CRC algorithm) should default to 
    #    "correct CRC" (which is typically algorithm 1)
    cfg_custom_defaults = {
        "algo_var":       None,   #
    }
    
    # #########################################################################
    def __init__(self, context, signal_identifier, 
                 message=None, cycle_time=None, debounce_time=None,
                 alias="", descr="", lookup=None,
                 change_delay=None, timeout=None, recovery_time=None
                 ):
        """ CRC bus signal (ECU-Tx => HIL-Rx) initialization for Gamma-V based
            CAN signal manipulation options
            
            Parameters:
                context             -   parent gaapi context 
                signal_identifier   -   identifier for CRC signal PV
                message             -   reference to associated RxCanBusMessage instance
                
                cycle_time      - (opt) cycle time in [ms], overrides settings in Message
                debounce_time   - (opt) minimum debounce delay between events in [ms],
                                        overrides settings in Message
                alias           - (opt) bus signal alias/name
                descr           - (opt) signal description
                lookup          - (opt) lookup table for values, see VarBase
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
        
        ## CRC algorithm type variable, selects active CRC algorithm
        ## to use for CRC validation.
        self.algo_var = None
        
        ## CRC check status variable
        self.crc_valid_var = None
        
        
        # #####################################################################
        _bus_signals_cangamma.CrcTxCanBusSignal.__init__(
            self, context=context, 
            signal_identifier=signal_identifier, message=message, 
            cycle_time=cycle_time, debounce_time=debounce_time,
            alias=alias, descr=descr, lookup=lookup,
            change_delay=change_delay, timeout=timeout, recovery_time=recovery_time,
        )
    
    # #########################################################################
    def getCrcStatus(self):
        """ Get status result of last CRC validation. """
        return _bus_signals_cangamma.CrcTxCanBusSignal.getCrcStatus(self)
        
    
    # #########################################################################
    # Inherited from TxCanBusSignal
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable, 
            see `signal_var`
            Returns the current info string from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignal.info(self)
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL CRC signal variable, see `signal_var`. 
            Returns the current value from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable, see `signal_var`
            
            Attention:
                For TxCanBusSignals, this will only overwrite the current 
                contents of the HIl receive buffer of the signal (which is 
                typically not too useful as it will be overwritten on next 
                update with data from CAN plugin)
            
            Parameters:
                value - value to set
            
            Returns the previous value from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data, 
            see `signal_var`. This uses the lookup values supplied in constructor.
            Fallback (if no matching state was found) will be the unmapped 
            numeric value.
            
            Returns the current state representation from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable, see `signal_var`.
            This uses the lookup values supplied in constructor.
            
            Attention:
                For TxFrBusSignals this will only overwrite the current 
                contents of the HIl receive buffer of the signal 
                (which typically is not too useful).
            
            Parameters:
                state - named state to set
            
            Returns the previous state representation from `signal_var`.
        """
        return _bus_signals_cangamma.TxCanBusSignal.setState(self, state)
    
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
        return _bus_signals_cangamma.TxCanBusSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_cangamma.TxCanBusSignal.reset(self, *args, **kwargs)
        

# #############################################################################
class AcRxCanBusSignal(_bus_signals_cangamma.AcRxCanBusSignal):
    """ Alive counter RX bus signal (HIL-Tx => ECU-Rx). """
    
    ## Configuration settings for new instances:  
    # Custom "hard" default value(s) to use for internal real time system 
    # variables. See RxFrBusSignal for further details.
    #
    # Mapping: <variable name as string>: <default value>
    #
    # Typical default values:
    # - mode switches for alive counters usually default to "running counter"
    #   See RxFrBusSignal for further details.
    # - Counter Offset, additive offset to counter value defaults to 0 
    cfg_custom_defaults = {
        "offset_var":        None, # offset to add to current counter value
        "mode_var":          None, # for parent RxCanBusSignal
        "dyn_count_var":     None, # for parent RxCanBusSignal
        "dyn_value_phy_var": None, # for parent RxCanBusSignal
    }
    
    # #########################################################################
    def __init__(self, context, signal_identifier, 
                 message=None, cycle_time=None, debounce_time=None,
                 alias="", descr="", lookup=None,
                 error_delay=None, change_delay=None, timeout=None, 
                 recovery_time=None
                 ):
        """ Alive counter bus signal (HIL-Tx => ECU-Rx) initialization for 
            Gamma-V based CAN signal manipulation options
            
            Parameters:
                context             -   parent gaapi context 
                signal_identifier   -   identifier for alive counter signal PV
                message             -   reference to associated RxCanBusMessage instance
                
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
        
        ## delay to wait after a "simple" alive counter error injection [ms] 
        self.error_delay = None
        
        ## Variable with additional alive counter offset
        # (offset will simply be added to current counter value)
        self.offset_var = None
        
        
        # Members inherited from RxCanBusSignal ###############################
        # (see Note above) 
        
        ## Dynamic Countdown value. 
        self.dyn_count_var = None
        ## Dynamic Value: value active while dyn_count_var decrements 
        # (depending on selected mode).
        self.dyn_value_var = None
        ## Dynamic Pattern value.
        self.dyn_pattern_var = None
        
        ## Physical static override value (for mode 0x01)
        self.static_value_phy_var = None
        ## Raw static override value (for mode 0x02)
        self.static_value_raw_var = None
        
        ## Mode switch variable for signal manipulation
        # (see RxCanBusSignal for full details)
        # 
        # For alive-counter signals:
        # * 0x10: alive-counter, counting
        # * 0x11: alive-counter, stopped (static value)
        # * 0x12: alive-counter, stopped while .dyn_count decrements, then continues counting from last count (mode 0x10)
        # * 0x13: alive-counter, stopped while .dyn_count decrements, continues counting in background (then mode 0x10)
        # 
        # * 0x14: alive-counter, add .offset to value
        # * 0x15: alive-counter stopped/started according to .dyn_pattern
        # * 0x16: alive-counter stopped/started according to .dyn_pattern (continues counting while stopped)
        self.mode_var = None
        
        # Members inherited from CanBusSignal #################################
        # (see Note above) 
        
        ## Signal PV address/identifier as base identifier for deriving sub-elements.
        # For CAN/Gamma signals, related variables follow the form 
        # `<base_identifier>.<suffix>`
        self.base_identifier = None
        ## reference to associated (Rx-)CanBusMessage instance
        self.message = None
        
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
        _bus_signals_cangamma.AcRxCanBusSignal.__init__(
            self, context=context, 
            signal_identifier=signal_identifier, message=message, 
            
            cycle_time=cycle_time, debounce_time=debounce_time, 
            alias=alias, descr=descr, lookup=lookup, 
            
            error_delay=error_delay, change_delay=change_delay, 
            timeout=timeout, recovery_time=recovery_time
        )
    
    # #########################################################################
    def setBasicAcError(self):
        """ Stop and hold Alive Counter at the current count. """
        # For alive counter signals:
        # 0x10: alive-counter, counting
        # 0x11: alive-counter, stopped (static value)
        # 0x12: alive-counter, stopped while .dyn_count decrements, then continues counting from last count (mode 0x10)
        # 0x13: alive-counter, stopped while .dyn_count decrements, continues counting in background (then mode 0x10)
        # 
        # 0x14: alive-counter, add .offset to value
        # 0x15: alive-counter stopped/started according to .dyn_pattern
        # 0x16: alive-counter stopped/started according to .dyn_pattern (continues counting while stopped)
        return _bus_signals_cangamma.AcRxCanBusSignal.setBasicAcError(self)
    
    # #########################################################################
    def clearBasicAcError(self):
        """ (Re-)enable normal Alive Counter behaviour (i.e. continue counting)."""
        return _bus_signals_cangamma.AcRxCanBusSignal.clearBasicAcError(self)
        
    
    # #########################################################################
    # Methods inherited from  RxCanBusSignal
    # #########################################################################
    def enableHilTx(self):
        """ Enable transmission of signal HIL => DUT.
            Note:
                This will enable transmission of _all_ signals of the parent 
                Message/PDU.
        """
        return _bus_signals_cangamma.AcRxCanBusSignal.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable transmission of signal HIL => DUT.
            Note:
                This will disable transmission of _all_ signals of the parent 
                Message/PDU.
        """
        return _bus_signals_cangamma.AcRxCanBusSignal.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger transmission ("kickout") of signal HIL => DUT (by 
            triggering the parent CAN-Message/PDU).
            Note:
                All other signals of the parent Message/PDU will also be sent.
        """
        return _bus_signals_cangamma.AcRxCanBusSignal.kickout(self)
        
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/RxBusSignal
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable (typically not 
            that useful for ECU-Rx/HIL-Tx AC-signals, though).
            Returns the current value from `signal_var`.
         """
        return _bus_signals_cangamma.AcRxCanBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable. 
            Parameters:
                value - value to set
            Returns the previous value from `signal_var`.
        """
        return _bus_signals_cangamma.AcRxCanBusSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data
            (typically not that useful for ECU-Rx/HIL-Tx AC-signals, though).
            Returns the current state's description.
        """
        return _bus_signals_cangamma.AcRxCanBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor.
            Parameters:
                state - named state to set
            Returns the previous state's description.
        """
        return _bus_signals_cangamma.AcRxCanBusSignal.setState(self, state)
    
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
        return _bus_signals_cangamma.AcRxCanBusSignal.getStateDescr(
            self, value=value, fallback=fallback
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. 
            Returns an info string.
        """
        return _bus_signals_cangamma.AcRxCanBusSignal.info(self)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. """
        _bus_signals_cangamma.AcRxCanBusSignal.reset(self, *args, **kwargs)
        

# #############################################################################
# Signal Container ---
# #############################################################################
class CanBusSignalContainer(_bus_signals_cangamma.CanBusSignalContainer):
    """ A BusSignalContainer for CAN Bus Signals """
    # #########################################################################
    def __init__(self, context):
        """ Override to add signals.
            
            Parameters:
                context - context used for contained BusSignals
        """
        _bus_signals_cangamma.CanBusSignalContainer.__init__(self, context)
    
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
        _bus_signals_cangamma.CanBusSignalContainer.resetAll(
            self, 
            verbosity=verbosity, 
            recursion_depth=recursion_depth
        )
    
    # #########################################################################
    def iterSignals(self, msg):
        """ Iterate over all signals that reference the specified CAN message/PDU.
            
            Parameters:
                msg - a CAN message/PDU instance
            
            Usage:
                for sig in bus.iterSignals(bus.tx_msg_FNORD):
                    print sig
            
            Returns an iterator object.
        """
        return _bus_signals_cangamma.CanBusSignalContainer.iterSignals(
            self, msg=msg
        )
        

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    import os
    import time
    import ttk_tools.rst.gamma_api_offline_stub as gamma_api
    
    base_path = r"D:\HIL_Projekte\Etaoin\Datenmodell"
    gamma = gamma_api.Gamma(
        system_file       = os.path.join(base_path, "system.xml"),
        config_file       = os.path.join(base_path, "config_local.xml"), 
        system_name_local = 'iSyst',
    )
    print "\n== get gamma version information ================================"
    print gamma.getGammaVersioninfo()
    
    print "gaapi (ref) version:", gamma.getReference().getVersion()
    
    
    
    # #########################################################################
    class BusSignals(CanBusSignalContainer):
        def __init__(self, gamma):
            self.tx_msg = TxCanBusMessage(gamma, 
                "iSyst:BusSystems.can3_iFIU_iSRC.HIL_RX.N0FIU_Status_Card19.payload", 
                cycle_time=100, debounce_time=10
            )
            self.rx_msg = RxCanBusMessage(gamma, 
                "iSyst:BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.payload", 
                cycle_time=100, debounce_time=10, alias="BAZ_Message"
            )
            self.rx_msg2 = RxCanBusMessage(gamma, 
                base_identifier="iSyst:BusSystems.can3_iFIU_iSRC.HIL_RX.FnordMsg.payload", 
                cycle_time=50, debounce_time=10
            )
            
            #
            self.BarBazSig  = TxCanBusSignal(gamma, "iSyst:BusSystems.can3_iFIU_iSRC.HIL_RX.N0FIU_Status_Card19.signals.State_Path_3_break.value", self.tx_msg)
            
            #
            self.FooBarSig  = RxCanBusSignal(gamma, "BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.value", self.rx_msg)
            self.BazQuuxSig = RxCanBusSignal(gamma, "BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_2.value", self.rx_msg)
            self.AnotherSig = RxCanBusSignal(gamma, "iSyst:BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_break.value", 
                alias="Another Bus Signal", descr="Another Signal to test", unit="rpm", 
                message=self.rx_msg, 
                change_delay=250, timeout=500, recovery_time=500,
            )
            
            self.BasicSig  = RxCanBusSignal(gamma, "BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_1.value", self.rx_msg)
            self.BazQuuxSig = RxCanBusSignal(gamma, "BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_2.value", self.rx_msg)
            self.AnotherSig = RxCanBusSignal(gamma, "iSyst:BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_break.value", 
                alias="Another Bus Signal", descr="Another Signal to test", unit="rpm", 
                message=self.rx_msg, 
                change_delay=250, timeout=500, recovery_time=500,
            )
            
            self.basicTxSig = TxCanBusSignalBasic(gamma, "iSyst:BusSystems.can3_iFIU_iSRC.HIL_RX.N0FIU_Status_Card19.signals.State.value",  self.tx_msg)
            self.basicRxSig = TxCanBusSignalBasic(gamma, "BusSystems.can3_iFIU_iSRC.HIL_TX.N0FIU_SetError_Card1.signals.Path_1_EI_2.value", self.rx_msg)
            
            #
            self.crc_signal = CrcRxCanBusSignal(gamma, "iSyst:BusSystems.can3_iFIU_iSRC.HIL_TX.FnordMsg.signals.CRC_Signal",          self.rx_msg2)
            self.ac_signal  = AcRxCanBusSignal(gamma,  "iSyst:BusSystems.can3_iFIU_iSRC.HIL_TX.FnordMsg.signals.AliveCounter_Signal", self.rx_msg2)
            
    
    bus_signals = BusSignals(gamma.getReference())
    
    print "# initial:"
    print bus_signals.FooBarSig.info()
    print bus_signals.BazQuuxSig.info()
    print bus_signals.AnotherSig.info()
    bus_signals.FooBarSig.set(1234)
    bus_signals.AnotherSig.set(1000)
    bus_signals.basicRxSig.set(42)
    
    time.sleep(bus_signals.AnotherSig.cycle_time / 1000.0)
    
    
    
    print "# changed:"
    print bus_signals.FooBarSig.info()
    print bus_signals.BazQuuxSig.info()
    print bus_signals.AnotherSig.info()
    print bus_signals.basicRxSig.info()
    
    print
    bus_signals.resetAll()
    print "# reset:"
    print bus_signals.FooBarSig.info()
    print bus_signals.BazQuuxSig.info()
    print bus_signals.AnotherSig.info()
    print bus_signals.basicRxSig.info()
    
    
    print 
    print "# iterSignals:"
    print 'Signals in rx_msg ("%s"):'%(bus_signals.rx_msg.alias)
    for sig in bus_signals.iterSignals(bus_signals.rx_msg):
        print " -> %-100s (%s)"%(sig, type(sig).__name__)
    
    print 'Signals in tx_msg ("%s"):'%(bus_signals.tx_msg.alias)
    for sig in bus_signals.iterSignals(bus_signals.tx_msg):
        print " -> %-100s (%s)"%(sig, type(sig).__name__)
    
    print "#" * 80
    
    def pv(obj, name):
        var = getattr(obj, name, None)
        print "  %-16s -> %-12s %s"%(name, type(var).__name__, var)
        
    
    print "-------------------------------------------------------------------"
    print bus_signals.ac_signal.message.alias
    pv(bus_signals.ac_signal.message, "cycle_time_var")
    pv(bus_signals.ac_signal.message, "kickout_var")
    print bus_signals.ac_signal.alias
    pv(bus_signals.ac_signal, "mode_var")
    pv(bus_signals.ac_signal, "ac_offset_var")
    
    print "-------------------------------------------------------------------"
    print bus_signals.FooBarSig.message.alias
    pv(bus_signals.FooBarSig.message, "cycle_time_var")
    pv(bus_signals.FooBarSig.message, "kickout_var")
    print bus_signals.FooBarSig.alias
    pv(bus_signals.FooBarSig, "mode_var")
    
    print "-------------------------------------------------------------------"
    print bus_signals.rx_msg.alias
    pv(bus_signals.rx_msg, "cycle_time_var")
    pv(bus_signals.rx_msg, "kickout_var")
    print bus_signals.rx_msg2.alias
    pv(bus_signals.rx_msg2, "cycle_time_var")
    pv(bus_signals.rx_msg2, "kickout_var")
    
    
    print "\nDone."
# @endcond DOXYGEN_IGNORE
# #############################################################################
