#******************************************************************************
# -*- coding: latin-1 -*-
# File    : Routine_Erase_Memory.py
# Title   : Routine_Erase_Memory
# Task    : Test for Routine_Check_Memory 0x3101 0xFF00  0x0101
#
# Author  : Mohammed Abdul Karim
# Date    : 19.11.2021
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 19.11.2021 | Mohammed     | initial
# 1.1  | 19.11.2021 | Mohammed     | Added Fehler Id
# 1.2  | 27.01.2021 | Mohammed     | reworked test script after Adding  preconditions
# 1.3  | 26.07.2022 | Mohammed     | Aktualisiert TestStep
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
    testresult.setTestcaseId("TestSpec_165")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_common = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_common = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    diag_ident = identifier_dict['Check Erase Memory']

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    ############################
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
    testresult.append(["[-0]", ""])
    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])

    # test step 1
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 2
    testresult.append(["[.] Routine starten: 0x3101 FF00 01 50 (Erase Memory)", ""])
    request = [0x31, 0x01] + diag_ident['identifier'] + [0x01, 0x50]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 3
    testresult.append(["[.] Prüfe auf Negative Response:0x7F3131", ""])
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkNegativeResponse(response, request, 0x31))

    # test step 4
    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, [0x31], 0x31, ticket_id= 'Fehler-Id:EGA-PRM-137'))

    # test step 5
    testresult.append(["[.] Wechsel in Extended Session : 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 6
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 7
    testresult.append(["[.] Routine starten: 0x3101 FF00 01 50 (Erase Memory)", ""])
    request = [0x31, 0x01] + diag_ident['identifier'] + [0x01, 0x50]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] Prüfe auf Negative Response:0x7F3131", ""])
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkNegativeResponse(response, request, 0x31))

    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, [0x31], 0x31, ticket_id= 'Fehler-Id:EGA-PRM-137'))

    # test step 10
    testresult.append(["[.] Wechsel in Programming Session : 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))

    # test step 11
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # test step 12
    testresult.append(["[.] Routine starten: 0x3101 FF00 01 50 (Erase Memory)", ""])
    request = [0x31, 0x01] + diag_ident['identifier'] + [0x01, 0x50]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 13
    testresult.append(["[.] Prüfe auf Negative Response:0x7F3133", ""])
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkNegativeResponse(response, request, 0x33, ticket_id='Fehler-Id:EGA-PRM-170'))

    # test step 14
    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, [0x31], 0x33, ticket_id='Fehler-Id:EGA-PRM-170'))

    # test step 15
    testresult.append(["[.] Wechsel in Default Session: 0x1001 und warte 1 Sekunde", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))
    time.sleep(1)

    # test step 16
    testresult.append(["[.] Wechsel in Factory Mode : 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    # test step 17
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 18
    testresult.append(["[.] Routine starten: 0x3101 FF00 01 50 (Erase Memory)", ""])
    request = [0x31, 0x01] + diag_ident['identifier'] +[0x01, 0x50]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 19
    testresult.append(["[.] Prüfe auf Negative Response:0x7F3131", ""])
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkNegativeResponse(response, request, 0x31))

    # test step 20
    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, [0x31], 0x31))

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
