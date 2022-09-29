# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : ORUnext_OnlineRemoteUpdateControlA.py
# Title   : ORUnext_OnlineRemoteUpdateControlA
# Task    : ORUnext OnlineRemoteUpdateControlA
#           
# Author  : Mohammed Abdul Karim
# Date    : 23.02.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 23.02.2022 | Mohammed     | initial
# 1.0  | 25.04.2022 | Mohammed     | Reworked
# ******************************************************************************

# ******************************************************************************


from _automation_wrapper_ import TestEnv # @UnresolvedImport
import functions_gearselection
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
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################


    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_306")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: KL30 an", ""])
    #testenv.startupECU()
    hil.cl30_on__.set(1)
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1-1.10
    testresult.append(["[.] Setze gulitige ORUnext Vorbedingungen", ""])
    testresult.append(["[.] Setze vbat_cl30__V auf 13V ", ""])
    hil.vbat_cl30__V.set(13.0)
    testresult.append(["[.] Setze OTAMC_D_01 setze auf VPE_PRODUCTION", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_CONTROL_A auf IDLE ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_CONTROL_D auf  IDLE ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)
    testresult.append(["[.] Setze VDSO_Vx3d auf 0 km/h (37766)", ""])
    testresult.append(func_gs.setVelocity_kmph(0))
    testresult.append(["[.] Setze Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))
    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append(["[.] Setze Kein CRC und BZ Fehler ", ""])
    testresult.append(["[.] Setze Kein E2E Timeout ", ""])
    testresult.append(["[.] Warte tMSG_CYCLE:500ms ", ""])
    time.sleep(0.5)
    testresult.append(["[-0]", ""])

    # test step 2
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 3
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 4
    testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))

    # test step 5
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # test step 6
    testresult.append(["[.] Wechsel in default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    # test step 7
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 8-8.2
    testresult.append(["[.] Setze ORU Signale ", ""])
    testresult.append(["[+] Setze ClampControl_01__KST_KL_15__value 0 ", ""])
    hil.ClampControl_01__KST_KL_15__value.set(0)
    testresult.append(["[.] Sezte ORU_CONTROL_A auf IDLE ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze vbat_cl30__V auf 5.7 ", ""])
    hil.vbat_cl30__V.set(5.7)
    testresult.append(["[.] Setze ORU_Control_D_01 Signal aus ", ""])
    hil.ORU_Control_D_01__period.setState("aus")
    tMSG_CYCLE = 0.50  # sec
    testresult.append(["[.] Warte 500ms (tMSG_CYCLE) ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 9
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 10
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 11
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 12-12.2
    testresult.append(["[.] Setze ORU Signale ", ""])
    testresult.append(["[+] Sezte ORU_CONTROL_A auf PENDING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(1)
    tMSG_CYCLE = 0.5  # sec
    testresult.append(["[.] Warte 500ms (tMSG_CYCLE) ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 13
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 14
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 15
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 16-16.2
    testresult.append(["[.] Setze ORU Signale ", ""])
    testresult.append(["[+] Sezte ORU_CONTROL_A auf PREPARATION ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(2)
    tMSG_CYCLE = 0.50  # sec
    testresult.append(["[.] Warte 500ms (tMSG_CYCLE) ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 17
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 18
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 19
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 20-20.2
    testresult.append(["[.] Setze ORU Signale ", ""])
    testresult.append(["[+] Sezte ORU_CONTROL_A auf PREPARATION_HV ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(3)
    tMSG_CYCLE = 0.50  # sec
    testresult.append(["[.] Warte 500ms (tMSG_CYCLE) ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 21
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 22
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 23
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 24-24.2
    testresult.append(["[.] Setze ORU Signale ", ""])
    testresult.append(["[+] Sezte ORU_CONTROL_A auf RUNNING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    tMSG_CYCLE = 0.50  # sec
    testresult.append(["[.] Warte 500ms (tMSG_CYCLE) ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 25
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 26
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 27
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 28-28.2
    testresult.append(["[.] Setze ORU Signale ", ""])
    testresult.append(["[+] Sezte ORU_CONTROL_A auf RUNNING_HV ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(5)
    tMSG_CYCLE = 0.50  # sec
    testresult.append(["[.] Warte 500ms (tMSG_CYCLE) ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 29
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 30
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 31
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 32-32.2
    testresult.append(["[.] Setze ORU Signale ", ""])
    testresult.append(["[+] Sezte ORU_CONTROL_A auf PENDING_NOTREADY ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(6)
    tMSG_CYCLE = 0.50  # sec
    testresult.append(["[.] Warte 500ms (tMSG_CYCLE) ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 33
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 34
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 35
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 36-36.2
    testresult.append(["[.] Setze ORU Signale ", ""])
    testresult.append(["[+] Sezte ORU_CONTROL_A auf OTA_FAILURE_POWERTRAIN_DISABLED ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(7)
    tMSG_CYCLE = 0.50  # sec
    testresult.append(["[.] Warte 500ms (tMSG_CYCLE) ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 37
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 38
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 39
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 40-40.2
    testresult.append(["[.] Setze ORU Signale ", ""])
    testresult.append(["[+] Sezte ORU_CONTROL_A auf FUNCTIONAL_SAFETY_RELEASE ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(8)
    tMSG_CYCLE = 0.50  # sec
    testresult.append(["[.] Warte 500ms (tMSG_CYCLE) ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 41
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 42
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 43
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 44-44.2
    testresult.append(["[.] Setze ORU Signale ", ""])
    testresult.append(["[+] Sezte ORU_CONTROL_A auf PREPARATION_SG ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(9)
    tMSG_CYCLE = 0.50  # sec
    testresult.append(["[.] Warte 500ms (tMSG_CYCLE) ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 45
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 46
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 47
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 48-48.2
    testresult.append(["[.] Setze ORU Signale ", ""])
    testresult.append(["[+] Sezte ORU_CONTROL_A auf Fehler ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(15)
    tMSG_CYCLE = 0.50  # sec
    testresult.append(["[.] Warte 500ms (tMSG_CYCLE) ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 49
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 50
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 51
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.shutdownECU()
    testenv.breakdown()
    # #########################################################################