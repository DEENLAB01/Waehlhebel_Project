#******************************************************************************
# -*- coding: latin1 -*-
#
# File    : basic_checks.py
# Package : ttk_checks
# Task    : Wrapper for basic low-level check functions for use in test 
#           automation.
#           This serves as "interface" to the precompiled module in delivery 
#           to enable code-completion in PyDev
# Type    : Base Implementation
# Python  : 2.5+
#
# Copyright 2012 - 2014 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date       | Author  | Description
#------------------------------------------------------------------------------
# 1.0  | 22.05.2012 | Tremmel | initial
# 1.1  | 20.02.2013 | Tremmel | fixes for review findings 
# 1.2  | 31.07.2014 | Tremmel | added abs_tol support to compare() (for numeric values)
#******************************************************************************
""" 
@package ttk_checks.basic_checks

Interface wrapper for basic check functions ("low-level") in ttk_checks._basic_checks.
This serves as "interface" to the precompiled module in delivery to enable 
code-completion in PyDev.

Example:
    status, info = checkBitPattern(0x85, '0bxxxx0101')

Conventions:
    Each function will return a tuple with two values:  
    * `status` - result check status, True/False.  
                 - Typically, True means that the check was successfully passed.  
                 - See individual function descriptions for details  
    * `info`  -  a dictionary with intermediate values calculated for the check,
                 e.g. effective min/max boundaries calculated from relative and 
                 absolute tolerances. 
                 - Key names of intermediate values follow the variable naming 
                   schema from our Python Style Guide 
                 - See https://wiki.isyst.de/wiki/Python_Styleguide).
    
    Intermediate values could be used to augment test result descriptions or 
    for additional processing.  
    See individual function descriptions for details.
    
    Check functions will only raise exceptions derived from the base class
    BasicCheckException (see module ttk_checks.checkceptions) for input value 
    check and processing errors.  
    Unless something goes completely wrong, no other exceptions should get raised.  
    
    If a check function raises an (unexpected) exception anyway, please file 
    a bug report: http://trac.isyst.de/iTestStudio/newticket
    or contact support at support.iteststudio@isyst.de
    
"""
import _basic_checks
from _basic_checks import CHECKBITMASK_DEFAULT_BIT_LENGTH #
from _basic_checks import CHECKBITMASK_MAX_BIT_LENGTH     # @UnusedImport 

# just to make them available
from _basic_checks import CONTAIN_MODES     # @UnusedImport 
from _basic_checks import COMPARE_OPERATORS # @UnusedImport 


# #############################################################################
def checkBit(value, offset, status=1):
    """ Check if the bit given by the value and offset is set or cleared 
        depending on the status.
        
        Parameters:
            value       -  Numeric value where the bit has to be checked
            offset      -  Offset of the bit inside of value (based on 0)
            status      -  The expected value of the bit (default 1)
        
        Returns a tuple (status, dictionary with intermediate values)  
            `status`              - True if the selected bit has the desired
                                    status, otherwise False.  
            `intermediate_values` - a dictionary with  
                'called_function'      : name of this function in string format  
                'value'                : input value  
                'offset'               : input bit offset  
                'bit_status_detected'  : actual bit status  
                'bit_status_expected'  : expected bit status (from input)  
    """
    return _basic_checks.checkBit(value, offset, status)
    

# #############################################################################
def checkBitMask(value, mask, operator="AND", 
                 bit_length=CHECKBITMASK_DEFAULT_BIT_LENGTH ):
    """ Check if the result of the operation given in 'operator' is 'greater 0'
        or 'equal 0'. The result is calculated with a dyadic operation. The 
        two operands are 'value' and 'mask'.
        
        Parameters:
            value       -   value to be checked (int/long)
            mask        -   mask to be used for operation in operator (long or string)
            operator    -   operator for check operation, one of 
                            ("AND", "OR", "XOR", "NAND", "NOR", "NXOR")
            bit_length  -   bit length for value and mask
        
        Returns a tuple (status, dictionary with intermediate values)  
            `status`               - True if result of operation is 'greater 0',
                                     False if it is 'equal 0'  
            `intermediate_values`  - a dictionary with  
                'result_string'    : result of operation in binary string format  
                'result_value'     : result of operation as long value  
                'source_value'     : input value  
                'source_mask'      : input mask  
                'source_operator'  : input operator  
                'source_bit_length': input bit length  
                'result_verdict'   : True if result value > 0  
                'called_function'  : name of this check function (as string)  
    """
    return _basic_checks.checkBitMask(value, mask, operator, bit_length)
    

