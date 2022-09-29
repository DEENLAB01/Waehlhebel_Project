# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_Response_On_Event.py
# Title   : Diagnose ResponseOnEvent
# Task    : Test for diag identifier 02B3
#
# Author  : S. Stenger
# Date    : 23.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 23.06.2021 | StengerS   | initial
# 1.1  | 23.08.2021 | Mohammed  | Added Ticket Id
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from diag_identifier import identifier_dict  # @UnresolvedImport

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_154")

    # Initialize variables ####################################################
    test_data = identifier_dict['Response_On_Event']

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+0]", ""])

    testresult.append(["[.] Initialisierung von ResponseOnEvent", ""])
    request = [0x86, 0x41, 0x03, 0x08, 0x19, 0x0E]
    expected_response = [0xC6, 0x41, 0x00, 0x03]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, expected_response, ticket_id='Fehler Id:EGA-PRM-28'))


    testresult.append(["[.] Starten des EventTriggers (StartResponseOnEvent)", ""])
    request = [0x86, 0x05, 0x00]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Status von ResponseOnEvent auslesen", ""])
    request = [0x22] + test_data['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["\xa0Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
    expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']['active']
    testresult.append(canape_diag.checkResponse(response, expected_response, ticket_id='Fehler Id:EGA-PRM-28'))


    testresult.append(["[.] Stoppen des EventTriggers (StopResponseOnEvent)", ""])
    request = [0x86, 0x00, 0x00]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkPositiveResponse(response, request, ticket_id='Fehler Id:EGA-PRM-28'))

    testresult.append(["[.] Status von ResponseOnEvent auslesen", ""])
    request = [0x22] + test_data['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["\xa0Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
    expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']['not active']
    testresult.append(canape_diag.checkResponse(response, expected_response))


    testresult.append(["[.] Deaktivieren des ResponseOnEvent (ClearResponseOnEvent)", ""])
    request = [0x86, 0x06, 0x00]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkPositiveResponse(response, request, ticket_id='Fehler Id:EGA-PRM-28'))

    testresult.append(["[.] Status von ResponseOnEvent auslesen", ""])
    request = [0x22] + test_data['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["\xa0Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    testresult.append(["\xa0Inhalt auf Korrektheit überprüfen", ""])
    expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']['not initialized']
    testresult.append(canape_diag.checkResponse(response, expected_response, ticket_id='Fehler Id:EGA-PRM-28'))


    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################