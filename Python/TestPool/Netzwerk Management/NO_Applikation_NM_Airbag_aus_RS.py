# ******************************************************************************
# -*- coding: latin1 -*-
# File    : NO_Applikation_NM_Airbag_aus_RS.py
# Title   : NO Applikation NM_Airbag aus RS
# Task    : A minimal "NO_Applikation_NM_Airbag_aus_RS!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name     | Description
# ------------------------------------------------------------------------------
# 1.0  | 27.07.2021 | Mohammed  | initial
# 1.1  | 16.11.2021 | Mohammed  | Added Waehlhebel_NM_aktiv_Tmin Signal
# ******************************************************************************

import time
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_nm
import functions_gearselection


# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_185")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    applikationsbotschaften = [hil.Waehlhebel_04__timestamp,
                               hil.DS_Waehlhebel__timestamp,
                               hil.KN_Waehlhebel__timestamp, ]

    nm_botschaften = [hil.NM_Waehlhebel__timestamp]
    messages_cycle_times = {str(hil.Waehlhebel_04__timestamp): 10,
                            str(hil.DS_Waehlhebel__timestamp): 1000,
                            str(hil.KN_Waehlhebel__timestamp): 500,
                            str(hil.NM_Waehlhebel__timestamp): 200,
                            }
    tolerance_percent = 0.10
    cycletime_tol_perc = 0.10
    ttimeout = 1.0
    ttimeout_tol_perc = 0.05
    nm_stop_s = 0.4
    t_send_after_wakeup = 0.15  # to be clarified

    meas_vars = [hil.cl15_on__, hil.Waehlhebel_04__timestamp,
                 hil.DS_Waehlhebel__timestamp, hil.KN_Waehlhebel__timestamp,
                 hil.NM_Waehlhebel__timestamp, hil.NM_HCP1__NM_HCP1_FCAB__value]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte KL30 und KL15 aus ", ""])
    hil.cl30_on__.set(0)
    hil.cl15_on__.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+0]", ""])

    testresult.append(["[.] Starte DAQ Messung für Applikations- und NM-Botschaften", ""])
    testresult.append(["Folgende Signale werden mitgemessen:\n%s" % meas_vars, ""])
    daq.startMeasurement(meas_vars)
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1)

    testresult.append(["[.] Schalte KL30 und KL30 ein", ""])
    hil.cl30_on__.set(1)
    hil.cl15_on__.set(1)
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1)

    testresult.append(["[.] Prüfe Signal NM_Waehlhebel:NM_Waehlhebel_NM_State", ""])
    descr, verdict = basic_tests.checkStatus(
        current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value,
        nominal_status=1,
        descr="Prüfe, dass Wert 1 (NM_RM_aus_BSM) gesetzt ist"
    )
    testresult.append([descr, verdict])

    testresult.append(["[.] Prüfe Signal NM_Waehlhebel_NM_aktiv_Tmin:Mindestaktivzeit", ""])
    descr, verdict = basic_tests.checkStatus(
        current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value,
        nominal_status=1,
        descr="Prüfe, dass Wert 1 (Mindestaktivzeit) gesetzt ist"
    )
    testresult.append([descr, verdict])

    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1)
    testresult.append(["[.] Schalte KL15 und Restbussimulation aus", ""])
    testresult.append(["Setze KL15 auf 0", "INFO"])
    hil.cl15_on__.set(0)
    testresult.append(["[.] Warte 2500ms", ""])
    time.sleep(2.5)

    testresult.append(["[.] Prüfe Signal NM_Waehlhebel:NM_Waehlhebel_NM_State", ""])
    descr, verdict = basic_tests.checkStatus(
        current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value,
        nominal_status=1,
        descr="Prüfe, dass Wert 1 (NM_RM_aus_BSM) gesetzt ist"
    )
    testresult.append([descr, verdict])

    testresult.append(["[.] Prüfe Signal NM_Waehlhebel_NM_aktiv_Tmin:Mindestaktivzeit", ""])
    descr, verdict = basic_tests.checkStatus(
        current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value,
        nominal_status=1,
        descr="Prüfe, dass Wert 1 (Mindestaktivzeit) gesetzt ist"
    )
    testresult.append([descr, verdict])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################
