# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_SecurityAccess.py
# Title   : Diagnose Security Access
# Task    : Tests if security access is successful
#
# Author  : S. Stenger
# Date    : 31.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 31.05.2021 | StengerS     | initial
# 1.1  | 09.12.2021 | Mohammed     | Reworked after TestSpec Update
# ******************************************************************************
#
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
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+0]", ""])

    # 1. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\x0a1. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # 2.1 Wechsel in Extended Session: 0x1003
    testresult.append(["\x0a2. Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # 3.1 Wechsel in EGA Mode: 0x1060
    testresult.append(["\x0a3. Wechsel in EGA Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    # 4. Tester present aktivieren
    testresult.append(["\x0a4. Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    # 5./6./7. Security Access
    testresult.append(["\x0a5. Seed anfragen: 0x2761"])
    seed_1, result = canape_diag.requestSeed()
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(result)

    testresult.append(["\x0a6. Key berechnen:"])
    key_1, verdictkey = canape_diag.calculateKey(seed_1)
    testresult.extend(verdictkey)

    testresult.append(["\x0a7. Key senden: 0x2762 + <berechnet key>:"])
    verdict = canape_diag.sendKey(key_1)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(verdict)

    testresult.append(["\x0a8. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    testresult.append(["\x0a9. Seed anfragen: 0x2761"])
    seed, result = canape_diag.requestSeed()
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(result)

    testresult.append(["\x0a10. Wechsel in Default Session: 0x1001", ""])
    testresult.extend(
        canape_diag.changeAndCheckDiagSession('default'))  ########################  change diagnose session to default

    testresult.append(["\x0a11. Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))  ########################  change diagnose session to extended

    testresult.append(["\x0a12. Wechsel in EGA Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    testresult.append(["\x0a13. Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    testresult.append(["\x0a14. Seed anfragen: 0x2761"])
    seed_2, result = canape_diag.requestSeed()
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(result)

    testresult.append(["\x0a15. Seed anfragen: 0x2761"])
    seed_3, result = canape_diag.requestSeed()
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(result)

    testresult.append(["\x0a16. Seeds vergleichen"])
    testresult.append(["Prüfe, dass <seed 1> != <seed 2> != <seed 3>", "INFO"])

    if (seed_1 != seed_2) and (seed_1 != seed_3) and (seed_2 != seed_3):
        descr = ("Alle drei Seeds sind unterschiedlich:\n"
                 "1. Seed: %s\n"
                 "2. Seed: %s\n"
                 "3. Seed: %s\n" % (str(HexList(seed_1)), str(HexList(seed_2)), str(HexList(seed_3))))
        verdict = "PASSED"
    else:
        descr = ("Alle drei Seeds sind NICHT unterschiedlich:\n"
                 "1. Seed: %s\n"
                 "2. Seed: %s\n"
                 "3. Seed: %s\n" % (str(HexList(seed_1)), str(HexList(seed_2)), str(HexList(seed_3))))
        verdict = "FAILED"
    testresult.append([descr, verdict])

    testresult.append(["\x0a17. Key senden: 0x2762 + <seed 3>"])
    verdict = canape_diag.sendKey(HexList(seed_3), pos_response=False, exp_nrc=0x35)
    testresult.append(["Auf Negativ Response überprüfen", ""])
    testresult.extend(verdict)

    testresult.append(["\x0a18. Key senden: 0x2762 + <Key 1>"])
    verdict = canape_diag.sendKey(key_1, pos_response=False, exp_nrc=0x24)
    testresult.append(["Auf Negativ Response überprüfen", ""])
    testresult.extend(verdict)

    testresult.append(["\x0a19. Seed anfragen: 0x2761"])
    seed_1, result = canape_diag.requestSeed()
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(result)

    testresult.append(["\x0a20. Warten 10 Minuten bis ECU freigeschaltet wird "])
    time.sleep(10*60)

    testresult.append(["\x0a21. Seed anfragen: 0x2761"])
    seed4, result = canape_diag.requestSeed()
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(result)

    testresult.append(["\x0a22. Key berechnen:"])
    key4, verdictkey = canape_diag.calculateKey(seed4)
    testresult.extend(verdictkey)

    testresult.append(["\x0a23. Key senden: 0x2762 + <berechnet key>:"])
    verdict = canape_diag.sendKey(key4)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(verdict)

    testresult.append(["\x0a24. Wechsel in Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    '''
##############################################################################################################
    testresult.append(["[.] Erfolgreichen Security Access durchführen", ""])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    # 8. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # 9. Seed anfordern
    testresult.append(["[.] Erneut Seed anfordern, muss mit '0' beantwortet werden", ""])
    seed, result = canape_diag.requestSeed()
    testresult.extend(result)
    if seed == [0x00, 0x00, 0x00, 0x00]:
        descr = "Seed entspricht dem erwartetem Wert:\n %s == [0x00, 0x00, 0x00, 0x00]" % str(HexList(seed))
        verdict = "PASSED"
    else:
        descr = "Seed entspricht NICHT dem erwartetem Wert:\n %s != [0x00, 0x00, 0x00, 0x00]" % str(HexList(seed))
        verdict = "FAILED"
    testresult.append([descr, verdict])

    # 10. Wechsel in Default Session: 0x1001
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    # 11./12. Wechsel in Extended Session: 0x1003
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # 13. Tester present aktivieren
    testresult.append(["\xa0Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    # 14./15./16. Seeds anfordern und vergleichen
    testresult.append(["[.] Zwei weitere Seeds anfordern und mit dem ersten Seed vergleichen", ""])
    seed_2, result = canape_diag.requestSeed()
    testresult.extend(result)
    seed_3, result = canape_diag.requestSeed()
    testresult.extend(result)

    if (seed_1 != seed_2) and (seed_1 != seed_3) and (seed_2 != seed_3):
        descr = ("Alle drei Seeds sind unterschiedlich:\n"
                 "1. Seed: %s\n"
                 "2. Seed: %s\n"
                 "3. Seed: %s\n" % (str(HexList(seed_1)), str(HexList(seed_2)), str(HexList(seed_3))))
        verdict = "PASSED"
    else:
        descr = ("Alle drei Seeds sind NICHT unterschiedlich:\n"
                 "1. Seed: %s\n"
                 "2. Seed: %s\n"
                 "3. Seed: %s\n" % (str(HexList(seed_1)), str(HexList(seed_2)), str(HexList(seed_3))))
        verdict = "FAILED"
    testresult.append([descr, verdict])

    # 17. Seed_3 als Key schicken
    testresult.append(["[.] Den aktuellen Seed als Key schicken", ""])
    result = canape_diag.sendKey(seed_3, pos_response=False, exp_nrc=0x35)
    testresult.extend(result)

    # 18. Key_1 als Key schicken
    testresult.append(["[.] Den ersten, 'veralteten' Key schicken", ""])
    result = canape_diag.sendKey(key_1, pos_response=False, exp_nrc=0x36)
    testresult.extend(result)

    # 19. Seed anfordern
    testresult.append(["[.] Seed anfordern: ECU muss gesperrt sein", ""])
    seed, result = canape_diag.requestSeed(pos_response=False, exp_nrc=0x37)
    testresult.extend(result)

    # 20. 10 Minuten warten
    testresult.append(["[.] 10 Minuten warten, um ECU zu entsperren", ""])
    time.sleep(timer_unlock_ecu)

    # 21./22./23. Security Access
    testresult.append(["[.] Erfolgreichen Security Access durchführen", ""])
    seed_4, key_4, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    # 24./25. Erneut Default Session anfordern: 0x1001
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))


    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()
    '''

finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print "Done."
