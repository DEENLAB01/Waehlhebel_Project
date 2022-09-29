#******************************************************************************
# -*- coding: latin1 -*-
#
# File    : basic_tests.py
# Package : ttk_checks
# Task    : Wrapper for basic test/evaluation functions for test automation 
#           that directly generate test report entries.
#           This serves as "interface" to the precompiled module in delivery 
#           to enable code-completion in PyDev
# Type    : Interface
# Python  : 2.5+
#
# Author  : J.Tremmel
# Copyright 2012 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date       | Author  | Description
#------------------------------------------------------------------------------
# 1.0  | 21.05.2012 | Tremmel | initial
# 1.1  | 16.09.2012 | Tremmel | added checkStatus() as special case of checkTolerance()
# 1.2  | 18.10.2013 | Tremmel | checkStatus() now supports optional not-equal check
# 1.3  | 07.03.2013 | Tremmel | updates for minor review findings
# 1.4  | 31.07.2014 | Tremmel | added abs_tol support to compare() (for numeric values)
# 1.5  | 18.03.2016 | Tremmel | added info to checkTolerance's docstring
# 1.25 | 27.04.2020 | Tremmel | added test function compareCE (a variant of compare)
#******************************************************************************
""" 
@package ttk_checks.basic_tests

Interface wrapper for basic test/evaluation functions that directly generate 
test report entries in ttk_checks._basic_tests.
This serves as "interface"to the precompiled module ttk_checks._basic_tests
in delivery to enable code-completion in PyDev.

Example:
    testresult.append(
        checkBitPattern(
            cal.io_error_bits, '0bxxxx0101',
            "Both low side drivers should report errors."
        )
    )

Conventions:
    Each function will take the required parameters for the test to perform 
    plus two additional parameters for report formatting:
      * `descr`  - a description string that will be placed at the start of the 
                   result description text
      * `format` - a format-string that specifies/overrides the formatting of the 
                   automatically generated part of the description.
    
    Do not override `format` unless absolutely necessary.  
    If you want to change the default output formatting of a test function, 
    it would be better to look into changing the current localization 
    (see ttk_checks.basic_tests_loc), so all tests will use consistent result 
    formatting.  
    See also http://docs.python.org/library/stdtypes.html#string-formatting
    
    If an input value has a get()-method, it will be called to get the 
    current value. Otherwise the value will be used as-is.  
    This permits "CalVar" or "HilVar" instances to be directly used in test
    function parameters.  
    See ttk_base.variables_base
    
    If an input value has associated meta data (like "Cal" or "Hil" Vars or 
    basic values wrapped as MetaValues), it can be used in the automatically
    generated description (e.g. unit or alias names)  
    See ttk_base.variables_base, ttk_base.values_base.meta()
    
    Each function will return exactly one result entry for a test results
    list, i.e. typically a list containing `["<description>", "<VERDICT>"]`  
    See https://wiki.isyst.de/wiki/Testresult for more info on our standard 
    test results.
    
    Exceptions occurring "inside" a test function have to be caught; the 
    function will return a result entry containing the error text and verdict 
    `ERROR`.  
    That means it should _not_ be necessary to wrap the test function into yet
    another `try .. except` block.  
    
    If a test function raises an (unexpected) exception anyway, please file 
    a bug report: http://trac.isyst.de/iTestStudio/newticket
    or contact support at support.iteststudio@isyst.de
    
"""
import _basic_tests
from basic_checks import CHECKBITMASK_DEFAULT_BIT_LENGTH


