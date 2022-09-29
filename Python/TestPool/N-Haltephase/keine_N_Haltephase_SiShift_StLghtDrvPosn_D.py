# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : keine_N_Haltephase_SiShift_StLghtDrvPosn_D.py
# Title   : keine_N_Haltephase_SiShift_StLghtDrvPosn_D = D
# Task    : N Haltephase wird nicht gestartet (SiShift_StLghtDrvPosn = 5)
#
# Author  : Mohammed Abdul Karim
# Date    : 16.07.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 18.07.2021 |  Mohammed | initial
# 1.1  | 04.02.2022 | Mohammed  | Added Fehler ID
# 1.3  | 07.02.2022 | Mohammed | Added Strommonitoring
# 1.4  | 27.04.2022 | Mohammed   | Added NM_Waehlhebel_FCAB = 1, 12, 41
# 1.5  | 28.07.2022 | Mohammed   | Rework
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
import functions_nm
from functions_nm import _checkStatus
import time

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
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    test_variable = hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value
    test_variable.alias = "Waehlhebel_04:WH_Zustand_N_Haltephase_2"

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_178")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    testresult.append(["[.] Waehlhebelposition D aktiviert und 4 Sekunden warten ", ""])
    descr, verdict = func_gs.changeDrivePosition('D')
    testresult.append(["\xa0" + descr, verdict])
    testresult.append(["\xa04000 ms warten", ""])
    time.sleep(4)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    # testresult.append(["[-0]", ""])

    testresult.append(["[.] CAN-Trace auswerten", ""])
    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2 auf 0", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    testresult.append(["\xa0 Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Tmin auf 0", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 (Inaktiv) ist",
        )
    )

    testresult.append(["\xa0 Prüfe NM_Waehlhebel_FCAB:mindestens --> 01_CarWakeUp, 12_GearSelector und 41_Diagnosis_Powertrain", ""])
    testresult.append(func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [1], [],
                                               descr="NM_Waehlhebel_FCAB:01_CarWakeUp"))
    testresult.append(func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [12], [],
                                               descr="NM_Waehlhebel_FCAB:12_GearSelector"))
    testresult.append(func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [41], [],
                                               descr="NM_Waehlhebel_FCAB:41_Diagnosis_Powertrain"))

    testresult.append(["[.] Setze SiShift FlgStrtNeutHldPha auf 1 (StartNeutralHoldPhase)", ""])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(1)

    testresult.append(["[+] Waehlhebelposition D aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('D')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze KL15 auf 0 (inactive)", ""])
    hil.cl15_on__.set(0)

    testresult.append(["[.] Warte 150 ms und CAN-Trace auswerten", ""])
    time.sleep(0.15)

    testresult.append(["\xa0 Prüfe, dass N-Haltephase inaktiv ist", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 (inaktiv) ist",
        )
    )

    testresult.append(["[-0]", ""])

    testresult.append(["[.] Schalte Senden von empfangenen Signalen aus (HiL -> ECU)", ""])
    hil.can0_HIL__HIL_TX__enable.set(0)
    testresult.append(["[+] Prüfe, 1 min warten...nach 1 min CAN-Trace auswerten", ""])
    time.sleep(60)
    temp_value = func_nm.low_current()
    testresult.append(basic_tests.checkRange(value=temp_value / 1000,
                                             min_value=0.0,  # 0mA
                                             max_value=0.002,  # 2mA
                                             descr=" Prüfe, dass Strom zwischen 0mA und 2mA liegt"))
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
