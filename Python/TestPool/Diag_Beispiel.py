#******************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_HW_Stand_84.py
# Task    : A minimal "Diagnose_HW_Stand!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 16.02.2021 | Abdul Karim  | initial
#******************************************************************************
import time
import canapeapi
from _automation_wrapper_ import TestEnv
from ttk_base.baseutils import HexList
from ttk_checks import basic_tests
testenv = TestEnv()

## Diagnosesessions wechseln
## Kl. 15 ein
## Initialisierungsphase abgeschlossen P aktiviert
try:
    testenv.setup()
    testresult = testenv.getResults()
    hil = testenv.getHil()
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
## Initialisierungsphase abgeschlossen P aktiviert

    request = [0x10, 0x02]
    # print "sendHexRequest: %s" % (HexList(request))
    response = canape_diag.sendHexRequest(request)
    print "      response: %s" % (response)
    testresult.append(["respose: %s" % (response)])

    ## Cleanup
    hil=None
    canapi_diag=None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################