# ############################################################################
def checkBitMask(value, mask, operator="AND", 
                 bit_length=CHECKBITMASK_DEFAULT_BIT_LENGTH,
                 pass_on_true=True,
                 descr="", format=None # @ReservedAssignment: format
    ):
    """ Check result of the operation given in `operator`. Depending on 
        parameter `pass_on_true`, the test will be PASSED if the result is 
        True (i.e. 'greater 0') or False (i.e. 'equal 0').
        
        Parameters:
            value        -  value to be checked
            mask         -  mask to be used for operation in operator
            operator     -  operator for check operation, one of 
                            ("AND", "OR", "XOR", "NAND", "NOR", "NXOR")  
                            see _basic_checks.CHECKBITMASK_*-constants.
            bit_length   -  bit length for value and mask
            
            pass_on_true -  if True, test will be PASSED if result is 'greater 0',
                            otherwise it will be PASSED if the result is 'equal 0'
            descr        -  user specific description shown at the start of the 
                            result text
            format       -  format string to control/override appearance of the 
                            automatically created result text.  
                            A format override should only rarely be used.
        
        Usage:
            testresult.append(
                checkBitMask(
                    value      = status_bits, # 0b00001100
                    mask       = 0x0F,
                    operator   = "AND",
                    bit_length = 8,
                    descr      = "Some bits of the lower nibble should be set"
                )
            )
        Text: Sample Result Output:
            PASSED  Some bits of the lower nibble should be set
                    Value:    12 (status_bits_alias)
                    Operator: AND
                    Mask:     15
                    Result:   0b00001100
        
        Returns a single [<description>, <verdict>] test result entry.
    """
    return _basic_tests.checkBitMask(
        value, mask, operator, bit_length, pass_on_true, 
        descr=descr, format=format
    )
    

# #############################################################################
def checkBitPattern(value, pattern, descr="", format=None): # @ReservedAssignment: format
    """ Check that a numeric value matches a certain pattern.
        
        Parameters:
            value     - value to check. The value must match the full pattern 
                        in order to pass. Values may be numeric (int/long),
                        string representations of binary/hexadecimal values 
                        ("0xABCD", "0b1010" etc.) or a list of bytes.
            
            pattern   - a string describing the desired bit pattern.  
                        * a pattern must always describe the full value 
                          (i.e. all bits from start to end).  
                        * a pattern starting with "0x" will be interpreted as hexadecimal 
                        * "0b" at the beginning denotes a binary pattern 
                        * "X" marks "don't care" sections (may appear anywhere in pattern)
            
            descr     -  user specific description shown at the start of the 
                         result text
            
            format    -  format string to control/override appearance of the 
                         automatically created result text.  
                         A format override should only rarely be used.
        
        Info: Pattern String Examples: 
            * `0xABC123`   - a hexadecimal 20-bit pattern
            * `123ABC`     - without a prefix, pattern defaults to hexadecimal
            * `0b0101101`  - a binary 6-bit pattern
            * `0xAABXX2`   - X designates "don't care" (4-bit-nibbles in hex 
                             patterns)
            * `0b1XX001`   - "don't care" on a bit level in binary patterns
            * `0xAA[8]BB`  - longer "don't care"-sections can be written as
                             a repetition number in square brackets. This example
                             pattern is 48 bits long with 32 don't care bits in 
                             the middle.
            * `0b10[8]00`  - as above but in a binary pattern: 12 bits with 8
                             don't care bits in the middle.
            * `0xAA BB CC` - whitespace will be ignored for pattern check, but
                             plain spaces will be retained in formatted 
                             intermediate values
            * `0xab Ab aB` - patterns are not case sensitive
        
        Usage:
            testresult.append(
                checkBitPattern(
                    value   = io_error_bits, 
                    pattern = "0bxxxx0101",
                    descr   = "Both low side drivers should report errors."
                )
            )
            testresult.append(
                checkBitPattern(
                    io_error_bits, "0b0000xxxx",
                    "Both high side drivers should not report any errors."
                )
            )
        
        Text: Sample Result Output:
            PASSED  Both low side drivers should report errors.
                    Pattern: XXXX0101
                    Value:   10000101 (io_error_bits)
            ----------------------------------------------------------------
            FAILED  Both high side drivers should not report any errors.
                    Pattern: 0000XXXX
                    Value:   10000101 (io_error_bits)
        
        Returns a single [<description>, <verdict>] test result entry.
    """
    return _basic_tests.checkBitPattern(
        value, pattern, 
        descr=descr, format=format
    )
    

