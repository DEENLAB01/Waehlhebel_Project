#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : __init__.py
# Package : ttk_base
# Task    : Package ttk_base - common functions, base definitions and 
#           abstraction layer for calibrations / real time variables
# Python  : 2
#
# Copyright 2011 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 13.10.2011 | J.Tremmel | initial
# 1.1  | 08.12.2011 | J.Tremmel | added package version info
# 1.2  | 02.01.2012 | J.Tremmel | set version: beta release
# 1.3  | 30.07.2012 | J.Tremmml | => 1.1.0 - updates, added values_base
# 1.4  | 01.10.2012 | J.Tremmml | => 1.2.0 - updates, added Snapshot
# 1.5  | 06.02.2013 | J.Tremmel | added package path
# 1.6  | 11.02.2013 | J.Tremmel | merged functionality from ttk_version;
#                               | TTk release now follows version of ttk_base
# 1.7  | 20.02.2013 | J.Tremmel | => 1.3.0
# 1.8  | 08.05.2013 | J.Tremmel | => 1.3.1
# 1.9  | 10.10.2013 | J.Tremmel | => 1.3.2 beta
# 1.10 | 31.07.2014 | J.Tremmel | => 1.3.3 intermediate build
# 1.11 | 11.09.2014 | J.Tremmel | => 1.3.4 rc2 (intermediate release before 1.4.0)
# 1.12 | 24.09.2014 | J.Tremmel | => 1.3.4 rc3 (intermediate release before 1.4.0)
# 1.13 | 24.10.2014 | J.Tremmel | => 1.3.4 rc4 (yet another intermediate release before 1.4.0)
#                               | => 1.3.4 final
# 1.14 | 18.12.2015 | J.Tremmel | => 1.4.0
# 1.15 | 14.03.2016 | J.Tremmel | => 1.4.1 (additional class-config for ttk_bus)
# 1.16 | 18.03.2016 | J.Tremmel | => 1.4.2 (additional bugfixes)
# 1.17 | 04.04.2016 | L.Morgus  | wrapper for _init_
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 2.0  | 22.12.2016 | J.Tremmel | => 2.0.0
# 2.1  | 15.07.2020 | J.Tremmel | 2.1.0
#******************************************************************************
from _init_ import version
from _init_ import version_info
from _init_ import showReleaseInfo
from _init_ import _package_path

# #############################################################################
if __name__ == "__main__":
    print "package path: %s"%(_package_path)
    showReleaseInfo()