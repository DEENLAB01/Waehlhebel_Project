# ******************************************************************************
# -*- coding: latin1 -*-
# File    : E2E_248.py
# Title   : SiShift_BZ_Error_Jump
# Task    : BZ-Sprünge abwechselnd mit 2 richtigen BZ-Werten beaufschlagen für n/3+1 Zyklen, um  qualifizierten BZ-Fehlereintrag zu erhalten.
#
# Author  : Devangbhai Patel
# Date    : 11.10.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 11.10.2022 | Devangbhai   | initial


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
    test_data = identifier_dict['Check Programming Preconditions']
    SiShift_CRC= crc_dict['SiShift_01']
    exp_wrong_prec = [0xA7]

    aktiv_dtc = [(0xE00102, 0x27)]
    passiv_dtc = [(0xE00102, 0x26)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("E2E_248")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])

    testresult.append(["[.] Setze SiShift_FlgStrtNeutHldPha = 0", ""])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(0)

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
    testresult.append(["[+] Warte 2500ms", ""])
    time.sleep(2.5)

    testresult.append(["[.] Werte Wählhebel_04 Botschaft aus.", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Fahrstufe__value.get(),
            nominal_status=15,
            equal=False,
            descr="Prüfe WH_Fahrstufe != 15 ist"))

    # test step 2
    testresult.append(["[-]  Warte bis SiShift_01:SiShift_01_BZ = 0.", ""])
    while True:
        BZ_value= hil.SiShift_01__SiShift_01_20ms_BZ__value.get()
        if BZ_value == 0:
            # BZ switch on
            hil.SiShift_01__SiShift_01_20ms_BZ__switch.set(1)
            time.sleep(0.000)
            break

    # test step 3
    testresult.append(["[.]  Überschreibe SiShift_01_BZ  5x (n/3+1) mit je einer S-PDU mit um (BSZ_DeltaMaxInit+3 = 5) "
                       "inkrementierten Botschaftszähler, dann zwei S-PDUs mit um 1 inkrementierten Botschaftszähler. "
                       "(ausgehend von BZ=0: 1->5, 2, 3, 4->8, 5, 6, 7->11, 8, 9, 10->14, 11, 12, 13->1, 14, 15, 0->4)",
                       ""])
    bz_ = [5, 2, 3, 8, 5, 6, 11, 8, 9, 14, 11, 12, 1, 14, 15, 4]
    for i in bz_:
        if i== bz_[-1]:
            hil.SiShift_01__SiShift_01_20ms_CRC__value.set(SiShift_CRC['%s' % i])
            hil.SiShift_01__SiShift_01_20ms_BZ__value.set(i)
            print i, "THIS VALUE IS SET", SiShift_CRC['%s' % i]
            # BZ switch OFF
            hil.SiShift_01__SiShift_01_20ms_BZ__switch.set(0)
            break
        else:
            hil.SiShift_01__SiShift_01_20ms_CRC__value.set(SiShift_CRC['%s' % i])
            hil.SiShift_01__SiShift_01_20ms_BZ__value.set(i)
            print i, "THIS VALUE IS SET", SiShift_CRC['%s' % i]
            time.sleep(0.015)

    # test step 4
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc))

    # test step 5
    testresult.append(["[.]   Warte 200ms (3 + n/2) + 20 ms (Toleranz)", ""])
    time.sleep(0.200 + 0.020)

    # test step 6
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemory(passiv_dtc))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[-] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=True)