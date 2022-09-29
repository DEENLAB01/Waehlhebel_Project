# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : ORUnext_SesionWechseln_inISO_Frequenz.py
# Title   : ORUnext_SesionWechseln_inISO_Frequenz
# Task    : ORUnext Session Wechseln in ISO Frequenz

# Author  : Mohammed Abdul Karim
# Date    : 23.05.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 23.05.2022 | Mohammed  | initial
# 1.1  | 15.08.2022 | Mohammed  | Added TestStep 12
# ******************************************************************************
# must be ISO CANID!

from _automation_wrapper_ import TestEnv  # @UnresolvedImport
import functions_gearselection
from ttk_checks import basic_tests
import time

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################

    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_399")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: KL30 an und KL15 aus", ""])
    testenv.startupECU()
    # hil.cl30_on__.set(1)
    # hil.cl15_on__.set(0)

    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Setze OBD_Driving_Cycle auf 1", ""])
    hil.OBD_03__OBD_Driving_Cycle__value.set(1)

    # test step 2-2.5
    testresult.append(["[.] Setze ungülitige  ORUnext Vorbedingungen", ""])
    testresult.append(["[+] Setze OTAMC_D_01 auf VPE_None", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze ORU_CONTROL_A auf PREPARATION ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(2)
    testresult.append(["[.] Setze ORU_CONTROL_D auf  PREPARATION ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(2)
    testresult.append(["[.] Warte 1 Sekunde ", ""])
    time.sleep(1)
    testresult.append(["[.] Setze ORU_CONTROL_A auf RUNNING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_CONTROL_D auf  RUNNING ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    tMSG_CYCLE = 0.5  # sec
    testresult.append(["[.] Warte tMSG_CYCLE: 500ms ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 3
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 4
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 5
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 6
    testresult.append(["[.] Setze vbat_cl30__V auf 13V", ""])
    hil.vbat_cl30__V.set(13.0)

    # test step 7
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # test step 8-8.10
    testresult.append(["[.] Setze gulitige ORUnext Vorbedingungen", ""])
    testresult.append(["[+] Setze vbat_cl30__V auf 13V ", ""])
    hil.vbat_cl30__V.set(13.0)
    testresult.append(["[.] Setze OTAMC_D_01 setze auf VPE_PRODUCTION", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_CONTROL_A auf IDLE ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_CONTROL_D auf  IDLE ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)
    testresult.append(["[.] Setze VDSO_Vx3d auf 0 km/h (37766)", ""])
    testresult.append(func_gs.setVelocity_kmph(0))
    testresult.append(["[.] Setze Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))
    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append(["[.] Setze Kein CRC und BZ Fehler ", ""])
    testresult.append(["[.] Setze Kein E2E Timeout ", ""])
    testresult.append(["[.] Warte tMSG_CYCLE:500ms ", ""])
    time.sleep(0.5)
    testresult.append(["[-0]", ""])

    # test step 9
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 10
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 11
    testresult.append(["[.] Warte 1 Sekunde", ""])
    time.sleep(1)

    # test step 12
    testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming', read_active_session=False))

    # test step 13
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.shutdownECU()
    testenv.breakdown()
    # #########################################################################