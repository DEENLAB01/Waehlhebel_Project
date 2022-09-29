# ******************************************************************************
# -*- coding: latin1 -*-
# File    : kein_Gangwechsel_ohne_mechan_Betaetigung.py
# Title   : Kein Gangwechsel ohne mechan Betaetigung
# Task    : Kein Gangwechsel ohne mechan Betaetigung
#
# Author  : Mohammed Abdul Karim
# Date    : 30.07.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name     | Description
# ------------------------------------------------------------------------------
# 1.0  | 30.07.2021 | Mohammed | initial
# ******************************************************************************
# Imports #####################################################################
import time
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_11")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    wh_sensorRoh = hil.Waehlhebel_04__WH_SensorPos_roh__value

    meas_vars = [wh_fahrstufe, wh_sensorRoh]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 und KL15 an)", ""])
    testenv.startupECU()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["\xa0Start DAQ Measurement für WH_Fahrstufe und WH_SensorPos_roh ", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["[.] Warte 100ms", ""])
    time.sleep(0.100)

    testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=wh_fahrstufe,
            nominal_status=4,
            descr="Prüfe, dass WH_Fahrstufe = 4 ist"
        )
    )

    testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=wh_sensorRoh,
            nominal_status=4,
            descr="Prüfe, dass wh_sensorRoh = 4 ist"
        )
    )

    testresult.append(["[.] Warte 10s", ""])
    time.sleep(10)

    testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=wh_fahrstufe,
            nominal_status=4,
            descr="Prüfe, dass WH_Fahrstufe = 4 ist"
        )
    )

    testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=wh_sensorRoh,
            nominal_status=4,
            descr="Prüfe, dass wh_sensorRoh = 4 ist"
        )
    )

    testresult.append(["[.] Warte 2 Sekunde, bevor DAQ Messung beendet wird", ""])
    time.sleep(2)
    testresult.append(["Stopp DAQ Measurement", "INFO"])
    daq_data = daq.stopMeasurement()
    time.sleep(0.5)
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])

    # erzeuge Plot für Testreport (ohne KL15)
    plot_data = {}
    for mes in [wh_fahrstufe, wh_sensorRoh]:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(
        daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    ## Cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################
