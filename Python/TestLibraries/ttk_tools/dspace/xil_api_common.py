#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : xil_api_common.py
# Package : ttk_tools.dspace
# Task    : Common shared definitions and error classes for xil_api
#
# Type    : Implementation
# Python  : 2.7 (but 2.5 compatible)
#
# Copyright 2016 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 18.10.2016 | J.Tremmel  | initial, refactored error classes
# 1.1  | 21.12.2016 | J.Tremmel  | moved writeMAPortConfigXML here 
# 1.6  | 02.02.2018 | J.Tremmel  | added Python 2.5 compatibility tweaks
# 1.7  | 22.06.2020 | J.Tremmel  | updated writeMAPortConfigXML examples
#******************************************************************************
"""
@package ttk_tools.dspace.xil_api_common
Common shared definitions and error classes for xil_api.

Note:
    All relevant "constants"/definitions will be imported from their .NET 
    implementation, so there's not much here besides shared exception classes.
    
"""
from __future__ import with_statement # Python 2.5 compatibility
import os
import codecs
from ttk_base.errors import TTkException


# #############################################################################
class TestbenchError(TTkException):
    """ Base class for "other" testbench errors that are not handled
        by XIL TestbenchPortExceptions
    """
    def __init__(self, msg, source=None, orig_exception=None):
        TTkException.__init__(self, msg)
        self.source         = source
        self.orig_exception = orig_exception
        

# #############################################################################
class StimulusError(TestbenchError):
    """ Errors during Stimulus setup/execution."""
    

# #############################################################################
def writeMAPortConfigXML(sdf_file_path, platform_name="DS1006", xml_file_path=None):
    """ Write a simple MAPort XML configuration file for dSPACE implementations
        to the specified path.
        
        Parameters:
            sdf_file_path  -  path to system description file (*.sdf).  
                              Note that this file does not have to exist to 
                              write the XML 
            platform_name  -  name of target platform hardware
            xml_file_path  -  file path to write configuration to.  
                              If None, a default file named "MAPortConfig.xml" 
                              will be created in same folder as the SDF-file.
        Note:
            `sdf_file_path` can be specified as an absolute path or as relative 
            to the location of the XML file (i.e. `xml_file_path`).
        
        Example:
            writeMAPortConfigXML(
                sdf_file_path = r"D:\HIL-Projekte\Demo\Modell\demo.sdf",
                platform_name = "DS1006"
            )
            # => configuration will be written to 
            # D:\HIL-Projekte\Demo\Modell\MAPortConfig.xml
        
        Example:
            maport_config_path = os.path.join(
                _base_project_path, "ControlDesk", "MAPortConfig.xml"
            )
            sdf_file_path = os.path.join(
                # "scalexio" is the project folder below <hil_project>/ControlDesk/
                "scalexio", "Variable Descriptions", 
                "Inbetriebnahme.sdf", "Inbetriebnahme.sdf" # yep, folder and file are named the same
            )
            xil_api_common.writeMAPortConfigXML(
                sdf_file_path = sdf_file_path, # a relative path
                platform_name = "SCALEXIO",    # see platform properties in ControlDesk
                xml_file_path = maport_config_path
            )
            
        
        Returns the path to the written MAPort configuration file.
    """
    sdf_file_path = os.path.normpath(os.path.abspath(sdf_file_path))
    if xml_file_path is None:
        xml_file_path = os.path.join(
            os.path.dirname(sdf_file_path), "MAPortConfig.xml"
        )
    
    def escape(s):
        # just in case: escape "special" XML characters
        return s.replace("&", "&amp;") \
                .replace("<", "&lt;")  \
                .replace(">", "&gt;")
    
    xml = u"""<?xml version="1.0" encoding="utf-8"?>
<PortConfigurations>
    <MAPortConfig>
        <PlatformName>%(platform_name)s</PlatformName>
        <SystemDescriptionFile>%(sdf_file_path)s</SystemDescriptionFile>
    </MAPortConfig>
</PortConfigurations>
"""%{
        u"platform_name": escape(platform_name.strip()),
        u"sdf_file_path": escape(sdf_file_path)
    }
    with codecs.open(xml_file_path, "wb", encoding="utf-8") as fh:
        fh.write(xml)
    
    return xml_file_path
    

# #############################################################################
# @cond DOXYGEN_IGNORE 
# #############################################################################
if __name__ == '__main__':  # pragma: no cover (contains only sample code)
    import tempfile
    
    xml_path = writeMAPortConfigXML(
        sdf_file_path = os.path.join(tempfile.gettempdir(), "demo.sdf"),
        platform_name = "DS1006"
    )
    print "#", xml_path
    print "--8<%s"%("-" * 76)
    with codecs.open(xml_path, "r", encoding="utf-8") as f:
        print(f.read())
    print "%s>8--"%("-" * 76)
    
# @endcond DOXYGEN_IGNORE
# #############################################################################
