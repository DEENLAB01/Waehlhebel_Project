#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : sdf_parser.py
# Package : ttk_tools.dspace
# Task    : Parser for System Description Files (.sdf)
#
# Type    : Interface
# Python  : 2.5+
#
# Author  : J. Tremmel
# Date    : 09.12.2008
# Copyright 2008 - 2016 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Author  | Description
#------------------------------------------------------------------------------
# 1.0  | 09.12.2008 | Tremmel | initial
# 1.1  | 26.05.2009 | Tremmel | updated descriptions, added verbosity parameter
#                             | to getInfo()
# 1.2  | 30.06.2009 | Tremmel | added warning_level parameter to getInfo()
# 1.3  | 11.03.2010 | Tremmel | Pylint-cleanup
# 1.4  | 12.12.2011 | Tremmel | added "system type" for ds1006
# 1.5  | 30.03.2012 | Tremmel | added a more direct error message if .sdf file 
#                             | was not found
# 1.6  | 05.06.2012 | Tremmel | moved to package ttk_tools
# 1.7  | 18.12.2015 | Tremmel | split into interface and base implementation
# 1.8  | 08.04.2016 | Tremmel | moved to sub-package ttk_tools.dspace
#******************************************************************************
"""
@package ttk_tools.dspace.sdf_parser
Interface wrapper for System Description Files (.sdf) parser in 
ttk_tools.dspace._sdf_parser.
"""
import _sdf_parser


# #############################################################################
def getInfo(sdf_file, verbosity=2, warning_level=1):
    """ Get information from the supplied System Description File 
        
        Parameters: 
            sdf_file       -  file/path to sdf-file
            verbosity      -  0: no additional info will be displayed  
                              1: also display info summary  
                              2: also display header
            warning_level  -  0: warnings will not be displayed  
                              1: display warnings  
                              2: also display fallback warnings
                              
        Returns a tuple containing (board_name, system type)
    """
    return _sdf_parser.getInfo(
        sdf_file      = sdf_file, 
        verbosity     = verbosity,
        warning_level = warning_level
    )


# #############################################################################
# @cond DOXYGEN_IGNORE
# #############################################################################
if __name__ == "__main__": # pragma: no cover (main contains only sample code)
    import os
    import inspect
    
    # #########################################################################
    script_path = os.path.realpath(inspect.currentframe().f_code.co_filename)
    script_path = os.path.dirname(script_path)
    
    sample_data_path = script_path
    while (os.path.basename(sample_data_path)):
        sample_data_path = os.path.dirname(sample_data_path)
        if os.path.basename(sample_data_path) == 'src':
            sample_data_path = os.path.dirname(sample_data_path)
            sample_data_path = os.path.join(sample_data_path, 'samples')
            break
    # #########################################################################
    
    files = filter(
        lambda n: n.lower().endswith(".sdf"), 
        os.listdir(sample_data_path)
    )
    print
    for file_name in files:
        file_name = os.path.join(sample_data_path, file_name)
        print getInfo(file_name)
        print
    if not files:
        print '> no .sdf files found in samples folder "%s"'%(sample_data_path)

# @endcond DOXYGEN_IGNORE
# #############################################################################        