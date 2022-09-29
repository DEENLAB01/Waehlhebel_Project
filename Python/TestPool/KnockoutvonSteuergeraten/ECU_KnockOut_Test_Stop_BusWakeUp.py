# ******************************************************************************
# -*- coding: latin1 -*-
# File    : ECU_KnockOut_Test_Stop_BusWakeUp.py
# Title   :ECU_KnockOut_Test_Stop_BusWakeUp
# Task    : Test for ECU_KnockOut_Test_Stop_BusWakeUp
#
# Author  : Devangbhai Patel
# Date    : 06.10.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 05.10.2021 | Devangbhai   | initial
# 1.1  | 03.01.2022 | Devangbhai   | Rework according to test specification
# 1.2  | 14.02.2022 | Devangbhai   | Rework according to new specification
# 1.3  | 03.03.2022 | Devangbhai | Added sleep time to adjust the time delay
# 1.4  | 22.03.2022 | Devangbhai | Reworked according to the new test specification (Reply from Matricz)


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
    testresult.setTestcaseId("TestSpec_271")

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

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # test step 1
    testresult.append(["\x0a 1. In extended Session, setze ECUKnockOut_Tmr auf 12, BusKnockout_Tmr auf 15 und NVEM coupling auf Inactive/Not Implemented"])
    testresult.append(["\xa0 Change to extended session", "INFO"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x0C, 0x0F]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 2
    testresult.append(["\x0a 2. Prüfe BusKnockOut_Tmr"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BusKnockoutTmr_start = None
    ECUKnockoutTmr_start = None
    if response[0:3] == [98, 2, 203]:
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BusKnockoutTmr_start = response[4]
        ECUKnockoutTmr_start = response[3]
        if BusKnockoutTmr_start is not None:
            BusKnockoutTmr_start = BusKnockoutTmr_start
        else:
            BusKnockoutTmr_start = 0
        if ECUKnockoutTmr_start is not None:
            ECUKnockoutTmr_start = ECUKnockoutTmr_start
        else:
            ECUKnockoutTmr_start = 0
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    if BusKnockoutTmr_start and ECUKnockoutTmr_start is not None:
        testresult.append(basic_tests.compare(BusKnockoutTmr_start, '>', ECUKnockoutTmr_start,
                                              descr="Prüfe dass BusKnockOut_Tmr > ECUKnockOut_Tmr"))
    else:
        testresult.append(["\xa0 ECU/BUSKnockout_TMR kann nicht auslesen ", "FAILED"])

    # test step 3
    testresult.append(["\x0a 3. Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer", ""])
    # time.sleep(61)
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 15,
                                           descr=" KN_Waehlhebel_ECUKnockOutTimer = 15")]

    # test step 4
    testresult.append(["\x0a 4. Prüfe ECUKnockOut_Ctr"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    ECUKnockOut_Ctr_start = None

    if response[0:3] == [98, 2, 202]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        ECUKnockOut_Ctr_start = response[3]
        if ECUKnockOut_Ctr_start is not None:
            ECUKnockOut_Ctr_start = ECUKnockOut_Ctr_start
        else:
            ECUKnockOut_Ctr_start = 0
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    if ECUKnockOut_Ctr_start is not None:
        testresult += [basic_tests.checkStatus(ECUKnockOut_Ctr_start, 0, descr="Prüfe dass ECUKnockOut_Ctr == 0x00)")]
    else:
        testresult.append(["\xa0 ECUKnockOut_Ctr kann nicht auslesen", "FAILED"])

    # test step 5
    testresult.append(["\x0a5. KL15 ausschalten"])
    hil.cl15_on__.set(0)

    # test step 6
    testresult.append(["\x0a 6. Prüfe Bus State", ""])
    request = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    bus_sleep = None

    if response[0:3] == [98, 9, 243]:
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        bus_sleep = response[3]
        testresult.append(["Prüfe dass Bus State != Bus Sleep", ""])
        testresult += [basic_tests.checkStatus(bus_sleep, 1, equal=False, descr="Prüfe dass Bus State != Bus Sleep")]
    else:
        testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        testresult.append(["\xa0 Kein Positive response erhalten.  Bus State kann nicht auslasen", "FAILED"])

    # test step 7
    testresult.append(["\x0a 7. In den Factory session wechsel und Security Access durchführen. KnockOut_Test auf 0x1 setzen (Bit 1: Bus State == Bus Sleep)"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x01]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 8
    testresult.append(["\x0a 8.  Prüfe Bus State"])
    req = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    [response, result] = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    expected_resp = [0x62] + diag_ident_KN_TEST_MODE['identifier'] + [0x01]
    testresult.append(["Prüfe  Bus State == Bus Sleep", ""])
    testresult.append(canape_diag.checkResponse(response, expected_resp))

    # test step 9
    testresult.append(["\x0a 9. Senden nur der NM Botschaft und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen"])
    func_nm.hil_ecu_tx_signal_state_for_Knockout()

    # test step 10
    testresult.append(["\x0a 10.  Prüfe  KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 12,
                                           descr=" KN_Waehlhebel_ECUKnockOutTimer = 12")]

    # test step 11
    testresult.append(["\x0a 11. Prüfe, dass KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer nach 1 Minute um 1 dekrementiert wird", ""])
    time.sleep(1 * 60)
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 11, descr=" KN_Waehlhebel_ECUKnockOutTimer = 11 (wird dekrementiertr)")]

    # test step 12
    testresult.append(["\x0a 12.  In den Factory session wechsel und Security Access durchführen. KnockOut_Test auf 0x0 setzen (Testfunktion deaktiviert; Bus State != Bus Sleep)"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)
    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x00]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 13
    testresult.append(["\x0a 13. Prüfe Bus State", ""])
    request = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    bus_sleep = None

    if response[0:3] == [98, 9, 243]:
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        bus_sleep = response[3]
        testresult.append(["Prüfe dass Bus State != Bus Sleep", ""])
        testresult += [basic_tests.checkStatus(bus_sleep, 1, equal=False, descr="Prüfe dass Bus State != Bus Sleep (Bus-WakeUp)")]
    else:
        testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        testresult.append(["\xa0 Kein Positive response erhalten.  Bus State kann nicht auslasen", "FAILED"])

    # test step 14
    testresult.append(["\x0a 14. Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 11, descr="  KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer == 11 (Reset durch Bus State != Bus Sleep)(Wert vor letztem Bus-WakeUp)")]

    # test step 15
    testresult.append(["\x0a 15.Prüfe 70 s lang, dass KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer eingefroren ist", ""])
    timerlist = []

    KN_Waehlhebel_ECUKnockOutTimer = 11
    sec = 70
    timeout = sec + t()
    value_boolean = True

    while timeout > t():
        timerlist.append(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value.get())

    for timer_values in timerlist:
        if KN_Waehlhebel_ECUKnockOutTimer != timer_values:
            value_boolean = False
            break
    testresult.append(["\xa0 KN_Waehlhebel_ECUKnockOutTimer blieb %s Sekunden lang konstant bei %s"
                       % (sec, KN_Waehlhebel_ECUKnockOutTimer), "PASSED"]) if value_boolean \
        else testresult.append(["\xa0 KN_Waehlhebel_ECUKnockOutTimer blieb %s Sekunden lang nicht konstant bei %s"
                                % (sec, KN_Waehlhebel_ECUKnockOutTimer), "FAILED"])

    # test step 16
    testresult.append(["\x0a 16.  Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 0, descr="KN_Waehlhebel_ECUKnockOut = 0x0")]

    # test step 17
    testresult.append(["\x0a 17. Schalte Senden von RX Signalen (HiL --> ECU) ein, Schalte Kl15 ein", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=True, all_other_send=True)

    # test step 18
    testresult.append(["\x0a 18. Warte 10s"])
    time.sleep(10)

    # test step 19
    testresult.append(["\x0a 19. KL15 ausschalten und warte 2sec"])
    hil.cl15_on__.set(0)
    time.sleep(2)

    # test step 20
    testresult.append(["\x0a 20. Prüfe Bus State", ""])
    request = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    bus_sleep = None

    if response[0:3] == [98, 9, 243]:
        bus_sleep = response[3]
        testresult.append(["Prüfe dass Bus State != Bus Sleep", ""])
        testresult += [basic_tests.checkStatus(bus_sleep, 1, equal=False, descr="Prüfe dass Bus State != Bus Sleep")]
    else:
        testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        testresult.append(["\xa0 Kein Positive response erhalten.  Bus State kann nicht auslasen", "FAILED"])

    # test step 21
    testresult.append(["\x0a 21. In den Factory session wechsel und Security Access durchführen. KnockOut_Test auf 0x5 setzen (Bit 1 und 3: Bus State == Bus Sleep und Vetos unterdrückt (intern und von Testfunktion, Bit 2)) und warte 2sec"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)
    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x05]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(2)

    # test step 22
    testresult.append(["\x0a 22. Prüfe Bus State", ""])
    request = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    bus_sleep = None

    if response[0:3] == [98, 9, 243]:
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        bus_sleep = response[3]
        testresult.append(["Prüfe dass Bus State = Bus Sleep", ""])
        testresult += [
            basic_tests.checkStatus(bus_sleep, 5, descr="Prüfe dass (Bit 1 und 3: Bus State == Bus Sleep und Vetos unterdrückt (intern und von Testfunktion, Bit 2)")]
    else:
        testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        testresult.append(["\xa0 Kein Positive response erhalten.  Bus State kann nicht auslasen", "FAILED"])

    # test step 23
    testresult.append(["\x0a 23. Senden nur der NM Botschaft und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen"])
    func_nm.hil_ecu_tx_signal_state_for_Knockout()

    # test step 24
    testresult.append(["\x0a 24. Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 12,
                                           descr=" KN_Waehlhebel_ECUKnockOutTimer = 12 ")]

    # test step 25
    testresult.append(["\x0a 25. Prüfe, dass KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer nach 1 Minute um 1 dekrementiert wird", ""])
    time.sleep(60)
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 11,
                                           descr=" KN_Waehlhebel_ECUKnockOutTimer = 11 ")]

    # test step 26
    testresult.append(["\x0a 26.  Warte bis KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer == 10 (Timeout: 61 s)", ""])
    timeout = 61
    t_out = timeout + t()
    while t_out > t():
        if hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value.get() == 10:
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value hat kein auf 10 gesetz in 61 sec",
                 "FAILED"])
            break
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 10,
                                           descr=" KN_Waehlhebel_ECUKnockOutTimer = 10")]

    # test step 27
    testresult.append(["\x0a 27. In den Factory session wechsel und Security Access durchführen. KnockOut_Test auf 0x0 setzen (Testfunktion deaktiviert; Bus State != Bus Sleep)"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x00]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 28
    testresult.append(["\x0a 28. Prüfe Bus State", ""])
    request = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    bus_sleep = None

    if response[0:3] == [98, 9, 243]:
        bus_sleep = response[3]
        testresult.append(["Prüfe dass Bus State != Bus Sleep", ""])
        testresult += [
            basic_tests.checkStatus(bus_sleep, 1, equal=False, descr="Prüfe dass Bus State != Bus Sleep (Bus-WakeUp)")]
    else:
        testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        testresult.append(["\xa0 Kein Positive response erhalten.  Bus State kann nicht auslasen", "FAILED"])

    # test step 29
    testresult.append(["\x0a 29. Prüfe KN_Waehlhebel: KN_Waehlhebel_ECUKnockOutTimer", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 10, descr=" KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer == 10 (Reset durch Bus State != Bus (Wert vor letztem Bus-WakeUp)")]

    # test step 30
    testresult.append(["\x0a 30.Prüfe 70 s lang, dass KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer eingefroren ist", ""])
    timerlist = []
    KN_Waehlhebel_ECUKnockOutTimer = 10
    sec = 70
    timeout = sec + t()
    value_boolean = True

    while timeout > t():
        timerlist.append(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value.get())

    for timer_values in timerlist:
        if KN_Waehlhebel_ECUKnockOutTimer != timer_values:
            value_boolean = False
            break
    testresult.append(["\xa0 KN_Waehlhebel_ECUKnockOutTimer blieb %s Sekunden lang konstant bei %s"
                       % (sec, KN_Waehlhebel_ECUKnockOutTimer), "PASSED"]) if value_boolean \
        else testresult.append(["\xa0 KN_Waehlhebel_ECUKnockOutTimer blieb %s Sekunden lang nicht konstant bei %s"
                                % (sec, KN_Waehlhebel_ECUKnockOutTimer), "FAILED"])

    # test step 31
    testresult.append(["\x0a 31.  Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 0, descr="KN_Waehlhebel_ECUKnockOut = 0x0")]

    # test step 32
    testresult.append(["\xa0 32. Schalte Senden von RX Signalen (HiL --> ECU) ein, Schalte Kl15 ein", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=True, all_other_send=True)
    hil.cl15_on__.set(1)

    # test step 33
    testresult.append(["\x0a 33. Warte 10s"])
    time.sleep(10)

    # test step 34
    testresult.append(["\x0a 34. KL15 ausschalten"])
    hil.cl15_on__.set(0)

    # test step 35
    testresult.append(["\x0a 35. Prüfe Bus State", ""])
    request = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    bus_sleep = None

    if response[0:3] == [98, 9, 243]:
        bus_sleep = response[3]
        testresult.append(["Prüfe dass Bus State != Bus Sleep", ""])
        testresult += [basic_tests.checkStatus(bus_sleep, 1, equal=False, descr="Prüfe dass Bus State != Bus Sleep")]
    else:
        testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        testresult.append(["\xa0 Kein Positive response erhalten.  Bus State kann nicht auslasen", "FAILED"])

    # test step 36
    testresult.append(["\x0a 36. In den Factory session wechsel und Security Access durchführen. KnockOut_Test auf 0x7 setzen (Bit 1, 2 und 3: Bus State == Bus Sleep, Test-Veto aktiv, aber Vetos unterdrückt (intern und von Testfunktion, Bit 2))"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x07]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0 Prüfe Negative Response: 0x7F, 0x2E, 0x31 ist"])
    testresult.append(canape_diag.checkNegativeResponse(response, request, 0x31))

    # test step 37
    testresult.append(["\x0a 37. Prüfe Bus State", ""])
    request = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    bus_sleep = None
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    if response[0:3] == [98, 9, 243]:
        bus_sleep = response[3]
        testresult.append(["Prüfe dass Bus State != Bus Sleep", ""])
        testresult += [
            basic_tests.checkStatus(bus_sleep, 0, descr="Prüfe dass Bus State != Bus Sleep")]
    else:
        testresult.append(["\xa0 Kein Positive response erhalten.  Bus State kann nicht auslasen", "FAILED"])

    # test step 38
    testresult.append(["\x0a 38. Senden nur der NM Botschaft und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen"])
    func_nm.hil_ecu_tx_signal_state_for_Knockout()

    # test step 39
    testresult.append(["\x0a 39. Prüfe KN_Waehlhebel_ECUKnockOutTimer", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 10, descr=" KN_Waehlhebel_ECUKnockOutTimer = 10 ")]

    # test step 40
    testresult.append(["\x0a 40. Prüfe 70 s lang, dass KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer konstant bleibt", ""])
    timerlist = []
    KN_Waehlhebel_ECUKnockOutTimer = 10
    sec = 70
    timeout = sec + t()
    value_boolean = True

    while timeout > t():
        timerlist.append(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value.get())

    for timer_values in timerlist:
        if KN_Waehlhebel_ECUKnockOutTimer != timer_values:
            value_boolean = False
            break
    testresult.append(["\xa0 KN_Waehlhebel_ECUKnockOutTimer blieb %s Sekunden lang konstant bei %s"
                       % (sec, KN_Waehlhebel_ECUKnockOutTimer), "PASSED"]) if value_boolean \
        else testresult.append(["\xa0 KN_Waehlhebel_ECUKnockOutTimer blieb %s Sekunden lang nicht konstant bei %s"
                                % (sec, KN_Waehlhebel_ECUKnockOutTimer), "FAILED"])

    # test step 41
    testresult.append(["\x0a 41.  Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 0, descr="KN_Waehlhebel_ECUKnockOut = 0x0")]

    # test step 42
    testresult.append(["\x0a 42. Prüfe ECUKnockOut_Ctr"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    ECUKnockOut_Ctr_end = None

    if response[0:3] == [98, 2, 202]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        ECUKnockOut_Ctr_end = response[3]
        if ECUKnockOut_Ctr_end is not None:
            ECUKnockOut_Ctr_end = ECUKnockOut_Ctr_end
        else:
            ECUKnockOut_Ctr_end = 0
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    if ECUKnockOut_Ctr_end is not None:
        testresult += [basic_tests.checkStatus(ECUKnockOut_Ctr_end, 0, descr="Prüfe dass ECUKnockOut_Ctr == 0x00)")]
    else:
        testresult.append(["\xa0 ECUKnockOut_Ctr kann nicht auslesen ", "FAILED"])

    # test step 43
    testresult.append(["\x0a 43. In extended Session, setze ECUKnockOut_Tmr auf 15 setzen"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x0F, 0x0F]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()
    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)