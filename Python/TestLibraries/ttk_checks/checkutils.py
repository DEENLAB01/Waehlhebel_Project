#******************************************************************************
# -*- coding: latin1 -*-
#
# File    : checkutils.py
# Package : ttk_checks
# Task    : Utilities for check functions
#
# Type    : Interface
# Python  : 2.5+
#
# Copyright 2011 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date       | Author  | Description
#------------------------------------------------------------------------------
# 1.0  | 31.07.2017 | Tremmel | initial, interface to _checkutils 1.20
# 1.1  | 13.03.2020 | Tremmel | updated for _checkutils 1.24
# 1.2  | 13.03.2020 | Tremmel | updated for _checkutils 1.26
# 1.3  | 30.03.2020 | Tremmel | updated for _checkutils 1.27: simplified 
#                             | localization reference handling.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2.0  | 15.07.2020 | Tremmel | removed obsolete getMetaInfo
#******************************************************************************
""" 
@package ttk_checks.checkutils
Interface wrapper for check functions utilities in ttk_checks._checkutils
"""
import _checkutils

## maximum divergence to still accept a float value to be "intended" as int/long
from _checkutils import FLOAT_CONVERSION_LIMIT  # @UnusedImport

## IEEE-754 double-precision => 52 bits explicitly stored
from _checkutils import FLOAT_CONVERSION_MAX_VALUE # @UnusedImport


# #############################################################################
class DefaultDict(_checkutils.DefaultDict):
    """ A dictionary that returns empty strings instead of raising KeyErrors."""
    

# #############################################################################
def buildDescription(descr_format, entries):
    """ Build a result description from a supplied format string and 
        entries. If the format is invalid, all available entries will be
        returned.
        
        Parameters:
            descr_format   - a format string (preferably referencing entries of, 
                             well, entries. If an non-existing entry is referenced,
                             an empty string will be added in its place.
            
            entries        - a dictionary of entries to use in `format_str`
        
        Examples:
            >>> d =  {"foo": "FOO", "baz": 12345}
            >>> buildDescription("Lorem: %(foo)s\nIpsum: %(bar)s%(baz)d", d)
            Lorem: FOO
            Ipsum: 12345
            >>> buildDescription("Lorem: %(foo)x\nIpsum: %(bar)s%(baz)d", d)
            Invalid Format Specified: %x format: a number is required, not str
            Available entries:
            'baz':    12345
            'foo':    FOO
        
        Returns a formatted description string 
    """
    return _checkutils.buildDescription(
        descr_format   = descr_format, 
        entries        = entries,
    )
    

# #############################################################################
def getInteger(value):
    """ Cast a numeric value to an integer (int/long) number, but perform 
        sanity checks before (relevant for float input values).  
        If `value` is already long (or int), it will simply be returned as-is.
        
        Note:
            Raises an ValueConversionError if `value` does not appear to be 
            representing an integer or if it cannot fit into a double-precision 
            float without loss of precision.
        
        Parameters:
            value - numeric value to interpret as integer number
        
        Returns an int (if value fits into int range), or a long value.
    """
    return _checkutils.getInteger(value)


# @cond DOXYGEN_IGNORE
def getNaturalNumber(value):
    """ See getInteger - renamed, as we actually return integers, not just
        natural numbers (i.e. also negative whole values)
    """
    return _checkutils.getInteger(value)
# @endcond DOXYGEN_IGNORE


# #############################################################################
def resolveValue(value):
    """ Get a value of the input parameter if it supports a "get" function, 
        otherwise return it as-is.
        
        Raise a ttk_base.errors.TTkException if the get() call results in an 
        ttk_base.errors.TTkErrorString.
    """ 
    return _checkutils.resolveValue(value)
    

