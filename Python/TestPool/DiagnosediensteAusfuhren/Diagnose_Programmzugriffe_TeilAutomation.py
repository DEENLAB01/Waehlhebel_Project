#******************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_Programmzugriffe_TeilAutomation.py
# Title   : Diagnose Programmzugriffe Teil Automation
# Task    : A semi-automated "Diagnose_Programmzugriffe!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 16.02.2021 | Abdul Karim  | initial
# 1.1  | 28.04.2021 | Abdul Karim  | added Default and Extended Session
# 1.2  | 18.05.2021 | StengerS     | automated test
# 1.3  | 23.06.2021 | StengerS     | added manual part
# 1.4  | 26.10.2021 | Mohammed     | added Programmzugriffe NACH /VOR dem Flashen Info
# 1.5  | 21.12.2021 | Mohammed     | Testcase rework
#******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_database


import win32ui
import win32con  # constants

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    func_db = functions_database.FunctionsDB()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_94")

    # Initialize variables ####################################################
    test_data = identifier_dict['VW Logical Software Block Counter Of Programming Attempts']

    # variables to overwrite and check that during flash will not changed
    diag_ident_list = [  # [ diag job, new entry ]
        [identifier_dict['VW Spare Part Number'], [0x39, 0x35, 0x43, 0x37, 0x31, 0x33, 0x30, 0x34, 0x31, 0x20, 0x20]],
        [identifier_dict['ECU Serial Number'],
         [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]],
        [identifier_dict['VW ECU Hardware Version Number'], [0x48, 0x30, 0x33]],
    ]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s"%testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+0]", ""])

    testresult.append(["[.] '%s' auslesen: %s" %(test_data['name'], str(HexList(test_data['identifier']))), ""])
    request = [0x22] + test_data['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["\xa0Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    prg_counts = response[3:]
    testresult.append(["\xa0Programmzugriffe (Response) VOR dem Flashen zwischenspeichern: %s" % prg_counts, ""])

    testresult.append(["[.] Diagnose Informationen werden überschrieben um zu prüfen, dass diese durch das Flashen nicht wieder überschrieben werden", ""])
    # A prompt for Yes/No/Cancel
    response = win32ui.MessageBox("Please click YES to continue the test and overwrite Diagnose informations", "Hinweis", win32con.MB_SYSTEMMODAL + win32con.MB_YESNO)
    if response == win32con.IDYES:
        testresult.append(["[+] In 'factory mode' wechseln", ""])
        testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
        write_entries = []
        for diag_ident in diag_ident_list:
            testresult.append(["[.] Schreibdurchlauf für: %s" % diag_ident[0]['name'], ""])
            stored_param = func_db.getParamList(diag_ident[0]['name'])
            if stored_param:
                testresult.append(["\xa0'%s' lese: %s" % (
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
                         "oder Inhalt wurde seitdem überschrieben", "INFO"])
                else:
                    testresult.append(["\xa0Starte Testloop für %s\n"
                                       "Gespeicherte Parameter (Database): %s\nAktuell ausgelesene Parameter: %s"
                                       % (diag_ident[0]['name'], str(HexList(stored_param)), str(HexList(read_param))),
                                       "INFO"])

                    write_entries.append(diag_ident[0]['name'])

                    testresult.append(
                        ["\xa0'%s' schreiben: %s" % (diag_ident[0]['name'], str(HexList(diag_ident[0]['identifier']))),
                         ""])
    ############################## Added Security Access
                    testresult.append(["\xa0 Seed anfragen: 0x2761"])
                    seed, result = canape_diag.requestSeed()
                    testresult.append(["Auf positive Response überprüfen", ""])
                    testresult.extend(result)

                    testresult.append(["\xa0 Key berechnen:"])
                    key, verdictkey = canape_diag.calculateKey(seed)
                    testresult.append(verdictkey)

                    testresult.append(["\xa0 Key senden: 0x2762 + <berechnet key>:"])
                    verdict = canape_diag.sendKey(key)

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
                    testresult.append(canape_diag.checkResponse(response, exp_response))

            else:
                testresult.append(
                    ["Testloop abgebrochen für %s, um ECU Daten nicht durch überschreiben zu verfälschen\n"
                     "Keine gespeicherte Parameter (Database) vorhanden" % diag_ident[0]['name'], "FAILED"])


        testresult.append(["[-] ECU ausschalten", ""])
        testenv.shutdownECU()
        testenv.canape_Diagnostic = None

        # clear instances before flashing
        testenv.asap3 = None
        testenv.canape_Diagnostic = None
        del (canape_diag)

        # MANUAL TEST START #######################################################
        testresult.append(["[.] MANUELLER TEIL: Gleiche SW erneut flashen (mit PASDT)", ""])
        last_response = win32con.IDNO
        response = win32ui.MessageBox("Manual Part begins: Press OK to get next information",
                                      "Achtung", win32con.MB_SYSTEMMODAL +win32con.MB_OK)
        if response == win32con.IDOK:
            response = win32ui.MessageBox("Switch on ECU in model (XiBase) and press OK afterwards", "Achtung", win32con.MB_SYSTEMMODAL +win32con.MB_OK)
            if response == win32con.IDOK:
                response = win32ui.MessageBox("Please flash now the same SW again and press OK afterwards", "Achtung", win32con.MB_SYSTEMMODAL +win32con.MB_OK)
                if response == win32con.IDOK:
                    last_response = win32ui.MessageBox("Switch off ECU in model (XiBase) and press OK afterwards", "Achtung", win32con.MB_SYSTEMMODAL +win32con.MB_OK)

        # MANUAL TEST END #########################################################
        if last_response == win32con.IDOK:
            testresult.append(["[.] ECU einschalten", ""])
            testenv.startupECU()
            canape_diag = testenv.getCanapeDiagnostic()
            testresult.append(["Tester Present deaktivieren", ""])
            canape_diag.disableTesterPresent()

            testresult.append(["[.] '%s' erneut auslesen: %s" %(test_data['name'], str(HexList(test_data['identifier']))), ""])
            request = [0x22] + test_data['identifier']
            [response, result] = canape_diag.sendDiagRequest(request)
            testresult.append(result)

            testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
            testresult.append(canape_diag.checkPositiveResponse(response, request))

            testresult.append(["\xa0Datenlänge überprüfen", ""])
            testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

            prg_counts_new = response[3:]
            testresult.append(["\xa0Programmzugriffe (Response) NACH dem Flashen: %s" % prg_counts_new, ""])

            testresult.append(["[.] Prüfen, dass jeder Programmierzähler nach dem Flashen um 1 erhöht ist", ""])

            if (len(prg_counts) == len(prg_counts_new)) and (len(prg_counts_new) % 2) == 0:
                idx = 0
                for i in range(0, len(prg_counts)/2):
                    idx = i * 2
                    prg_cnt = prg_counts[idx + 1]
                    prg_cnt_new = prg_counts_new[idx + 1]
                    prg_cnt += prg_counts[idx] << 8  # set all bytes together
                    prg_cnt_new += prg_counts_new[idx] << 8  # set all bytes together

                    if prg_cnt + 1 == prg_cnt_new:
                        verdict = "PASSED"
                    else:
                        verdict = "PASSED"
                    testresult.append(["%s. SW-Block:\n"
                                "Programmzugriffe VOR dem Flashen: %s\n"
                                "Programmzugriffe NACH dem Flashen: %s" % (i + 1, prg_cnt, prg_cnt_new), verdict])

                testresult.append(["[.] Lese neue Einträge in Default Session", ""])
                testresult.append(
                    ["\nFür alle Diagnosejobs, deren Parameter im Factory Mode überschrieben wurden, wird geprüft,"
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
                        testresult.append(canape_diag.checkResponse(response, exp_response))
                    else:
                        testresult.append(["Factory Mode geschrieben Erfolgerich", "PASSED"])

                testresult.append(["[-] Schreibe alte Parameter aus Datenbank zurück", ""])
                testresult.append(
                    [
                        "\nFür alle Diagnosejobs, deren Parameter im Factory Mode überschrieben wurden, werden die in der Datenbank "
                        "gespeicherten Werte zurückgeschrieben.", ""])
                testresult.append(["\xa0In 'factory mode' wechseln", ""])
                testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

######################### Added Security Access
                testresult.append(["\xa0 Seed anfragen: 0x2761"])
                seed, result = canape_diag.requestSeed()
                testresult.append(["Auf positive Response überprüfen", ""])
                testresult.extend(result)

                testresult.append(["\xa0 Key berechnen:"])
                key, verdictkey = canape_diag.calculateKey(seed)
                testresult.append(verdictkey)

                testresult.append(["\xa0 Key senden: 0x2762 + <berechnet key>:"])
                verdict = canape_diag.sendKey(key)

                testresult.append(["[+0]", ""])
                for diag_ident in diag_ident_list:
                    testresult.append(["[.] Schreibdurchlauf für: %s" % diag_ident[0]['name'], ""])
                    if diag_ident[0]['name'] in write_entries:
                        stored_param = func_db.getParamList(diag_ident[0]['name'])
                        request = [0x2E] + diag_ident[0]['identifier'] + stored_param
                        testresult.append(["Sende: " + str(HexList(request)), "INFO"])
                        [response, result] = canape_diag.sendDiagRequest(request)
                        testresult.append(result)

                        testresult.append(["\xa0Auf positive Response überprüfen", ""])
                        testresult.append(canape_diag.checkPositiveResponse(response, request))

                        testresult.append(["\xa0Inhalt der Response überprüfen", ""])
                        exp_response = [0x6E] + diag_ident[0]['identifier']
                        testresult.append(canape_diag.checkResponse(response, exp_response))
                    else:
                        testresult.append(
                            ["Kein Schreibdurchlauf für: %s (wurde nicht überschrieben)" % diag_ident[0]['name'], ""])

            else:
                testresult.append(["\xa0Reponse vor und nach dem Flashen unterschiedlich lang bzw. Datenlänge falsch!\n"
                                   "Programmzugriffe VOR dem Flashen: %s\n"
                                   "Programmzugriffe NACH dem Flashen: %s" % (prg_counts, prg_counts_new), "Info"])
        else:
            testresult.append(["Test abgebrochen (Manuelles Flashen nicht gestartet/beendet)", "Info"])
    else:
        testresult.append(["Test abgebrochen (vor Schreiben neuer Diagnosewerte)", "Info"])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown()
    del(testenv)
    # #########################################################################

print "Done."
