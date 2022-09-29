# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : flashing_via_vflash.py
# Task    : flasing of software via Vflash
#
# Author  : Devangbhai Patel
# Date    : 20.10.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 20.10.2021 | Devangbhai  | initial
# ******************************************************************************


from vflash_api_common import FLASH_TIMEOUT
from vflash_api_common import VFlashStatus
from vflash_api_common import VFlashResult
from vflash_api_common import VFlashError
from vflash_api_common import VFlashResultError
from vflash_api_common import VFlashDLLError
import _vflash_api

import os
import time
from xml.dom.minidom import parse
from ttk_tools.vector.vflash_api import VFlashAPI
from _automation_wrapper_ import TestEnv


testenv = TestEnv()

testenv.setup()
testresult = testenv.getResults()

testenv.startupECU()

odx_file_path    = r'C:\Users\DEENLAB01\Desktop\SW0060\210915___Application_C2_Wp13Rel_1.0.0\FL_95C713041_0060_H02WAEHLHEBEL_V001_E.pdx'
flash_file_path = r"C:\Users\DEENLAB01\Desktop\SW0060\210914\Fbl_C2_Wp13Rel_1.0.0\vFlashProject\MP_EGA_PM_SCHALTBETAETIGUNG.vflash"
vflash_dll_path  = r'C:\Program Files (x86)\Vector vFlash 7\Bin\VFlashAutomation.dll'
activate_network = False
flash_timeout = 2000

# def updateVFlashFile(vflash_file_path, odx_file_path):
#     """ Update vflash_file_path with path to odx container """
#     os.chmod(vflash_file_path, 0777)
#     dom = parse(vflash_file_path)
#     node = dom.getElementsByTagName("ODXFFlashData")[0]
#     node = node.getElementsByTagName("FilePath")[0]  # select first description tag
#
#     if node.getAttribute('RelativePath'):
#         print node.getAttribute('RelativePath')
#         # FIXME: relative path should probably be relative to vflash_file_path,
#         #        and not just the base file name
#         #        => Python 2-6+ we could simply use os.path.relpath(path, start_path)
#         node.setAttribute('RelativePath', os.path.basename(odx_file_path))
#         print node.getAttribute('RelativePath')
#
#     if node.getAttribute('AbsolutePath'):
#         print node.getAttribute('AbsolutePath')
#         node.setAttribute('AbsolutePath', odx_file_path)
#         print node.getAttribute('AbsolutePath')
#
#     f = open(vflash_file_path, "wb")
#     f.write(dom.toxml())
#     f.close()
#
#
# # #########################################################################
# # flash with log output on console
# # #########################################################################
# print "[start] vFlash Automation [timestamp: %s]" % (time.ctime())
# updateVFlashFile(flash_file_path, odx_file_path)

vf = VFlashAPI(vflash_dll_path)

print "# vFlash Automation: "
print "    vflash dll path: %s" % (vf.dll_path)
print "    flash file path: %s" % (flash_file_path)

testresult = []  # initial, empty result list
print "# vFlash Automation: Flash Progress:"
try:
    vf.flash(flash_file_path, testresult, activate_network, flash_timeout)
except VFlashResultError, ex:
    testresult.append(["%s" % ex, "FAILED"])
except Exception, ex:
    testresult.append(["%s: %s" % (type(ex).__name__, ex), "ERROR"])

print "# vFlash Automation: Flash Result (Summary):"
for item, verdict in testresult:
    print "%-72s | %s" % (item, verdict)

print "[done] vFlash Automation [timestamp: %s]" % (time.ctime())

testenv.shutdownECU()

testenv.breakdown()