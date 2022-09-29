# ******************************************************************************
# -*- coding: latin1 -*-
# File    : kein_ECU_KnockOut_KL15_EIN.py
# Title   : kein_ECU_KnockOut_KL15_EIN
# Task    : Test für Kein ECU KnockOut mit KL15 EIN
#
# Author  : Mohammed Abdul Karim
# Date    : 22.11.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 22.11.2021 | Mohammed   | initial
# 1.2  | 17.12.2021 | Devangbhai   | Rework according to new specification
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList
from diag_identifier import identifier_dict
import functions_common
from ttk_checks import basic_tests
import functions_gearselection
import time
import functions_nm
from time import time as t
import os

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_com = functions_common.FunctionsCommon(testenv)

    # Initialize variables ####################################################
    diag_ident_KN_CTR = identifier_dict['Knockout_counter']
    diag_ident_KN_TMR = identifier_dict['Knockout_timer']
    test_variable = hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value
    func_nm = functions_nm.FunctionsNM(testenv)

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_203")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[.] Wechsle in die Extended Session", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    testresult.append(["[.] BusKnockOut_Tmr und ECUKnockOut_Tmr auf 15 setzen"])
    request = [0x2E] + diag_ident_KN_TMR['identifier'] + [0x0F, 0x0F]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] BusKnockOut_Ctr und ECUKnockOut_Ctr auf 0 setzen"])
    request = [0x2E] + diag_ident_KN_CTR['identifier'] + [0x00, 0x00]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["Überprüfen, dass Request positiv beantwortet wird", "INFO"])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.]  ECU ausschalten", ""])
    testenv.canape_Diagnostic = None
    testenv.asap3 = None
    testenv.canape_Diagnostic = None
    del (canape_diag)
    testenv.shutdownECU()

    testresult.append(["[.]  Warte 10sekund", ""])
    time.sleep(10)

    testresult.append(["[.] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()

    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    ###
    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # test step 1
    testresult.append(["\x0a  1. Prüfe Diagnoseparameter ECUKnockOut_Ctr (22 02 CA) und speichere Wert in ecuctr_start (Variable) für späteren Vergleich"])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    ECUKnockOut_Ctr_start = None
    if response[0:3] == [98, 2, 202]:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))
        ECUKnockOut_Ctr_start = response[3]
        if ECUKnockOut_Ctr_start is not None:
            ECUKnockOut_Ctr_start = ECUKnockOut_Ctr_start
            testresult.append(["\xa0 Gespeichere Wert für ecuctr_start (Variable) für späteren Vergleich ist %s" % ECUKnockOut_Ctr_start])
        else:
            ECUKnockOut_Ctr_start = 0
            testresult.append(["\xa0 Gespeichere Wert für ecuctr_start (Variable) für späteren Vergleich ist %s" % ECUKnockOut_Ctr_start])
    else:
        testresult.append(["Auf positive Response überprüfen", ""])
        testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 2
    testresult.append(["\xa0 2. Lese Signal KN_Waehlhebel_ECUKnockOutTimer "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 15, descr="KN_Waehlhebel_ECUKnockOutTimer = 15 (Ausgangswert)")]

    # test step 3
    testresult.append(["\x0a3. Warte 1,5min"])
    time.sleep(90)

    # test step 4
    testresult.append(["\xa0 4. Lese Signal KN_Waehlhebel_ECUKnockOutTimer "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 15, descr="KN_Waehlhebel_ECUKnockOutTimer = 15 (Timer läuft nicht)"),]

    # test step 5
    testresult.append(["\x0a5. Warte 1,5min "])
    time.sleep(90)

    # test step 6
    testresult.append(["\xa06. Lese Signal KN_Waehlhebel_ECUKnockOutTimer "])
    testresult += [basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 15, descr="KN_Waehlhebel_ECUKnockOutTimer = 15 (Timer läuft nicht)"),]

    # test step 7
    testresult.append(["\x0a7. Warte 12,5min "])
    time.sleep(12.5*60)

    # test step 8
    testresult.append(["\xa08. Lese Signal KN_Waehlhebel_ECUKnockOutTimer "])
    testresult += [ basic_tests.checkStatus(hil.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value, 15, descr="KN_Waehlhebel_ECUKnockOutTimer = 15 (Timer läuft nicht)"),]

    # test step 9
    testresult.append(["\x0a 9.Prüfe Diagnoseparameter ECUKnockOut_Ctr (22 02 CA)", ""])
    request = [0x22] + diag_ident_KN_CTR['identifier']
    response_diag, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkPositiveResponse(response_diag, request))
    ECUKnockOut_Ctr_end = None

    if response_diag[0:3] == [98, 2, 202]:
        ECUKnockOut_Ctr_end = response_diag[3]
        if ECUKnockOut_Ctr_end is not None:
            ECUKnockOut_Ctr_end = ECUKnockOut_Ctr_end
        else:
            ECUKnockOut_Ctr_end = 0
    else:
        testresult.append(
            ["\xa0 Kein Positive response erhalten.  ECUKnockOut_Ctr kann nicht auslasen", "FAILED"])

    # if ECUKnockOut_Ctr_start and ECUKnockOut_Ctr_end is not None:
    testresult.append(basic_tests.checkStatus(current_status=ECUKnockOut_Ctr_end,nominal_status=ECUKnockOut_Ctr_start,descr="Prüfe, dass ECUKnockOut_Ctr = ecuctr_start", ))

    # else:
    #     testresult.append(["\xa0 ECUKnockOut_Ctr kann nicht auslasen. ECUKnockOut_Ctr kann nicht mit ecuctr_start vergleichen", "FAILED"])

    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()
    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)