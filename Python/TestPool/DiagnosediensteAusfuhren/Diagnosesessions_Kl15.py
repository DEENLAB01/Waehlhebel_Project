# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnosesessions_Kl15.py
# Title   : Diagnosesessions Kl15
# Task    : Test correct session behaviour when switching KL15 on
#
# Author  : S. Stenger
# Date    : 21.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 21.06.2021 | StengerS     | initial
# 1.1  | 09.12.2021 | H. Förtsch   | reworked test script by test spec
# ******************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
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

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_134")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Schalte KL15 aus", ""])
    testresult.append(["Setze KL15 auf 0", "INFO"])
    hil.cl15_on__.set(0)

    # test step 2
    testresult.append(["[.] Warte 1 Sekunden", ""])
    time.sleep(1)

    # test step 3
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 4
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 5
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 6
    testresult.append(["[.] Schalte KL15 an", ""])
    testresult.append(["Setze KL15 auf 1", "INFO"])
    hil.cl15_on__.set(1)

    # test step 7
    testresult.append(["[.] Warte 1 Sekunden", ""])
    time.sleep(1)

    # test step 8
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################
