# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : Diagnose_Factory_Mode.py
# Task    : Test for write entrie in factory mode
#
# Author  : An3Neumann
# Date    : 28.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 28.06.2021 | An3Neumann | initial
# 1.1  | 23.08.2021 | Mohammed   | Added Ticke Id
# 1.2  | 23.08.2021 | Mohammed   | Rework
# 1.3  | 19.11.2021 | Mohammed   | Added Security Access
# ******************************************************************************
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
import functions_database

import time

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_158")

    # Initialize functions ####################################################
    func_common = functions_common.FunctionsCommon(testenv)
    func_db = functions_database.FunctionsDB()

    # Initialize variables ####################################################
    diag_ident_list = [  # [ diag job, new entry ]
        [identifier_dict['VW Spare Part Number'], [0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x31, 0x32]],
        [identifier_dict['System Supplier Identifier'], [0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39]],
        [identifier_dict['ECU Serial Number'], [0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0x31, 0x32]],
        [identifier_dict['System Supplier ECU Hardware Number'], [0x31, 0x32, 0x34, 0x35, 0x36, 0x37, 0x39, 0x38, 0x30]],
        [identifier_dict['System Supplier ECU Hardware Version Number'], [0x30, 0x30, 0x37]],
        [identifier_dict['System Supplier ECU Software Number'], [0x30, 0x30, 0x37, 0x38, 0x39, 0x40, 0x41, 042, 0x43]],
        [identifier_dict['System Supplier ECU Software Version Number'], [0x30, 0x30, 0x37]],
        [identifier_dict['VW System Name Or Engine Type'], [0x30, 0x30, 0x37, 0x38, 0x39, 0x41, 0x42, 0x43, 0x44, 0x45, 0x46, 0x47, 0x48]],
        [identifier_dict['VW ECU Hardware Version Number'], [0x30, 0x30, 0x37]],
        [identifier_dict['VW Workshop System Name'], [0x30, 0x30, 0x37, 0x38, 0x39]],
       # [identifier_dict['Fingerprint And Programming Date Of Logical Software Blocks'], [0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01]],
        #[identifier_dict['Fingerprint And Programming Date Of Logical Software Blocks'], [0x01] * 10 * 1],
        [identifier_dict['VW FAZIT Identification String'],
         [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE]],
    ]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Aktiviere Tester Present", ""])
    canape_diag.enableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["[+] In 'default session' wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))
    testresult.append(["[.] In 'factory mode' wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    testresult.append(["\xa0 Auslesen der Active Diagnostic Session: 0x22F186 ", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    testresult.append(["\xa0Security Access aktivieren"])

    testresult.append(["\xa0Seed anfragen: 0x2761"])
    seed, result = canape_diag.requestSeed()
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(result)

    testresult.append(["\xa0 Key berechnen:"])
    key, verdictkey = canape_diag.calculateKey(seed)
    testresult.append(verdictkey)

    testresult.append(["\xa0 Key senden: 0x2762 + <berechnet key>:"])
    verdict = canape_diag.sendKey(key)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(verdict)

    testresult.append(["[.] Schreibe neue Einträge im Factory Mode", ""])
    testresult.append(["\nFür alle Diagnosejob, zu denen gespeicherte Parameter (aus ECU Identifikation) in der "
                          "Datenbank vorliegen, wird der Schreibvorgang im Factory Mode durchgeführt.\n"
                          "Wenn in ECU Identifikation der Job keine Parameter zurückliefert (neg. Response) "
                          "werden die Parameter nicht überschrieben!", ""])
    testresult.append(["[+0]", ""])
    write_entries = []
    for diag_ident in diag_ident_list:
        testresult.append(["[.] Schreibdurchlauf für: %s" % diag_ident[0]['name'], ""])
        stored_param = func_db.getParamList(diag_ident[0]['name'])
        if stored_param:
            testresult.append(["\xa0'%s' lese (in Default Session): %s" % (
            diag_ident[0]['name'], str(HexList(diag_ident[0]['identifier']))), ""])
            request = [0x22] + diag_ident[0]['identifier']
            [response, result] = canape_diag.sendDiagRequest(request)
            read_param = response[3:]

            if stored_param != read_param:
                testresult.append(
                    ["Testloop abgebrochen für %s, um ECU Daten nicht durch überschreiben zu verfälschen\n"
                     "Gespeicherte Parameter (Database): %s\nAktuell ausgelesene Parameter: %s"
                     % (diag_ident[0]['name'], str(HexList(stored_param)), str(HexList(read_param))), "INFO"])
                testresult.append(
                    ["Gespeicherte Parameter in Databank weichen ab. Entweder 'ECU Identifikation' lief nicht, "
                     "oder Inhalt wurde seitdem überschrieben", "FAILED"])
            else:
                testresult.append(["\xa0Starte Testloop für %s\n"
                                   "Gespeicherte Parameter (Database): %s\nAktuell ausgelesene Parameter: %s"
                                   % (diag_ident[0]['name'], str(HexList(stored_param)), str(HexList(read_param))),
                                   "INFO"])

                write_entries.append(diag_ident[0]['name'])

                testresult.append(
                    ["\xa0'%s' schreiben: %s" % (diag_ident[0]['name'], str(HexList(diag_ident[0]['identifier']))), ""])
                # schreibe neue Daten (im Factory Mode)
                request = [0x2E] + diag_ident[0]['identifier'] + diag_ident[1]
                testresult.append(["Sende: " + str(HexList(request)), "INFO"])
                [response, result] = canape_diag.sendDiagRequest(request)
                testresult.append(result)
                testresult.append(["\xa0Auf positive Response überprüfen", ""])
                testresult.append(canape_diag.checkPositiveResponse(response, request))

                testresult.append(["\xa0'%s' lese (im Factory Mode): %s" % (
                diag_ident[0]['name'], str(HexList(diag_ident[0]['identifier']))), ""])
                request = [0x22] + diag_ident[0]['identifier']
                [response, result] = canape_diag.sendDiagRequest(request)

                testresult.append(["\xa0Auf positive Response überprüfen", ""])
                testresult.append(canape_diag.checkPositiveResponse(response, request))

                testresult.append(["\xa0Inhalt der Response überprüfen", ""])
                exp_response = [0x62] + diag_ident[0]['identifier'] + diag_ident[1]
        else:
            testresult.append(["Testloop abgebrochen für %s, um ECU Daten nicht durch überschreiben zu verfälschen\n"
                               "Keine gespeicherte Parameter (Database) vorhanden" % diag_ident[0]['name'], "FAILED"])

    testresult.append(["[-] Lese neue Einträge in Default Session", ""])
    testresult.append(["\nFür alle Diagnosejobs, deren Parameter im Factory Mode überschrieben wurden, wird geprüft,"
                          " dass die neuen Parameter auch in der Default Session lesbar sind", ""])
    testresult.append(["\xa0Zurück in 'default session' wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))
    testresult.append(["[+0]", ""])
    for diag_ident in diag_ident_list:
        testresult.append(["[.] Lesedurchlauf für: %s" % diag_ident[0]['name'], ""])
        if diag_ident[0]['name'] in write_entries:
            testresult.append(["\xa0'%s' lese (im Default Session): %s" % (
                diag_ident[0]['name'], str(HexList(diag_ident[0]['identifier']))), ""])
            request = [0x22] + diag_ident[0]['identifier']
            [response, result] = canape_diag.sendDiagRequest(request)
            read_param = response[3:]

            testresult.append(["\xa0Auf positive Response überprüfen", ""])
            testresult.append(canape_diag.checkPositiveResponse(response, request))

            testresult.append(["\xa0Inhalt der Response überprüfen", ""])
            exp_response = [0x62] + diag_ident[0]['identifier'] + diag_ident[1]
        else:
            testresult.append(["Es wurden keine Werte im Factory Mode geschrieben", "FAILED"])

    testresult.append(["[-] Schreibe alte Parameter aus Datenbank zurück", ""])
    testresult.append(
        ["\nFür alle Diagnosejobs, deren Parameter im Factory Mode überschrieben wurden, werden die in der Datenbank "
         "gespeicherten Werte zurückgeschrieben.", ""])
    testresult.append(["\xa0In 'factory mode' wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    # get Security Access
    testresult.append(["\xa0Auslesen der Active Diagnostic Session: 0x22F186 ", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    testresult.append(["\xa0Security Access aktivieren"])

    testresult.append(["\xa0Seed anfragen: 0x2761"])
    seed, result = canape_diag.requestSeed()
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(result)

    testresult.append(["\xa0Key berechnen:"])
    key, verdictkey = canape_diag.calculateKey(seed)
    testresult.append(verdictkey)

    testresult.append(["\xa0Key senden: 0x2762 + <berechnet key>:"])
    verdict = canape_diag.sendKey(key)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(verdict)

    testresult.append(["[+0]", ""])
    for diag_ident in diag_ident_list:
        testresult.append(["[.] Schreibdurchlauf für: %s" % diag_ident[0]['name'], ""])
        if diag_ident[0]['name'] in write_entries:
            request = [0x2E] + diag_ident[0]['identifier'] + stored_param
            testresult.append(["Sende: " + str(HexList(request)), "INFO"])
            [response, result] = canape_diag.sendDiagRequest(request)
            testresult.append(result)

            testresult.append(["\xa0Auf positive Response überprüfen", ""])
            testresult.append(canape_diag.checkPositiveResponse(response, request))

            testresult.append(["\xa0Inhalt der Response überprüfen", ""])
            exp_response = [0x62] + diag_ident[0]['identifier'] + stored_param
            testresult.append(canape_diag.checkResponse(response, exp_response, ticket_id='Fehler Id:EGA-PRM-29'))

        else:
            testresult.append(
                ["Kein Schreibdurchlauf für: %s (wurde nicht überschrieben)" % diag_ident[0]['name'], ""])

    testresult.append(["[-0]", ""])

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