# ############################################################################
def checkBitPattern(value, pattern):
    """ Check that a numeric value matches a certain pattern.
        
        Parameters:
            value     - value to check. The value must match the full pattern 
                        in order to pass. Values may be numeric (int/long),
                        string representations of binary/hexadecimal values 
                        ("0xABCD", "0b1010" etc.) or a list of bytes.
            
            pattern   - a string describing the desired bit pattern.  
                        Note that a pattern must always describe the full 
                        value (i.e. all bits from start to end). 
                         * A pattern starting with "0x" will be interpreted as 
                           hexadecimal 
                         * "0b" at the beginning denotes a binary pattern 
                         * "X" marks "don't care" sections (anywhere in pattern)
                        
                        See examples for further details.
        
        Examples: 
            "0xABC123"   - a hexadecimal 20-bit pattern
            "123ABC"     - without a prefix, pattern defaults to hexadecimal
            "0b0101101"  - a binary 6-bit pattern
            "0xAABXX2"   - X designates "don't care" (4-bit-nibbles in hex 
                           patterns)
            "0b1XX001"   - "don't care" on a bit level in binary patterns
            "0xAA[8]BB"  - longer "don't care"-sections can be written as
                           a repetition number in square brackets. This example
                           pattern is 48 bits long with 32 don't care bits in 
                           the middle.
            "0b10[8]00"  - as above but in a binary pattern: 12 bits with 8
                           don't care bits in the middle.
            "0xAA BB CC" - whitespace will be ignored for pattern check, but
                           plain spaces will be retained in formatted 
                           intermediate values
            "0xab Ab aB" - patterns are not case sensitive
            
        
        Returns a tuple (status, dictionary with intermediate values)  
            `status`              - True if pattern matches, otherwise False  
            `intermediate_values` - a dictionary with  
                'condensed_value'  :  value w/o whitespace formatting  
                'condensed_pattern':  pattern w/o whitespace formatting  
                'formatted_value'  :  value with whitespace formatted like pattern  
                'formatted_pattern':  pattern with whitespace formatting  
                'mismatch_position':  position where first mismatch occurred
                                      (from condensed_pattern), -1 if pattern 
                                      matches.  
                'called_function'  :  name of this check function (as string)
    """
    return _basic_checks.checkBitPattern(value, pattern)
    

# #############################################################################
def checkRange(value, min_value, max_value):
    """ Checks if value is in defined range (min_value <= value <= max_value).
        
        Parameters:
            value             -  value to be checked (int/long/float)
            min_value         -  lower limit
            max_value         -  upper limit
        
        Examples:
            checkRange([0x2,-5.0, 7L])     -> True
            checkRange([0x2,7L, 5.0])      -> True
            checkRange([5, 7, 9])          -> False
            checkRange([2,"a", 7])         -> raises an exception
        
        Returns a tuple (status, dictionary with intermediate values)  
            `status`               - True or False if value is in defined range  
            `intermediate_values`  - a dictionary with  
                'value'              : input value that has been checked  
                'min_value'          : lower Limit  
                'max_value'          : upper limit  
                'called_function'    : name of this function in string format  
    """
    return _basic_checks.checkRange(value, min_value, max_value)
    

# #############################################################################
def checkTolerance(current_value, rated_value,
                   rel_pos=0,    abs_pos=0,
                   rel_neg=None, abs_neg=None
    ):
    """ Check if the current value is within a specified range of the rated 
        value. The range is defined by an absolute and a relative tolerance. 
        Both abs and rel tolerances will be added. 
        
        Note: 
            If a _symmetric_ tolerance range is desired, only `rel_pos` and/or 
            `abs_pos` need to be set.
        
        Info: Relative Tolerances
            Relative tolerance values are specified as factors in relation to 
            the supplied `rated_value`.  
            A range of `0.0 .. 1.0` maps to `0 .. 100 %` 
        
        Parameters:
            current_value    -   value to be checked
            rated_value      -   expected value
            rel_pos          -   (optional) relative positive tolerance 
                                  as factor, typically in range 0.0..1.0
            abs_pos          -   (optional) absolute positive tolerance
            rel_neg          -   (optional) relative negative tolerance 
                                  as factor, typically in range 0.0..1.0
            abs_neg          -   (optional) absolute negative tolerance
        
        Returns:
            a tuple (status, dictionary with intermediate values)  
                `status`                - True if value is within tolerance, otherwise False  
                `intermediate_values`   - a dictionary with  
                    'current_value'    : value to be checked  
                    'rated_value'      : expected value to be checked against  
                    'rel_pos'          : actual relative positive tolerance  
                    'abs_pos'          : actual absolute positive tolerance  
                    'rel_neg'          : actual relative negative tolerance  
                    'abs_neg':         : actual absolute negative tolerance  
                    'lower_boundary'    : calculated lower boundary (from tolerances)  
                    'upper_boundary'    : calculated upper boundary (from tolerances)  
                    'effective_abs_pos' : effective positive tolerance, absolute (based on both abs and rel pos)  
                    'effective_abs_neg' : effective negative tolerance, absolute (based on both abs and rel neg)  
                    'called_function'   : name of this check function (as string)  
    """
    return _basic_checks.checkTolerance(
        current_value, rated_value,
        rel_pos, abs_pos,
        rel_neg, abs_neg,
    )
    

