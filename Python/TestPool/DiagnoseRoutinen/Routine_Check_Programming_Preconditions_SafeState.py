# *****************************************************************************
# -*- coding: latin-1 -*-
# File    : Routine_Check_Programming_Preconditions_SafeState.py
# Title   : Routine Check Programming Preconditions SafeState
# Task    : Test for Routine Diagnosejob 0x3101 0x0203
#
# Author  : Mohammed Abdul Karim
# Date    : 30.06.2022
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 30.06.2021 | Mohammed     | initial
# 1.1  | 04.07.2021 | Mohammed     | Added ECU_Sleep -> ECU_WakeUp
# 1.2  | 16.08.2021 | Mohammed     | Rework
# *****************************************************************************

# Imports #####################################################################

from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
from ttk_base.values_base import meta

from diag_identifier import identifier_dict
from functions_diag import HexList
import functions_gearselection
from time import time as t
import time

# #############################################################################
def checkProgrammingPrecondition(exp_content):
    """ Checks the programming precondition
    Parameters:
        exp_content - expected content as list of bytes
    Returns:
        None
    """
    # test step
    testresult.append(["[.] Programmiervorbedingungen prüfen: 0x3101 + {}"
                       .format(HexList(test_data['identifier'])),
                       ""])
    request = [0x31, 0x01] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, 4))

    # test step
    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    if exp_content:
        testresult.append(basic_tests.checkStatus(meta(len(response[4:]),
                                                       alias="Länge des Inhalts"),
                                                  len(exp_content),
                                                  descr="{} Element".format(len(exp_content))))
        if len(response[4:]) == len(exp_content):
            testresult.append(basic_tests.compare(meta(response[4:],
                                                       alias="Inhalt"),
                                                  "==",
                                                  meta(exp_content,
                                                       alias="Erwarteter Inhalt"),
                                                  descr="Inhalt der Response"))
        else:
            testresult.append(['Inhalt der Response kann nicht verglichen werden.', 'FAILED'])
    else:
        testresult.append(basic_tests.checkStatus(meta(len(response[4:]),
                                                       alias="Länge des Inhalts"),
                                                  0,
                                                  descr="Kein Inhalt - Liste leer"))

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_259")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    test_data = identifier_dict['Check Programming Preconditions']
    exp_wrong_prec = [0xA7]
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    wh_fahrstufe_fehlerwert = 15
    allowed_fahrstufe = [4, 5, 6, 7]  # Nicht betigt, D, N, R

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))

    testresult.append(["[.] VDSO_Vx3d = 32766 (0 km/h)",""])
    testresult.append(func_gs.setVelocity_kmph(0))

    testresult.append(["[.] Setze MM_PropulsionSystemActive auf 0", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append(["[.] Setze OTAMC_D_01 setze auf VPE_NONE", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze ORU_CONTROL_A auf RUNNING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_CONTROL_D auf  RUNNING ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    testresult.append(["[.] Warte Zykluszeit", ""])
    time.sleep(0.500)

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Lese aktuelle Diagnose Session aus und Warte 2 Sekunde", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))
    time.sleep(2)

    # test step 2 and 3
    checkProgrammingPrecondition(exp_content=[])

    # test step 4
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 5
    testresult.append(["[.] Lese aktuelle Extended Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test steps 6 and 7
    checkProgrammingPrecondition(exp_content=[])

    # test step 8
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    # test step 9
    testresult.append(["[.] Lese aktuelle Factory Mode aus", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test steps 10 and 11
    checkProgrammingPrecondition(exp_content=[])

    # test step 12
    sec = 0.500
    timeout = sec + t()
    testresult.append(["[.] Sende zweite CRC-Fehler für ORU_Control_A::ORU_Control_A_CRC", ""])
    while timeout > t():
        hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0)

    testresult.append(["[+] Warte für 220ms (FR=Fehlerreaktionszeit) + 10ms Toleranz", ""])
    time.sleep(0.230)

    # testresult.append(["[.] Sende Erste SiShift-CRC Fehler ", ""])
    # sec = 0.019
    # timeout = sec + t()
    # hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)
    # while timeout > t():
    #     hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)
    #
    # testresult.append(["[+] Warte 20ms Sekunde", ""])
    # time.sleep(0.020)
    #
    # testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    # current_fahrstufe = wh_fahrstufe.get()
    # testresult.append(
    #     basic_tests.contains(
    #         defined_values=current_fahrstufe,
    #         current_value=wh_fahrstufe_fehlerwert,
    #         descr="Prüfe Waehlhebel_04:WH_Fahrstufe = 15"
    #     )
    # )
    #
    # testresult.append(["[.] Sende Zweite SiShift-CRC Fehler", ""])
    # sec = 0.019
    # timeout = sec + t()
    # hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)
    # while timeout > t():
    #     hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)
    # testresult.append(["[+] Warte 20ms Sekunde", ""])
    # time.sleep(0.020)
    #
    # testresult.append(["[.] Warte 2 Sekunde", ""])
    # time.sleep(2)
    # #
    # testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    # current_fahrstufe = wh_fahrstufe.get()
    # testresult.append(
    #     basic_tests.contains(
    #         defined_values=current_fahrstufe,
    #         current_value=wh_fahrstufe_fehlerwert,
    #         descr="Prüfe Waehlhebel_04:WH_Fahrstufe = 15"
    #     )
    # )
    testresult.append(["[-0]", ""])

    # test step 13
    testresult.append(["[.] Wechsel in Default Session: 0x1001 und warte 2 Sekunde", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))
    time.sleep(2)

    # test step 14
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test steps 15 and 16
    checkProgrammingPrecondition(exp_content=exp_wrong_prec)

    # test step 17
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 18
    testresult.append(["[.] Lese aktuelle Extended Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test steps 19 and 20
    checkProgrammingPrecondition(exp_content=exp_wrong_prec)

    # test step 21
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    # test step 22
    testresult.append(["[.] Lese aktuelle Factory Mode aus", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test steps 23 and 24
    checkProgrammingPrecondition(exp_content=exp_wrong_prec)

    # test steps 25
    testresult.append(["[.] Führe erneuten OP-PowerCycle (ECU_Sleep -> ECU_WakeUp) durch, um SafeState zu verlassen", ""])
    hil.cl15_on__.set(0)
    time.sleep(.200)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(20)

    testresult.append(["[+] Prüfe Ruhestrom während ECU_Sleep", ""])
    testresult.append(basic_tests.checkRange(value=hil.cc_mon__A,
                                             min_value=0.0,  # 0mA
                                             max_value=0.006,  # 6mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt", ))

    testresult.append(["[.] Warte 2 s nach WakeUp", ""])
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(2)
    testresult.append(["[-0]", ""])

    # test step 26
    testresult.append(["[.] Lese aktuelle Diagnose Session aus und Warte 2 Sekunde", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))
    time.sleep(2)

    checkProgrammingPrecondition(exp_content=[])

    # testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    # current_fahrstufe = wh_fahrstufe.get()
    # testresult.append(
    #     basic_tests.contains(
    #         defined_values=allowed_fahrstufe,
    #         current_value=current_fahrstufe,
    #         descr="Prüfe Waehlhebel_04:WH_Fahrstufe = 4"
    #     )
    # )

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup #################################################################
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

print "Done."
