#******************************************************************************
# -*- coding: latin-1 -*-
# File    : values_base.py
# Package : ttk_base
# Task    : Wrapper class for values with additional meta information
#           This serves as "interface" to the precompiled module in delivery 
#           to enable code-completion in PyDev
#
# Type    : Interface
# Python  : 2.5+
#
# Copyright 2012 - 2020 iSyst Intelligente Systeme GmbH
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Author  | Description
#------------------------------------------------------------------------------
# 1.0  | 22.05.2012 | Tremmel | initial
# 1.1  | 10.03.2016 | Tremmel | added support for lookup-tables
# 1.2  | 20.09.2016 | Tremmel | added support for custom value representations
# 1.3  | 02.02.2018 | Tremmel | tweaks in sample code for Python 2.5
#******************************************************************************
"""
@package ttk_base.values_base
Interface Wrapper for values with additional meta information in 
ttk_base._values_base.

This serves as "interface" to the precompiled module in delivery to enable 
code-completion in PyDev.
"""
import _values_base


# #############################################################################
def meta(value, unit="", alias="", descr="", lookup=None, fmt=None):
    """ Factory function to create "meta" instances of the supplied value
        that have some additional meta attributes bolted on. Additionally,
        meta instances have a method info() that will return an info string 
        (alias and current value, similar to variables from variables_base.
        See _values_base.MetaValue
        
        Example: What's the point?
            # Wrapping a value in a meta instance permits check/test functions
            # to extract the associated meta data to give better feedback.
            >>> checkTolerance(11.3, 12, abs_pos=.8)[0]
            Expected value: 12
            Current value:  11.3
            Absolute Tolerance:  +/- 0.8 V
            
            from ttk_base.values_base import meta
            >>> checkTolerance(meta(11.3, "V"), meta(12, "V"), abs_pos=.8)[0]
            Expected value: 12 V
            Current value:  11.3 V
            Absolute Tolerance:  +/- 0.8 V
            
            # As variables using VarBase can also contain meta data, a simple 
            # check might look like this:
            >>> checkTolerance(cal.v_bat, meta(12, "V"), abs_pos=.8)[0]
            Expected value: 12 V
            Current value:  12.41 V
            Absolute Tolerance:  +/- 0.8
        
        Attention:
            Meta data is - more or less - just "eye candy" for nicer report 
            output. It does **not** influence the actual test processing, so
            you could compare apples and oranges, V and mA, or mV and kV.  
            Just don't expect the values to be "automagically" converted to 
            their base units for comparison purposes.
        
        Example: Meta data does not influence checks
            # This is just wrong (though the check will be PASSED, 
            # as it ignores meta info):
            >>> checkTolerance(meta(12, "V"), meta(12, "mV"), abs_pos=.8)[0]
            Expected value: 12 mV
            Current value:  12 V
            Absolute Tolerance:  +/- 0.8 V
        
        Info: Meta Attributes (via MetaValue):
            * .alias - alias name
            * .descr - description string
            * .unit  - unit string
            * .fmt   - value formatting
            
            If a lookup table has been supplied, it will be available as
            .state_lookup (same as for VarBase-derived variables).  
            See _values_base.MetaValue
        
        Info: MetaValue Methods:
            * .info()                   - gets an info string for this value
            * .hasStateLookup()         - True if a lookup table is configured
            * .getStateDescr(value)     - get a state description text for the value
            * .hasFormattedRep()        - True if a non-default format is configured
            * .getFormattedValue(value) - get a formatted string representation for the value
            
            See _values_base.MetaValue  
            Compare interface of ttk_base._variables_base.VarBase
        
        Parameters:
            value   -   value that should get meta info added. Currently
                        supported types are int, long, float, str and unicode
            unit    -   meta info: value's unit, e.g. mV
            alias   -   meta info: an alias name for the value
            descr   -   meta info: description/comment text
            lookup  -   meta info: lookup table, dict with mappings
                                   {value => "state name"} 
            fmt     -   meta info: format string to use for value representation
        
        Returns an instance of a class derived from value's class, that has
        the additional meta attributes set.
    """
    return _values_base.meta(
        value=value, 
        unit=unit, 
        alias=alias, 
        descr=descr, 
        lookup=lookup,
        fmt=fmt
    )
    

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__":  # pragma: no cover (main contains only sample code)
    import sys
    
    def safePrint(*args):
        # default stdout encoding in Python 2.5 seems to be None which
        # falls back to ASCII, so printing higher unicode chars would raise
        # UnicodeEncodeErrors
        for s in args:
            if isinstance(s, unicode):
                # no keyword argument "error" in Python 2.5 (only positional)
                s = s.encode(sys.stdout.encoding or "latin-1", "replace") 
            print s,
        print
    
    # #########################################################################
    def show(meta_value):
        safePrint("meta: %-16s => info(): %s"%(meta_value, meta_value.info())) 
        
    value = meta(123, unit="mV", descr="Lorem Ipsum")
    value.unit = "V"
    show(value)
    
    show( meta(123, unit="mV", descr="Lorem Ipsum", fmt="%.2f") )
    show( meta(123, alias="hex_status", fmt="0x%.2X") )
    show( meta(4711, "mA") )
    show( meta(4711, "mA", alias="some_value") )
    show( meta(u"öäü", alias="unicode/text-string") )
    show( meta("foo",  alias="byte-string") )
    show( meta("foo",  alias="bytes-string (repr as fmt)", fmt="%r") )
    show( meta([1, 2, 3, "foo"], alias="some_list", descr="a list with meta info") )
    show( meta((1, 2, 3), alias="some_tuple", descr="a tuple with meta info") )
    
    # #########################################################################
    print("\n", "# " * 40)
    
    def metaInfo(*args, **kwargs):
        ##print "meta(%s)"%(", ".join(["%s"%(s) for s in args] + ["%s=%s"%(k,v) for k,v in kwargs.items()]))
        value = meta(*args, **kwargs)
        safePrint("%-6s => %-42s # %s"%(value, value.info(), value.descr))
    
    lut = {0: "zero", 1: "one", 2: "two", 3: "three", 42: "forty-two", "foo": "bar", (1, 2): "tuple with 1, 2"}
    metaInfo(1,       alias="int_status",   lookup=lut, descr="prime use-case for status lookup")
    metaInfo(1,       alias="hex_status",   lookup=lut, descr="prime use-case for status lookup", fmt="%#x")
    metaInfo(1,       alias="hex_status",   lookup=lut, descr="prime use-case for status lookup", fmt="%#06x")
    metaInfo(2.0,     alias="float_status", lookup=lut, descr="status w/ float, works as long as float values match")
    metaInfo((1, 2),  alias="tuple_status", lookup=lut, descr="status w/ tuple, not that useful")
    metaInfo([1, 2],  alias="list_status",  lookup=lut, descr="status w/ list, no status lookup for lists (non-hashable)")
    metaInfo("foo",   alias="str_status",   lookup=lut, descr="status w/ string, not that useful, too")
    
    print("\nDone.")
# @endcond DOXYGEN_IGNORE #####################################################
