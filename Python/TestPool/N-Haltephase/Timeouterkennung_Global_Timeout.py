#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Timeouterkennung_Global_Timeout.py
# Title   : Timeouterkennung Global Timeout
# Task    : Timeouterkennung der N-Haltephase durch Global-Timeout
#
# Author  : A. Abdul Karim
# Date    : 22.07.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 22.07.2021 | Mohammed Abdul Karim | initial
# 1.1  | 30.07.2021 | Mohammed Abdul Karim | Rework
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

#### Using Ref TestSpec_117
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
    ###

    # Initialize variables ####################################################
    test_variable = hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value
    test_variable.alias = "Waehlhebel_04:WH_Zustand_N_Haltephase_2"
    SiShift_period = hil.SiShift_01__period
    exp_dtc = 0x200100
    failure_reset_time = 1.0  # Todo

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_183")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

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
            )
        )

    testresult.append(["[.] Prüfe Werte der Botschaft NM_Waehlhebel", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="NM_Waehlhebel_CBV_AWB: Aktiver_WakeUp"),
        func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [12], [],
                                 descr="NM_Waehlhebel_FCAB:12_GearSelector"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1,
                                descr="WH_Zustand_N_Haltephase_2:aktiv_Timer_laeuft"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1,
                                descr="NM_Waehlhebel_NM_aktiv_Tmin:Mindestaktivzeit"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv")
    ]

    testresult.append([" Warte 500 ms (initial Timeout)", ""])
    time.sleep(0.500)

    testresult.append(["[.] Lese Fehlerspeicher aus (0x200100 -DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory([[exp_dtc, dc.DTCactive]]))

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

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

    testresult.append(["[.] Prüfe,  Es werden keine Botschaften versendet oder empfangen", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.0,  # 0mA
            max_value=0.02,  # 2mA
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
