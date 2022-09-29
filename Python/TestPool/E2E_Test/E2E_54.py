# ******************************************************************************
# -*- coding: latin1 -*-
# File    : E2E_54.py
# Title   : SiShift_BZ_Error_Diag_Suppressed
# Task    : Erstmalige Fehlererkennung SiShift_01_BZ während "Initialized" bei ausgeblendeter Diagnose.
#
# Author  : Devangbhai Patel
# Date    : 20.07.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 20.07.2022 | Devangbhai   | initial
# 1.1  | 19.08.2022 | Devangbhai   | Added correct Precondition


from _automation_wrapper_ import TestEnv
from functions_diag import HexList
from diag_identifier import identifier_dict
import functions_common
from ttk_checks import basic_tests
import functions_gearselection
import time
from time import time as t
import functions_nm
from ttk_base.values_base import meta
import os

# Instantiate test environment
testenv = TestEnv()

aktiv_dtc = [(0xE00101, 0x27)]
passiv_dtc = [(0xE00101, 0x26)]

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

    # set Testcase ID #########################################################
    testresult.setTestcaseId("E2E_54")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])

    testresult.append(["[.] Setze OTAMC_D_01 VehicleProtectedEnvironment auf 0", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)

    testresult.append(["[.] Setze ORU_Control_A_01 OnlineRemoteUpdateControlA auf 4", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)

    testresult.append(["[.] setze ORU_Control_D_01 OnlineRemoteUpdateControlD auf 4", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)

    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    testresult.append(["[.] Setze Systeminfo_01_SI_NWDF_30 auf 0", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(0)

    hil.cl30_on__.set(1)
    hil.cl15_on__.set(1)
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Fahrstufe__value.get(),
            nominal_status=15,
            equal=False,
            descr="Prüfe WH_Fahrstufe != 15 ist"))

    testresult.append(["[.] Schalte KL 15 aus and RBS aus", ""])
    hil.ClampControl_01__KST_KL_15__value.set(0)
    hil.cl15_on__.set(0)

    time.sleep(0.120)
    func_nm.hil_ecu_tx_off_state("aus")
    time.sleep(2)

    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(canape_diag.resetEventMemory())

    testresult.append(["[.] Warte 16sec und prüfe Busruhe", ""])
    time.sleep(16)

    testresult.append(basic_tests.checkRange(value=hil.cc_mon__A,
                                  min_value=0.0,  # 0mA
                                  max_value=0.006,  # 6mA
                                  descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt",))

    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])

    # test step 1 and 2
    testresult.append(["[.] Schalte Kl30, setze SiShift_01 zyklus zeit auf 0.", ""])
    testresult.append(["[.] Schaltle Kl15 ein und RBS an und warte bis erste NM Botschaft empfäng", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_e2e(allstate=1, sisft=0, otamc=1, oruA=1, ourD=1)
    result = func_nm.is_bus_started()
    testresult.append(result)
    hil.Systeminfo_01__period.set(20)
    time.sleep(0.010)
    hil.Systeminfo_01__period.setState("an")

    # test step 2.1
    testresult.append(["[+] warte 40ms (Wechsel nach Initialized, Der Initiale Timeout beträgt 500ms)", ""])
    time.sleep(0.040)

    # test step 3
    testresult.append(["[-]  Setze SiShift_01 zyklus zeit auf 20ms und sende Permanant SiShift_01_BZ failure.", ""])
    hil.SiShift_01__SiShift_01_20ms_BZ__switch.set(1)
    hil.SiShift_01__period.setState("an")

    # test step 4
    testresult.append(["[.] Warte 240 ms.(n-q Botscahft in FIFO= 14-2= 12*20 = 240ms ) ", ""])
    time.sleep(0.240)

    # test step 5
    # testresult.append(["[.] Lese Fehlerspeicher (0xE00102 DTC aktiv)", ""])
    # testresult.append(canape_diag.checkEventMemory(passiv_dtc))
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 6
    testresult.append(["[.] Warte 500ms(TDiagStart) - 240ms (aus Schritt 4) + 20ms Toleranze", ""])
    time.sleep(0.500-0.240 + 0.020)

    # test step 7
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # testresult.append(["[+] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    # testresult.append(
    #     basic_tests.checkStatus(
    #         current_status=hil.Waehlhebel_04__WH_Fahrstufe__value.get(),
    #         nominal_status=15,
    #         equal=True,
    #         descr="Prüfe WH_Fahrstufe != 15 ist"))

    # test step 8
    testresult.append(["[.] Sende keine mehr SiShift_BZ failure und warte 140ms. (Wechsel nach Normal State, n/2 Botschaft im FIFO = 14/2= 7*20 = 140ms )", ""])
    hil.SiShift_01__SiShift_01_20ms_BZ__switch.set(0)
    time.sleep(0.140 + 0.035)

    # test step 9
    testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Fahrstufe__value.get(),
            nominal_status=15,
            equal=False,
            descr="Prüfe WH_Fahrstufe != 15 ist"))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[-] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=True)

