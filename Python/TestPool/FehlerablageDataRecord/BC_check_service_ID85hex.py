# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : BC_check_service_ID85hex.py
# Title   : BC check_service for ID85hex
# Task    : BC check_service for ID85hex
#
# Author  : M.A. Mushtaq
# Date    : 23.02.2022
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 23.02.2022 | M.A. Mushtaq | initial
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import functions_hil

import time
import functions_gearselection

from functions_diag import HexList  # @UnresolvedImport

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

    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()
    func_hil = functions_hil.FunctionsHil(testenv, hil)

    # Initialize variables ####################################################

    request = [[0x85, 0x02, 0xFF, 0xFF, 0xFF], [0x85, 0x01, 0xFF, 0xFF, 0xFF]]
    geschwindigkeit = [0, 0]
    PropulsionSystemActive = [0, 1]
    exp_wrong_prec = [0x05]
    PropulsionSystemActive_switch = hil.OBD_04__MM_PropulsionSystemActive__value
    # Q-LAH_80124-10260,Q-LAH_80124-9017,Q-LAH_80124-9018,Q-LAH_80124-9296
    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_376")

    # TEST PRE CONDITIONS #####################################################

    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    # #  ###############################################################
    # state = "aus"
    # hil.ORU_Control_A_01__period.setState(state)
    # hil.ORU_Control_D_01__period.setState(state)
    # hil.OTAMC_D_01__period.setState(state)
    # # ##########################################################

    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])
    for i in range(2):

        testresult.append(["[.] Wechsel in default Session: 0x1001", ""])
        testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

        testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
        testresult.extend(canape_diag.checkDiagSession('default'))

        testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
        testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

        testresult.append(["[.] Lese aktuelle Extended Session aus", ""])
        testresult.extend(canape_diag.checkDiagSession('extended'))

        testresult.append(["[.] VDSO_Vx3d = %s km/h" %(geschwindigkeit[i]), ""])
        testresult.append(func_gs.setVelocity_kmph(geschwindigkeit[i]))
        time.sleep(2)  # wait 2 second

        testresult.append(["[.] PropulsionSystemActive_switch = %s " %(i), ""])
        PropulsionSystemActive_switch.set(PropulsionSystemActive[i])
        time.sleep(.5)

        [response, result] = canape_diag.sendDiagRequest(request[0])
        testresult.append(result)
        testresult.append(["Empfangene Response: %s" % str(HexList(response)), ""])

        if i == 0:
            testresult.append(["[.] Auf positive Response überprüfen Mit Boundary Condition", ""])
            descr, verdict = canape_diag.checkPositiveResponse(response, request[0], 2)
            testresult.append([descr, verdict])
            [response, result] = canape_diag.sendDiagRequest(request[1])
            testresult.append(result)
        else:
            testresult.append(["[.] Auf negative Response überprüfen Mit falche Boundary Condition", ""])
            testresult.append(canape_diag.checkNegativeResponse(response, [0x85], 0x22))  # 0x7f2822

    testresult.append(["[.] reset back the changes", ""])
    [response, result] = canape_diag.sendDiagRequest(request[1])
    testresult.append(result)
    # TEST POST CONDITIONS ####################################################
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
