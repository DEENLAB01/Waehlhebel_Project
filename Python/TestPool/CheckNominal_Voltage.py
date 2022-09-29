#******************************************************************************
# -*- coding: latin1 -*-
# File    : CheckNominal_Voltage.py
# Task    : A minimal "CheckNominal_Voltage!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 22.12.2020 | Abdul Karim  | initial
#******************************************************************************
import time
from _automation_wrapper_ import TestEnv    ## import TestEnv
testenv = TestEnv()                         ## instantiate TestEnv
from ttk_checks import basic_tests          ## import project libraries
try:
   # #####################################################################
   testenv.setup()                  ## Set up test environment
   testresult=testenv.getResults()  ##
   hil=testenv.getHil()         ## HiL variable container
   testenv.startupECU()         ## start up ECU
   time.sleep(.200)
  ## To DO... CANape oder gama
   testresult.append(["Test Nominal Voltage i.O.", "PASSED"])
   testresult.append(
       basic_tests.checkTolerance(
           hil.vbat_cl30__V, 14.0, 0.05, descr = "Check nominal supply voltage"
        )
    )
   #  Testcase-IDs
   testresult.append([
       "WH sendet FBL-Version",
       "[[TC-ID]] TestSpec_XX",
       "PASSED"] )

   # cleanup
   hil = None
   ## To DO


finally:
   # #########################################################################
   testenv.breakdown()
   # #########################################################################