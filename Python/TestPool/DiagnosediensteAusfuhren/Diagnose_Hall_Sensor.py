# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_Hall_Sensor.py
# Title   : Diagnose Hall Sensor
# Task    : Read out ADC values of hall sensor and check if values are in range
#
# Author  : S. Stenger
# Date    : 21.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# *****************************************************************************
# ********************************* Version ***********************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 21.05.2021 | StengerS     | initial
# 1.1  | 31.05.2021 | StengerS     | added info for not implemented jobs
# 1.2  | 21.10.2021 | Mohammed     | Korrected  0 <= <Sensorwert 1> <= 4095 (0xFFF) values
# 1.3  | 09.12.2021 | H. Förtsch   | reworked test script by test spec
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_130")

    # Initialize variables ####################################################
    test_list = [identifier_dict['Hall-Sensor ADC1'],
                 identifier_dict['Hall-Sensor ADC2']]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    for test_data in test_list:
        # test step 1 and 4
        testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                           .format(HexList(test_data['identifier']), test_data['name']),
                           ""])
        request = [0x22] + test_data['identifier']
        response, result = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

        # test step 2 and 5
        testresult.append(["[.] Datenlänge überprüfen", ""])
        testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

        # test step 3 and 6
        testresult.append(["[.] Sensorwert auswerten", ""])
        if len(response) > 3:
            data = response[3:]  # just take data of complete response
            adc_value_dec = 0
            i = len(response) - 3 - 1
            for adc_value in data:
                adc_value_dec += adc_value << (i * 8)  # set all bytes together
                i -= 1

            testresult.append(["Empfangene Daten (Rohwert): {}\nEntspricht dem ADC Wert: {}"
                               .format(str(HexList(data)), adc_value_dec),
                               "INFO"])
            testresult.append(basic_tests.checkRange(adc_value_dec, 0, 0xFFF))

        else:
            testresult.append(["Keine Auswertung möglich, da falsche oder keine Response empfangen wurde!", "FAILED"])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print "Done."
