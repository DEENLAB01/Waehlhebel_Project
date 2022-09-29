#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : __init__.py
# Package : ttk_tools
# Task    : Package ttk_tools - rtp/calibration/... tool access modules
#
# Copyright 2011 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 06.10.2011 | J.Tremmel | initial
# 1.1  | 08.12.2011 | J.Tremmel | added package version info
# 1.2  | 02.01.2012 | J.Tremmel | set version: beta release
# 1.3  | 30.07.2012 | J.Tremmel | => 1.1.0 - updated tools, new offline stubs
# 1.4  | 01.12.2012 | J.Tremmel | => 1.2.0 - added sdmlib-stub, minor tweaks
# 1.5  | 20.02.2013 | J.Tremmel | => 1.3.0 - added license verification
# 1.6  | 10.10.2013 | J.Tremmel | => 1.3.1 - minor bugfixes
# 1.7  | 11.09.2014 | J.Tremmel | => 1.3.2 - updates, GammaAPI (initial) 
# 1.8  | 24.10.2014 | J.Tremmel | => 1.3.3 - raised for release (various updates
#                               | and fixes, GammaV-API official release)
# 1.9  | 18.12.2015 | J.Tremmel | => 1.4.0 - release (various updates)
# 1.10 | 14.03.2015 | J.Tremmel | => 1.4.1 - bugfixes
# 1.11 | 04.04.2016 | L.Morgus  | wrapper for _init_
# 1.12 | 22.12.2016 | J.Tremmel | => 2.0.0 - general refactoring, vendor specific 
#                               | sub-packages, added dSPACE XIL testbench access 
#******************************************************************************
"""
@package ttk_tools
Modules for tool access.
"""
from _init_ import version
from _init_ import version_info
 
# #############################################################################
if __name__ == "__main__":
    print "# Package ttk_tools, version %s"%(version)




