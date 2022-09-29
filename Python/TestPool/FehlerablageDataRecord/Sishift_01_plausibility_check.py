# *******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Sishift_01_plausibility_check.py
# Title   : Sishift_01_plausibility_check
# Task    : Sishift_01 Plausibility Check

# Author  : Mohammed Abdul Karim
# Date    : 07.04.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************** Version ***********************************
# ******************************************************************************
# Rev. | Date        | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 07.04.2022  | Mohammed  | initial
# ******************************************************************************

from _automation_wrapper_ import TestEnv

testenv = TestEnv()

# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
import time
import functions_hil
import data_common as dc
from ttk_daq import eval_signal

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()
    func_hil = functions_hil.FunctionsHil(testenv, hil)

    # Initialize variables ####################################################
    period_var = hil.SiShift_01__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 5000  # CAN_3244
    activ_dtcs = [(0xE00101, 0x27)]
    pasiv_dtcs1 = [(0xE00101, 0x2E), (0xE00101, 0x2E)]
    failure_set_time = 0.1
    voltage_settle_time = 0.02  # do not know the actual time
    failure_reset_time = 0.1

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_yy")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[-] Test Vorbedingungen: KL30 und KL15 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append([" set Systeminfo_01_SI_NWDF_30 =1  ", "INFO"])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(["[+0]", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])


    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    cal = None
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()

