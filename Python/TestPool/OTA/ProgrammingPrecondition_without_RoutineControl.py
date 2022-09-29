# *****************************************************************************
# -*- coding: latin-1 -*-
# File    : ProgrammingPrecondition_without_RoutineControl.py
# Title   : ProgrammingPrecondition_without_RoutineControl
# Task    : Test for Diagnosejob 0x22 0x0448 OTA
#
# Author  : Mohammed Abdul Karim
# Date    : 06.05.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 06.05.2022 | Mohammed   | initial
# 1.1  | 10.07.2022 | Mohammed     | Added right Precondition
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
from result_list import ResultList  # @UnresolvedImport (in test_support libs)

from functions_diag import HexList, ResponseDictionaries  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
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
    testresult.setTestcaseId("TestSpec_368")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_common = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    rd = ResponseDictionaries()

    # Initialize variables ####################################################
    test_data = identifier_dict['Programming_preconditions']
    _, all_resp = rd.Programming_preconditions()

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: KL30 an und KL15 aus", ""])
    #testenv.startupECU()
    hil.cl30_on__.set(1)
    hil.cl15_on__.set(0)
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])

    # test step 1
    testresult.append(["[.] Setze VehicleProtectedEnvironment_D auf 0 (VPE_none)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)

    # test step 2
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 3
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 4
    testresult.append(["[.] Setze ORU ,PropulsionSystemActive und VDS=_3d Signale", ""])
    testresult.append(["[+] Setze PropulsionSystemActive_switch = 0", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append(["[.] Setze VDSO_Vx3d auf (+/-5 km/h)", ""])
    testresult.append(func_gs.setVelocity_kmph(0))
    testresult.append(["[.] Setze VehicleProtectedEnvironment_D auf 0 (VPE_none)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze ORU_01.ORU_Status auf 4 (RUNNING", ""])
    hil.ORU_01__ORU_Status__value.set(4)
    testresult.append(["[.] Setze ORU_Control_A_01.OnlineRemoteUpdateControlA auf 4 (RUNNING", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_Control_D_01.OnlineRemoteUpdateControlD auf 4 (RUNNING", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    testresult.append(["[.] Warte 5100ms", ""])
    time.sleep(5.1)
    testresult.append(["[-0]", ""])

    # test step 5
    testresult.append(["[.] Auslessen der Programming Preconditions: 0x0448", ""])
    testresult.append(["[+] Diagnose Request schicken: 0x22 {} (Lese {})"
                      .format(HexList(test_data['identifier']), test_data['name']),
                       ""])
    request = [0x22] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 5.1
    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 5.2
    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))
    testresult.append(["[-0]", ""])

    # test step 6
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 7
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 8
    testresult.append(["[.] Setze OTAMC ,PropulsionSystemActive und VDS_3d Signale", ""])
    testresult.append(["[+] Setze VehicleProtectedEnvironment_D auf 0 (VPE_none)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze PropulsionSystemActive_switch = 0", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append(["[.] Setze VDSO_Vx3d auf (100 km/h)", ""])
    testresult.append(func_gs.setVelocity_kmph(100))
    testresult.append(["[.] Warte 5100ms", ""])
    time.sleep(5.1)
    testresult.append(["[-0]", ""])

    # test step 9
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)

    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 10
    testresult.append(["[.] Warte 5000ms", ""])
    time.sleep(5.0)

    # test step 11
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 12
    testresult.append(["[.] System wartet 1000 ms", ""])
    time.sleep(1.0)

    # test step 13
    testresult.append(["[.] Auslessen der Programming Preconditions: 0x0448", ""])
    testresult.append(["[+] Diagnose Request schicken: 0x22 {} (Lese {})"
                      .format(HexList(test_data['identifier']), test_data['name']),
                       ""])
    request = [0x22] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 13.1
    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 13.2
    testresult.append(["[.] Warte 5000ms", ""])
    time.sleep(5.0)
    testresult.append(["[-0]", ""])

    # test step 14
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 15
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 16
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 17
    testresult.append(["[.] Setze VehicleProtectedEnvironment_D auf 0 (VPE_none)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)

    # test step 18
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 19
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 20
    testresult.append(["[.] Setze PropulsionSystemActive_switch = 0", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append(["[.] Setze VDSO_Vx3d auf (100 km/h)", ""])
    testresult.append(func_gs.setVelocity_kmph(100))

    # test step 21
    testresult.append(["[.] Warte 5100ms", ""])
    time.sleep(5.1)

    # test step 23
    testresult.append(["[.] Prüfe die erhaltenen Programming Preconditions beim Kundendienst", ""])
    response_content = response[3:]

    preconditions_count = response_content[0]
    preconditions_list = response_content[1:]

    # test step 23.1
    testresult.append(["[+] Vergleiche erste Byte mit Responselänge", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=preconditions_count,
            nominal_status=len(preconditions_list),
            descr="Prüfe, dass erstes Byte (0x{:02X}) und Anzahl an Preconditions übereinstimmt"
                .format(preconditions_count)))

    # test step 23.2
    testresult.append(['[.] Prüfe aufgelistete Preconditions', ''])
    subresult = ResultList()
    exp_list = test_data['expected_response']
    for precond in preconditions_list:
        precond_name = all_resp.get(precond, "Unbekannte Precondition")
        if precond in exp_list:
            subresult.append(["Expected precondition found in response: 0x{:02X} ({})"
                             .format(precond, precond_name, ),
                              "PASSED"])
            exp_list.remove(precond)
        else:
            subresult.append(["Precondition is not expected: 0x{:02X} ({})"
                             .format(precond, precond_name),
                              "FAILED"])

    # if exp_list:
    #     for precond in exp_list:
    #         precond_name = all_resp.get(precond, "Unbekannte Precondition")
    #         subresult.append(["Expected Precondition not found in Response: 0x{:02X} ({})"
    #                          .format(precond, precond_name),
    #                           "FAILED"])

    testresult.enableEcho(False)
    testresult.append(subresult.getCombinedResult())
    testresult.enableEcho(True)

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
