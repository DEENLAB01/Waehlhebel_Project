# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Bus_KnockOut_Daten_Datensicherung.py
# Title   :Bus_KnockOut_Daten_Datensicherung
# Task    : Test for Bus_KnockOut_Daten_Datensicherung
#
# Author  : Devangbhai Patel
# Date    : 04.01.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 04.01.2022 | Devangbhai   | initial
# 1.1  | 10.02.2022 | Devangbhai | Rework according to new specification
# 1.2  | 03.03.2022 | Devangbhai | Added sleep time to adjust the time delay



from _automation_wrapper_ import TestEnv
from functions_diag import HexList
from diag_identifier import identifier_dict
import functions_common
from ttk_checks import basic_tests
import functions_gearselection
import time
from time import time as t
import functions_nm
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

    # Initialize variables ####################################################
    diag_ident_KN_CTR = identifier_dict['Knockout_counter']
    diag_ident_KN_TMR = identifier_dict['Knockout_timer']
    diag_ident_KN_TEST_MODE = identifier_dict['Knockout_test_mode']
    func_nm = functions_nm.FunctionsNM(testenv)

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_272")

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
    testresult.append(["?berpr?fen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] BusKnockOut_Ctr und ECUKnockOut_Ctr auf 0 setzen"])
    request = [0x2E] + diag_ident_KN_CTR['identifier'] + [0x00, 0x00]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["?berpr?fen, dass Request positiv beantwortet wird", "INFO"])
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

    # TEST PROCESS ########################################################################################################################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # test step 1
    testresult.append(["\x0a 1. In extended session Setze BusKnockOut_Tmr auf 15min und NVEM coupling auf Inktiv. "])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    testresult.append(["\xa0 BusKnockOut_Tmr auf 15, ECUKnockOut_Tmr auf 15 und NVEM coupling auf inaktive"])
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x0F, 0x0F]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["?berpr?fen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 2
    testresult.append(["\x0a2.Prufe BusKnockOut_Tmr and speichere den Wert als bus_tmr"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BusKnockoutTmr_start = None
    if response[0:3] == [98, 2, 203]:
        testresult.append(["Auf positive Response ?berpr?fen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BusKnockoutTmr_start = response[4]
        if BusKnockoutTmr_start is not None:
            if BusKnockoutTmr_start > 64:
                BusKnockoutTmr_start = BusKnockoutTmr_start - 64  # removing the active coupling value bit
            else:
                BusKnockoutTmr_start = BusKnockoutTmr_start  # No active NVEM coupling
                testresult.append([
                                      "\xa0 Gespeichere Wert f?r BusKnockoutTmr_start (Variable) f?r sp?teren Vergleich ist %s" % BusKnockoutTmr_start])
        else:
            BusKnockoutTmr_start = 0

        testresult += [basic_tests.checkStatus(BusKnockoutTmr_start, 15, descr="KN_Waehlhebel_BUSKnockOutTimer = 15")]

    else:
        testresult.append(["Auf positive Response ?berpr?fen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 3
    testresult.append(["\x0a 3.Pr?fe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 15,
                                           descr="KN_Waehlhebel_BUSKnockOutTimer = 15")]

    # test step 4
    testresult.append(["\x0a 4. Warte 1,5min"])
    time.sleep(1.5 * 60)

    # test step 5
    testresult.append(["\x0a 5.Pr?fe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    if BusKnockoutTmr_start is not None:
        testresult += [
            basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, BusKnockoutTmr_start,
                                    descr=" KPr?fe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == bus_tmr == 15 (Ausgangswert; Timer l?uft nicht)")]

    # test step 5.1
    testresult.append(["\x0a 5.1. Pr?fe BusKnockOut_Ctr"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BUSKnockOut_Ctr_start = None

    if response[0:3] == [98, 2, 202]:
        testresult.append(["Auf positive Response ?berpr?fen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BUSKnockOut_Ctr_start = response[4]
        if BUSKnockOut_Ctr_start is not None:
            BUSKnockOut_Ctr_start = BUSKnockOut_Ctr_start
        else:
            BUSKnockOut_Ctr_start = 0
        testresult.append(basic_tests.checkStatus(BUSKnockOut_Ctr_start, 0, descr=" BusKnockOut_Ctr = 0"))
    else:
        testresult.append(["Auf positive Response ?berpr?fen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 6
    testresult.append(["\x0a 6. KL15 ausschalten und warte 12 sec"])
    hil.cl15_on__.set(0)
    time.sleep(12)

    # test step 7
    testresult.append(["\x0a 7. Senden nur der NM Botschaft und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen."])
    func_nm.hil_ecu_tx_signal_state_for_Knockout()

    # test step 8
    testresult.append(["\x0a 8.  Pr?fe veto w?rde erkannt"])
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 1,
                                              descr="KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 1 (Veto Aktiv)"))

    # test step 9
    testresult.append(["\x0a 9. Pr?fe 70 s lang, dass KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer eingefroren ist", ""])
    timerlist = []

    KN_Waehlhebel_BusKnockOutTimer = 15
    sec = 70
    timeout = sec + t()
    value_boolean = True

    while timeout > t():
        timerlist.append(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value.get())

    for timer_values in timerlist:
        if KN_Waehlhebel_BusKnockOutTimer != timer_values:
            value_boolean = False
            break
    testresult.append(
        ["KN_Waehlhebel_BusKnockOutTimer blieb %s Sekunden lang konstant bei %s" % (
        sec, KN_Waehlhebel_BusKnockOutTimer), "PASSED"]) \
        if value_boolean else testresult.append(
        ["KN_Waehlhebel_BusKnockOutTimer blieb %s Sekunden lang nicht konstant bei %s"
         % (sec, KN_Waehlhebel_BusKnockOutTimer), "FAILED"])

    # test step 10
    testresult.append(["\x0a 10. Wechsel in die Entwicklersession, (in Factory mode security access d?rchf?hren) "
                       "Setze mittels 2E 09 F3: KnockOut_Test_mode  auf 0x4 * (Supress Veto == Active), "
                       "um BUSKnockOut testen zu k?nnen und warte 2sec"])

    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchf?hren", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x04]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Pr?fe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(2)

    # test step 11
    testresult.append(["\x0a 11. Pr?fe kein veto w?rde erkannt."])
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0,
                                              descr="KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 0 (Initwert)"))

    # test step 12
    testresult.append(["\x0a 12 Pr?fe KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer nach 60 Sekunden"])
    time.sleep(60)
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 14,
                                              descr="KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer = 14 (wird dekrementiert)"))

    # test step 13
    testresult.append(["\x0a 13. Warte bis KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer == 0 (Timeout: 14min)"])
    timeout = 14 * 60
    t_out = timeout + t()
    while t_out > t():
        if hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value.get() == 0:
            testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 0, descr="KN_Waehlhebel_BUSKnockOutTimer = 0")]
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer  hat kein auf 0 gesetz in 14min", "FAILED"])
            break

    # test step 14
    testresult.append(["\x0a 14. Schalte alle signal (HIL--> ECU) aus. "])
    time.sleep(0.400)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=False, all_other_send=False)

    # test step 15
    testresult.append(["\x0a 15. Pr?fe, dass Reset des SG stattfindet"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 2,
                                           descr=" KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 2 (0x2= Funktion_ausgeloest)")]

    # test step 16
    testresult.append(["\x0a 16. Warte 1 min. und Pr?fe Busruhe", ""])
    time.sleep(60)
    descr, verdict = func_gs.checkBusruhe(daq)
    testresult.append([descr, verdict])

    # test step 17
    testresult.append(["\x0a 17. Schalte alle signal (HIL--> ECU) ein. Schalte KL15 ein und warte 5sec.", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=True, all_other_send=True)
    time.sleep(5)

    # test step 18
    testresult.append(["\x0a 18 Pr?fe nichtfl?chtige Speicherung von BusKnockOut_Tmr"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BusKnockoutTmr = None
    if response[0:3] == [98, 2, 203]:
        testresult.append(["Auf positive Response ?berpr?fen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BusKnockoutTmr = response[4]
        if BusKnockoutTmr is not None:
            if BusKnockoutTmr > 64:
                BusKnockoutTmr = BusKnockoutTmr - 64  # removing the active coupling value bit
                testresult.append(["\xa0 NVEM couplling ist Aktive", "FAILED"])
            else:
                BusKnockoutTmr = BusKnockoutTmr  # No active NVEM coupling
                testresult.append(["\xa0 NVEM couplling ist inaktive", "PASSED"])
        else:
            BusKnockoutTmr = 0

        testresult += [basic_tests.checkStatus(BusKnockoutTmr, 15, descr="KN_Waehlhebel_BUSKnockOutTimer = 15")]
    else:
        testresult.append(["Auf positive Response ?berpr?fen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 19
    testresult.append(["\x0a 19 Pr?fe nichtfl?chtige Speicherung von BusKnockOut_ctr"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response_diag, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    ECUKnockOut_Ctr_end = None

    if response_diag[0:3] == [98, 2, 202]:
        ECUKnockOut_Ctr_end = response_diag[4]
        if ECUKnockOut_Ctr_end is not None:
            ECUKnockOut_Ctr_end = ECUKnockOut_Ctr_end
        else:
            ECUKnockOut_Ctr_end = 0

        if BUSKnockOut_Ctr_start is not None:
            testresult.append(basic_tests.checkStatus(
                current_status=ECUKnockOut_Ctr_end,
                nominal_status=1,
                descr=" BusKnockOut_ctr == 1 (wird inkrementiert)", ))
    else:
        testresult.append(
            ["Kein Positive response erhalten.  BusKnockOut_Ctr kann nicht auslasen", "FAILED"])

    # test step 20
    testresult.append(["\x0a 20. Pr?fe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 2,
                                           descr=" KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 2 (0x2= Funktion_ausgeloest)")]

    # test step 21
    testresult.append(["\x0a 21.Pr?fe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    if BusKnockoutTmr_start is not None:
        testresult += [
            basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, BusKnockoutTmr_start,
                                    descr=" KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == bus_tmr == 15 (Reset durch SG-Reset)")]

    # test step 22
    testresult.append(["\x0a 22. In extended session Setze BusKnockOut_Tmr auf 16min und NVEM coupling auf Aktiv.und warte 2sec "])
    testresult.append(["\xa0 Change to extended session"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    testresult.append(["\xa0 Setze BusKnockOut_Tmr auf 15, ECUKnockOut_Tmr auf 15 und NVEM coupling auf aktive"])
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x0F, 0x50]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(["?berpr?fen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(2)

    # test step 23
    testresult.append(["\x0a 23.Prufe BusKnockOut_Tmr and speichere den Wert als bus_tmr_2 "])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BusKnockoutTmr_2 = None
    if response[0:3] == [98, 2, 203]:
        testresult.append(["Auf positive Response ?berpr?fen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BusKnockoutTmr_2 = response[4]
        if BusKnockoutTmr_2 is not None:
            if BusKnockoutTmr_2 > 64:
                BusKnockoutTmr_2 = BusKnockoutTmr_2 - 64  # removing the active coupling value bit
            else:
                BusKnockoutTmr_2 = BusKnockoutTmr_2  # No active NVEM coupling
                testresult.append(["\xa0 Gespeichere Wert f?r BusKnockoutTmr_2 (Variable) f?r sp?teren Vergleich ist %s" % BusKnockoutTmr_2])
        else:
            BusKnockoutTmr_2 = 0

        testresult += [basic_tests.checkStatus(BusKnockoutTmr_2, 16, descr="KN_Waehlhebel_BUSKnockOutTimer = 16")]

    else:
        testresult.append(["Auf positive Response ?berpr?fen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 24
    testresult.append(["\x0a 24.Pr?fe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 16,
                                           descr="KN_Waehlhebel_BUSKnockOutTimer = 16")]

    # test step 25
    testresult.append(["\x0a 25. Warte 1,5min"])
    time.sleep(1.5 * 60)

    # test step 26.1
    testresult.append(["\x0a 26.1 Pr?fe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    if BusKnockoutTmr_2 is not None:
        testresult += [
            basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, BusKnockoutTmr_2,
                                    descr=" KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == bus_tmr_2 == 16 (Ausgangswert; Timer l?uft nicht)")]
    else:
        testresult.append(["bus_tmr_2 kann nicht auslesen ", "FAILED"])

    # test step 26.2
    testresult.append(["\x0a 26.2 Pr?fe BusKnockOut_Ctr"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Auf positive Response ?berpr?fen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    BUSKnockOut_Ctr_2 = None

    if response[0:3] == [98, 2, 202]:
        BUSKnockOut_Ctr_2 = response[4]
        if BUSKnockOut_Ctr_2 is not None:
            BUSKnockOut_Ctr_2 = BUSKnockOut_Ctr_2
        else:
            BUSKnockOut_Ctr_2 = 0
        testresult.append(basic_tests.checkStatus(BUSKnockOut_Ctr_2, 1, descr=" BusKnockOut_Ctr = 1"))
    else:
        testresult.append(["Auf positive Response ?berpr?fen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 27
    testresult.append(["\x0a27. KL15 ausschalten und warte 12 sec"])
    hil.cl15_on__.set(0)
    time.sleep(12)

    # test step 28
    testresult.append(
        ["\x0a 28. Senden nur der NM Botschaft, NVEM12 Botschaft und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen."])
    func_nm.hil_ecu_tx_signal_state_for_Knockout()
    hil.NVEM_12__period.setState("an")

    # test step 29
    testresult.append(["\x0a 29.  Pr?fe veto w?rde erkannt"])
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 1,
                                              descr="KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 1 (Veto Aktiv)"))

    # test step 30
    testresult.append(
        ["\x0a 30. Pr?fe 70 s lang, dass KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer eingefroren ist", ""])
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
    testresult.append(
        ["\xa0 KN_Waehlhebel_BusKnockOutTimer blieb %s Sekunden lang konstant bei %s" % (
        sec, KN_Waehlhebel_BusKnockOutTimer), "PASSED"]) \
        if value_boolean else testresult.append(
        ["\xa0 KN_Waehlhebel_BusKnockOutTimer blieb %s Sekunden lang nicht konstant bei %s"
         % (sec, KN_Waehlhebel_BusKnockOutTimer), "FAILED"])

    # test step 31
    testresult.append(["\x0a 31. Wechsel in die Entwicklersession, (in Factory mode security access d?rchf?hren) "
                       "Setze mittels 2E 09 F3: KnockOut_Test_mode  auf 0x4 * (Supress Veto == Active), "
                       "um BUSKnockOut testen zu k?nnen und warte 2sec"])

    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchf?hren", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x04]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Pr?fe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(2)

    # test step 32
    testresult.append(["\x0a 32 Pr?fe kein veto w?rde erkannt."])
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0,
                                              descr="KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 0 (Initwert)"))

    # test step 33
    testresult.append(["\x0a 33 Pr?fe KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer nach 60 Sekunden"])
    time.sleep(60)
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 15,
                                              descr="KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer = 15 (wird dekrementiert)"))

    # test step 34
    testresult.append(["\x0a 34. Warte bis KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer == 0 (Timeout: 15 min)"])
    timeout = 15 * 60
    t_out = timeout + t()
    while t_out > t():
        if hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value.get() == 0:
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer  hat kein auf 0 gesetz in 15min", "FAILED"])
            break

    # test step 35
    testresult.append(["\x0a 35.Pr?fe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 0,
                                           descr="KN_Waehlhebel_BUSKnockOutTimer = 0")]

    # test step 36
    testresult.append(["\x0a 36. Pr?fe, dass nach 60 sekund Kein Reset des SG stattfindet "])
    time.sleep(60)
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0,
                                           descr="KN_Waehlhebel_BUSKnockOutTimer = 0")]

    # test step 37
    testresult.append(["\x0a 37. Pr?fe KN_Waehlhebel:Waehlhebel_Abschaltstufe", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__Waehlhebel_Abschaltstufe__value, 0,
                                           descr="KN_Waehlhebel:Waehlhebel_Abschaltstufe  == 0 (keine_Einschraenkung)")]

    # test step 38
    testresult.append(["\x0a 38. Pr?fe NVEM_12:NVEM_Abschaltstufe", ""])
    testresult += [basic_tests.checkStatus(hil.NVEM_12__NVEM_Abschaltstufe__value, 3, equal=False,
                                           descr="NVEM_12:NVEM_Abschaltstufe__value != 3")]

    # test step 39
    testresult.append(["\x0a 39. Sende NVEM_12:NVEM_Abschaltstufe = 3 (Stufe_3) und warte 500ms", ""])
    hil.NVEM_12__NVEM_Abschaltstufe__value.set(3)
    time.sleep(0.500)

    # test step 40
    testresult.append(["\x0a 40. Pr?fe KN_Waehlhebel:Waehlhebel_Abschaltstufe", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__Waehlhebel_Abschaltstufe__value, 1,
                                           descr="KN_Waehlhebel:Waehlhebel_Abschaltstufe  == 1  (Funktionseinschraenkung)")]

    # test step 41
    testresult.append(["\x0a 41.  Pr?fe, dass Reset des SG stattfindet"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 2,
                                           descr=" KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 2 (0x2= Funktion_ausgeloest)")]

    # test step 42
    testresult.append(["\x0a 42. Schalte alle signal (HIL--> ECU) aus", ""])
    time.sleep(0.280)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=False, all_other_send=False)

    # test step 43
    testresult.append(["\x0a 43. Warte 1 min. und Pr?fe Busruhe", ""])
    time.sleep(60)
    descr, verdict = func_gs.checkBusruhe(daq)
    testresult.append([descr, verdict])

    # test step 44
    testresult.append(["\x0a 44. Schalte alle signal (HIL--> ECU) ein. Schalte KL15 ein und warte 5 sec", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=True, all_other_send=True)
    time.sleep(5)

    # test step 45
    testresult.append(["\x0a 45 Pr?fe nichtfl?chtige Speicherung von BusKnockOut_Tmr"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BusKnockoutTmr = None
    if response[0:3] == [98, 2, 203]:
        testresult.append(["Auf positive Response ?berpr?fen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BusKnockoutTmr = response[4]
        if BusKnockoutTmr is not None:
            if BusKnockoutTmr > 64:
                BusKnockoutTmr = BusKnockoutTmr - 64  # removing the active coupling value bit
                testresult.append(["\xa0 NVEM couplling ist Aktive", "PASSED"])
            else:
                BusKnockoutTmr = BusKnockoutTmr  # No active NVEM coupling
                testresult.append(["\xa0 NVEM couplling ist inaktive", "FAILED"])
        else:
            BusKnockoutTmr = 0

        testresult += [basic_tests.checkStatus(BusKnockoutTmr, 16, descr="BUSKnockOutTimer = 16")]
    else:
        testresult.append(["Auf positive Response ?berpr?fen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 46
    testresult.append(["\x0a 46. Pr?fe nichtfl?chtige Speicherung von BusKnockOut_ctr"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response_diag, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkPositiveResponse(response_diag, request))
    ECUKnockOut_Ctr_end = None

    if response_diag[0:3] == [98, 2, 202]:
        ECUKnockOut_Ctr_end = response_diag[4]
        if ECUKnockOut_Ctr_end is not None:
            ECUKnockOut_Ctr_end = ECUKnockOut_Ctr_end
        else:
            ECUKnockOut_Ctr_end = 0

        if BUSKnockOut_Ctr_start is not None:
            testresult.append(basic_tests.checkStatus(
                current_status=ECUKnockOut_Ctr_end,
                nominal_status=2,
                descr=" BusKnockOut_ctr == 2 (wird inkrementiert)", ))
    else:
        testresult.append(
            ["Kein Positive response erhalten.  BusKnockOut_Ctr kann nicht auslasen", "FAILED"])

    # test step 47
    testresult.append(["\x0a 47. Pr?fe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 2,
                                           descr=" KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 2 (0x2= Funktion_ausgeloest)")]

    # test step 48
    testresult.append(["\x0a 48. Pr?fe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 16,
                                    descr=" KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == bus_tmr_2 == 16 (Reset durch SG-Reset)")]

    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()
    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)