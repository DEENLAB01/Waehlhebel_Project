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

    #hil.VDSO_05__period.setState(state)
    #hil.Diagnose_01__period.setState("aus")
    #hil.ClampControl_01__period.setState("aus")
    hil.NVEM_12__period.setState("aus")
    hil.Dimmung_01__period.setState("aus")
    hil.NM_Airbag__period.setState("aus")
    hil.OBDC_Funktionaler_Req_All_FD__period.setState("aus")
    hil.OBD_03__period.setState("aus")
    #hil.OBD_04__period.setState("aus")
    hil.ORU_Control_A_01__period.setState("aus")
    hil.ORU_Control_D_01__period.setState("aus")
    hil.OTAMC_D_01__period.setState("aus")
    hil.Systeminfo_01__period.setState("aus")
    hil.NM_HCP1__period.setState("aus")
    hil.ORU_01__period.setState("aus")
   #hil.SiShift_01__period.setState("aus")

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 2
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    test_data = DIAG_SESSION_DICT['extended']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response,request, job_length=2))

    # test step 3
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 4
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d =  10 km/h Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.setVelocity_kmph(10)
    testresult.append(["\xa0" + descr, verdict])

 #   testresult.append(["[.] Setze Geschwindigkeit auf VDSO_Vx3d == {}km/h"
  #                    .format(geschwindigkeit1),
  #                     ""])
  #  testresult.append(func_gs.setVelocity_kmph(velocity_kmph=10))

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # test step 4.1
    testresult.append(["Warte 2 sec", ""])
    time.sleep(2)

    # test step 4.2
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 5
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request, exp_nrc=0x88, ticket_id='Fehler-Id:EGA-PRM-179'))

    # test step 6
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d =  6 km/h Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    #testresult.append(["[.] Setze Geschwindigkeit auf VDSO_Vx3d == {}km/h"
    #                  .format(6),
    #                   ""])
    #testresult.append(func_gs.setVelocity_kmph(5))
    descr, verdict = func_gs.setVelocity_kmph(6)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # test step 6.1
    testresult.append(["Warte 2 sec", ""])
    time.sleep(2)

    # test step 6.2
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 7
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request, exp_nrc=0x88, ticket_id='Fehler-Id:EGA-PRM-179'))

    # test step 8
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d =  5 km/h Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    #testresult.append(["[.] Setze Geschwindigkeit auf VDSO_Vx3d == {}km/h"
    #                  .format(5),
    #                   ""])
    #testresult.append(func_gs.setVelocity_kmph(5))
    descr, verdict = func_gs.setVelocity_kmph(5)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # test step 8.1
    testresult.append(["Warte 2 sec", ""])
    time.sleep(2)

    # test step 8.2
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 9
    testresult.append(["\xa0Überprüfen, dass Request positive beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response,request, job_length=2))

    # test step 10
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d =  2 km/h Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    #testresult.append(["[.] Setze Geschwindigkeit auf VDSO_Vx3d == {}km/h"
    #                  .format(geschwindigkeit4),
    #                   ""])
   # testresult.append(func_gs.setVelocity_kmph(2))
    descr, verdict = func_gs.setVelocity_kmph(2)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # test step 10.1
    testresult.append(["Warte 2 sec", ""])
    time.sleep(2)

    # test step 10.2
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 11
    testresult.append(["\xa0Überprüfen, dass Request positive beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # test step 12
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d =  0 km/h Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # test step 12.1
    testresult.append(["Warte 2 sec", ""])
    time.sleep(2)

    # test step 12.2
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 13
    testresult.append(["\xa0Überprüfen, dass Request positive beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # test step 14
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d =  -2 km/h Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    #testresult.append(["[.] Setze Geschwindigkeit auf VDSO_Vx3d == {}km/h"
   #                   .format(geschwindigkeit5),
    #                   ""])
    #testresult.append(func_gs.setVelocity_kmph(-2))
    descr, verdict = func_gs.setVelocity_kmph(-2)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # test step 14.1
    testresult.append(["Warte 2 sec", ""])
    time.sleep(2)

    # test step 14.2
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 15
    testresult.append(["\xa0Überprüfen, dass Request positive beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # test step 16
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d =  -5 km/h Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    #testresult.append(["[.] Setze Geschwindigkeit auf VDSO_Vx3d == {}km/h"
   #                   .format(geschwindigkeit6),
    #                   ""])
    #testresult.append(func_gs.setVelocity_kmph(-5))

    descr, verdict = func_gs.setVelocity_kmph(-5)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # test step 16.1
    testresult.append(["Warte 2 sec", ""])
    time.sleep(2)

    # test step 16.2
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 17
    testresult.append(["\xa0Überprüfen, dass Request positive beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # test step 18
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d =  -6 km/h Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    #testresult.append(["[.] Setze Geschwindigkeit auf VDSO_Vx3d == {}km/h"
    #                  .format(geschwindigkeit7),
    #                   ""])
    #testresult.append(func_gs.setVelocity_kmph(-6))
    descr, verdict = func_gs.setVelocity_kmph(-6)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # test step 18.1
    testresult.append(["Warte 2 sec", ""])
    time.sleep(2)

    # test step 18.2
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 19
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request, exp_nrc=0x88, ticket_id='Fehler-Id:EGA-PRM-179'))

    # test step 20
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d =  -10 km/h Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    #testresult.append(["[.] Setze Geschwindigkeit auf VDSO_Vx3d == {}km/h"
    #                  .format(geschwindigkeit8),
    #                   ""])
    #testresult.append(func_gs.setVelocity_kmph(-10))
    descr, verdict = func_gs.setVelocity_kmph(-10)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # test step 20.1
    testresult.append(["Warte 2 sec", ""])
    time.sleep(2)

    # test step 20.2
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 21
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request, exp_nrc=0x88, ticket_id='Fehler-Id:EGA-PRM-179'))

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
