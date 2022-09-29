# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_Programmzugriffe_TeilAutomation_NotUsed.py
# Title   : Diagnose Programmzugriffe Manuell (teilautomatisch)
# Task    : A semi-automated "Diagnose_Programmzugriffe!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 16.02.2021 | Abdul Karim  | initial
# 1.1  | 28.04.2021 | Abdul Karim  | added Default and Extended Session
# 1.2  | 18.05.2021 | StengerS     | automated test
# 1.3  | 23.06.2021 | StengerS     | added manual part
# 1.4  | 26.10.2021 | Mohammed     | added Programmzugriffe NACH /VOR dem Flashen Info
# 1.5  | 24.11.2021 | Mohammed     | added Security Accesss
# 1.6  | 02.12.2021 | H. Förtsch   | reworked test script by test spec
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import win32con  # constants
from win32ui import MessageBox  # @UnresolvedImport pylint: disable=no-name-in-module

from functions_diag import HexList
from diag_identifier import identifier_dict
import functions_database


# #############################################################################
def modifyDiagValue(key):
    """ Modify the value of the diagnose identifier
    Parameter:
        key - key of identifier_dict
    """
    diag_ident = identifier_dict[key]
    bytes_list = identifier_dict[key]["test_values"]

    testresult.append(["[.] {}".format(diag_ident['name']), ""])

    # test step x.y.1
    testresult.append(["[+] Schreibdurchlauf für: {}".format(diag_ident['name']), ""])

    stored_param = func_db.getParamList(diag_ident['name'])

    assert stored_param, ("Testloop abgebrochen für {}, um ECU Daten nicht durch überschreiben zu verfälschen\n"
                          "Keine gespeicherte Parameter (Database) vorhanden") \
                          .format(diag_ident['name'])

    testresult.append(["\xa0'{}' lese: {}"
                       .format(diag_ident['name'], HexList(diag_ident['identifier'])),
                       ""])
    diag_request = [0x22] + diag_ident['identifier']
    diag_response, diag_result = canape_diag.sendDiagRequest(diag_request)
    testresult.append(diag_result)

    read_param = diag_response[3:]

    assert stored_param == read_param, \
        ("Testloop abgebrochen für {name}, um ECU Daten nicht durch überschreiben zu verfälschen\n"
         "Gespeicherte Parameter (Database): {stored}\n"
         "Aktuell ausgelesene Parameter: {current}"
         "Gespeicherte Parameter in Databank weichen ab. "
         "Entweder 'ECU Identifikation' lief nicht, oder Inhalt wurde seitdem überschrieben") \
        .format(name=diag_ident['name'],
                stored=HexList(stored_param),
                current=HexList(read_param))

    testresult.append(["\xa0Starte Testloop für {}\n"
                       "Gespeicherte Parameter (Database): {}\n"
                       "Aktuell ausgelesene Parameter: {}"
                       .format(diag_ident['name'],
                               HexList(stored_param),
                               HexList(read_param)),
                       "INFO"])

    testresult.append(["\xa0'{}' schreiben: {}"
                       .format(diag_ident['name'],
                               HexList(diag_ident['identifier'])),
                       ""])
    testresult.append(["\xa0 Seed anfragen: 0x2761"])
    seed, diag_result = canape_diag.requestSeed()
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(diag_result)

    testresult.append(["\xa0 Key berechnen:"])
    key, diag_result = canape_diag.calculateKey(seed)
    testresult.extend(diag_result)

    testresult.append(["\xa0 Key senden: 0x2762 + <berechnet key>:"])
    diag_result = canape_diag.sendKey(key)
    testresult.append(["Auf positive Response überprüfen", ""])
    testresult.extend(diag_result)

    # schreibe neue Daten
    diag_request = [0x2E] + diag_ident['identifier'] + bytes_list
    testresult.append(["Sende: {}".format(HexList(diag_request)), "INFO"])
    diag_response, diag_result = canape_diag.sendDiagRequest(diag_request)
    testresult.append(diag_result)
    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(diag_response, diag_request))

    # test step x.y.2
    testresult.append(["[.] Prüfe Inhalt", ""])
    testresult.append(["\xa0'{}' lese (im Factory Mode): {}"
                       .format(diag_ident['name'],
                               HexList(diag_ident['identifier'])),
                       ""])
    diag_request = [0x22] + diag_ident['identifier']
    diag_response, diag_result = canape_diag.sendDiagRequest(diag_request)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(diag_response, diag_request))

    testresult.append(["\xa0Inhalt der Response überprüfen", ""])
    testresult.append(canape_diag.checkResponse(diag_response[3:], bytes_list))

    # silently go one chapter level up
    testresult.append(["[-0]", ""])

