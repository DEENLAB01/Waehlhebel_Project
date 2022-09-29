# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : ORUnext_Preconditions_KL30.py
# Title   : ORUnext_Preconditions_KL30
# Task    : ORUnext Preconditions in KL30
#           
# Author  : M.A. Mushtaq
# Date    : 23.02.2022
# Copyright 2022 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 23.02.2022 | M.A. Mushtaq | initial
# 1.1  | 28.04.2022 | Mohammed     | initial
# 1.2  | 09.05.2022 | Mohammed     | Added Testschritte
# 1.3  | 05.07.2022 | Mohammed     | Added Fehler ID
# ******************************************************************************

# ******************************************************************************


from _automation_wrapper_ import TestEnv # @UnresolvedImport
import functions_hil
import data_common as dc
from diag_identifier import DIAG_SESSION_DICT
import functions_gearselection
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
    daq = testenv.getGammaDAQ()
    func_hil = functions_hil.FunctionsHil(testenv, hil)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    # Initialize variables ####################################################
    voltage_uv = dc.voltage_range['Undervoltage']
    set_voltage_invalid_uv = float(voltage_uv['voltage']) - float(voltage_uv['voltage']) * float(
    voltage_uv['tol_perc'] / 100.0) - float(voltage_uv['hil_tol_ma'])
    set_voltage_back_valid = float(dc.voltage_range['Normal']['voltage'])

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_292")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    time.sleep(5)

    Physical_ID = 0x1C400253
    response_CAN_ID= 0x1C420253
    Functional_req_CAN_ID = 0x1C410200

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Setze OBD_Driving_Cycle auf 1", ""])
    hil.OBD_03__OBD_Driving_Cycle__value.set(1)

    # test step 2
    testresult.append(["[.] Setze ungültige ORUnext Vorbedingungen", ""])
    testresult.append(["[+] Setze OTAMC_D_01 auf VPE_PRODUCTION", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_CONTROL_A auf  RUNNING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_CONTROL_D auf RUNNING ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    tMSG_CYCLE = 2  # sec
    testresult.append(["[.] Warte tMSG_CYCLE: 2s ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 3
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 4
    testresult.append(["[.] Lese aktuelle Extended Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 5
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    test_data = DIAG_SESSION_DICT['programming']
    request = test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["\xa0Überprüfen, Positive Response ", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request,exp_nrc=0x22))

    # test step 6
    testresult.append(["[.] Setze Spannung auf %sV (gültige Spannung)" % set_voltage_back_valid, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_back_valid)
    testresult.append([descr, verdict])

    # test step 7
    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(canape_diag.resetEventMemory())
    time.sleep(2)
    # test step 8
    testresult.append(["[.] Setze gültige ORUnext Vorbedingungen", ""])
    testresult.append(["[+] Setze OTAMC_D_01 auf VPE_none", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze ORU_CONTROL_A auf  RUNNING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_CONTROL_D auf RUNNING ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    testresult.append(["[.] Setze VDSO_Vx3d auf 0 km/h (37766)", ""])
    testresult.append(func_gs.setVelocity_kmph(0))
    testresult.append(["[.] Setze Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))
    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    tMSG_CYCLE = 2.0  # sec
    testresult.append(["[.] Warte tMSG_CYCLE: 2s ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 9
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 10
    testresult.append(["[.] Lese aktuelle Extended Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 11
    testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming', ticket_id='FehlerID:EGA-PRM-226'))

    # test step 12
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming', ticket_id='FehlerID:EGA-PRM-226'))

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