# #############################################################################
def checkBit(value, offset, status=1, descr="", format=None): # @ReservedAssignment: format
    """ Check if the bit given by the value and offset is set or cleared 
        depending on the status.
        
        Parameters:
            value     -  Numeric value where the bit has to be checked
            offset    -  Offset of the bit inside of value (based on 0)
            status    -  The expected value of the bit (default 1)
            descr     -  user specific description printed on the start of the 
                         single test result
            format    -  format string to control/override appearance of the 
                         automatically created result text.  
                         A format override should only rarely be used.
        
        Usage: 
            testresult.append(
                checkBit(
                    value  = status_bits,  # 0b00001100
                    offset = 3, 
                    status = 1, 
                    descr = "Bit 3 should be set"
                 )
            )
            testresult.append(
                checkBit(status_bits, 1, 0, descr="Bit 1 should be clear")
            )
        
        Text: Sample Result Output:
            PASSED  Bit 3 should be set
                    Offset: 3
                    Value:  0b00001100 (status_bits)
                    Expected state: 1
                    Detected state: 1
            ----------------------------------------------------------------
            PASSED  Bit 1 should be clear
                    Offset: 1
                    Value:  0b00001100 (status_bits)
                    Expected state: 0
                    Detected state: 0
        
        Returns a single [<description>, <verdict>] test result entry.
    """
    return _basic_tests.checkBit(
        value, offset, status, 
        descr=descr, format=format
    )
    

# #############################################################################
def checkTolerance(current_value, rated_value,
                   rel_pos=0,     abs_pos=0,
                   rel_neg=None,  abs_neg=None, 
                   descr="", format=None   # @ReservedAssignment (format)
    ):
    """ Check if the current value is within a specified range of the rated 
        value. The range is defined by an absolute and a relative tolerance. 
        Both tolerance types will be added to get the effective tolerance. 
        
        Note: 
            If a _symmetric_ tolerance range is desired, only `rel_pos` and/or 
            `abs_pos` need to be set.
        
        Info: Relative Tolerances
            Relative tolerance values are specified as factors in relation to 
            the supplied `rated_value`.  
            A range of `0.0 .. 1.0` maps to `0 .. 100 %` 
        
        Info: Using both relative and absolute tolerances:
            Internally, both tolerances are added to determine the effective
            boundary values:  
            `lower_boundary = abs_neg + rel_neg * abs(rated_value) + rated_value`  
            `upper_boundary = abs_pos + rel_pos * abs(rated_value) + rated_value`  
            
            `current_value` will pass the check if its value lies between the
            calculated boundary values:  
            `lower_boundary <= current_value <= upper_boundary`
        
        Parameters:
            current_value    -   value to be checked
            rated_value      -   expected value
            rel_pos          -   (optional) relative positive tolerance 
                                  as factor, typically in range 0.0..1.0
            abs_pos          -   (optional) absolute positive tolerance
            rel_neg          -   (optional) relative negative tolerance 
                                  as factor, typically in range 0.0..1.0
            abs_neg          -   (optional) absolute negative tolerance
            descr            -   user specific description printed on 
                                 the start of the single test result
            format           -   format string to control/override appearance 
                                 of the automatically created result text.  
                                 A format override should only rarely be used.
        
        Usage: 
            testresult.append(
                checkTolerance(
                    u_supply, 12.0, abs_pos = 0.8, 
                    descr="Check nominal supply voltage level."
                 )
            )
            testresult.append(
                checkTolerance(
                    u_supply, 12.0, abs_pos = 0.2, abs_neg = -0.8,
                    descr="Check with asymmetric abs tolerance values"
                )
            )
            testresult.append(
                checkTolerance(
                    u_supply, 12.0, rel_pos = 0.01,  rel_neg = -0.07,
                    descr="Check with asymmetric rel tolerance values"
                )
            )
        
        Text: Sample Result Output:
            PASSED  Check nominal supply voltage level.
                    Expected value: 12.0 V
                    Current value:  11.3 V (Supply Voltage)
                    Absolute Tolerance:  +/- 0.8 V
            ----------------------------------------------------------------
            PASSED  Check with asymmetric abs tolerance values
                    Expected value: 12.0 V
                    Current value:  11.3 V (Supply Voltage)
                    Absolute Tolerance:  +0.2 V / -0.8 V
            ----------------------------------------------------------------
            PASSED  Check with asymmetric rel tolerance values
                    Expected value: 12.0 V
                    Current value:  11.3 V (Supply Voltage)
                    Relative Tolerance:  +0.01 / -0.07
        
        Returns a single [<description>, <verdict>] test result entry.
    """
    return _basic_tests.checkTolerance(
        current_value, rated_value,
        rel_pos, abs_pos,
        rel_neg, abs_neg,
        descr=descr, format=format
    )
    