# #############################################################################
def checkDiagValue(key):
    """ Checks the value of the diagnose identifier
    Parameter:
        key - key of identifier_dict
    """
    diag_ident = identifier_dict[key]
    bytes_list = identifier_dict[key]["test_values"]

    # test step x.1
    testresult.append(["[.] Lesedurchlauf für: {}".format(diag_ident['name']), ""])

    testresult.append(["\xa0'{}' lese (im Default Session): {}"
                       .format(diag_ident['name'],
                               HexList(diag_ident['identifier'])),
                       ""])
    diag_request = [0x22] + diag_ident['identifier']
    diag_response, diag_result = canape_diag.sendDiagRequest(diag_request)
    testresult.append(diag_result)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(diag_response, diag_request))

    testresult.append(["\xa0Inhalt der Response überprüfen", ""])
    testresult.append(canape_diag.checkResponse(diag_response[3:], bytes_list))

# #############################################################################
def resetDiagValue(key):
    """ Reset the value of the diagnose identifier
    Parameter:
        key - key of identifier_dict
    """
    diag_ident = identifier_dict[key]
    stored_param = func_db.getParamList(diag_ident['name'])

    testresult.append(["[.] {}".format(diag_ident['name']), ""])

    # test step 17.x.1
    testresult.append(["[+] Schreibdurchlauf für: {}".format(diag_ident['name']), ""])

    diag_request = [0x2E] + diag_ident['identifier'] + stored_param
    testresult.append(["Sende: {}".format(HexList(diag_request)), "INFO"])
    diag_response, diag_result = canape_diag.sendDiagRequest(diag_request)
    testresult.append(diag_result)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(diag_response, diag_request))

    # test step 17.x.2
    testresult.append(["[.] Prüfe Inhalt", ""])

    diag_request = [0x22] + diag_ident['identifier']
    diag_response, diag_result = canape_diag.sendDiagRequest(diag_request)
    testresult.append(diag_result)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(diag_response, diag_request))

    testresult.append(["\xa0Inhalt der Response überprüfen", ""])
    testresult.append(canape_diag.checkResponse(diag_response[3:], stored_param))

    # silently go one chapter level up
    testresult.append(["[-0]", ""])


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

    identifier_dict['VW Spare Part Number']['test_values'] = [0x31, 0x32, 0x33, 0x34, 0x35,
                                                              0x36, 0x37, 0x38, 0x39, 0x31,
                                                              0x32]
    identifier_dict['ECU Serial Number']['test_values'] = [0x31, 0x32, 0x34, 0x35, 0x36, 0x37,
                                                           0x38, 0x20, 0x20, 0x20, 0x20, 0x20,
                                                           0x20, 0x20, 0x20, 0x20, 0x20, 0x20,
                                                           0x20, 0x20]
    identifier_dict['VW ECU Hardware Version Number']['test_values'] = [0x30, 0x30, 0x37]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] '{}' auslesen: {}"
                       .format(test_data['name'],
                               HexList(test_data['identifier'])),
                       ""])
    request = [0x22] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 2
    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    # test step 3
    prg_counts = response[3:]
    testresult.append(["[.] Programmzugriffe (Response) VOR dem Flashen zwischenspeichern: {}"
                       .format(HexList(prg_counts)),
                       ""])

    testresult.append(["Diagnose Informationen werden überschrieben, um zu prüfen, "
                       "dass diese durch das Flashen nicht wieder überschrieben werden",
                       "INFO"])

    # A prompt for Yes/No/Cancel
    response = MessageBox("Please click YES to continue the test and overwrite Diagnose informations",
                          "Hinweis",
                          win32con.MB_SYSTEMMODAL + win32con.MB_YESNO)
    assert response == win32con.IDYES, "Test abgebrochen (vor Schreiben neuer Diagnosewerte)"

    # test step 4
    testresult.append(["[.] In 'factory mode' wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    # test step 5
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test steps 6
    testresult.append(["[.] Neue Daten über Diagnose schreiben", ""])
    # silently go one chapter sublevel down
    testresult.append(["[+0]", ""])
    # test step 6.1
    modifyDiagValue('VW Spare Part Number')
    # test step 6.2
    modifyDiagValue('ECU Serial Number')
    # test step 6.3
    modifyDiagValue('VW ECU Hardware Version Number')

    # test step 7
    testresult.append(["[-] ECU ausschalten", ""])
    testenv.shutdownECU()
    testenv.canape_Diagnostic = None

    # clear instances before flashing
    testenv.asap3 = None
    testenv.canape_Diagnostic = None
    del (canape_diag)

    # MANUAL TEST START #######################################################
    # test steps 8
    testresult.append(["[.] MANUELLER TEIL: Gleiche SW erneut flashen (mit PASDT)", ""])
    # silently go one chapter sublevel down
    testresult.append(["[+0]", ""])

    for message in ["Manual Part begins:\n\nSwitch on ECU in model (XiBase) and press OK afterwards",
                    "Please flash now the same SW again and press OK afterwards",
                    "Switch off ECU in model (XiBase) and press OK afterwards"]:
        testresult.append(["[.] {}".format(message), ""])
        response = MessageBox(message,
                              "Achtung",
                              win32con.MB_SYSTEMMODAL + win32con.MB_OKCANCEL)
        assert response == win32con.IDOK, "Test abgebrochen (Manuelles Flashen nicht gestartet/beendet)"
        testresult.append(["Manual test step done.", "INFO"])

    # MANUAL TEST END #########################################################
    # test step 9
    testresult.append(["[-] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # test step 10
    testresult.append(["[.] Auslesen der Programmzugriffe: {}"
                       .format(HexList(test_data['identifier'])),
                       ""])
    request = [0x22] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 11
    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    prg_counts_new = response[3:]
    testresult.append(["\xa0Programmzugriffe (Response) NACH dem Flashen: {}".format(prg_counts_new), ""])

    # test step 12
    testresult.append(["[.] Prüfen, dass jeder Programmierzähler nach dem Flashen um 1 erhöht ist", ""])

    assert (len(prg_counts) == len(prg_counts_new)) and (len(prg_counts_new) % 2) == 0, \
        ("Reponse vor und nach dem Flashen unterschiedlich lang bzw. Datenlänge falsch!\n"
         "Programmzugriffe VOR dem Flashen: {}\n"
         "Programmzugriffe NACH dem Flashen: {}") \
        .format(prg_counts, prg_counts_new)

    for idx in range(0, len(prg_counts), 2):
        prg_cnt = prg_counts[idx + 1]
        prg_cnt_new = prg_counts_new[idx + 1]
        prg_cnt += prg_counts[idx] << 8  # set all bytes together
        prg_cnt_new += prg_counts_new[idx] << 8  # set all bytes together

        if prg_cnt + 1 == prg_cnt_new:
            verdict = "PASSED"
        else:
            verdict = "FAILED"
        testresult.append(["{}. SW-Block:\n"
                           "Programmzugriffe VOR dem Flashen: {}\n"
                           "Programmzugriffe NACH dem Flashen: {}"
                           .format(idx / 2 + 1, prg_cnt, prg_cnt_new),
                           verdict])

    # test step 13
    testresult.append(["[.] Lese neue Einträge in Default Session", ""])
    testresult.append(["\nFür alle Diagnosejobs, deren Parameter im Factory Mode überschrieben wurden, "
                       "wird geprüft, dass die neuen Parameter auch in der Default Session lesbar sind",
                       ""])
    testresult.append(["\xa0Zurück in 'default session' wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    # test step 14
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test steps 15
    testresult.append(["[.] Neue Daten über Diagnose schreiben", ""])
    # silently go one chapter sublevel down
    testresult.append(["[+0]", ""])
    # test step 15.1
    checkDiagValue('VW Spare Part Number')
    # test step 15.2
    checkDiagValue('ECU Serial Number')
    # test step 15.3
    checkDiagValue('VW ECU Hardware Version Number')

    # test step 16
    testresult.append(["[-] Schreibe alte Parameter aus Datenbank zurück", ""])
    testresult.append(["\nFür alle Diagnosejobs, deren Parameter im Factory Mode überschrieben wurden, "
                       "werden die in der Datenbank gespeicherten Werte zurückgeschrieben.",
                       ""])
    # test step 16.1
    testresult.append(["[+] ]In 'factory mode' wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))
    # test step 16.2
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test steps 17
    testresult.append(["[-] Werte zurückschreiben", ""])
    # silently go one chapter sublevel down
    testresult.append(["[+0]", ""])
    # test steps 17.1.x
    resetDiagValue('VW Spare Part Number')
    # test steps 17.2.x
    resetDiagValue('ECU Serial Number')
    # test steps 17.3.x
    resetDiagValue('VW ECU Hardware Version Number')

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

# handle assertion exceptions in case of breaking up the test
except AssertionError as ex:
    testresult.append([ex, "FAILED"])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    del testenv
    # #########################################################################

print "Done."
