# ******************************************************************************
# -*- coding: latin1 -*-
# File    : PFIFF_VDOS_Timeout_338733.py
# Title   : PFIFF_VDOS_Timeout_338733
# Task    : Erstmalige PFIFF_VDOS_Timeout_338733
#
# Author  : Mohammed Abdul Karim
# Date    : 22.09.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 22.07.2022 | Mohammed   | initial

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
from functions_nm import _checkStatus


import os

# Instantiate test environment
testenv = TestEnv()

aktiv_dtc = [(0xE00104, 0x27)]
passiv_dtc = [(0xE00104, 0x26)]

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
    testresult.setTestcaseId("VDOS_Timeout_338733")

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

    testresult.append(["[.] Setze Systeminfo_01_SI_NWDF_30 auf 1", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

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
    #func_nm.hil_ecu_e2e(allstate=1, sisft=0, otamc=1, oruA=1, ourD=1)
    state ="an"
    hil.SiShift_01__period.setState(state)
    hil.ClampControl_01__period.setState(state)
    hil.VDSO_05__period.setState("aus")
    hil.Diagnose_01__period.setState(state)
    hil.NVEM_12__period.setState(state)
    hil.Dimmung_01__period.setState(state)
    hil.NM_Airbag__period.setState(state)
    hil.OBD_03__period.setState(state)
    hil.OBD_04__period.setState(state)
    hil.ORU_Control_A_01__period.setState(state)
    hil.ORU_Control_D_01__period.setState(state)
    hil.OTAMC_D_01__period.setState(state)
    hil.Systeminfo_01__period.setState(state)
    hil.NM_HCP1__period.setState(state)
    result = func_nm.is_bus_started()
    testresult.append(result)

    hil.Systeminfo_01__period.set(20)
    time.sleep(0.010)
    hil.Systeminfo_01__period.setState("an")

    # test step 2.1
    testresult.append(["[+]  warte 500ms ", ""])
    time.sleep(0.500)

    testresult.append(["[.] Lese Fehlerspeicher ", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["[+]  warte 500ms ", ""])
    time.sleep(.5)
    testresult.append(["[.] Lese Fehlerspeicher (0xE00104 DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory([(0xE00104, 0x27)]))




    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[-] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=True)
