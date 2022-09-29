#******************************************************************************
# -*- coding: latin-1 -*-
# File    : Routine_Clear_user_defined_DTC_information.py
# Title   : Routine Clear user defined DTC information
# Task    : Test for Routine Diagnosejob 0x3101 0x045A
#
# Author  : An3Neumann
# Date    : 09.07.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 09.07.2021 | An3Neumann | initial
# 1.1  | 23.08.2021 | Mohammed | Added Fehler Id
# 1.2  | 04.02.2022 | Mohammed | Update Test script after changing TestSpec.
#******************************************************************************
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
import functions_gearselection
import functions_nm
import time
from ttk_checks import basic_tests

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_166")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_common = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    diag_ident = identifier_dict['Clear_user_defined_DTC_information']
    test_sessions = {
        1: {'session': 'Default Session', 'allowed': False},
        2: {'session': 'Factory Mode', 'allowed': True},
        3: {'session': 'Extended Session', 'allowed': True},
        4: {'session': 'Programming Session', 'allowed': False},
    }
    erase_indication = [0xFF, 0xFF, 0xFF]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    ############################
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s"%testenv.script_name.split('.py')[0], ""])

    for session in test_sessions:
        curr_session = test_sessions[session]['session']
        set_check_session = curr_session.split(' ')[0].lower()
        allowed = test_sessions[session]['allowed']
        if session == 1:
            # Auslesen der Active Diagnostic Session: 0x22F186
            testresult.append(["[+] Lese aktuelle Diagnose Session aus", ""])
            testresult.extend(canape_diag.checkDiagSession(set_check_session))
        else:
            # Wechsel in Extended Session: 0x1003
            testresult.append(["[.] In die %s wechseln"%curr_session, ""])
            testresult.extend(canape_diag.changeAndCheckDiagSession(set_check_session))
            time.sleep(1)


        testresult.append(["[.] '%s' ausführen: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
        request = [0x31, 0x01] + diag_ident['identifier'] + erase_indication
        [response, result] = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        if allowed:

            testresult.append(["\xa0Auf positive Response überprüfen", ""])
            descr, verdict = canape_diag.checkPositiveResponse(response, request, 4)
            testresult.append([descr, verdict])

            testresult.append(["\xa0Datenlänge überprüfen", ""])
            if verdict == 'FAILED':
                testresult.append(["Prüfung der Datenlänge nicht möglich, da keine positive Response kam", "FAILED"])
            else:
                testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length'], 4))

        else:

            testresult.append(["\xa0Auf negative Response überprüfen", ""])
            testresult.append(canape_diag.checkNegativeResponse(response, [0x31], 0x31))
    '''

    # test step 12
    testresult.append(["[.]  Bus off (globaler TimeOut) anlegen", ""])
    func_nm.hil_ecu_tx_off_state("aus")

    # test step 13
    testresult.append(["[.] Lese Fehlerspeicher aus ", ""])
    testresult.append(["\x0a Prüfe 0xE00100 in Fehlerspeicher vorhanden", ""])
    active_dtcs = [(0xE00100, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='Fehler Id:139'))

    # test step 14
    testresult.append(["\x0a Wechsel in Default Session: 0x1001", "Info"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # test step 15
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 16
    request = [0x31, 0x01] + diag_ident['identifier'] + erase_indication
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, [0x31], 0x31))

    # test step 17
    testresult.append(["[.] Lese Fehlerspeicher aus ", ""])
    testresult.append(["\x0a Prüfe 0xE00100 in Fehlerspeicher vorhanden", ""])
    active_dtcs = [(0xE00100, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='Fehler Id:139'))

    # test step 18
    testresult.append(["\x0a Wechsel in Extended Session: 0x1001", "Info"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 19
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 20
    request = [0x31, 0x01] + diag_ident['identifier'] + erase_indication
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 21
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 22
    testresult.append(["[.]  Bus off (globaler TimeOut) anlegen", ""])
    func_nm.hil_ecu_tx_off_state("aus")

    # test step 23
    testresult.append(["[.] Lese Fehlerspeicher aus ", ""])
    testresult.append(["\x0a Prüfe 0xE00100 in Fehlerspeicher vorhanden", ""])
    active_dtcs = [(0xE00100, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='Fehler Id:139'))

    # test step 24
    testresult.append(["\x0a Wechsel in Factory Mode: 0x1060", "Info"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    # test step 25
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 26
    request = [0x31, 0x01] + diag_ident['identifier'] + erase_indication
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 27
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 28
    testresult.append(["[.]  Bus off (globaler TimeOut) anlegen", ""])
    func_nm.hil_ecu_tx_off_state("aus")

    # test step 29
    testresult.append(["[.] Lese Fehlerspeicher aus ", ""])
    testresult.append(["\x0a Prüfe 0xE00100 in Fehlerspeicher vorhanden", ""])
    active_dtcs = [(0xE00100, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='Fehler Id:139'))

    # test step 30
    testresult.append(["\x0a Wechsel in Default Session: 0x1001", "Info"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # test step 31
    testresult.append(["\x0a Wechsel in Programming Session: 0x1002", "Info"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))

    # test step 32
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # test step 33
    request = [0x31, 0x01] + diag_ident['identifier'] + erase_indication
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, [0x31], 0x31))

    # test step 34
    testresult.append(["[.] Lese Fehlerspeicher aus ", ""])
    testresult.append(["\x0a Prüfe 0xE00100 in Fehlerspeicher vorhanden", ""])
    active_dtcs = [(0xE00100, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='Fehler Id:139'))
'''
    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup #################################################################
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

print "Done."
