# ******************************************************************************
# -*- coding: latin1 -*-
# File    : KL15_EIN_In_DefaultSession.py
# Title   : KL15 EIN In DefaultSession
# Task    : A minimal "KL15_EIN_In_DefaultSession!" test script
#
# Author  : Mohammed Abdul Karim
# Date    : 14.10.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 14.10.2021 | Mohammed  | initia
# 1.1  | 04.11.2021 | Devang    | Added correct evaluation method
# 1.2  | 17.12.2021 | Devang    | Rework according to Test specification
# 1.3  | 14.01.2022 | Mohammed  | Rework according to Test specification changed

# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import time
from ttk_daq import eval_signal

# Instantiate test environment
testenv = TestEnv()
hil = testenv.getHil()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_311")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    nm_Waehlhebel_Diag = hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value

    meas_vars = [nm_Waehlhebel_Diag]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte KL30 und KL15 ein", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # 1. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\x0a1. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # 2
    testresult.append(["\x0a2. Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )
    ## 3
    testresult.append(["\x0a3. Signal-Aufzeichnung von NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(["\xa0 Start DAQ Measurement", ""])
    daq.startMeasurement(meas_vars)

    ## 4
    testresult.append(["\x0a4. Warte 5 Sekunde", ""])
    time.sleep(5)

    # 5. Wechsel in Extended Session: 0x1003
    testresult.append(["\x0a5. Erneut Default Session anfordern: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # 6. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\x0a6. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    #7
    testresult.append(["\x0a7. Warte 7s", ""])
    time.sleep(7)

    #8
    testresult.append([" \x0a8. Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )


    # 9
    testresult.append(["\x0a9. Warte 4s", ""])
    time.sleep(4)

    # 10
    testresult.append(["\x0a10. Stoppe DAQ Measurement", ""])
    daq_data = daq.stopMeasurement()
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])

    # 11
    testresult.append([" \x0a11. Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    plot_data = {}
    for mes in [nm_Waehlhebel_Diag]:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))

    NM_Waehlhebel_NM_aktiv_Diag_eval = daq_data[str(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value)]
    NM_Waehlhebel_NM_aktiv_Diag = eval_signal.EvalSignal(NM_Waehlhebel_NM_aktiv_Diag_eval)
    NM_Waehlhebel_NM_aktiv_Diag.clearAll()
    time_zero = NM_Waehlhebel_NM_aktiv_Diag.getTime()
    NM_aktiv_Diag_ein_time = NM_Waehlhebel_NM_aktiv_Diag.find(operator="==", value=1)
    NM_aktiv_Diag_aus_time = NM_Waehlhebel_NM_aktiv_Diag.findNext(operator="==", value=0)

    if NM_aktiv_Diag_aus_time is not None:
        testresult.append(["NM_aktiv_Diag aus Zeitpunkt: %ss" % (NM_aktiv_Diag_aus_time - time_zero), "Info"])
        testresult.append(["\x0a12 Prüfe, dass NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag wechselt genau einmal von 1 auf 0, genau 10 s nach letztem Request oder Response ist"])
        testresult.append(["Der Wert von NM_Waehlhebel_NM_aktiv_Diag wird bei %ss auf 0 gesetzt" % (NM_aktiv_Diag_aus_time - time_zero), "PASSED"])
    else:
        testresult.append(["NM_aktiv_Diag aus Zeitpunkt nicht erkannt", "INFO"])
        testresult.append( ["\x0a12 Prüfe, dass NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag im gemessenen Zeitraum konstant 1 ist"])
        testresult.append(["NM_Waehlhebel_NM_aktiv_Diag == 1 während des Messzeitraumes", "FAILED"])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print "Done."
