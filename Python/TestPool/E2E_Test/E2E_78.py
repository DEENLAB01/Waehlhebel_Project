# ******************************************************************************
# -*- coding: latin1 -*-
# File    : E2E_78.py
# Title   : SiShift_NoError_Normal
# Task    : Keine Fehlererkennung während 10-maliger Fehlerbeaufschlagung unterhalb Toleranzschwelle (BZ-Fehler, Timeout-Fehler).
#
# Author  : Devangbhai Patel
# Date    : 25.07.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 25.07.2022 | Devangbhai   | initial
# 1.1  | 15.08.2022 | Devangbhai   | Changed the cycle time to 95ms insted of 200 in test step 6
# 1.2  | 19.08.2022 | Devangbhai   | Added correct Precondition

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
    test_data = identifier_dict['Check Programming Preconditions']
    exp_wrong_prec = [0xA7]

    aktiv_dtc = [(0xE00103, 0x27)]
    passiv_dtc = [(0xE00103, 0x26)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("E2E_78")

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

    # test step 1
    testresult.append(["[.] Schalte Kl.30 ein und starte RBS und warte bis erste NM Botschaft empfängt", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_e2e(allstate=1, sisft=1, otamc=1, oruA=1, ourD=1)
    result = func_nm.is_bus_started()
    testresult.append(result)

    # test step 1.1
    testresult.append(["[+]  Warte 2500 ms.(Wechsel nach Normal aus Initialized-> TDiagStart = 500ms)", ""])
    time.sleep(2.500)
    testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Fahrstufe__value.get(),
            nominal_status=15,
            equal=False,
            descr="Prüfe WH_Fahrstufe != 15 ist"))

    testresult.append(["[-] Sende SiShift_01 BZ > SiShift_01 Timeout failure unterlab Toleranzschwelle und "
                       "prufe Fehlerspeicher/WH_Fahrstufe und dann sende SiShift_01 BZ < SiShift_01 Timeout failure "
                       "unterlab Toleranzschwelle und prufe fehlerspeicher/WH_Fahrstufe ", ""])
    for i in range(1, 11):
        hil.SiShift_01__SiShift_01_20ms_BZ__switch.set(1)
        time.sleep(0.080)
        hil.SiShift_01__period.set(0)
        time.sleep(0.040)
        hil.SiShift_01__period.set(20)
        time.sleep(0.080)
        hil.SiShift_01__period.set(0)
        time.sleep(0.040)
        hil.SiShift_01__SiShift_01_20ms_BZ__switch.set(0)
        hil.SiShift_01__period.set(20)
        testresult.append(["\xa0 Lese  WH_Fahrstufe Fehlerspeicher aus nach Schleife %s" % i, ""])
        testresult.append(
            basic_tests.checkStatus(
                current_status=hil.Waehlhebel_04__WH_Fahrstufe__value.get(),
                nominal_status=15,
                equal=False,
                descr="Prüfe WH_Fahrstufe != 15 ist"))
        testresult.append(canape_diag.checkEventMemoryEmpty())

        time.sleep(14 * 0.020)

        hil.SiShift_01__SiShift_01_20ms_BZ__switch.set(1)
        time.sleep(0.040)
        hil.SiShift_01__period.set(0)
        time.sleep(0.080)
        hil.SiShift_01__period.set(20)
        time.sleep(0.040)
        hil.SiShift_01__period.set(0)
        time.sleep(0.080)
        hil.SiShift_01__SiShift_01_20ms_BZ__switch.set(0)
        hil.SiShift_01__period.set(20)

        testresult.append(["\xa0 Lese WH_Fahrstufe Fehlerspeicher aus nach Schleife %s" % i, ""])
        testresult.append(canape_diag.checkEventMemoryEmpty())
        testresult.append(
                basic_tests.checkStatus(
                    current_status=hil.Waehlhebel_04__WH_Fahrstufe__value.get(),
                    nominal_status=15,
                    equal=False,
                    descr="Prüfe WH_Fahrstufe != 15 ist"))
        time.sleep(14 * 0.020)

    # # test step 2
    # testresult.append(["[-] Setze SiShift_01 zyklus zeit auf 95ms. (Qualifikation Zeit für Timeout DTC eintrag = n-q+ 1= 13 fehlende Botschaft im FIFO  )", ""])
    # hil.SiShift_01__period.set(95)
    #
    # # test step 3
    # testresult.append(["[.]  Warte 150ms. (3 Zyklus Zeit mit neue Zyklus Zeit)", ""])
    # time.sleep(0.285)
    #
    # # test step 4
    # testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    # testresult.append(
    #     basic_tests.checkStatus(
    #         current_status=hil.Waehlhebel_04__WH_Fahrstufe__value.get(),
    #         nominal_status=15,
    #         equal=False,
    #         descr="Prüfe WH_Fahrstufe != 15 ist"))
    #
    # # test step 5
    # testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    # testresult.append(canape_diag.checkEventMemoryEmpty())
    #
    # # test step 6
    # testresult.append(["[.] Setze SiShift_01 zyklus zeit auf 20ms und warte 140ms+ 20ms Toleranze (n/2 gültige signal im FIFO)",""])
    # hil.SiShift_01__period.set(20)
    # time.sleep(0.140 + 0.020)
    #
    # # test step 7
    # testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    # testresult.append(
    #     basic_tests.checkStatus(
    #         current_status=hil.Waehlhebel_04__WH_Fahrstufe__value.get(),
    #         nominal_status=15,
    #         equal=False,
    #         descr="Prüfe WH_Fahrstufe != 15 ist"))
    #
    # # test step 8
    # testresult.append(["[.] Halte SiShift_01_BZ.", ""])
    # hil.SiShift_01__SiShift_01_20ms_BZ__switch.set(1)
    #
    # # test step 9
    # testresult.append(["[.]  Warte 200ms (Qualifikation Zeit für BZ Failure DTC eintrag = n-q+ 1= 13 fehlende Botschaft im FIFO )", ""])
    # time.sleep(0.200)
    #
    # # test step 10
    # testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    # testresult.append(
    #     basic_tests.checkStatus(
    #         current_status=hil.Waehlhebel_04__WH_Fahrstufe__value.get(),
    #         nominal_status=15,
    #         equal=False,
    #         descr="Prüfe WH_Fahrstufe != 15 ist"))
    #
    # # test step 11
    # testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    # testresult.append(canape_diag.checkEventMemoryEmpty())
    #
    # # test step 12
    # testresult.append(["[.] Setze  SiShift_01_BZ wider fort und warte 140ms+ 20ms Toleranze (n/2 gültige signal im FIFO)", ""])
    # hil.SiShift_01__SiShift_01_20ms_BZ__switch.set(0)
    # hil.SiShift_01__period.set(20)
    # time.sleep(0.140 + 0.020)
    #
    # # test step 13
    # testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    # testresult.append(
    #     basic_tests.checkStatus(
    #         current_status=hil.Waehlhebel_04__WH_Fahrstufe__value.get(),
    #         nominal_status=15,
    #         equal=False,
    #         descr="Prüfe WH_Fahrstufe != 15 ist"))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=True)