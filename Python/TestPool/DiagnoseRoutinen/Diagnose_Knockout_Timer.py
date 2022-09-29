# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_Knockout_Timer.py
# Title   : Diagnose Knockou Timer
# Task    : A minimal "Diagnose Knockout Timer!" test script

# Author  : Mohammed Abdul Karim
# Date    : 05.11.2021
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ********************************* Version ***********************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 10.11.2021 | Mohammed     | initial
# 1.1  | 10.11.2021 | Mohammed     | Rework
# 1.2  | 10.01.2022 | H. Förtsch   | reworked test script by test spec
# 1.3  | 27.01.2022 | Mohammed     | Corrected in Test Step 2.8, 3.1, 3.2 and 4.1
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList
from diag_identifier import identifier_dict

# #############################################################################
def writeKnockoutTimer(value):
    """ Writes a value of knockout timer
    Parameter:
        value - list of bytes
    Returns:
        [response, result]
    """
    testresult.append(["[.] Schreiben der Knockout Timer: 0x2E02CB + {} ({})"
                       .format(HexList(value), value),
                       ""])
    return canape_diag.sendDiagRequest([0x2E, 0x02, 0xCB] + value)

testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    hil = testenv.getHil()
    testresult = testenv.getResults()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    test_data = identifier_dict['Knockout_timer']

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_162")

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

    # test step 1
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 1.1
    request = [0x22] + test_data['identifier']
    testresult.append(["[+] Auslesen der Knockout Timer: {}".format(HexList(request))])
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    knockout_timer_orig = response[3:]
    testresult.append(["Knockout Timer: {}".format(HexList(knockout_timer_orig)),
                       "INFO"])

    # test step 1.2
    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    # test step 1.3
    testresult.append(["[.] BusKnockOut_Tmr_NVEM auswerten", ""])
    testresult.append(canape_diag.checkResponseBitMask(response, 'XXXXXX1XXXXXXXXX'))
    if testresult[-1][-1] == "PASSED":
        testresult.append(["NVEM Kopplung: aktiv", "PASSED"])
    else:
        testresult.append(["NVEM Kopplung: nicht aktiv", "FAILED"])

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
    knockout_timer = [0x3C, 0x3C]
    # testresult.append(["[.] Schreiben der Knockout Timer: 0x2E02CB + {} ({})"
    #                    .format(HexList(knockout_timer), knockout_timer),
    #                    ""])
    # req = [0x2E, 0x02, 0xCB] + knockout_timer
    # response, result = canape_diag.sendDiagRequest(req)
    # testresult.append(result)
    response, result = writeKnockoutTimer(knockout_timer)
    testresult.append(result)######## added
    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkResponse(response, [0x6E, 0x02, 0xCB], ticket_id='Fehler Id:EGA-PRM-227')) ########### added

    # test step 2.9
    testresult.append(["[.] Auslesen der Knockout Timer: 0x2202CB"])
    req = [0x22, 0x02, 0xCB]
    response, result = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response:0x6202CB + {}"
                       .format(HexList(knockout_timer)),
                       ""])
    expected_resp = [0x62, 0x02, 0xCB] + knockout_timer
    testresult.append(canape_diag.checkResponse(response, expected_resp))

    # test step 3
    testresult.append(["[-] Versuchen, ungültigen Wert für den Timer zu schreiben (< Min-Wert)"])
    # silently go one chapter level down
    testresult.append(["[+0]", ""])

    # test step 3.1
    # knockout_timer = [0xF2, 0x00]
    # testresult.append(["[+] Schreiben der Knockout Timer: 0x2E02CB + {}"
    #                    .format(HexList(knockout_timer)),
    #                    ""])
    # req = [0x2E, 0x02, 0xCB] + knockout_timer
    # response, result = canape_diag.sendDiagRequest(req)
    # testresult.append(result)
    response, result = writeKnockoutTimer([0xF2, 0x00])

    testresult.append(["\xa0Prüfe auf Negative Response: 0x7F 2E 31", ""])
    #testresult.append(canape_diag.checkNegativeResponse(response, req, 0x31))
    testresult.append(canape_diag.checkResponse(response, [0x7F, 0x2E, 0x31]))  ########### added

    # test step 3.2
    # knockout_timer = [0x3A, 0xF0]
    # testresult.append(["[+] Schreiben der Knockout Timer: 0x2E02CB + {}"
    #                    .format(HexList(knockout_timer)),
    #                    ""])
    # req = [0x2E, 0x02, 0xCB] + knockout_timer
    # response, result = canape_diag.sendDiagRequest(req)
    # testresult.append(result)
    response, result = writeKnockoutTimer([0x3A, 0xF0])
    testresult.append(result)  ######## added
    testresult.append(["\xa0Prüfe auf Positive Response: 0x6E 02 CB", ""])
    #testresult.append(canape_diag.checkNegativeResponse(response, req, 0x7F))
    testresult.append(canape_diag.checkResponse(response, [0x6E, 0x02, 0xCB]))  ########### added

    # test step 4
    testresult.append(["[-] Anpasswerte wieder auf vorherige Werte setzen", ""])
    # silently go one chapter level down
    testresult.append(["[+0]", ""])

    # test step 4.1
    # testresult.append(["[+] Schreiben des Knockout Timer: 0x2E02CB + {}"
    #                    .format(HexList(knockout_timer_orig)),
    #                    "INFO"])
    # req = [0x2E, 0x02, 0xCB] + knockout_timer_orig
    # response, result = canape_diag.sendDiagRequest(req)
    # testresult.append(result)
    response, result = writeKnockoutTimer(knockout_timer_orig)
    testresult.append(result)  ######## added
    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    #testresult.append(canape_diag.checkPositiveResponse(response, request))
    testresult.append(canape_diag.checkResponse(response, [0x6E, 0x02, 0xCB], ticket_id='Fehler Id:EGA-PRM-227'))  ########### added

    # test step 4.2
    testresult.append(["[.] Auslesen der Knockout Timer: 0x2202CB"])
    req = [0x22, 0x02, 0xCB]
    response, result = canape_diag.sendDiagRequest(req)
    testresult.append(result)

    testresult.append(["\xa0Prüfe Positive Response:0x6202CB + {}"
                       .format(HexList(knockout_timer_orig)),
                       ""])
    expected_resp = [0x62, 0x02, 0xCB] + knockout_timer_orig
    testresult.append(canape_diag.checkResponse(response, expected_resp, ticket_id='Fehler Id:EGA-PRM-227'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

print "Done."
