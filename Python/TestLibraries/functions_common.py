# *****************************************************************************
# -*- coding: latin-1 -*-
# File    : functions_common.py
# Task    : functions for different use cases
#
# Author  : An3Neumann
# Date    : 18.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# *****************************************************************************
# ********************************* Version ***********************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 18.05.2021 | An3Neumann   | initial
# 1.1  | 21.12.2021 | H. Förtsch   | added function calcBytes2Value
# *****************************************************************************
import time
import os
from isytest import isystructure  # @UnresolvedImport


# #############################################################################
def calcBytes2Value(byte_list):
    """ Calculates a value from a list of bytes
    Parameter:
        byte_list - list of integer values (0x00..0xFF)

    Returns:
        integer value
    """
    return reduce(lambda x, y: (x << 8) | y, byte_list)


# #############################################################################
# #############################################################################
class FunctionsCommon(object):

    def __init__(self, testenv):
        """
         init constructor
        """
        self.testenv = testenv

    # #########################################################################
    def waitSecondsWithResponse(self, wait_second, wait_intervall_s=5):
        """
            wait_second:         time to wait in seconds
            wait_intervall:      intervall for response

        """

        if wait_second > (wait_intervall_s + 2):
            i = int(wait_second / wait_intervall_s)
            rest = wait_second - (int(i) * wait_intervall_s)

            for j in range(i):
                time.sleep(wait_intervall_s)
                print "... %ss" % (wait_intervall_s * (j + 1))
            if rest > 0:
                time.sleep(rest)
                print "... %ss" % (rest)
        else:
            # smaller waitintervall+2 seconds, no response needed
            time.sleep(wait_second)

    # #########################################################################
    def getVersionFromiTestStudio(self, current_series, version):
        """
        Parameter:
            current_series  - name of current test series
            version         - version which shall be read out, 'SOFTWAREVERSION' or 'HARDWAREVERSION'
        Info:
           Reads out the version from project data in iTestStudio. Precondition
           is a test start via iTestStudio.
        Return:
            exp_version     - version from iTestStudio
        """
        if version in ['SOFTWAREVERSION', 'HARDWAREVERSION']:
            ser_folder = self.testenv.config.getAbsPath("FOLDERS", "test_series")
            ser_path = os.path.join(ser_folder, current_series)
            ser_data = isystructure.readTestSeries(ser_path)
            for key, value in sorted(ser_data.get("META", {}).iteritems()):
                if key == version:
                    exp_version = value
        else:
            print("Version which shall be read out out is not in %s " % ser_data)
        return exp_version
