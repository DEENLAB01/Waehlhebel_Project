# *****************************************************************************
# -*- coding: latin1 -*-
# File    : CAN_TX_Signal_NM_Waehlhebel_NM_Waehlhebel_UDS_CC.py
# Title   : CAN TX Signal NM_Waehlhebel_NM_Waehlhebel_UDS_CC
# Task    : Test of ECU-Tx => HIL-Rx Signals of CAN Message NM_Waehlhebel_NM_Waehlhebel_UDS_CC
#
# Author  : Mohammed Abdul Karim
# Date    : 01.02.2022
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
#
# *****************************************************************************
# ********************************* Version ***********************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 01.02.2022 | Mohammed     | initial

# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv

from functions_diag import HexList
from diag_identifier import identifier_dict
from ttk_checks import basic_tests
import time
from time import time as t
# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("CAN_84")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    nm_Waehlhebel_UDS_CC = hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value
    meas_vars = [nm_Waehlhebel_UDS_CC]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: Kl15 und Kl30", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])
    daq.startMeasurement(meas_vars)

    # test step 1
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 2, 3
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 4
    testresult.append(["[.] Diagnoseservice Communication Control schicken : 0x280101", ""])
    request = [0x28] + [0x01, 0x01]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkResponse(response, [0x68, 0x01]))

    # test step 4.1
    testresult.append(["[.] Warte 100ms", ""])
    time.sleep(.100)

    # test step 4.2
    testresult.append(["\xa0 Auslesen und Prüfen des vom HiL empfangenen Signals (Toleranz: 0).", ""])
    timerlist = []
    sec = 0.0
    timeout = sec + t()
    while timeout > t():
        timerlist.append(nm_Waehlhebel_UDS_CC.get())

    len(timerlist),
    value = 1
    value_boolean = True
    for timer_values in timerlist:
        if value != timer_values:
            value_boolean = False
            break
    testresult.append(
        ["\xa0 Prüfe Waehlhebel_UDS_CC hat %s Sekunde HiL %s empfangenen" % (sec, value),
         "PASSED"]) if value_boolean else testresult.append(
        ["\xa0 Waehlhebel_UDS_CC nicht HiL empfangenen", "FAILED"])

    testresult.append(["[.] Prüfe NM_Waehlhebel:NM_Waehlhebel_UDS_CC = 1", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=nm_Waehlhebel_UDS_CC,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )

    # test step 5
    testresult.append(["[.] Diagnoseservice Communication Control schicken: 0x280001", ""])
    request = [0x28] + [0x00, 0x01]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkResponse(response, [0x68, 0x00]))

    # test step 5.1
    testresult.append(["[.] Warte 100ms", ""])
    time.sleep(.100)

    # test step 5.2
    testresult.append(["\xa0 Auslesen und Prüfen des vom HiL empfangenen Signals (Toleranz: 0).", ""])
    timerlist = []
    sec = 0.100
    timeout = sec + t()
    while timeout > t():
        timerlist.append(nm_Waehlhebel_UDS_CC.get())

    len(timerlist),
    value = 0
    value_boolean = True
    for timer_values in timerlist:
        if value != timer_values:
            value_boolean = False
            break
    testresult.append(
        ["\xa0 Prüfe Waehlhebel_UDS_CC hat %s Sekunde HiL %s empfangenen" % (sec, value),
         "PASSED"]) if value_boolean else testresult.append(
        ["\xa0 Waehlhebel_UDS_CC nicht HiL empfangenen", "FAILED"])

    testresult.append(["[.] Prüfe NM_Waehlhebel:NM_Waehlhebel_UDS_CC = 0", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=nm_Waehlhebel_UDS_CC,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    # test step 6
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["[.] Stoppe Measurement", ""])
    daq_data = daq.stopMeasurement()
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])
    plot_data = {}
    for mes in [nm_Waehlhebel_UDS_CC]:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))
    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print ("Done.")
