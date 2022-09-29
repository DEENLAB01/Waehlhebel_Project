# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Bus_KnockOut_Test_Stop_BusSleep.py
# Title   : Bus_KnockOut_Test_Stop_BusSleep
# Task    : Test for Bus_KnockOut_Test_Stop_BusSleep
#
# Author  : Mohammed Abdul Karim
# Date    : 22.12.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 22.12.2021 | Mohammed   | initial
# 1.1  | 09.02.2022 | Devangbhai | Rework according to new specification
# 1.2  | 04.03.2022 | Devangbhai | Added sleep time to adjust the time delay
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList
from diag_identifier import identifier_dict
import functions_common
from ttk_checks import basic_tests
import functions_gearselection
import time
import functions_nm
from time import time as t
import os

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_com = functions_common.FunctionsCommon(testenv)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    diag_ident_KN_CTR = identifier_dict['Knockout_counter']
    diag_ident_KN_TMR = identifier_dict['Knockout_timer']
    diag_ident_KN_TEST_MODE = identifier_dict['Knockout_test_mode']

    test_variable = hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value
    test_variable.alias = "KN_Waehlhebel:BusKnockOutTimer"
    func_com = functions_common.FunctionsCommon(testenv)

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_276")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[.] Wechsle in die Extended Session", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    testresult.append(["[.] BusKnockOut_Tmr und ECUKnockOut_Tmr auf 15 setzen"])
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x0F, 0x0F]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] BusKnockOut_Ctr und ECUKnockOut_Ctr auf 0 setzen"])
    request = [0x2E] + diag_ident_KN_CTR['identifier'] + [0x00, 0x00]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.]  ECU ausschalten", ""])
    testenv.canape_Diagnostic = None
    testenv.asap3 = None
    testenv.canape_Diagnostic = None
    del (canape_diag)
    testenv.shutdownECU()

    testresult.append(["[.]  Warte 10sekund", ""])
    time.sleep(10)

    testresult.append(["[.] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()

    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()
    # TEST PROCESS ####################################################################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # test step 1
    testresult.append(["\x0a1.  In Extended Sesssion Setze BusKnockOut_Tmr auf 17, ECUKnockOut_Tmr auf 18 und NVEM coupling auf Inktive und warte 1sec"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    testresult.append(["\xa0 BusKnockOut_Tmr auf 17, ECUKnockOut_Tmr auf 18 und NVEM coupling auf Inktive"])
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x12, 0x11]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 2
    testresult.append(["\x0a2.Prufe BusKnockOut_Tmr "])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BusKnockoutTmr_start = None
    if response[0:3] == [98, 2, 203]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BusKnockoutTmr_start = response[4]
        ECUKnockoutTmr_start = response[3]
        if BusKnockoutTmr_start and ECUKnockoutTmr_start is not None:
            if BusKnockoutTmr_start > 64:
                BusKnockoutTmr_start = BusKnockoutTmr_start - 64  # removing the active coupling value bit
                ECUKnockoutTmr_start = ECUKnockoutTmr_start
            else:
                BusKnockoutTmr_start = BusKnockoutTmr_start  # No active NVEM coupling
                ECUKnockoutTmr_start = ECUKnockoutTmr_start
        else:
            BusKnockoutTmr_start = 0
            ECUKnockoutTmr_start = 0

        testresult += [
            basic_tests.compare(left_value=BusKnockoutTmr_start, operator="<", right_value=ECUKnockoutTmr_start,
                                descr=" BusKnockOut_Tmr < ECUKnockOut_Tmr")]
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 3
    testresult.append(["\x0a 3.Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 17, descr="KN_Waehlhebel_BUSKnockOutTimer = 17")]

    # test step 4
    testresult.append(["\x0a 4. Prüfe BusKnockOut_Ctr"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BUSKnockOut_Ctr_start = None

    if response[0:3] == [98, 2, 202]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BUSKnockOut_Ctr_start = response[4]
        if BUSKnockOut_Ctr_start is not None:
            BUSKnockOut_Ctr_start = BUSKnockOut_Ctr_start
        else:
            BUSKnockOut_Ctr_start = 0
        testresult.append(basic_tests.checkStatus(BUSKnockOut_Ctr_start, 0, descr=" BusKnockOut_Ctr = 0"))
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 5
    testresult.append(["\x0a 5.  Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0,
                                           descr=" KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 0x0 (Funktion nicht ausgelöst, Initwert)")]

    # test step 6
    testresult.append(["\x0a6. KL15 ausschalten und warte 2sec "])
    hil.cl15_on__.set(0)
    time.sleep(2)

    # test step 7
    testresult.append( ["\x0a 7. Senden nur der NM Botschaft und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen."])
    func_nm.hil_ecu_tx_signal_state_for_Knockout()

    # test step 8
    testresult.append(["\x0a 8. Wechsel in die Entwicklersession, (in Factory mode security access dürchführen) "
                       "Setze mittels 2E 09 F3: KnockOut_Test_mode  auf 0x4 * (Supress Veto == Active) und warte 1, "
                       "um BUSKnockOut testen zu können"])

    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x04]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 9
    testresult.append(["\x0a 9. Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut, KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0,
                                           descr=" KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 0x0")]
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 17,
                                           descr="KN_Waehlhebel_BUSKnockOutTimer = 17")]

    # test step 10
    testresult.append( ["\x0a 10. Prüfe, dass KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer nach 1 Minute um 1 dekrementiert wird "])
    time.sleep(60)
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 16,
                                           descr="KN_Waehlhebel_BUSKnockOutTimer = 16  (wird dekrementiert)")]

    # test step 11
    testresult.append(["\x0a 11.  Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0,
                                           descr=" KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 0x0 (Funktion nicht ausgelöst)")]

    # test step 12
    testresult.append(["\x0a 12. Wechsel in die Entwicklersession, (in Factory mode security access dürchführen) "
                       "Setze mittels 2E 09 F3: KnockOut_Test_mode  auf 0x1 (Bus Sleep) und warte 1sec"])

    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_2, key_2, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x01]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 13
    testresult.append(["\x0a 13.Prüfe Bus State"])
    req = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    [response, result] = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    expected_resp = [0x62] + diag_ident_KN_TEST_MODE['identifier'] + [0x01]
    testresult.append(["Bus State == Bus Sleep", ""])
    testresult.append(canape_diag.checkResponse(response, expected_resp))

    # test step 14
    testresult.append(["\x0a 14.Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 16,
                                           descr="KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == 16 (wurde nicht zurückgesetzt)")]

    # test step 15
    testresult.append( ["\x0a 15.Prüfe 70 s lang, dass KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer nicht dekrementiert wird", ""])
    timerlist = []

    KN_Waehlhebel_BusKnockOutTimer = 16
    sec = 70
    timeout = sec + t()
    value_boolean = True

    while timeout > t():
        timerlist.append(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value.get())

    for timer_values in timerlist:
        if KN_Waehlhebel_BusKnockOutTimer != timer_values:
            value_boolean = False
            break
    testresult.append(["\xa0 KN_Waehlhebel_BusKnockOutTimer blieb %s Sekunden lang konstant bei %s"
                       % (sec, KN_Waehlhebel_BusKnockOutTimer), "PASSED"]) if value_boolean \
        else testresult.append(["\xa0 KN_Waehlhebel_BusKnockOutTimer blieb %s Sekunden lang nicht konstant bei %s"
                                % (sec, KN_Waehlhebel_BusKnockOutTimer), "FAILED"])

    # test step 16
    testresult.append(["\x0a 16.Wechsel in die Entwicklersession, (in Factory mode security access dürchführen) "
                       "Setze mittels 2E 09 F3: KnockOut_Test auf 0x4 (ungleich Bus Sleep) und warte 1sec"])

    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x04]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 17
    testresult.append(["\x0a 17.Prüfe Bus State"])
    req = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    [response, result] = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    expected_resp = [0x62] + diag_ident_KN_TEST_MODE['identifier'] + [0x04]
    testresult.append(["Bus State != Bus Sleep", ""])
    testresult.append(canape_diag.checkResponse(response, expected_resp))

    # test step 18
    testresult.append(["\x0a 18.Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 16,
                                           descr="KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == 16 (wurde nicht zurückgesetzt)")]

    # test step 19
    testresult.append(["\x0a 19. Prüfe, dass KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer nach 1 Minute um 1 dekrementiert wird "])
    time.sleep(60)
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 15,
                                           descr="KN_Waehlhebel_BUSKnockOutTimer = 15  (wird dekrementiert)")]

    # test step 20
    testresult.append(["\x0a 20. Prüfe BusKnockOut_Ctr"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BUSKnockOut_Ctr = None

    if response[0:3] == [98, 2, 202]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BUSKnockOut_Ctr = response[4]
        if BUSKnockOut_Ctr is not None:
            BUSKnockOut_Ctr = BUSKnockOut_Ctr
        else:
            BUSKnockOut_Ctr = 0
        testresult.append(basic_tests.checkStatus(BUSKnockOut_Ctr, 0, descr=" BusKnockOut_Ctr = 0"))
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 21
    testresult.append(["\x0a 21.  Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0,
                                           descr=" KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 0x0 (Funktion nicht ausgelöst)")]

    # Test Nachbedingungen
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()
    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)