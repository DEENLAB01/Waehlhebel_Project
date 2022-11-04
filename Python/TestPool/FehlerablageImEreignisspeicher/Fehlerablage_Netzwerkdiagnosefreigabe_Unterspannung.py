# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Fehlerablage_Netzwerkdiagnosefreigabe_Unterspannung.py
# Title   : Fehlerablage_Netzwerkdiagnosefreigabe_Unterspannung
# Task    : DTC 0xE00107 Netzwerkdiagnosefreigabe bei Unterspannung
#
# Author  : Devangbhai Patel
# Date    : 18.10.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 18.10.2022 | Devangbhai   | initial

from _automation_wrapper_ import TestEnv
import functions_common
import functions_gearselection
import time
import functions_nm

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

    aktiv_dtc_unterspannung = [(0x800100, 0x27), (0x800102, 0x27)]
    passiv_dtc_unterspannung = [(0x800100, 0x26), (0x800102, 0x26)]

    aktiv_dtc_ORUA_TO = [(0xE00107, 0x27)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_433")

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
    testresult.append(["[.] Setze  ORU_Control_A_01 Zykluszeit auf 0.", ""])
    hil.ORU_Control_A_01__period.setState("aus")

    # test step 2
    testresult.append(["[.] Warte 2500ms", ""])
    time.sleep(2.5)

    # test step 3
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 4
    testresult.append(["[.] Setze KL30 Spannung (NWDF ungültiger Bereich): 9,0V - 0,180V (2% Toleranz) - 0,03V (HiL Toleranz) = 8,79V", ""])
    hil.vbat_cl30__V.set(8.79)

    # test step 5
    testresult.append(["[.] Warte 500ms", ""])
    time.sleep(0.500)

    # test step 6
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 7
    testresult.append(["[.]   Setze Kl.30 Spannung zurück auf 13 V", ""])
    hil.vbat_cl30__V.set(13)

    # test step 8
    testresult.append(["[.] Warte 500ms (tDiagStart) + 200ms (Toleranz).", ""])
    time.sleep(0.500 + 0.200)

    # test step 9
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 10
    testresult.append(["[.] Warte 2500ms", ""])
    time.sleep(2.500)

    # test step 11
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 12
    testresult.append(["[.] Warte 2000ms (4500ms - 2500ms= 2000ms)", ""])
    time.sleep(2.000 + 0.250)

    # test step 13
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc_ORUA_TO))


    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[-] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=True)