# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : BC_check_service_ID10hex.py
# Title   : BC check for service  ID10hex
# Task    : BC check for service ID10hex
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
# 1.1  | 29.03.2022 | M.A. Mushtaq | Update according to test spec
# 1.2  | 16.08.2022 | Mohammed     | Update Precondition
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

    # testenv.startupECU()  # startup before cal vars are called
    # canape_diag = testenv.getCanapeDiagnostic()
    func_hil = functions_hil.FunctionsHil(testenv, hil)

    # Initialize variables ####################################################

    request = [[0x10, 0x03], [0x10, 0x02], [0x10, 0x01]]
    geschwindigkeit = [0, 0, 5, 5]
    PropulsionSystemActive = [0, 1, 0, 1]
    sig_str = ['Valid', 'Invalid', 'Valid', 'Invalid']
    # exp_wrong_prec = [0x05]
    PropulsionSystemActive_switch = hil.OBD_04__MM_PropulsionSystemActive__value
    # Q-LAH_80124-10260,Q-LAH_80124-9017,Q-LAH_80124-9018,Q-LAH_80124-9296
    # set Testcase ID #####################################################BC_for_service_ID11Hex.py####
    testresult.setTestcaseId("TestSpec_373")

    # TEST PRE CONDITIONS #####################################################

    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()

    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    #testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 0 (VPE_None)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 4 (RUNNING)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 4 (RUNNING)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])
    for i in range(4):

        testresult.append(["[.] Wechsel in Default Session: 0x1001", ""])
        [response, result] = canape_diag.sendDiagRequest(request[2])
        testresult.append(result)
        testresult.append(["Empfangene Response: %s" % str(HexList(response)), ""])
        testresult.append(["\xa0Auf positive Response überprüfen", ""])
        descr, verdict = canape_diag.checkPositiveResponse(response, request[2], 2)
        testresult.append([descr, verdict])

        testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
        [response, result] = canape_diag.sendDiagRequest(request[0])
        testresult.append(result)
        testresult.append(["Empfangene Response: %s" % str(HexList(response)), ""])
        testresult.append(["\xa0Auf positive Response überprüfen", ""])
        descr, verdict = canape_diag.checkPositiveResponse(response, request[0], 2)
        testresult.append([descr, verdict])

        testresult.append(["[.] Set %s Boundary Check Signals" %(sig_str[i]), ""])

        testresult.append(func_gs.setVelocity_kmph(geschwindigkeit[i]))
        time.sleep(2.5)  # wait 2 second

        testresult.append(["PropulsionSystemActive_switch = %s " %(PropulsionSystemActive[i]), "INFO"])
        PropulsionSystemActive_switch.set(PropulsionSystemActive[i])
        time.sleep(0.330)  # added time sleep of 1 cycle time.

        testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
        [response, result] = canape_diag.sendDiagRequest(request[1])
        testresult.append(result)
        testresult.append(["Empfangene Response: %s" % str(HexList(response)), ""])

        if i == 0 or i==2:
            testresult.append(["\xa0Auf positive Response überprüfen", ""])
            descr, verdict = canape_diag.checkPositiveResponse(response, request[1], 2)
            testresult.append([descr, verdict])
            #time.sleep(3)
        else:
            testresult.append(["\xa0Auf negative Response überprüfen", ""])
            testresult.append(canape_diag.checkNegativeResponse(response, [0x10], 0x22))

    testresult.append(["[.] Wechsel in Default Session: 0x1001", ""])
    [response, result] = canape_diag.sendDiagRequest(request[2])
    testresult.append(result)
    testresult.append(["Empfangene Response: %s" % str(HexList(response)), ""])
    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    descr, verdict = canape_diag.checkPositiveResponse(response, request[2], 2)
    testresult.append([descr, verdict])

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
