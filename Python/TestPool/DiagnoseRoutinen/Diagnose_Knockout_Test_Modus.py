# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_Knockout_Test_Modus.py
# Title   : Diagnose Knockout Test Modus
# Task    : A minimal "Diagnose Knockout Test Modus!" test script

# Author  : Mohammed Abdul Karim
# Date    : 15.11.2021
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 10.11.2021 | Mohammed  | initial
# 1.2  | 13.12.2021 | Mohammed   | Added Fehler id

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
from time import time as t

testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    hil = testenv.getHil()
    testresult = testenv.getResults()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_com = functions_common.FunctionsCommon(testenv)

    # Initialize variables ####################################################
    diag_ident = identifier_dict['Knockout_test_mode']

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_163")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # 1. In Default Session auslesen"
    testresult.append(["\xa01. In Default Session auslesen", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    testresult.append(["\xa01.2 Auslesen des Knockout Test Modes: 0x2209F3"])
    request = [0x22] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, ticket_id='Fehler-Id: EGA-PRM-134'))

    testresult.append(["Datenlänge: 1 Bytes überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length'], ticket_id='Fehler-Id: EGA-PRM-134'))

    testresult.append(["\xa0 2. Schreiben im Factory Mode", "INFO"])

    testresult.append(["\x0a 2.1 Wechsel in die Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    testresult.append(["\xa0 2.2 Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    testresult.append(["\x0a 2.3 Wechsel in Factory Mode:  0x1060", "INFO"])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    testresult.append(["\xa0 2.4 Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    testresult.append(["\xa0 2.5 Seed anfragen: 0x2761"])
    seed, result = canape_diag.requestSeed()
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(result)

    testresult.append(["\xa0 2.6 Key berechnen:"])
    key, verdictkey = canape_diag.calculateKey(seed)
    testresult.append(verdictkey)

    testresult.append(["\xa0 2.7 Key senden: 0x2762 + <berechnet key>:"])
    verdict = canape_diag.sendKey(key)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(verdict)

    testresult.append(["\xa0 3. Test Mode schreiben, lesen und nach KL15 Wechsel erneut lesen:"])

    testresult.append(["\xa0 3.1 Schreiben des Knockout Test Modes: 0x2E09F3 + 01"])
    req = [0x2E, 0x09, 0xF3, 0x01]
    [response, result] = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response: 0x6E 09F3 ist"])
    testresult.append(canape_diag.checkPositiveResponse(response, req))


    testresult.append(["\x0a 3.2 Auslesen des Knockout Test Modes: 0x2209F3"])
    req = [0x22, 0x09, 0xF3]
    [response, result] = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    expected_resp = [0x62, 0x09, 0xF3, 0x01]
    testresult.append(["Prüfe Positive Response: 0x6209F3 + 01", ""])
    testresult.append(canape_diag.checkResponse(response, expected_resp))

    testresult.append(["3.3 KL15 und Restbussimulation aus"])
    hil.cl15_on__.set(0)

    testresult.append(["3.4 Warte 1 Sekunde"])
    time.sleep(1)

    testresult.append(["3.5 KL15 und Restbussimulation an"])
    hil.cl15_on__.set(1)

    testresult.append(["3.6 1 Warte 1 Sekunde"])
    time.sleep(1)

    testresult.append(["\x0a 3.7 Auslesen des Knockout Test Modes: 0x2209F3"])
    req = [0x22, 0x09, 0xF3]
    [response, result] = canape_diag.sendDiagRequest(req)
    testresult.append(result)

   # testresult.append(["Prüfe Positive Response: 0x6209F3 ist", ""])
    #testresult.append(canape_diag.checkPositiveResponse(response, req))

    expected_resp = [0x62, 0x09, 0xF3, 0x00]
    testresult.append(["Prüfe Positive Response: 0x6209F3 + 00", ""])
    testresult.append(canape_diag.checkResponse(response, expected_resp, ticket_id='Fehler-Id: EGA-PRM-134'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print "Done."
