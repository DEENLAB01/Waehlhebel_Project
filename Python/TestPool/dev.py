# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Bus_KnockOut.py
# Title   : Bus_KnockOut.py
# Task    : Test for Bus KnockOut
#
# Author  : Mohammed Abdul Karim
# Date    : 17.12.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 17.12.2021 | Mohammed   | initial
# 1.2  | 17.12.2021 | Devangbhai   | Rework
# 1.3  | 21.12.2021 | Devangbhai | Removed DAQ measurement Added CANape restart method
# 1.4  | 22.12.2021 | Devangbhai | Added tester present enable insted of deactivate else knockout do not works

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


def check_cycletime(sec, application_msg=True, nm_msg=True):
    Waehlhebel_04__timestamp_list = []
    DS_Waehlhebel__timestamp_list = []
    KN_Waehlhebel__timestamp_list = []
    NM_Waehlhebel__timestamp_list = []

    timeout = sec + t()

    while timeout > t():
        timestamp_Waehlhebel_04 = hil.Waehlhebel_04__timestamp.get()
        timestamp_DS_Waehlhebel = hil.DS_Waehlhebel__timestamp.get()
        timestamp_KN_Waehlhebel = hil.KN_Waehlhebel__timestamp.get()
        timestamp_NM_Waehlhebel = hil.NM_Waehlhebel__timestamp.get()

        if len(Waehlhebel_04__timestamp_list) == 0 or Waehlhebel_04__timestamp_list[-1] != timestamp_Waehlhebel_04:
            Waehlhebel_04__timestamp_list.append(timestamp_Waehlhebel_04)

        elif len(DS_Waehlhebel__timestamp_list) == 0 or DS_Waehlhebel__timestamp_list[-1] != timestamp_DS_Waehlhebel:
            DS_Waehlhebel__timestamp_list.append(timestamp_DS_Waehlhebel)

        elif len(KN_Waehlhebel__timestamp_list) == 0 or KN_Waehlhebel__timestamp_list[-1] != timestamp_KN_Waehlhebel:
            KN_Waehlhebel__timestamp_list.append(timestamp_KN_Waehlhebel)

        elif len(NM_Waehlhebel__timestamp_list) == 0 or NM_Waehlhebel__timestamp_list[-1] != timestamp_NM_Waehlhebel:
            NM_Waehlhebel__timestamp_list.append(timestamp_NM_Waehlhebel)

    new_sec = sec * 1000
    Waehlhebel_04__timestamp = 10
    DS_Waehlhebel__timestamp = 1000
    KN_Waehlhebel__timestamp = 500
    NM_Waehlhebel_timestamp = 200

    testresult.append(basic_tests.checkRange((len(Waehlhebel_04__timestamp_list)) if application_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / Waehlhebel_04__timestamp) - 5) if application_msg else 0, ((new_sec / Waehlhebel_04__timestamp) + 5) if application_msg else 0, "Prüfen, ob die Applikation Botschaft Waehlhebel_04 mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (Waehlhebel_04__timestamp, sec)))
    testresult.append(basic_tests.checkRange((len(DS_Waehlhebel__timestamp_list)) if application_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / DS_Waehlhebel__timestamp) - 2) if application_msg else 0, ((new_sec / DS_Waehlhebel__timestamp) + 2) if application_msg else 0, "Prüfen, ob die Applikation Botschaft DS_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % ( DS_Waehlhebel__timestamp, sec)))
    testresult.append(basic_tests.checkRange((len(KN_Waehlhebel__timestamp_list)) if application_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / KN_Waehlhebel__timestamp) - 2) if application_msg else 0,((new_sec / KN_Waehlhebel__timestamp) + 2) if application_msg else 0, "Prüfen, ob die Applikation Botschaft KN_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % ( KN_Waehlhebel__timestamp, sec)))
    testresult.append(basic_tests.checkRange((len(NM_Waehlhebel__timestamp_list)) if nm_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / NM_Waehlhebel_timestamp) - 2) if nm_msg else 0, ((new_sec / NM_Waehlhebel_timestamp) + 2) if nm_msg else 0, "Prüfen, ob die Applikation Botschaft NM_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (NM_Waehlhebel_timestamp, sec)))


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
    testresult.setTestcaseId("TestSpec_204")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    func_nm.hil_ecu_tx_off_state("an")
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()
    # hil.ISOx_Waehlhebel_Req_FD__period.setState("an")

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
    # hil.ISOx_Waehlhebel_Req_FD__period.setState("aus")
    testenv.canape_Diagnostic = None

    # clear instances before flashing
    testenv.asap3 = None
    testenv.canape_Diagnostic = None
    del (canape_diag)

    testenv.shutdownECU()
    func_nm.hil_ecu_tx_off_state("aus")

    time.sleep(10)

    testresult.append(["\xa0 ECU einschalten", ""])
    testenv.startupECU()
    func_nm.hil_ecu_tx_off_state("an")
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()
    # hil.ISOx_Waehlhebel_Req_FD__period.setState("an")

    cal = testenv.getCal()

    ###
    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["\x0a1. Lese BusKnockOut_Tmr und speichere den Wert in bus_tmr"])
    testresult.append(["\xa0 Change to extended session"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))


    testresult.append(["\xa0 Prüfe Diagnoseparameter BUSKnockOut_Tmr (22 02 CB)"])
    request = [0x22] + diag_ident_KN_TMR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    BusKnockoutTmr_start = None

    if response[0:3] == [98, 2, 203]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        BusKnockoutTmr_start = response[4]
        if BusKnockoutTmr_start is not None:
            BusKnockoutTmr_start = BusKnockoutTmr_start
            testresult.append(["\xa0 Gespeichere Wert für BusKnockoutTmr_start (Variable) für späteren Vergleich ist %s" % BusKnockoutTmr_start])
        else:
            BusKnockoutTmr_start = 0
            testresult.append(["\xa0 Gespeichere Wert für BusKnockoutTmr_start (Variable) für späteren Vergleich ist %s" % BusKnockoutTmr_start])
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["\x0a Prüfe Diagnoseparameter ECUKnockOut_Ctr (22 02 CA)"])
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
            testresult.append(["\xa0 Gespeichere Wert für BUSKnockOut_Ctr_start (Variable) für späteren Vergleich ist %s" % BUSKnockOut_Ctr_start])
        else:
            BUSKnockOut_Ctr_start = 0
            testresult.append(["\xa0 Gespeichere Wert für BUSKnockOut_Ctr_start (Variable) für späteren Vergleich ist %s" % BUSKnockOut_Ctr_start])
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["\x0a 2. Prüfe InternalTmr_Bus", ""])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, BusKnockoutTmr_start, descr="KN_Waehlhebel_BUSKnockOutTimer(InternalTmr_BUS) = BusKnockoutTmr_start"),
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0, descr="KN_Waehlhebel_BUSKnockOut = 0")
    ]

    testresult.append(["\x0a3. Warte 1,5min"])
    time.sleep(90)

    testresult.append(["\x0a4. Prüfe InternalTmr_Bus", ""])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, BusKnockoutTmr_start,
                                descr="InternalTmr_Bus == bus_tmr (Ausgangswert; Timer läuft nicht)"),
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0,
                                descr="KN_Waehlhebel_BUSKnockOut = 0")
    ]

    testresult.append(["\x0a4. KL15 ausschalten "])
    hil.cl15_on__.set(0)

    testresult.append(["\x0a5. Warte 150ms"])
    time.sleep(0.150)

    testresult.append(["\x0a8. Schalte Senden von RX Signalen (HiL --> ECU) aus, NM_HCP und Clampcontol ist AN", "INFO"])
    func_nm.hil_ecu_tx_off_state("aus")
    hil.ClampControl_01__period.setState("an")
    hil.NM_HCP1__period.setState("an")
    # hil.ISOx_Waehlhebel_Req_FD__period.setState('an')

    time_to_sleep_after_RX_aus = 4
    time.sleep(time_to_sleep_after_RX_aus)

    testresult.append(["\x0a9. Prüfe dass Applikation und NM Botschaften werden gesendet ", ""])
    time_to_check_busruhe = 3
    check_cycletime(sec=time_to_check_busruhe, application_msg=True, nm_msg=True)
    testresult.append(["\x0aPrüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    testresult.append(["\x0a10. Warte 1,5min"])
    time.sleep(90 - time_to_check_busruhe - time_to_sleep_after_RX_aus)

    testresult.append(["\x0a11. Lese Botschaft KN_Waehlhebel aus"])
    testresult.append(["Prüfe der Botschaft KN_Waehlhebel", ""])

    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 14, descr="KN_Waehlhebel_BUSKnockOutTimer(InternalTmr_BUS) = 14"),
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0, descr="KN_Waehlhebel_BUSKnockOut = 0")
    ]

    testresult.append(["\x0a10.1 Warte 1min"])
    time.sleep(60)
    testresult.append(["Prüfe der Botschaft KN_Waehlhebel", ""])
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 13,
                                descr="KN_Waehlhebel_BUSKnockOutTimer(InternalTmr_BUS) = 13"),
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0,
                                descr="KN_Waehlhebel_BUSKnockOut = 0")
    ]

    testresult.append(["\x0a12. Warte 12 min # Adjusted the time to 12 insted of 12 to calculate the BswM_Notification_ESH_ModeNotification_BswM_MDGP_ESH_Mode variable"])
    time.sleep(60 * 12)
    testresult += [
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 1,
                                descr="KN_Waehlhebel_BUSKnockOutTimer(InternalTmr_BUS) = 1"),
        basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value, 0,
                                descr="KN_Waehlhebel_BUSKnockOut = 0")
    ]

    testresult.append(["\x0a12.1. Prüfe 80 s lang, dass BswM_Notification_ESH_ModeNotification_BswM_MDGP_ESH_Mode konstant bleibt", ""])
    timerlist = []
    sec = 70
    timeout = sec + t()
    while timeout > t():
        timerlist.append(cal.BswM_Notification_ESH_ModeNotification_BswM_MDGP_ESH_Mode.get())
    value = timerlist[0]
    value_boolean = True
    for timer_values in timerlist:
        if value != timer_values:
            value_boolean = False
            break
    testresult.append(
        ["\xa0 BswM_Notification_ESH_ModeNotification_BswM_MDGP_ESH_Mode hat konstant gebleiben", "PASSED"]) if value_boolean else testresult.append(
        ["\xa0 BswM_Notification_ESH_ModeNotification_BswM_MDGP_ESH_Mode hat nicht konstant gebleiben", "FAILED"])

    print "This is the value of BswM_Notification_ESH_ModeNotification_BswM_MDGP_ESH_Mode", timerlist

    testresult.append(["\x0a12.2  Lese BswM_Notification_ESH_ModeNotification_BswM_MDGP_ESH_Mode aus"])
    testresult += [basic_tests.checkStatus(cal.BswM_Notification_ESH_ModeNotification_BswM_MDGP_ESH_Mode, 2, descr="BswM_Notification_ESH_ModeNotification_BswM_MDGP_ESH_Mode = 2")]

    # hil.ISOx_Waehlhebel_Req_FD__period.setState('aus')

    testresult.append(["\x0a13. Prüfe Busruhe (Abschaltung ECU) nach 5 sek(SIGNAL TIMEOUT)"])
    time.sleep(5)
    testresult.append(["\xa0Prüfe Busruhe (0<I<2mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.0,  # 0mA
            max_value=0.002,  # 2mA
            descr="Prüfe, dass Strom zwischen 2mA und 0mA liegt"
        )
    )
    time_1 = time.time()
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    testresult.append([descr, verdict])
    time_2 = time.time()
    time_difference = time_2 - time_1

    testresult.append(["\x0a14. Warte 1 min"])
    time.sleep(60 - time_difference)

    testresult.append(["\x0a14.1 ECU ausschalten", ""])
    testenv.canape_Diagnostic = None

    # clear instances before flashing
    testenv.asap3 = None
    testenv.canape_Diagnostic = None
    del (canape_diag)
    time.sleep(5)

    testresult.append(["\x0a15. Schalte Senden von RX Signalen (HiL --> ECU) ein, Schalte Kl15 ein", ""])
    func_nm.hil_ecu_tx_off_state("an")
    hil.cl15_on__.set(1)
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()


    testresult.append(["\x0a18. Lese Botschaft KN_Waehlhebel aus", ""])

    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 15,
                                descr="KN_Waehlhebel_BUSKnockOutTimer(InternalTmr_BUS) = 15")]

    testresult.append(
        ["\x0a19. Wechsle in die Extended Session, Prüfe Diagnoseparameter BUSKnockOut_ (22 02 CA)", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    testresult.append(["\xa0 Prüfe ECUKnockOut_Ctr = ecuctr_start+ 1 ist"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response_diag, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    ECUKnockOut_Ctr_end = None

    if response_diag[0:3] == [98, 2, 202]:
        ECUKnockOut_Ctr_end = response_diag[4]
        if ECUKnockOut_Ctr_end is not None:
            ECUKnockOut_Ctr_end = ECUKnockOut_Ctr_end
            testresult.append(
                ["\xa0 Gespeichere Wert für BusKnockOut_Ctr (Variable) ist %s" % ECUKnockOut_Ctr_end])
        else:
            ECUKnockOut_Ctr_end = 0
            testresult.append(
                ["\xa0 Gespeichere Wert für BusKnockOut_Ctr (Variable) ist %s" % ECUKnockOut_Ctr_end])

        if BUSKnockOut_Ctr_start is not None:
            testresult.append(["\xa0 Prüf ECUKnockOut_Ctr = ecuctr_start + 1", ""])
            testresult.append(basic_tests.checkStatus(
                current_status=ECUKnockOut_Ctr_end,
                nominal_status=BUSKnockOut_Ctr_start + 1,
                descr="Prüfe, dass BUSKnockOut_Ctr = Busctr_start + 1", ))
    else:
        testresult.append(
            ["\xa0 Kein Positive response erhalten.  BusKnockOut_Ctr kann nicht auslasen", "FAILED"])

    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)