#******************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_ECUReset_KeyOffOnReset.py
# Title   : Diagnose ECUReset KeyOffOnReset
# Task    : Tests if ECUReset with subfunction KeyOffOnReset is working
#
# Author  : S. Stenger
# Date    : 31.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name         | Description
#------------------------------------------------------------------------------
# 1.0  | 31.05.2021 | StengerS     | initial
#******************************************************************************
#
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

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_133")

    # Initialize variables ####################################################


    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()


    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s"%testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+0]", ""])

    # 1. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.extend(canape_diag.checkDiagSession('default'))

    # 2./3. Wechsel in Extended Session: 0x1003
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))
    
    # 4. Tester present aktivieren
    testresult.append(["\xa0Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    # 5. ECU Reset
    testresult.append(["[.] ECU Reset mit Subfunktion 'KeyOffOnReset' durchführen", ""])
    result = canape_diag.performEcuReset(reset_type='KeyOffOnReset')
    testresult.extend(result)

    # 6. Warten
    testresult.append(["[.] 2 Sekunden warten", ""])
    time.sleep(2)

    # 7. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.extend(canape_diag.checkDiagSession('default'))


    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown()
    del(testenv)
    # #########################################################################

print "Done."
