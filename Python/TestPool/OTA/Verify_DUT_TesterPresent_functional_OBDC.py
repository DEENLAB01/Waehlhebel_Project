# ******************************************************************************
# -*- coding: latin-1 -*-
# File     : Verify_DUT_TesterPresent_functional_OBDC.py
# Title    : Verify_DUT_TesterPresent_functional_OBDC.py
# Task     : Verify DUT Tester Present in functional OBDC Identifier
#
# Author  : Mohammed Abdul Karim
# Date    : 02.05.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 02.05.2022 | Mohammed  | initial
# 1.1  | 05.05.2022 | Mohammed  | Reworked
# 1.2  | 06.05.2022 | Mohammed  | Added Testschritte
# ******************************************************************************


from _automation_wrapper_ import TestEnv  # @UnresolvedImport
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_gearselection
import simplified_bus_tests
from ttk_checks import basic_tests
import time

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################

    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()

    # Initialize variables ####################################################
    diag_ident = identifier_dict['Tester Present']
    cycle_time_ms = 2000
    tolerance_percent = 0.10

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_363")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[.] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    # test step 1
    testresult.append(["[.] Prüfe  RequestID = OBDC gesendet", ""])
    try:
        canape_xcp = testenv.getAsap3()
        testresult.append(["\xa0 Prüfe RequestID == OBDC ", "PASSED"])
    except:
        testresult.append(["\x0a RequestID != OBDC", "FAILED"])

    # Test step 2
    testresult.append(["[.] Diagnose Request TesterPresent physical (0x3E00) via OBDC Identifier ", ""])
    request_programming = [0x3E, 0x00]
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf Positive Response überprüfen: 0x7E00", ""])
    testresult.append(canape_diag.checkResponse(response, [0x7E, 0x00]))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.shutdownECU()
    testenv.breakdown()
    # #########################################################################