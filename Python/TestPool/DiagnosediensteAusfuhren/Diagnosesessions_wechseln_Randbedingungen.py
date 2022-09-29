# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnosesessions_wechseln_Randbedingungen.py
# Title   : Diagnosesessions wechseln Randbedingungen
# Task    : A minimal "Diagnosesessions_wechseln_Randbedingungen!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 15.02.2021 | Mohammed | initial
# 1.1  | 15.02.2021 | Mohammed | Added right NRC
# 1.2  | 25.05.2022 | Mohammed | Aktualisiert  Vorbedingungen
# 1.3  | 16.08.2022 | Mohammed | Rework
# ******************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from diag_identifier import DIAG_SESSION_DICT
import functions_gearselection
import time
# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_342")

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

    # testresult.append(["[.] VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    # descr, verdict = func_gs.setVelocity_kmph(0)
    # testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    testresult.append(["[.] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 0 (VPE_None)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 4 (Running)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 4 (IDLE)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    time.sleep(2)

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 3
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 4
    testresult.append(["[+] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 4-4.6
    testresult.append(["[.] Setze VDSO_Vx3d auf 10 km/h)", ""])
    descr, verdict = func_gs.setVelocity_kmph(10)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Warte 2 sec", ""])
    time.sleep(2)

    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request, exp_nrc=0x22, ticket_id='Fehler-Id:EGA-PRM-179'))
    testresult.append(["[-0]", ""])

    # test step 5-5.3
    testresult.append(["[.] Setze VDSO_Vx3d auf 6 km/h Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(6)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[+] Warte 2 sec", ""])
    time.sleep(2)

    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request, exp_nrc=0x22, ticket_id='Fehler-Id:EGA-PRM-179'))
    testresult.append(["[-0]", ""])

    # test step 6-6.4
    testresult.append(["[.] Setze VDSO_Vx3d auf 5 km/h Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(5)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[+] Warte 2 sec", ""])
    time.sleep(2)

    # test step 4
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))

    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))
    testresult.append(["[-0]", ""])

    testresult.append(["[.] Wechsel in Default Session: 0x1001 und Warte 1 Sekunde", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))
    time.sleep(1)

    testresult.append(["[+] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 3
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 4
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 8-8.3
    testresult.append(["[.] Setze VDSO_Vx3d auf 0 km/h Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Warte 2 sec", ""])
    time.sleep(2)

    testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))

    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))
    testresult.append(["[-0]", ""])

    testresult.append(["[.] Wechsel in Default Session: 0x1001 und Warte 1 Sekunde", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))
    time.sleep(1)

    testresult.append(["[+] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 3
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 4
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 10
    testresult.append(["[.] Setze VDSO_Vx3d auf -4.9 km/h Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(-4.9)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Warte 2 sec", ""])
    time.sleep(2)

    testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))

    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))
    testresult.append(["[-0]", ""])

    # test step 14
    testresult.append(["[.] Wechsel in Default Session: 0x1001 und Warte 1 Sekunde", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))
    time.sleep(1)

    testresult.append(["[+] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 15
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 17
    testresult.append(["[.] Setze VDSO_Vx3d auf -10 km/h Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(-10)
    testresult.append(["\xa0" + descr, verdict])
    testresult.append(["[.] Warte 2 sec", ""])
    time.sleep(2)

    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request, exp_nrc=0x22, ticket_id='Fehler-Id:EGA-PRM-179'))
    testresult.append(["[-0]", ""])

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
