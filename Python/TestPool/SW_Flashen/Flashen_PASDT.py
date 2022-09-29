# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : Flashen_PASDT.py
# Title   : Software Flashen mit dem PASDT
# Task    : Software Flashen mit PASDT Manuell
#
# Author  : Mohammed Abdul Karim
# Date    : 29.03.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 29.03.2022 | Mohammed  | initial

# ******************************************************************************
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
import win32con  # constants
from win32ui import MessageBox  # @UnresolvedImport pylint: disable=no-name-in-module
import functions_gearselection
import time

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_2")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_common = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    test_data = identifier_dict['VW Application Software Version Number']

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: KL15 und KL30 an", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    ############################
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[+] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))


    request = [0x22] + test_data['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 11
    # test step Manueller Test
    prg_counts = response[3:]
    testresult.append(["[.] MANUELLER TEIL:SW flashen mit PASDT: {}"
                      .format(HexList(prg_counts)),
                       ""])

    testresult.append(["beim Standard-Flashvorgang mit PASDT in der entsprechenden Maske :Tester Serial Number",
                       "INFO"])

    # A prompt for Yes/No/Cancel
    response = MessageBox("Please click YES to continue the test and overwrite Diagnose informations",
                          "Hinweis",
                          win32con.MB_SYSTEMMODAL + win32con.MB_YESNO)
    assert response == win32con.IDYES, "Test abgebrochen (vor Schreiben neuer Diagnosewerte)"

    testresult.append(["[.] '%s' schreiben: %s" % (test_data['name'], str(HexList(test_data['identifier']))), ""])
    request = [0x22] + test_data['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step
    testresult.append(["[.] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step
    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    # test step
    testresult.append(["[.] Inhalt der Response überprüfen", ""])
    expected_response = [0x62] + test_data['identifier'] + test_data['expected_response']
    testresult.append(canape_diag.checkResponse(response, expected_response))

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
