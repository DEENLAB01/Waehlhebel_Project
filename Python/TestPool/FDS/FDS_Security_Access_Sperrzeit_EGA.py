# ******************************************************************************
# -*- coding: latin1 -*-
# File    : FDS_Security_Access_Sperrzeit_EGA.py
# Title   : FDS Security Access Sperrzeit in EGA Session
# Task    : FDS Security Access Sperrzeit in EGA Session
#
# Author  : Mohammed Abdul Karim
# Date    : 31.05.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 27.10.2021 | Mohammed     | initial
# 1.1  | 27.10.2021 | Mohammed     | Rework
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import time
from functions_diag import HexList  # @UnresolvedImport
from ttk_checks import basic_tests

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_308")

    # Initialize variables ####################################################

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

    # test step 2
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 3
    testresult.append(["[.] Lese aktuelle Extended Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 4
    testresult.append(["[.] Tester Present aktivieren: 3E 00", ""])
    req_TesterPresent = [0x3E, 0x00]
    [response, result] = canape_diag.sendDiagRequest(req_TesterPresent)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 7E 00 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, req_TesterPresent, job_length=2))

    # test step 5
    testresult.append(["[.] Wechsel in EGA Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    # test step 6
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 7
    testresult.append(["[.] Seed anfragen: 0x2761"])
    seed, result = canape_diag.requestSeed()
    testresult.append(["Prüfe Positive Response: 0x6761 + <seed 1> ist", ""])
    testresult.extend(result)

    wrong_key = [0x10, 0xA3, 0x1B, 0x03]
    testresult.append(["\x0aKey berechnen", ""])
    key_calculated, ver = canape_diag.calculateKey(seed)
    testresult.extend(ver)

    # test step 8
    if key_calculated!= wrong_key:
        testresult.append(["[.] Falschen Key senden: 0x2762 + <wrong key 1> "])
        verdict, res4 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x35, special=False)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2735", ""])
        testresult.append(res4)
    else:
        testresult.append(["[.] Falschen Key senden: 0x2762 + <wrong key 1>"])
        verdict, res4 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x35, special=False)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2735", ""])
        testresult.append(res4)

    # test step 9
    testresult.append(["[.] Seed anfragen: 0x2761"])
    seed, result = canape_diag.requestSeed()
    testresult.append(["Prüfe Positive Response: 0x6761 + <seed 2> ist", ""])
    testresult.extend(result)

    wrong_key = [0x10, 0xA3, 0x1B, 0x04]
    testresult.append(["\x0aKey berechnen", ""])
    key_calculated, ver = canape_diag.calculateKey(seed)
    testresult.extend(ver)

    # test step 10
    if key_calculated != wrong_key:
        testresult.append(["[.] Falschen Key senden: 0x2762 + <wrong key 2> "])
        verdict, res5 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x36, special=False)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2736", ""])
        testresult.append(res5)
    else:
        testresult.append(["[.] falschen Key senden: 0x2762 + <wrong key 2>"])
        verdict, res5 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x36, special=False)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2736", ""])
        testresult.append(res5)

    # test step 11
    testresult.append(["[.] Seed anfragen: 0x2761"])
    seed, result = canape_diag.requestSeed(pos_response=False, exp_nrc=0x37, special=False)
    testresult.append(["Prüfe Negative Response: 0x7F2737", ""])
    testresult.extend(result)

    wrong_key = [0x10, 0xA3, 0x1B, 0x05]
    testresult.append(["\x0aKey berechnen", ""])
    key_calculated, ver = canape_diag.calculateKey(seed)
    testresult.extend(ver)

    # test step 12
    if key_calculated != wrong_key:
        testresult.append(["[.] Falschen Key senden: 0x2762 + <wrong key 3> "])
        verdict, res6 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x24, special=False)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2724", ""])
        testresult.append(res6)
    else:
        testresult.append(["[.] Falschen Key senden: 0x2762 + <wrong key 3>"])
        verdict, res6 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x37, special=False)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2724", ""])
        testresult.append(res6)

    # test step 13
    testresult.append(["\xa0Zugriffsversuch während Sperrzeit:"])
    testresult.append(["[.] Warte 5 Minute"])
    time.sleep(300)

    # test step 14
    testresult.append(["[.] Seed anfragen: 0x2761", ""])
    seed, result = canape_diag.requestSeed(pos_response=False, exp_nrc=0x7F, special=False)
    testresult.append(["Prüfe Negative Response: 0x7F277F", ""])
    testresult.extend(result)

    # test step 15
    testresult.append(["\xa0Zugriffsversuch während Sperrzeit:"])
    testresult.append(["[.] Warte 5 Minute"])
    time.sleep(300)

    # test step 16
    testresult.append(["[.] Wechsel in Factory Mode:  0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    # test step 17
    testresult.append(["[.] Seed anfragen: 0x2761"])
    seed, result = canape_diag.requestSeed()
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(result)

    # test step 18
    testresult.append(["[.] Key berechnen:<key 4>"])
    key, verdictkey = canape_diag.calculateKey(seed)
    testresult.append(verdictkey)

    # test step 19
    testresult.append(["[.] Key senden: 0x2762 + <key 4>"])
    verdict = canape_diag.sendKey(key)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(verdict)

    # test step 20
    testresult.append(["\xa0Prüfen, ob KeyCounter auf 0 zurückgesetzt wurde:", ""])
    testresult.append(["[.] Seed anfragen: 0x2761", ""])
    seed, result = canape_diag.requestSeed()
    testresult.append(["Prüfe Positive Response: 0x6761 + <seed 4> ist", ""])
    testresult.extend(result)

    wrong_key = [0x10, 0xA3, 0x1B, 0x16]
    testresult.append(["\x0aKey berechnen", ""])
    key_calculated, ver = canape_diag.calculateKey(seed)
    testresult.extend(ver)

    # test step 21
    if key_calculated != wrong_key:
        testresult.append(["[.] Falschen Key senden: 0x2762 + <wrong key 5> "])
        verdict, res7 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x24, special=False)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2735", ""])
        testresult.append(res7)
    else:
        testresult.append(["[.] Falschen Key senden: 0x2762 + <wrong key 5>"])
        verdict, res7 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x35, special=False)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2735", ""])
        testresult.append(res7)

    # test step 22
    testresult.append(["[.] Seed anfragen: 0x2761", ""])
    seed, result = canape_diag.requestSeed()
    testresult.append(["Prüfe Positive Response: 0x6761 + <seed 6> ist", ""])
    testresult.extend(result)

    wrong_key = [0x10, 0xA3, 0x1B, 0x26]
    testresult.append(["\x0aKey berechnen", ""])
    key_calculated, ver = canape_diag.calculateKey(seed)
    testresult.extend(ver)

    # test step 23
    if key_calculated != wrong_key:
        testresult.append(["[.] falschen Key senden: 0x2762 + <wrong key 6> "])
        verdict, res8 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x24, special=False)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2735", ""])
        testresult.append(res8)
    else:
        testresult.append(["[.] falschen Key senden: 0x2762 + <wrong key 6>"])
        verdict, res8 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x36, special=False)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2735", ""])
        testresult.append(res8)

    # test step 24
    testresult.append(["[.] Seed anfragen: 0x2761", ""])
    seed, result = canape_diag.requestSeed()
    testresult.append(["Prüfe Positive Response: 0x6711 + <seed 7> ist", ""])
    testresult.extend(result)

    wrong_key = [0x10, 0xA3, 0x1B, 0x07]
    testresult.append(["\x0aKey berechnen", ""])
    key_calculated, ver = canape_diag.calculateKey(seed)
    testresult.extend(ver)

    # test step 25
    if key_calculated != wrong_key:
        testresult.append(["[.] falschen Key senden: 0x2762 + <wrong key 7> "])
        verdict, res9 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x24, special=False)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2735", ""])
        testresult.append(res9)
    else:
        testresult.append(["[.] falschen Key senden: 0x2762 + <wrong key 7>"])
        verdict, res9 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x37, special=False)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2735", ""])
        testresult.append(res9)

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print ("Done.")
