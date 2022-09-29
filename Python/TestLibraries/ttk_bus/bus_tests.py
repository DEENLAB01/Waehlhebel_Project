#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : bus_tests.py
# Package : ttk_bus
# Task    : Wrapper for basic interface test functions (bus signal <-> ECU) 
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
# Rev. | Date       | Author   | Description
#------------------------------------------------------------------------------
# 1.0  | 14.09.2012 | Tremmel  | initial wrapper
# 1.1  | 05.10.2012 | Tremmel  | added wrapper for testSignals()
# 1.2  | 03.05.2013 | Tremmel  | added testBasicCrcError and testBasicAcError
# 1.3  | 01.10.2013 | Tremmel  | added manual trigger option to testBasic*Error
# 1.4  | 29.01.2014 | Tremmel  | added optional adaptive re-tests to testRxSignal/testTxSignal
# 1.5  | 18.03.2016 | Tremmel  | tweaked sample/test code in __main__
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2.0  | 15.07.2020 | Tremmel  | test functions now use ttk_checks.adv_tests.
#                              | testSignals now just calls testVar, but no 
#                              | longer supports a custom format string
#******************************************************************************
""" 
@package ttk_bus.bus_tests
Interface wrapper for bus/interface test functions (HIL <--bus-signal--> DUT) 
in ttk_bus._bus_tests.
This serves as "interface" to the precompiled module in delivery to enable 
code-completion in PyDev.  
Requires package ttk_checks.

Example:
    testresult.append(
        testRxSignal(
            bus.rx_sig,
            set_value = 100, 
            set_value_descr = "Some test value", 
            check_var_list = [
                {"var": cal.some_var,       "value": 0,   "abs_pos": 0.01, "abs_neg": -0.1 },
                {"var": cal.some_other_var, "value": 2.1, "rel_pos": 0.05 },  
                {"var": cal.status_var,     "value": 3 },  
            
            ],
            descr = "This is the supplied testRxSignal description text"
        )  
    )
    testresult.append(
        testTxSignal([{'var': cal.status, 'value': 1}], bus.tx_status_sig, 1 )
    )  

Conventions:
    * Signal directions are specified as relative to the DUT:
       - Tx - transmitted from ECU => received by HIL
       - Rx - received by ECU <= transmitted from HIL
    
    * Each function will take the required parameters for the test to perform 
      plus two additional parameters for report formatting:  
       - `descr`  - a description string that will be placed at the start of the 
                    result description text  
       - `format` - a format-string that specifies/overrides the formatting of the 
                    automatically generated part of the description.  
                    * Do __not__ override this unless absolutely necessary. 
                    * If you want to change the default output formatting of a 
                      test function, you should look into changing the current 
                      localization (see ttk_bus.bus_tests_loc), so all tests will 
                      use consistent result formatting.
                    * See also http://docs.python.org/library/stdtypes.html#string-formatting
    
    * If an input value has a get()-method, it will be called to get the 
      current value. Otherwise the value will be used as-is.
      - This permits simple read access to CalVar or HilVar instances.  
      - See ttk_base.variables_base
    
    * If an input value has associated meta data (like Hil/Cal Vars or basic 
      values wrapped as MetaValues), it can show up in the automatically
      generated description (e.g. unit or alias names).  
      - See ttk_base.variables_base, ttk_base.values_base.meta()
    
    * Exceptions occurring "inside" a test function have to be caught; the 
      function will return a result entry containing the error text and
      verdict ERROR.
      - That means it should not be necessary to wrap the test function into yet
        another `try ... except` block.
      - If a test function raises an (unexpected) exception anyway, please file 
        a bug report: http://trac.isyst.de/iTestStudio/newticket
        or contact support at support.iteststudio@isyst.de
"""
import _bus_tests


