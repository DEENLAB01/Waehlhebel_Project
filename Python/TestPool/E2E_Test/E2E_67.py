# ******************************************************************************
# -*- coding: latin1 -*-
# File    : E2E_67.py
# Title   : OTAMC_D_Timeout_Init
# Task    : Erstmalige Timeout-Fehlererkennung OTAMC_D_01 während "Initialized"
#
# Author  : Devangbhai Patel
# Date    : 31.07.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 31.07.2022 | Devangbhai   | initial
# 1.1  | 05.08.2022 | Devangbhai   | Added Ticket ID
# 1.2  | 19.08.2022 | Devangbhai   | Added correct Precondition
# 1.3  | 31.08.2022 | Devangbhai   | Rework according to new specification
# 1.4  | 05.09.2022 | Devangbhai   | Added Ticket ID



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


def checkProgrammingPrecondition(exp_content, ticket_id = None):
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

    testresult.append(["[+] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, 4))

    # test step
    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    if exp_content:
        testresult.append(_checkStatus(meta(len(response[4:]),
                                            alias="Länge des Inhalts"),
                                       len(exp_content),
                                       descr="{} Element".format(len(exp_content)), ticket_id=ticket_id))
        if len(response[4:]) == len(exp_content):
            testresult.append(_compare(meta(response[4:],
                                            alias="Inhalt"),
                                       "==",
                                       meta(exp_content,
                                            alias="Erwarteter Inhalt"),
                                       descr="Inhalt der Response", ticket_id=ticket_id))
        else:
            testresult.append(['Inhalt der Response kann nicht verglichen werden.', 'FAILED'])
    else:
        testresult.append(_checkStatus(meta(len(response[4:]),
                                            alias="Länge des Inhalts"),
                                       0,
                                       descr="Kein Inhalt - Liste leer", ticket_id=ticket_id))



# Instantiate test environment
testenv = TestEnv()

aktiv_dtc = [(0xE00109, 0x27)]
passiv_dtc = [(0xE00109, 0x26)]

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

    # set Testcase ID #########################################################
    testresult.setTestcaseId("E2E_67")

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
                                             descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt", ))

    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])

    # test step 1 and 2
    testresult.append(["[.] Schalte Kl30 ein, setze OTAMC_D_01 Zykluszeit auf 0.", ""])
    testresult.append(["[.] Schaltle Kl15 ein und RBS an und warte bis erste NM Botschaft empfängt ", ""])
    hil.ClampControl_01__KST_KL_15__value.set(1)
    hil.cl15_on__.set(1)
    func_nm.hil_ecu_e2e(allstate=1, sisft=1, otamc=0, oruA=1, ourD=1)
    result = func_nm.is_bus_started()
    testresult.append(result)
    hil.Systeminfo_01__period.set(20)
    time.sleep(0.010)
    hil.Systeminfo_01__period.setState("an")

    # test step 2.1
    testresult.append(["[+]  warte 1500ms + 500ms+ Toleranz (Wechsel nach Initialized, Der initiale Timeout beträgt 1500ms + 500ms tDiagStart)", ""])
    time.sleep(1.500 + 0.500 + 0.100)

    # test step 3
    testresult.append(["[-] Programmiervorbedingungen prüfen: 0x3101 + {}".format(HexList(test_data['identifier'])), ""])
    checkProgrammingPrecondition(exp_content=[0xA7], ticket_id="EGA-PRM-290")

    # test step 4
    testresult.append(["[-] Lese Fehlerspeicher (0xE00109 DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc, ticket_id="EGA_PRM_273"))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[-] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=True)
