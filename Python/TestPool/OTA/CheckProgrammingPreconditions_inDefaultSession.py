# *****************************************************************************
# -*- coding: latin-1 -*-
# File    : CheckProgrammingPreconditions_inDefaultSession.py
# Title   : CheckProgrammingPreconditions_inDefaultSession
# Task    : Check Programming Preconditions in Default Session
#
# Author  : Mohammed Abdul Karim
# Date    : 02.05.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 02.05.2022 | Mohammed     | initial
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
    testresult.setTestcaseId("TestSpec_365")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    test_data = identifier_dict['Check Programming Preconditions']
    geschwindigkeit = 10
    #exp_wrong_prec = [0xA5, 0x05] # geschwindigkeit, Selector P

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: KL30 an und KL15 aus", ""])
    # testenv.startupECU()
    hil.cl30_on__.set(1)
    hil.cl15_on__.set(0)
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present Aktivieren", ""])
    canape_diag.enableTesterPresent()
    testresult.append(["[.] Setze OTAMC_D_01 setze auf VPE_PRODUCTION", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_CONTROL_A auf IDLE ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_CONTROL_D auf  IDLE ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)
    testresult.append(["[.] Setze VDSO_Vx3d auf 0 km/h (37766)", ""])
    testresult.append(func_gs.setVelocity_kmph(0))
    testresult.append(["[.] Setze Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))
    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

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

        testresult.append(["[.] Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

        testresult.append(["[.] Datenlänge überprüfen", ""])
        testresult.append(canape_diag.checkDataLength(response, len(expected_data), job_length=4))

        # test step
        testresult.append(["[.] Inhalt der Response überprüfen", ""])
        if not expected_data:
            testresult.append(["Kein Inhalt erwartet - Liste soll leer sein", "INFO"])
        expected_response = [0x71, 0x01] + test_data['identifier'] + expected_data
        testresult.append(canape_diag.checkResponse(response, expected_response))

    # test step 1
    testresult.append(["[.] Setze ORU_01_Status auf IDLE und Warte Zykluszeit", ""])
    hil.ORU_01__ORU_Status__value.set(0)
    time.sleep(.500)

    # test step 2
    testresult.append(["[.] Wechsel in Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # test step 3
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test steps 4 - 6
    _checkTestData(expected_data=[])

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
