#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Verlaengerung_N_Haltephase_Timer4_N_Haltephase.py
# Title   : Verlaengerung N-Haltephase Timer4
# Task    : Verlängerung der N-Haltephase Timer4
#
# Author  : A. Neumann
# Date    : 02.07.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 02.07.2021 | A. Neumann | initial
#******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
import functions_common
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
    func_com = functions_common.FunctionsCommon(testenv)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    test_variable = hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value
    test_variable.alias = "Waehlhebel_04:WH_Zustand_N_Haltephase_2"

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_117")

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
    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    testresult.append(["[.] Setze SiShift_FlgStrtNeutHldPha = 1, VDSO_Vx3d  = 32766, SIShift_StLghtDrvPosn  = 6 und KL15 aus -  Prüfe, dass %s auf 1 wechselt" % test_variable.alias, ""])
    testresult.append(["\xa0Setze SiShift FlgStrtNeutHldPha auf 1 (StartNeutralHoldPhase)", ""])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(1)

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["\xa0Setze KL15 auf 0 (inactive)", ""])
    hil.cl15_on__.set(0)
    time.sleep(0.15)

    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(.15)

    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )

    for time_sleep in [60, 60*23]:
        testresult.append(["[.] Prüfe nach %s Minute Busruhe und Strommonitoring" % (time_sleep / 60), ""])
        func_com.waitSecondsWithResponse(time_sleep)
        descr, verdict = func_gs.checkBusruhe(daq, 1)

        testresult.append([descr, verdict])
        testresult.append(
            basic_tests.checkRange(
                value=hil.cc_mon__A.get(),
                min_value=0.002,  # 2mA
                max_value=0.100,  # 100mA
                descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
            )
        )

    testresult.append(["[.] Prüfe Ablauf Timer 1", ""])
    descr, verdict = func_nm.waitTillTimerEnds(timer=1, wait_time=60)
    testresult.append([descr, verdict])

    testresult.append(["[.] Prüfe Ablauf Timer 2", ""])
    descr, verdict = func_nm.waitTillTimerEnds(timer=2)
    testresult.append([descr, verdict])

    testresult.append(["[.] Prüfe Ablauf Timer 3", ""])
    descr, verdict = func_nm.waitTillTimerEnds(timer=3)
    testresult.append([descr, verdict])

    testresult.append(["[.] Prüfe Start Timer 4", ""])
    descr, verdict = func_nm.waitTillTimerEnds(timer=4, wait_time=0.5, switch_rx_signals=False)
    testresult.append([descr, verdict])

    testresult.append(["[.] Setze Geschwindigkeit > v_Stillstand um Timer 4 zu verlängern", ""])
    cycle_vdso = hil.VDSO_05__period.value_lookup['an']
    descr, verdict = func_gs.setVelocity_kmph(1.008, True, (cycle_vdso*2/1000))
    testresult.append([descr, verdict])

    testresult.append(["[.] Warte 1 Minute und prüfe, dass Timer 4 verlängert wird ", ""])
    time.sleep(60)

    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 5 ist",
        )
    )
    testresult.append(["\xa0Prüfe NM_Waehlhebel:NM_Waehlhebel_FCAB", ""])
    descr, verdict = func_nm.checkFcabBitwise(fcab_value=hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), bit_exp_one=[1], bit_exp_zero=[])
    testresult.append([descr, verdict])

    testresult.append(["[.] Setze Geschwindigkeit < v_Stillstand", ""])
    descr, verdict = func_gs.setVelocity_kmph(0, True, (cycle_vdso * 2 / 1000))
    testresult.append([descr, verdict])

    testresult.append(["[.] Prüfe Ablauf Timer 4", ""])
    descr, verdict = func_nm.waitTillTimerEnds(timer=4)
    testresult.append([descr, verdict])

    testresult.append(["[.] Prüfe Ablauf Timer Ende", ""])
    descr, verdict = func_nm.waitTillTimerEnds(timer='ende')
    testresult.append([descr, verdict])

    testresult.append(["[.] Prüfe Busruhe", ""])
    func_com.waitSecondsWithResponse(1)
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
