# ******************************************************************************
# -*- coding: latin1 -*-
# File    : ECU_KnockOut.py
# Title   : ECU_KnockOut
# Task    : Test for ECU KnockOut
#
# Author  : Mohammed Abdul Karim
# Date    : 07.02.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 07.02.2022 | Mohammed   | initial
# 1.1  | 13.02.2022 | Devangbhai | Rework according to new specification
# 1.2  | 03.03.2022 | Devangbhai | Added sleep time to adjust the time delay
# 1.3  | 21.03.2022 | Devangbhai | Added sleep time after Knockout


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
from functions_nm import _checkStatus
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
    test_variable = hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value
    func_nm = functions_nm.FunctionsNM(testenv)

    measure_signal = [hil.ClampControl_01__KST_KL_15__value,
                      hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value,
                      hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value]
    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_202")

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

    # Test step 1
    testresult.append(["\x0a 1. Lese Botschaft KN_Waehlhebel aus, Prüfe Diagnoseparameter ECUKnockOut_Ctr (22 02 CA) und speichere Wert in ecuctr_start (Variable) für späteren Vergleich"])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 15, descr="KN_Waehlhebel_ECUKnockOutTimer = 15"),
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 0 or 1, descr="KN_Waehlhebel_ECUKnockOut = 0 or 1")]

    testresult.append(["\x0a Prüfe Diagnoseparameter ECUKnockOut_Ctr (22 02 CA)"])
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
            testresult.append( ["\xa0 Gespeichere Wert für ecuctr_start (Variable) für späteren Vergleich ist %s" % ECUKnockOut_Ctr_start])
        else:
            ECUKnockOut_Ctr_start = 0
            testresult.append( ["\xa0 Gespeichere Wert für ecuctr_start (Variable) für späteren Vergleich ist %s" % ECUKnockOut_Ctr_start])
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 2
    testresult.append(["\x0a 2. Warte 1,5 min und Lese Botschaft KN_Waehlhebel aus", ""])
    time.sleep(1.5* 60)

    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 15, descr="KN_Waehlhebel_ECUKnockOutTimer = 15"),
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 0 or 1, descr="KN_Waehlhebel_ECUKnockOut = 0 or 1")]

    # test step 3
    testresult.append(["\x0a 3. Messung starten: \n ClampControl_01__KST_KL_15__value, \nKN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer, \nKN_Waehlhebel:KN_Waehlhebel_ECUKnockOut"])
    daq.startMeasurement(measure_signal)

    # test step 4
    testresult.append(["\x0a4. KL15 ausschalten und warte 12sec"])
    hil.cl15_on__.set(0)
    time.sleep(2)

    # test step 5
    testresult.append(["\x0a 5. Wechsel in die Entwicklersession, (in Factory mode security access dürchführen) Setze mittels 2E 09 F3: KnockOut_Test_mode  auf 0x1 * (Bit 1: Bus State == Bus Sleep), um ECUKnockOut testen zu können"])
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
    testresult.append(["\x0a 6.Prüfe Bus State"])
    req = [0x22] + diag_ident_KN_TEST_MODE['identifier']
    [response, result] = canape_diag.sendDiagRequest(req)
    testresult.append(result)
    expected_resp = [0x62] + diag_ident_KN_TEST_MODE['identifier'] + [0x01]
    testresult.append(["Bus State == Bus Sleep", ""])
    testresult.append(canape_diag.checkResponse(response, expected_resp))

    # test step 7
    testresult.append(["\x0a7. Warte 2"])
    time.sleep(2)

    # test step 8
    testresult.append(["\x0a 8. Senden nur der NM Botschaft und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen."])
    func_nm.hil_ecu_tx_signal_state_for_Knockout()

    # test step 9
    testresult.append(["\x0a 9. Prüfe der Botschaft KN_Waehlhebel", ""])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 15, descr="KN_Waehlhebel_ECUKnockOutTimer = 15"),
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 0, descr="KN_Waehlhebel_ECUKnockOut = 0")]

    # test step 10
    testresult.append(["\x0a 10. Warte 1,5min"])
    time.sleep(90)

    # test step 11
    testresult.append(["\x0a11. Lese Botschaft KN_Waehlhebel aus"])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 14, descr="KN_Waehlhebel_ECUKnockOutTimer = 14(Wird dekrementiert)"),
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 0, descr="KN_Waehlhebel_ECUKnockOut = 0")]

    # test step 12
    testresult.append(["\x0a 12. Warte 1 min und prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer "])
    time.sleep(60)
    testresult.append(["Prüfe der Botschaft KN_Waehlhebel", ""])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 13,
                                descr="KN_Waehlhebel_ECUKnockOutTimer = 13 (Wird dekrementiert)"),
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 0,
                                descr="KN_Waehlhebel_ECUKnockOut = 0")]

    # test step 13
    testresult.append(["\x0a 13. Warte bis KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTime == 0.(Timeout = 13min)"])
    timeout = 13 * 60
    t_out = timeout + t()
    while t_out > t():
        if hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value.get() == 0:
            break
        elif t_out > t() == False:
            testresult.append(["\xa0 KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value hat kein auf 0 gesetz in 13 min", "FAILED"])
            break

    # test step 14
    testresult.append(["\x0a 14. Lese Botschaft KN_Waehlhebel aus"])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 0,
                                descr="KN_Waehlhebel_ECUKnockOutTimer = 0"),
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 2,
                                descr="KN_Waehlhebel_ECUKnockOut == 0x2 (Funktion_ausgeloest)")]

    # test step 15
    testresult.append(["\x0a 15. Schalte alle signal (HIL--> ECU) aus und stope DAQ messungen", ""])
    time.sleep(0.500)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=False, all_other_send=False)
    daq_data = daq.stopMeasurement()

    testresult.append(["\xa0Werte KL15 Signal aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data[str(measure_signal[0])],
        filename="KL15",
        label_signal="KL15")
    testresult.append([descr, plot, verdict])

    testresult.append(["\xa0Werte KN_Waehlhebel_ECUKnockOutTimer aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data[str(measure_signal[1])],
        filename="KN_Waehlhebel_ECUKnockOutTimer",
        label_signal="KN_Waehlhebel_ECUKnockOutTimer,")
    testresult.append([descr, plot, verdict])

    testresult.append(["\xa0Werte KN_Waehlhebel_ECUKnockOut aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data[str(measure_signal[2])],
        filename="KN_Waehlhebel_ECUKnockOut",
        label_signal="KN_Waehlhebel_ECUKnockOut,")
    testresult.append([descr, plot, verdict])

    # test step 16
    testresult.append(["\x0a16. Warte 1 min"])
    time.sleep(60)

    # test step 17
    testresult.append(["\x0a17. Schalte Senden von RX Signalen (HiL --> ECU) ein, Schalte Kl15 ein und warte 5sec", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_tx_signal_state_for_Knockout(NM_Clampcontrol_send=True, all_other_send=True)
    time.sleep(5)

    # test step 18
    testresult.append(["\x0a 18Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOut", ""])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value, 2,
                                           descr="KN_Waehlhebel_ECUKnockOut = 0x2(Funktion_ausgelöst )")]

    # test step 19
    testresult.append(["\x0a 19.Prüfe KN_Waehlhebel:KN_Waehlhebel_ECUKnockOutTimer", ""])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 15,
                                descr="KN_Waehlhebel_ECUKnockOutTimer = 15 (Bus-Wert entspricht früherem Tmr-Restwert; in diesem Fall: 0, da Tmr abgelaufen ist)"),]

    # test step 20
    testresult.append(["\x0a 20.Prüfe Diagnoseparameter ECUKnockOut_Ctr (22 02 CA)", ""])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response_diag, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkPositiveResponse(response_diag, request))
    ECUKnockOut_Ctr_end = None

    if response_diag[0:3] == [98, 2, 202]:
        ECUKnockOut_Ctr_end = response_diag[3]
        if ECUKnockOut_Ctr_end is not None:
            ECUKnockOut_Ctr_end = ECUKnockOut_Ctr_end
        else:
            ECUKnockOut_Ctr_end = 0
    else:
        testresult.append(
            ["\xa0 Kein Positive response erhalten.  ECUKnockOut_Ctr kann nicht auslasen", "FAILED"])

    if ECUKnockOut_Ctr_end is not None:
        testresult.append(["\xa0 Prüf ECUKnockOut_Ctr = ecuctr_start + 1", ""])
        testresult.append(basic_tests.checkStatus(
            current_status=ECUKnockOut_Ctr_end,
            nominal_status=ECUKnockOut_Ctr_start + 1,
            descr="Prüfe, dass ECUKnockOut_Ctr = ecuctr_start + 1", ))

    else:
        testresult.append(["\xa0 ECUKnockOut_Ctr kann nicht auslasen. ECUKnockOut_Ctr kann nicht mit ecuctr_start vergleichen", "FAILED"])

    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()
    time.sleep(5)
    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)