# #############################################################################
def updateMetaInfo(meta, value, key_prefix="", 
                   meta_attrs=None, setdefaults=False, fallback_value=None):
    """ Extract meta info from `value` (if info is available) and update the 
        supplied meta dictionary with those values.
        Keys will only be present/updated if the value has matching info.
        
        Note: Default meta_attrs:
            * `unit`  - unit as a string
            * `descr` - description as a string
            * `alias` - alias name  as a string
            * `state` - string description of current state (if available from lookup)
            * `fmt`   - value formatted using an available format string (e.g. "0x%02X") 
        
        Info: Key naming
            Entries will be added with a leading `key_prefix`, so with a
            `key_prefix = "source_var_"` 
            and the default `meta_attrs`, the following keys will be added/updated
            (as long as the `value` provides the respective members):
            * "source_var_unit" 
            * "source_var_descr" 
            * "source_var_alias"
            * "source_var_state"
            * "source_var_fmt"
            plus
            * "formatted_source_var_alias" (see next note)
        
        Note: alias
            For `alias` an additional entry `formatted_<key_prefix>_alias` 
            will be added that will contain the alias name formatted with the 
            l10n-format `<alias info format>`.
        
        Note: value and current_value
            If `value` is not an instance that provides either 
              * a suitable string representation of its "value" (e.g. basic 
                types like int or float) or
              * a method getFormattedValue (like all VarBase-derived variables) 
            the formatted representation entry ("fmt") will most likely not 
            contain the expected value but default to something like 
            <foo.NotSoGood object at 0x000000000E8588D0>.
            
            If a separate value (e.g. a float value from a .get() operation) is 
            available, it can be supplied as `current_value` and will be used
            as fallback representation for `value`.
        
        Parameters: 
            meta           - dictionary to update, potentially with already 
                             existing meta entries 
            value          - value (or a VarBase derived instance) that may 
                             have additional meta info attached (unit, description, ...)
            key_prefix     - prefix to prepend to dictionary keys
            meta_attrs     - list of custom meta attributes to extract.  
                             Defaults to `("unit", "descr", "alias", "state", "fmt")`
            setdefaults    - if True, already existing meta keys will not get 
                             overwritten (i.e. only default values will be set)
            fallback_value  - optional current/resolved value of the supplied 
                             `value` parameter.  
                             Defaults to `value`. See note.
    """
    _checkutils.updateMetaInfo(
        meta            = meta, 
        value           = value, 
        key_prefix      = key_prefix,
        meta_attrs      = meta_attrs, 
        setdefaults     = setdefaults,
        fallback_value  = fallback_value,
    )
    

# #############################################################################
def updateMetaStateDescr(meta, source_var, value, key):
    """ Update (or create) a meta entry with a state description for the
        supplied value, using the lookup-table from `source_var`. 
        An already existing state description will not be overwritten.
        
        Parameters:
            meta           - dictionary to update, potentially with already 
                             existing meta entries 
            source_var     - source variable (or meta-enhanced value) with lookup table
            value          - value to lookup
            key            - key name for state info (typically `<name>_state`)
        
    """
    _checkutils.updateMetaStateDescr(
        meta           = meta, 
        source_var     = source_var, 
        value          = value, 
        key            = key, 
    )
    

# #############################################################################
def updateMetaFormattedValue(meta, source_var, value, key="fmt", fallback_value=None):
    """ Update (or create) a meta entry with a formatted value representation 
        for the supplied value, using the formatting defined in `source_var`.
        
        An already existing non-default formatted value representation will 
        not be overwritten.
        
        Parameters:
            meta           - dictionary to update, potentially with already 
                             existing meta entries 
            source_var     - source variable (or meta-enhanced value) with value 
                             formatting hints to update default representations
            value          - actual value to format (might have its own value 
                             formatting hints, though)
            key            - key name for state info (typically `<name>_fmt`)
            fallback_value - optional fallback value (typically a a base type 
                             like int or float) to use for value representation 
                             if no suitable formatting can be found for `value`
        
        Note: fallback_value vs. value 
            If a "partial" variable has been supplied, e.g. a basic object with
            just a get() method but not much else (no getFormattedValue() and 
            not even a custom __str__ method), the fallback representation would
            be something like `"<foo.NotSoGood object at 0x000000000E8588D0>"`.
            
            By providing an optional resolved fallback_value (like used in 
            source_vars_info), we can deal with this special case.
        
    """
    _checkutils.updateMetaFormattedValue(
        meta           = meta, 
        source_var     = source_var, 
        value          = value, 
        key            = key, 
        fallback_value = fallback_value,
    )
    

# #############################################################################
def updateMetaEntries(meta, *source_vars_info):
    """ All-in-one update of meta data. 
        
        * update all meta entries of the supplied variables (see updateMetaInfo()),  
          then 
        * fill any missing entries that can be derived from other source
          variables.  
          This means shared meta data like units or lookup values -- 
          checks/comparisons make not much sense if source values use different 
          definitions.
        
        Parameters:
            meta               - dictionary to update, potentially with already 
                                 existing meta entries 
            
            *source_vars_info  - all following entries must be triples of 
                                 `[source_var, meta_key_prefix, current_value]`.  
                                 * `current_value` may be None if no state lookup 
                                   is desired.  
                                 * If `current_value` is None, a VarBase or
                                   meta()-wrapped value will use its last value 
                                   to provide a formatted value
    
    """
    _checkutils.updateMetaEntries(meta, *source_vars_info)
    

