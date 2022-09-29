#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : __init__.py
# Package : ttk_daq
# Task    : Package ttk_daq - data acquisition/signal/measurement evaluation \
#           utilities
# Python  : 2.5+
#
# Copyright 2015 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 03.02.2015 | J.Tremmel | initial package (restructured from original daq_utils.py)
# 1.1  | 18.12.2015 | J.Tremmel | 1.0.0 => release
# 1.2  | 25.01.2016 | L.Morgus  | wrapper for _init_
#******************************************************************************
"""
@package ttk_daq
Utilities for data acquisition/signal/measurement evaluation
"""
from _init_ import version
from _init_ import version_info
 
# #############################################################################
if __name__ == "__main__":
    print "# Package ttk_daq, version %s"%(version)