# #############################################################################
def testRxSignal(bus_signal_data, set_value, set_value_descr='', 
                 check_var_list=None,  max_retests=0,
                 descr='', format=None): # @ReservedAssignment: format
    """ Check the behaviour of a single bus signal sent from HIL system and 
        received by the ECU. 
        
        Info: This function ...
            * sets the signal contained in bus_signal_data in the HIL 
              model/system 
            * triggers sending the signal if needed (for event-triggered PDUs)
            * waits for value change(s) to propagate to the ECU/DUT
            * checks the value(s) inside the ECU using the supplied cal
              variables.
        
        Parameters:
            bus_signal_data -  data structure which describes the signal on 
                               the bus system. See bus_signals_base.RxBusSignal
            set_value       -  value to set on the HIL side
            set_value_descr -  string which describes the value to set
            check_var_list  -  list of dictionaries with variable, rated value 
                               and tolerance
            max_retests     -  how many times an additional delay should be
                               applied before re-testing failed results  
                               (0: no re-tests will be performed)
            descr           -  user specific description shown at the start of 
                               the result text
            format          -  format string to control/override appearance of 
                               the automatically created result text. 
                               A format override should only rarely be used.
        
        Example: check_var_list structure
            check_var_list = [
                { "var":     <variable to check (CalVar, HilVar, ...)>,
                  "value":   <rated/expected value>,
                  "rel_pos": <relative positive tolerance (optional)>,
                  "abs_pos": <absolute positive tolerance (optional)>,
                  "rel_neg": <relative negative tolerance (optional)>,
                  "abs_neg": <absolute negative tolerance (optional)>,
                },
                ...
            ]
            Note that abs_tol/rel_tol can be used as alias for abs_pos/rel_pos
            See ttk_checks.basic_checks.checkTolerance for more info on 
            use of tolerance values.
        
        Info: "var" and "value" in check_var_list
            Both the variable to check and the expected "value" can actually
            be HilVar/CalVar instances, meta()-wrapped MetaValue instances or
            plain scalar numeric values.
            
            This means that it is possible to compare the values of two 
            ecu/cal variables  
            `   {"var": cal.some_variable, "value": cal.some_other_variable}  `  
            or between hil and ecu  
            `   {"var": cal.foobar, "value": hil.barbaz}                      `  
            or even (admittedly, not too useful)  
            `   {"var": 3, "value": 3.2, "abs_tol": .4}                       `  
            
            If you want to show units in the test report, you could wrap values
            in a MetaValue:  
            `    {"var": cal.shrdlu, "value": meta(3.2, "mV"), "abs_tol": .4} `  
            See ttk_base.values_base.meta
            
            If all tolerances of a check_var_list entry remain un-set 
            (i.e. None), the values will be treated as discrete integer states 
            for comparison. If a value does not appear to be an integer value,
            the test will fail with verdict ERROR (and the actual check using 
            the un-cast value(s) will most likely fail as well).  
            See ttk_checks.checkutils.getInteger
        
        Returns a single test result entry (with a single verdict for all 
        checked cal variables).
    """
    return _bus_tests.testRxSignal(
        bus_signal_data, set_value, set_value_descr, 
        check_var_list, 
        max_retests,
        descr=descr, format=format
    )
    

##############################################################################
def testTxSignal(set_var_list,
                 bus_signal_data, check_value, check_value_descr="",
                 rel_pos=None, abs_pos=None,
                 rel_neg=None, abs_neg=None,
                 max_retests=0,
                 descr='', format=None): # @ReservedAssignment: format
    """ Check the behaviour of a single bus signal sent from the ECU and 
        received by the HIL system. 
        
        Info: This function ...
            * sets the value(s) inside the ECU using the supplied cal variables 
            * waits for value change(s) to propagate to HIL
            * checks the signal of the HIL system using bus_signal_data.
        
        Parameters:
            set_var_list      -  list of dictionaries with variable and
                                 value (see example, below)
            bus_signal_data   -  data structure which describes the signal on 
                                 the bus system. See bus_signals_base.TxBusSignal
            check_value       -  rated/expected value that should be received on 
                                 the HIL side
            check_value_descr -  string which describes the expected value
            rel_pos           -  (optional) relative positive tolerance
            abs_pos           -  (optional) absolute positive tolerance
            rel_neg           -  (optional) relative negative tolerance
            abs_neg           -  (optional) absolute negative tolerance
            max_retests       -  how many times an additional delay should be
                                 applied before re-testing failed results
                                 (0: no re-tests will be performed) 
            descr             -  user specific description shown at the start 
                                 of the result text
            format            -  format string to control/override appearance 
                                 of the automatically created result text.  
                                 If a tuple of strings is supplied, it should 
                                 contain three entries:  
                                 (main_format>, <set_format>, <check_format>).  
                                 A format override should only rarely be used.
        
        Example: set_var_list structure
           set_var_list = [
               { "var":   <variable to set (i.e. a CalVar, HilVar, ...)>,
                 "value": <value to set>,
                 "descr": <value description, optional>,
               },
               ...
           ]
        
        Returns a single test result entry.
    """
    return _bus_tests.testTxSignal(
        set_var_list,
        bus_signal_data, check_value, check_value_descr,
        rel_pos, abs_pos, rel_neg, abs_neg, 
        max_retests,
        descr=descr, format=format
    )
    

