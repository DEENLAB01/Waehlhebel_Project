# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : ClampControl_01_Timeout_check.py
# Title   : ClampControl_01_Timeout_check
# Task    : Set ClampControl_01_Timeout  error 
#           --> check DTC is active and confirmed after debounce time
#           --> enabled ClampControl_01
#           --> verfiy if dtc is passive and confirmed
# Author  : M.A. Mushtaq
# Date    : 21.03.2022
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 21.03.2022 | M.A. Mushtaq | initial
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import functions_hil

import time


# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    
    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()
    func_hil = functions_hil.FunctionsHil(testenv, hil)
    # Initialize variables ####################################################
    clampControl_01_switch = hil.ClampControl_01__period
    clampControl_01_switch_values = [100, 0]
    
    activ_dtcs = [(0xE00105, 0x2F)]
    pasiv_dtcs = [(0xE00105, 0x2C)]
    clampControl_01_debounce_time = 1.05

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_387")
    
    # TEST PRE CONDITIONS #####################################################

    testresult.append(["[-] Test Vorbedingungen", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(["[+0]", ""])
    testresult.append(canape_diag.resetEventMemory())
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append([" set Systeminfo_01_SI_NWDF_30 =1  ", "INFO"])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)
    time.sleep(1.01)

    testresult.append(["[.] Disabled clampControl_01", ""])
    clampControl_01_switch.set(0)
   
    testresult.append(["Warte %ss - " %clampControl_01_debounce_time, "INFO"])
    time.sleep(clampControl_01_debounce_time)
    testresult.append(["[.] Lese Fehlerspeicher (clampControl_01 Timeout-DTC aktiv)", ""])
   
    testresult.append(canape_diag.checkEventMemory(activ_dtcs))
    
    # testresult.append(["[+0]", ""])
    # testresult.append(["[-] perform 3 OCY", ""])
    # func_hil.perform3OYC()

    testresult.append(["[+0]", ""])
    testresult.append(["[-] Enabled clampControl_01", ""])
    clampControl_01_switch.set(100)
    time.sleep(clampControl_01_debounce_time)

    # testresult.append(["[+0]", ""])
    # testresult.append(["[-] perform 1 OCY", ""])
    # hil.cl15_on__.set(0)
    # time.sleep(.2)
    # hil.cl15_on__.set(1)
    # time.sleep(clampControl_01_debounce_time)

    testresult.append(["[+0]", ""])
    testresult.append(["[-] Lese Fehlerspeicher (clampControl_01 DTC Pasiv und Confirmed)", ""])
    testresult.append(canape_diag.checkEventMemory(pasiv_dtcs, mode="ONE_OR_MORE"))

    testresult.append(["[+0]", ""])
    testresult.append(["[-] Lösche Fehlerspeicher", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())
    
    # TEST POST CONDITIONS ####################################################
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
