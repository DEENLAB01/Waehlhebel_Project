#******************************************************************************
# -*- coding: latin-1 -*-
# File    : variables_base.py
# Task    : Wrapper class for variables' base classes  (hil, cal, ...)
#           This serves as "interface" to the precompiled module in delivery 
#           to enable code-completion in PyDev
#
# Type    : Interface
# Python  : 2.5+
#
# Author  : J.Tremmel 
# Date    : 17.01.2012
# Copyright 2012 - 2020 iSyst Intelligente Systeme GmbH
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Author    | Description
#------------------------------------------------------------------------------
# 1.0  | 17.01.2012 | J.Tremmel | initial
# 1.1  | 26.01.2012 | J.Tremmel | added resetAll to container interface
# 1.2  | 22.05.2012 | J.Tremmel | added parameters default and resettable
# 1.3  | 24.08.2012 | J.Tremmel | added wrapper for class Snapshot
# 1.4  | 11.10.2013 | J.Tremmel | added raw_mode switch to CalVar
# 1.5  | 19.03.2014 | J.Tremmel | added optional verbosity to reset(), renamed
#                               | resetAll's parameter "verbose" to "verbosity" 
#                               | for consistency with naming in VarBase
# 1.6  | 25.04.2014 | Morgus/Trenkel | add support for gamma V variables 
# 1.7  | 27.05.2014 | J.Tremmel | added wrapper for GammaVarDeferred
# 1.8  | 15.12.2015 | J.Tremmel | GammaVarContainer: use same parameter name 
#                               | ("gamma_api"), as in base implementation
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2.0  | 15.01.2016 | J.Tremmel | split device/vendor-specific implementations 
#                               | into their own packages
# 2.1  | 20.09.2016 | J.Tremmel | support for custom value representations
# 2.2  | 15.07.2020 | Tremmel   | removed obsolete "helper" imports for migration from TTk 1.x.x
#******************************************************************************
"""
@package ttk_base.variables_base
Interface Wrapper for variables' base classes in ttk_base._variables_base.

This serves as "interface" to the precompiled module in delivery to enable 
code-completion in PyDev.

Note:
    ttk_base._variables_base also defines VarBase, the base class for 
    specific variable classes. This base class has no wrapped counterpart 
    here, though, as it is only intended for internal use.
    
    See derived classes for details:
        * ttk_base.dspace_rtplib.variables.Var
        * ttk_base.dspace_xilapi.variables.Var
        * ttk_base.rst_gammav.variables.Var
        * ttk_base.vector_canape.variables.Var
    
    A basic implementation VarBase is included in this wrapper, which is 
    not connected to any external interface. See DummyVar

"""
import _variables_base


# #############################################################################
# A minimal stub/dummy test variable not connected to any external interface
# #############################################################################
class DummyVar(_variables_base.DummyVar):
    """ A minimal dummy test variable not connected to any external interface. 
        This is a simple (and direct) implementation of _variables_base.VarBase 
        with get() and set() methods adapted to write to a member variable 
        instead of accessing an external API.
    """
    # #########################################################################
    def __init__(self, context, identifier, unit="", alias="", descr="", 
                 lookup=None, default=None, resettable=True, fmt=None):
        """ Variable initialization.
            
            Parameters:
                context     - parent context that handles tool references
                              This is usually a reference to a variables
                              container or to a tool/api instance, but can be
                              anything for a "DummyVar"
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
        """
        _variables_base.DummyVar.__init__(
            self, context, identifier, 
            unit=unit, alias=alias, descr=descr, 
            lookup=lookup, default=default, 
            resettable=resettable, fmt=fmt
        )
        
    # #########################################################################
    def get(self, *args, **kwargs):
        """ Get the current value. 
            Returns the current value.
        """
        return _variables_base.DummyVar.get(self, *args, **kwargs)
    
    # #########################################################################
    def set(self, value, *args, **kwargs):
        """ Set a new value. 
            
            Parameters: 
                value - value to set
                
            Returns the original value before the set operation occurred. 
        """
        return _variables_base.DummyVar.set(self, value, *args, **kwargs)
    
    # #########################################################################
    def getState(self):
        """ Get a textual state for the variable's current data. This uses 
            the lookup values supplied in constructor.
            Fallback (if no matching state was found) will be the unmapped 
            numeric value.
            
            Returns the description for the value.
        """
        return _variables_base.DummyVar.getState(self)
    
    # #########################################################################
    def setState(self, state):
        """ Set a textual state to the variable. This uses the lookup values 
            supplied in constructor.
            Fallback (if no matching state text was found) will be the
            unmapped input state.
            
            Parameters:
                state - named state to set
                
            Returns the description for the previously set value.
        """
        return _variables_base.DummyVar.setState(self, state)
        
    # #########################################################################
    def reset(self, verbosity=1):
        """ Reset the variable to its initial value before the first set() call.
            Parameters:
                verbosity - verbosity of log output   
                            0: silent  
                            1: show calls to non-resettable variables  
                            2: show all reset calls  
        """
        return _variables_base.DummyVar.reset(self, verbosity)
    
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
        return _variables_base.DummyVar.info(self)
    

