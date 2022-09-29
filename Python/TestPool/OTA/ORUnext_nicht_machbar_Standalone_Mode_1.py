# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : ORUnext_nicht_machbar_Standalone_Mode_1.py
# Title   : ORUnext_nicht_machbar_Standalone_Mode_1
# Task    : ORUnext nicht machbar in Standalone Mode 1
#           
# Author  : M.A. Mushtaq
# Date    : 23.02.2022
# Copyright 2022 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 23.02.2022 | M.A. Mushtaq | initial
# 1.1  | 21.04.2022 | Mohammed     | Rework
# 1.2  | 07.05.2022 | Mohammed     | Added Testschritte
# 1.3  | 23.06.2022 | Mohammed     | Added E2E Botschaft Timeout
# ******************************************************************************

# ******************************************************************************


from _automation_wrapper_ import TestEnv # @UnresolvedImport

import time
import functions_gearselection
from ttk_checks import basic_tests

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
    testresult.setTestcaseId("TestSpec_293")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory())

    #############################################
    testresult.append([" \x0a Setze alle E2E Botschaft Timeout aus", "INFO"])
    hil.SiShift_01__period.setState("aus")
    hil.ORU_Control_A_01__period.setState("aus")
    hil.ORU_Control_D_01__period.setState("aus")
    hil.ORU_01__period.setState("aus")
    hil.OTAMC_D_01__period.setState("aus")
    hil.ORU_01__period.setState("aus")
    #############################################

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1-1.2
    testresult.append(["[.] Auslesen DID: 0xF1F2 (KL30 Signal Read)", ""])
    request = [0x22] + [0xF1, 0xF2]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["[+] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Prüfe Voltage : 13-16 V", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.vbat_cl30__V.get(),  # letzer Sendetimestamp
            min_value=6.0,
            max_value=16.0,
            descr="Check that value is in range"
        )
    )
    testresult.append(["[-0]", ""])

    # test step 2-2.1
    testresult.append(["[.] Auslesen DID: 0xF1F3 (Temeprature Sensor Read)", ""])
    request = [0x22] + [0xF1, 0xF3]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["[+] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    testresult.append(["[-0]", ""])

    # test step 3
    testresult.append(["[.] Auslessen Standalone_Modes_1: 0x22 C1 C1 10", ""])
    request_Standalone_Modes_1 = [0x22, 0xC1, 0x10]

    response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_1)
    testresult.append(["[+] Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_Standalone_Modes_1))
    testresult.append(["[-0]", ""])

    # test step 4
    testresult.append(["[.] Setze ORUnext Signale ", ""])
    testresult.append(["[+] Setze OTAMC_D_01 auf VPE_none", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze VDSO_Vx3d auf 0 km/h", ""])
    testresult.append(func_gs.setVelocity_kmph(0))
    testresult.append(["[.] Setze ORU_CONTROL_A auf  RUNNING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_CONTROL_D auf RUNNING ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))
    testresult.append(["[.] PropulsionSystemActive auf NotAktive", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append(["[.] Setze ClampControl_01_KST_KL_15 auf 0 ", ""])
    hil.ClampControl_01__KST_KL_15__value.set(0)
    testresult.append(["[.] Warte 500ms (tMSG_CYCLE)", ""])
    time.sleep(0.500)
    testresult.append(["[-0]", ""])

    # test step 5
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    # test step 6
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 7-7.3
    testresult.append(["[.] Security Access aktivieren", ""])

    testresult.append(["[+] Seed anfragen: 0x2761", ""])
    seed, result = canape_diag.requestSeed()
    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.extend(result)

    testresult.append(["[.] Key berechnen: <key 1>", ""])
    key, result = canape_diag.calculateKey(seed)
    testresult.append(result)

    testresult.append(["[.] Key senden: 0x2762 + <key 1>", ""])
    result = canape_diag.sendKey(key)
    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.extend(result)
    testresult.append(["[-0]", ""])
    time.sleep(1)
    # test step 8
    testresult.append(["[.] Schreiben des ECU Standalone-Modes 1: 0x2E C1 10 BD DB 6B 3A", ""])
    write_standalone_modes_1 = [ 0x2E, 0xC1, 0x10, 0xBD, 0xDB, 0x6B, 0x3A]
    response, verdict = canape_diag.sendDiagRequest(write_standalone_modes_1)
    testresult.append(["[+] Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, write_standalone_modes_1))
    testresult.append(["[-0]", ""])

    # test step 9
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 10
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 11
    testresult.append(["[.] Auslessen Standalone_Modes_1 : 0x22 C1 C1 10", ""])
    request_Standalone_Modes_1 = [0x22, 0xC1, 0x10]
    response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_1)
    testresult.append(["[+] Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_Standalone_Modes_1))
    testresult.append(["[-0]", ""])

    # test step 12
    testresult.append(["[.] Auslessen Standalone_Modes_2 : 0x22 C1 C1 11", ""])
    request_Standalone_Modes_2 = [0x22, 0xC1, 0x11]
    response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_2)
    testresult.append(["[+] Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_Standalone_Modes_2))
    testresult.append(["[-0]", ""])

    # test step 13
    testresult.append(["[.] Wechsel in default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    # test step 14
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 15
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 16
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 17
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