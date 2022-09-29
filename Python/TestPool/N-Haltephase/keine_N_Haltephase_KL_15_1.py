# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : keine_N_Haltephase_KL_15_1.py
# Title   : keine N Haltephase KL_15=1
# Task    : N Haltephase wird nicht gestartet (KL_15 = 0)
#
# Author  : Mohammed Abdul Karim
# Date    : 13.07.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 18.05.2021 | Mohammed         | initial
# 1.1  | 15.09.2021 | Devangbhai Patel | Rework
# 1.2  | 02.02.2022 | Mohammed         | corrected NM_Waehlhebel_NM_aktiv_Tmin signal value
# 1.3  | 04.02.2022 | Mohammed         | Added Fehler ID
# 1.4  | 27.07.2022 | Mohammed         | Rework
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_daq import eval_signal
from ttk_checks import basic_tests
import functions_gearselection
import functions_nm
from functions_nm import _checkStatus, _checkRange
import time
from time import time as t

# Instantiate test environment
testenv = TestEnv()


def check_cycletime(sec, application_msg=True, nm_msg=True):
    Waehlhebel_04__timestamp_list = []
    DS_Waehlhebel__timestamp_list = []
    KN_Waehlhebel__timestamp_list = []
    NM_Waehlhebel__timestamp_list = []

    timeout = sec + t()

    while timeout > t():
        timestamp_Waehlhebel_04 = hil.Waehlhebel_04__timestamp.get()
        timestamp_DS_Waehlhebel = hil.DS_Waehlhebel__timestamp.get()
        timestamp_KN_Waehlhebel = hil.KN_Waehlhebel__timestamp.get()
        timestamp_NM_Waehlhebel = hil.NM_Waehlhebel__timestamp.get()

        if len(Waehlhebel_04__timestamp_list) == 0 or Waehlhebel_04__timestamp_list[-1] != timestamp_Waehlhebel_04:
            Waehlhebel_04__timestamp_list.append(timestamp_Waehlhebel_04)

        elif len(DS_Waehlhebel__timestamp_list) == 0 or DS_Waehlhebel__timestamp_list[-1] != timestamp_DS_Waehlhebel:
            DS_Waehlhebel__timestamp_list.append(timestamp_DS_Waehlhebel)

        elif len(KN_Waehlhebel__timestamp_list) == 0 or KN_Waehlhebel__timestamp_list[-1] != timestamp_KN_Waehlhebel:
            KN_Waehlhebel__timestamp_list.append(timestamp_KN_Waehlhebel)

        elif len(NM_Waehlhebel__timestamp_list) == 0 or NM_Waehlhebel__timestamp_list[-1] != timestamp_NM_Waehlhebel:
            NM_Waehlhebel__timestamp_list.append(timestamp_NM_Waehlhebel)

    new_sec = sec * 1000
    Waehlhebel_04__timestamp = 10
    DS_Waehlhebel__timestamp = 1000
    KN_Waehlhebel__timestamp = 500
    NM_Waehlhebel_timestamp = 200

    testresult.append(basic_tests.checkRange((len(Waehlhebel_04__timestamp_list)) if application_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / Waehlhebel_04__timestamp) - 5) if application_msg else 0, ((new_sec / Waehlhebel_04__timestamp) + 5) if application_msg else 0, "Prüfen, ob die Applikation Botschaft Waehlhebel_04 mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (Waehlhebel_04__timestamp, sec)))
    testresult.append(basic_tests.checkRange((len(DS_Waehlhebel__timestamp_list)) if application_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / DS_Waehlhebel__timestamp) - 2) if application_msg else 0, ((new_sec / DS_Waehlhebel__timestamp) + 2) if application_msg else 0, "Prüfen, ob die Applikation Botschaft DS_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % ( DS_Waehlhebel__timestamp, sec)))
    testresult.append(basic_tests.checkRange((len(KN_Waehlhebel__timestamp_list)) if application_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / KN_Waehlhebel__timestamp) - 2) if application_msg else 0,((new_sec / KN_Waehlhebel__timestamp) + 2) if application_msg else 0, "Prüfen, ob die Applikation Botschaft KN_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % ( KN_Waehlhebel__timestamp, sec)))
    testresult.append(basic_tests.checkRange((len(NM_Waehlhebel__timestamp_list)) if nm_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / NM_Waehlhebel_timestamp) - 2) if nm_msg else 0, ((new_sec / NM_Waehlhebel_timestamp) + 2) if nm_msg else 0, "Prüfen, ob die Applikation Botschaft NM_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (NM_Waehlhebel_timestamp, sec)))


