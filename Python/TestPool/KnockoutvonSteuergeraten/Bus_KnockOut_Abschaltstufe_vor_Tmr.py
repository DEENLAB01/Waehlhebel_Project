# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Bus_KnockOut_Abschaltstufe_vor_Tmr.py
# Title   : Bus_KnockOut_Abschaltstufe_vor_Tmr.py
# Task    : Test for Bus KnockOut Abschaltstufe vor Tmr
#
# Author  : Devangbhai Patel
# Date    : 07.02.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 07.02.2022 | Devangbhai | Initial
# 1.1  | 17.02.2022 | Devangbhai | Added 100ms wait time in test step 18
# 1.2  | 21.02.2022 | Devangbhai | Added 400ms wait time in test step 18
# 1.3  | 24.02.2022 | Devangbhai | Added 100ms wait time in test step 18
# 1.4  | 03.03.2022 | Devangbhai | Added sleep time to adjust the time delay
# 1.5  | 25.05.2022 | Mohammed   | Added Fehler ID

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
    diag_ident_KN_TEST_MODE = identifier_dict['Knockout_test_mode']
    func_nm = functions_nm.FunctionsNM(testenv)

    measure_signal = [hil.ClampControl_01__KST_KL_15__value,
                      hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value,
                      hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value,
                      hil.NVEM_12__NVEM_Abschaltstufe__value]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_329")

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
    testresult.append(canape_diag.checkPositiveResponse(response, request, ticket_id='FehlerID:EGA-PRM-224'))

    testresult.append(["[.] BusKnockOut_Ctr und ECUKnockOut_Ctr auf 0 setzen"])
    request = [0x2E] + diag_ident_KN_CTR['identifier'] + [0x00, 0x00]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request, ticket_id='FehlerID:EGA-PRM-224'))

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

    ###
    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # test step 1
    testresult.append(["\x0a  1. In extended session Setze BusKnockOut_Tmr auf 15min und NVEM coupling auf Aktiv. "])
    testresult.append(["\xa0 Change to extended session"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    testresult.append(["\xa0 BusKnockOut_Tmr auf 15, ECUKnockOut_Tmr auf 15 und NVEM coupling auf aktive"])
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x0F, 0x4F]
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
                BusKnockoutTmr_start = BusKnockoutTmr_start - 64 # removing the active coupling value bit
            else:
                BusKnockoutTmr_start = BusKnockoutTmr_start # No active NVEM coupling
                testresult.append(["\xa0 Gespeichere Wert für BusKnockoutTmr_start (Variable) für späteren Vergleich ist %s" % BusKnockoutTmr_start])
        else:
            BusKnockoutTmr_start = 0

        testresult += [basic_tests.checkStatus(BusKnockoutTmr_start, 15, descr="BUSKnockOutTimer = 15")]

    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 3
    testresult.append(["\x0a 3.Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 15,
                                           descr="KN_Waehlhebel_BUSKnockOutTimer = 15")]

    # test step 4
    testresult.append(["\x0a 4. Warte 1,5min"])
    time.sleep(1.5 *60)

    # test step 5
    testresult.append(["\x0a 5.Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    if BusKnockoutTmr_start is not None:
        testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, BusKnockoutTmr_start,
                                               descr=" Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == bus_tmr == 15 (Ausgangswert; Timer läuft nicht)")]

    # test step 5.1
    testresult.append(["\x0a 5.1. Prüfe BusKnockOut_Ctr"])
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
    testresult.append(["\x0a 6. Messung starten: \n ClampControl_01__KST_KL_15__value, \nKN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer, \nKN_Waehlhebel:KN_Waehlhebel_BusKnockOut, \nNVEM_12:NVEM_Abschaltstufe"])
    daq.startMeasurement(measure_signal)

    # test step 7
    testresult.append(["\x0a7. KL15 ausschalten und warte 11 sec"])
    hil.cl15_on__.set(0)
    time.sleep(11)

    # test step 8
    testresult.append(["\x0a8. Senden nur der NM Botschaft, NVEM 12 und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen."])
    func_nm.hil_ecu_tx_signal_state_for_Knockout()
    hil.NVEM_12__period.setState("an")

    # test step 9
    testresult.append(["\x0a9.  Prüfe veto würde erkannt"])
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 1, descr="KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 1 (Veto Aktiv)"))

    # test step 10
    testresult.append(["\x0a10. Prüfe 70 s lang, dass KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer eingefroren ist", ""])
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
        ["\xa0 KN_Waehlhebel_BusKnockOutTimer blieb %s Sekunden lang konstant bei %s" %(sec, KN_Waehlhebel_BusKnockOutTimer), "PASSED"]) \
        if value_boolean else testresult.append(["\xa0 KN_Waehlhebel_BusKnockOutTimer blieb %s Sekunden lang nicht konstant bei %s"
                                                 %(sec, KN_Waehlhebel_BusKnockOutTimer), "FAILED"])

    # test step 11
    testresult.append(["\x0a 11. Wechsel in die Entwicklersession, (in Factory mode security access dürchführen) "
                       "Setze mittels 2E 09 F3: KnockOut_Test_mode  auf 0x4 * (Supress Veto == Active), "
                       "um BUSKnockOut testen zu können und a´warte 2 sec"])

    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x04]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request, ticket_id='FehlerID:EGA-PRM-224'))
    time.sleep(2)

    # test step 12.1
    testresult.append(["\x0a 12.1. Prüfe kein veto würde erkannt."])
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0,
                                              descr="KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 0 (Initwert)"))

    # test step 12.2
    testresult.append(["\x0a 12.2 Prüfe KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer nach 60 Sekunden"])
    time.sleep(60)
    testresult.append(basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 14,
                                           descr="KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer = 14 (wird dekrementiert)"))

    # test step 13
    testresult.append(["\x0a 13. Warte bis KN_Waehlhebel:KN_Waehlhebel_BUSKnockOutTimer == 0 (Timeout: 14min)"])
    timeout = 14 * 60
    t_out = timeout + t()
    while t_out > t():
        if hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value.get() == 0:
            break
        elif t_out > t() == False:
            testresult.append(["\xa0 KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer  hat kein auf 0 gesetz in 14min", "FAILED"])
            break

    # test step 14
    testresult.append(["\x0a 14.Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 0,
                                           descr="KN_Waehlhebel_BUSKnockOutTimer = 0")]

    # test step 15
    testresult.append(["\x0a 15. Prüfe, dass nach 60sekund Kein Reset des SG stattfindet "])
    time.sleep(60)
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0,
                                           descr="KN_Waehlhebel_BUSKnockOutTimer = 0")]

    # test step 16
    testresult.append(["\x0a 16. Prüfe KN_Waehlhebel:Waehlhebel_Abschaltstufe", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__Waehlhebel_Abschaltstufe__value, 0,
                                           descr="KN_Waehlhebel:Waehlhebel_Abschaltstufe  == 0 (keine_Einschraenkung)")]

    # test step 17
    testresult.append(["\x0a 17. Prüfe NVEM_12:NVEM_Abschaltstufe", ""])
    testresult += [basic_tests.checkStatus(hil.NVEM_12__NVEM_Abschaltstufe__value, 3, equal=False,
                                           descr="NVEM_12:NVEM_Abschaltstufe__value != 3")]

    # test step 18
    testresult.append(["\x0a 18. Sende NVEM_12:NVEM_Abschaltstufe = 3 (Stufe_3) und warte 500ms", ""])
    hil.NVEM_12__NVEM_Abschaltstufe__value.set(3)
    time.sleep(0.500)

    # test step 19
    testresult.append(["\x0a 19. Prüfe KN_Waehlhebel:Waehlhebel_Abschaltstufe", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__Waehlhebel_Abschaltstufe__value, 1,
                                           descr="KN_Waehlhebel:Waehlhebel_Abschaltstufe  == 1  (Funktionseinschraenkung)")]

    # test step 20
    testresult.append(["\x0a 20.  Prüfe, dass Reset des SG stattfindet"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 2,
                                           descr=" KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 2 (0x2= Funktion_ausgeloest)")]

    # test step 21
    testresult.append(["\x0a 21. Schalte alle signal (HIL--> ECU) aus und stope DAQ messungen", ""])
    time.sleep(0.400)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=False, all_other_send=False)
    daq_data = daq.stopMeasurement()

    # test step 22
    testresult.append(["\x0a 22. Warte 1 min. und Prüfe Busruhe", ""])
    time.sleep(60)
    descr, verdict = func_gs.checkBusruhe(daq)
    testresult.append([descr, verdict])

    # test step 23
    testresult.append(["\x0a 23. Schalte alle signal (HIL--> ECU) ein. Schalte KL15 ein und warte 5sec", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=True, all_other_send=True)
    time.sleep(5)

    # test step 24
    testresult.append(["\x0a 24 Prüfe nichtflüchtige Speicherung von BusKnockOut_Tmr"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    testresult.append(result)
    BusKnockoutTmr = None
    if response[0:3] == [98, 2, 203]:
        BusKnockoutTmr = response[4]
        if BusKnockoutTmr is not None:
            if BusKnockoutTmr > 64:
                BusKnockoutTmr = BusKnockoutTmr - 64  # removing the active coupling value bit
                # testresult.append(["\xa0 NVEM couplling ist Aktive" , "PASSED"])
            else:
                BusKnockoutTmr = BusKnockoutTmr  # No active NVEM coupling
                # testresult.append(["\xa0 NVEM couplling ist inaktive", "FAILED"])
        else:
            BusKnockoutTmr = 0

        testresult += [basic_tests.checkStatus(BusKnockoutTmr, 15, descr="KN_Waehlhebel_BUSKnockOutTimer = 15")]

    # test step 25
    testresult.append(["\x0a 25 Prüfe nichtflüchtige Speicherung von BusKnockOut_ctr"])
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
    else:
        testresult.append(
            ["\xa0 Kein Positive response erhalten.  BusKnockOut_Ctr kann nicht auslasen", "FAILED"])


    # test step 26
    testresult.append(["\x0a 26. Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOut"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 2, descr=" KN_Waehlhebel:KN_Waehlhebel_BusKnockOut = 2 (0x2= Funktion_ausgeloest)")]

    # test step 27
    testresult.append(["\x0a 27.Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer "])
    if BusKnockoutTmr_start is not None:
        testresult += [
            basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, BusKnockoutTmr_start,
                                    descr=" Prüfe KN_Waehlhebel:KN_Waehlhebel_BusKnockOutTimer == bus_tmr == 15 ")]

    #
    # test step 28
    testresult.append(["\x0a 28.Messdatenauswertung:"])
    testresult.append(["\xa0Werte KL15 Signal aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data[str(measure_signal[0])],
        filename="KL15",
        label_signal="KL15")
    testresult.append([descr, plot, verdict])

    testresult.append(["\xa0Werte KN_Waehlhebel_BusKnockOutTimer aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data[str(measure_signal[1])],
        filename="KN_Waehlhebel_BusKnockOutTimer",
        label_signal="KN_Waehlhebel_BusKnockOutTimer,")
    testresult.append([descr, plot, verdict])

    testresult.append(["\xa0Werte KN_Waehlhebel_BusKnockOut aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data[str(measure_signal[2])],
        filename="KN_Waehlhebel_BusKnockOut",
        label_signal="KN_Waehlhebel_BusKnockOut,")
    testresult.append([descr, plot, verdict])

    testresult.append(["\xa0Werte NVEM_12:NVEM_Abschaltstufe aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data[str(measure_signal[3])],
        filename="NVEM_12",
        label_signal="NVEM_12_NVEM_Abschaltstufe,")
    testresult.append([descr, plot, verdict])

    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)