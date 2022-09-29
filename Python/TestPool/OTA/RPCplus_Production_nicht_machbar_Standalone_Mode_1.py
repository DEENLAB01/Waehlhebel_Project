# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : RPCplus_Production_nicht_machbar_Standalone_Mode_1.py
# Title   : RPCplus_Production_nicht_machbar_Standalone_Mode_1
# Task    : RPCplus Production nicht machbar in Standalone Mode 1
#
# Author  : Mohammed Abdul Karim
# Date    : 22.04.2021
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 22.04.2022 | Mohammed     | Initial
# 1.1  | 11.05.2022 | Mohammed     | Added Testschritte
# 1.3  | 23.06.2022 | Mohammed     | Added E2E Botschaft Timeout
# 1.4  | 21.07.2022 | Mohammed  | Added Raumtemperatur zwischen -40 to 90 Grad
# ******************************************************************************

# ******************************************************************************


from _automation_wrapper_ import TestEnv  # @UnresolvedImport

import time
import functions_gearselection
from ttk_checks import basic_tests
from functions_diag import HexList  # @UnresolvedImport
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
    testresult.setTestcaseId("TestSpec_388")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory())

    #############################################
    testresult.append([" \x0a Setze alle E2E Botschaft Timeout", "INFO"])
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

    # test step 1-1.3
    testresult.append(["[.] Setze vbat_cl30__V auf 13V", ""])
    hil.vbat_cl30__V.set(13.0)
    testresult.append(["[+] Auslesen DID: 0xF1F2 (KL30 Signal Read)", ""])
    request = [0x22] + [0xF1, 0xF2]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["[.] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    testresult.append(["[.] KL30 Signal auswerten", ""])
    if len(response) > 3:
        data = response[3:]  # just take data of complete response
        kl30_value_dec = 0
        i = len(response) - 3 - 1
        for kl30_value in data:
            kl30_value_dec += kl30_value << (i * 8)  # set all bytes together
            i -= 1

        testresult.append(["Empfangene Daten (Rohwert): {}\nEntspricht dem Kl30 Signal Wert: {}"
                          .format(str(HexList(data)), kl30_value_dec),
                           "INFO"])
        testresult.append(basic_tests.checkRange(kl30_value_dec, 0, 0xFFFF))

    else:
        testresult.append(["Keine Auswertung möglich, da falsche oder keine Response empfangen wurde!", "FAILED"])

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
    testresult.append(["[.] Temeprature Sensor auswerten", ""])
    if len(response) > 3:
        data = response[3:]  # just take data of complete response
        temp_value_dec = 0
        i = len(response) - 3 - 1
        for temp_value in data:
            temp_value_dec += temp_value << (i * 8)  # set all bytes together
            i -= 1

        testresult.append(["Empfangene Daten (Rohwert): {}\nEntspricht dem Temeprature Sensor Wert: {}"
                          .format(str(HexList(data)), temp_value_dec),
                           "INFO"])
        testresult.append(basic_tests.checkRange(temp_value_dec, 0, 0x5A))

    else:
        testresult.append(["Keine Auswertung möglich, da falsche oder keine Response empfangen wurde!", "FAILED"])
    testresult.append(["[-0]", ""])

    # test step 3-3.1
    testresult.append(["[.] Auslessen Standalone_Modes_1: 0x22 C1 C1 10", ""])
    request_Standalone_Modes_1 = [0x22, 0xC1, 0x10]

    response, verdict = canape_diag.sendDiagRequest(request_Standalone_Modes_1)
    testresult.append(["[+] Auf Positiv Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request_Standalone_Modes_1))
    testresult.append(["[-0]", ""])

    # test step 4
    testresult.append(["[.] Setze ungültige RPCplus Vorbedingungen ", ""])
    testresult.append(["[+] Setze VehicleProtectedEnvironment auf 0 (VPE_None)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze kein E2E Timeout, CRC und BZ Fehler ", ""])
    testresult.append(["[.] Setze VDSO_05:VDSO_Vx3d auf (0 to +/-5 km/h)", ""])
    testresult.append(func_gs.setVelocity_kmph(0))
    testresult.append(["[.] Setze ORU_Control_A_01:OnlineRemoteUpdateControlA auf 1 (PENDING)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(1)
    testresult.append(["[.] Setze ORU_Control_D_01__OnlineRemoteUpdateControlD auf 1 (PENDING)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(1)
    testresult.append(["[.] Setze ClampControl_01_KST_KL_15 auf 0 ", ""])
    hil.ClampControl_01__KST_KL_15__value.set(0)
    testresult.append(["[.] Warte tMSG_CYCLE: 500ms", ""])
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

    # test step 8
    #testresult.append(["[-] Schreiben des ECU Standalone-Mode 1", ""])
    testresult.append(["[.] Schreiben des ECU Standalone-Modes 1: 0x2E C1 10 BD DB 6B 3A", ""])
    write_standalone_modes_1 = [0x2E, 0xC1, 0x10, 0xBD, 0xDB, 0x6B, 0x3A]
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

    # test step 11
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