# #############################################################################
def testSignals(set_var_list=None, check_var_list=None, min_wait_time_ms=0, descr=''):
    """ Check the values of multiple variables/signals as a result of setting
        multiple other variables/signals. Between setting and checking, a 
        configurable time will be waited to deal with propagation delay. This
        wait time defaults to the minimum practicable wait time of all involved 
        bus signals.
        
        Info: This function:
            * sets the value(s) to the variables in set_var_list
            * triggers sending of any event-based signals included in set_var_list
            * waits for value change(s) to propagate to the ECU/DUT
            * checks the value(s) for variables in check_var_list
        
        Note:
            While this function can perform the same tests as testRxSinal() and 
            testTxSignal(), its flexibility somewhat limits description formatting.
        
        Parameters:
            set_var_list     -  Variables to set: a list of dictionaries with 
                                variable and value 
            check_var_list   -  Variables to check: a list of dictionaries with 
                                variable, rated value and tolerance
            min_wait_time_ms -  minimum wait time before performing checks
            descr            -  user specific description shown at the start of 
                                the result text
        
        Example: Wait time before check (propagation delay)
            wait_time = max(
                min_wait_time_ms, 
                max(<change delay of signals to set>) +
                max(<change delay of signals to check>)
            )
            # Note: a bus signal's wait time defaults to 2x cycle time
        
        Example: set_var_list structure
           set_var_list = [
               { "var":   <variable to set (e.g. a CalVar, HilVar, RxBusSignal, ...)>,
                 "value": <value to set>,
                 "descr": <value description, optional>,
               },
               ...
           ]
           See ttk_base.variables_base, ttk_bus.bus_signals_base
        
        Example: check_var_list structure
            check_var_list = [
                { "var":     <variable to check (CalVar, HilVar, TxBusSignal, ...)>,
                  "value":   <rated/expected value>,
                  "rel_pos": <relative positive tolerance (optional)>,
                  "abs_pos": <absolute positive tolerance (optional)>,
                  "rel_neg": <relative negative tolerance (optional)>,
                  "abs_neg": <absolute negative tolerance (optional)>,
                },
                ...
            ]
            # Note that abs_tol/rel_tol can be used as alias for abs_pos/rel_pos
            # See ttk_base.variables_base, ttk_bus.bus_signals_base
            # See ttk_checks.basic_checks.checkTolerance for more info on 
            # use of tolerance values.
        
        Info: "var" and "value" in check- and set_var_list
            Both the variable to check and the expected "value" can actually
            be HilVar/CalVar or (Rx)BusSignal instances, meta()-wrapped 
            MetaValue instances or plain scalar numeric values.
            
            This means that it is possible to compare the values of two 
            ecu/cal variables  
            `    {"var": cal.some_variable, "value": cal.some_other_variable} `  
            or between hil and ecu  
            `    {"var": cal.foobar,     "value": hil.barbaz}                 `  
            `    {"var": bus.barsignal,  "value": cal.bazquux}                `  
            or even (admittedly, not too useful)  
            `    {"var": 3, "value": 3.2, "abs_tol": .4}                      `  
            
            If you want to show units in the test report, you could wrap values
            in a MetaValue:  
            `   {"var": cal.shrdlu, "value": meta(3.2, "mV"), "abs_tol": .4}  `  
            See ttk_base.values_base.meta
            
            If all tolerances of a check_var_list entry remain un-set 
            (i.e. None), the values will be treated as discrete integer states 
            for comparison. If a value does not appear to be an integer value,
            the test will fail with verdict ERROR (and the actual check using 
            the un-cast value(s) will most likely fail as well).  
            See ttk_checks.checkutils.getInteger
        
        Returns a single test result entry (with a single verdict for all 
        checked variables).
    """
    return _bus_tests.testSignals(
        set_var_list, check_var_list, min_wait_time_ms,
        descr=descr
    )
    

