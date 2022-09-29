# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_Bootloader.py
# Title   : Diagnose Bootloader
# Task    : Reads out SW version and part number in bootloader mode
#
# Author  : S. Stenger
# Date    : 31.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 31.05.2021 | StengerS     | initial
# 1.1  | 18.08.2021 | Mohammed     | Added Ticket ID
# 1.2  | 26.10.2021 | Mohammed     | Added Bootloader Version
# 1.3  | 28.10.2021 | Mohammed     | Rework
# 1.4  | 03.12.2021 | H. Förtsch   | reworked test script by test spec
# 1.5  | 19.01.2022 | Mohammed     | corrected Bootloder version
# 1.6  | 28.01.2021 | Mohammed     | reworked test script after Adding  preconditions
# 1.7  | 23.05.2022 | Mohammed     | Aktualisiert  Vorbedingungen
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
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
    testresult.setTestcaseId("TestSpec_126")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    test_list = [identifier_dict['VW Application Software Version Number'],
                 identifier_dict['VW ECU Hardware Number'],
                 identifier_dict['VW ECU Hardware Version Number'],
                 identifier_dict['VW Spare Part Number']]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    ############################
    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    testresult.append(["[+] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 1 (VPE_PRODUCTION)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 0 (IDLE)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 0 (IDLE)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)
    #time.sleep(2)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    #testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186 ", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 2
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 3
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))
    #time.sleep(1)

    # test step 4
    testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming', read_active_session=False))

    # test step 5
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # test step 6 to 9
    for test_data in test_list:
        testresult.append(["[.] {}".format(test_data['name']), ""])

        if test_data['name'] == 'VW Application Software Version Number':
            expected_data = [0x30, 0x31, 0x31, 0x31]  #
        else:
            expected_data = test_data['expected_response']

        # test step x.1
        testresult.append(["[+] '{}' auslesen: {}"
                           .format(test_data['name'], HexList(test_data['identifier'])),
                           ""])
        request = [0x22] + test_data['identifier']
        response, result = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

        # test step x.2
        testresult.append(["[.] Datenlänge überprüfen", ""])
        testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

        # test step x.3
        testresult.append(["[.] Inhalt auf Korrektheit überprüfen", ""])
        testresult.append(canape_diag.checkResponse(response[3:], expected_data, ticket_id='Fehler Id:EGA-PRM-20'))

        # silently go one chapter level up, add next parent chapter
        testresult.append(["[-0]", ""])

    # test step 10
    testresult.append(["[.] Wechsel in Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    # test step 11
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown()
    del testenv
    # #########################################################################

print "Done."
