# *****************************************************************************
# -*- coding: latin1 -*-
# File    : CAN_TX_Signal_KN_Waehlhebel_NM_Waehlhebel_FCIB.py
# Title   : CAN TX Signal KN Waehlhebel NM_Waehlhebel_FCIB
# Task    : Test of ECU-Tx => HIL-Rx Signals of CAN Message KN_Waehlhebel_NM_Waehlhebel_FCIB
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
import functions_nm
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
    testresult.setTestcaseId("CAN_72")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    NM_Waehlhebel_FCIB = hil.KN_Waehlhebel__NM_Waehlhebel_FCIB__value
    meas_vars = [NM_Waehlhebel_FCIB]

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
        timerlist.append(NM_Waehlhebel_FCIB.get())

    len(timerlist),
    value = 1099511629825
    value_boolean = True
    for timer_values in timerlist:
        if value != timer_values:
            value_boolean = False
            break
    testresult.append(
        ["\xa0 Prüfe KN_Waehlhebel_NM_Waehlhebel_FCIB hat %s Sekunde konstant %s gebleiben" % (sec, value),
         "PASSED"]) if value_boolean else testresult.append(
        ["\xa0 KN_Waehlhebel_NM_Waehlhebel_FCIB nicht konstant gebleiben", "FAILED"])

    testresult.append(["[.] Prüfe KN_Waehlhebel: NM_Waehlhebel_FCIB = 01_CarWakeUp, 12_GearSelector und 41_DiagnosisPowertrain gesendet", ""])
    testresult += [
        func_nm.checkFcabBitwise(NM_Waehlhebel_FCIB.get(), [1], [], descr="NM_Waehlhebel_FCIB:01_CarWakeUp"),
        func_nm.checkFcabBitwise(NM_Waehlhebel_FCIB.get(), [12], [], descr="NM_Waehlhebel_FCIB:12_GearSelector"),
        func_nm.checkFcabBitwise(NM_Waehlhebel_FCIB.get(), [41], [], descr="NM_Waehlhebel_FCIB:41_DiagnosisPowertrain")
    ]

    # test step 2
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["[.] Stoppe Measurement", ""])
    daq_data = daq.stopMeasurement()
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])

    plot_data = {}
    for mes in [NM_Waehlhebel_FCIB]:
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
