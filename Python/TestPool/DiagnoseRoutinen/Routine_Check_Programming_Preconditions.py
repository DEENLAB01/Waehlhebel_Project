# *****************************************************************************
# -*- coding: latin-1 -*-
# File    : Routine_Check_Programming_Preconditions.py
# Title   : Routine Check Programming Preconditions
# Task    : Test for Routine Diagnosejob 0x3101 0x0203
#
# Author  : An3Neumann
# Date    : 08.07.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 08.07.2021 | An3Neumann   | initial
# 1.1  | 22.12.2021 | H. Förtsch   | reworked test script by test spec
# 1.2  | 10.01.2022 | Mohammed     | Corrected exp_wrong_prec value
# 1.3  | 31.01.2022 | Mohammed     | Corrected exp response value
# 1.5  | 14.04.2022 | Mohammed     | Added Zykluszeit
# 1.6  | 24.05.2022 | Mohammed     | Aktualisiert  Vorbedingungen
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv

from functions_diag import HexList
from diag_identifier import identifier_dict
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
    testresult.setTestcaseId("TestSpec_149")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    test_data = identifier_dict['Check Programming Preconditions']
    geschwindigkeit = 10
    exp_wrong_prec = [0xA5, 0x05] # geschwindigkeit, Selector P

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()
    testresult.append(["[.] Setze SiShift_01:SIShift_StLghtDrvPosn auf P", ""])
    testresult.append(func_gs.changeDrivePosition('P'))
    testresult.append(["[.] Setze Geschwindigkeit auf 0km/h", ""])
    testresult.append(func_gs.setVelocity_kmph(velocity_kmph=0))

    testresult.append(["[.] Setze MM_PropulsionSystemActive auf 0", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append(["[.] Setze OTAMC_D_01 setze auf VPE_NONE", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze ORU_CONTROL_A auf RUNNING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_CONTROL_D auf  RUNNING ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    testresult.append(["[.] Warte Zykluszeit", ""])
    time.sleep(0.500)

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # -------------------------------------------------------------------------
    def _checkTestData(expected_data):
        # test step
        testresult.append(["[.] Programmiervorbedingungen prüfen: 0x3101 {}"
                           .format(HexList(test_data['identifier'])),
                           ""])
        request = [0x31, 0x01] + test_data['identifier']
        response, result = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

        testresult.append(["\xa0Datenlänge überprüfen", ""])
        testresult.append(canape_diag.checkDataLength(response, len(expected_data), job_length=4))

        # test step
        testresult.append(["[.] Inhalt der Response überprüfen", ""])
        if not expected_data:
            testresult.append(["Kein Inhalt erwartet - Liste soll leer sein", "INFO"])
        expected_response = [0x71, 0x01] + test_data['identifier'] + expected_data
        testresult.append(canape_diag.checkResponse(response, expected_response))

    # test step 1
    testresult.append(["[.] Lese aktuelle Diagnose Session aus und warte 2 Sekunde", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))
    time.sleep(2)

    # test steps 2 - 3
    _checkTestData(expected_data=[])

    # test step 4
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 5
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test steps 6 - 7
    _checkTestData(expected_data=[])

    # test step 8
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    # test step 9
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))
    #time.sleep(1)
    # test steps 10 - 11
    _checkTestData(expected_data=[])

    # test step 12
    testresult.append(["[.] Setze Geschwindigkeit auf {}km/h".format(geschwindigkeit), ""])
    testresult.append(func_gs.setVelocity_kmph(velocity_kmph=geschwindigkeit))

    # test step 13
    testresult.append(['[.] Setze SiShift_01:SIShift_StLghtDrvPosn auf "R"', ""])
    testresult.append(func_gs.changeDrivePosition('R'))
    testresult.append(['[.] Warte 2 Sekunde ', ""])
    time.sleep(2)

    # test step 14
    testresult.append(["[.] Wechsel in Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    # test step 15
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test steps 16 - 17
    _checkTestData(expected_data=[0xA5, 0x05])

    # test step 18
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 19
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test steps 20 - 21
    _checkTestData(expected_data=[0xA5, 0x05])

    # test step 22
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    # test step 23
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test steps 24 - 25
    _checkTestData(expected_data=[0xA5, 0x05])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup #################################################################
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

print "Done."
