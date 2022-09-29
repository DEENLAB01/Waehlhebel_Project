# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Read_Ambient_data_with_service_ID19hex_SiShift_01.py
# Title   : Read_Ambient_data_with_service_ID19hex_Sishift_01
# Task    : Read Ambient data of dtc with 1906 SiShift_01
#
# Author  : Mohammed Abdul Karim
# Date    : 07.04.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 07.04.2022 | Mohammed     | initial
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
    func_hil = functions_hil.FunctionsHil(testenv, hil)

    # Initialize variables ####################################################

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_377X")

    # TEST PRE CONDITIONS #####################################################
    request = [0x19, 0x06, 0xE0, 0x01, 0x01, 0x01]
    exp_value = [[0x27, 0x06, 0x01], [0x28, 0x000050, 0x002B20F246], [0x01, 0x00, 0x01]]
    parameter_name = [['StatusOfDTC', 'DTCPriority', 'OCC'],
                      ['Aging_counter', 'Km-Mileage', 'Timestamp'],
                      ['Trip_counter', 'Healing_counter', 'Confirmation_Threshold']]
    set_value_list = [80, 15, 9, 6, 10, 12, 16]
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))

    testresult.append(["[.] setting up the following values"
                       "\nKilometerstand = %s \nStunde = %s \nMinute = %s \nSekunde = %s"
                       "\nJahr = %s \nMonat = %s \nTag = %s"
                       % (set_value_list[0], set_value_list[1], set_value_list[2], set_value_list[3],
                          set_value_list[4], set_value_list[5], set_value_list[6]), ""])
    hil.Diagnose_01__DW_Kilometerstand__value.set(set_value_list[0])
    hil.Diagnose_01__UH_Stunde__value.set(set_value_list[1])
    hil.Diagnose_01__UH_Minute__value.set(set_value_list[2])
    hil.Diagnose_01__UH_Sekunde__value.set(set_value_list[3])
    hil.Diagnose_01__UH_Jahr__value.set(set_value_list[4])
    hil.Diagnose_01__UH_Monat__value.set(set_value_list[5])
    hil.Diagnose_01__UH_Tag__value.set(set_value_list[6])

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    for loop in range(2):
        testresult.append(["[.] disabled SiShift_01 PDU", ""])
        hil.SiShift_01__period.set(0)
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

        testresult.append(["[.] DTCExtendedDataRecordNumber 0X02 ", ""])
        request[-1] = 2
        [response, result] = canape_diag.sendDiagRequest(request)
        testresult.append(result)
        testresult.append(["Empfangene Response: %s" % str(HexList(response)), ""])
        testresult.extend(canape_diag.analysisExtendedDataRecordResponse(response, exp_value[1], parameter_name[1]))

        if loop == 1:
            testresult.append(["[.] Switch KL 15 OFF and ON with Delay ", ""])
            hil.ClampControl_01__KST_KL_15__value.set(0)
            time.sleep(.200)
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

        testresult.append(["[.] Enabled SiShift_01 PDU", ""])
        hil.SiShift_01__period.set(20)
        time.sleep(1)

    testresult.append(["[+0]", ""])
    testresult.append(["[-] Lösche Fehlerspeicher", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

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
