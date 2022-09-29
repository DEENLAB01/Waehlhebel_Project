# ******************************************************************************
# -*- coding: latin1 -*-
# File    : ECU_KnockOut_Daten_Datensicherung.py
# Title   :ECU KnockOut Daten Datensicherung
# Task    : Test for ECU Knockout Daten Datensicherung
#
# Author  : Devangbhai Patel
# Date    : 27.09.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 27.09.2021 | Devangbhai   | initial
# 1.1  | 12.10.2021 | Mohammed     | Rework
# 1.2  | 22.12.2021 | Devangbhai   | Rework according to test specification
# 1.3  | 14.02.2022 | Devangbhai   | Rework according to new specification
# 1.4  | 03.03.2022 | Devangbhai   | Added sleep time to adjust the time delay
# 1.5  | 17.03.2022 | Devangbhai   | Added sleep time after Knockout happens
# 1.6  | 25.07.2022 | Mohammed     | test step 7 aktualisiert

# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
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

    # Initialize variables ####################################################
    diag_ident_KN_CTR = identifier_dict['Knockout_counter']
    diag_ident_KN_TMR = identifier_dict['Knockout_timer']
    diag_ident_KN_TEST_MODE =identifier_dict['Knockout_test_mode']
    func_nm = functions_nm.FunctionsNM(testenv)

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_267")

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
    testresult.append(["\x0a 1. In extended Session setze ECUKnockOut_Tmr auf 3, BusKnockout_Tmr auf 15, unf NVEM coupliling auf Inaktive/not Implemented"])
    testresult.append(["\xa0 Change to extended session", "INFO"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x03, 0x0F]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 2
    testresult.append(["\x0a 2. Prüfe BusKnockOut_Tmr"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    BusKnockoutTmr_start = None
    ECUKnockoutTmr_start = None
    if response[0:3] == [98, 2, 203]:
        BusKnockoutTmr_start = response[4]
        ECUKnockoutTmr_start = response[3]
        if BusKnockoutTmr_start is not None:
            BusKnockoutTmr_start = BusKnockoutTmr_start
            testresult.append(["\xa0 Gespeichere Wert für BusKnockoutTmr_start (Variable) für späteren Vergleich ist %s" % BusKnockoutTmr_start, "INFO"])
        else:
            BusKnockoutTmr_start = 0
            testresult.append(["\xa0 Gespeichere Wert für BusKnockoutTmr_start (Variable) für späteren Vergleich ist %s" % BusKnockoutTmr_start,"INFO"])

        if ECUKnockoutTmr_start is not None:
            ECUKnockoutTmr_start = ECUKnockoutTmr_start
            testresult.append(["\xa0 Gespeichere Wert für ECUKnockoutTmr_start (Variable) für späteren Vergleich ist %s" % ECUKnockoutTmr_start, "INFO"])
        else:
            ECUKnockoutTmr_start = 0
            testresult.append(["\xa0 Gespeichere Wert für ECUKnockoutTmr_start (Variable) für späteren Vergleich ist %s" % ECUKnockoutTmr_start, "INFO"])
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    if BusKnockoutTmr_start and ECUKnockoutTmr_start is not None:
        testresult.append(basic_tests.compare(BusKnockoutTmr_start, '>', ECUKnockoutTmr_start, descr="Prüfe dass BusKnockOut_Tmr > ECUKnockOut_Tmr"))

    else:
        testresult.append(["\xa0 ECU/BUSKnockout_TMR kann nicht auslesen ", "FAILED"])

    # test step 3
    testresult.append(["\x0a 3. Prüfe ECUKnockOut_Ctr"])
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
        testresult += [basic_tests.checkStatus(ECUKnockOut_Ctr_start, 0,
                                               descr=" ECUKnockOut_Ctr = 0")]
    else:
        testresult.append(["\xa0 ECUKnockOut_Ctr kann nicht auslesen ", "FAILED"])

    # test step 4
    testresult.append(["\x0a 4. KL15 ausschalten.  Senden nur der NM Botschaft und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen"])
    hil.cl15_on__.set(0)
    func_nm.hil_ecu_tx_signal_state_for_Knockout()

    # test step 5
    testresult.append(["\x0a  5.In den Factory Mode wechsel und Security Access durchführen. KnockOut_Test auf 0x1 setzen* und warte 2sec"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)
    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x01]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 6
    testresult.append(["\x0a 6. Prüfe Bus State"])
    req = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    [response, result] = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    expected_resp = [0x62] + diag_ident_KN_TEST_MODE['identifier'] + [0x01]
    testresult.append(["Prüfe  Bus State == Bus Sleep", ""])
    testresult.append(canape_diag.checkResponse(response, expected_resp))
    time.sleep(2)

    # test step 7
    testresult.append(["\x0a 7. KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer und NM_Waehlhebel_FCAB == nur 07_Basefunction_CrossSection (andere == '0')", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 3, descr="KN_Waehlhebel_ECUKnockOutTimer = 3")]

    testresult.append(func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [7], [],
                                               descr="Prüfe NM_Waehlhebel_FCAB: nur 07_Basefunction_CrossSection  (andere == '0')"))
    # test step 8
    testresult.append(["\x0a 8. Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer und KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut  nach 61 Sekunden", ""])
    time.sleep(61)
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 2, descr="KN_Waehlhebel_ECUKnockOutTimer = 2 (wird dekrementiert)"),
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 0, descr="KN_Waehlhebel_ECUKnockOut = 0")]

    # test step 9
    testresult.append(["\x0a 9. Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer und KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut nach 60 Sekunden", ""])
    time.sleep(60)
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 1, descr="KN_Waehlhebel_ECUKnockOutTimer = 1 (wird dekrementiert)"),
                   basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 0, descr="KN_Waehlhebel_ECUKnockOut = 0")]

    # test step 10
    testresult.append(["\x0a 10. Prüfe ECUKnockOut_Ctr"])
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
        testresult += [basic_tests.checkStatus(ECUKnockOut_Ctr_middle, 0, descr=" ECUKnockOut_Ctr = 0")]
    else:
        testresult.append(["\xa0 ECUKnockOut_Ctr kann nicht auslesen ", "FAILED"])

    # test step 11
    testresult.append(["\x0a 11. Warte bis KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer == 0 (Timeout: 1 min)", ""])
    timeout = 1 * 60
    t_out = timeout + t()
    while t_out > t():
        if hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value.get() == 0:
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value hat kein auf 0 gesetz in 1 min", "FAILED"])
            break

    # test step 12
    testresult.append(["\x0a 12. Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer, KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 0,
                                           descr="KN_Waehlhebel_ECUKnockOutTimer = 0 "),
                   basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 2,
                                           descr="KN_Waehlhebel_ECUKnockOut = 2")]

    # test step 13
    testresult.append(["\x0a 13. Schalte alle signal (HIL--> ECU) aus", ""])
    time.sleep(0.7)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=False, all_other_send=False)

    # test step 14
    testresult.append(["\x0a 14. Warte 1min und prüfe Busruhe", ""])
    time.sleep(60)
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    testresult.append([descr, verdict])

    # test step 15
    testresult.append(["\x0a 15. Schalte Senden von RX Signalen (HiL --> ECU) ein, Schalte Kl15 ein und warte 5sec", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=True, all_other_send=True)
    time.sleep(5)

    # test step 16
    testresult.append(["\x0a 16. Prüfe nichtflüchtige Speicherung von ECUKnockOut_Tmr, ECUKnockOut_Ctr"])
    testresult.append(["\xa0 ECUKnockOut_Tmr auslesen ", "INFO"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    ECUKnockoutTmr_end = None

    if response[0:3] == [98, 2, 203]:
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        ECUKnockoutTmr_end = response[3]
        if ECUKnockoutTmr_end is not None:
            ECUKnockoutTmr_end = ECUKnockoutTmr_end
        else:
            ECUKnockoutTmr_end = 0
    else:
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    if ECUKnockoutTmr_end is not None:
        testresult.append(basic_tests.compare(ECUKnockoutTmr_end, '==', 3, descr="Prüfe dass ECUKnockOut_tmr == 3"))
    else:
        testresult.append(["\xa0 ECUKnockOut_Tmr kann nicht auslesen ", "FAILED"])

    testresult.append(["\xa0 ECUKnockOut_Ctr auslesen ", "INFO"])
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
        testresult.append(basic_tests.compare(ECUKnockOut_Ctr_end, '==', 1, descr="ECUKnockOut_Ctr == 1 (wurde inkrementiert)"))
    else:
        testresult.append(["\xa0 ECUKnockOut_Ctr kann nicht auslesen ", "FAILED"])

    # test step 17
    testresult.append(["\x0a 17. Prüf ob KnockOut_Test zuruckgesetzt"])
    req = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    [response, result] = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    expected_resp = [0x62] + diag_ident_KN_TEST_MODE['identifier'] + [0x00]
    testresult.append(canape_diag.checkResponse(response, expected_resp))

    # test step 18
    testresult.append(["\x0a 18. Prüfe nichtflüchtige Speicherung von KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer"])
    if ECUKnockoutTmr_end is not None:
        testresult.append(basic_tests.compare(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, '==', ECUKnockoutTmr_end , descr="Prüfe dass  KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer == ECUKnockOut_Tmr = 3"))
        testresult.append(basic_tests.compare(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, '==', 3, descr="Prüfe dass  KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer = 3"))

    else:
        testresult.append(["KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer kann nicht mit  ECUKnockout_Tmr Vergleichen", "FAILED"])
        testresult.append(basic_tests.compare(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, '==', 3, descr="Prüfe dass  KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer = 3"))

    # test step 19
    testresult.append(["\x0a 19. In extended Session setze ECUKnockOut_Tmr auf 1, BusKnockout_Tmr auf 15, unf NVEM coupliling auf Inaktive/not Implemented"])
    testresult.append(["\xa0 Change to extended session", "INFO"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x01, 0x0F]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 20
    testresult.append(["\x0a 20. Prüfe BusKnockOut_Tmr"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    BusKnockoutTmr_start_2 = None
    ECUKnockoutTmr_start_2 = None
    if response[0:3] == [98, 2, 203]:
        BusKnockoutTmr_start_2 = response[4]
        ECUKnockoutTmr_start_2 = response[3]
        if BusKnockoutTmr_start_2 is not None:
            BusKnockoutTmr_start_2 = BusKnockoutTmr_start_2
        else:
            BusKnockoutTmr_start_2 = 0

        if ECUKnockoutTmr_start_2 is not None:
            ECUKnockoutTmr_start_2 = ECUKnockoutTmr_start_2
        else:
            ECUKnockoutTmr_start_2 = 0

    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
    if BusKnockoutTmr_start_2 and ECUKnockoutTmr_start_2 is not None:
        testresult.append(basic_tests.compare(BusKnockoutTmr_start_2, '>', ECUKnockoutTmr_start_2,
                                              descr="Prüfe dass BusKnockOut_Tmr > ECUKnockOut_Tmr"))
    else:
        testresult.append(["\xa0 ECU/BUSKnockout_TMR kann nicht auslesen ", "FAILED"])

    # test step 21
    testresult.append(["\x0a 21. Prüfe ECUKnockOut_Ctr"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    ECUKnockOut_Ctr_start_2 = None

    if response[0:3] == [98, 2, 202]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        ECUKnockOut_Ctr_start_2 = response[3]
        if ECUKnockOut_Ctr_start_2 is not None:
            ECUKnockOut_Ctr_start_2 = ECUKnockOut_Ctr_start_2
        else:
            ECUKnockOut_Ctr_start_2 = 0

    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    if ECUKnockOut_Ctr_start_2 is not None:
        testresult += [basic_tests.checkStatus(ECUKnockOut_Ctr_start_2, 1,
                                               descr=" ECUKnockOut_Ctr = 1")]
    else:
        testresult.append(["ECUKnockOut_Ctr kann nicht auslesen ", "FAILED"])

    # test step 22
    testresult.append(["\x0a 22. KL15 ausschalten.  Senden nur der NM Botschaft und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen"])
    hil.cl15_on__.set(0)
    func_nm.hil_ecu_tx_signal_state_for_Knockout()

    # test step 23
    testresult.append(["\x0a  23.In den Factory Mode wechsel und Security Access durchführen. KnockOut_Test auf 0x1 setzen* und warte 2sec"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)
    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x01]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(2)

    # test step 24
    testresult.append(["\x0a 24. Prüfe Bus State"])
    req = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    [response, result] = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    expected_resp = [0x62] + diag_ident_KN_TEST_MODE['identifier'] + [0x01]
    testresult.append(["Prüfe  Bus State == Bus Sleep", ""])
    testresult.append(canape_diag.checkResponse(response, expected_resp))


    # test step 25
    testresult.append(["\x0a 25. KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 1,
                                           descr="KN_Waehlhebel_ECUKnockOutTimer = 1")]

    # test step 26
    testresult.append(["\x0a 26.  Prüfe ECUKnockOut_Ctr"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    ECUKnockOut_Ctr_start_3 = None

    if response[0:3] == [98, 2, 202]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        ECUKnockOut_Ctr_start_3 = response[3]
        if ECUKnockOut_Ctr_start_3 is not None:
            ECUKnockOut_Ctr_start_3 = ECUKnockOut_Ctr_start_3
        else:
            ECUKnockOut_Ctr_start_3 = 0
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    if ECUKnockOut_Ctr_start_3 is not None:
        testresult += [basic_tests.checkStatus(ECUKnockOut_Ctr_start_3, 1, descr="ECUKnockOut_Ctr = 1")]
    else:
        testresult.append(["ECUKnockOut_Ctr kann nicht auslesen ", "FAILED"])

    # test step 27
    testresult.append(["\x0a 27. Warte bis KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer == 0 (Timeout: 1 min)", ""])
    timeout = 1 * 60
    t_out = timeout + t()
    while t_out > t():
        if hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value.get() == 0:
            break
        elif t_out > t() == False:
            testresult.append(["\xa0 KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value hat kein auf 0 gesetz in 1 min", "FAILED"])
            break

    # test step 28
    testresult.append(["\x0a 28. Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer, KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 0,
                                           descr="KN_Waehlhebel_ECUKnockOutTimer = 0 "),
                   basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 2,
                                           descr="KN_Waehlhebel_ECUKnockOut = 2")]

    # test step 29
    testresult.append(["\x0a 29. Schalte alle signal (HIL--> ECU) aus", ""])
    time.sleep(0.7)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=False, all_other_send=False)

    # test step 30
    testresult.append(["\x0a 30. Warte 1min und prüfe Busruhe", ""])
    time.sleep(60)
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    testresult.append([descr, verdict])

    # test step 31
    testresult.append(["\xa0 31.Schalte Senden von RX Signalen (HiL --> ECU) ein, Schalte Kl15 ein und warte 5sec", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=True, all_other_send=True)
    time.sleep(5)

    # test step 32
    testresult.append(["\x0a 32. Prüfe ECUKnockOut_Tmr"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    ECUKnockoutTmr_end_2 = None
    if response[0:3] == [98, 2, 203]:
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        ECUKnockoutTmr_end_2 = response[3]
        if ECUKnockoutTmr_end_2 is not None:
            ECUKnockoutTmr_end_2 = ECUKnockoutTmr_end_2
        else:
            ECUKnockoutTmr_end_2 = 0
    else:
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    if ECUKnockoutTmr_end_2 is not None:
        testresult.append(basic_tests.compare(ECUKnockoutTmr_end_2, '==', 1, descr="Prüfe dass ECUKnockOut_tmr == 1"))
    else:
        testresult.append(["\xa0 ECUKnockOut_Tmr kann nicht auslesen ", "FAILED"])

    # test step 33
    testresult.append(["\x0a 33. ECUKnockOut_Tmr auslesen "])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    ECUKnockOut_Ctr_end_2 = None
    if response[0:3] == [98, 2, 202]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        ECUKnockOut_Ctr_end_2 = response[3]
        if ECUKnockOut_Ctr_end_2 is not None:
            ECUKnockOut_Ctr_end_2 = ECUKnockOut_Ctr_end_2
        else:
            ECUKnockOut_Ctr_end_2 = 0
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    if ECUKnockOut_Ctr_end_2 is not None:
        testresult.append(
            basic_tests.compare(ECUKnockOut_Ctr_end_2, '==', 2, descr="ECUKnockOut_Ctr == 2 (wurde inkrementiert)"))
    else:
        testresult.append(["ECUKnockOut_Ctr kann nicht auslesen ", "FAILED"])

    # test step 34
    testresult.append(["\x0a 35. Prüfe nichtflüchtige Speicherung von KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer"])
    if ECUKnockoutTmr_end_2 is not None:
        testresult.append(
            basic_tests.compare(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, '==', ECUKnockoutTmr_end_2,
                                descr="Prüfe dass  KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer == ECUKnockOut_Tmr = 1"))
        testresult.append(basic_tests.compare(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, '==', 1,
                                              descr="Prüfe dass  KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer = 1"))
    else:
        testresult.append(["KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer kann nicht mit  ECUKnockout_Tmr Vergleichen", "FAILED"])
        testresult.append(basic_tests.compare(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, '==', 1,
                                              descr="Prüfe dass  KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer = 1"))

    # test step 35
    testresult.append(["\x0a 35. KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 2, descr="KN_Waehlhebel_ECUKnockOut = 2")]

    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()
    # cleanup
    hil = None

finally:
    testenv.breakdown(ecu_shutdown=False)