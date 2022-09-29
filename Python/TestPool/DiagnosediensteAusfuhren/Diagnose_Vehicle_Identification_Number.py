# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_Vehicle_Identification_Number.py
# Title   : Diagnose Vehicle Identification Number
# Task    : Test for Diag identifier F190
#
# Author  : M. Abdul Karim
# Date    : 10.06.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 23.09.2021 | Mohammed   | initial
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport


# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_Unknown12")


    # Initialize variables ####################################################
    diag_ident = identifier_dict['Diagnose Vehicle Identification Number']


    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[+] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    testresult.append(["[.] '%s' auslesen: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x22] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length']))

    testresult.append(["[.] ]Inhalt der Response überprüfen", ""])
    exp_response = [0x62] + diag_ident['identifier'] + diag_ident['expected_response']
    testresult.append(canape_diag.checkResponse(response, exp_response))

    # Wechsel in Extended Session: 0x1003
    testresult.append(["[.] In die Extended Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))


    # Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    testresult.append(["[.] '%s' auslesen: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x22] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length']))

    testresult.append(["[.] Inhalt der Response überprüfen", ""])
    exp_response = [0x62] + diag_ident['identifier'] + diag_ident['expected_response']
    testresult.append(canape_diag.checkResponse(response, exp_response))

    # Wechsel in Wechsel in Factory Mode: 0x1060
    testresult.append(["[.] In die Programming Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    testresult.append(["[.] '%s' auslesen: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x22] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length']))

    testresult.append(["[.] Inhalt der Response überprüfen", ""])
    exp_response = [0x62] + diag_ident['identifier'] + diag_ident['expected_response']
    testresult.append(canape_diag.checkResponse(response, exp_response))

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