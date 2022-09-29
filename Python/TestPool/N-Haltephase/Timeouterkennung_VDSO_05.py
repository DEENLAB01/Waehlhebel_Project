#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Timeouterkennung_VDSO_05.py
# Title   : Timeouterkennung VDSO_05
# Task    : Timeouterkennung der N-Haltephase durch VDSO_05-Timeout
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
#******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
import functions_common
import functions_nm
import time
import functions_hil
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
    func_hil = functions_hil.FunctionsHil(testenv, hil)

    # Initialize variables ####################################################
    test_variable = hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value
    test_variable.alias = "Waehlhebel_04:WH_Zustand_N_Haltephase_2"
    VDSO_05__period_period = hil.VDSO_05__period
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    allowed_fahrstufe = [4, 5, 6, 7, 8 ]  # nicht_betaetigt, D, N, R, P,
    wh_fahrstufe_fehlerwert = 15 # 'Fehler
    exp_dtc = 0x200104
    failure_reset_time = 1.0  # Todo

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_184")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
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

    for time_sleep in [60, 60*25]:
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
            ))

    testresult.append(["[.] Prüfe Ablauf Timer 1", ""])
    descr, verdict = func_nm.waitTillTimerEnds(timer=1)
    testresult.append([descr, verdict])

    testresult.append(["[.] Setze Geschwindigkeit > v_Stillstand um Timer 4 zu verlängern", ""])
    cycle_vdso = hil.VDSO_05__period.value_lookup['an']
    descr, verdict = func_gs.setVelocity_kmph(0, True, (cycle_vdso * 0 / 1000))
    testresult.append([descr, verdict])

    descr, verdict = func_gs.switchAllRXMessagesOn()
    testresult.append([descr, verdict])

    testresult.append([" Warte 5000ms (tMSG_CYCLE)", ""])
    time.sleep(5)
    testresult.append(["[.] Lese Fehlerspeicher aus (0x200104 -DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory([[exp_dtc, dc.DTCactive]]))

    cycle_vdso = hil.VDSO_05__period.value_lookup['an']
    descr, verdict = func_gs.setVelocity_kmph(0, True, (cycle_vdso * 5 / 1000))

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append([" Warte 1000ms ", ""])
    time.sleep(1)
    testresult.append(["[.] Lese Fehlerspeicher auslesen (0x200104 -DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory([[exp_dtc, dc.DTCactive]]))

    testresult.append(["[.] Prüfe Ablauf Timer 2", ""])
    descr, verdict = func_nm.waitTillTimerEnds(timer=2)
    testresult.append([descr, verdict])

    testresult.append(["[.] Prüfe Ablauf Timer 3", ""])
    descr, verdict = func_nm.waitTillTimerEnds(timer=3)
    testresult.append([descr, verdict])

    cycle_vdso = hil.VDSO_05__period.value_lookup['an']
    descr, verdict = func_gs.setVelocity_kmph(0, True, (cycle_vdso * 5 / 1000))

    descr, verdict = func_gs.switchAllRXMessagesOn()
    testresult.append([descr, verdict])

    cycle_vdso = hil.VDSO_05__period.value_lookup['an']
    descr, verdict = func_gs.setVelocity_kmph(0, True, (cycle_vdso * 5 / 1000))

    testresult.append([" Warte 5000ms (tMSG_CYCLE)", ""])
    time.sleep(5)
    testresult.append(["[.] Lese Fehlerspeicher aus (0x200104 -DTC aktiv)", ""])  ###
    testresult.append(canape_diag.checkEventMemory([[exp_dtc, dc.DTCactive]]))

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    cycle_vdso = hil.VDSO_05__period.value_lookup['an']
    descr, verdict = func_gs.setVelocity_kmph(0, True, (cycle_vdso * 5 / 1000))

    testresult.append([" Warte 1000ms (Fehlerspeicher erneut auslesen)", ""])
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append([" Warte 1000ms ", ""])
    time.sleep(1)
    testresult.append(["[.] Lese Fehlerspeicher auslesen (0x200104 -DTC aktiv)", ""])  ###
    testresult.append(canape_diag.checkEventMemory([[exp_dtc, dc.DTCactive]]))

    testresult.append(["[.] Prüfe Start Timer 4", ""])
    descr, verdict = func_nm.waitTillTimerEnds(timer=4, wait_time=0.5, switch_rx_signals=False)
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
