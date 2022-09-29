# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_Knockout.py
# Title   : Diagnose Knockout
# Task    : Test for reading the Diagnose_Knockout
#
# Author  : S. Stenger
# Date    : 25.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 25.05.2021 | StengerS     | initial
# 1.1  | 25.06.2021 | StengerS     | added write jobs
# 1.2  | 20.12.2021 | H. Förtsch   | reworked test script by test spec
# 1.3  | 28.01.2021 | Mohammed     | reworked test script after Adding preconditions
# 1.4  | 28.01.2021 | Mohammed     | Vorbedingungen aktualisiert
# *****************************************************************************

# Imports #####################################################################
import time
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
    testresult.setTestcaseId("TestSpec_128")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize functions ####################################################
    hil = testenv.getHil()

    # Initialize variables ####################################################
    test_list = [identifier_dict['Knockout_counter'],
                 identifier_dict['Knockout_timer'],
                 identifier_dict['Knockout_test_mode']]

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

    # test steps 1
    testresult.append(["[.] In Default Session auslesen", ""])
    testresult.append(["[+0]", ""])
    response_dict = {}
    for test_data in test_list:

        testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                           .format(HexList(test_data['identifier']), test_data['name']),
                           ""])
        request = [0x22] + test_data['identifier']
        response, result = canape_diag.sendDiagRequest(request)
        testresult.append(result)

        testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

        testresult.append(["[.] Datenlänge überprüfen", ""])
        testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

        if test_data['name'] == 'Knockout_timer':
            testresult.append(["[.] BusKnockOut_Tmr_NVEM auswerten: aktiv", ""])
            testresult.append(canape_diag.checkResponseBitMask(response, 'XXXXXX1XXXXXXXXX'))

        if len(response) > 3:
            response_dict[test_data['name']] = response[3:]
            testresult.append(["\xa0Ausgelesener {}: {}"
                               .format(test_data['name'], response[3:]),
                               ""])
        else:
            testresult.append(["Unerwartete Response! Folgende Tests davon betroffen!", "FAILED"])

    # test steps 2
    testresult.append(["[-] Versuchen in Default, Extended und in Programming Session Anpasswerte zu schreiben", ""])
    testresult.append(["[+0]", ""])

    request_counter = [0x2E, 0x02, 0xCA] + response_dict['Knockout_counter']
    request_timer = [0x2E, 0x02, 0xCB] + response_dict['Knockout_timer']
    request_testmode = [0x2E, 0x09, 0xF3] + response_dict['Knockout_test_mode']

    for session in ['default', 'extended', 'programming']:

        testresult.append(["\nSchreiben in '{} session' überprüfen".format(session), ""])
        if session != "default":
            testresult.append(["[.] Wechsel in {} Session".format(session.capitalize()), ""])
            testresult.extend(canape_diag.changeAndCheckDiagSession(session))
            testresult.extend(canape_diag.changeAndCheckDiagSession(session, read_active_session=False))
            testresult.append(["[.] Lese aktuelle {} Session aus".format(session.capitalize()), ""])
            testresult.extend(canape_diag.checkDiagSession(session))

        # set knockout counter
        if session == "default":
            testresult.append(["[.] Knockout Counter schreiben und auf negative Response prüfen", ""])
            response, result = canape_diag.sendDiagRequest(request_counter)
            testresult.append(result)
            testresult.append(canape_diag.checkNegativeResponse(response, request_counter, 0x7F))

            # set knockout timer
            testresult.append(["[.] Knockout Timer schreiben und auf negative Response prüfen", ""])
            response, result = canape_diag.sendDiagRequest(request_timer)
            testresult.append(result)
            testresult.append(canape_diag.checkNegativeResponse(response, request_timer, 0x7F))

            # set knockout testmode
            testresult.append(["[.] Knockout Testmode schreiben und auf negative Response prüfen", ""])
            response, result = canape_diag.sendDiagRequest(request_testmode)
            testresult.append(result)
            testresult.append(canape_diag.checkNegativeResponse(response, request_testmode, 0x7F))

        elif session == "extended":
            testresult.append(["[.] Knockout Counter schreiben und auf positive Response prüfen", ""])
            response, result = canape_diag.sendDiagRequest(request_counter)
            testresult.append(result)
            testresult.append(canape_diag.checkPositiveResponse(response, request_counter))

            # set knockout timer
            testresult.append(["[.] Knockout Timer schreiben und auf positive Response prüfen", ""])
            response, result = canape_diag.sendDiagRequest(request_timer)
            testresult.append(result)
            testresult.append(canape_diag.checkPositiveResponse(response, request_timer))

            # set knockout testmode
            testresult.append(["[.] Knockout Testmode schreiben und auf negative Response prüfen", ""])
            response, result = canape_diag.sendDiagRequest(request_testmode)
            testresult.append(result)
            testresult.append(canape_diag.checkNegativeResponse(response, request_testmode, 0x33))

        elif session == "programming":
            testresult.append(["[.] Knockout Counter schreiben und auf negative Response prüfen", ""])
            response, result = canape_diag.sendDiagRequest(request_counter)
            testresult.append(result)
            testresult.append(canape_diag.checkNegativeResponse(response, request_counter, 0x31))

            # set knockout timer
            testresult.append(["[.] Knockout Timer schreiben und auf negative Response prüfen", ""])
            response, result = canape_diag.sendDiagRequest(request_timer)
            testresult.append(result)
            testresult.append(canape_diag.checkNegativeResponse(response, request_timer, 0x31))

            # set knockout testmode
            testresult.append(["[.] Knockout Testmode schreiben und auf negative Response prüfen", ""])
            response, result = canape_diag.sendDiagRequest(request_testmode)
            testresult.append(result)
            testresult.append(canape_diag.checkNegativeResponse(response, request_testmode, 0x31))

    # test steps 3
    testresult.append(["[-] Schreiben im Factory Mode", ""])

    # test step 3.1
    testresult.append(["[+] Wechsel in die Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    # test step 3.2
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 3.3
    testresult.append(["[.]  Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    # test step 3.4
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 3.5
    testresult.append(["[.] Seed anfragen: 0x2761", ""])
    seed, result = canape_diag.requestSeed()
    testresult.extend(result)

    # test step 3.6
    testresult.append(["[.] Key berechnen", ""])
    key, result = canape_diag.calculateKey(seed)
    testresult.append(result)

    # test step 3.7
    testresult.append(["[.] Key senden: 0x2762 + {}".format(HexList(key)), ""])
    result = canape_diag.sendKey(key)
    testresult.extend(result)

    # test step 3.8
    knockout_counter = [0xC8, 0xC8]
    request_counter = [0x2E, 0x02, 0xCA] + knockout_counter
    testresult.append(["[.] Schreiben der Knockout Counter: 0x2E02CA + C8C8 (jew. 200dez)", ""])
    response, result = canape_diag.sendDiagRequest(request_counter)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, [0x6E, 0x02, 0xCA]))

    # test step 3.9
    request = [0x22, 0x02, 0xCA]
    testresult.append(["[.] Auslesen der Knockout Counter: 0x2202CA", ""])
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, ticket_id='Fehler Id:EGA-PRM-227'))
    #testresult.append(canape_diag.checkResponse(response,
    #                                            [0x62, 0x02, 0xCA, 0xC8, 0xC8],
    #                                            ticket_id='Fehler Id:EGA-PRM-21'))
    #expected_resp = [0x62, 0x02, 0xCA] + knockout_counter
    #testresult.append(canape_diag.checkResponse(response, expected_resp, ticket_id='Fehler Id:EGA-PRM-21' ))

    # test step 3.10
    knockout_timer = [0x3C, 0x3C]
    request_timer = [0x2E, 0x02, 0xCB] + knockout_timer
    testresult.append(["[.] Schreiben der Knockout Timer: 0x2E0CB + 3C3C (jew. 60dez)", ""])
    response, result = canape_diag.sendDiagRequest(request_timer)
    testresult.append(result)
    # testresult.append(canape_diag.checkNegativeResponse(response, request_testmode, 0x31))
    testresult.append(canape_diag.checkResponse(response, [0x6E, 0x02, 0xCB]))

    # test step 3.11
    testresult.append(["[.] Auslesen der Knockout Timer: 0x2202CB", ""])
    response, result = canape_diag.sendDiagRequest([0x22, 0x02, 0xCB])
    testresult.append(result)
    #testresult.append(canape_diag.checkResponse(response, [0x62, 0x02, 0xCB, 0x3C, 0x3C]))
    expected_resp = [0x62, 0x02, 0xCB] + knockout_timer
    testresult.append(canape_diag.checkResponse(response, expected_resp, ticket_id='Fehler Id:EGA-PRM-227'))

    # test steps 4
    testresult.append(["[-] Versuchen, ungültigen Wert für den Timer zu schreiben (< Min-Wert)", ""])

    # test step 4.1
    testresult.append(["[+] Schreiben der Knockout Timer: 0x2E02CB + F200", ""])
    request_timer = [0x2E, 0x02, 0xCB] + [0xF2, 0x00]
    response, result = canape_diag.sendDiagRequest(request_timer)
    testresult.append(result)
    testresult.append(canape_diag.checkNegativeResponse(response, request_timer, 0x31))

    # test step 4.2
    testresult.append(["[.] Schreiben der Knockout Timer: 0x2E02CB + 3A80", ""])
    request_timer = [0x2E, 0x02, 0xCB] + [0x3A, 0x80] # 0x3A = 0011 1010 = 14 dez and BusKnockOut_Tmr_NVEM = 1 --> 0xF0 to 0x80 replaced
    response, result = canape_diag.sendDiagRequest(request_timer)
    testresult.append(result)
    testresult.append(canape_diag.checkNegativeResponse(response,
                                                        request_timer,
                                                        0x31,  #
                                                        ticket_id='Fehler Id:EGA-PRM-227'))  # NRC tbc
    # test steps 5
    testresult.append(["[-] Anpasswerte wieder auf vorherige Werte setzen", ""])

    # test step 5.1
    testresult.append(["[+] Schreiben der Knockout Counter: 0x2E02CA + <counter>", ""])
    request_counter = [0x2E, 0x02, 0xCA] + response_dict['Knockout_counter']  # [0x03, 0x30]
    response, result = canape_diag.sendDiagRequest(request_counter)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, [0x6E, 0x02, 0xCA]))
    #time.sleep(2)
    # test step 5.2
    testresult.append(["[.] Schreiben der Knockout Timer: 0x2E02CB + <timer>", ""])
    request_timer = [0x2E, 0x02, 0xCB] + response_dict['Knockout_timer']  # [0x0F, 0x0F]
    response, result = canape_diag.sendDiagRequest(request_timer)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, [0x6E, 0x02, 0xCB]))

    # test step 5.3
    testresult.append(["[.] Auslesen der Knockout Counter: 0x2202CA", ""])
    response, result = canape_diag.sendDiagRequest([0x22, 0x02, 0xCA])
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response,
                                                [0x62, 0x02, 0xCA] + response_dict['Knockout_counter'],
                                                ticket_id='Fehler Id:EGA-PRM-21')) # [0x03, 0x30]

    # test step 5.4
    testresult.append(["[.] Auslesen der Knockout Timer: 0x2202CB", ""])
    response, result = canape_diag.sendDiagRequest([0x22, 0x02, 0xCB])
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response,
                                                [0x62, 0x02, 0xCB] + response_dict['Knockout_timer']))  # [0x0F, 0x0F]

    # test steps 6
    testresult.append(["[-] Test Mode schreiben, lesen und nach KL15 Wechsel erneut lesen", ""])

    # test step 6.1
    testresult.append(["[+] Schreiben des Knockout Test Modes: 0x2E09F3 + 01", ""])
    request_testmode = [0x2E, 0x09, 0xF3] + [0x01]
    response, result = canape_diag.sendDiagRequest(request_testmode)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, [0x6E, 0x09, 0xF3]))

    # test step 6.2
    testresult.append(["[.] Auslesen des Knockout Test Modes: 0x2209F3", ""])
    response, result = canape_diag.sendDiagRequest([0x22, 0x09, 0xF3])
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, [0x62, 0x09, 0xF3, 0x01]))

    # test step 6.3
    testresult.append(["[.] KL15 und Restbussimulation aus", ""])
    testresult.append(["Setze KL15 auf 0 und Zykylzeit Warten", "INFO"])
    hil.cl15_on__.set(0)
    time.sleep(0.150)
    testresult.append(["Schalte Senden von empfangenen Signalen aus (HiL -> ECU)", "INFO"])
    hil.can0_HIL__HIL_TX__enable.set(0)

    # test step 6.4
    testresult.append(["[.] 1 Sekunde warten", ""])
    time.sleep(1)

    # test step 6.5
    testresult.append(["[.] KL15 und Restbussimulation an", ""])
    testresult.append(["Setze KL15 auf 1", "INFO"])
    hil.cl15_on__.set(1)
    testresult.append(["Schalte Senden von empfangenen Signalen an (HiL -> ECU)", "INFO"])
    hil.can0_HIL__HIL_TX__enable.set(1)

    # test step 6.6
    testresult.append(["[.] 1 Sekunde warten", ""])
    time.sleep(1)

    # test step 6.7
    # read knockout testmode
    testresult.append(["[.] Auslesen des Knockout Test Modes: 0x2209F3", ""])
    response, result = canape_diag.sendDiagRequest([0x22, 0x09, 0xF3])
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response, [0x62, 0x09, 0xF3, 0x00]))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    del(testenv)
    # #########################################################################

print "Done."
