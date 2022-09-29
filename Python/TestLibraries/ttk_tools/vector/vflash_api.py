#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : vflash_api.py
# Package : ttk_tools.vector
# Task    : Access to vFlash API functions.
# Type    : Interface
# Python  : 2.5+
#
# Copyright 2017 - 2020 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.1  | 05.05.2017 | P. Wunner  | initial 
#                                  takeover from vflash_api Christian Orth
# 1.2  | 09.05.2018 | J.Tremmel  | minor refactoring and cleanup
# 1.3  | 20.04.2020 | J.Tremmel  | removed obsolete MAX_LEN_ERROR_TEXT import
# 1.5  | 28.04.2020 | J.Tremmel  | updated to match _vflash_api v1.5
#                                | (vFlash DLL detection from system PATH )
#******************************************************************************
""" 
@package ttk_tools.vector.vflash_api
Interface to vFlash API function access in  ttk_tools.vector._vflash_api
"""

# Defines / Constants / Defaults ##############################################
from vflash_api_common import FLASH_TIMEOUT
from vflash_api_common import VFlashStatus       # @UnusedImport
from vflash_api_common import VFlashResult       # @UnusedImport

# Error handling ##############################################################
from vflash_api_common import VFlashError        # @UnusedImport
from vflash_api_common import VFlashResultError  # @UnusedImport
from vflash_api_common import VFlashDLLError     # @UnusedImport

# vflash_api Application Class ################################################
import _vflash_api


# #############################################################################
# Connection to vFlashAPI
# #############################################################################
class VFlashAPI(_vflash_api.VFlashAPI):
    ''' Python Wrapper for accessing vFlash API functions. '''
    
    # #########################################################################
    def __init__(self, dll_path=None):
        """ Parameters:
                dll_path  - Path to vFlash C-API DLL file.  
                            None: Detect suitable DLL from system PATH
            
            Note: DLL 
                Use path to "VFlashAutomation.dll" for 32-bit Python 
                and path to "VFlashAutomation64.dll" for 64-bit Python.  
                
                Both DLLs should be available in the "Bin/" sub folder of the 
                vFlash installation (or alternatively in the "Bin/Automation/" 
                sub folder)
                
                If `dll_path` is set to a folder path, VFlashAPI will try to 
                load a suitable DLL from this folder.
                
                If `dll_path` is None, VFlashAPI will try to locate a suitable 
                DLL from system PATH entries (default vFlash installer adds
                the vFlash Bin/Automation/ folder to PATH)
            
            Usage:
                # with DLL auto-detect:
                vflash_api = VFlashAPI()
        """
        _vflash_api.VFlashAPI.__init__(self, dll_path)
    
    # #########################################################################
    def flash(self, flash_file, testresult=None, activate_network=False, 
                    flash_timeout=FLASH_TIMEOUT):
        """ Start flashing the software with vFlash C-API,
            
            Info: Steps of the state machine:
                1 - vFlash Initialization
                2 - Load Project
                3 - Activate Network (optional), 
                    availability depends on DLL version
                4 - Flash software
                5 - Unload Project
                6 - Deinitialize vFlash Library
            
            Parameters:
                flash_file       - Path to the flash file
                testresult       - List where all the testresults are stored
                activate_network - Only necessary when an active FlexRay node
                                   should be simulated. Available since 
                                   vFlash version 2.5
                flash_timeout    - Timeout of flash procedure in seconds
                                   standard: 1000 seconds, see FLASH_TIMEOUT
            
            Example:
                flash(
                    flash_file = r'D:\Hil_Projekte\flashfile.odx',
                    testresult = testresult,
                    activate_network = False
                )
            
            Returns a testresult list
        """
        return _vflash_api.VFlashAPI.flash(
            self, 
            flash_file = flash_file, 
            testresult = testresult, 
            activate_network = activate_network,
            flash_timeout = flash_timeout
        )
        

# #############################################################################
# @cond DOXYGEN_IGNORE 
# #############################################################################
if __name__ == '__main__':  # pragma: no cover (contains only sample code)
    import os
    import time
    from xml.dom.minidom import parse
    
    #odx_file_path    = r'C:\Users\s-nu-chs-hil\Downloads\HIL_0815\Flashcontainer\FL_11223344_V0815_E.odx'
    flash_file_path  = r"D:\temp\sw_0815_vFlash\Project1.vflash"
    #vflash_dll_path  = r'C:\Program Files (x86)\Vector vFlash 3.1\Bin\VFlashAutomation.dll'
    #vflash_dll_path  = r'C:\Program Files (x86)\Vector vFlash 5\Bin\VFlashAutomation.dll'
    vflash_dll_path  = None # use auto-detect from PATH
    activate_network = False
    flash_timeout    = 2000
    
    # TODO: Should this remain here as example? 
    #       Maybe move to vflash_api_common -JT 2018-05-09
    def updateVFlashFile(vflash_file_path, odx_file_path):
        """ Update vflash_file_path with path to odx container """
        os.chmod(vflash_file_path, 0777)
        dom = parse(vflash_file_path)
        node = dom.getElementsByTagName("ODXFFlashData")[0]
        node = node.getElementsByTagName("FilePath")[0] # select first description tag
        
        if node.getAttribute('RelativePath'):
            print node.getAttribute('RelativePath')
            # FIXME: relative path should probably be relative to vflash_file_path,
            #        and not just the base file name
            #        => Python 2-6+ we could simply use os.path.relpath(path, start_path)
            node.setAttribute('RelativePath', os.path.basename(odx_file_path))
            print node.getAttribute('RelativePath')
            
        if node.getAttribute('AbsolutePath'):
            print node.getAttribute('AbsolutePath')
            node.setAttribute('AbsolutePath', odx_file_path)
            print node.getAttribute('AbsolutePath')
        
        f = open(vflash_file_path, "wb")
        f.write(dom.toxml())
        f.close()
    
    # #########################################################################
    # flash with log output on console
    # #########################################################################
    print "[start] vFlash Automation [timestamp: %s]"%(time.ctime())
    #updateVFlashFile(flash_file_path, odx_file_path)
    
    vf = VFlashAPI(vflash_dll_path)
    
    print "# vFlash Automation: "
    print "    vflash dll path: %s"%(vf.dll_path)
    print "    flash file path: %s"%(flash_file_path)
    
    
    testresult = []  # initial, empty result list
    print "# vFlash Automation: Flash Progress:"
    try:
        vf.flash(flash_file_path, testresult, activate_network, flash_timeout)
    except VFlashResultError, ex:
        testresult.append(["%s"%ex, "FAILED"])
    except Exception, ex:
        testresult.append(["%s: %s"%(type(ex).__name__, ex), "ERROR"])
    
    print "# vFlash Automation: Flash Result (Summary):"
    for item, verdict in testresult:
        print "%-72s | %s"%(item, verdict)
        
    print "[done] vFlash Automation [timestamp: %s]"%(time.ctime())
    
    
# @endcond DOXYGEN_IGNORE
# #############################################################################
