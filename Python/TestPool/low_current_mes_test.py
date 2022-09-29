#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : low_current_measurement.py
# Title   : low_current_measurement
# Task    : low_current_measurement
#
# Author  : M.A.Mushtaq
# Date    : 01.02.2022
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 07.05.2021 | M.A.Mushtaq| initial
# 
#******************************************************************************
from _automation_wrapper_ import TestEnv
testenv = TestEnv()

import time
# Imports #####################################################################

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()
    
    # Initialize functions ####################################################
    hil = testenv.getHil()
    testenv.startupECU()  # startup before cal vars are called
    can_bus = testenv.getCanBus()

    # TEST PROCESS ############################################################


    # set Testcase ID #########################################################
    #setTestcaseId(testresult, 'NA')
    testresult.append(["\nlow_current_measurement", ""]) 


    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    
    hil.N1SRC_SetMode__Mode__value.set(3)
    hil.N1SRC_SetMode__trigger.set(0)
    hil.N1SRC_SetMode__trigger.set(1)
    time.sleep(0.1)
    hil.load_number_select.set(102)
    time.sleep(0.1)
    hil.error_type.set(1)
    time.sleep(0.1)
    hil.N1SRC_ReqData__CycleTime__value.set(0)
    hil.N1SRC_ReqData__trigger.set(0)
    hil.N1SRC_ReqData__trigger.set(1)
    time.sleep(1)
    current_val = hil.N1SRC_Measurement_Low__CurrentLow__value.get()
    
    testresult.append(["\nlow_current_measurement %d mA" %(current_val*0.0085), ""]) 
    
    time.sleep(0.1)
    hil.load_number_select.set(0)
    time.sleep(0.1)
    hil.error_type.set(0)
    time.sleep(0.1)
    hil.N1SRC_SetMode__Mode__value.set(0)
    hil.N1SRC_SetMode__trigger.set(0)
    hil.N1SRC_SetMode__trigger.set(1)
    
    
    # clear any currently used test case id ###################################
    testresult.clearTestcaseId()
    
    # TEST POST CONDITIONS ####################################################
    testresult.append(["\nTest Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()
    
    # cleanup
    cal = None
    hil = None
    can_bus = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