# #############################################################################
def bin(value, prefix='0b', min_bit_width=0): # @ReservedAssignment: bin
    """ Create a binary representation of the input value. A rather recursive 
        approach, works similar to the built-in function bin() that is 
        available in Python 2.6+, but with some additional convenience features.
        
        Parameters:
            value         - value to represent as a binary string
            
            prefix        - prefix to prepend the string (usually "0b", just
                            like bin() would add and similar to the "0x" for hex)
            
            min_bit_width - a minimum bit width to enforce (filled with zeros)
        
        Returns a string with a binary representation of the input value.
    """
    return _checkutils.bin(
        value         = value, 
        prefix        = prefix, 
        min_bit_width = min_bit_width
    )
    

# #############################################################################
def getTracebackString(limit=None):
    """ Get current traceback info as a string (or an empty string if no 
        exception is currently active).
    """
    return _checkutils.getTracebackString(limit=limit)
    

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__":  # pragma: no cover (main contains only sample code)
    import sys
    
    class OutputStreamProxy(object):
        def __init__(self, stream):
            self._stream = stream
            self._encoding = getattr(stream, "encoding", None) or "latin1"
        
        def __getattr__(self, name):
            return getattr(self._stream, name)
        
        def write(self, s):
            if not isinstance(s, basestring):
                s = str(s)
            try:
                return self._stream.write(s)
            except (TypeError, UnicodeError):
                pass
            return self._stream.write(s.encode(self._encoding, "backslashreplace"))
        
        def writelines(self, lines):
            if not lines:
                return 
            for line in lines:
                self.write(line)
        
    sys.stdout = OutputStreamProxy(sys.stdout)
    
    
    # #########################################################################
    print("\n" + "# " * 40)
    d =  {"foo": "FOO", "baz": 12345}
    
    print("# valid:")
    print(buildDescription("Lorem: %(foo)s\nIpsum: %(bar)s%(baz)d", d))
    
    print("# unknown format marker:")
    print(buildDescription("Lorem: %(foo)s\nIpsum: %(bar)p%(baz)d", d))
    
    print("# mismatching format + unknown format marker (in order of appearance in string):")
    print(buildDescription("Lorem: %(foo)x\nIpsum: %(bar)p%(baz)d", d))
    
    print("# unknown format marker + mismatching format (in order of appearance in string):")
    print(buildDescription("Lorem: %(foo)p\nIpsum: %(bar)x%(baz)d", d))
    
    print("# mismatching format:")
    print(buildDescription("Lorem: %(foo)x\nIpsum: %(bar)s%(baz)d", d))
    
    # #########################################################################
    print("\n", "# " * 40)
    print("# encoding woes (mixed (byte-)string, non-ASCII-byte-string, unicode):")
    print(buildDescription(
        "%(foo)s / %(bar)s / %(baz)s", 
        {"foo": "äöüF°°\x01\x96", "bar": u"äöüF°°\x01\x96", "baz": 1235}
    ))
    print("# dto. + nested data structures with yet more strings")
    descr = buildDescription(
        '| "%(foo)s" / "%(bar)s" / "%(baz)s" / "%(qux)s"\n'
        '| "%(pip)s"\n'
        '| "%(dip)s"', 
        {
            "foo": "str-äöü\x96°\xe4\xf6\xfc\xa0\xdf\x95", 
            "bar": u"uni-äöü\x96°\xe4\xf6\xfc\xa0\xdf\u2022",
            "baz": "str-abc",
            "qux": u"uni-abc",
            "pip": [
                 "str-äöü\x96°\xe4\xf6\xfc\xa0\xdf\x95", 
                u"uni-äöü\x96°\xe4\xf6\xfc\xa0\xdf\u2022", 
                 "str-abc", 
                u"uni-abc", 
                [
                     "str-äöü\x96°\xe4\xf6\xfc\xa0\xdf\x95", 
                    u"uni-äöü\x96°\xe4\xf6\xfc\xa0\xdf\u2022", 
                     "str-abc", 
                    u"abc",
                ]
            ],
            "dip": {
                "str-äöü\x96°":   "äöü\x96°\xe4\xf6\xfc\xa0\xdf\x95", 
                u"uni-äöü\x96°": u"äöü\x96°uni-\xe4\xf6\xfc\xa0\xdf\u2022",
                "str-abc":        "abc", 
                u"uni-abc":      u"abc",
            }
        }
    )
    print("Type:", type(descr))
    print(descr)
    
    print("\nDone.")
# @endcond DOXYGEN_IGNORE
# #############################################################################
