#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Timeouterkennung_SiShift_01_nach_Ende_Timer4.py
# Title   : Timeouterkennung N-Haltephase SiShift Timer4 Ende
# Task    : Timeouterkennung der N-Haltephase SiShift Timer4 nach Ende
#
# Author  : Mohammed Abdul Karim
# Date    : 22.07.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 22.07.2021 | M. Abdul Karim | initial
# 1.1  | 26.07.2021 | M. Abdul Karim | Rework
#******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
import functions_common
import functions_nm
import time
import data_common as dc

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
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    allowed_fahrstufe = [4, 5, 6, 7, 8 ]  # nicht_betaetigt, D, N, R, P,
    wh_fahrstufe_fehlerwert = 15 # 'Fehler'
    exp_dtc = 0X200101
    failure_reset_time = 1.0  # Todo
    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_182")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    testresult.append(["[.] Warte 200ms", ""])
    time.sleep(0.200)
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[.] Prüfe Waehlhebel_04:WH_Fahrstufe != 15", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = allowed_fahrstufe,
            current_value= current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe: WH_Fahrstufe != 15 ist"
        )
    )

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
    testresult.append(["[.] Warte 150ms", ""])
    time.sleep(0.15)

    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])

    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )

    for time_sleep in [60, 60*24]:
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
    descr, verdict = func_nm.waitTillTimerEnds(timer=2, switch_rx_signals=False)
    testresult.append([descr, verdict])

    testresult.append(["[.] Prüfe Ablauf Timer 3", ""])
    descr, verdict = func_nm.waitTillTimerEnds(timer=3)
    testresult.append([descr, verdict])

    testresult.append(["[.] Prüfe Start Timer 4", ""])
    descr, verdict = func_nm.waitTillTimerEnds(timer=4)
    testresult.append([descr, verdict])

    testresult.append(["[.] 5000ms (tMSG_CYCLE)", ""])
    time.sleep(5)
    testresult.append(["[.] Lese Fehlerspeicher aus (0x200101 -DTC aktiv)", ""]) ### Todo:
    testresult.append(canape_diag.checkEventMemory([[exp_dtc, dc.DTCactive]]))

    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])

    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    testresult.append(["Warte TTimeout 1000 ms (RS-->PBSM)", "INFO"])
    testresult.append(["[.] Prüfe, dass in Ready Sleep Mode gewechselt wurde", ""])
    t_timeout_s = 1
    testresult.append(["[.] Warte %sms + 1000ms (T Timeout)" % (t_timeout_s * 1000), ""])
    func_com.waitSecondsWithResponse(t_timeout_s * 1.05 + 0.1)

    testresult.append(["[.] Warte TWaitBusSleep 750 ms (PBSM-->BSM)", ""])
    testresult.append(["[.] Prüfe, dass in Prepare Bus-Sleep Mode gewechselt wurde", ""])
    t_timeout_s = 1
    testresult.append(["[.] Warte %sms + 750ms (T Timeout)" % (t_timeout_s * 750), ""])
    func_com.waitSecondsWithResponse(t_timeout_s * 1.05 + 0.1)

    testresult.append(["[.] Prüfe, Es werden keine Botschaften versendet oder empfangen", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.0,  # 0mA
            max_value=0.002,  # 2mA
            descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt"
        )
    )

    descr, verdict = func_gs.checkBusruhe(daq)
    testresult.append([descr, verdict])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
    del (testenv)

print "done"