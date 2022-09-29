# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : BC_check_service_ID11hex.py
# Title   : BC check for service  ID11hex
# Task    : BC check for service ID11hex
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
# 1.1  | 24.03.2022 | Mohammed     | Added Fehler ID
# 1.1  | 31.03.2022 | M.A. Mushtaq | reworked on test
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

    request = [0x11, 0x02]
    geschwindigkeit = [0, 0, 5, 5]
    PropulsionSystemActive = [0, 1, 0, 1]
    # exp_wrong_prec = [0x05]
    PropulsionSystemActive_switch = hil.OBD_04__MM_PropulsionSystemActive__value
    # Q-LAH_80124-10260,Q-LAH_80124-9017,Q-LAH_80124-9018,Q-LAH_80124-9296
    # set Testcase ID #####################################################BC_for_service_ID11Hex.py####
    testresult.setTestcaseId("TestSpec_374")

    # TEST PRE CONDITIONS #####################################################

    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()

    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])
    for i in range(4):

        testresult.append(["[.] VDSO_Vx3d = %s km/h" %(geschwindigkeit[i]), ""])
        testresult.append(func_gs.setVelocity_kmph(geschwindigkeit[i]))
        time.sleep(2.5)  # wait 2 second

        testresult.append(["[.] PropulsionSystemActive_switch = %s " %(PropulsionSystemActive[i]), ""])
        PropulsionSystemActive_switch.set(PropulsionSystemActive[i])
        time.sleep(0.330) # added time sleep of 1 cycle time.

        [response, result] = canape_diag.sendDiagRequest(request)
        testresult.append(result)
        testresult.append(["Empfangene Response: %s" % str(HexList(response)), ""])

        if i == 0 or i == 2:
            testresult.append(["\xa0Auf positive Response überprüfen", ""])
            descr, verdict = canape_diag.checkPositiveResponse(response, request, 2)
            testresult.append([descr, verdict])
            time.sleep(3)
        else:
            testresult.append(["\xa0Auf positive Response überprüfen", ""])
            descr, verdict = canape_diag.checkPositiveResponse(response, request, 2)
            testresult.append([descr, verdict])

            #testresult.append(canape_diag.checkNegativeResponse(response, [0x11], 0x22, ticket_id='FehlerId: EGA-PRM-181'))

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
