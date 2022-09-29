# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : ORUnext_Preconditions_Vehicle_Speed.py
# Title   : ORUnext_Preconditions_Vehicle_Speed
# Task    : ORUnext Preconditions in Vehicle Speed
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
# 1.1  | 25.04.2022 | Mohammed     | Reworked
# 1.3  | 23.05.2022 | Mohammed     | Aktualisiert  Vorbedingungen
# ******************************************************************************

# ******************************************************************************


from _automation_wrapper_ import TestEnv # @UnresolvedImport
import functions_gearselection
import time
from ttk_checks import basic_tests

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
    testresult.setTestcaseId("TestSpec_302")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Setze VDSO_Vx3d auf (8 km/h)", ""])
    func_gs.setVelocity_kmph(8)

    # test step 2-2.4
    testresult.append(["[.] Setze ungulitige ORUnext Precondition", ""])
    testresult.append(["[+] Setze OTAMC_D_01 auf VPE_none", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze ORU_CONTROL_A auf  PREPARATION ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(2)
    testresult.append(["[.] Setze ORU_CONTROL_D auf PREPARATION ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(2)
    tMSG_CYCLE = 0.5  # sec
    testresult.append(["[.] Warte 500ms (tMSG_CYCLE) ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 3-3.2
    testresult.append(["[.] Auslesen DID: 0xF1F2 (KL30 Signal Read)", ""])
    # res, verdict = canape_diag.sendDiagRequest([0x22, 0xF1, 0xF2])
    # testresult.append(["\xa0 raw output from DID F1F2 %s -" % (res), ""])
    # testresult.append(["\xa0 voltage = %s mV -" % (int(hex((res[3] << 8) | res[4]), 16)), "PASSED"])
    # testresult.append(["[.] '%s' auslesen: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x22] + [0xF1, 0xF2]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["[+] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Prüfe Voltage : 13-16 V", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.vbat_cl30__V.get(),  # letzer Sendetimestamp
            min_value=6.0,
            max_value=16.0,
            descr="Check that value is in range"
        )
    )
    testresult.append(["[-0]", ""])

    # test step 4-4.1
    testresult.append(["[.] Auslesen DID: 0xF1F3 (Temeprature Sensor Read)", ""])
    #res, verdict = canape_diag.sendDiagRequest([0x22, 0xF1, 0xF3])
    #testresult.append(["\xa0 Prüfe Temeprature zwischen -40 to 90 Grad = %s degree" % (int(hex(res[3]), 16)), "INFO"])
    request = [0x22] + [0xF1, 0xF3]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(["[+] Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))
    testresult.append(["[-0]", ""])

    # test step 5
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 6
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 7
    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)
    testresult.append(["\xa0Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))

    # test step 8-8.10
    testresult.append(["[.] Setze gulitige ORUnext Vorbedingungen", ""])
    hil.vbat_cl30__V.set(13.0)
    testresult.append(["[+] Setze VDSO_Vx3d auf (<+/-5 km/h)", ""])
    testresult.append(func_gs.setVelocity_kmph(0))
    testresult.append(["[.] Setze Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))
    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append(["[.] Setze Kein CRC und BZ Fehler ", ""])
    testresult.append(["[.] Setze Kein E2E Timeout ", ""])
    testresult.append(["[.] Setze OTAMC_D_01 auf VPE_none", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze ORU_CONTROL_A auf  RUNNING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_CONTROL_D auf RUNNING ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    tMSG_CYCLE = 0.5  # sec
    testresult.append(["[.] Warte tMSG_CYCLE: 500ms ", ""])
    time.sleep(tMSG_CYCLE)
    testresult.append(["[-0]", ""])

    # test step 9
    testresult.append(["[.] Wechsel in default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    # test step 10
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 11
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 12
    testresult.append(["[.] Lese aktuelle Diagnose Session aus und warte 2 Sekunde", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))
    time.sleep(2)

    # test step 13
    testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming', ticket_id='FehlerID:EGA-PRM-226'))

    # test step 14
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