# #############################################################################
# Snapshot Container
# #############################################################################
class Snapshot(_variables_base.Snapshot):
    """ Store and restore a "snapshot" of multiple variables' values.
        
        Example:
            snapshot = Snapshot(cal.foo, cal.bar, hil.baz)
            cal.foo.set(1234)
            hil.baz.set(0.05)
            # [...]
            snapshot.restore()
    """
    # #########################################################################
    def __init__(self, *variables):
        """ Create a snapshot of the supplied variables. Note that you can use 
            multiple snapshot instances to quickly switch between snapshots.
            
            Parameters:
                 variables - either a list of variables or each variable as 
                             individual argument
        """
        _variables_base.Snapshot.__init__(self, *variables)
    
    # #########################################################################
    def add(self, variable):
        """ Add a variable to the snapshot and store its value. If a variable 
            is already in the snapshot, its snapshot-value will be updated.
            
            Parameters:
                variable - variable to add to snapshot; has to support a
                           get()-method.
        """
        _variables_base.Snapshot.add(self, variable)
    
    # #########################################################################
    def remove(self, variable):
        """ Remove a variable from the snapshot discarding any stored value.
            
            Parameters:
                variable - variable to remove
            
            Returns True if variable has been removed, otherwise False.
        """
        return _variables_base.Snapshot.remove(self, variable)
    
    # #########################################################################
    def recapture(self):
        """ Take a fresh snapshot of all contained variables. """
        _variables_base.Snapshot.recapture(self)
    
    # #########################################################################
    def restore(self, verbosity=1):
        """ Restore all contained variables to the states/values they had when 
            the snapshot was 
            
            Note:
                The order in which values will be restored is **not** specified.
            
            Parameters:
                verbosity - debug messages:  
                            0: only warnings  
                            1: more chatty
        """
        _variables_base.Snapshot.restore(self, verbosity=verbosity)


# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    
    # Import base class for containers for the test container (with "dummy" vars)
    # For "normal" variables, the specific/matching VarContainer classes found 
    # in implementation-specific sub-packages are the better choice.
    from ttk_base._variables_base import VarContainerBase
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    class TestVar(DummyVar):
        """ A test dummy-variable that is rather verbose. """
        def get(self):
            value = DummyVar.get(self)
            #print '[getting]   "%s", value is %r'%(self, value)
            print '[getting]   "%s", value is %s'%(self, self.getFormattedValue())
            return value
        def set(self, value): # noqa E301
            print '[setting]   "%s" to %r'%(self, value)
            return DummyVar.set(self, value)
        def reset(self, verbosity=0):  # @UnusedVariable verbosity # noqa E301
            print '[resetting] "%s"'%(self)
            return DummyVar.reset(self)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    class ContainerTest(VarContainerBase):
        """ An example container with several test (dummy) variables and
            data structures.
        """
        def __init__(self):
            self.foo    = TestVar(self, "foo!")
            self.bar    = TestVar(self, "bar!")
            self.baz    = TestVar(self, "baz!")
            self.states = TestVar(self, "states", lookup={1: "one", 2: "two", 3: "three", 255: "two hundred fifty-five"}, fmt="0x%02X") # noqa 501
            self.kl30 = TestVar(self, "KL30", unit="V", resettable=False, fmt="%.2f")
            self.text = "hmm"
            self.number = 123
            
            self.a_list = [self.foo, "a string", self.bar, TestVar(self, "NI!")]
            
            self.a_recursive_list = [TestVar(self, "Recursive")]
            self.a_recursive_list.append(self.a_list)
            self.a_recursive_list.append(self.a_recursive_list)
            
            self.a_dict = {
                'one':  TestVar(self, "one"), 
                'two':  TestVar(self, "two"),
                'dict inside': { 
                    'one-one': TestVar(self, "one-one"), 
                    'one-two': TestVar(self, "one-two"),
                },
                "some string": "Lorem Ipsum",
                'a list':  [
                    TestVar(self, "list-one"), 
                    TestVar(self, "list-two"), 
                ]
            }
            
            # some "variables" that will raise errors during reset()
            self.badvar      = TestVar(self, "a_bad_variable")
            self.also_badvar = self.badvar
            self.too_many_badvars = [self.badvar, self.badvar, self.badvar]
            
            def noreset():
                raise Exception("simulated error during reset")
            self.badvar.reset = noreset
            del(noreset)
    
    # #########################################################################
    print
    print("#" * 80)
    print("# Container...")
    print("#" * 80)
    ct = ContainerTest()
    print("\n-- initial values... --------------------------------------------")
    ct.foo.get()
    ct.kl30.get()
    ct.badvar.get()
    
    print("\n-- changing some values... --------------------------------------")
    ct.foo.set("dummy (DummyVars should accept any data type)")
    ct.kl30.set(14.0)
    ct.badvar.set("something") 
    print("-- current values:")
    ct.foo.get()
    ct.kl30.get()
    ct.badvar.get()
    
    print
    print("-- Container resetAll()... ----------------------------------------")
    print('# NO''TE: "badvar" will raise an exception when reset, but reset()/resetAll() will have to tolerate this.')
    ct.resetAll(4, 3)
    print("-- current values:")
    ct.foo.get()
    ct.kl30.get()
    ct.badvar.get()
    print("# Note: kl30 is configured with resettable=False, so it will not be reset.")
    print("#       badvar raises an error during reset , so it stays at its previous value.")
    
    # #########################################################################
    print
    print("#" * 80)
    print("# Snapshot...")
    print("#" * 80)
    print("\n-- setting values... --------------------------------------------")
    foo_val, bar_var, baz_val = 1, 2, 3
    ct.foo.set(foo_val)
    ct.bar.set(bar_var)
    ct.baz.set(baz_val)
    
    print("\n-- getting values... --------------------------------------------")
    print("\n".join([ct.foo.info(), ct.bar.info(), ct.baz.info()]))
    assert [v.last_value for v in (ct.foo, ct.bar, ct.baz)] == [foo_val, bar_var, baz_val], "init values must match"
    
    print("\n-- taking snapshot... -------------------------------------------")
    snapshot = Snapshot(ct.foo, ct.bar, ct.baz)
    
    print("\n-- setting new values... ----------------------------------------")
    ct.foo.set(1234)
    ct.baz.set(0.05)
    print("\n".join([ct.foo.info(), ct.bar.info(), ct.baz.info()]))
    assert [v.last_value for v in (ct.foo, ct.bar, ct.baz)] != [foo_val, bar_var, baz_val], "(some) value have to have changed"
    
    print("\n-- restoring snapshot... ----------------------------------------")
    snapshot.restore(verbosity=1)
    print("\n".join([ct.foo.info(), ct.bar.info(), ct.baz.info()]))
    assert [v.last_value for v in (ct.foo, ct.bar, ct.baz)] == [foo_val, bar_var, baz_val], "restored values have to match init values"
    
    
    # #########################################################################
    print
    print("#" * 80)
    print("# var.setStates()...")
    print("#" * 80)
    print(ct.states.info())
    print("-- trying to set an unspecified/invalid state... ------------------")
    ct.states.setState("foo")
    print("# Note: A state not found in the lookup table will be set as-is using set().")
    print("#       So setState('foo') will turn into set('foo'), which may or may")
    print("#       not work, depending on the specific variable's implementation.")
    # Note: setting a numeric (e.g. CANape-) variable to a string value will 
    #       most likely raise an exception. Since the dummy variables are not 
    #       type specific, it will work here, though.
    print(ct.states.info())
    print("-- trying to set a specified/valid state... -----------------------")
    ct.states.setState("one")
    print(ct.states.info())
    print("-- resetting the variable... --------------------------------------")
    ct.states.reset()
#    print vars(ct).keys()
#    snapshot2 = Snapshot( [getattr(ct, v) for v in vars(ct).keys()] )
    print("\nDone.")
# @endcond DOXYGEN_IGNORE #####################################################
