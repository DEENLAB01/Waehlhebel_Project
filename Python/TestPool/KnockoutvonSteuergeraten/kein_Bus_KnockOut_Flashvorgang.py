# ******************************************************************************
# -*- coding: latin1 -*-
# File    : kein_Bus_KnockOut_Flashvorgang.py
# Title   : kein_Bus_KnockOut_Flashvorgang
# Task    : Test for Kein Bus KnockOut Flashvorgang
#
# Author  : Devangbhai Patel
# Date    : 17.12.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 17.12.2021 | Devangbhai   | initial
# 1.1  | 20.12.2021 | Devangbhai   | Rework according to test specification
# 1.2  | 22.12.2021 | Devangbhai | Added tester present enable insted of deactivate else knockout do not works
# 1.3  | 11.02.2022 | Devangbhai | Rework according to new specification

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
import functions_nm
from time import time as t
import os
import win32ui
import win32con  # constants


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
    diag_ident_KN_TEST_MODE =identifier_dict['Knockout_test_mode']
    func_nm = functions_nm.FunctionsNM(testenv)

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_205")

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

    ###
    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # test step 1
    testresult.append(["\x0a1.  In Extended Sesssion Setze BusKnockOut_Tmr auf 16, "])
    testresult.append(["\xa0Wechsle in die Extended Session", "INFO"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x0F, 0x10]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 2
    testresult.append(["\x0a 2. Prüfe KN_Waehlhebel_BusKnockOutTimer"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 16, descr="KN_Waehlhebel_BusKnockOutTime = 16")]

    # test step 3
    testresult.append(["\x0a 3. Prüfe BusKnockOut_Ctr und speichere Wert in busctr_start"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    busctr_start = None

    if response[0:3] == [98, 2, 202]:
        busctr_start = response[4]
        if busctr_start is not None:
            busctr_start = busctr_start
            testresult.append( ["\xa0 Gespeichere Wert für BusKnockOut_Ctr (Variable) für späteren Vergleich ist %s" % busctr_start])
        else:
            busctr_start = 0
            testresult.append(
                ["\xa0 Gespeichere Wert für BusKnockOut_Ctr (Variable) für späteren Vergleich ist %s" % busctr_start])
    else:
        testresult.append(["\xa0 Kein Positive response erhalten.  BusKnockOut_Ctr kann nicht auslasen", "FAILED"])

    # test step 4
    testresult.append(["\x0a 4. Setze KL15 ausschalten 0 (inactive)", ""])
    hil.cl15_on__.set(0)

    # test step 5
    testresult.append(["\x0a 5. Senden nur der NM Botschaft und Clampcontrol von HIL--> ECU. Alle anderen Botschaften stoppen."])
    func_nm.hil_ecu_tx_signal_state_for_Knockout()

    # test step 6
    testresult.append(["\x0a 6. Wechsel in die Entwicklersession, (in Factory mode security access dürchführen) "
                       "Setze mittels 2E 09 F3: KnockOut_Test_mode  auf 0x4 * (Supress Veto == Active)"])

    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    testresult.append(["\xa0 Erfolgreichen Security Access durchführen", "INFO"])
    seed_1, key_1, result = canape_diag.performSecurityAccess()
    testresult.extend(result)

    request = [0x2E] + diag_ident_KN_TEST_MODE['identifier'] + [0x04]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 7
    testresult.append(["\x0a 7. Warte 61s)", ""])
    time.sleep(61)

    # test step 8
    testresult.append(["\x0a 8.  Prüfe KN_Waehlhebel_BUSKnockOutTimer"])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 15, descr="KN_Waehlhebel_BusKnockOutTime = 15 (wird dekrementiert)")]

    # test step 9
    testresult.append(["\x0a 9. Flashvorgang starten"])
    testresult.append(["\xa0 MANUELLER TEIL: Gleiche SW erneut flashen (mit PASDT)", ""])
    last_response = win32con.IDNO
    response_win = win32ui.MessageBox("Manual Part begins: Press OK to get next information",
                                  "Achtung", win32con.MB_SYSTEMMODAL + win32con.MB_OK)
    if response_win == win32con.IDOK:
        response_win = win32ui.MessageBox("Switch on ECU in model (XiBase) and press OK afterwards", "Achtung",
                                      win32con.MB_SYSTEMMODAL + win32con.MB_OK)
        if response_win == win32con.IDOK:
            response_win = win32ui.MessageBox("Please flash now the same SW again and press OK afterwards", "Achtung",
                                          win32con.MB_SYSTEMMODAL + win32con.MB_OK)

            # test step 10
            testresult.append(["\x0a 10. Prüfe Bus-Kommunikation", ""])
            check_cycletime(5, application_msg=True, nm_msg=True)

            # test step 11
            testresult.append(["\x0a 11. Prüfe Bus State", ""])
            request = [0x22] + diag_ident_KN_TEST_MODE['identifier']
            response_diag, result = canape_diag.sendDiagRequest(request)
            testresult.append(result)
            bus_sleep = None

            if response_diag[0:3] == [98, 9, 243]:
                bus_sleep = response_diag[3]
                testresult.append(["Prüfe dass Bus State != Bus Sleep", ""])
                testresult += [basic_tests.checkStatus(bus_sleep, 1, equal=False,
                                                       descr="Prüfe dass Bus State != Bus Sleep")]
            else:
                testresult.append(["\xa0 Kein Positive response erhalten.  Bus State kann nicht auslasen", "FAILED"])

            # test step 12
            testresult.append(["\x0a 12. Warte 70s)", ""])
            time.sleep(70)

            # test step 13
            testresult.append(["\x0a 13. Prüfe KN_Waehlhebel_BUSKnockOutTimer"])
            testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value, 15, descr="KN_Waehlhebel_BusKnockOutTimer == 15 (wird nicht dekrementiert, obwohl Startbedingungen für Bus-KnockOut-Algorithmus erfüllt)")]

            # test step 14
            testresult.append(["\x0a 14. Prüfe BusKnockOut_Ctr"])
            request = [0x22] + diag_ident_KN_CTR['identifier']
            response_diag, result = canape_diag.sendDiagRequest(request)
            testresult.append(result)
            busctr_end = None

            if response_diag[0:3] == [98, 2, 202]:
                busctr_end = response_diag[4]
                if busctr_start is not None:
                    busctr_end = busctr_end
                    testresult.append(["\xa0 Gespeichere Wert für BusKnockOut_Ctr (Variable) für Vergleich ist %s" % busctr_end])
                else:
                    busctr_end = 0
                    testresult.append(["\xa0 Gespeichere Wert für BusKnockOut_Ctr (Variable) für  Vergleich ist %s" % busctr_end])

                if busctr_start is not None:
                    testresult.append(["\xa0 Prüf ECUKnockOut_Ctr == ecuctr_start (unverändert)", ""])
                    testresult.append(basic_tests.checkStatus(
                        current_status=busctr_start,
                        nominal_status=busctr_end,
                        descr="Prüfe, dass ECUKnockOut_Ctr == ecuctr_start (unverändert)", ))
            else:
                testresult.append(["\xa0 Kein Positive response erhalten.  BusKnockOut_Ctr kann nicht auslasen", "FAILED"])

            # test step 15
            if response_win == win32con.IDOK:
                last_response = win32ui.MessageBox("Warte bis Flashvorgang beendet. Press OK afterwards","Achtung", win32con.MB_SYSTEMMODAL + win32con.MB_OK)

                # test step 16
                testresult.append(["\x0a 16. Prüfe BusKnockOut_Ctr"])
                request = [0x22] + diag_ident_KN_CTR['identifier']
                response_diag, result = canape_diag.sendDiagRequest(request)
                testresult.append(result)
                busctr_end_2 = None

                if response_diag[0:3] == [98, 2, 202]:
                    busctr_end_2 = response_diag[4]
                    if busctr_end_2 is not None:
                        busctr_end_2 = busctr_end_2
                        testresult.append(
                            ["\xa0 Gespeichere Wert für BusKnockOut_Ctr (Variable) ist %s" % busctr_end_2])
                    else:
                        busctr_end_2 = 0
                        testresult.append(
                            ["\xa0 Gespeichere Wert für BusKnockOut_Ctr (Variable) ist %s" % busctr_end_2])

                    if busctr_start is not None:
                        testresult.append(["\xa0 Prüf BusKnockOut_Ctr == busctr_start (unverändert)", ""])
                        testresult.append(basic_tests.checkStatus(
                            current_status=busctr_start,
                            nominal_status=busctr_end_2,
                            descr="Prüfe, dass BusKnockOut_Ctr == busctr_start (unverändert)", ))
                else:
                    testresult.append(
                        ["\xa0 Kein Positive response erhalten.  BusKnockOut_Ctr kann nicht auslasen", "FAILED"])
        else:
            testresult.append(["Test abgebrochen (Manuelles Flashen nicht gestartet/beendet)", "Info"])

    else:
        testresult.append(["Test abgebrochen (Manuelles Flashen nicht gestartet/beendet)", "Info"])

    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()
    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)