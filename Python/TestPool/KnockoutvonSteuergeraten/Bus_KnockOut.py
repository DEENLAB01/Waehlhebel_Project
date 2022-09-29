# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Bus_KnockOut.py
# Title   : Bus_KnockOut.py
# Task    : Test for Bus KnockOut
#
# Author  : Mohammed Abdul Karim
# Date    : 08.02.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 08.02.2022 | Mohammed   | initial
# 1.1  | 24.02.2022 | Mohammed   | Added Fehler Id
# 1.2  | 25.02.2022 | Devangbhai | Rework
# 1.3  | 03.03.2022 | Devangbhai | Added sleep time to adjust the time delay
# 1.4  | 21.03.2022 | Devangbhai | Added sleep time after knockout in test step 14
# 1.5  | 25.03.2022 | Devangbhai | exchanged the test step 14 and 15


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

    # KN_Waehlhebel_BusKnockOutTimer = hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value
    # KN_Waehlhebel_BusKnockOut = hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value
    # NVEM_Abschaltstufe = hil.NVEM_12__NVEM_Abschaltstufe__value
    #
    # meas_vars = [KN_Waehlhebel_BusKnockOutTimer, KN_Waehlhebel_BusKnockOut, NVEM_Abschaltstufe]

    measure_signal = [hil.ClampControl_01__KST_KL_15__value,
                      hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value,
                      hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value,
                      hil.NVEM_12__NVEM_Abschaltstufe__value]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_204")

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
    testresult.append(["\x0a 1 In extended session Setze BusKnockOut_Tmr auf 15min und NVEM coupling auf Inactive"])
    testresult.append(["\xa0 Change to extended session"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    testresult.append(["\xa0 Setze BusKnockOut_Tmr und auf 15 min und NVEM coupling auf Inactive"])
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x0F, 0x0F]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 2
    testresult.append(["\x0a2.Prufe BusKnockOut_Tmr and speichere den Wert als bus_tmr"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BusKnockoutTmr_start = None
    if response[0:3] == [98, 2, 203]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BusKnockoutTmr_start = response[4]
        if BusKnockoutTmr_start is not None:
            if BusKnockoutTmr_start > 64:
                BusKnockoutTmr_start = BusKnockoutTmr_start - 64  # removing the active coupling value bit
            else:
                BusKnockoutTmr_start = BusKnockoutTmr_start  # No active NVEM coupling
                testresult.append(["\xa0 Gespeichere Wert für BusKnockoutTmr_start (Variable) für späteren Vergleich ist %s" % BusKnockoutTmr_start])
        else:
            BusKnockoutTmr_start = 0

        testresult += [basic_tests.checkStatus(BusKnockoutTmr_start, 15, descr="BUSKnockOutTimer = 15")]

    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 3
    testresult.append(["\x0a 3. Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == 15 "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 15,
                                descr="KN_Waehlhebel_BusKnockOutTimer = 15 (Ausgangswert)") ]

    # test step 4
    testresult.append(["\x0a 4. Warte 1,5min"])
    time.sleep(1.5 * 60)
    # time.sleep(5)

    # test step 5
    testresult.append(["\x0a 5. Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == 15 (Ausgangswert: Timer läuft nicht) "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 15,descr="KN_Waehlhebel_BusKnockOutTimer = 15 (Ausgangswert)")]

    # test step 5.1
    testresult.append(["\x0a 5.1 BusKnockOut_Ctr"])
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

    # test step 6
    testresult.append(["\x0a 6. Start DAQ Measurement:Messung starten"])
    daq.startMeasurement(measure_signal)
    time.sleep(2)

    # test step 7
    testresult.append(["\x0a 7. Kl15 ausschalten und warte 12sec."])
    hil.cl15_on__.set(0)
    time.sleep(12)

    # test step 7.1
    testresult.append(["\x0a 7.1 Senden nur der NM Botschaft und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen."])
    func_nm.hil_ecu_tx_signal_state_for_Knockout()

    # test step 8
    testresult.append(["\x0a 8 Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 1  (0x1= Veto_aktiv)"])
    testresult += [
       basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 1,
                               descr="KN_Waehlhebel_BusKnockOut = 1 (0x1= Veto_aktiv)"),]

    # testresult.append(_checkStatus(current_status=hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value,
    #                                 nominal_status=1,
    #                                 descr="KN_Waehlhebel_BusKnockOut = 1 (0x1= Veto_aktiv) ist",
    #                                 ticket_id='FehlerId:EGA-PRM-149'))
    # test step 9
    testresult.append(["\x0a 9 Prüfe 70 s lang, dass KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer eingefroren ist"])
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
        ["\xa0 KN_Waehlhebel_BusKnockOutTimer blieb %s Sekunden lang konstant bei %s" % (
        sec, KN_Waehlhebel_BusKnockOutTimer), "PASSED"]) \
        if value_boolean else testresult.append(
        ["\xa0 KN_Waehlhebel_BusKnockOutTimer blieb %s Sekunden lang nicht konstant bei %s"
         % (sec, KN_Waehlhebel_BusKnockOutTimer), "FAILED"])

    # test step 10
    testresult.append(["\x0a 10. Wechsel in die Entwicklersession, (in Factory mode security access dürchführen) Setze mittels 2E 09 F3: KnockOut_Test_mode  auf 0x4 * (Supress Veto == Active), um BUSKnockOut testen zu können und warte 2sec"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x04]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    time.sleep(2)

    # test step 11
    testresult.append(["\x0a 11 Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 0  (0x0= kein Veto erkannt)"])
    # testresult += [ basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0, descr="KN_Waehlhebel_BusKnockOut = 0 (0x0= Funktion_nicht_ausgeloest)"),]

    testresult.append(_checkStatus(current_status=hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value,
                                   nominal_status=0,
                                   descr="KN_Waehlhebel_BusKnockOut = 0 (0x0= Funktion_nicht_ausgeloest) ist",
                                   ticket_id='FehlerId:EGA-PRM-149'))
    # test step 12
    testresult.append(["\x0a 12 Prüfe KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer nach 60 Sekunden"])
    time.sleep(60)
    testresult += [ basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 14, descr="KN_Waehlhebel_BusKnockOutTimer = 14")]

    # teststep 13
    testresult.append(["\x0a 13 Warte bis KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer == 0 (Timeout: 14min)"])
    timeout = 14 * 60
    t_out = timeout + t()
    while t_out > t():
        if hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value.get() == 0:
            testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 0,
                                                   descr="KN_Waehlhebel_BusKnockOutTimer = 0")]

            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer  hat kein auf 0 gesetz in 14min", "FAILED"])
            break

    # teststep 14
    testresult.append(["\x0a 14 Prüfe dass  Reset des SG stattfindet"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 2,
                                           descr="KN_Waehlhebel_BusKnockOut = 2 (0x2= Funktion_ausgeloest)")]

    # test step 15
    testresult.append(["\x0a15. Schalte alle signal (HIL--> ECU) aus. und stoppe DAQ messung", ""])
    time.sleep(0.500)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=False, all_other_send=False)
    daq_data = daq.stopMeasurement()


    # teststep 16
    testresult.append(["\x0a 16 Warte 1 min. und Prüfe Busruhe"])
    time.sleep(60)
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    testresult.append([descr, verdict])

    # teststep 17
    testresult.append(["\x0a 17 Schalte alle signal (HIL--> ECU) ein. Schalte KL15 ein und warte 5sec."])
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=True, all_other_send=True)
    hil.cl15_on__.set(1)
    time.sleep(5)

    # teststep 18
    testresult.append(["\x0a 18 Prüfe BusKnockOut_Tmr == 15 bus_tmr "])
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
                testresult.append(["\xa0 NVEM couplling ist Aktive", "FAILED"])
            else:
                BusKnockoutTmr = BusKnockoutTmr  # No active NVEM coupling
                testresult.append(["\xa0 NVEM couplling ist inaktive", "PASSED"])
        else:
            BusKnockoutTmr = 0
        testresult += [basic_tests.checkStatus(BusKnockoutTmr, 15, descr="KN_Waehlhebel_BUSKnockOutTimer = 15")]

    # teststep 19
    testresult.append(["\x0a 19 Prüfe nichtflüchtige Speicherung von BusKnockOut_Ctr"])
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

    # teststep 20
    testresult.append(["\x0a 20. Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 2, descr="KN_Waehlhebel_BusKnockOut = 2 (0x2= Funktion_ausgeloest)")]

    # testresult.append(_checkStatus(current_status=hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value,
    #                                nominal_status=0,
    #                                descr="KN_Waehlhebel_BusKnockOut = 0 (0x0= Funktion_nicht_ausgeloest) ist",
    #                                ticket_id='FehlerId:EGA-PRM-149'))

    # teststep 21
    testresult.append( ["\x0a21 Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer = 15(bus_tmr) == (Reset durch SG-Reset)"])
    testresult += [ basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 15, descr="KN_Waehlhebel_BusKnockOutTimer = 15"),]


    # testresult.append(_checkStatus(current_status=hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value,
    #                                nominal_status=14,
    #                                descr="KN_Waehlhebel_BusKnockOutTimer = 14 ist",
    #                                ticket_id='FehlerId:EGA-PRM-149'))

    # test step 22
    testresult.append(["\x0a22. Start Analyse of DAQ Measurement", ""])
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
