# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Routine_Check_Memory.py
# Title   : Routine Check Memory
# Task    : Test for Routine Diagnosejob 0x3101 0x0202
#
# Author  : Mohammed Abdul Karim
# Date    : 15.02.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 15.02.2022 | Mohammed   | initial
# 1.1  | 23.05.2022 | Mohammed     | Aktualisiert  Vorbedingungen
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import time
import functions_gearselection
import functions_common
import win32con  # constants
from win32ui import MessageBox  # @UnresolvedImport pylint: disable=no-name-in-module


# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_164")


    # Initialize variables ####################################################
    diag_ident = identifier_dict['Check Memory']

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_common = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

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

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    testresult.append(["[.] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 1 (VPE_PRODUCTION)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 0 (IDLE)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 0 (IDLE)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Lese aktuelle Diagnose Session aus"])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 2
    testresult.append(["[.] Routine starten: 0x3101 0x0202 0x00"])
    request = [0x31, 0x01] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0 Prüfe auf Negative Response:0x7F317E"])
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkNegativeResponse(response, request, 0x31))

    # test step 3
    testresult.append(["[.] In die Extended Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 4
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 5
    testresult.append(["[.] Routine starten: 0x3101 0x0202 0x00"])
    request = [0x31, 0x01] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0 Prüfe auf Negative Response:0x7F317E"])
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkNegativeResponse(response, request, 0x31))

    # test step 6
    testresult.append(["[.] In die Factory Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    # test step 7
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 8
    testresult.append(["[.] Routine starten: 0x3101 0x0202 0x00"])
    request = [0x31, 0x01] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0 Prüfe auf Negative Response:0x7F317E"])
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkNegativeResponse(response, request, 0x31))

    # test step 9
    testresult.append(["[.] In die Extended Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))
    #time.sleep(2)
    # test step 10
    testresult.append(["[.] In die Programming Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))

    # test step 11
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # test step 12

    # test step Manueller Test
    prg_counts = response[3:]
    testresult.append(["[.] Manuell die Übertragungsdauer der Routine überprüfen während SW Flashen: {}"
                      .format(HexList(prg_counts)),
                       ""])

    testresult.append(["\x0a beim Standard-Flashvorgang mit vFlash in der entsprechenden Maske :Tester Serial Number",
                       "INFO"])

    # A prompt for Yes/No/Cancel
    response = MessageBox("Please click YES to continue the test and overwrite Diagnose informations",
                          "Hinweis",
                          win32con.MB_SYSTEMMODAL + win32con.MB_YESNO)
    assert response == win32con.IDYES, "Test abgebrochen (vor Schreiben neuer Diagnosewerte)"

    testresult.append(["\x0a Prüfe Manuell die Übertragungsdauer der Routine überprüfen während SW Flashen: max 4 Sekunde ist", "PASSED"])

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