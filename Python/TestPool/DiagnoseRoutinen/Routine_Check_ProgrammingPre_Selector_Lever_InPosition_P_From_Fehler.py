# *****************************************************************************
# -*- coding: latin-1 -*-
# File    : Routine_Check_ProgrammingPre_Selector_Lever_InPosition_P_From_Fehler.py
# Title   : Routine CheckProgrammingPre SelectorLever InPosition P From Fehler
# Task    : Test for Routine Diagnosejob 0x3101 0x0203
#
# Author  : Mohammed Abdul Karim
# Date    : 29.09.2021
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 28.09.2021 | Mohammed     | initial
# 1.1  | 12.10.2021 | Mohammed     | Added TestSpec ID
# 1.2  | 24.11.2021 | Mohammed     | Rework
# 1.3  | 10.01.2022 | H. Förtsch   | reworked test script by test spec
# 1.4  | 10.01.2022 | Mohammed     | Corrected exp_wrong_prec value
# 1.5  | 14.04.2022 | Mohammed     | Added Zykluszeit
# 1.6  | 24.05.2022 | Mohammed     | Aktualisiert  Vorbedingungen
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
from ttk_base.values_base import meta

from diag_identifier import identifier_dict
from functions_diag import HexList
import functions_gearselection
import time

# pylint: disable=invalid-name

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
    testresult.setTestcaseId("TestSpec_266")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    test_data = identifier_dict['Check Programming Preconditions']
    exp_wrong_prec = [0xA5]

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
    testresult.append(["[.] Lese aktuelle Diagnose Session aus und warte 2 Sekunde", ""])
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
    #time.sleep(1)
    # test steps 6 and 7
    checkProgrammingPrecondition(exp_content=[])

    # test step 8
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    # test step 9
    testresult.append(["[.] Lese aktuelle Factory Mode aus", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))
    #time.sleep(1)
    # test steps 10 and 11
    checkProgrammingPrecondition(exp_content=[])

    # test step 12
    testresult.append(["[.] Setze SiShift_01:SIShift_StLghtDrvPosn = Fehler", ""])
    testresult.append(func_gs.changeDrivePosition('Fehler'))

    testresult.append(["\x0a[12.1] Warte 2 Sekunde", ""])
    time.sleep(2)

    # test step 13
    testresult.append(["[.] Wechsel in Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

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