# #############################################################################
def checkStatus(current_status, nominal_status, equal=True,
                descr="", format=None):  # @ReservedAssignment (format)
    """ Check if the current status value is identical to the nominal status
        value. Both statuses will be interpreted as int/long values for the
        comparison. 
        
        Note:
            If one or both values cannot be represented as natural numbers, 
            the test will fail with verdicts.ERROR.
        
        Parameters:
            current_status   -   status to be checked
            nominal_status   -   expected status to be checked against 
            equal            -   True to check status for `==`, 
                                 False to check for `!=`
            descr            -   user specific description printed on 
                                 the start of the single test result
            format           -   format string to control the the print out 
                                 of the single test result
        
        Usage: 
            testresult.append(
                checkStatus(
                    status_var, 1,
                    descr="Check that status is 'on'"
                 )
            )
            testresult.append(
                checkStatus(
                    status_var, 3, equal=False,
                    descr="Check that status is not 'disabled'"
                 )
            )
        
        Text: Sample Result Output:
            PASSED  Check that status is 'on'
                    Current status:  1 [on] (some_status_var)
                    Expected status: 1 [on]
            ----------------------------------------------------------------
            PASSED  Check that status is not 'disabled'
                    Current status:  1 [on] (some_status_var)
                    Expected status: != 3 [disabled]
        
        Returns a single [<description>, <verdict>] test result entry.
    """

    return _basic_tests.checkStatus(
        current_status, nominal_status, equal,
        descr=descr, format=format
    )
    

# #############################################################################
def checkRange(value, min_value, max_value, 
               descr="", format=None): # @ReservedAssignment: format
    """ Check if value is in defined range (`min_value <= value <= max_value`).
        
        Parameters:
            value          -  value to be checked
            min_value      -  lower Limit
            max_value      -  upper Limit 
            descr          -  user specific description printed on the start 
                              of the single test result
            format         -  format string to control/override appearance 
                              of the automatically created result text.  
                              A format override should only rarely be used.
        
        Usage: 
            testresult.append(
                checkRange(
                    analog_value, 
                    min_value = 12, 
                    max_value = 54, 
                    descr="Check that value is in range"
                 )
            )
        
        Text: Sample Result Output:
            PASSED  Check that value is in range
                    Value:     42.0 mA (analog_value)
                    Min value: 12 mA
                    Max value: 54 mA
        
        Returns a single [<description>, <verdict>] test result entry.
    """
    return _basic_tests.checkRange(
        value, min_value, max_value, 
        descr=descr, format=format
    )
    

