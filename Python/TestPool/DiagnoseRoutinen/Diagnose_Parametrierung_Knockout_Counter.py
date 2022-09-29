# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_Parametrierung_Knockout_Counter.py
# Title   : Diagnose Parametrierung Knockout Counter
# Task    : A minimal "Diagnose Parametrierung Knockout Counter!" test script
#
# Author  : Mohammed Abdul Karim
# Date    : 23.06.2021
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ********************************* Version ***********************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 03.11.2021 | Devangbhai   | initial
# 1.1  | 15.11.2021 | Mohammed     | Rework
# 1.2  | 10.01.2022 | H. Förtsch   | reworked test script by test spec
# 1.3  | 27.01.2022 | Mohammed     | Corrected in Test Step 2.8 und 3.1
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from diag_identifier import identifier_dict
from functions_diag import HexList

testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    hil = testenv.getHil()
    testresult = testenv.getResults()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    test_data = identifier_dict['Knockout_counter']
    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_161")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 1.1
    request = [0x22] + test_data['identifier']
    testresult.append(["[+] Auslesen der Knockout Counter: {}".format(HexList(request))])
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    knockout_counter_orig = response[3:]
    testresult.append(["Knockout Counter: {}".format(HexList(knockout_counter_orig)),
                       "INFO"])

    # test step 1.2
    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    # test step 2
    testresult.append(["[-] Schreiben im Factory Mode"])

    # test step 2.1
    testresult.append(["[+] Wechsel in die Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # test step 2.2
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 2.3
    testresult.append(["[.] Wechsel in Factory Mode:  0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode'))

    # test step 2.4
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 2.5
    testresult.append(["[.] Seed anfragen: 0x2761"])
    seed, result = canape_diag.requestSeed()
    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.extend(result)

    # test step 2.6
    testresult.append(["[.] Key berechnen:"])
    key, result = canape_diag.calculateKey(seed)
    testresult.append(result)

    # test step 2.7
    testresult.append(["[.] Key senden: 0x2762 + {}:".format(HexList(key))])
    result = canape_diag.sendKey(key)
    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.extend(result)

    # test step 2.8
    knockout_counter = [0xC8, 0xC8]
    testresult.append(["[.] Schreiben der Knockout Counter: 0x2E02CA + {} ({})"
                       .format(HexList(knockout_counter), knockout_counter),
                       ""])
    req = [0x2E, 0x02, 0xCA] + knockout_counter
    response, result = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    #testresult.append(canape_diag.checkPositiveResponse(response, request))
    testresult.append(canape_diag.checkResponse(response, [0x6E, 0x02, 0xCA]))  ########### added

    # test step 2.9
    testresult.append(["[.] Auslesen der Knockout Counter: 0x2202CA"])
    req = [0x22, 0x02, 0xCA]
    response, result = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response:0x6202CA + {}"
                       .format(HexList(knockout_counter)),
                       ""])
    expected_resp = [0x62, 0x02, 0xCA] + knockout_counter
    testresult.append(canape_diag.checkResponse(response, expected_resp))

    # test step 3
    testresult.append(["[-] Anpasswerte wieder auf vorherige Werte setzen", ""])

    # test step 3.1
    testresult.append(["[+] Schreiben des Knockout Counter: 0x2E02CA + {}"
                       .format(HexList(knockout_counter_orig)),
                       ""])
    req = [0x2E, 0x02, 0xCA] + knockout_counter_orig
    response, result = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    #testresult.append(canape_diag.checkPositiveResponse(response, request))
    testresult.append(canape_diag.checkResponse(response, [0x6E, 0x02, 0xCA]))  ########### added

    # test step 3.2
    testresult.append(["[.] Auslesen der Knockout Counter: 0x2202CA"])
    req = [0x22, 0x02, 0xCA]
    response, result = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response:0x6202CA + {}"
                       .format(HexList(knockout_counter_orig)),
                       ""])
    expected_resp = [0x62, 0x02, 0xCA] + knockout_counter_orig
    testresult.append(canape_diag.checkResponse(response, expected_resp))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

print "Done."
