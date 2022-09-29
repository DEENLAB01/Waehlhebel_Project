# ******************************************************************************
# -*- coding: latin1 -*-
# File    : XCP_Kommunikation.py
# Title   : XCP Kommunikation
# Task    : A minimal "XCP_Kommunikation!" test script
#
# Author  : Mohammed Abdul Karim
# Date    : 17.03.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 17.03.2022 | Mohammed  | initial
# 1.1  | 07.06.2022 | Mohammed  | Rework

# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import time
from ttk_daq import eval_signal

# Instantiate test environment
testenv = TestEnv()
hil = testenv.getHil()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_381")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    testenv.startupECU()  # startup before cal vars are called
    can_bus = testenv.getCanBus()
    canape_diag = testenv.getCanapeDiagnostic()

    # Initialize variables ####################################################

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte KL30 und KL15 ein", ""])

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # test step 1
    testresult.append(["[.] Prüfe XCP-Kommunikation deaktiv(Offline) ist", ""])

    try:
        canape_xcp = testenv.getCanapeCal()
        testresult.append(["\xa0XCP Kommunikation noch Aktiv (CANape Online).", "FAILED"])
    except:
        testresult.append(["\xa0XCP Kommunikation nicht Aktiv (CANape Offline).", "PASSED"])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print "Done."
