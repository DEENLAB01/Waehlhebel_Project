# ******************************************************************************
# -*- coding: latin1 -*-
# File    : TimeBetweenClamp15offTo30off.py
# Title   : TimeBetweenClamp15offTo30off
# Task    : Test for an automatic reset from nondefault to default session
#
# Author  : S. Stenger
# Date    : 20.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 20.05.2021 | StengerS   | initial
# 1.1  | 23.06.2021 | StengerS   | added teststeps to trigger timeout again
# 1.2  | 27.10.2021 | Mohammed   | Rework
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import time
from data_common import s3_timeout

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_xxxx")

    # Initialize variables ####################################################
    request_dict = {
        1: {
            'identifier': [0xF1, 0x87, 0xF1,0x87],
            'name': 'TimeBetweenClamp15offTo30off',
            'expected_response': [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4],
            'exp_data_length': 3},
        2: {
            'identifier': [0x10, 0x02],
            'name': 'programming',
            'expected_response': [0x50, 0x02, 0x00, 0x32, 0x01, 0xF4],
            'exp_data_length': 3,  # Bytes
        },
        3: {
            'identifier': [0x10, 0x03],
            'name': 'extended',
            'expected_response': [0x50, 0x03, 0x00, 0x32, 0x01, 0xF4],
            'exp_data_length': 3
        },
    }

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # 1. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa01. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))


    testresult.append(["\x0a2. Überprüfen, dass erneuter Request nach Ablauf von S3 timeout den Timer in der Extended Session neu startet", ""])
    # 2.1. Wechsel in die Extended Session: 0x1003
    testresult.append(["\x0a2.1 Wechsel in Extended Session: 0x1003",""])
    for test in request_dict:
        test_data = request_dict[test]
        if test_data['name'] == 'extended':
            request = test_data['identifier']
            [response, result] = canape_diag.sendDiagRequest(request)
            testresult.append(result)
            testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
            testresult.append(canape_diag.checkPositiveResponse(response, request, job_length=2))

    # 2.2 Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\xa02.2 Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # 2.3 Warten (< S3 timeout)
    testresult.append(["\xa02.3 Warten (S3-Timeout - 1000ms: 4000ms)", ""])
    time.sleep(4)



    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print "Done."
