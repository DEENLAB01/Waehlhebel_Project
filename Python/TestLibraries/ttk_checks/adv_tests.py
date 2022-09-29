#******************************************************************************
# -*- coding: latin1 -*-
#
# File    : adv_tests.py
# Package : ttk.checks
# Task    : Wrapper for advanced test/evaluation functions for test automation 
#           that directly generate test report entries. These functions are 
#           somewhat more complex than those in basic_tests.py
#           This serves as "interface" to the precompiled module in delivery 
#           to enable code-completion in PyDev
# Type    : Interface
# Python  : 2.5+
#
# Copyright 2015 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date       | Author  | Description
#------------------------------------------------------------------------------
# 1.0  | 17.12.2015 | Tremmel | initial
#******************************************************************************
""" 
@package ttk_checks.adv_tests
Interface wrapper for advanced test/evaluation functions in ttk_checks._adv_tests.
These functions are more complex than those in ttk_checks.basic_tests 

This serves as "interface" to the precompiled module in delivery 
to enable code-completion in PyDev.
"""
import _adv_tests


# #############################################################################
def testVars(set_var_list=None, check_var_list=None, min_wait_time_ms=100, descr=''):
    """ Check the values of multiple variables/signals as a result of setting
        multiple other variables/signals. Between setting and checking, a 
        configurable time will be waited to deal with propagation delay. This
        wait time defaults to the minimum practicable wait time of all involved 
        bus signals.
        
        Info: This function ...
            * sets the value(s) to the variables in set_var_list
            * triggers sending of any event-based signals included in set_var_list
              - "needs triggering" is determined by evaluating `cycle_time` 
                 members of set vars (if present)
              - triggering is performed by calling a method `kickout()` or 
                `trigger()` (whichever is available)
            * waits for value change(s) to propagate to ECU/DUT  
              - this depends on both the specified `min_wait_time_ms` and any
                `change_delay` members of entries in set or check var lists.
            * checks the value(s) for variables in check_var_list
        
        Parameters:
            set_var_list     -  Variables to set: a list of dictionaries with 
                                variable and value 
            check_var_list   -  Variables to check: a list of dictionaries with 
                                variable, expected value and tolerance
            min_wait_time_ms -  minimum wait time between setting variables and
                                performing checks
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
               { "var":   <variable to set (e.g. a CalVar, HilVar or anything with a set() method),
                 "value": <value to set>,
                 "descr": <value description, optional>,
               },
               
        
        Example: set_var_list and function calls
           # For special cases, the set var list may also contain function calls
           # (which might be useful to insert additional delays or similar):
           set_var_list = [
               { "var":    cal.reset_var, "value": 1, descr="enable reset" },
               { "func":   time.sleep,
                 "args":   [1.0], # positional arguments
                 "kwargs": {},    # keyword arguments
                 "descr":  "Wait for one second before clearing reset again",
               },
               { "var":   cal.reset_var, "value": 0 },
               # or a simple call like this:
               { "func":  someCustomFunction,
                 "descr": "a custom function that does no need any parameters",
               },
               ...
           ] 
        
        Example: check_var_list structure
            # A basic entry:
            check_var_list = [
                { "var":     <variable to check (CalVar, HilVar, ...)>,
                  "operator": <check operator, defaults to "==">,
                  "value":   <expected value(s)>
                  "abs_tol": <absolute tolerance (optional)>,
                  "rel_tol": <relative tolerance (optional)>,
                }
            ]  
            # abs_tol/rel_tol are aliases for checkTolerances's abs_pos/rel_pos
            # (when separate _pos/_neg tolerances are not required).
            # If you need non-symmetrical tolerances (e.g. -1/+5), you can
            # specify tolerances separately:
            check_var_list = [
                { "var":      <variable to check (CalVar, HilVar, ...)>,
                  "operator": <check operator, defaults to "==">,
                  "value":    <expected value> or a list of expected values, of which one has to pass
                  "rel_pos":  <relative positive tolerance (optional)>,
                  "abs_pos":  <absolute positive tolerance (optional)>,
                  "rel_neg":  <relative negative tolerance (optional)>,
                  "abs_neg":  <absolute negative tolerance (optional)>,
                },
                ...
            ]
            # See basic_checks.checkTolerance for details on tolerance parameters
            # "==" is default when operator entry is omitted
        
        Example: extended check_var_list structure
            check_var_list = [
                { "var":     <variable to check (CalVar, HilVar, ...)>,
                  "operator": "==", # "==" or "in"
                  "value":   <expected value> or a list of multiple expected values of which one has to match
                  "abs_pos": <absolute tolerance (optional)>,
                  "rel_pos": <relative tolerance (optional)>,
                },
                { "var":     <variable to check (CalVar, HilVar, ...)>,
                  "operator": "!=", # "!=" or "not in"
                  "value":   <expected value> or a list of multiple expected values, none of which must match
                  "abs_pos": <absolute tolerance (optional)>,
                  "rel_pos": <relative tolerance (optional)>,
                },  
                { "var":     <variable to check (CalVar, HilVar, ...)>,
                  "operator": ">", # "<", "<=", ">=" or ">"
                  "value":   <expected value> 
                  # no tolerances are used for "greater/less than" comparisons
                },
                ...
            ]
         
         Example: Using a list of multiple expected values (usually for status values):
            # Operator "==" or "in": one value has to match
            check_var_list = [
                { "var":       cal.e2e_status,
                  "operator": "in"
                  "value":    [E2E_P04STATUS_OK, E2E_P04STATUS_OKSOMELOST],
                }
            ]
            
            # Operator "!=" or "not in": no value may match:
            check_var_list = [
                { "var":      cal.e2e_status,
                  "operator": "not in",
                  "value":    [E2E_P04STATUS_NONEWDATA, E2E_P04STATUS_ERROR, 
                               E2E_P04STATUS_REPEATED, E2E_P04STATUS_WRONGSEQUENCE],
                }
            ]
            
        
        Info: "var" and "value" in check- and set_var_list
            Both variable to check and the expected "value" can actually
            be any VarBase derived instance, meta()-wrapped MetaValue instances 
            or plain scalar numeric values.
            
            This means that it is possible to compare the values of two 
            ecu/cal variables:  
            `   {"var": cal.some_variable, "value": cal.some_other_variable} `  
            or between hil and ecu  
            `   {"var": cal.foobar,     "value": hil.barbaz}                 `  
            `   {"var": bus.barsignal,  "value": cal.bazquux}                `  
            or even (admittedly, not too useful)  
            `   {"var": 3, "value": 3.2, "abs_tol": .4}                      `  
        
        Info: Units and plain values
            If none of the involved variables/values has a "unit" specified 
            and you want to show units in the test report, you could wrap 
            values in a MetaValue:  
            `   {"var": cal.shrdlu, "value": meta(3.2, "mV"), "abs_tol": .4} `  
            See ttk_base.values_base.meta()
        
        Info: Status values and tolerances:
            If all tolerances of a check_var_list entry remain un-set 
            (i.e. None), the values will be treated as discrete integer states 
            during comparison. If a value does not appear to be an integer value,
            the test will fail with verdict ERROR (and the actual check using 
            the un-cast value(s) will most likely fail as well).  
            See ttk_checks.checkutils.getInteger()
        
        Returns a single test result entry [<description>, <VERDICT>] 
        (with a single resulting verdict for all checked variables).
    """
    return _adv_tests.testVars(
        set_var_list     = set_var_list, 
        check_var_list   = check_var_list, 
        min_wait_time_ms = min_wait_time_ms, 
        descr = descr,
    )
    

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__":  # pragma: no cover (main contains only sample code)
    import time
    from ttk_base.variables_base import DummyVar
    testresult = []
    
    var1 = DummyVar(None, "var1_name", 
        lookup={0: 'false', 1: 'true', 2: 'n.d.', 3: 's.n.a.'},
        unit="var1-unit",
    )
    var2 = DummyVar(None, "var2_name", unit="var2-unit")
    var3 = DummyVar(None, "var3_name", unit="mA")
    
    testresult.append(
        testVars(
            set_var_list = [
                {"var": var1, "value": 1,   "descr": "1st value to set"},
                {"var": var2, "value": 2,   "descr": "2nd value to set"},
                {"func": time.sleep, "args":  [0.200], "descr": "waiting a bit..." },
                {"var": var3, "value": 2.2, "descr": "3rd value to set"},
            ],
            check_var_list = [
                {"var": var3, "value": 0, "abs_tol": 0.1, "descr": "[1st]"},
                {"var": var2, "operator": "!=", "value": 0, },
                {"var": var2, "operator": "!=", "value": var1, },
                {"var": var3, "operator": "!=", "value": 0, "abs_tol": 0.1},
                {"var": var2, "operator": ">",  "value": 1},
                {"var": var2, "operator": ">",  "value": 1, "abs_tol": 0.1},
                {"var": var2, "operator": "<",  "value": 4},
                {"var": var1, "operator": "<=", "value": var2},
                {"var": var1, "operator": "<=", "value": var2},
                {"var": var1, "operator": "in", "value": [1, 2, 3]},
                {"var": var1, "operator": "not in", "value": [1, 2, 3]},
            ],
            descr = "A description text"
        )
    )
    
    testresult.append(
        testVars(
            check_var_list = [
                {"var": 1, "value": 1, "abs_tol": 0.1},
                {"var": var1, "operator": "in", "value": [1, 2, 4711]},
                {"var": 1, "operator": "in", "value": [1, 2, 3]},
            ],
            descr = "Only checks"
        )
    )
    
    testresult.append(
        testVars(
            descr = "Nothing set, nothing checked => no verdict"
        )
    )
    
    testresult.append(
        testVars(
            descr = "Nothing set, nothing checked (and not even a delay).\n"
                    "Again, no check => no verdict",
            min_wait_time_ms = 0
        )
    )
    
    # #########################################################################
    for entry in testresult:
        verdict = entry[-1]
        indent  = max(8, len(verdict))
        descr   = ("\n".join(entry[:-1])).replace("\n", "\n" + " " * (indent + 1))
        print('-' * 64)
        print("%-*s%s"%(indent, verdict, descr))
        
    
    print("Done.")
    

# @endcond DOXYGEN_IGNORE 
# #############################################################################