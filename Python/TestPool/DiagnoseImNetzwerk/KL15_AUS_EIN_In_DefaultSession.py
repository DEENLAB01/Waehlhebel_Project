# ******************************************************************************
# -*- coding: latin1 -*-
# File    : KL15_AUS_EIN_In_DefaultSession.py
# Title   : KL15 AUS EIN in  DefaultSession
# Task    : A minimal "KL15_AUS_EIN_In_DefaultSession!" test script
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
# 1.0  | 14.10.2021 | Mohammed  | initial
# 1.1  | 04.11.2021 | Devang    | Added correct evaluation method
# 1.2  | 17.12.2021 | Mohammed  | Rework according to Test specification
# 1.3  | 14.01.2022 | Mohammed  | Rework according to Test specification changed
# 1.4  | 17.03.2022 | Devangbhai  | Rework according to Test specification changed

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
    testresult.setTestcaseId("TestSpec_316")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    nm_Waehlhebel_Diag = hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value

    meas_vars = [nm_Waehlhebel_Diag]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+]Schalte KL30 und KL15 ein", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["\x0aSignal-Aufzeichnung von NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(["\xa0 Start DAQ Measurement", ""])
    daq.startMeasurement(meas_vars)

    #1
    testresult.append(["\x0a1. KL15 ausschalten und warte 150ms ", ""])
    hil.cl15_on__.set(0)
    time.sleep(0.150)

    # 2. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\x0a2. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # 3
    testresult.append(["\x0a3. Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", "INFO"])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )

    # 4. Wechsel in Default Session: 0x1001
    testresult.append(["\x0a 4.  Wechsel in Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # 5. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\x0a5. Auslesen der Active Diagnostic Session: 0x22F186", "INFO"])
    testresult.extend(canape_diag.checkDiagSession('default'))

    ## 6
    testresult.append(["\x0a6. Warte 2 Sekunden", ""])
    time.sleep(2.0)

    # 7
    testresult.append(["\x0a7. Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", "INFO"])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )

    ## 8
    testresult.append(["\x0a8. KL15 einschalten ", ""])
    hil.cl15_on__.set(1)

    ##9
    testresult.append(["\x0a9. Warte 12 Sekunden", ""])
    time.sleep(12)

    testresult.append(["\x0a10. Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", "INFO"])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    testresult.append(["\x0a12. Stoppe Measurement", ""])
    daq_data = daq.stopMeasurement()
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])

    plot_data = {}
    for mes in [nm_Waehlhebel_Diag]:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))

finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print "Done."
