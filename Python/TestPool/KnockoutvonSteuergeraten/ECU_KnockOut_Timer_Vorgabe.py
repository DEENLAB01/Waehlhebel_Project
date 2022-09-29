# ******************************************************************************
# -*- coding: latin1 -*-
# File    : ECU_KnockOut_Timer_Vorgabe.py
# Title   :ECU_KnockOut_Timer_Vorgabe
# Task    : Test for ECU_KnockOut_Timer_Vorgabe
#
# Author  : Devangbhai Patel
# Date    : 05.10.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 27.09.2021 | Devangbhai   | initial
# 1.1  | 22.12.2021 | Devangbhai   | Rework according to test specification
# 1.2  | 03.01.2022 | Devangbhai   | Rework according to test specification
# 1.3  | 14.02.2022 | Devangbhai   | Rework
# 1.4  | 04.03.2022 | Devangbhai   | Added sleep time to adjust the time delay
# 1.5  | 23.03.2022 | Devangbhai   | Added PRM Ticket number
# 1.6  | 05.05.2022 | Devangbhai   | change the value in test step 7 and 29




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
import os
import functions_nm
from functions_nm import _checkStatus


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
    testresult.setTestcaseId("TestSpec_268")

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

    #  test step 1
    testresult.append(["\x0a 1. In extended Session, setze BusKnockOut_Tmr auf 62** und NVEM coupliling auf Inaktive/not Implemented. Warte 1sec"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x0F, 0x3E]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 2
    testresult.append(["\x0a 2. Lese ECUKnockOut_Tmr und speichere den Wert als ecu_tmr_start"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    ecu_tmr_start = None

    if response[0:3] == [98, 2, 203]:
        ecu_tmr_start = response[3]
        if ecu_tmr_start is not None:
            ecu_tmr_start = ecu_tmr_start
        else:
            ecu_tmr_start = 0
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
    if ecu_tmr_start is not None:
        testresult.append(["\xa0 Gespeichere Wert für ECUKnockoutTmr (Variable) für späteren Vergleich ist %s" % ecu_tmr_start, "INFO"])
    else:
        testresult.append(["\xa0 ECUKnockoutTmr kann nicht auslesen ", "FAILED"])

    # test step 3
    testresult.append(["\x0a 3.Setze ECUKnockOut_Tmr auf 5 und warte 1s"])
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x05, 0x3E]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 4
    testresult.append(["\x0a 4.Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer", ""])
    if ecu_tmr_start is not None:
        testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, ecu_tmr_start,
                                           descr="KN_Waehlhebel_ECUKnockOutTimer = 15  (Bus-Wert nicht identisch mit internem Tmr-Wert; Bus-Wert entspricht früherem Tmr-Restwert; in diesem Fall: Vorgabewert, da Tmr nicht dekrementiert wurde)")]
    else:
        testresult.append(["\xa0 N_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer kann nicht mit ecu_tmr_start vergleichen", "FAILED"])

    # test step 5
    testresult.append(["\x0a 5. Prüfe ECUKnockOut_Ctr"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    ECUKnockOut_Ctr_start = None

    if response[0:3] == [98, 2, 202]:

        ECUKnockOut_Ctr_start = response[3]
        if ECUKnockOut_Ctr_start is not None:
            ECUKnockOut_Ctr_start = ECUKnockOut_Ctr_start
        else:
            ECUKnockOut_Ctr_start = 0

    if ECUKnockOut_Ctr_start is not None:
        testresult += [basic_tests.checkStatus(ECUKnockOut_Ctr_start, 0, descr="Prüfe dass ECUKnockOut_Ctr == 0x00)")]
    else:
        testresult.append(["\xa0 ECUKnockOut_Ctr kann nicht auslesen", "FAILED"])

    # test step 6
    testresult.append(["\x0a6. KL15 ausschalten und warte 1sec"])
    hil.cl15_on__.set(0)
    time.sleep(1)

    # test step 7
    testresult.append(["\x0a7.Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 1, descr="KN_Waehlhebel_ECUKnockOut = 1")]

    # test step 8
    testresult.append(["\x0a8. Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer"])
    if ecu_tmr_start is not None:
        testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, ecu_tmr_start , descr="KN_Waehlhebel_ECUKnockOutTimer =  ecu_tmr_start (Restwert ist Vorgabewert, da Tmr nicht dekrementiert wurde)")]
    else:
        testresult.append(["\xa0 KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer kann nicht mit ecu_tmr_start vergleichen", "FAILED"])

    # test step 9
    testresult.append(["\x0a 9.Wechsel in die Entwicklersession, (in Factory mode security access dürchführen) .KnockOut_Test auf 0x1 setzen* und warte 1sec"])
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

    # test step 10
    testresult.append(["\x0a 10. Senden nur der NM Botschaft und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen"])
    func_nm.hil_ecu_tx_signal_state_for_Knockout()

    # test step 11
    testresult.append(["\x0a11.  Prüfe Bus State"])
    req = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    [response, result] = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    expected_resp = [0x62] + diag_ident_KN_TEST_MODE['identifier'] + [0x01]
    testresult.append(["Prüfe  Bus State == Bus Sleep", ""])
    testresult.append(canape_diag.checkResponse(response, expected_resp))

    # test step 12
    testresult.append(["\x0a12.  Prüfe  KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 5, descr=" KN_Waehlhebel_ECUKnockOutTimer = 5")]
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 0, descr="KN_Waehlhebel_ECUKnockOut = 0 (zurückgesetzt, Init)")]


    # test step 13
    testresult.append(["\x0a13. Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer nach 61 Sekunden", ""])
    time.sleep(61)
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 4, descr=" KN_Waehlhebel_ECUKnockOutTimer = 4 (wird dekrementiert)")]

    # test step 14
    testresult.append(["\x0a 14.In extended Session, setze ECUKnockout_Tmr  auf 61 und warte 1s"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x3D, 0x3E]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 15
    testresult.append(["\x0a 15. Prüfe  KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer", ""])
    testresult += [_checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 4, descr=" KN_Waehlhebel_ECUKnockOutTimer = 4 (laufender Timer wird nicht überschrieben)", ticket_id='FehlerId:EGA-PRM-173')]

    # test step 16
    testresult.append(["\x0a 16. Wechsel in die Entwicklersession, (in Factory mode security access dürchführen) . KnockOut_Test auf 0x3 setzen (Veto) und warte 1s"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)
    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x03]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 17
    testresult.append(["\x0a17. Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer", ""])
    testresult += [_checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 4, descr=" KN_Waehlhebel_ECUKnockOutTimer = 4 (Timer wird bei auftretendem Veto nicht überschrieben)", ticket_id='FehlerId:EGA-PRM-173')]

    testresult.append(["\x0a18. In extended Session, setze ECUKnockOut_Tmr auf 32 und warte 1s", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x20, 0x3E]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 19
    testresult.append(["\x0a 19. Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer", ""])
    testresult += [_checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 4, descr=" KN_Waehlhebel_ECUKnockOutTimer = 4 (Timer wird bei auftretendem Veto nicht überschrieben)", ticket_id='FehlerId:EGA-PRM-173')]

    # test step 20
    testresult.append(["\x0a 20. Wechsel in die Entwicklersession, (in Factory mode security access dürchführen) .KnockOut_Test auf 0x1 setzen*. Warte 1s "])
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

    # test step 21
    testresult.append(["\x0a21. Warte bis  KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer == 3", ""])
    timeout = 1 * 60
    t_out = timeout + t()
    while t_out > t():
        if hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value.get() == 3:
            break
        elif t_out > t() == False:
            testresult.append(["\xa0 KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value hat kein auf 3 gesetz in 1 min", "FAILED"])
            break
    # testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 3, descr=" KN_Waehlhebel_ECUKnockOutTimer = 3")]
    testresult += [_checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 3, descr=" KN_Waehlhebel_ECUKnockOutTimer = 3", ticket_id='FehlerId:EGA-PRM-173')]


    # test step 22
    testresult.append(["\x0a 22. Prüfe ECUKnockOut_Ctr"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    ECUKnockOut_Ctr_middle = None

    if response[0:3] == [98, 2, 202]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        ECUKnockOut_Ctr_middle = response[3]
        if ECUKnockOut_Ctr_middle is not None:
            ECUKnockOut_Ctr_middle = ECUKnockOut_Ctr_middle
        else:
            ECUKnockOut_Ctr_middle = 0

    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    if ECUKnockOut_Ctr_middle is not None:
        testresult += [basic_tests.checkStatus(ECUKnockOut_Ctr_middle, 0, descr="Prüfe dass ECUKnockOut_Ctr == 0x00)")]
    else:
        testresult.append(["\xa0 ECUKnockOut_Ctr kann nicht auslesen", "FAILED"])

    # test step 23
    testresult.append(["\x0a 23. Schalte Senden von alle RX Signalen (HiL --> ECU) ein, Schalte Kl15 ein und warte 2sec"])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=True, all_other_send=True)
    time.sleep(2)

    # test step 24
    testresult.append(["\x0a24. Prüfe ECUKnockOut_Tmr"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    ecu_tmr = None
    if response[0:3] == [98, 2, 203]:
        ecu_tmr = response[3]
        if ecu_tmr is not None:
            ecu_tmr = ecu_tmr
        else:
            ecu_tmr = 0
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    if ecu_tmr is not None:
        testresult += [basic_tests.checkStatus(ecu_tmr, 32, descr="Prüfe dass ECUKnockOut_Tmr == 32)")]
    else:
        testresult.append(["ECUKnockOut_Tmr kann nicht auslesen", "FAILED"])

    # test step 25
    testresult.append(["\x0a25. Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer", ""])
    testresult += [_checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 3, descr=" KN_Waehlhebel_ECUKnockOutTimer = 3  (Restwert) ", ticket_id='FehlerId:EGA-PRM-173')]


    # test step 26
    testresult.append(["\x0a 26. Prüfe ECUKnockOut_Ctr"])
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
        testresult.append(["ECUKnockOut_Ctr kann nicht auslesen", "FAILED"])

    # tests tep 27
    testresult.append(["\x0a 27.Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 1, descr="KN_Waehlhebel_ECUKnockOut = 1(Veto war aktiv, keine Abschaltung)")]

    # test step 28
    testresult.append(["\x0a 28. KL15 ausschalten und warte 1sec"])
    hil.cl15_on__.set(0)
    time.sleep(1)

    # test step 29
    testresult.append(["\x0a 29.Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 1, descr="KN_Waehlhebel_ECUKnockOut = 1")]

    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()
    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)