# #############################################################################
def contains(defined_values, current_value, mode="all"):
    """ Checks if current_value is an element or sub-set of defined_values.
        The order of elements is not important.
        
        Note:
            While it is possible to compare lists of float values, it might 
            lead to unexpected results due to rounding errors. 
        
        Parameters:
            defined_values -  list of scalars to be searched in
            current_value  -  function checks if this scalar (or list) is 
                              contained in 'defined_values'
            mode           -  search mode (one of 'all', 'any', 'none', 'not',
                              see CONTAIN_MODES)
        
        Examples:
            contains([1,3,5], 3, mode="any")       -> True
            contains([1,3,5], 7, mode="none")      -> True
            contains([1,3,5], [3, 45], mode="all") -> False
            contains([1,3,5], [3, 45], mode="any") -> True
            contains([1,3,5], [3, 45], mode="not") -> False
            contains([1,3,5], [3, 5],  mode="all") -> True
        
        Info: Available Modes:
            * "all":         each value of 'current_value' should be in `defined_values`
            * "any":         at least one element of 'current_value' should be in `defined_values`
            * "none"/"not":  no element of 'current_value' should be in `defined_values`
        
        Returns a tuple (status, dictionary with intermediate values)  
            `status`              - True or False if current_value is an element 
                                    of defined_values, depending on mode  
            `intermediate_values` - a dictionary with  
                'in_list'         : List of all elements of current_value that are in defined_values.  
                'not_in_list'     : List of all elements of current_value that are not in defined_values.  
                'current_value'   : value(s) that have been checked  
                'defined_values'  : values that have been checked against  
                'mode'            : check mode  
    
    """
    return _basic_checks.contains(defined_values, current_value, mode)
    

# #############################################################################
def compare(left_value, operator, right_value, abs_tol=0):
    """ Verify the conditional relationship between two operands based on 
        the given operator.
        
        Parameters:
            left_value  -  left operand of the relational expression
            operator    -  the relational operator given as a string
                           (one of "=", "==", "<", ">", "<=", ">=", "!=", "<>")
            right_value -  right operand of the relational expression
            abs_tol     -  absolute tolerance for use in equality/non-equality
                           checks of numeric types
        
        Note:
            A tolerance > 0 is mandatory for equality checks (==, !=) involving 
            float values.  
            See checkTolerance() for more in-depth options like relative and 
            non-symmetric tolerances.
        
        Info:
            When comparing lists, they must contain the same number of elements 
            or a BasicCheckException will be raised.  
            List compare currently only supports `==` and `!=` operators, 
            as the behavior for other operations is unspecified.
        
        Info: Relational operator strings:
            * "="  : equal to
            * "==" : equal to
            * "<"  : less than
            * ">"  : greater than
            * "<=" : less than or equal to
            * ">=" : greater than or equal to
            * "!=" : not equal to
            * "<>" : not equal to
        
        Returns a tuple (status, dictionary with intermediate values)  
            `status`               - True if expression evaluates to True,
                                     otherwise False  
            `intermediate_values`  - a dictionary with  
                'left_value'       : left value of expression  
                'right_value'      : right value of expression  
                'operator'         : used operator  
                'abs_tol'          : tolerance (absolute, for numeric checks)  
                'compare_mode'     : kind of comparison that was performed (numeric, string, list, other)  
                'called_function'  : name of this check function (as string)  
    """
    return _basic_checks.compare(left_value, operator, right_value, abs_tol)
    

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    status, info = checkBitPattern(0x85, '0bxxxx 01 01')
    print "Status:", status
    print "Intermediate Values:"
    for key, value in info.iteritems():
        print "  %-20s: %s"%(key, value)
# @endcond DOXYGEN_IGNORE
# #############################################################################
