# *****************************************************************************
# -*- coding: latin1 -*-
# File    : CAN_TX_Signal_KN_Waehlhebel_Waehlhebel_KompSchutz.py
# Title   : CAN TX Signal KN Waehlhebel Waehlhebel KompSchutz
# Task    : Test of ECU-Tx => HIL-Rx Signals of CAN Message KN_Waehlhebel_Waehlhebel_KompSchutz
#
# Author  : Mohammed Abdul Karim
# Date    : 08.02.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
#
# *****************************************************************************
# ********************************* Version ***********************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 08.02.2022 | Mohammed     | initial

# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv

from functions_diag import HexList
from diag_identifier import identifier_dict
from ttk_checks import basic_tests
from time import time as t
import time

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("CAN_59")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    KN_Waehlhebel_KompSchutz = hil.KN_Waehlhebel__Waehlhebel_KompSchutz__value

    meas_vars = [KN_Waehlhebel_KompSchutz]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: Kl15 und Kl30 an", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])
    testresult.append(["\xa0 Start DAQ Measurement", ""])
    daq.startMeasurement(meas_vars)

    # test step 1
    testresult.append(["[.] Auslesen und Prüfen des vom HiL empfangenen Signals (Toleranz: 0) für 30 sec", ""])
    timerlist = []
    sec = 30
    timeout = sec + t()
    while timeout > t():
        timerlist.append(KN_Waehlhebel_KompSchutz.get())

    len(timerlist),
    value = 0
    value_boolean = True
    for timer_values in timerlist:
        if value != timer_values:
            value_boolean = False
            break
    testresult.append(
        ["\xa0 Prüfe KN_Waehlhebel_KompSchutz hat %s Sekunde konstant %s gebleiben" % (sec, value),
         "PASSED"]) if value_boolean else testresult.append(
        ["\xa0 KN_Waehlhebel_KompSchutz nicht konstant gebleiben", "FAILED"])

    testresult.append(["[.] Prüfe KN_Waehlhebel:KN_Waehlhebel_KompSchutz = 0x0 gesendet", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=KN_Waehlhebel_KompSchutz,
            nominal_status=0,
            descr="Prüfe, dass Wert 0x0 ist",
        )
    )

    # test step 2
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["[.] Stoppe Measurement", ""])
    daq_data = daq.stopMeasurement()
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])
    plot_data = {}
    for mes in [KN_Waehlhebel_KompSchutz]:
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
