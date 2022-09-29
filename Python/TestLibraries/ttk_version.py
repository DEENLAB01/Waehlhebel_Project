#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : ttk_version.py
# Task    : Version information for TestToolkit releases (i.e. which packages
#           are included in this release)
#
# Author  : J.Tremmel
# Date    : 01.10.2012
# Copyright 2012 - 2013 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 01.10.2012 | J.Tremmel | initial
# 1.1  | 11.02.2013 | J.Tremmel | functionality moved to ttk_base
#******************************************************************************
""" 
Version information for TestTooklkit releases 
"""
# #############################################################################
if __name__ == "__main__":
    import ttk_base
    ttk_base.showReleaseInfo()
    