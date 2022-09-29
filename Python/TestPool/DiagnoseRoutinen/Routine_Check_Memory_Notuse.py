#******************************************************************************
# -*- coding: latin-1 -*-
# File    : Routine_Check_Memory_Notuse.py
# Title   : Routine Check_Memory_Notuse
# Task    : Test for Routine Diagnosejob 0x3101 0x0202
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
# 1.0  | 09.07.2021 | An3Neumann   | initial
# 1.1  | 19.11.2021 | Mohammed     | Added Fehler Id
# 1.2  | 27.01.2021 | Mohammed     | reworked test script after Adding  preconditions

#******************************************************************************
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
import time
import functions_gearselection
from ttk_checks import basic_tests

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_164")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_common = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize functions ####################################################
    func_common = functions_common.FunctionsCommon(testenv)

    # Initialize variables ####################################################
    diag_ident = identifier_dict['Check Memory']
    test_sessions = {
        1: {'session': 'Default Session', 'allowed': False},
        2: {'session': 'Factory Mode', 'allowed': False},
        3: {'session': 'Extended Session', 'allowed': False},
        4: {'session': 'Programming Session', 'allowed': True},
    }
    routine_control_option = [0x00]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Aktiviere Tester Present", ""])
    canape_diag.enableTesterPresent()

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
        request = [0x31, 0x01] + diag_ident['identifier'] + routine_control_option
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
            testresult.append(canape_diag.checkNegativeResponse(response, [0x31], 0x31, ticket_id='Fehler-Id: EGA-PRM-136'))

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