# #############################################################################
def testBasicCrcError(crc_signal_data, 
                      check_var_list_before=None, check_var_list_after=None,
                      manual_wait_cycles=None,
                      manual_triggers_before=0,
                      manual_triggers_between=0,
                      manual_trigger_delay_ms=0,
                      descr='', format=None): # @ReservedAssignment: format
    """ Check ECU behaviour on CRC signal errors (for messages sent from HIL 
        system and received by the ECU).
        
        Info: This function ...
            * checks the "before" variables, 
            * sets the crc signal to an error state, 
            * waits a defined number of message cycles, then 
            * checks the "after" variables.
        
        Parameters:
            crc_signal_data         - CrcBusSignal data structure which describes 
                                      the crc signal. See bus_signals_base
            check_var_list_before   - variables to verify before injecting an
                                      error. A list of dictionaries with 
                                      variable, rated value and tolerance
                                      See parameter example in testSignals()
            check_var_list_after    - variables to verify after injecting an
                                      error. A list of dictionaries with 
                                      variable, rated value and tolerance
                                      See parameter example in testSignals()
            manual_wait_cycles      - if set, overrides the default number of
                                      cycle times to wait between crc error 
                                      injection and variable checks
                                      (crc_signal_data.error_delay)
            manual_triggers_before  - number of manual triggers to perform on 
                                      bus signal (via  kickout()) prior to the 
                                      "before" check. Obviously this makes the 
                                      most sense for event-based signals
            manual_triggers_between - number of manual triggers to perform on 
                                      bus signal (via  kickout()) prior to the 
                                      "after" check. Again, this makes the 
                                      most sense for event-based signals
            manual_trigger_delay_ms - [ms] delay between trigger calls (usually
                                      the kickout() method has its own built-in 
                                      minimum delay, though)
            
            descr  -  user specific description shown at start of result text
            format -  format string to control/override appearance of 
                      automatically created result text.  
                      A format override should only rarely be used.
        
        Returns a single test result entry (with a single verdict for all 
        checked variables).
    """
    return _bus_tests.testBasicCrcError(
        crc_signal_data, 
        check_var_list_before, 
        check_var_list_after,
        manual_wait_cycles, 
        manual_triggers_before,
        manual_triggers_between,
        manual_trigger_delay_ms,
        descr=descr, format=format
    )
    

