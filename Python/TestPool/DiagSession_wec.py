# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnosesessions_wechseln.py
# Title   : Diagnose Sessions wechseln
# Task    : A minimal "Diagnosesessions_wechseln!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 15.02.2021 | Abdul Karim  | initial
# 1.1  | 28.04.2021 | Abdul Karim  | added Default and Extended Session
# 1.2  | 20.05.2021 | StengerS     | automated test
# 1.3  | 25.05.2021 | StengerS     | added more session transitions
# 1.4  | 06.07.2021 | Mohammed     | adaped new TestSpec.
# 1.5  | 29.09.2021 | Mohammed     | Rework
# 1.6  | 29.09.2021 | Mohammed     | TestSpec anpassen
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_82xx")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # 1. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa01. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # 2. Wechsel in Extended Session: 0x1003
    testresult.append(["\xa02. Wechsel in Extended Session: 0x1003", "Info"])
    request_programming = [0x10, 0x03]
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_programming))
    #testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # 3. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa03. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # 4. Erneut Extended Session anfordern: 0x1003
    testresult.append(["\xa04. Erneut Extended Session anfordern: 0x1003", ""])
   # testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    request_programming = [0x10, 0x03]
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_programming))

    # 5. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa05. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # 6. Wechsel in die Programming Session: 0x1002
    testresult.append(["\xa06. Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_programming))

    # 7. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa07. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # 8. Wechsel in die Extended Session: 0x1003
    testresult.append(["\xa08. Wechsel in Extended Session: 0x1003", "Info"])
    request_extended = [0x10, 0x03]
    testresult.append(["\xa0Versuchen, in 'extended session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_extended)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_extended, 0x7E))

    # 9. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa09. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # 10. Erneut Programming Session anfordern: 0x1002
    testresult.append(["\xa010. Erneut Programming Session anfordern: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_programming))

    # 11. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa011. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # 12. Wechsel in die Default Session: 0x1001
    testresult.append(["\xa012. Wechsel in die Default Session: 0x1001", ""])
    request_programming = [0x10, 0x01]
    testresult.append(["\xa0Versuchen, in 'Default session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_programming))

    # 13. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa013. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # 14. Wechsel in die Extended Session: 0x1003
    testresult.append(["\xa014. Wechsel in Extended Session: 0x1003", ""])
    request_programming = [0x10, 0x03]
    testresult.append(["\xa0Versuchen, in 'Extended session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_programming))

    # 15. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa015. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # 16. Wechsel in die Default Session: 0x1001
    testresult.append(["\xa016. Wechsel in die Default Session: 0x1001", ""])
    request_programming = [0x10, 0x01]
    testresult.append(["\xa0Versuchen, in 'Default session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_programming))

    # 17. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa017. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # 18. Wechsel in die Programming Session: 0x1002
    testresult.append(["\xa018. Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x7E))

    # 19. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa019. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # 20. Erneut Default Session anfordern: 0x1001
    testresult.append(["\xa020. Erneut Default Session anfordern: 0x1001", ""])
    request_programming = [0x10, 0x01]
    testresult.append(["\xa0Versuchen, in 'Default session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_programming))

    # 21. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa021. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print "Done."
