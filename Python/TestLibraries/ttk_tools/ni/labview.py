#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : labview.py
# Package : ttk_tools.ni
# Task    : Access to LabView via COM server
# Type    : Interface
# Python  : 2.5+
#
# Copyright 2019, 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 18.12.2019 | J.Tremmel | initial
# 1.1  | 03.06.2020 | J.Tremmel | fixed bad char escape in docstring sample paths
#******************************************************************************
""" 
@package ttk_tools.ni.labview
Interface wrapper for LabView VI COM access in ttk_tools.ni._labview

This module serves as "interface" to the precompiled module in delivery to 
enable code-completion in PyDev.
"""
from ttk_tools.ni import _labview


# #############################################################################
class LabView(_labview.LabView):
    """ Access to LabView VI controls/variables via COM interface.  
        
        Note:
            The LabView App needs to be build with COM/ActiveX server support 
            (and registered as a COM server) to enable remote access.
    """
    
    # #########################################################################
    def __init__(self, com_obj_name, base_path):
        """ Parameters:
                com_obj_name  - name of the COM server application object, 
                                e.g. "FooApp1.Application"
                base_path     - base path to LabView-compiled COM server executable,
                                e.g. 'C:/utilities/Foo_Ver1__By_Labview/Foo.exe'
        """
        _labview.LabView.__init__(
            self, com_obj_name=com_obj_name, base_path=base_path
        )
    
    # #########################################################################
    def close(self):
        """ Close/quit current LabView connection. """
        _labview.LabView.close(self)
        
    # #########################################################################
    def getVi(self, vi_name):
        """ Get a reference to the named virtual instrument.
            Parameter:
                vi_name - name of VI to get
            Returns a COM reference to the VI.
        """
        return _labview.LabView.getVi(self, vi_name)
    
    # #########################################################################
    def getViVar(self, identifier):
        """ Get current value of a VI's variable/control.
            Parameter:
                identifier - identifier of variable with prefixed VI name, 
                             separated by a slash e.g. "Bar.vi/variable_name"
            Returns the current value 
        """
        return _labview.LabView.getViVar(self, identifier)
    
    # #########################################################################
    def setViVar(self, identifier, value):
        """ Set value to a VI's variable/control.
            Parameter:
                identifier - identifier of variable with prefixed VI name, 
                             separated by a slash e.g. "Bar.vi/variable_name"
                value      - value to set
        """
        return _labview.LabView.setViVar(
            self, identifier=identifier, value=value
        )
        

# #############################################################################
# @cond DOXYGEN_IGNORE 
# #############################################################################
if __name__ == '__main__':  # pragma: no cover (contains only sample code)
    
    print("Done")
    
# @endcond DOXYGEN_IGNORE
# #############################################################################
