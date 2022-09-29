#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : bus_signals_frbs.py
# Package : ttk_bus
# Task    : Wrapper classes for bus/interface signal descriptions.
#           Specific implementation for dSpace FlexRay blocksets (using 
#           PDU-based blockset generation with signals added to BusSystems)
# Python  : 2.5+
# Type    : Interface
#
# Copyright 2015 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Author    | Description
#------------------------------------------------------------------------------
# 1.0  | 18.02.2015 | L.Morgus  | initial
# 1.1  | 26.02.2015 | J.Tremmel | expanded descriptions and examples
# 1.2  | 16.12.2015 | J.Tremmel | tweaked docstrings and sample code in __main__
# 1.3  | 25.02.2016 | J.Tremmel | added FrBusSignalContainer with iterSignals()
#                               | added config class variables for default 
#                               | values of "internal" HilVars as well as values
#                               | for Rx-PDU disable mode and CRC normal/error 
#                               | types (all with prefix cfg_)
# 1.6  | 25.11.2016 | J.Tremmel | updated interface methods
# 1.7  | 29.08.2017 | J.Tremmel | added interface descriptions for getStateDescr methods
# 1.8  | 15.07.2020 | J.Tremmel | removed obsolete signal parameters min/max_value
#******************************************************************************
"""
@package ttk_bus.bus_signals_frbs
Interface wrapper for bus/interface signal classes in ttk_bus._bus_signals_frbs.
Specific implementation for dSpace FlexRay blocksets using PDU-based blockset 
generation with signals added to Trc/BusSystems.

Convention:
    Signal directions are relative to the DUT:
      * Tx - transmitted by ECU => received from HIL
      * Rx - received by ECU <= transmitted from HIL
"""
import _bus_signals_frbs
from   _bus_signals_frbs import FrbsError # @UnusedImport (just to make it available)


