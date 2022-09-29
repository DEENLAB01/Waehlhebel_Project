# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Bus_KnockOut_3.py
# Title   : Bus_KnockOut_3.py
# Task    : Test for Bus KnockOut with NVEM is set to ON with NVEM 12 timeout
#
# Author  : Devangbhai Patel
# Date    : 17.03.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 17.03.2022 | Devangbhai   | initial
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList
from diag_identifier import identifier_dict
import functions_common
from ttk_checks import basic_tests
from ttk_daq import eval_signal
import functions_gearselection
import time
import functions_nm
# from functions_nm import hil_ecu_tx_signal_state_for_Knockout
from time import time as t
import os
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

    KN_Waehlhebel_BusKnockOutTimer = hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value
    KN_Waehlhebel_BusKnockOut = hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value
    NVEM_Abschaltstufe = hil.NVEM_12__NVEM_Abschaltstufe__value

    meas_vars = [KN_Waehlhebel_BusKnockOutTimer, KN_Waehlhebel_BusKnockOut, NVEM_Abschaltstufe]
    measure_signal = [hil.ClampControl_01__KST_KL_15__value,
                      hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value,
                      hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value,
                      hil.NVEM_12__period]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_382")

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
    testresult.append(["Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["\x0a1 In extended session Setze BusKnockOut_Tmr auf 16min und NVEM coupling auf Aktiv und warte 2sec"])
    testresult.append(["\xa0 Change to extended session"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    testresult.append(["\xa0 Setze BusKnockOut_Tmr und auf 16 min und NVEM coupling auf active"])
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x0F, 0x50]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(2)

    # test step 2
    testresult.append(["\x0a 2 Prüfe BusKnockOut_Tmr == 16 bus_tmr "])
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
                testresult.append(["\xa0 Gespeichere Wert für BusKnockoutTmr_start (Variable) für späteren Vergleich ist %s" % BusKnockoutTmr_start])
        else:
            BusKnockoutTmr_start = 0
            testresult.append(["\xa0 Gespeichere Wert für BusKnockoutTmr_start (Variable) für späteren Vergleich ist %s" % BusKnockoutTmr_start])

        testresult += [basic_tests.checkStatus(BusKnockoutTmr_start, 16, descr="BUSKnockOutTimer = 16")]

    # test step 3
    testresult.append(["\x0a3 Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == 16"])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 16, descr="KN_Waehlhebel_BusKnockOutTimer = 16")]

    # test step 4
    testresult.append(["\x0a4 Warte 1,5min"])
    time.sleep(1.5*60)

    # test step 5.1
    testresult.append(["\x0a5.1 Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == 16 (Ausgangswert: Timer läuft nicht) "])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 16,
                                descr="KN_Waehlhebel_BusKnockOutTimer = 16"),
    ]

    # test step 5.2
    testresult.append(["\x0a 5.2 BusKnockOut_Ctr "])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    BUSKnockOut_Ctr_start = None

    if response[0:3] == [98, 2, 202]:
        BUSKnockOut_Ctr_start = response[4]
        if BUSKnockOut_Ctr_start is not None:
            BUSKnockOut_Ctr_start = BUSKnockOut_Ctr_start
        else:
            BUSKnockOut_Ctr_start = 0
        testresult.append(basic_tests.checkStatus(BUSKnockOut_Ctr_start, 0, descr=" BusKnockOut_Ctr = 0"))

    # test step 6
    testresult.append(["\x0a 6 Start DAQ Measurement"])
    daq.startMeasurement(measure_signal)

    # test step 7
    testresult.append(["\x0a7 KL15 ausschalten und warte 12sec"])
    hil.cl15_on__.set(0)
    time.sleep(12)

    # test step 8
    testresult.append(["\x0a 8 Senden nur der NM Botschaft, Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen. (Timeout der NVEM 12 Botschaft)"])
    func_nm.hil_ecu_tx_signal_state_for_Knockout()

    # test step 9
    testresult.append(["\x0a 9 Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 1  (0x1= Veto_aktiv)"])
    #testresult += [
     #   basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 1,
    #                            descr="KN_Waehlhebel_BusKnockOut = 1 (0x1= Veto_aktiv)"),
    #]
    testresult.append(_checkStatus(current_status=hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value,
                                   nominal_status=1,
                                   descr="KN_Waehlhebel_BusKnockOut = 1 (0x1= Veto_aktiv) ist",
                                   ticket_id='FehlerId:EGA-PRM-149'))

    # test step 10
    testresult.append(["\x0a10 Prüfe 70 s lang, dass KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer eingefroren ist"])
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

    # test step 11
    testresult.append(["\x0a11 Wechsel in die Entwicklersession, (in Factory mode security access dürchführen) und warte 2sec"])
    testresult.append(["[.] Wechsel in Factory Mode:  0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    testresult.append(["[.] Seed anfragen: 0x2761"])
    seed, result = canape_diag.requestSeed()
    testresult.append(["\xa0 Auf positive Response überprüfen", ""])
    testresult.extend(result)

    testresult.append(["[.] Key berechnen:"])
    key, result = canape_diag.calculateKey(seed)
    testresult.append(result)

    testresult.append(["[.] Key senden: 0x2762 + {}:".format(HexList(key))])
    result = canape_diag.sendKey(key)
    testresult.append(["\xa0 Auf positive Response überprüfen", ""])
    testresult.extend(result)

    testresult.append(["[.] KnockOut_Test_mode auf 0x4 setzen"])
    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x4]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(2)

    # test step 12
    testresult.append(["\x0a12 Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 0  (0x0= kein Veto erkannt)"])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0,
                                descr="KN_Waehlhebel_BusKnockOut = 0 (0x0= Funktion_nicht_ausgeloest)"),
    ]

    # test step 13
    testresult.append(["\x0a13 Prüfe KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer nach 60 Sekunden"])
    time.sleep(60)
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 15, descr="KN_Waehlhebel_BusKnockOutTimer = 15"),
    ]

    # test step 14
    testresult.append(["\x0a14. Prüfe KN_Waehlhebel:Waehlhebel_Abschaltstufe = 0 (keine_Einschraenkung)"])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__Waehlhebel_Abschaltstufe__value, 0,
                                descr="KN_Waehlhebel_Abschaltstufe = 0"),
    ]

    # teststep 15
    testresult.append(["\x0a15. Warte bis KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer == 0 (Timeout: 15min)"])
    # warte bis timer = 0
    timeout = 15* 60
    t_out = timeout + t()
    while t_out > t():
        if hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value.get() == 0:
            testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 0,
                                        descr="KN_Waehlhebel_BusKnockOutTimer = 0"),
            ]
            break
        elif t_out > t() == False:
            testresult.append(["\xa0 KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer  hat kein auf 0 gesetz in 15min", "FAILED"])
            break

    # Test step 16
    testresult.append(["\x0a 16. Schalte alle signal (HIL--> ECU) aus und Stoppe Measurement", ""])
    time.sleep(0.500)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=False, all_other_send=False)
    daq_data = daq.stopMeasurement()

    # test step 17
    testresult.append(["\x0a 17. Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 2 (0x2= Funktion_ausgeloest)"])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 2,
                                descr="KN_Waehlhebel_BusKnockOut = 2 (0x2= Funktion_ausgeloest)"),
    ]


    # teststep 18
    testresult.append(["\x0a 18. Warte 1 min. und Prüfe Busruhe"])
    time.sleep(60)
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    testresult.append([descr, verdict])

    # test step 19
    testresult.append(["\x0a 19. Schalte alle signal (HIL--> ECU) ein und warte 5sec", ""])
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=True, all_other_send=True)
    hil.cl15_on__.set(1)
    time.sleep(5)

    # teststep 20
    testresult.append(["\x0a 20 Prüfe BusKnockOut_Tmr == 16 bus_tmr "])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    BusKnockoutTmr = None
    if response[0:3] == [98, 2, 203]:
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

    # test step 21
    testresult.append(["\x0a 21. Prüfe nichtflüchtige Speicherung von BusKnockOut_Ctr "])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response_diag, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Auf positive Response überprüfen", ""])
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
                nominal_status=1,
                descr=" BusKnockOut_ctr == 1 (wird inkrementiert)", ))

    # teststep 22
    testresult.append(["\x0a 22. Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 2  (0x2= Funktion ausgeloest)"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 2,
                               descr="KN_Waehlhebel_BusKnockOut = 2  (0x2= Funktion ausgeloest)")]

    # testresult.append(_checkStatus(current_status=hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value,
    #                                nominal_status=0,
    #                                descr="KN_Waehlhebel_BusKnockOut = 0 (0x0= Funktion_nicht_ausgeloest) ist",
    #                                ticket_id='FehlerId:EGA-PRM-149'))

    # teststep 23
    testresult.append(["\x0a 23. Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer = 16(bus_tmr) == (Reset durch SG-Reset)"])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 16,
                                descr="KN_Waehlhebel_BusKnockOutTimer = 16"),
    ]

    # teststep 24.
    testresult.append(["\x0a 24. Start Analyse of DAQ Measurement", ""])
    testresult.append(["\n Messdatenauswertung: KN_Waehlhebel Signale", ""])
    plot_data = {}
    for mes in measure_signal:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))



    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)