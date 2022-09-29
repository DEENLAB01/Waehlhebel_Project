# ******************************************************************************
# -*- coding: latin1 -*-
# File    : E2E_45.py
# Title   : ORU_Control_A_CRC_Error_SSP_Init
# Task    : Wiederholte Fehlererkennung ORU_Control_A und Wechsel nach "Safe State Permanent" aus "Initialized" über "Normal".
#
# Author  : Devangbhai Patel
# Date    : 29.07.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 29.07.2022 | Devangbhai   | initial
# 1.1  | 12.08.2022 | Devangbhai   | Changed the timing to 2.5s insted of 1.5s  in step 1.1
# 1.2  | 19.08.2022 | Devangbhai   | Added correct precondition,

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
from functions_nm import _checkStatus, _compare

import os

def checkProgrammingPrecondition(exp_content, ticket= None):
    """ Checks the programming precondition
    Parameters:
        exp_content - expected content as list of bytes
    Returns:
        None
    """
    # test step
    request = [0x31, 0x01] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, 4))

    # test step
    testresult.append(["\xa0 Prüfe Inhalt der Response", ""])
    if exp_content:
        testresult.append(_checkStatus(meta(len(response[4:]),
                                                       alias="Länge des Inhalts"),
                                                  len(exp_content),
                                                  descr="{} Element".format(len(exp_content)), ticket_id= ticket))
        if len(response[4:]) == len(exp_content):
            testresult.append(_compare(meta(response[4:],
                                                       alias="Inhalt"),
                                                  "==",
                                                  meta(exp_content,
                                                       alias="Erwarteter Inhalt"),
                                                  descr="Inhalt der Response",ticket_id= ticket))
        else:
            testresult.append(['Inhalt der Response kann nicht verglichen werden.', 'FAILED'])
    else:
        testresult.append(_checkStatus(meta(len(response[4:]), alias="Länge des Inhalts"), 0, descr="Kein Inhalt - Liste leer", ticket_id=ticket))
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

    aktiv_dtc = [(0xE0010D, 0x27)]
    passiv_dtc = [(0xE0010D, 0x26)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("E2E_45")

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

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])

    # test step 1
    testresult.append(["[.]  Schalte Kl.30 ein und starte RBS  warte bis erste NM Botschaft empfängt. ", ""])
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_e2e(allstate=1, sisft=1, otamc=1, oruA=1, ourD=1)
    result = func_nm.is_bus_started()
    testresult.append(result)

    # test step 1.1
    testresult.append(["[+]  Warte 2500ms. (Wechsel nach Normal State)", ""])
    time.sleep(2.500)

    # test step 2
    testresult.append(["[-] Programmiervorbedingungen prüfen: 0x3101 + {}".format(HexList(test_data['identifier'])),""])
    checkProgrammingPrecondition(exp_content=[])

    # test step 3
    testresult.append(["[.] Sende einmal CRC-Error für ORU_Control_A_01_CRC. (Wechsel nach  Safe State)", ""])
    sec = 0.300
    timeout = sec + t()
    while timeout > t():
        ORUA_timestamp = hil.ORU_Control_A_01__timestamp.get()
        hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0)
        hil.ORU_Control_A_01__period.setState("an")
        new_timestamp = hil.ORU_Control_A_01__timestamp.get()
        if ORUA_timestamp != new_timestamp:
            break

    # test step 4
    testresult.append(["[.] Warte 500ms", ""])
    time.sleep(0.500)

    # test step 5
    testresult.append(["[.] Programmiervorbedingungen prüfen: 0x3101 + {}".format(HexList(test_data['identifier'])), ""])
    checkProgrammingPrecondition(exp_content=[0xA7], ticket="EGA_PRM_280")

    # testresult.append(["Wechsel in Extended Session: 0x1003", "INFO"])
    # testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))
    # testresult.append(["Wechsel in Programming Session : 0x1002", "INFO"])
    # testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))
    # testresult.append(["Wechsel in Extended Session: 0x1003", "INFO"])
    # testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # test step 6
    testresult.append(["[.] Sende Zweite CRC-Error für ORU_Control_A_01_CRC. (Wechsel nach  Safe State permanant)", ""])
    sec = 0.400
    timeout = sec + t()
    while timeout > t():
        ORUA_timestamp = hil.ORU_Control_A_01__timestamp.get()
        hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0)
        new_timestamp = hil.ORU_Control_A_01__timestamp.get()
        if ORUA_timestamp != new_timestamp:
            break

    # test step 7
    testresult.append(["[.] Warte 220ms (FehlerReaktionZeit)", ""])
    time.sleep(0.220)

    # test step 8
    testresult.append(
        ["[.] Programmiervorbedingungen prüfen: 0x3101 + {}".format(HexList(test_data['identifier'])), ""])
    checkProgrammingPrecondition(exp_content=[0xA7])

    # test step 9
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[-] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=True)