# #############################################################################
def compare(left_value, operator, right_value, abs_tol=0,
            descr="", format=None): # @ReservedAssignment: format
    """ Verify the conditional relationship between two operands based on the 
        given operator.
        
        Parameters:
            left_value  -  left operand of the relational expression
            operator    -  relational operator given as a string, see below
            right_value -  right operand of the relational expression
            abs_tol     -  absolute tolerance for equality/non-equality
                           checks of numeric types
            descr       -  user specific description printed on the start of
                           the single test result
            format      -  format string to control/override appearance 
                           of the automatically created result text.  
                           If a tuple of strings is supplied, it should 
                           contain two (or three) entries:  
                           `(<long_format>, <compact_format>)` or
                           `(<long_format>, <compact_format>, <alias_length_boundary>)`  
                           where alias_length_boundary is the average alias  
                           name length at which to switch to "long" format.  
                           A format override should only rarely be used.
        
        Info: Tolerance
            A a tolerance > 0 is mandatory for equality / non-equality checks 
            involving float values.  
            See checkTolerance() for more in-depth options like relative and 
            non-symmetric tolerances.
        
        Info: Long/Compact Description Formats
            If input values have no overly long aliases, a more compact output 
            format will be used.
            
            Compact format samples:  
              * 1.2 mA (short alias 1) < 2.5 mA (short alias 2)  
              * 1.2 mA (short alias 1) == 2.5 mA (short alias 2) +/- 0.4 mA  
            
            Long format samples:
              * 1.2 mA < 2.5 mA  
                Left Value:  A rather unreasonably long alias name  
                Right Value: Another quite verbose alias name  
              * 1.2 mA == 2.5 mA +/- 0.4 mA  
                Left Value:  A rather unreasonably long alias name  
                Right Value: Another quite verbose alias name  
            
            Default `alias_length_boundary` for switching between formats is 
            32 characters.  
            This value can  be configured in `hil_project.ini`, 
            section `[TestToolkit]` with key/option `alias_length_boundary`.
            
        
        Info: Relational operator strings:
            * "==" : equal to
            * "<"  : less than
            * ">"  : greater than
            * "<=" : less than or equal to
            * ">=" : greater than or equal to
            * "!=" : not equal to
        
        Usage: 
            testresult.append(
                compare(
                    left_value  = analog_value,
                    operator    = "==", 
                    right_value = 42, 
                    abs_tol     = 0.01,
                    descr="Comparing float values for equality requires a defined tolerance"
                 )
            )
            testresult.append(
                compare(
                    status_var, "==", 1,
                    descr = "Comparing integer values"
                 )
            )
            testresult.append(compare(status_var, "<=",         3, descr = "Comparing integer values"))
            testresult.append(compare("Foo",      "==",     "Foo", descr = "Comparing strings"))
            testresult.append(compare([1, 2, 3],  "!=", [2, 3, 4], descr = "Comparing lists"))
        
        Text: Sample Result Output:
            PASSED  Comparing float values for equality requires a defined tolerance
                    42.0 mA (analog_value) == 42.0 mA +/- 0.01 mA
            ----------------------------------------------------------------
            PASSED  Comparing integer values
                    1 [on] (some_status_var) == 1 [on]
            ----------------------------------------------------------------
            PASSED  Comparing integer values
                    1 [on] (some_status_var) <= 3 [disabled]
            ----------------------------------------------------------------
            PASSED  Comparing strings
                    Foo == Foo
            ----------------------------------------------------------------
            PASSED  Comparing lists
                    [1, 2, 3] != [2, 3, 4]
        
        Returns a single [<description>, <verdict>] test result entry.
    """
    return _basic_tests.compare(
        left_value, operator, right_value, abs_tol,
        descr=descr, format=format
    )
    

# #############################################################################
def compareCE(current_value, operator, expected_value, abs_tol=0, descr=""):
    """ Verify the conditional relationship between current and expected value
        based on the given operator.
        
        This is a compare variant with an alternative output formatting to 
        explicitly label input values as "current" and "expected".
        See also basic_tests.compare.
        
        Parameters:
            current_value  - left operand of the relational expression
            operator       - relational operator given as a string, see below
            expected_value - right operand of the relational expression
            abs_tol        - absolute tolerance for equality/non-equality
                             checks of numeric types
            descr          - user specific description printed on the start of
                             the single test result
        
        Info: Tolerance
            A tolerance > 0 is mandatory for equality / non-equality checks 
            involving float values.  
        
        Info: Relational operator strings:
            * "==" : equal to
            * "<"  : less than
            * ">"  : greater than
            * "<=" : less than or equal to
            * ">=" : greater than or equal to
            * "!=" : not equal to
        
        Usage: 
            testresult.append(
                compareCE(
                    current_value  = analog_value,
                    operator       = "==", 
                    expected_value = 42, 
                    abs_tol        = 0.01,
                    descr="Comparing float values for equality requires a defined tolerance"
                 )
            )
            testresult.append(compareCE(status_var, "==",         1, descr="Comparing integer values"))
            testresult.append(compareCE(status_var, "<=",         3, descr="Comparing integer values"))
            testresult.append(compareCE("Foo",      "==",     "Foo", descr="Comparing strings"))
            testresult.append(compareCE([1, 2, 3],  "!=", [2, 3, 4], descr="Comparing lists"))
            
        
        Text: Sample Result Output:
            PASSED  Comparing float values for equality requires a defined tolerance
                    Current:  42.0 mA (analog_value) 
                    Expected: == 42.0 mA +/- 0.01 mA
            ----------------------------------------------------------------
            PASSED  Comparing integer values
                    Current:  1 [on] (some_status_var) 
                    Expected: == 1 [on]
            ----------------------------------------------------------------
            PASSED  Comparing integer values
                    Current:  1 [on] (some_status_var) 
                    Expected: <= 3 [disabled]
            ----------------------------------------------------------------
            PASSED  Comparing strings
                    Current:  Foo 
                    Expected: == Foo
            ----------------------------------------------------------------
            PASSED  Comparing lists
                    Current:  [1, 2, 3] 
                    Expected: != [2, 3, 4]
        
        Returns a single [<description>, <verdict>] test result entry.
    """
    return _basic_tests.compareCE(
        current_value, operator, expected_value, abs_tol,
        descr=descr
    )
    

