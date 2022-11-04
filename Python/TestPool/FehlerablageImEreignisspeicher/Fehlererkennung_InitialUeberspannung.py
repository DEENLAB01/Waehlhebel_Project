# ******************************************************************************
# -*- coding: latin1 -*-
# File    : Fehlererkennung_InitialUeberspannung.py
# Title   : Fehlererkennung_InitialÜberspannung
# Task    : DTC 0x800101 Initiale Überspannungserkennung und Ablage im Fehlerspeicher
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

    aktiv_dtc = [(0x800100, 0x27), (0x800101, 0x27)]
    passiv_dtc = [(0x800100, 0x26), (0x800101, 0x27)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_426")

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
    testresult.append(["[.] Setze KL30 Spannung (ungültiger Bereich): 16V + 0,32V (2% Toleranz) + 0,03V (HiL Toleranz) = 16,656V",""])
    hil.vbat_cl30__V.set(16.656)

    # test step 5
    testresult.append(["[.] Schalte Kl.15 ein und starte RBS und warte bis erste NM Botschaft empfängt", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_e2e(allstate=1, sisft=1, otamc=1, oruA=1, ourD=1)
    result = func_nm.is_bus_started()
    testresult.append(result)

    # test step 6
    testresult.append(["[.] Warte 500ms (Fehlerqualifizierungszeit)", ""])
    time.sleep(.500)

    # test step 7
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc, ticket_id="EGA-PRM-296"))

    # test step 8
    testresult.append(["[.]   Setze Kl.30 Spannung zurück auf 13 V", ""])
    hil.vbat_cl30__V.set(13)

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[-] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=True)