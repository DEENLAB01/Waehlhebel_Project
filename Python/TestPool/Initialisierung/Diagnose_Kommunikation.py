# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_Kommunikation.py
# Title   : Diagnose Kommunikation
# Task    : Reads out Diagnose_Kommunikation
#
# Author  : Mohammed Abdul Karim
# Date    : 17.03.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 17.03.2022 | Mohammed     | initials
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_gearselection

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_384")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    test_list = [identifier_dict['VW Application Software Version Number'],
                 identifier_dict['VW ECU Hardware Number'],
                 identifier_dict['VW ECU Hardware Version Number']]
                 #identifier_dict['VW Spare Part Number']]

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

    testresult.append(["\xa0 Setze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186 ", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 2 to 7
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
        testresult.append(canape_diag.checkResponse(response[3:], expected_data))

        # silently go one chapter level up, add next parent chapter
        testresult.append(["[-0]", ""])


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
