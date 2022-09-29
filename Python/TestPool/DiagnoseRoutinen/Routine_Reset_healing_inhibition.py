#******************************************************************************
# -*- coding: latin-1 -*-
# File    : Routine_Reset_healing_inhibition.py
# Task    : Test for Routine Diagnosejob 0x3101 0x006A8
#
# Author  : An3Neumann
# Date    : 05.07.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 07.07.2021 | An3Neumann | initial
# 1.1  | 23.08.2021 | Mohammed | Added Fehler Id
#******************************************************************************
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
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
    testresult.setTestcaseId("TestSpec_160")

    # Initialize functions ####################################################
    func_common = functions_common.FunctionsCommon(testenv)

    # Initialize variables ####################################################
    diag_ident = identifier_dict['Reset_healing_inhibition']
    test_sessions = {
        1: {'session': 'Default Session', 'sec_access': False, 'allowed': False},
        2: {'session': 'Extended Session', 'sec_access': False, 'allowed': False},
        3: {'session': 'Extended Session', 'sec_access': True, 'allowed': True},
        4: {'session': 'Factory Mode', 'sec_access': False,  'allowed': False},
        5: {'session': 'Factory Mode', 'sec_access': True,  'allowed': True},
    }

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

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


        if test_sessions[session]['sec_access']:
            testresult.append(["[.] Erfolgreichen Security Access durchführen", ""])
            _, _, result = canape_diag.performSecurityAccess()
            testresult.extend(result)

        testresult.append(["[.] '%s' ausführen: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
        request = [0x31, 0x01] + diag_ident['identifier']
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
            testresult.append(canape_diag.checkNegativeResponse(response, [0x31], 0x7F, ticket_id='Fehler Id:EGA-PRM-32'))


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
