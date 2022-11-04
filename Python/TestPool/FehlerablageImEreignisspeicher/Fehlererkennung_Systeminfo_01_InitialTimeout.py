# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Fehlererkennung_Systeminfo_01_InitialTimeout.py
# Title   : Fehlererkennung_Systeminfo_01_InitialTimeout
# Task    : DTC 0xE00106 Initiale Timeouterkennung Systeminfo_01 und Ablage im Fehlerspeicher
#
# Author  : Devangbhai Patel
# Date    : 16.10.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 16.10.2022 | Devangbhai   | initial
# 1.1  | 03.11.2022 | Devangbhai   | corrected the steps according to the new test specification

from _automation_wrapper_ import TestEnv
from functions_diag import HexList
from diag_identifier import identifier_dict
from CRC_values import crc_dict
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

    aktiv_dtc = [(0xE00106, 0x27)]
    passiv_dtc = [(0xE00106, 0x26)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_424")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    hil.cl30_on__.set(1)
    hil.cl15_on__.set(1)

    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze Systeminfo_01_SI_NWDF_30 auf 1", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag = testenv.getCanapeDiagnostic()
    canape_diag.disableTesterPresent()

    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(canape_diag.resetEventMemory())
    testresult.append(canape_diag.checkEventMemoryEmpty())

    ####################################################################################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])

    # test step 1
    testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Fahrstufe__value.get(),
            nominal_status=15,
            equal=False,
            descr="Prüfe WH_Fahrstufe != 15 ist"))

    # test step 2
    testresult.append(["[.] Schalte KL 15 aus and RBS aus", ""])
    hil.ClampControl_01__KST_KL_15__value.set(0)
    hil.cl15_on__.set(0)

    time.sleep(0.120)
    func_nm.hil_ecu_tx_off_state("aus")
    time.sleep(2)

    # test step 3
    testresult.append(["[.] Warte 16sec und prüfe CAN-Kommunikation", ""])
    time.sleep(16)

    testresult.append(basic_tests.checkRange(value=hil.cc_mon__A,
                                             min_value=0.0,  # 0mA
                                             max_value=0.006,  # 6mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt", ))

    # test step 4
    testresult.append(["[.] Setze Zykluszeit der Botschaft Systeminfo_01 auf 0 ms", ""])
    hil.Systeminfo_01__period.setState("aus")

    # test step 5
    testresult.append(["[.] Schalte Kl.15 ein und starte RBS und warte bis erste NM Botschaft empfängt", ""])
    hil.cl15_on__.set(1)
    hil.VDSO_05__period.setState("an")
    hil.ClampControl_01__period.setState("an")
    hil.Diagnose_01__period.setState("an")
    hil.NVEM_12__period.setState("an")
    hil.Dimmung_01__period.setState("an")
    hil.NM_Airbag__period.setState("an")
    hil.OBD_03__period.setState("an")
    hil.OBD_04__period.setState("an")
    hil.NM_HCP1__period.setState("an")
    hil.SiShift_01__period.setState("an")
    hil.ORU_Control_A_01__period.setState("an")
    hil.ORU_Control_D_01__period.setState("an")
    hil.OTAMC_D_01__period.setState("an")
    result = func_nm.is_bus_started()
    testresult.append(result)

    # test step 6
    testresult.append(["[.]  Warte 5000ms (Timeout s_NWDF)", ""])
    time.sleep(5)

    # test step 7
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 8
    testresult.append(["[.] Warte 700ms (tDiagStart)", ""])
    time.sleep(0.700)

    # test step 9
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 10
    testresult.append(["[.]   Warte 5000ms (tMSG_Timeout) + 250ms Toleranze", ""])
    time.sleep(5 + 0.250)

    # test step 11
    testresult.append(["[.] Lese Fehlerspeicher", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc))


    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[-] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=True)