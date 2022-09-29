#******************************************************************************
# -*- coding: latin-1 -*-
# File    : Diagnose_Fingerprint_Read&Write.py
# Task    : Test for Diagnosejob 0x22 0xF15A und 0x2E 0xF15A
#
# Author  : An3Neumann
# Date    : 22.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 22.06.2021 | An3Neumann   | initial
# 1.1  | 03.02.2022 | Mohammed     | reworked test script after Adding  preconditions
# 1.2  | 16.02.2022 | Mohammed     | Added Security Method
# 1.3  | 23.05.2022 | Mohammed     | Aktualisiert  Vorbedingungen
# 1.4  | 25.07.2022 | Mohammed     | Testschritte Aktualisiert

#******************************************************************************
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
    testresult.setTestcaseId("TestSpec_167")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_common = functions_common.FunctionsCommon(testenv)
    write_value = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09]
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    diag_ident = identifier_dict['Fingerprint']

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: KL15 und KL30 an", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    testresult.append(["[.] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 1 (VPE_PRODUCTION)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 0 (IDLE)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 0 (IDLE)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    # silently go one chapter level up
    # testresult.append(["[-0]", ""])

    # Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    testresult.append(["[.] '%s' schreiben: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x2E] + diag_ident['identifier'] + write_value
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, [0x2E], 0x7F))

    # Wechsel in Extended Session: 0x1003
    testresult.append(["[.] In die Extended Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))
    time.sleep(1)

    # Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))
    
    testresult.append(["[.] '%s' schreiben: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x2E] + diag_ident['identifier'] + write_value
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, [0x2E], 0x31))
    
    # Wechsel in Programming Session: 0x1002
    testresult.append(["[.] In die Programming Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))
    #time.sleep(2)

    # Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    testresult.append(["[.] '%s' schreiben: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x22] + diag_ident['identifier'] + write_value
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, [0x22], 0x13))

    testresult.append(["[.] Security Access aktivieren", ""])
    testresult.extend(canape_diag.SecurityAccessProg())

    testresult.append(["[.] '%s' schreiben: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x2E] + diag_ident['identifier'] + write_value
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

   # test step 11
    # test step Manueller Test
    prg_counts = response[3:]
    testresult.append(["[.] MANUELLER TEIL:SW flashen mit vFlash: {}"
                      .format(HexList(prg_counts)),
                       ""])

    testresult.append(["\xa0beim Standard-Flashvorgang mit vFlash in der entsprechenden Maske :Tester Serial Number",
                       "INFO"])

    # A prompt for Yes/No/Cancel
    response = MessageBox("Please click YES to continue the test and overwrite Diagnose informations",
                          "Hinweis",
                          win32con.MB_SYSTEMMODAL + win32con.MB_YESNO)
    assert response == win32con.IDYES, "Test abgebrochen (vor Schreiben neuer Diagnosewerte)"

    testresult.append(["[.] Während Flashvorgang übernommenen Fingerprint mit  0x22F15B auslesen", ""])
    request = [0x22] + [0xF1, 0x5B]
    [response1, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[+] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response1, request))

    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response1, 20))

    write_value1 = [0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x22, 0x09, 0x05, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x00]
    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    expected_response = [0x62] + [0xF1, 0x5B] + write_value1
    testresult.append(canape_diag.checkResponse(response1, expected_response, ticket_id='FehlerId:EGA-PRM-168'))
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
