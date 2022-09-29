# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : Diagnose_Basic_Setting_Status.py
# Task    : Test for Diagnosejob 0x22 0x0102 
#
# Author  : An3Neumann
# Date    : 22.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 22.06.2021 | An3Neumann | initial
# 1.1  | 09.12.2021 | Mohammd    | Rework
# 1.2  | 05.01.2022 | Mohammd    | Removed Security part
# 1.3  | 17.01.2022 | Mohammd    | Rework after TestSpec Korrigiert.
# ******************************************************************************
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import ResponseDictionaries
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
from ttk_checks import basic_tests
import time

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_153")

    # Initialize functions ####################################################
    func_common = functions_common.FunctionsCommon(testenv)
    rd = ResponseDictionaries()

    # Initialize variables ####################################################
    diag_ident = identifier_dict['Basic Settings Status']
    exp_security_access_response = [0xC0]
    exp_routine_response = [0xC0]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["[+] '%s' auslesen: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x22] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length']))

    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    expected_response = [0x62] + diag_ident['identifier'] + diag_ident['expected_response']
    testresult.append(canape_diag.checkResponse(response, expected_response))

    # Wechsel in Extended Session: 0x1003
    testresult.append(["[.] Wechsel in die Extended Session", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    testresult.append(["[.] Aktuelle Diagnose Session prüfen", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    testresult.append(["[.] Starten Routine ClearUserDefinDTCInfor_Start_Routine_COP", ""])
    request = [0x31, 0x01, 0x04, 0x5A, 0xFF, 0xFF, 0xFF]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] '%s' auslesen: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x22] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length']))

    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    expected_response = [0x62] + diag_ident['identifier'] + exp_security_access_response
    testresult.append(canape_diag.checkResponse(response, expected_response, ticket_id='Fehler Id:EGA-PRM-131'))

    testresult.append(["[.] Wechsel in die Default Session", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    testresult.append(["[.] Aktuelle Diagnose Session prüfen", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    testresult.append(["[.] Starten Routine ClearUserDefinDTCInfor_Start_Routine_COP", ""])
    request = [0x31, 0x01, 0x04, 0x5A, 0xFF, 0xFF, 0xFF]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] '%s' auslesen: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x22] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length']))

    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    expected_response = [0x62] + diag_ident['identifier'] + exp_security_access_response
    testresult.append(canape_diag.checkResponse(response, expected_response, ticket_id='Fehler Id:EGA-PRM-131'))

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
