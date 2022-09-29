# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : BC_check_service_ID1906hex.py
# Title   : BC_check_service_ID1906hex
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
from ttk_checks import basic_tests
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

    # Q-LAH_80124-10260,Q-LAH_80124-9017,Q-LAH_80124-9018,Q-LAH_80124-9296
    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_NA")

    # TEST PRE CONDITIONS #####################################################
    request = [0x19, 0x06, 0xE0, 0x01, 0x04, 0x01]

    exp_value = [[0x27, 0x02, 0x01], [0x28, 0x02, 0x01], [0x01, 0x00, 0x01]]
    parameter_name = [['StatusOfDTC', 'DTCPriority', 'OCC'],
                      ['Aging_counter', 'Km-Mileage', 'Timestamp'],
                      ['Trip_counter', 'Healing_counter', 'Confirmation_Threshold']]

    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()

    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))

    hil.Diagnose_01__DW_Kilometerstand__value.set(80)
    hil.Diagnose_01__UH_Stunde__value.set(15)
    hil.Diagnose_01__UH_Minute__value.set(9)
    hil.Diagnose_01__UH_Sekunde__value.set(6)
    hil.Diagnose_01__UH_Jahr__value.set(10)
    hil.Diagnose_01__UH_Monat__value.set(12)
    hil.Diagnose_01__UH_Tag__value.set(16)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    for loop in range(2):
        testresult.append(["[.] disabled VDSO_05 PDU", ""])
        hil.VDSO_05__period.set(0)
        time.sleep(1)

        testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
        testresult.extend(canape_diag.checkDiagSession('default'))

        testresult.append(["[.] DTCExtendedDataRecordNumber 0X01", ""])
        request[-1] = 1

        [response, result] = canape_diag.sendDiagRequest(request)
        testresult.append(result)
        testresult.append(["Empfangene Response: %s" % str(HexList(response)), ""])
        exp_value[0][-1] += loop
        testresult.extend(canape_diag.analysisExtendedDataRecordResponse(response, exp_value[0], parameter_name[0]))

        testresult.append(["[.] DTCExtendedDataRecordNumber 0X02", ""])
        request[-1] = 2
        [response, result] = canape_diag.sendDiagRequest(request)
        testresult.append(result)
        testresult.append(["Empfangene Response: %s" % str(HexList(response)), ""])
        testresult.extend(canape_diag.analysisExtendedDataRecordResponse(response, exp_value[1], parameter_name[1]))

        if loop == 1:
            hil.ClampControl_01__KST_KL_15__value.set(0)
            time.sleep(.120)
            hil.ClampControl_01__KST_KL_15__value.set(1)
            time.sleep(2)
            exp_value[2][0] += 1
            exp_value[2][-1] += 1

        testresult.append(["[.] DTCExtendedDataRecordNumber 0X03", ""])
        request[-1] = 3
        [response, result] = canape_diag.sendDiagRequest(request)
        testresult.append(result)
        testresult.append(["Empfangene Response: %s" % str(HexList(response)), ""])
        testresult.extend(canape_diag.analysisExtendedDataRecordResponse(response, exp_value[2], parameter_name[2]))

        testresult.append(["[.] Enabled VDSO_05 PDU", ""])
        hil.VDSO_05__period.set(20)
        time.sleep(1)
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
