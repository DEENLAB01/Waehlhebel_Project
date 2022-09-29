#******************************************************************************
# -*- coding: latin-1 -*-
# File    : errors.py
# Package : ttk_base
# Task    : Base classes and definitions for TestToolkit exceptions/errors
#
# Type    : Implementation
# Python  : 2.5+
#
# Author  : J.Tremmel 
# Date    : 09.08.2013
# Copyright 2013 - 2016 iSyst Intelligente Systeme GmbH
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Author  | Description
#------------------------------------------------------------------------------
# 1.0  | 09.08.2013 | Tremmel | initial
# 1.1  | 18.01.2016 | Tremmel | tweaked sample code in __main__ 
#******************************************************************************
"""
@package ttk_base.errors
Base classes and definitions for TestToolkit exceptions/errors.
"""


# #############################################################################
class TTkErrorString(str):
    """ A wrapper for error message strings so they can be distinguished
        from "normal" string values (like contents of ASCII-type variables
        in the case of calibration devices)
    """
    

# #############################################################################
class TTkException(Exception):
    """ Base Exception for TestToolkit packages. """
    

# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__":  # pragma: no cover (main contains only sample code)
    es = TTkErrorString("TTkErrorString")
    s = "Normal String "
    print "%-14s --> str-instance: %s, TTkErrorString-instance: %s"%(
        es, isinstance(es, str), isinstance(es, TTkErrorString)
    )
    print "%-14s --> str-instance: %s, TTkErrorString-instance: %s"%(
        s,  isinstance(s, str),  isinstance(s, TTkErrorString)
    )
    print "# A TTkException:"
    raise TTkException("This is a TTkException")

# @endcond DOXYGEN_IGNORE #####################################################
