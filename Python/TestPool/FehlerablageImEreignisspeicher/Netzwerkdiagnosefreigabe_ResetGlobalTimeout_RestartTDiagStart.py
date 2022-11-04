# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Netzwerkdiagnosefreigabe_ResetGlobalTimeout_RestartTDiagStart.py
# Title   : Netzwerkdiagnosefreigabe_ResetGlobalTimeout_RestartTDiagStart
# Task    : DTC 0xE00104 Netzwerkdiagnosefreigabe Restart tDiagStart bei Rückkehr aus Global Timeout
#
# Author  : Devangbhai Patel
# Date    : 19.10.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 19.10.2022 | Devangbhai   | initial
# 1.1  | 04.11.2022 | Devangbhai | Added Ticket ID


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

    aktiv_dtc = [(0xE00104, 0x27)]
    passiv_dtc = [(0xE00104, 0x26)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_436")

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

    testresult.append(["[.] Setze OTAMC_D_01 VehicleProtectedEnvironment auf 0", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)

    testresult.append(["[.] Setze ORU_Control_A_01 OnlineRemoteUpdateControlA auf 4", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)

    testresult.append(["[.] setze ORU_Control_D_01 OnlineRemoteUpdateControlD auf 4", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)

    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag = testenv.getCanapeDiagnostic()
    canape_diag.disableTesterPresent()

    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(canape_diag.resetEventMemory())
    testresult.append(canape_diag.checkEventMemoryEmpty())

    ####################################################################################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])

    # test step 1
    testresult.append(["[.] Warte 3000ms", ""])
    time.sleep(3)

    # test step 2
    testresult.append(["[.] Stoppe RBS.", ""])
    func_nm.hil_ecu_tx_off_state("aus")

    # test step 3
    testresult.append(["[.] Warte 3000ms", ""])
    time.sleep(3)

    # test step 4
    testresult.append(["[.] Starte RBS mit VDSO_05 Zykluszeit = 0ms.", ""])
    hil.VDSO_05__period.setState("aus")
    hil.ClampControl_01__period.setState("an")
    hil.Diagnose_01__period.setState("an")
    hil.NVEM_12__period.setState("an")
    hil.Dimmung_01__period.setState("an")
    hil.NM_Airbag__period.setState("an")
    hil.OBD_03__period.setState("an")
    hil.OBD_04__period.setState("an")
    hil.Systeminfo_01__period.setState("an")
    hil.NM_HCP1__period.setState("an")
    hil.SiShift_01__period.setState("an")
    hil.ORU_Control_A_01__period.setState("an")
    hil.ORU_Control_D_01__period.setState("an")
    hil.OTAMC_D_01__period.setState("an")

    # test step 5
    testresult.append(["[.] Lese Fehlerspeicher", ""])
    testresult.append(canape_diag.checkEventMemory([(0xE00100, 0x27), (0xE00101, 0x27)], ticket_id="EGA-PRM-297"))

    # test step 6
    testresult.append(["[.]  Warte 500ms (tDiagStart) + 200ms (Toleranz)", ""])
    time.sleep(0.500 + 0.200)

    # test step 7
    testresult.append(["[.] Lese Fehlerspeicher", ""])
    testresult.append(canape_diag.checkEventMemory([(0xE00100, 0x26), (0xE00101, 0x26)], ticket_id="EGA-PRM-297"))

    # test step 8
    testresult.append(["[.]  Warte 500ms (tMSG_Timeout)", ""])
    time.sleep(0.500)

    # test step 9
    testresult.append(["[.] Lese Fehlerspeicher", ""])
    testresult.append(canape_diag.checkEventMemory([(0xE00100, 0x26), (0xE00101, 0x26), (0xE00104, 0x27)], ticket_id="EGA-PRM-297"))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[-] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=True)