# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Ablauf_Empfang_SiShift_StLghtDrvPosn_INIT_nach_Start_N_Haltephase.py
# Title   : Ablauf der N Haltephase durch Empfang SiShift = 0
# Task    : Ablauf der N-Haltephase durch Empfang (SIShift_StLghtDrvPosn = 0)
#
# Author  : Mohammed Abdul Karim
# Date    : 14.07.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 18.05.2021 | Mohammed | initial
# 1.1  | 18.05.2021 | Mohammed | Rework
# 1.2  | 18.05.2021 | Mohammed | Added review TestSpec
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
import functions_nm
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
    testresult.setTestcaseId("TestSpec_122")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    testresult.append(["[.] Waehlhebelposition D aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('D')
    testresult.append(["\xa0" + descr, verdict])

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+] Prüfe, dass %s zum Teststart wie erwartet gesetzt ist (=0)" % test_variable.alias, ""])

    # test step 1
    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2 = 0", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    # test step 2
    testresult.append(["\xa02 Setze SiShift_FlgStrtNeutHldPha = 1,VDSO_Vx3d = 32766 (0 km/h),SIShift_StLghtDrvPosn = 6, und 200ms warten ", "INFO"])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(1)

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])
    testresult.append(["\xa0 Warte 200ms", ""])
    time.sleep(.200)

    testresult.append(["\x0aPrüfe, dass WH_Zustand_N_Haltephase_2 = 0 ", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    # test step 3
    testresult.append(["\xa03 Setze KL15 auf 0 (inactive) und 300ms Warten", ""])
    hil.cl15_on__.set(0)
    time.sleep(.300)

    testresult.append(["\xa04 Setze  SiShift_StLghtDrvPos auf 0 ", ""])
    descr, verdict = func_gs.changeDrivePosition('Init')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2 = 1", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 (aktiv_Timer_laeuft) ist",
        )
    )

    # test step 5
    testresult.append(["\xa05. Schalte Senden von RX Signalen (HiL --> ECU) aus", ""])
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])

    # test step 5.1
    testresult.append(["\xa05. 1 min warten...nach 1 min CAN-Trace auswerten", ""])
    time.sleep(60)
    testresult.append(["Prüfe Strommonitoring und Busruhe nach 1 Minute", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    testresult.append(["\x0aPrüfe, Kein Senden und Empfangen von Botschaften (WH im lokalen Nachlauf)", ""])
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    testresult.append([descr, verdict])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