try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    test_variable = hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value
    test_variable.alias = "Waehlhebel_04:WH_Zustand_N_Haltephase_2"

    ############################################################################
    applikationsbotschaften = [hil.Waehlhebel_04__timestamp,
                               hil.DS_Waehlhebel__timestamp,
                               hil.KN_Waehlhebel__timestamp, ]

    nm_botschaften = [hil.NM_Waehlhebel__timestamp]
    messages_cycle_times = {str(hil.Waehlhebel_04__timestamp): 10,
                            str(hil.DS_Waehlhebel__timestamp): 1000,
                            str(hil.KN_Waehlhebel__timestamp): 500,
                            str(hil.NM_Waehlhebel__timestamp): 200,
                            }

    cycletime_tol_perc = 0.10
    ttimeout = 1.0
    ttimeout_tol_perc = 0.05
    nm_stop_s = 0.4

    meas_vars = applikationsbotschaften + nm_botschaften + [hil.cl15_on__]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_173")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    testresult.append(["[.] Waehlhebelposition D aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('D')
    testresult.append(["\xa0" + descr, verdict])

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    # testresult.append(["[-0]", ""])

    testresult.append(["\xa0Start DAQ Measurement für Zustandsanalyse", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["[.] CAN-Trace auswerten", ""])
    testresult.append(["\xa0 Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2 auf 0", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    testresult.append(["[.] Setze SiShift FlgStrtNeutHldPha auf 1 (StartNeutralHoldPhase)", ""])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(1)

    testresult.append(["[+] Waehlhebelposition N aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Warte 150 ms und CAN-Trace auswerten", ""])
    time.sleep(0.150)

    testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 (KL15_EIN) ist",
        )
    )

    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 (aktiv) ist",
        )
    )
    testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Waehlhebel_CBV_AWB", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 (Inaktiv) ist",
        )
    )
    testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Waehlhebel_CBV_CRI", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 (NM_mit_Clusteranforderungen) ist",
        )
    )

    testresult.append(["\xa0Prüfe Signal NM_Waehlhebel:NM_Waehlhebel_FCAB", ""])
    descr, test_id, verdict = func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [12], [],
                                              "Prüfe, dass Wert 2048 (2_GearSelector) ist")
    testresult.append([descr, verdict])

    testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Waehlhebel_SNI_10", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_SNI_10__value,
            nominal_status=83,
            descr="Prüfe, dass Wert 83 (Waehlhebel_SNI) ist",
        )
    )

    testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_State", ""])
    testresult.append(
        _checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 (NM_RM_aus_BSM ) ist", ticket_id='EGA-PRM-164'
        )
    )

    testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Waehlhebel_UDS_CC", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 (Inaktiv) ist",
        )
    )

    testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Waehlhebel_Wakeup_V12", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 (Bus_Wakeup) ist",
        )
    )

    testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 (Inaktiv) ist",
        )
    )

    testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Tmin", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 0 (Inaktiv) ist",
        )
    )

    testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Aktiv_N_Haltephase_abgelaufen", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 (Inaktiv) ist",
        )
    )
    testresult.append(["[-0]", ""])

    testresult.append(["[.] 1 min warten...nach 1 min CAN-Trace auswerten", ""])
    time.sleep(60)

    # check if Application messages and NM messages are getting send
    check_cycletime(20)
    testresult.append(["[-0]", ""])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
