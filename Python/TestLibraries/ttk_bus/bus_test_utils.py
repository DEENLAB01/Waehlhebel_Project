#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : bus_test_utils.py
# Package : ttk_bus
# Task    : Interface to utility functions for bus tests
# Python  : 2.5+
# Type    : Interface
#
# Copyright 2016 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 26.04.2016 | JoTremmel  | initial, refactored from _bus_signals_base
#                                | and existing test utility modules
# 1.1  | 22.12.2016 | JoTremmel  | split into interface and base implementation
#******************************************************************************
"""
@package ttk_bus.bus_test_utils
Interface wrapper for bus test utility functions in ttk_bus._bus_test_utils.
"""
import _bus_test_utils


# #############################################################################
def getIntRangeValues(min_value=None, max_value=None, amount=5):
    """ Get a list of equally distributed (unique) values within min and max 
        value boundaries.
        
        Parameters: 
            min_value - lower boundary of value range 
            max_value - upper boundary of value range 
            amount    - maximum amount of values to be returned (fewer values
                        might be returned if the range cannot fit enough integers)
        
        Returns a list of values equally distributed between min and max
        values.
    """
    return _bus_test_utils.getIntRangeValues(
        min_value = min_value, 
        max_value = max_value, 
        amount    = amount
    )
    

# #############################################################################
def getRangeValues(min_value=None, max_value=None, amount=5):
    """ Get a list of equally distributed values within min and max value
        boundaries.
        
        Parameters: 
            min_value - lower boundary of value range 
            max_value - upper boundary of value range 
            amount    - how many values should be returned  
        
        Returns a list of values equally distributed between min and max
        values. 
    """
    return _bus_test_utils.getRangeValues(
        min_value = min_value, 
        max_value = max_value, 
        amount    = amount
    )
    

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == '__main__': # pragma: no cover (main contains only sample code)
    
    def printRV(minv, maxv, amount):
        values = getRangeValues(minv, maxv, amount)
        print "%2s values between %s and %2s : \t%s"%(
            amount, minv, maxv, values
        )
        
    def printRIV(minv, maxv, amount):
        values = getIntRangeValues(minv, maxv, amount)
        print "%2s (%s unique) int values between %s and %2s : \t%s"%(
            amount, len(values), minv, maxv, values
        )
        
    print "\n", "#" * 80
    print "# getRangeValues:"
    printRV(0, 0, 11)
    printRV(0, 1, 11)
    printRV(0, 2, 11)
    printRV(0, 3, 11)
    printRV(0, -7, 3)
    printRV(2, -7, 3)
    printRV(3, -7, 3)
    
    print "\n", "#" * 80
    print "# getIntRangeValues"
    printRIV(0, 0, 11)
    printRIV(0, 1, 11)
    printRIV(0, 2, 11)
    printRIV(0, 3, 11)
    printRIV(0, -7, 3)
    printRIV(2, -7, 3)
    printRIV(3, -7, 3)



# @endcond DOXYGEN_IGNORE
# #############################################################################    