# #############################################################################
class FrTxPdu(_bus_signals_frbs.FrTxPdu):
    """ FlexRay ECU-Tx (ECU-Tx => HIL-Rx) PDU data. 
        Extends FrPdu with access to status variables `error_status_var` and 
        `data_receive_counter_var`.
    """
    # #########################################################################
    def __init__(self, context, cycle_time=0, debounce_time=0, 
                 bus_systems_path=None,
                 alias='', descr='',
                 change_delay=None, timeout=None, recovery_time=None):
        """ FlexRay ECU-Tx (HIL-Rx) PDU data.
            
            Parameters:
                context           - parent context (an RTE application instance to 
                                    resolve signal/variable paths)
                cycle_time        - cycle time in [ms], 0 for event-triggered PDUs
                debounce_time     - minimum debounce delay time between events in 
                                    [ms] for event-triggered PDUs
                
                bus_systems_path  - base path to PDU below Bus Systems
                
                alias             - PDU alias/name
                descr             - (opt) PDU description (may be used in report entries)
                
                change_delay      - (opt) delay to wait after a value change [ms],  
                                          defaults to 2x max(cycle_time, debounce_time)
                timeout           - (opt) detection time for timeout errors [ms],  
                                          defaults to 2x max(cycle_time, debounce_time)
                recovery_time     - (opt) time for recovery/"wiedergut" checks [ms],  
                                          defaults to 2x max(cycle_time, debounce_time)
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion  may 
        #       find them even if the base class code cannot be analyzed.
        
        ## HIL-Rx PDU Error Status variable (a "HilVar" instance).
        # > "Indicates various statuses. Each status has its own bit,  
        # >  so parallel statuses are possible."
        # 
        # - Bit 0: Communication controller (CC) FlexRay bus synchronization error
        #       * 0: CC is synchronized 
        #       * 1: CC not synchronized
        # - Bit 1: Buffer access error
        #       * 0: no buffer access error 
        #       * 1: error while accessing buffer
        # - Bit 2: Boundary violation in FlexRay slot
        #       * 0: no boundary violation detected
        #       * 1: boundary violation detected
        # - Bit 3: Syntax error in FlexRay slot
        #       * 0: no syntax error detected
        #       * 1: syntax error detected
        # - Bit 4: Content error in FlexRay slot
        #       * 0: no content error detected
        #       * 1: content error detected
        # - Bit 5: Empty slot (FlexRay static frames only)
        #       * 0: data received in static slot
        #       * 1: slot is empty, no data received in static slot
        # - Bit 6: Software CRC calculation error
        #       * 0: CRC from last received frame is correct (or CRC calculation deactivated). 
        #       * 1: CRC from last received frame is not correct.
        # - Bits 7 to 15: unused
        #
        self.error_status_var = None
        
        ## HIL-Rx Data Receiver Counter variable (a "HilVar" instance).
        # > "Counts the number of received PDUs. Null frames are ignored."
        self.data_receive_counter_var = None
        
        ## HIL-Rx Nullframe variable (a "HilVar" instance).
        # > "Indicates whether the received frame was a null frame
        # >  (only for static PDUs)"
        #  * 0: last received frame was not a null frame
        #  * 1: last received frame was a null frame
        self.nullframe_var = None
        
        # Members inherited from FrPdu (see Note above) #######################
        ## PDU alias name
        self.alias = None
        ## PDU description text
        self.descr = None
        ## context (reference to assigned RTE application instance)
        self.context = None
        ## base path to PDU below BusSystems
        self.bus_systems_path = None
        
        # timings #############################################################
        ## cycle time of PDU in [ms]
        self.cycle_time = None
        ## minimum debounce delay for event-triggered PDUs in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        # #####################################################################
        _bus_signals_frbs.FrTxPdu.__init__(
            self, context=context,
            cycle_time=cycle_time, 
            debounce_time=debounce_time,
            bus_systems_path=bus_systems_path,
            alias=alias, descr=descr,
            change_delay=change_delay,
            timeout=timeout,
            recovery_time=recovery_time,
        )
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs): 
        """ Call reset() on all contained variables/signals that support it.
            Simple, non-recursive approach.
        """
        _bus_signals_frbs.FrTxPdu.reset(self, *args, **kwargs)
        

# #############################################################################
class FrRxPdu(_bus_signals_frbs.FrRxPdu):
    """ FlexRay ECU-Rx (HIL-Tx => ECU-Rx) PDU data.
        Extends FrPdu with methods for enableHilTx(), disableHilTx() and 
        kickout() (trigger).
    """
    ## Configuration setting for new instances: 
    # Disable mode to use if no specific mode has been supplied in constructor.
    #
    # Mode used for disabling PDU Hil-Tx:
    # * "tm" - use user defined transmission mode (99), which is strictly event/trigger-based 
    # * "ub" - use Update Bit configuration (availability depends on FR configuration)
    # * "en" - use an available enable switch (Tx, HW or SW Enable)
    cfg_disable_mode = "tm"
    
    ## Configuration setting for new instances: 
    # Custom "hard" default values to use for internal real time system 
    # variables (for example: switch settings), so a reset() will always 
    # reset those variables to defined values (and not just those that were 
    # accessed).  
    # This might be helpful if "other" tests fail to properly clean up the
    # test environment after they are done.
    # 
    # Mapping: <variable name as string>: <default value>
    #
    # A value of None (or a missing variable name) enables normal/automatic 
    # reset behavior.
    #
    # Typical default values:
    # - source switches usually default to "source: simulink model"
    #    * 0: source: model/trc 
    #    * 1: source: bus systems
    # - tx-enable vars default to "enabled"
    #    * 0: tx disabled 
    #    * 1: tx enabled
    # - Transmission Mode depends on PDU setup, usually the default is "TM True"
    #    *  0: TM False
    #    *  1: TM True
    #    * 99: TM user defined 
    # - kickout/trigger variables: Triggers below BusSystems will (should...) 
    #   auto-reset to 0 once the PDU has been triggered. 
    # - Update Bit behavior defaults to "automatic"
    #    * 0: use automatic Update Bit 
    #    * 1: use static Update Bit (from associated /Value)  
    #
    cfg_custom_defaults = {
        "tx_enable_var":         None,
        "tx_enable_switch":      None,
        "update_bit_enable_var": None,
        "update_bit_switch":     None,
        "tm_var":                None,
        "tm_switch":             None,
        "manual_enable_var":     None,
        "kickout_var":           None,
        "kickout_switch":        None,
    }
    
    # #########################################################################
    def __init__(self, context, cycle_time=0, debounce_time=0,
                 enable_path=None, bus_systems_path=None,
                 alias='', descr='',
                 change_delay=None, timeout=None, recovery_time=None,
                 disable_mode=None):
        """ FlexRay ECU-Rx (HIL-Tx) PDU data.
            
            Parameters:
                context           - parent context (an RTE application instance to 
                                    resolve signal/variable paths)
                
                cycle_time        - cycle time in [ms], 0 for event-triggered PDUs
                debounce_time     - minimum debounce delay time between events 
                                    in [ms]
                enable_path       - model path to manually added tx enable switch 
                                    (if available). This will override any
                                    disable switches in BusSystems
                bus_systems_path  - base path to PDU below Bus Systems
                
                alias             - PDU alias/name
                descr             - (opt) PDU description (may be used in report entries)
                
                change_delay      - (opt) delay to wait after a value change [ms],  
                                          defaults to 2x max(cycle_time, debounce_time)
                timeout           - (opt) detection time for timeout errors [ms],  
                                          defaults to 2x max(cycle_time, debounce_time)
                recovery_time     - (opt) time for recovery/"wiedergut" checks [ms],  
                                          defaults to 2x max(cycle_time, debounce_time)
                
                disable_mode      - (opt) mode used for disabling PDU Hil-Tx:  
                                        * "tm": use the user defined transmission 
                                                mode (99), which is strictly 
                                                event/trigger-based  
                                        * "ub": use Update Bit configuration
                                                (availability depends on FR 
                                                configuration)  
                                        * "en": use an available enable switch 
                                                (Tx, HW or SW Enable)  
                                        * None: configured cfg_disable_mode will be used.
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class' code cannot be analyzed.
        
        ## HIL-Tx-enable/disable variable (for disable_mode: en)
        # (a "HilVar" instance)
        self.tx_enable_var          = None
        ## HIL-Tx-enable/disable source-switch (for disable_mode: en)  
        # (a "HilVar" instance)
        self.tx_enable_switch       = None
        
        ## Update Bit handling variable (for disable_mode: ub)  
        # (a "HilVar" instance)
        self.update_bit_enable_var  = None
        ## Update Bit handling source-switch (for disable_mode: ub)  
        # (a "HilVar" instance)
        self.update_bit_switch      = None
        
        ## Transmission Mode handling variable (for disable_mode: tm)  
        # (a "HilVar" instance)
        self.tm_var                 = None
        ## Transmission Mode handling source-switch (for disable_mode: tm)  
        # (a "HilVar" instance)
        self.tm_switch              = None
        
        ## Manual enable switch variable (when specified via enable_path)  
        # (a "HilVar" instance)
        self.manual_enable_var      = None
        
        ## PDU Kickout/Trigger variable  
        # (a "HilVar" instance)
        self.kickout_var            = None
        ## PDU Kickout/Trigger source-switch  
        # (a "HilVar" instance)
        self.kickout_switch         = None
        
        # Members inherited from FrPdu (see Note above) #######################
        ## PDU alias name
        self.alias = None
        ## PDU description text
        self.descr = None
        ## context (reference to assigned RTE application instance)
        self.context = None
        ## base path to PDU below BusSystems
        self.bus_systems_path = None
        
        # timings #############################################################
        ## cycle time of PDU in [ms]
        self.cycle_time = None
        ## minimum debounce delay for event-triggered PDUs in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        # #####################################################################
        _bus_signals_frbs.FrRxPdu.__init__(
            self, context=context, 
            cycle_time=cycle_time, 
            debounce_time=debounce_time, 
            enable_path=enable_path, 
            bus_systems_path=bus_systems_path, 
            alias=alias, descr=descr,
            change_delay=change_delay, 
            timeout=timeout, recovery_time=recovery_time, 
            disable_mode=disable_mode
        )
    
    # #########################################################################
    def initUpdateBitControl(self):
        """ Initialize variables for Update Bit control. Will be called 
            automatically depending on selected disable_mode during __init__.  
            See FrRxPdu.update_bit_switch, FrRxPdu.update_bit_enable_var
        """
        _bus_signals_frbs.FrRxPdu.initUpdateBitControl(self)
    
    # #########################################################################
    def initTransmissionModeControl(self):
        """ Initialize variables for Transmission Mode control. Will be called 
            automatically depending on selected disable_mode during __init__.  
            See FrRxPdu.tm_switch, FrRxPdu.tm_var
        """
        _bus_signals_frbs.FrRxPdu.initTransmissionModeControl(self)
    
    # #########################################################################
    def initTxEnableControl(self):
        """ Initialize variables for Tx Enable control. Will be called 
            automatically depending on selected disable_mode during __init__.  
            See FrRxPdu.tx_enable_switch, FrRxPdu.tx_enable_var
        """
        _bus_signals_frbs.FrRxPdu.initTxEnableControl(self)
    
    # #########################################################################
    def enableHilTx(self):
        """ (Re-)enable sending of PDU, depending on selected disable_mode 
            (see __init__). This overrides current settings from Simulink Model, 
            use FrRxPdu.reset() to restore initial behavior.
        """
        _bus_signals_frbs.FrRxPdu.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable sending of PDU, depending on selected disable_mode 
            (see __init__). This overrides current settings from Simulink Model,
            use FrRxPdu.reset() to restore initial behavior.
        """
        _bus_signals_frbs.FrRxPdu.disableHilTx(self)
        
    
    # #########################################################################
    def kickout(self, delay_ms=None):
        """ Trigger sending of the PDU. 
            
            Parameters: 
                delay_ms - [ms] Delay to wait before clearing kickout/trigger 
                           variable again (it _should_ auto-reset if trigger 
                           variable is located below BusSystems, but anyway).
            
            Info: Default Delay:
               Delay defaults to 1/2 self.debounce_time (if debounce_time is 
               explicitly set) or alternatively to 1/2 self.change_delay.  
               Default delay will never be shorter than 5 ms.
            
        """
        _bus_signals_frbs.FrRxPdu.kickout(self, delay_ms=delay_ms)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs): 
        """ Call reset() on all contained variables/signals that support it.
            Simple, non-recursive approach.
        """
        _bus_signals_frbs.FrRxPdu.reset(self, *args, **kwargs)
        

# #############################################################################
class TxFrBusSignal(_bus_signals_frbs.TxFrBusSignal):
    """ A FLexRay signal sent from DUT to the test system (ECU Tx => HIL Rx). 
        
        This class mainly adds a member variable `status_var` that contains 
        the HIL-Rx status of the signal (useful for `NOT-VALID` values, as the 
        received signal will remain at the last valid value).
    """
    # #########################################################################
    def __init__(self, context, base_path, pdu=None, 
                 cycle_time=None, debounce_time=None,
                 unit="", alias="", descr="", lookup=None,
                 change_delay=None, timeout=None, recovery_time=None):
        """ Tx bus signal initialization.
            
            Example: BusSystems Path Structure:
                # path to signal value variable
                BusSystems/FlexRay/Monitoring/ECU_NAME/Channel A/PDU_NAME/Signals/SIGNAL_NAME_IN/Value
                # or
                BusSystems/FlexRay/Monitoring/ECU_NAME/Channel A/PDU_NAME/Signals/SIGNAL_NAME_IN/Physical Value
            
            Parameters:
                context       - parent context (an RTE application instance to 
                                resolve signal/variable paths)
                base_path     - base path to signal below BusSystems (use path 
                                to `/Value` or `/Physical Value` as appropriate)
                pdu           - reference to associated TxFrPdu instance
                
                cycle_time    - (opt) cycle time in [ms], overrides settings in PDU
                debounce_time - (opt) minimum debounce delay time in [ms], 
                                      overrides settings in PDU
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
        
        ## HIL-Rx-Status information (a "HilVar" instance).
        # > "Status information of the received or monitored signal. Only 
        # >  available if signal is selected for 'Signal RX Status Access'
        # >  feature in FlexRay Configuration Tool"  
        # > (compare FlexRayConfigFeatures.pdf)
        #
        # The values have the following meanings:
        # * 0: No error
        # * 1: Access error
        # * 2: Signal is not received
        # * 4: Signal is invalid
        # * 8: CRC is incorrect 
        #
        self.status_var = None
        
        
        # Members inherited from FrBusSignal (see Note above) #################
        
        ## model path of value variable
        self.value_path = None
        ## base model path (base path used for deriving sub-element paths)
        self.base_path = None
        ## reference to parent FrRxPdu
        self.pdu = None
        
        
        # Members inherited from BusSignal (see Note above) ###################
        
        ## context (reference to assigned RTE application instance)
        self.context = None
        ## main bus signal variable on HIL-side (a "HilVar" instance)
        self.signal_var = None
        ## signal alias name (from signal_var)
        self.alias = None
        ## signal unit  (from signal_var)
        self.unit  = None
        ## signal description text
        self.descr  = None
        
        # timings #############################################################
        ## cycle time of signal in [ms] (that is, of the associated message or PDU)
        self.cycle_time = None
        ## minimum debounce delay for event-triggered signals in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        # #####################################################################
        _bus_signals_frbs.TxFrBusSignal.__init__(
            self, context, 
            base_path=base_path, pdu=pdu, 
            cycle_time=cycle_time, debounce_time=debounce_time,
            unit=unit, alias=alias, descr=descr, lookup=lookup,
            change_delay=change_delay, timeout=timeout, 
            recovery_time=recovery_time, 
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable,
            see signal_var.
            Returns the current info string from signal_var.
        """
        return _bus_signals_frbs.TxFrBusSignal.info(self)
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable, see signal_var. 
            Returns the current value from signal_var.
        """
        return _bus_signals_frbs.TxFrBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable, see signal_var. 
            
            Note: 
                For TxFrBusSignals this will only overwrite the current
                contents of the HIl receive buffer of the signal 
                (which is not too useful).
            
            Parameters:
                value - new value to set
            
            Returns the previous value from signal_var.
        """
        return _bus_signals_frbs.TxFrBusSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data. 
            This uses the lookup values supplied in constructor, see signal_var.
            Fallback (if no matching state was found) will be the unmapped 
            numeric value. 
            
            Returns the current state representation from signal_var.
        """
        return _bus_signals_frbs.TxFrBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable, see signal_var. 
            This uses the lookup values supplied in constructor. 
            
            Note:
                For TxFrBusSignals this will only overwrite the current
                contents of the HIl receive buffer of the signal (which is not 
                too useful).
            
            Parameters:
                state - named state to set
            
            Returns the previous state description from signal_var.
        """
        return _bus_signals_frbs.TxFrBusSignal.setState(self, state)
    
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
        return _bus_signals_frbs.TxFrBusSignal.getStateDescr(self, value=value, fallback=fallback)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable members/variables of this bus signal. """
        _bus_signals_frbs.TxFrBusSignal.reset(self, *args, **kwargs)
        

# #############################################################################
class RxFrBusSignal(_bus_signals_frbs.RxFrBusSignal):
    """ A FlexRay signal sent from test system to the DUT (ECU Rx <= HIL Tx). 
    """
    
    ## Configuration setting for new instances: 
    # Custom "hard" default value(s) to use for internal real time system 
    # variables (for example: switch settings), so a reset() will always reset 
    # those variables to defined values (and not just those variables that have 
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
    # - source switches usually default to "source: simulink model"
    #    * 0: source: simulink model/trc 
    #    * 1: source: bus systems
    #
    cfg_custom_defaults = {
        "switch_var": None,
    }
    
    # #########################################################################
    def __init__(self, context, base_path, pdu=None, 
                 cycle_time=None, debounce_time=None,
                 unit="", alias="", descr="", lookup=None,
                 change_delay=None, timeout=None, recovery_time=None):
        """ Rx bus signal initialization.
            
            Example: BusSystems Signal Path Structure:
                # path to signal value variable
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/SIGNAL_NAME_OUT/Value
                # or 
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/SIGNAL_NAME_OUT/Physical Value
            
            Parameters:
                context       - parent context (an RTE application instance to 
                                resolve signal/variable paths)
                base_path     - base path to signal below BusSystems (use path 
                                to `/Value` or `/Physical Value` as appropriate)
                pdu           - reference to associated RxFrPdu instance
                
                cycle_time    - (opt) cycle time in [ms], overrides settings in PDU
                debounce_time - (opt) minimum debounce delay time in [ms], 
                                      overrides settings in PDU
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
        
        ## Source Switch variable (a "HilVar" instance).
        # * 0: value source is Simulink Model 
        # * 1: value source is BusSystems
        self.switch_var = None
        
        
        # Members inherited from FrBusSignal (see Note above) #################
        
        ## model path of value variable
        self.value_path = None
        ## base model path (base path for deriving sub-element paths)
        self.base_path = None
        ## reference to parent FrRxPdu
        self.pdu = None
        
        # Members inherited from BusSignal (see Note above) ###################
        
        ## context (reference to assigned RTE application instance)
        self.context = None
        ## main bus signal variable on HIL-side, (a "HilVar" instance)
        self.signal_var = None
        ## signal alias name (from signal_var)
        self.alias = None
        ## signal unit (from signal_var)
        self.unit  = None
        ## signal description text
        self.descr  = None
        
        
        # timings #############################################################
        ## cycle time of signal in [ms] (that is, of the associated message or PDU)
        self.cycle_time = None
        ## minimum debounce delay for event-triggered signals in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        
        # #####################################################################
        _bus_signals_frbs.RxFrBusSignal.__init__(
            self, context, 
            base_path=base_path, pdu=pdu, 
            cycle_time=cycle_time, debounce_time=debounce_time,
            unit=unit, alias=alias, descr=descr, lookup=lookup,
            change_delay=change_delay, timeout=timeout, 
            recovery_time=recovery_time, 
        )
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable,
            see signal_var.
            
            Attention:
                Please note that for RxFrBusSignals, this will show info on the 
                contents of the HIL-send-buffer (below BusSystems), not the 
                value from Model/Simulink source nor the last seen signal value 
                on FlexRay bus.
            
            Returns the current info string from signal_var.
        """
        return _bus_signals_frbs.RxFrBusSignal.info(self)
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable, see signal_var. 
            
            Attention:
                Please note that for RxFrBusSignals, this will get the current 
                value of the HIL-send-buffer (below BusSystems), not the value 
                from Model/Simulink source nor the last seen signal value on 
                FlexRay bus.
            
            Returns the current value from signal_var.
        """
        return _bus_signals_frbs.RxFrBusSignal.get(self)
        
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable below BusSystems
            (and switch the signal source to "BusSystems").
            
            Parameters:
                value - value to set
            
            Returns the previous value from signal_var.
        """
        _bus_signals_frbs.RxFrBusSignal.set(self, value=value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data. 
            This uses the lookup values supplied in constructor, see signal_var.
            Fallback (if no matching state was found) will be the unmapped 
            numeric value.
            
            Attention:
                Please note that for RxFrBusSignals, this will get the current 
                value of the HIL-send-buffer (below BusSystems), not the value 
                from Model/Simulink source nor the last seen signal value on 
                FlexRay bus.
            
            Returns the current state representation from signal_var.
        """
        return _bus_signals_frbs.RxFrBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable below BusSystems
            (and switches the signal source to "BusSystems"). This uses the 
            lookup values supplied in constructor.
            
            Parameters:
                state - named state to set
            
            Returns the previous state representation  from signal_var.
        """
        _bus_signals_frbs.RxFrBusSignal.setState(self, state=state)
    
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
        return _bus_signals_frbs.RxFrBusSignal.getStateDescr(self, value=value, fallback=fallback)
    
    # #########################################################################
    def enableHilTx(self):
        """ Enable transmission of signal HIL => DUT (if the assigned PDU 
            supports it).
            Note: This will enable transmission of all signals of the parent PDU.
        """
        _bus_signals_frbs.RxFrBusSignal.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable transmission of signal HIL => DUT (if the assigned PDU 
            supports it). 
            Note: This will disable transmission of all signals of the parent PDU.
        """
        _bus_signals_frbs.RxFrBusSignal.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger transmission ("kickout") of signal HIL => DUT (by 
            triggering the parent PDU). 
            Note: This means all other signals of the parent PDU will be sent
                  as well
        """
        _bus_signals_frbs.RxFrBusSignal.kickout(self)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. Note that this
            will also switch the variable source switch back from BusSystems
            to (default) Simulink/Model.
        """
        _bus_signals_frbs.RxFrBusSignal.reset(self, *args, **kwargs)
        

# #############################################################################
class CrcFrBusStatus(_bus_signals_frbs.CrcFrBusStatus):
    """ CRC Tx-Signal status (ECU Tx => HIL Rx) and associated switch variables 
        for dSPACE FlexRay blockset with PDU-based modeling.
        
        Note:
            This is essentially a basic "HilVar" containing the CRC status 
            plus additional sub-variables.
    """
    
    ## Configuration settings for new instances: 
    # Custom "hard" default value(s) to use for internal real time system 
    # variables (for example: switch settings)  
    #
    # Mapping: <variable name as string>: <default value>
    #
    # See description at FrRxPdu for additional details.
    #
    # Typical default values:
    # - source switches usually default to "source: simulink model"
    #    * 0: source: simulink model / trc 
    #    * 1: source: bus system
    # - CRC calculation/check enable variable: "disabled" is a safe default
    #   (enable in test as needed) as enabled checks w/ faulty CRCs will 
    #   freeze remaining signal data at the "last known good" value.
    #    * 0: calculation/check disabled
    #    * 1: calculation/check enabled
    #
    cfg_custom_defaults = {
        "switch_var":   None,
        "enable_var":   None,
    }
    
    # #########################################################################
    def __init__(self, context, crc_data_path, alias="", descr=""):
        """ Constructor for HIL-Rx CRC-check status variables.
            
            Info: CRC check status values:
                * 0: CRC valid
                * 1: CRC invalid
                * 2: CRC check is disabled
            
            Example: BusSystems Path Structure
                # CRC signal variable:
                BusSystems/FlexRay/Monitoring/ECU_NAME/Channel A/PDU_NAME/Signals/CRC_PDU_NAME_IN/Value
                # CRC status variable:
                BusSystems/FlexRay/Monitoring/ECU_NAME/Channel A/PDU_NAME/CRC Data/Status
            
            Parameters:
                context       - parent context (an RTE application instance to 
                                resolve signal/variable paths)
                crc_data_path - model path to /CRC Data/Status variable
                alias         - (opt) CRC signal alias/name
                descr         - (opt) CRC signal description
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion  may 
        #       find them even if the base class code cannot be analyzed.
        
        ## Source Switch variable for CRC check enable 
        # * 0: Simulink Model 
        # * 1: BusSystems
        self.switch_var = None
        
        ## CRC calculation/check enable variable ("CRC Enable")
        # * 0: calculation/check disabled
        # * 1: calculation/check enabled
        self.enable_var = None
        
        ## Status variable for CRC check (read-only)
        # * 0: CRC value is valid
        # * 1: CRC value is invalid
        # * 2: CRC check is disabled
        self.status_var = None
        _bus_signals_frbs.CrcFrBusStatus.__init__(
            self, context=context, 
            crc_data_path=crc_data_path, 
            alias=alias, descr=descr
        )
    
    # #########################################################################
    def enableCrcCalc(self):
        """ Enable CRC calculation/evaluation regardless of current setting in 
            simulink model.
            Use reset() to clear this override again.
        """
        _bus_signals_frbs.CrcFrBusStatus.enableCrcCalc(self)
    
    # #########################################################################
    def get(self):
        """ Get the current CRC status value from FlexRay blockset.
            
            Info: CRC check status values are:
               * 0: crc valid
               * 1: crc invalid
               * 2: check disabled
            
            Returns the current value from status var.
        """
        return _bus_signals_frbs.CrcFrBusStatus.get(self)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the current CRC status value from FlexRay 
            blockset.
            Returns the current state representation.
        """
        return _bus_signals_frbs.CrcFrBusStatus.getState(self)
    
    # #########################################################################
    def reset(self):
        """ Reset CRC check/calculation settings (default: switch back to 
            current setting in Simulink model).
        """
        _bus_signals_frbs.CrcFrBusStatus.reset(self)
        

# #############################################################################
class CrcFrBusSignal(_bus_signals_frbs.CrcFrBusSignal):
    """ A CRC RX bus signal derived from RxFrBusSignal (HIL-Tx => ECU-Rx) for 
        use with dSPACE FlexRay blockset with PDU-based structure. 
        See RxFrBusSignal for inherited methods.
    """
    
    ## Configuration setting for new instances: 
    # CRC type for "correct" CRC algorithm (normal mode).
    cfg_crc_normal_type = 1
    
    ## Configuration setting for new instances: 
    # CRC type for "incorrect" CRC algorithm (for error injection).
    cfg_crc_error_type  = 2
    
    ## Configuration settings for new instances:  
    # Custom "hard" default value(s) to use for internal real time system 
    # variables. See RxFrBusSignal for further details. 
    #
    # Mapping: <variable name as string>: <default value>
    #
    # Typical default values:
    # - source switches usually default to "source: simulink model"
    #    * 0: source: Simulink Model / TRC 
    #    * 1: source: BusSystems
    # - CRC enable (automatic CRC calculation) usually defaults to "enabled"
    #    * 0: CRC calculation disabled
    #    * 1: CRC calculation enabled
    # - CRC type (active CRC algorithm) should default to "correct CRC" 
    #   (which is typically algorithm 1)
    #
    cfg_custom_defaults = {
        "crc_type_var":     None,
        "crc_enable_var":   None,
        "crc_switch_var":   None, # default for crc enable/type switch
        "switch_var":       None, # default for static "value" switch (from base RxFrBusSignal)
    }
    
    
    # #########################################################################
    def __init__(self, context, base_model_path, 
                 pdu=None, cycle_time=None, debounce_time=None,
                 alias="", descr="",
                 error_delay=None, change_delay=None,  timeout=None, 
                 recovery_time=None):
        """ CRC bus signal initialization for dSPACE FlexRay blockset.
            See RxFrBusSignal.
            
            Note: CRC Types / Switch Codes:
                CRC Types for normal mode (correct CRC calculation) and 
                error mode (incorrect CRC calculation, e.g. calculated CRC + 1)
                are defined in members crc_normal_type and crc_error_type.
                
                Note that simply switching the CRC calculation off (e.g. CRC = 0x00)
                may lead to detection failures, as a static CRC value might 
                actually be correct for the current data.
                
                If you need different switch codes in your project, consider 
                setting CrcFrBusSignal.cfg_crc_normal_type and/or
                CrcFrBusSignal.cfg_crc_error_type before instantiating signals
                or sub-classing CrcFrBusSignal and overriding the crc types.
            
            Example: BusSystems CRC Signal Path Structure
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/CRC_PDU_NAME_OUT/Value
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/CRC_PDU_NAME_OUT/Dynamic Value
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/CRC_PDU_NAME_OUT/Countdown Value
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/CRC_PDU_NAME_OUT/Source Switch
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/CRC Data/CRC Enable
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/CRC Data/Type
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/CRC Data/Source Switch
                
                # base_model_path == "Value" path:
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/CRC_PDU_NAME_OUT/Value
            
            Parameters:
                context         - rtplib application instance
                base_model_path - base model path from which all required paths
                                  will be derived (use /Value of actual crc signal)
                pdu             - reference to associated FrRxPdu instance
                cycle_time      - (opt) cycle time in [ms], overrides settings in PDU
                debounce_time   - (opt) minimum debounce delay time in [ms], 
                                        overrides settings in PDU
                alias           - (opt) bus signal alias/name
                descr           - (opt) signal description
                error_delay     - (opt) delay to wait until a simple CRC error 
                                        should be detected [ms],
                                        defaults to 10x max(cycle_time, debounce_time)
                change_delay    - (opt) delay to wait after a value change [ms],  
                                        defaults to 2x max(cycle_time, debounce_time)
                timeout         - (opt) detection time for timeout errors [ms],  
                                        defaults to 2x max(cycle_time, debounce_time)
                recovery_time   - (opt) time for recovery/"wiedergut" checks [ms],  
                                        defaults to 2x max(cycle_time, debounce_time)
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class code cannot be analyzed.
        
        ## Source Switch variable for CRC Type/Enable (settings below /CRC Data/)
        #  (a "HilVar" instance)
        # * 0: Simulink Model
        # * 1: BusSystems
        self.crc_switch_var = None
        
        ## CRC Type variable, selects active CRC algorithm 
        # (a "HilVar" instance)
        self.crc_type_var   = None
        
        ## CRC Enable variable, enables/disables automatic CRC calculation 
        # (a "HilVar" instance)
        # * 0: CRC calculation disabled
        # * 1: CRC calculation enabled
        self.crc_enable_var = None
        
        ## CRC type for "correct" CRC algorithm (normal mode).
        # Initial value gets copied from class attribute, 
        # see CrcFrBusSignal.cfg_crc_normal_type
        self.crc_normal_type = self.cfg_crc_normal_type
        
        ## CRC type for "incorrect" CRC algorithm (for error injection).
        # Initial value gets copied from class attribute, 
        # see CrcFrBusSignal.cfg_crc_error_type
        self.crc_error_type  = self.cfg_crc_error_type
        
        ## delay [ms] to wait until a basic CRC error (like "CRC invalid")
        #  should be detected. This will be used in test functions.
        self.error_delay = None
        
        # Members inherited from RxFrBusSignal (see Note above) ##############
        
        ## Source Switch variable for static value (if automatic CRC calculation is disabled)
        #  (a "HilVar" instance)
        # * 0: Simulink Model 
        # * 1: BusSystems
        self.switch_var = None
        
        
        # Members inherited from FrBusSignal (see Note above) #################
        
        ## model path of value variable
        self.value_path = None
        ## base model path (base path for deriving sub-element paths)
        self.base_path = None
        ## reference to parent FrRxPdu
        self.pdu = None
        
        # Members inherited from BusSignal (see Note above) ###################
        
        ## context (reference to assigned RTE application instance)
        self.context = None
        ## main bus signal variable on HIL-side, (a "HilVar" instance)
        self.signal_var = None
        ## signal alias name (from signal_var)
        self.alias = None
        ## signal unit (from signal_var)
        self.unit  = None
        ## signal description text
        self.descr  = None
        
        
        # timings #############################################################
        ## cycle time of signal in [ms] (that is, of the associated message or PDU)
        self.cycle_time = None
        ## minimum debounce delay for event-triggered signals in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None
        
        # #####################################################################
        _bus_signals_frbs.CrcFrBusSignal.__init__(
            self, context=context, 
            base_model_path=base_model_path, 
            pdu=pdu, cycle_time=cycle_time, debounce_time=debounce_time, 
            alias=alias, descr=descr, 
            error_delay=error_delay, 
            change_delay=change_delay, 
            timeout=timeout, 
            recovery_time=recovery_time
        )
    
    # #########################################################################
    def setBasicCrcError(self):
        """ Switch CRC calculation to an algorithm producing incorrect CRCs.
            See CrcFrBusSignal.crc_error_type.
            
            Note: 
                If you want to use a different `crc_error_type` for a few test
                cases and re-use test functions that call this method for 
                simple error injection, you could reconfigure the active
                `crc_error_type` on-the-fly.
            
            Example: Temporarily reconfiguring crc_error_type
                # use error type 4711 for a single test
                orig_error_type = crc_signal.crc_error_type
                crc_signal.crc_error_type = 4711
                testBasicCrcError(crc_signal, ...)
                crc_signal.crc_error_type = orig_error_type
         
         """
        _bus_signals_frbs.CrcFrBusSignal.setBasicCrcError(self)
    
    # #########################################################################
    def clearBasicCrcError(self):
        """ Switch CRC calculation to an algorithm producing correct CRCs
            (which should be the default case).
            See CrcFrBusSignal.crc_normal_type.
            Note: 
                Use reset() to switch back to CRC Type from Simulink/Model.
        """
        _bus_signals_frbs.CrcFrBusSignal.clearBasicCrcError(self)
        
    
    # #########################################################################
    # Methods inherited from  RxFrBusSignal
    # #########################################################################
    
    # #########################################################################
    def enableHilTx(self):
        """ (Re-)enable sending of PDU, depending on selected disable_mode 
            (see constructor). This overrides current settings from Simulink 
            Model, use reset() to restore initial behavior.
            
            Note: This enables transmission of all signals of the parent PDU.
        """
        return _bus_signals_frbs.CrcFrBusSignal.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable sending of PDU, depending on selected disable_mode 
            (see constructor). This overrides current settings from Simulink 
            Model, use reset() to restore initial behavior.
            
            Note: This disables transmission of all signals of the parent PDU.
        """
        return _bus_signals_frbs.CrcFrBusSignal.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger transmission ("kickout") of signal HIL => DUT 
            (by triggering the parent PDU). 
            
            Note: This means all other signals of the parent PDU will be sent as well.
        """
        return _bus_signals_frbs.CrcFrBusSignal.kickout(self)
        
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/RxBusSignal
    # #########################################################################
    
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable
            (typically not that useful for ECU-Rx/HIL-Tx CRC-signals, though).
            Returns the current value from signal_var.
         """
        return _bus_signals_frbs.CrcFrBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL signal variable.
            Parameters:
                value - value to set
            Returns the previous value from signal_var
        """
        return _bus_signals_frbs.CrcFrBusSignal.set(self, value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data 
            (typically not that useful for ECU-Rx/HIL-Tx CRC-signals, though).
            Returns the current state representation from signal_var.
        """
        return _bus_signals_frbs.CrcFrBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor
            Parameters:
                state - named state to set
            Returns the previous state representation from signal_var.
        """
        return _bus_signals_frbs.CrcFrBusSignal.setState(self, state)
    
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
        return _bus_signals_frbs.CrcFrBusSignal.getStateDescr(self, value=value, fallback=fallback)
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable.
            Returns an info string.
        """
        return _bus_signals_frbs.CrcFrBusSignal.info(self)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. 
            Note: 
                This will also switch the Source Switch back to its default 
                state (which is usually `2: running counter from BusSystems`).
        """
        _bus_signals_frbs.CrcFrBusSignal.reset(self, *args, **kwargs)
        

# #############################################################################
class AcFrBusSignal(_bus_signals_frbs.AcFrBusSignal):
    """ An alive counter RX bus signal derived from RxFrBusSignal (HIL => ECU) 
        for use with dSPACE FlexRay blockset PDU-based data structures.
        See RxFrBusSignal for inherited methods.
    """
    
    ## Configuration settings for new instances: 
    # Custom "hard" default value(s) to use for internal real time system 
    # variables. See RxFrBusSignal for further details.
    #
    # Mapping: <variable name as string>: <default value>
    #
    # Typical default values:
    # - source switches for alive counters usually default to "running counter"
    #   *  0: static value from Simulink Model 
    #   *  1: static value from BusSystems
    #   *  2: running counter from BusSystems (usually the default)
    #   * 12: counter is stopped for time span specified by Countdown Value, 
    #         last value of alive counter is sent. When Countdown Value 
    #         reaches 0, Source Switch is switched back to last Switch value.
    # - Counter Runtime Behavior, usually defaults to "running"
    #   *  0: counter runs independently of the selected source 
    #   *  1: counter running
    #   *  2: counter stopped (at current value)
    # - Counter Offset, additive offset defaults to 0 
    # - Countdown Value (countdown timer for dynamic manipulation), 
    #   default should be 0 but value auto decrements down to 0 anyway.
    #
    cfg_custom_defaults = {
        "ac_runtime_behavior_var":  None, 
        "ac_offset_var":            None,
        "ac_countdown_value_var":   None,  
        "switch_var":               None, # default for "value" source switch (see note above)
    }
    
    # #########################################################################
    def __init__(self, context, base_model_path, 
                 pdu=None, cycle_time=None, debounce_time=None, 
                 alias="", descr="",
                 error_delay=None, change_delay=None, timeout=None, 
                 recovery_time=None):
        """ Alive counter bus signal initialization for dSPACE FlexRay blockset.
            
            Example: Alive Counter Signal Path Structure:
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/ALIV_PDU_NAME_OUT/Value
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/ALIV_PDU_NAME_OUT/Dynamic Value
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/ALIV_PDU_NAME_OUT/Validity
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/ALIV_PDU_NAME_OUT/Dynamic Validity
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/ALIV_PDU_NAME_OUT/Countdown Value
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/ALIV_PDU_NAME_OUT/Source Switch
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/ALIV_PDU_NAME_OUT/AliveCounter/Value   # Note: read-only
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/ALIV_PDU_NAME_OUT/AliveCounter/Runtime Behavior
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/ALIV_PDU_NAME_OUT/AliveCounter/Offset
                
                # base_model_path == "Value" path:
                BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_NAME/Signals/ALIV_PDU_NAME_OUT/Value
            
            Parameters:
                context         - rtplib application instance
                base_model_path - base model path from which all required paths
                                  will be derived, use /Value of counter signal.
                pdu             - reference to associated FrPdu instance
                cycle_time      - (opt) cycle time in [ms], overrides settings in PDU
                debounce_time   - (opt) minimum debounce delay time in [ms], 
                                        overrides settings in PDU
                alias           - (opt) bus signal alias/name
                descr           - (opt) signal description
                error_delay     - (opt) delay to wait until a simple alive counter
                                        error should be detected [ms],
                                        defaults to 10x max(cycle_time, debounce_time)
                change_delay    - (opt) delay to wait after a value change [ms],  
                                        defaults to 2x max(cycle_time, debounce_time)
                timeout         - (opt) detection time for timeout errors [ms],  
                                        defaults to 2x max(cycle_time, debounce_time)
                recovery_time   - (opt) time for recovery/"wiedergut" checks [ms],  
                                        defaults to 2x max(cycle_time, debounce_time)
        """
        # Note: base class members added explicitly here (they will be updated 
        #       in base class' constructor) so automatic code completion may 
        #       find them even if the base class' code cannot be analyzed.
        
        ## delay [ms] to wait until a basic Alive Counter error (like "AC stopped")
        #  should be detected. This will be used in test functions.
        self.error_delay = None
        
        ## Counter Runtime Behavior variable (a "HilVar" instance).
        # * 0: "The alive counter runs independently of the selected source 
        #       for the signal (Source Switch variable)"
        # * 1: counter running  
        #      "The alive counter runs only if its value is really sent 
        #       (Switch is 2 or 12). If it is switched to another source than 
        #       the alive counter, for example, a value from the Simulink 
        #       model, the alive counter stops."
        # * 2: counter stopped (at current value)  
        #      "The alive counter stops at the current value."
        self.ac_runtime_behavior_var = None 
        
        ## Counter Offset variable: offset to current counter value (a "HilVar" instance).
        # > "Allows you to add an offset to the value of the alive counter 
        # >  at run time."
        self.ac_offset_var           = None
        
        ## Countdown Value: countdown timer for dynamic manipulation (a "HilVar" instance).
        # > "Time span for dynamic signal manipulation. 
        # >  It specifies how often the dynamic values are sent."
        self.ac_countdown_value_var  = None 
        
        
        # Members inherited from RxFrBusSignal (see Note above) ##############
        
        ## Source Switch variable for static counter value (a "HilVar" instance).
        # *  0: static value from Simulink Model 
        # *  1: static value from BusSystems
        # *  2: running counter from BusSystems
        # * 12: counter is stopped for time span specified by Countdown Value, 
        #       last value of alive counter is sent. When Countdown Value 
        #       reaches 0, Source Switch is switched back to the last Switch value.
        #
        # See dSPACE: FlexRayConfigFeatures.pdf "Using an Alive Counter in the Simulation"
        self.switch_var = None
        
        
        # Members inherited from FrBusSignal (see Note above) #################
        
        ## model path of value variable
        self.value_path = None
        ## base model path (base path for deriving sub-element paths)
        self.base_path = None
        ## reference to parent FrRxPdu
        self.pdu = None
        
        # Members inherited from BusSignal (see Note above) ###################
        
        ## context (reference to assigned RTE application instance)
        self.context = None
        ## main Alive Counter bus signal value variable on HIL-side 
        # (a "HilVar" instance)
        self.signal_var = None
        ## Alive Counter signal alias name (from signal_var)
        self.alias = None
        ## signal unit (from signal_var; usually empty for Alive Counters)
        self.unit  = None
        ## Alive Counter signal description text
        self.descr  = None
        
        
        # timings #############################################################
        ## cycle time of signal in [ms] (that is, of the associated message or PDU)
        self.cycle_time = None
        ## minimum debounce delay for event-triggered signals in [ms]
        self.debounce_time = None
        ## delay to wait after a value change [ms] 
        self.change_delay = None
        ## detection time for timeout errors [ms]
        self.timeout = None
        ## time for recovery/"wiedergut" checks [ms]
        self.recovery_time = None 
        
        # #####################################################################
        _bus_signals_frbs.AcFrBusSignal.__init__(
            self, context=context, 
            base_model_path=base_model_path, 
            pdu=pdu, cycle_time=cycle_time, debounce_time=debounce_time, 
            alias=alias, descr=descr, 
            error_delay=error_delay, 
            change_delay=change_delay, 
            timeout=timeout, 
            recovery_time=recovery_time
        )
    
    # #########################################################################
    def setBasicAcError(self):
        """ Stop and hold Alive Counter at the current count. """
        _bus_signals_frbs.AcFrBusSignal.setBasicAcError(self)
    
    # #########################################################################
    def clearBasicAcError(self):
        """ (Re-)enable normal Alive Counter behaviour (continue counting)."""
        _bus_signals_frbs.AcFrBusSignal.clearBasicAcError(self)
        
    
    # #########################################################################
    # Methods inherited from  RxFrBusSignal
    # #########################################################################
    def enableHilTx(self):
        """ (Re-)enable sending of PDU, depending on selected disable_mode 
            (see constructor). This overrides current settings from Simulink 
            Model, use reset() to restore initial behavior.
            
            Note: This enables transmission of all signals of the parent PDU.
        """
        return _bus_signals_frbs.AcFrBusSignal.enableHilTx(self)
    
    # #########################################################################
    def disableHilTx(self):
        """ Disable sending of PDU, depending on selected disable_mode 
            (see constructor). This overrides current settings from Simulink 
            Model, use reset() to restore initial behavior.
            
            Note: This disables transmission of all signals of the parent PDU.
        """
        return _bus_signals_frbs.AcFrBusSignal.disableHilTx(self)
    
    # #########################################################################
    def kickout(self):
        """ Trigger transmission ("kickout") of signal HIL => DUT (by 
            triggering the parent PDU). 
            
            Note: This means all other signals of the parent PDU will be sent as well.
        """
        return _bus_signals_frbs.AcFrBusSignal.kickout(self)
    
    # #########################################################################
    # Basic methods inherited from  BusSignal/RxBusSignal
    # #########################################################################
    def get(self):
        """ Get the current value of the HIL signal variable
            (typically not that useful for ECU-Rx/HIL-Tx AC-signals, though).
         """
        return _bus_signals_frbs.AcFrBusSignal.get(self)
    
    # #########################################################################
    def set(self, value):
        """ Set a value to the HIL Alive Counter signal variable below BusSystems
            (and switch the signal source to "BusSystems", static value).
            If a value is set to an Alive Counter signal, the Alive Counter
            value will stay at this static value until reset() gets called.
            See possible AcFrBusSignal.switch_var values for Alive Counter signals.
            
            Parameters:
                value - static value to set
            
            Returns the previous value from signal_var.
        """
        _bus_signals_frbs.AcFrBusSignal.set(self, value=value)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the HIL signal variable's current data 
            (typically not that useful for ECU-Rx/HIL-Tx AC-signals, though).
            Returns the current state's description from signal_var.
        """
        return _bus_signals_frbs.AcFrBusSignal.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the HIL signal variable. This uses the 
            lookup values supplied in constructor.
            Parameters:
                state - named state to set
            Returns the previous state's description.
        """
        return _bus_signals_frbs.AcFrBusSignal.setState(self, state)
    
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
        return _bus_signals_frbs.AcFrBusSignal.getStateDescr(self, value=value, fallback=fallback)
    
    # #########################################################################
    def info(self):
        """ Get a current info string about the HIL signal variable. 
            
            Returns a formatted info string.
        """
        return _bus_signals_frbs.AcFrBusSignal.info(self)
    
    # #########################################################################
    # Inherited from ResettableContainer
    # #########################################################################
    def reset(self, *args, **kwargs):
        """ Reset all resettable variables of this bus signal. 
            Note: 
                This will also switch the Source Switch back to its default 
                state (which is usually `2: running counter from BusSystems`).
        """
        _bus_signals_frbs.AcFrBusSignal.reset(self, *args, **kwargs)
        

# #############################################################################
# Signal Container
# #############################################################################
class FrBusSignalContainer(_bus_signals_frbs.FrBusSignalContainer):
    """ A BusSignalContainer for FlexRay Bus Signals """
    
    # #########################################################################
    def __init__(self, context):
        """ Override to add signals.
            
            Parameters:
                context - context used for contained BusSignals
        """
        _bus_signals_frbs.FrBusSignalContainer.__init__(self, context)
    
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
        _bus_signals_frbs.FrBusSignalContainer.resetAll(
            self, 
            verbosity=verbosity, 
            recursion_depth=recursion_depth
        )
    
    # #########################################################################
    def iterSignals(self, pdu):
        """ Iterate over all signals that reference the specified PDU.
            
            Parameters:
                pdu - a PDU instance
            
            Usage:
                for sig in bus.iterSignals(bus.tx_pdu_FNORD):
                    print sig
            
            Returns an iterator object.
        """
        return _bus_signals_frbs.FrBusSignalContainer.iterSignals(self, pdu=pdu)
        

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    import time
    # just for output formatting:
    from _bus_signals_frbs import FrPdu, FrBusSignal
    import ttk_tools.dspace.rtplib_offline_stub as rtplib
    appl = rtplib.Appl("foo.sdf", "bar1005", "Offline")
    
#     import ttk_tools.dspace.xil_api_offline_stub as xil_api
#     appl = xil_api.XilTestbench("fnord.xml", product_version="1895-B")
    
    print
    print "== RxFrBusSignal =================================================="
    sig = RxFrBusSignal(appl, "BusSystems/FlexRay/Sending/QUX/Channel A/BAZ_PDU/Signals/FOOBAR_OUT/Value", cycle_time=10)
    print "# original value:"
    print sig.info()
    print "# changed value:"
    sig.set(123)
    print sig.info()
    print "# value after signal.reset():"
    sig.reset()
    print sig.info()
    
    
    # #########################################################################
    class BusSignals(FrBusSignalContainer):
        def __init__(self, appl):
            self.rx_pdu = FrRxPdu(
                appl, cycle_time=100, debounce_time=0, 
                bus_systems_path="BusSystems/FlexRay/Sending/ECU_NAME/Channel A/A_PDU",
                alias="A_PDU"
            )
            self.tx_pdu = FrTxPdu(
                appl, cycle_time=20, debounce_time=0, 
                bus_systems_path="BusSystems/FlexRay/Monitoring/DUT_NAME/Channel A/ANOTHER_PDU",
                alias="Another_PDU",
            )
            self.FooBarSig  = RxFrBusSignal(appl, "BusSystems/FlexRay/Sending/ECU_NAME/Channel A/A_PDU/Signals/SOME_SIGNAL_OUT/Value", self.rx_pdu)
            self.BazQuuxSig = TxFrBusSignal(appl, "BusSystems/FlexRay/Monitoring/DUT_NAME/Channel A/ANOTHER_PDU/Signals/QUX_IN/Value", self.tx_pdu)
            self.AnotherSig = RxFrBusSignal(appl, "BusSystems/FlexRay/Sending/ECU_NAME/Channel A/A_PDU/Signals/ANOTHER_SIGNAL_OUT/Value", 
                alias="Another Bus Signal", descr="Another Signal to test", unit="rpm", 
                pdu=self.rx_pdu, 
                change_delay=250, timeout=500, recovery_time=500,
            )
            
            self.crc_sig = CrcFrBusSignal(
                appl, "BusSystems/FlexRay/Sending/ECU_NAME/Channel A/A_PDU/Signals/SomeCrcSignal/Physical Value",
                pdu=self.rx_pdu, alias="SomeCrcSignal"
            )
            self.ac_sig = AcFrBusSignal(
                appl, "BusSystems/FlexRay/Sending/ECU_NAME/Channel A/A_PDU/Signals/SomeAcSignal/Physical Value",
                pdu=self.rx_pdu, alias="SomeAcSignal"
            )
            self.crc_status = CrcFrBusStatus(
                appl, "BusSystems/FlexRay/Monitoring/ECU_NAME/Channel A/ANOTHER_PDU/Signals/CRC Data/Status",
            )
            
            # #################################################################
            self.rx_pdu_auto = FrRxPdu(appl, 
                cycle_time=100, debounce_time=0, disable_mode=None, descr="automatic/default disable mode",
                bus_systems_path="BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_auto", 
            )
            self.rx_pdu_en = FrRxPdu(appl, 
                cycle_time=100, debounce_time=0, disable_mode="en", descr="tx-disable via tx/sw/hw enable",
                bus_systems_path="BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_EN", 
            )
            self.rx_pdu_ub = FrRxPdu(appl, 
                cycle_time=100, debounce_time=0, disable_mode="ub", descr="tx-disable via update bit modification",
                bus_systems_path="BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_UB", 
            )
            self.rx_pdu_tm = FrRxPdu(appl, 
                cycle_time=100, debounce_time=0, disable_mode="tm", descr="tx-disable via user defined transmission mode",
                bus_systems_path="BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_EM", 
            )
            self.rx_pdu_man = FrRxPdu(appl, 
                cycle_time=100, debounce_time=0, descr="tx-disable via manually defined enable var (this overrides disable mode)",
                enable_path="Model Root/some/path/PDU Enable Switch/Value",
                bus_systems_path="BusSystems/FlexRay/Sending/ECU_NAME/Channel A/PDU_EM", 
            )
            
    
    print
    print "== FrBusSignalContainer with signals =============================="
    bus_signals = BusSignals(appl)
    
    print "# initial values:"
    print bus_signals.FooBarSig.info()
    print bus_signals.BazQuuxSig.info()
    print bus_signals.AnotherSig.info()
    bus_signals.FooBarSig.set(1234)
    bus_signals.AnotherSig.set(1000)
    time.sleep(bus_signals.AnotherSig.cycle_time / 1000.0)
    
    print "# changed values:"
    print bus_signals.FooBarSig.info()
    print bus_signals.BazQuuxSig.info()
    print bus_signals.AnotherSig.info()
    
    print "# resetting container:"
    bus_signals.resetAll(verbosity=2)
    
    print "# after reset:"
    print bus_signals.FooBarSig.info()
    print bus_signals.BazQuuxSig.info()
    print bus_signals.AnotherSig.info()
    
    print 
    print "# iterSignals:"
    print 'Signals in rx_pdu ("%s"):'%(bus_signals.rx_pdu.alias)
    for sig in bus_signals.iterSignals(bus_signals.rx_pdu):
        print " ->", sig
    print 'Signals in tx_pdu ("%s"):'%(bus_signals.tx_pdu.alias)
    for sig in bus_signals.iterSignals(bus_signals.tx_pdu):
        print " ->", sig
    
    print
    print "== Mini-Member-Check =============================================="
    print
    
    # #########################################################################
    # mini-check: Signal methods, PDU disable modes and kickout/trigger 
    # #########################################################################
    for name, var in sorted(vars(bus_signals).iteritems(), key=lambda x: x[1].__class__):
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        if isinstance(var, FrBusSignal):
            print
            print "# Signal: %s (%s)"%(name, var.__class__.__name__)
            print "  get()   ->", var.get()
            print "  set(42) ->", var.set(42)
            print "  info()  ->", var.info()
            
            if isinstance(var, TxFrBusSignal):
                print "  status_var:", var.status_var.info()
            
            elif isinstance(var, RxFrBusSignal):
                
                print "  disableHilTx..."
                var.disableHilTx()
                print "  enableHilTx..."
                var.enableHilTx()
                print "  trigger/kickout()..."
                var.kickout()
                
                if isinstance(var, CrcFrBusSignal):
                    print "  setBasicCrcError()..."
                    var.setBasicCrcError()
                    print "  clearBasicCrcError()..."
                    var.clearBasicCrcError()
                
                elif isinstance(var, AcFrBusSignal):
                    print "  setBasicAcError()..."
                    var.setBasicAcError()
                    print "  clearBasicAcError()..."
                    var.clearBasicAcError()
            
            print "  reset()..."
            var.reset()
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        elif isinstance(var, CrcFrBusStatus):
            print
            print "# CRC status: %s (%s)"%(name, var.__class__.__name__)
            print "  get()  ->", var.get()
            print "  info() ->", var.info()
            print "  enableCrcCalc()..."  
            var.enableCrcCalc()
            print "  reset()..."
            var.reset()
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        elif isinstance(var, FrPdu): 
            print
            print "# PDU: %s (%s)"%(name, var.__class__.__name__)
            if isinstance(var, FrRxPdu): 
                print "# %s (disable mode '%s')"%(var.descr or "<no descr>", var._disable_mode)
                print "  disableHilTx..."
                var.disableHilTx()
                print "  enableHilTx..."
                var.enableHilTx()
                print "  trigger/kickout()..."
                var.kickout()
                print "-- initialized internal model variables --"
                for n in ("tx_enable_var",         "tx_enable_switch",
                          "update_bit_enable_var", "update_bit_switch",
                          "tm_var", "tm_switch",
                          "manual_enable_var",
                          "kickout_var", "kickout_switch"):
                    v = getattr(var, n, None)
                    if v is None: 
                        continue
                    print "  %-24s => %s"%(n, v.info())
                    
            
            elif isinstance(var, FrTxPdu):
                print "  error_status_var:        ", var.error_status_var.info()
                print "  data_receive_counter_var:", var.data_receive_counter_var.info()
            
            else:
                print "> FrPdu: %s"%(name)
        
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        else:
            print "[skipped] %s (%s)"%(name, var.__class__)
            
    
    print "\nDone."
# @endcond DOXYGEN_IGNORE
# #############################################################################
