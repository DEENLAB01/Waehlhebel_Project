#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : __init__.py
# Package : ttk_bus
# Task    : Package ttk_bus - test functions for bus/interface tests.
# Python  : 2.5+
#
# Copyright 2012 - 2016 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 26.06.2012 | J.Tremmel | initial
# 1.1  | 10.10.2012 | J.Tremmel | 1.1.0 Beta (l10n update, testSignals)
# 1.2  | 20.02.2013 | J.Tremmel | 1.2.0 - added license verification
# 1.3  | 08.05.2013 | J.Tremmel | 1.3.0 Beta
# 1.4  | 10.10.2013 | J.Tremmel | 1.3.1
# 1.5  | 11.09.2014 | J.Tremmel | 1.3.2 updates and fixes
# 1.6  | 24.10.2014 | J.Tremmel | 1.3.3 cleanup in bus_signals modules
# 1.7  | 18.12.2015 | J.Tremmel | 1.4.0 - interfaces for bus_signals_*, updates and fixes
# 1.8  | 11.03.2016 | J.Tremmel | 1.4.1 - updates and fixes (class config)
# 1.9  | 18.03.2016 | J.Tremmel | 1.4.2 - more bugfixes
# 1.10 | 04.04.2016 | L.Morgus  | wrapper for _init_
#******************************************************************************
"""
@package ttk_bus
Test functions for bus/interface tests and abstraction layer for "bus signals".
"""
from _init_ import version
from _init_ import version_info

# #############################################################################
if __name__ == "__main__":
    print "# Package ttk_bus, version %s"%(version)