#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Bus_KnockOut_Timer_Vorgabe.py
# Title   : Bus KnockOut Timer Vorgabe
# Task    : BUs KnockOut Timer Vorgabe

# Author  : Devangbhai Patel
# Date    :  05.01.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 05.01.2022 | Devangbhai   | initial
# 1.1  | 10.02.2022 | Devangbhai | Rework according to new specification
# 1.2  | 04.03.2022 | Devangbhai | Added sleep time to adjust the time delay

#******************************************************************************
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
    testresult.setTestcaseId("TestSpec_273")

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
    testresult.append(["\x0a 1. In Extended Sesssion Setze ECUKnockOut_Tmr auf 62** und warte 2s"])
    testresult.append(["\xa0 Change to extended session"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x3E, 0x0F]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(2)

    # test step 2
    testresult.append(["\x0a 2.Setze BUSKnockout_Tmr  auf 61 und warte 2s"])
    request_2 = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x3E, 0x3D]
    response, result = canape_diag.sendDiagRequest(request_2)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request_2))
    time.sleep(2)

    # test step 3
    testresult.append(["\x0a3.Prufe BusKnockOut_Tmr"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    BusKnockoutTmr_start = None

    if response[0:3] == [98, 2, 203]:
        BusKnockoutTmr_start = response[4]
        if BusKnockoutTmr_start is not None:
            if BusKnockoutTmr_start > 64:
                BusKnockoutTmr_start = BusKnockoutTmr_start - 64  # removing the active coupling value bit
            else:
                BusKnockoutTmr_start = BusKnockoutTmr_start  # No active NVEM coupling
        else:
            BusKnockoutTmr_start = 0

        testresult += [basic_tests.checkStatus(BusKnockoutTmr_start, 61, descr="KN_Waehlhebel_BUSKnockOutTimer = 61")]


    # test step 4
    testresult.append(["\x0a 4.Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 61, descr="KN_Waehlhebel_BUSKnockOutTimer = 61")]

    # test step 5
    testresult.append(["\x0a 5.Setze BUSKnockout_Tmr  auf 15 und warte 2s"])
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x3E, 0x0F]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(2)

    # test step 6
    testresult.append(["\x0a 6.Prufe BusKnockOut_Tmr"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BusKnockoutTmr_1 = None

    if response[0:3] == [98, 2, 203]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BusKnockoutTmr_1 = response[4]
        if BusKnockoutTmr_1 is not None:
            if BusKnockoutTmr_1 > 64:
                BusKnockoutTmr_1 = BusKnockoutTmr_1 - 64  # removing the active coupling value bit
            else:
                BusKnockoutTmr_1 = BusKnockoutTmr_1  # No active NVEM coupling
        else:
            BusKnockoutTmr_1 = 0

        testresult += [basic_tests.checkStatus(BusKnockoutTmr_1, 15, descr="KN_Waehlhebel_BUSKnockOutTimer = 15")]
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 7
    testresult.append(["\x0a7. Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer ", ""])
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 15, descr="KN_Waehlhebel_BUSKnockOutTimer = 15"))

    # test step 8
    testresult.append(["\x0a 8. Prüfe  BUSKnockOut_Ctr (22 02 CA)"])
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
        testresult += [basic_tests.checkStatus(BUSKnockOut_Ctr_start, 0, descr=" Prüfe BusKnockOut_Ctr == 0x00")]
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 9
    testresult.append(["\x0a 9.Prüfe kein Veto wurde erkannt", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0, descr="KN_Waehlhebel_BUSKnockOut = 0")]

    # test step 10
    testresult.append(["\x0a 10. KL15 ausschalten und warte 16 sec"])
    hil.cl15_on__.set(0)
    time.sleep(16)

    # tests tep 11
    testresult.append(["\x0a 11. Senden nur der NM Botschaft und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen."])
    func_nm.hil_ecu_tx_signal_state_for_Knockout()

    # test step 12
    testresult.append(["\x0a 12.Prüfe Veto wurde erkannt", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 1, descr="KN_Waehlhebel_BUSKnockOut = 0x1 (Veto erkannt)")]

    # test step 13
    testresult.append(["\x0a 13. Wechsel in die Entwicklersession, (in Factory mode security access dürchführen) "
                       "Setze mittels 2E 09 F3: KnockOut_Test_mode  auf 0x4 * (Supress Veto == Active) und warte 1s"])

    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_2, key_2, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x04]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 14
    testresult.append(["\x0a 14.Prüfe kein Veto wurde erkannt", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0, descr="KN_Waehlhebel_BUSKnockOut = 0")]

    # test step 15
    testresult.append(["\x0a 15. Prüfe, dass KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer nach 60 sekund"])
    time.sleep(60)
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 14,
                                           descr="KN_Waehlhebel_BUSKnockOutTimer = 14 (wird dekrementiert)")]

    # test step 16
    testresult.append(["\x0a 16. In Extended Sesssion Setze BUSKnockOut_Tmr auf 61 und warte 1s"])
    testresult.append(["\xa0 Change to extended session"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x3E, 0x3D]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 17
    testresult.append(["\x0a17. Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer", ""])
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 14, descr="KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == 14 (laufender Timer wird nicht überschrieben)"))

    # test step 18
    testresult.append(["\x0a 18. Warte bis KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer == 13 (Timeout: 1 min)"])
    timeout = 60
    t_out = timeout + t()
    while t_out > t():
        if hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value.get() == 13:
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer  hat kein auf 13 gesetz in 1 min", "FAILED"])
            break
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 13,
                                              descr="KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == 13"))

    # test step 19
    testresult.append(["\x0a 19. Wechsel in die Entwicklersession, (in Factory mode security access dürchführen)"
                       "Setze mittels 2E 09 F3: KnockOut_Test_mode  auf 0x2 * (Veto == Active) und warte 1s, "])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x02]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 20
    testresult.append(["\x0a 20. Warte 60 s"])
    time.sleep(60)

    # test step 21
    testresult.append(["\x0a 21. Prüfe Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer"])
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 13,  descr="KN_Waehlhebel_BUSKnockOutTimer = 13  (Veto aktiv, Timer läuft nicht ab)"))

    # test step 22
    testresult.append(["\x0a 22. In Extended Sesssion Setze BUSKnockOut_Tmr auf 32 und warte 1s"])
    testresult.append(["\xa0 Change to extended session"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x3E, 0x20]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 23
    testresult.append(["\x0a 23. Prüfe KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer"])
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 13, descr="KN_Waehlhebel_BUSKnockOutTimer = 13   (Timer ist eingefroren, d.h. wird nicht überschrieben während Veto aktiv)"))

    # test step 24
    testresult.append(["\x0a 24. Wechsel in die Entwicklersession, (in Factory mode security access dürchführen) "
                       "Setze mittels 2E 09 F3: KnockOut_Test_mode  auf 0x4 * (Supress Veto == Active) und warte 1s"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_2, key_2, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x04]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(1)

    # test step 25
    testresult.append(["\x0a 25.Prüfe kein Veto wurde erkannt", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0, descr="KN_Waehlhebel_BUSKnockOut = 0")]

    # test step 26
    testresult.append(["\x0a 26. Warte bis KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer == 12 (Timeout: 1 min)"])
    timeout = 60
    t_out = timeout + t()
    while t_out > t():
        if hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value.get() == 12:
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer  hat kein auf 12 gesetz in 1 min", "FAILED"])
            break
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 12,
                                              descr="KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == 12"))

    # test step 27
    testresult.append(["\x0a 27. Prüfe  BUSKnockOut_Ctr"])
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
        testresult += [basic_tests.checkStatus(BUSKnockOut_Ctr, 0, descr=" Prüfe BusKnockOut_Ctr == 0x00")]
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 28
    testresult.append(["\x0a 28. Schalte alle signal (HIL--> ECU) ein. Schalte KL15 ein.  (Timer Reset) und warte 1sec", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=True, all_other_send=True)
    time.sleep(1)

    # test step 29
    testresult.append(["\x0a29. Prüfe BusKnockOut_Tmr"])
    testresult.append(["\xa0 Prüfe Diagnoseparameter BUSKnockOut_Tmr (22 02 CB)"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BusKnockoutTmr = None
    if response[0:3] == [98, 2, 203]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BusKnockoutTmr = response[4]
        if BusKnockoutTmr is not None:
            BusKnockoutTmr = BusKnockoutTmr
        else:
            BusKnockoutTmr = 0
        testresult.append(basic_tests.checkStatus(BusKnockoutTmr, 32, descr="Prüfe BusKnockOut_Tmr == 32 (zuletzt gesetzter Wert)"))
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 30
    testresult.append(["\x0a 30. Prüfe KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer"])
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 32, descr="KN_Waehlhebel_BUSKnockOutTimer = 32 (Reset durch KL15; Übernahme des gesetzten Wertes)"))

    # test step 31
    testresult.append(["\x0a 31. Prüfe  BUSKnockOut_Ctr"])
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
        testresult += [basic_tests.checkStatus(BUSKnockOut_Ctr, 0, descr=" Prüfe BusKnockOut_Ctr == 0x00")]
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 32
    testresult.append(["\x0a 32. Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0, descr="KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 0")]

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