# #############################################################################
def contains(defined_values, current_value, mode="all", 
            descr="", format=None): # @ReservedAssignment: format
    """ Check if current_value is an element (or sub set) of defined_values.
        
        Examples:
            contains([1,3,5], 3, mode="any")  -> ["...", "PASSED"]
            contains([1,3,5], [3, 45])        -> ["...", "FAILED"]
            contains([1,3,5], 7, mode="none") -> ["...", "PASSED"]
        
        Parameters:
            defined_values -  List of scalars to be searched in
            current_value  -  the function checks if this scalar or list is 
                              contained in 'defined_values'
            mode           -  search mode (see below) 
            descr          -  user specific description printed on the start of
                              the single test result
            format         -  format string to control the the print out of the 
                              single test result.  
                              A format override should only rarely be used.
        
        Info: Available Modes:
            * "all":        each value of 'current_value' should be in `defined_values`
            * "any":        at least one element of 'current_value' should be in `defined_values`
            * "none"/"not": no element of 'current_value' should be in `defined_values`
        
        Usage: 
            testresult.append(
                contains(
                    defined_values = list_value, 
                    current_value = 3,
                    mode = "any",
                    descr = "value has to be present in list"
                 )
            )
            testresult.append( 
                contains(list_value, [1, 9], mode="any", descr="at least one value has to be defined")
            )
            testresult.append( 
                contains(list_value, [3, 5], descr="all values have to be defined")
            )
            testresult.append( 
                contains(list_value, [7, 9], mode="none", descr="none of the values may be contained")
            )
        
        Text: Sample Result Output:
            PASSED  value has to be present in list
                    Defined values: [1, 3, 5]
                    Current value:  3
                    Mode:           any
            ----------------------------------------------------------------
            PASSED  at least one value has to be defined
                    Defined values: [1, 3, 5]
                    Current value:  [1, 9]
                    Mode:           any
            ----------------------------------------------------------------
            PASSED  all values have to be defined
                    Defined values: [1, 3, 5]
                    Current value:  [3, 5]
                    Mode:           all
            ----------------------------------------------------------------
            PASSED  none of the values may be contained
                    Defined values: [1, 3, 5]
                    Current value:  [7, 9]
                    Mode:           none
        
        Returns a single [<description>, <verdict>] test result entry.
    """
    return _basic_tests.contains(
        defined_values, current_value, mode, 
        descr=descr, format=format
    ) 
    

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    from ttk_base.values_base import meta
    print("#" * 80)
    
    testresult = []
    
    
    
    
    # #########################################################################
    # Some Examples
    # 
    status_bits   = meta(0x0C, alias="status_bits", fmt="bin8")
    io_error_bits = meta(0x85, alias="io_error_bits") 
    analog_value  = meta(42.0, alias="analog_value", unit="mA")
    u_supply      = meta(11.3, unit="V", alias="Supply Voltage")
    status_var    = meta(1, alias="some_status_var", 
                         lookup={0: "off", 1: "on", 2: "error", 3: "disabled"})
    list_value    = meta([1, 3, 5], alias="a_list_value", 
                         descr="a value containing a list")
                         
    
    # checkBitMask ############################################################
    testresult.append(["checkBitMask", ""])
    testresult.append(
        checkBitMask(
            value      = status_bits, # 0b00001100
            mask       = 0x0F,
            operator   = "AND",
            bit_length = 8,
            descr      = "Some bits of the lower nibble should be set"
        )
    )
    
    
    # checkBitPattern ############################################################
    testresult.append(["checkBitPattern", ""])
    testresult.append(
        checkBitPattern(
            value   = io_error_bits, 
            pattern = "0bxxxx0101",
            descr   = "Both low side drivers should report errors."
        )
    )
    testresult.append(
        checkBitPattern(
            io_error_bits, "0b0000xxxx",
            "Both high side drivers should not report any errors."
        )
    )
    testresult.append(
        checkBitPattern(
            "foobar", "0b0000xxxx",
            "This should not work and create an error result."
        )
    )
    
    
    # checkBit ################################################################
    testresult.append(["checkBit", ""])
    testresult.append(
        checkBit(
            value  = status_bits,  # 0b00001100
            offset = 3, 
            status = 1, 
            descr = "Bit 3 should be set"
        )
    )
    testresult.append(
        checkBit(status_bits, 1, 0, descr="Bit 1 should be clear")
    )
    
    
    # checkTolerance ##########################################################
    testresult.append(["checkTolerance", ""])
    testresult.append(
        checkTolerance(
            u_supply, 12.0, 
            abs_pos=0.8, descr="Check nominal supply voltage level."
        )
    )
    testresult += [
        checkTolerance(11.3, 12, abs_pos=.8, descr="Check with plain values"),
        checkTolerance(meta(11.3, "V"), meta(12, "V"), abs_pos=.8, descr="Supply voltage check"),
        checkTolerance(meta(12, "V"), meta(12, "mV"), abs_pos=.8,
                       descr="Careful, units will only be added to output text and not\n"
                             "influence the actual test result processing"),
    ]
    
    testresult.append(
        checkTolerance(
            u_supply, 12.0, abs_pos = 0.2, abs_neg = -0.8,
            descr="Check with asymmetric abs tolerance values"
        )
    )
    testresult.append(
        checkTolerance(
            u_supply, 12.0, rel_pos = 0.01,  rel_neg = -0.07,
            descr="Check with asymmetric rel tolerance values"
        )
    )
    
    
    # checkStatus #############################################################
    testresult.append(["checkStatus", ""])
    testresult.append(
        checkStatus(
            status_var, 1,
            descr="Check that status is 'on'"
        )
    )
    testresult.append(
        checkStatus(
            status_var, 3, equal=False,
            descr="Check that status is not 'disabled'"
        )
    )
    
    # checkRange ##############################################################
    testresult.append(["checkRange", ""])
    testresult.append(
        checkRange(
            analog_value, 
            min_value = 12, 
            max_value = 54, 
            descr="Check that value is in range"
        )
    )
    
    # compare #################################################################
    testresult.append(["compare", ""])
    testresult.append(
        compare(
            left_value  = analog_value,
            operator    = "==", 
            right_value = 42, 
            abs_tol     = 0.01,
            descr="Comparing float values for equality requires a defined tolerance"
        )
    )
    testresult.append(
        compare(
            status_var, "==", 1,
            descr = "Comparing integer values"
        )
    )
    testresult.append(compare(status_var, "<=",         3, descr = "Comparing integer values"))
    testresult.append(compare("Foo",      "==",     "Foo", descr = "Comparing strings"))
    testresult.append(compare([1, 2, 3],  "!=", [2, 3, 4], descr = "Comparing lists"))
    
    
    # contains ################################################################
    testresult.append(["contains", ""])
    testresult.append(
        contains(
            defined_values = list_value, 
            current_value = 3,
            mode = "any",
            descr = "value has to be present in list"
        )
    )
    testresult.append( 
        contains(list_value, [1, 9], mode = "any", descr="at least one value has to be defined")
    )
    testresult.append( 
        contains(list_value, [3, 5], descr="all values have to be defined")
    )
    testresult.append( 
        contains(list_value, [7, 9], mode="none", descr="none of the values may be contained")
    )
    
    
    
    # #########################################################################
    # just print test result entries in a somewhat formatted way  
    print("#" * 80)
    for entry in testresult:
        descr, verdict = "\n".join(entry[:-1]), entry[-1].strip()
        if verdict:
            # result entry
            indent = max(8, len(verdict) + 2)
            descr = descr.replace("\n", "\n" + " " * indent)
            print('-' * 64)
            print("%-*s%s"%(indent, verdict, descr))
        else:
            # "header" entry 
            descr = descr.replace("\n", " ")
            print("\n# %s #%s\n"%(descr, "#" * max(0, 80 - len(descr))))
            
            
    
    print("\nDone.")
# @endcond DOXYGEN_IGNORE
# #############################################################################
