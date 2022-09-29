#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : __init__.py
# Package : ttk_checks
# Task    : Package ttk_checks - check and test utility functions
# Python  : 2
#
# Copyright 2011 - 2016 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 15.07.2011 | J.Tremmel | initial
# 1.1  | 02.01.2012 | J.Tremmel | set version: beta release
# 1.2  | 30.07.2012 | J.Tremmel | => 1.1.0 - interface wrappers
# 1.3  | 01.12.2012 | J.Tremmel | => 1.2.0 - bugfixes, better output formatting,
#                               |            added convenience functions
# 1.4  | 20.02.2013 | J.Tremmel | => 1.3.0 - fixes for review findings, 
#                               |            added license verification 
# 1.5  | 11.10.2013 | J.Tremmel | => 1.3.1 - minor fixes and enhancements
# 1.6  | 01.08.2014 | J.Tremmel | => 1.3.2 - updates and fixes
# 1.7  | 24.10.2014 | J.Tremmel | => 1.3.3 - raised for release (various updates and fixes)
# 1.8  | 18.12.2015 | J.Tremmel | 1.4.0 - adv_tests
# 1.9  | 14.03.2016 | J.Tremmel | 1.4.1 - better unicode handling in checkutils
# 1.10 | 18.03.2016 | J.Tremmel | 1.4.2 - more bugfixes for string decoding issues
# 1.11 | 04.04.2016 | L.Morgus  | wrapper for _init_
#******************************************************************************
"""
@package ttk_checks
Check and test utility functions
"""
from _init_ import version
from _init_ import version_info
 
# #############################################################################
if __name__ == "__main__":
    print "# Package ttk_checks, version %s"%(version)