# #############################################################################
def testBasicAcError(ac_signal_data, 
                     check_var_list_before=None, check_var_list_after=None,
                     manual_wait_cycles=None,
                     manual_triggers_before=0,
                     manual_triggers_between=0,
                     manual_trigger_delay_ms=0,
                     descr='', format=None): # @ReservedAssignment: format
    """ Check ECU behaviour on alive counter signal errors (for messages sent 
        from HIL system and received by the ECU). 
        
        Info: This function ...
            * checks the "before" variables, 
            * sets the alive counter signal to an error state, 
            * waits a defined number of message cycles, then 
            * checks the "after" variables.
        
        Parameters:
            ac_signal_data          -  AcBusSignal data structure which describes 
                                       the crc signal. See bus_signals_base
            check_var_list_before   -  variables to verify before injecting an
                                       error. A list of dictionaries with 
                                       variable, rated value and tolerance
                                       See parameter example in testSignals()
            check_var_list_after    -  variables to verify after injecting an
                                       error. A list of dictionaries with 
                                       variable, rated value and tolerance
                                       See parameter example in testSignals()
            manual_wait_cycles      -  if set, overrides the default number of
                                       cycle times to wait between crc error 
                                       injection and variable checks 
                                       (ac_signal_data.error_delay)
            manual_triggers_before  -  number of manual triggers to perform on 
                                       bus signal (via  kickout()) prior to the 
                                       "before" check. Obviously this makes the 
                                       most sense for event-based signals
            manual_triggers_between -  number of manual triggers to perform on 
                                       bus signal (via  kickout()) prior to the 
                                       "after" check. Again, this makes the 
                                       most sense for event-based signals
            manual_trigger_delay_ms -  [ms] delay between trigger calls (usually
                                       the kickout() method has its own built-in 
                                       minimum delay, though)
            
            descr  -  user specific description shown at start of result text
            format -  format string to control/override appearance of 
                      automatically created result text.  
                      A format override should only rarely be used.
        
        Returns a single test result entry (with a single verdict for all 
        checked variables).
    """
    return _bus_tests.testBasicAcError(
        ac_signal_data, 
        check_var_list_before, 
        check_var_list_after,
        manual_wait_cycles, 
        manual_triggers_before,
        manual_triggers_between,
        manual_trigger_delay_ms,
        descr=descr, format=format
    )
    

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    try:
        from isytest import sys_utils # test support
        sys_utils.hardenStdout()
    except ImportError:
        # just nice-to-have to avoid stdout encoding woes
        pass
    
    import ttk_tools.dspace.rtplib_offline_stub as rtplib
    import ttk_tools.vector.canapeapi_offline_stub as canapeapi
    
    from  ttk_bus.bus_signals_base import RxBusSignal, TxBusSignal, BusSignalContainer
    
    try:
        from  ttk_base.variables_base  import CalVar, CalVarContainer
    except ImportError:
        # migration: TTk 2.0 structure
        from  ttk_base.vector_canape.variables import Var as CalVar 
        from  ttk_base.vector_canape.variables import VarContainer as CalVarContainer
    
    try:
        from  ttk_base.variables_base  import HilVar, HilVarContainer
    except ImportError:
        # migration: TTk 2.0 structure
        from  ttk_base.dspace_rtplib.variables import Var as HilVar
        from  ttk_base.dspace_rtplib.variables import VarContainer as HilVarContainer
    
    from  ttk_base.values_base     import meta
    
    from  ttk_bus.bus_signals_base import CrcBusSignal
    from  ttk_bus.bus_signals_base import AcBusSignal
    
    # set up a dummy real time application
    appl = rtplib.Appl("foo.sdf", "bar1005", "Offline")
    
    # likewise, create a dummy canape instance
    asap3  = canapeapi.CANapeASAP3(working_dir="I:/am/offline")
    canape = canapeapi.CANapeDevice(asap3, db_filename="offline.a2l")
    
    
    # #########################################################################
    class CalVars(CalVarContainer):
        def __init__(self, tool_ref=None):
            CalVarContainer.__init__(self, tool_ref=tool_ref)
            self.some_var        = CalVar(self, "some_cal_var", unit="", descr="some var description")
            self.some_other_var  = CalVar(self, "some_other_cal_var", unit="mA")
            self.yet_another_var = CalVar(self, "yet_another_cal_var")
            self.foo             = CalVar(self, "Foo", unit="foo")
            self.bar             = CalVar(self, "Bar", unit="bar")
            self.baz             = CalVar(self, "Baz", unit="baz")
            self.status          = CalVar(self, "status_var", lookup={0: 'zerö', 1: 'öne', 2: 'twö', 3: 'thrée'})
    
    class HilVars(HilVarContainer):
        def __init__(self, application):
            HilVarContainer.__init__(self, application)
            appl = application
            self.cv_vorgabe = HilVar(appl, 'Model Root/CV/Value', "V", resettable=False)
            self.cv_monitor = HilVar(appl, 'Model Root/Analog Inputs/CVmon/Out1', "V")
            self.kl30       = HilVar(appl, 'Model Root/KL30/Value', lookup={0: "off", 1: "on"}, resettable=False)
            self.kl15       = HilVar(appl, 'Model Root/KL15/Value', lookup={0: "off", 1: "on"}, resettable=False)
            self.setquux = HilVar(appl, "Model Root/Foo/Bar/Quux/Value")
            self.getbaz  = HilVar(appl, "Model Root/Foo/Bar/Baz/Out1")
    
    class BusSignals(BusSignalContainer):
        def __init__(self, appl):
            self.tx_sig = TxBusSignal(appl, "Model Root/CAN/TxFööoBarSig/Out1", 10,
                                      descr="this is a tx-signal description", unit="V")
            self.rx_sig = RxBusSignal(appl, "Model Root/CAN/RxFooBarSig/Value", 100,
                                      descr="this is a rx-signal description", unit="A")
            
            self.rx_status_sig = RxBusSignal(
                appl, "Model Root/CAN/RxStatusSig/Value", 100,
                descr="this is a rx-signäl \xa0 with a discrete state description",
                lookup={0: 'false', 1: u'true', 2: u'n.d.', 3: u's.n.ä.\x96öüß°'},
            )
            self.tx_status_sig = TxBusSignal(
                appl, "Model Root/CAN/TxStatusSig/Out1", 10,
                descr="this is a tx-signäl with a discrèté stäté dèscriptiön",
                lookup={0: 'false', 1: 'true', 2: 'n.d.', 3: 's.n.a.'},
            )
            self.another_sig = RxBusSignal(
                appl, "Model Root/CAN/Another Signal/Value", 
                alias="Another Bus Signal", descr=u"Anöthér Signäl to tést", unit="rpm", 
                cycle_time=100, 
                change_delay=250, timeout=500, recovery_time=500,
                min_value=0, max_value=4000
            )
            self.crc_signal = CrcBusSignal(
                appl, 'BusSystems/FlexRay/Sending/ACSM/Static/ALIV_SEN_CLU_DT_EXT_RAW_OUT',
                descr=u"Á CRC Signäl to tést",
                alias = "ALIV_SEN_CLU_DT_EXT_RAW_OUT", cycle_time = 10
            )
            self.ac_signal = AcBusSignal(
                appl, 'BusSystems/FlexRay/Sending/emARS_v/Static/ALIV_ST_FTAX_ARS_OUT',
                descr=u"Án ÀLivé Cöuntér Signäl to tést",
                alias = "ALIV_ST_FTAX_ARS_OUT", cycle_time = 10
            )
    
    # #########################################################################
    hil = HilVars(appl)
    cal = CalVars(canape)
    bus = BusSignals(appl)
    
    hil.cv_vorgabe.set(14)
    hil.cv_monitor.set(13.8)
    hil.kl30.setState("on")
    hil.kl15.setState("on")
    
    cal.some_other_var.set(2.1)
    cal.yet_another_var.set(119.14)
    cal.foo.set(1.2)
    cal.bar.set(1.0)
    
    testresult = []
    
    testresult.append(testRxSignal(
        bus.rx_sig,
        set_value = 100, 
        set_value_descr = "Some test value", 
        check_var_list = [
            { "var": cal.some_var,        "value": 0,    "abs_pos": 0.001, "abs_neg": -.1 },
            { "var": cal.some_other_var,  "value": 2.1,  "abs_pos": 1.2 },
            { "var": cal.yet_another_var, "value": meta(121, "mA"),  "rel_neg": -0.1 },
            { "var": 4711,                "value": meta(4710, "µV"), "abs_tol": 5 },
            { "var": cal.foo,             "value": cal.bar, "abs_tol": 1 },
        
        ],
        descr = "This is the supplied testRxSignal description text"
    ))
    
    cal.baz.set(123.000000001)
    #result2 = testRxSignal(bus.another_sig, 123, "middle range", [{'var': cal.baz, 'value': 123}])
    
    cal.status.set(2)
    testresult.append(testRxSignal(
        bus.rx_status_sig, 3, "status 3", [{'var': cal.status, 'value': 3}]
    ))
    cal.status.set(3.000)
    testresult.append(testRxSignal(
        bus.rx_status_sig, 3, "status 3", [
            {'var': cal.status, 'value': 3.0001},
            {'var': cal.status, 'value': 3.0},
            {'var': cal.status, 'value': 3, 'abs_tol': 0.1}
        ]
    ))
    
    
    cal.status.set(3.000)
    bus.tx_sig.signal_var.set(2.024)
    testresult.append(testTxSignal(
        [ {'var': cal.foo, 'value': 1},
          {'var': cal.bar, 'value': 2, "descr": "bar is two"},
          {'var': cal.baz, 'value': 3},
        ],
        bus.tx_sig,
        check_value = 2, check_value_descr="This is a check_value_descr",
        abs_pos = 0.2,
        descr='This is a testTxSignal description'
    ))
    
    bus.tx_status_sig.signal_var.set(1)
    testresult.append(
        testTxSignal(
            [{'var': cal.status, 'value': 1}],
            bus.tx_status_sig, check_value = 1, 
            descr='This is another testTxSignal description'
        )
    )
    
    testresult.append(
        testSignals(
            [ {'var': cal.foo, 'value': 1},
              {'var': cal.bar, 'value': 2, "descr": "bar is two"},
              {'var': bus.rx_status_sig, 'value': 3},
              {'var': bus.rx_sig, 'value': 4711},
            ],
            [ {'var': cal.status, 'value': 0}, 
            ],
            descr='This is a testSignals description text'
        )
    )
    
    bus.tx_sig.set(14)
    bus.tx_status_sig.set(1)
    testresult.append(
        testSignals(
            [ {'var': cal.foo, 'value': 1},
              {'var': cal.bar, 'value': 2, "descr": "bar is two"},
              {'var': hil.cv_vorgabe, "value": 13.8},
            ],
            [ {'var': bus.tx_sig,        'value': 14},
              {'var': bus.tx_status_sig, 'value': 1},
              {'var': hil.cv_monitor,    "value": 14, "abs_tol": 0.3},
            ],
            #min_wait_time_ms = 500,
            descr='This is also a testSignals description text'
        )
    )
    
    # CRC & Alive Counter tests ###############################################
    cal.foo.set(1)
    cal.bar.set(0)
    
    testresult.append(
        testBasicCrcError(
            bus.crc_signal,
            check_var_list_before = [
                 {'var': cal.foo, 'value': 0},
                 {'var': cal.bar, 'value': 0, "descr": "bár is zero"},
            ],
            check_var_list_after = [
                 {'var': cal.foo, 'value': 1},
                 {'var': cal.bar, 'value': 2, "descr": u"bár is two"},
            ],
            descr='This is á testBasicCrcError description text'
        )
    )
    
    testresult.append(
        testBasicAcError(
            bus.ac_signal,
            check_var_list_before = [
                 {'var': cal.foo, 'value': 0},
                 {'var': cal.bar, 'value': 0, "descr": "bár is zero"},
            ],
            check_var_list_after = [
                 {'var': cal.foo, 'value': 1},
                 {'var': cal.bar, 'value': 2, "descr": u"bár is two"},
            ],
            descr=u'This is á testBasicAcError description text'
        )
    )
    
    cal.status.set(3)
    testresult.append(testRxSignal(
        bus.rx_status_sig, 3, "status 3", [
            {'var': cal.status, 'value': 2},
        ]
    ))
    
    
    # #########################################################################
    print "#" * 80
    # just print test result entries in a somewhat formatted way
    for entry in testresult:
        print '-' * 64
        
        verdict = entry[-1]
        indent = max(8, len(verdict) + 2)
        descr = ("\n".join(entry[:-1])).replace("\n", "\n" + " " * indent)
        print "%-*s%s"%(indent, verdict, descr)
        
    
    # cleanup not really needed for offline stubs, but anyway:
    canape = None
    asap3 = None
    appl = None
    
    print("Done.")
# @endcond DOXYGEN_IGNORE
# #############################################################################