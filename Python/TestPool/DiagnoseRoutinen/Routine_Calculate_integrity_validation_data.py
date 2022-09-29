#******************************************************************************
# -*- coding: latin-1 -*-
# File    : Routine_Calculate_integrity_validation_data.py
# Title   : Routine Calculate integrity validation data
# Task    : Test for Routine Diagnosejob 0x3101 0x0253
#
# Author  : An3Neumann
# Date    : 05.07.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 05.07.2021 | An3Neumann | initial
# 1.1  | 23.08.2021 | Mohammed   | Added Ticket Id
# 1.2  | 02.02.2022 | Mohammed   | corrected NRC
# 1.3  | 11.02.2022 | Mohammed   | Reworked after TestSpec correction
# 1.4  | 11.02.2022 | Mohammed   | Added Ticket Id
# 1.5  | 03.03.2022 | Mohammed   | TestSpec aktuliziert folgende PFIFF: 335337
# 1.6  | 26.07.2022 | Mohammed     | Aktualisiert TestStep
#******************************************************************************
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
import time
from ttk_checks import basic_tests
import functions_gearselection
from diag_identifier import DIAG_SESSION_DICT
from functions_nm import _compare
# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_157")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_common = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    diag_ident = identifier_dict['Calculate_integrity_validation_data']
    test_sessions = {
        1: {'session': 'Default Session', 'allowed': True},
        2: {'session': 'Extended Session', 'allowed': True},
        3: {'session': 'Factory Mode', 'allowed': True},
        # 4: {'session': 'Programming Session', 'allowed': False},
    }
    calc_result = diag_ident['expected_response'][0]
    hash_type = diag_ident['expected_response'][1]
    hash_value = diag_ident['expected_response'][2:]

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

    for session in test_sessions:
        curr_session = test_sessions[session]['session']
        set_check_session = curr_session.split(' ')[0].lower()
        allowed = test_sessions[session]['allowed']
        if session == 1:
            # Auslesen der Active Diagnostic Session: 0x22F186
            testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
            testresult.extend(canape_diag.checkDiagSession(set_check_session))
        else:
            # Wechsel in Extended Session: 0x1003
            testresult.append(["[.] In die %s wechseln"%curr_session, ""])
            testresult.extend(canape_diag.changeAndCheckDiagSession(set_check_session))
            time.sleep(1)

        for ident in diag_ident['identifier']:

            testresult.append(["[.] '%s (%s)' auslesen: %s" % (diag_ident['name'], ident, str(HexList(diag_ident['identifier'][ident]))), ""])
            request = [0x31, 0x01] + diag_ident['identifier'][ident]
            [response, result] = canape_diag.sendDiagRequest(request)
            testresult.append(result)

            if allowed:

                testresult.append(["[.] Auf positive Response überprüfen", ""])
                descr, verdict = canape_diag.checkPositiveResponse(response, request, 4)
                testresult.append([descr, verdict])

                testresult.append(["[.] Datenlänge überprüfen", ""])
                if verdict == 'FAILED':
                    testresult.append(["Prüfung der Datenlänge nicht möglich, da keine positive Response kam", "FAILED"])
                else:
                    testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length'], 4, ticket_id='Fehler Id:EGA-PRM-31'))

                testresult.append(["[.] Inhalt der Response überprüfen", ""])
                if verdict == 'FAILED':
                    testresult.append(
                        ["Prüfung des Inhaltes nicht möglich, da keine positive Response kam", "FAILED"])
                else:
                    check_response = response[4:]

                    testresult.append(["[+] Prüfe Byte 0: 'Result of Calculation'", ""])
                    testresult.append(
                        basic_tests.checkStatus(
                            current_status=check_response[0],
                            nominal_status=calc_result,
                            descr="Prüfe, dass Calculation Result wie erwartet ist (0x%02X)" % (calc_result)
                        )
                    )

                    testresult.append(["[.] Prüfe Byte 1: 'Type of Hash'", ""])
                    testresult.append(
                        basic_tests.checkStatus(
                            current_status=check_response[1],
                            nominal_status=hash_type,
                            descr="Prüfe, dass Hash Type wie erwartet ist (0x%02X)" % (hash_type)
                        )
                    )

                    testresult.append(["[.] Prüfe Byte 2-32: 'Hashvalue'", ""])
                    if len(check_response) > 2:
                        # if len(check_response) == 34:
                            # descr, verdict = basic_tests.checkStatus(
                            #         current_status=check_response[2:],
                            #         nominal_status=hash_value,
                            #         descr="Prüfe, dass Hash Type wie erwartet ist (%s)" % str(HexList(hash_value))
                            #     )
                        '''testresult.append(basic_tests.compare(
                            left_value=HexList(check_response[2:]),
                            operator="==",
                            right_value=HexList(hash_value),
                            descr="Prüfe, dass Hashvalue wie erwartet ist" ))
                            '''

                        testresult.append(_compare(
                            left_value=HexList(check_response[2:]),
                            operator="==",
                            right_value=HexList(hash_value),
                            descr="Prüfe, dass Hashvalue wie erwartet ist",
                            ticket_id='FehlerId:EGA-PRM-171'))

                        # testresult.append(
                        #     basic_tests.checkStatus(
                        #         current_status=HexList(check_response[2:]),
                        #         nominal_status=hash_value,
                        #         descr="Prüfe, dass Hash Type wie erwartet ist (0x%02X)" % (hash_type)
                        #     )
                        # )
                        # else:
                        #     descr = "Länge des Hashwertes ist falsch"
                        #     verdict = 'FAILED'
                    else:
                        descr = "Es wurde kein Hashwert zurückgegeben"
                        verdict = 'FAILED'
                    testresult.append([descr, verdict])
                    testresult.append(["[-0]", ""])
            else:
                testresult.append(["\xa0Auf negative Response überprüfen", ""])
                testresult.append(canape_diag.checkNegativeResponse(response, [0x31], 0x7F))

    #test step 16
    testresult.append(["[.] Wechsel in die Default Session: 0x1001", ""])
    test_data = DIAG_SESSION_DICT['default']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # test step 17
    testresult.append(["[.] Erneut Extended Session anfordern: 0x1003", ""])
    test_data = DIAG_SESSION_DICT['extended']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # # test step 18
    # testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    # test_data = DIAG_SESSION_DICT['programming']
    # request = test_data['identifier']
    # response, result = canape_diag.sendDiagRequest(request)
    # testresult.append(result)
    # testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    # testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # test step 18
    testresult.append(["[.] Wechsel in Programming Session : 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))

    # test step 19
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # test step 20
    testresult.append(["[.] '%s (%s)' auslesen: %s" % (diag_ident['name'], ident, str(HexList(diag_ident['identifier'][ident]))), ""])
    request = [0x31, 0x01] + diag_ident['identifier'][ident]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 20
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, [0x31], 0x31))

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
