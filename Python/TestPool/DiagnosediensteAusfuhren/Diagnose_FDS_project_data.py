#******************************************************************************
# -*- coding: latin-1 -*-
# File    : Diagnose_FDS_project_data.py
# Task    : Test for Diagnosejob 0x22 0xF1D5
#
# Author  : An3Neumann
# Date    : 25.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 25.06.2021 | An3Neumann   | initial
# 1.2  | 28.01.2021 | Mohammed     | reworked test script after Adding preconditions
# 1.3  | 26.07.2022 | Mohammed     | Aktualisiert TestStep
#******************************************************************************
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import ResponseDictionaries
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
from ttk_checks import basic_tests
import time
import functions_gearselection

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_168")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_common = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    diag_ident = identifier_dict['FDS_project_data']

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
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

    testresult.append(["[.] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 1 (VPE_PRODUCTION)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 0 (IDLE)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 0 (IDLE)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)
    testresult.append(["[-0]", ""])

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up

    # Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

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

    # Wechsel in Extended Session: 0x1003
    testresult.append(["[.] In die Extended Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))
    time.sleep(1)

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

    # Wechsel in Programming Session: 0x1002
    testresult.append(["[.] In die Programming Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))
    time.sleep(1)

    # Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

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

print "Done."
