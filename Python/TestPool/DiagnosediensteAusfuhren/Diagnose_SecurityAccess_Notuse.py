# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_SecurityAccess_Notuse.py
# Title   : Diagnose Security Access
# Task    : Tests if security access is successful
#
# Author  : S. Stenger
# Date    : 31.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 31.05.2021 | StengerS     | initial
# 1.1  | 03.12.2021 | H. Förtsch   | reworked test script by test spec
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import time
from functions_diag import HexList  # @UnresolvedImport

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_125")

    # Initialize variables ####################################################
    timer_unlock_ecu = 10 * 60  # 10 minutes

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
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # add next parent chapter
    testresult.append(["[.]", ""])

    # test step 2.1
    testresult.append(["[+] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 2.2
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # go one chapter level up, add next parent chapter
    testresult.append(["[-]", ""])

    # test step 3.1
    testresult.append(["[+] Wechsel in Programming Session: 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming', read_active_session=False))

    # test step 3.2
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # test step 4
    testresult.append(["[-] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    # test step 5
    testresult.append(["[.] Seed anfragen: 0x2711", ""])
    seed_1, result = canape_diag.requestSeed()
    testresult.extend(result)

    # test step 6
    testresult.append(["[.] Key berechnen", ""])
    key_1, result = canape_diag.calculateKey(seed_1)
    testresult.extend(result)

    # test step 7
    testresult.append(["[.] Key senden: 0x2712 + {}".format(HexList(key_1)), ""])
    result = canape_diag.sendKey(key_1)
    testresult.extend(result)

    # test step 8
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 9
    testresult.append(["[.] Seed anfragen: 0x2711", ""])
    seed, result = canape_diag.requestSeed()
    testresult.extend(result)
    expected_seed = [0x00, 0x00, 0x00, 0x00]
    if seed == expected_seed:
        descr = ("Seed entspricht dem erwartetem Wert:\n"
                 "{} == {}") \
                .format(HexList(seed) ,HexList(expected_seed))
        verdict = "PASSED"
    else:
        descr = ("Seed entspricht NICHT dem erwartetem Wert:\n"
                 "{} != {}") \
                .format(HexList(seed) ,HexList(expected_seed))
        verdict = "FAILED"
    testresult.append([descr, verdict])

    # test step 10
    testresult.append(["[.] Wechsel in Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    # test step 11
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 12
    testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming', read_active_session=False))

    # test step 13
    testresult.append(["[.] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    # test step 14
    testresult.append(["[.] Seed anfragen: 0x2711", ""])
    seed_2, result = canape_diag.requestSeed()
    testresult.extend(result)

    # test step 15
    testresult.append(["[.] Seed anfragen: 0x2711", ""])
    seed_3, result = canape_diag.requestSeed()
    testresult.extend(result)

    # test step 16
    testresult.append(["[.] Seeds vergleichen", ""])
    if (seed_1 != seed_2) and (seed_1 != seed_3) and (seed_2 != seed_3):
        descr = ("Alle drei Seeds sind unterschiedlich:\n"
                 "1. Seed: {}\n"
                 "2. Seed: {}\n"
                 "3. Seed: {}\n"
                 .format(HexList(seed_1), HexList(seed_2), HexList(seed_3)))
        verdict = "PASSED"
    else:
        descr = ("Alle drei Seeds sind NICHT unterschiedlich:\n"
                 "1. Seed: {}\n"
                 "2. Seed: {}\n"
                 "3. Seed: {}\n"
                 .format(HexList(seed_1), HexList(seed_2), HexList(seed_3)))
        verdict = "FAILED"
    testresult.append([descr, verdict])

    # 17. Seed_3 als Key schicken
    testresult.append(["[.] Den aktuellen Seed als Key schicken", ""])
    testresult.append(["Sende: {}".format(HexList(seed_3)), "INFO"])
    result = canape_diag.sendKey(seed_3, pos_response=False, exp_nrc=0x35)
    testresult.extend(result)

    # 18. Key_1 als Key schicken
    testresult.append(["[.] Den ersten, 'veralteten' Key schicken", ""])
    testresult.append(["Sende: {}".format(HexList(seed_1)), "INFO"])
    result = canape_diag.sendKey(key_1, pos_response=False, exp_nrc=0x36)
    testresult.extend(result)

    # 19. Seed anfordern
    testresult.append(["[.] Seed anfordern: ECU muss gesperrt sein", ""])
    seed, result = canape_diag.requestSeed(pos_response=False, exp_nrc=0x37)
    testresult.extend(result)

    # 20. 10 Minuten warten
    testresult.append(["[.] 10 Minuten warten, um ECU zu entsperren", ""])
    time.sleep(timer_unlock_ecu)

    # test step 21
    testresult.append(["[.] Seed anfragen: 0x2711", ""])
    seed_4, result = canape_diag.requestSeed()
    testresult.extend(result)

    # test step 22
    testresult.append(["[.] Key berechnen", ""])
    key_4, result = canape_diag.calculateKey(seed_4)
    testresult.extend(result)

    # test step 23
    testresult.append(["[.] Key senden: 0x2712 + {}".format(HexList(key_1)), ""])
    result = canape_diag.sendKey(key_1)
    testresult.extend(result)

    # test step 24
    testresult.append(["[.] Wechsel in Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    # test step 25
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    del testenv
    # #########################################################################

print "Done."
