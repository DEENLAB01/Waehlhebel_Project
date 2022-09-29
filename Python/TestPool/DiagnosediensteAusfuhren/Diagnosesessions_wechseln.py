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
# 1.7  | 02.12.2021 | H. Förtsch   | reworked test script by test spec
# 1.8  | 27.01.2021 | Mohammed     | reworked test script after Adding  preconditions
# 1.9  | 23.05.2022 | Mohammed     | Aktualisiert  Vorbedingungen
# ******************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from diag_identifier import DIAG_SESSION_DICT
import functions_gearselection

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_82")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    testresult.append(["[.] Waehlhebelposition P aktiviert ", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    testresult.append(["[.] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 1 (VPE_PRODUCTION)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 0 (IDLE)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 0 (IDLE)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    # silently go one chapter level up
    #testresult.append(["[-0]", ""])

    # 1. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # 2. Wechsel in Extended Session: 0x1003
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    test_data = DIAG_SESSION_DICT['extended']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response,request, job_length=2))

    # 3. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # 4. Erneut Extended Session anfordern: 0x1003
    testresult.append(["[.] Erneut Extended Session anfordern: 0x1003", ""])
    test_data = DIAG_SESSION_DICT['extended']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response,request, job_length=2))

    # 5. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # 6. Wechsel in die Programming Session: 0x1002
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # 7. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # 8. Wechsel in die Extended Session: 0x1003
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    request_extended = [0x10, 0x03]
    testresult.append(["\xa0Versuchen, in 'extended session' zu wechseln", ""])
    response, result = canape_diag.sendDiagRequest(request_extended)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_extended, 0x7E))

    # 9. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # 10. Erneut Programming Session anfordern: 0x1002
    testresult.append(["[.] Erneut Programming Session anfordern: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # 11. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # 12. Wechsel in die Default Session: 0x1001
    testresult.append(["[.] Wechsel in die Default Session: 0x1001", ""])
    test_data = DIAG_SESSION_DICT['default']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # 13. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # 14. Wechsel in die Extended Session: 0x1003
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    test_data = DIAG_SESSION_DICT['extended']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # 15. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # 16. Wechsel in die Default Session: 0x1001
    testresult.append(["[.] Wechsel in die Default Session: 0x1001", ""])
    test_data = DIAG_SESSION_DICT['default']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # 17. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # 18. Wechsel in die Programming Session: 0x1002
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    response, result = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # 19. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # 20. Erneut Default Session anfordern: 0x1001
    testresult.append(["[.] Erneut Default Session anfordern: 0x1001", ""])
    test_data = DIAG_SESSION_DICT['default']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # 21. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
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
