#******************************************************************************
# -*- coding: latin-1 -*-
# File    : Routine_Verify_Partial_Software_Checksum.py
# Task    : Test for Routine_Verify_Partial_Software_Checksum 0x3101054420040050 Checksume
# Task    : Tests if Routine_Verify_Partial_Software_Checksum is successful
#
# Author  : Mohammed Abdul Karim
# Date    : 23.11.2021
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name         | Description
#------------------------------------------------------------------------------
# 1.0  | 23.11.2021 | Mohammed     | initial
# 1.1  | 13.11.2021 | Mohammed     | Added Fehler Id
# 1.2  | 27.01.2021 | Mohammed     | reworked test script after Adding  preconditions
# 1.2  | 03.03.2022 | Mohammed     | TestSpec aktuliziert folgende PFIFF-Ticket: 335350
# 1.5  | 23.05.2022 | Mohammed     | Aktualisiert  Vorbedingungen
# 1.6  | 26.07.2022 | Mohammed     | Aktualisiert TestStep
#******************************************************************************
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
import time
from ttk_checks import basic_tests
import functions_gearselection

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_156")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_common = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    diag_ident = identifier_dict['Routine Verify Partial Software Checksum']

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 1 (VPE_PRODUCTION)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 0 (IDLE)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 0 (IDLE)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)
    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    time.sleep(1)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: %s"%testenv.script_name.split('.py')[0], ""])

    # test step 1
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 2
    testresult.append(["[.] Routine starten: 0x3101 0544 20 04 00 50 31 22 AA 9D (Verify_partial_software_checksum)", ""])
    request = [0x31, 0x01] + diag_ident['identifier'] + [0x20, 0x04, 0x00, 0x50, 0x31, 0x22, 0xAA, 0x9D]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 3
    #testresult.append(["[.] Prüfe auf Negative Response:0x7F31 + 1 Byte", ""])
    testresult.append(["[.] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 4
    testresult.append(["[.] Inhalt der Response überprüfen", ""])
    exp_response = [0x62] + diag_ident['identifier'] + diag_ident['expected_response']
    testresult.append(canape_diag.checkResponse(response, [0x71, 0x01, 0x05, 0x44, 0x00]))

    # test step 5
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 6
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 7
    testresult.append(["[.] Routine starten: 0x3101 0544 20 04 00 50 31 22 AA 9D (Verify_partial_software_checksum)", ""])
    request = [0x31, 0x01] + diag_ident['identifier'] + [0x20, 0x04, 0x00, 0x50, 0x31, 0x22, 0xAA, 0x9D]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 8
    testresult.append(["[.] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, ticket_id='Fehler-Id: EGA-PRM-132'))

    # test step 9
    testresult.append(["[.] Inhalt der Response überprüfen", ""])
    exp_response = [0x62] + diag_ident['identifier'] + diag_ident['expected_response']
    testresult.append(canape_diag.checkResponse(response, [0x71, 0x01, 0x05, 0x44, 0x00]))

    # test step 10
    testresult.append(["[.] Wechsel in Programming Session : 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))

    # test step 11
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # test step 12
    testresult.append(["[.] Routine starten: 0x3101 0544 20 04 00 50 31 22 AA 9D (Verify_partial_software_checksum)", ""])
    request = [0x31, 0x01] + diag_ident['identifier'] + [0x20, 0x04, 0x00, 0x50, 0x31, 0x22, 0xAA, 0x9D]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 13
    testresult.append(["[.] Prüfe auf Negative Response:0x7F31 + 1 Byte", ""])
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkNegativeResponse(response, request, 0x31))

    # test step 14
    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, [0x31], 0x31, ticket_id='Fehler-Id:EGA-PRM-137'))

    # test step 15
    testresult.append(["[.] Wechsel in Defaul Session Mode: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))
    time.sleep(1)
    # test step 16
    testresult.append(["[.] Wechsel in Factory Session : 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))
    time.sleep(1)
    # test step 17
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 18
    testresult.append(["[.] Routine starten: 0x3101 0544 20 04 00 50 31 22 AA 9D (Verify_partial_software_checksum)", ""])
    request = [0x31, 0x01] + diag_ident['identifier'] + [0x20, 0x04, 0x00, 0x50, 0x31, 0x22, 0xAA, 0x9D]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, ticket_id='Fehler-Id: EGA-PRM-229'))

    testresult.append(["[.] Inhalt der Response überprüfen", ""])
    exp_response = [0x62] + diag_ident['identifier'] + diag_ident['expected_response']
    testresult.append(canape_diag.checkResponse(response, [0x71, 0x01, 0x05, 0x44, 0x00], ticket_id='Fehler-Id: EGA-PRM-229'))

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
