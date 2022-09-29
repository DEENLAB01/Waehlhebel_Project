# ******************************************************************************
# -*- coding: latin1 -*-
# File    : DiagnoseSessions_Reset.py
# Title   : Diagnose Sessions Reset
# Task    : Test for an automatic reset from nondefault to default session
#
# Author  : S. Stenger
# Date    : 20.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 20.05.2021 | StengerS     | initial
# 1.1  | 23.06.2021 | StengerS     | added teststeps to trigger timeout again
# 1.2  | 27.10.2021 | Mohammed     | Rework
# 1.3  | 17.11.2021 | Mohammed     | Rework after Isyst Review
# 1.4  | 02.12.2021 | H. Förtsch   | reworked test script by test spec
# 1.5  | 19.01.2022 | Mohammed     | Added Aktion 3.9. Toleranz: 0.15s
# 1.6  | 27.01.2021 | Mohammed     | reworked test script after Adding preconditions
# 1.7  | 23.05.2022 | Mohammed     | Aktualisiert  Vorbedingungen
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import time
from data_common import s3_timeout
from diag_identifier import DIAG_SESSION_DICT
import functions_gearselection

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_124")

    # Initialize variables ####################################################

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    ############################
    # hil.Diagnose_01__period.setState("aus")
    # hil.NVEM_12__period.setState("aus")
    # hil.Dimmung_01__period.setState("aus")
    # hil.NM_Airbag__period.setState("aus")
    # hil.OBDC_Funktionaler_Req_All_FD__period.setState("aus")
    # hil.OBD_03__period.setState("aus")
    # hil.Systeminfo_01__period.setState("aus")
    # hil.NM_HCP1__period.setState("aus")
    # hil.ORU_01__period.setState("aus")
    # hil.OBDC_Waehlhebel_Req_FD__period.setState("aus")
    # hil.OTAMC_01__period.setState("aus")
    # hil.ISOx_Waehlhebel_Req_FD__period.setState("aus")
    # hil.DIA_SAAM_Req__period.setState("aus")
    # hil.ISOx_Funkt_Req_All_FD__period.setState("aus")
    # hil.DPM_01__period.setState("aus")

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

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    # silently go one chapter level up
    #testresult.append(["[-0]", ""])

    # 1. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    testresult.append(["[.] Überprüfen, dass erneuter Request nach Ablauf von S3 timeout "
                       "den Timer in der Extended Session neu startet", ""])

    # 2.1. Wechsel in die Extended Session: 0x1003
    testresult.append(["[+] Wechsel in Extended Session: 0x1003",""])
    test_data = DIAG_SESSION_DICT['extended']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # 2.2 Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # 2.3 Warten (< S3 timeout)
    timeout = s3_timeout - 1
    testresult.append(["[.] Warten (S3-Timeout - 1000ms: {}ms)".format(timeout * 1000), ""])
    time.sleep(timeout)

    # 2.4 Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # 2.5 Warten (< S3 timeout)
    timeout = s3_timeout - 1
    testresult.append(["[.] Warten (S3-Timeout - 1000ms: {}ms)".format(timeout * 1000), ""])
    time.sleep(timeout)

    # 2.6 Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186' ist", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # 2.7 Warten (= S3 timeout)
    timeout = s3_timeout
    testresult.append(["[.] Warten (S3-Timeout: {}ms)".format(timeout * 1000), ""])
    time.sleep(timeout)

    # 2.8 Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    testresult.append(["[-] Überprüfen, dass erneuter Request nach Ablauf von S3 timeout "
                       "den Timer in der Programming Session  neu startet", ""])

    # 3.1 Wechsel in die Extended Session: 0x1003
    testresult.append(["[+] Wechsel in Extended Session: 0x1003", ""])
    test_data = DIAG_SESSION_DICT['extended']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # 3.2 Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # 3.3 Wechsel in die Programming Session: 0x1002
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # 3.4 Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # 3.5 Warten (< S3 timeout)
    timeout = s3_timeout - 1
    testresult.append(["[.] Warten (S3-Timeout - 1000ms: {}ms)".format(timeout * 1000), ""])
    time.sleep(timeout)

    # 3.6 Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # 3.7 Warten (< S3 timeout)
    timeout = s3_timeout - 1
    testresult.append(["[.] Warten (S3-Timeout - 1000ms: {}ms)".format(timeout * 1000), ""])
    time.sleep(timeout)

    # 3.8 Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # 3.9 Warten (= S3 timeout)
    timeout = s3_timeout + .15
    testresult.append(["[.] Warten (S3-Timeout: {}ms)".format(timeout * 1000), ""])
    time.sleep(timeout)

    # 3.10 Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    del testenv
    # #########################################################################

print "Done."
