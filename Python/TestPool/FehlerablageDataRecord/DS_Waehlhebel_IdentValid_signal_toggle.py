# *****************************************************************************
# -*- coding: latin1 -*-
# File    : DS_Waehlhebel_IdentValid_signal_toggle.py
# Title   : DS_Waehlhebel_IdentValid_signal_toggle
# Task    : change identification data [VW FAZIT Identification String] and check DS_Waehlhebel IdentValid signal
#
# Author  : Mohammed Abdul Karim
# Date    : 01.04.2022
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 17.02.2022 | M.A.Mushtaq  | initial
# 1.1  | 05.05.2022 | Mohammed     | initial
# 1.2  | 27.06.2022 | Mohammed     | Reworked
# 1.3  | 28.06.2022 | Mohammed     | TestSpec Aktualisiert

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
from ttk_daq import eval_signal
import time
# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_386")
    bus = testenv.getCanBus()
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    test_data = identifier_dict['VW FAZIT Identification String']
    sig1 = bus.DS_Waehlhebel__DS_Waehlhebel_IdentValid__value
    meas_vars = [sig1]
    ticket_id = 'EGA-PRM-204'
    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.enableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\nStarte Testprozess: %s"%testenv.script_name.split('.py')[0], ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Start DAQ Measurement für DS_Waehlhebel__DS signals Analyse", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    # test step 2.-2.3
    testresult.append(["[.] '%s' auslesen: %s" %(test_data['name'], HexList(test_data['identifier'])), ""])
    request = [0x22] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    fazit_identification_orig = response[3:]

    testresult.append(["[+] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    testresult.append(["[.] Inhalt auf Korrektheit überprüfen", ""])
    testresult.append(canape_diag.checkResponse(fazit_identification_orig, test_data['expected_response']))
    testresult.append(["[-0]", ""])

    # test step 3-3.1
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    testresult.append(["[+] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))
    testresult.append(["[-0]", ""])

    # test step 4-4.3
    testresult.append(["[.] Security Access aktivieren", ""])

    testresult.append(["[+] Seed anfragen: 0x2761", ""])
    seed, result = canape_diag.requestSeed()
    testresult.extend(result)

    testresult.append(["[.] Key berechnen: <key 1>", ""])
    key, result = canape_diag.calculateKey(seed)
    testresult.extend(result)

    testresult.append(["[.] Key senden: 0x2762 + <key 1>", ""])
    verdict = canape_diag.sendKey(key)
    testresult.extend(verdict)
    testresult.append(["[-0]", ""])

    # test step 5-5.7
    fazit_identification = [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    request = [0x2E, 0xF1, 0x7C]
    testresult.append(["[.] Schreibe VW FAZIT Identification String: 0x{} + 0x{}"
                       .format("".join("{:02X}".format(x) for x in request),
                               "".join("{:02X}".format(x) for x in fazit_identification)),
                       ""])
    response, result = canape_diag.sendDiagRequest(request + fazit_identification)

    testresult.append(["[+] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    testresult.append(["[.] Sleep for 80ms + 10ms tol", ""])
    time.sleep(.09)

    # test step 8
    # testresult.append(["[.] Prüfe Inhalt: 0x{}"
    #                    .format(" ".join("{:02X}".format(x) for x in fazit_identification)),
    #                    ""])
    # request = [0x2E, 0xF1, 0x7C]
    # response, result = canape_diag.sendDiagRequest(request)
    # testresult.append(result)
    # testresult.append(canape_diag.checkResponse(response[3:], fazit_identification))
    testresult.append(["[.] Prüfe Inhalt: 0x{}"
                       .format(" ".join("{:02X}".format(x) for x in fazit_identification)),
                       ""])
    request = [0x22, 0xF1, 0x7C]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response[3:], fazit_identification))

    testresult.append(["[.] KL30 aus und Warte etwa 2 sec", ""])
    hil.cl30_on__.set(0)
    time.sleep(2)

    testresult.append(["[.] KL30 an und Warte Zykluszeit", ""])
    hil.cl30_on__.set(1)
    time.sleep(0.100)

    testresult.append(["[.] Clear CANape", ""])
    testenv.canape_Diagnostic = None
    testenv.asap3 = None
    testenv.canape_Diagnostic = None
    del (canape_diag)
    time.sleep(10)

    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()
    testresult.append(["[-0]", ""])

    testresult.append(["[.] Wechsel in default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    testresult.append(["[+] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))
    testresult.append(["[-0]", ""])

    # test step 6-6.1
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    # test step 7
    testresult.append(["[+] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))
    testresult.append(["[-0]", ""])

    # test step 8.-8.3
    testresult.append(["[.] Security Access aktivieren", ""])

    testresult.append(["[+] Seed anfragen: 0x2761", ""])
    seed, result = canape_diag.requestSeed()
    testresult.extend(result)

    testresult.append(["[.] Key berechnen: <key 1>", ""])
    key, result = canape_diag.calculateKey(seed)
    testresult.extend(result)

    testresult.append(["[.] Key senden: 0x2762 + <key 1>", ""])
    verdict = canape_diag.sendKey(key)
    testresult.extend(verdict)
    testresult.append(["[-0]", ""])

    # test step 9.-9.2
    request = [0x2E, 0xF1, 0x7C]
    testresult.append(["[.] Schreibe originale VW FAZIT Identification String: 0x{} + 0x{}"
                      .format(" ".join("{:02X}".format(x) for x in request),
                              " ".join("{:02X}".format(x) for x in fazit_identification_orig)),
                       ""])
    response, result = canape_diag.sendDiagRequest(request + fazit_identification_orig)

    testresult.append(["[+] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Inhalt auf Korrektheit überprüfen", ""])
    testresult.append(canape_diag.checkResponse(fazit_identification_orig, test_data['expected_response']))

    testresult.append(["[.] Sleep for 80ms + 10ms tol", ""])
    time.sleep(.09)
    testresult.append(["[-0]", ""])

    # test step 10.-10.1
    testresult.append(["[.] Stopp DAQ Measurement", ""])
    daq_data = daq.stopMeasurement()
    time.sleep(0.5)

    time_1 = []
    for i in range(len(meas_vars)):
        sig_status_data = daq_data[str(meas_vars[i])]
        analyse_sig1_data = eval_signal.EvalSignal(sig_status_data)
        analyse_sig1_data.clearAll()
        for i in range(2):
           time_1 = analyse_sig1_data.findChanged(forward=True, threshold=0.5)

    if time_1:
        testresult.append([" %s::\nValue Toggle from 1-->0-->1 " % (meas_vars[0].alias), "PASSED"])

    else:
        testresult.append([" %s::\nValue did not Toggle from 1-->0-->1 " % (meas_vars[0].alias),"[[COMMENT]] %s" % ticket_id, "FAILED"])
    #     only for debugging
    testresult.append(["[+] Analysiere DS_Waehlhebel_IdentValid signal", ""])
    plot_data = {}
    for mes in meas_vars:
        plot_data[str(mes)] = daq_data[str(mes)]
    #
    #     testresult.append(
    #         daq.plotMultiShot(plot_data, "test_signal_multi"))
    testresult.append(
        daq.plotSingleShot(daq_data=plot_data[str(mes)],
                           filename="lokalaktiv_signal_toggle",
                           label_signal="lokalaktiv"))
    testresult.append(["[-0]", ""])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    del testenv
    # #########################################################################

print "Done."
