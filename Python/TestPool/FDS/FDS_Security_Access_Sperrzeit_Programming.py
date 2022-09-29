# ******************************************************************************
# -*- coding: latin1 -*-
# File    : FDS_Security_Access_Sperrzeit_Programming.py
# Title   : FDS Security Access Sperrzeit in Programming Session
# Task    : FDS Security Access Sperrzeit in Programming Session
#
# Author  : Mohammed Abdul Karim
# Date    : 24.03.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 24.03.2022 | Mohammed     | initial
# 1.1  | 28.04.2022 | Mohammed     | Reworked
# 1.2  | 04.08.2022 | Mohammed     | Aktualisiert  Vorbedingungen
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import time
from functions_diag import HexList  # @UnresolvedImport
from ttk_checks import basic_tests
import functions_gearselection

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_385")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    # Initialize variables ####################################################

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    testresult.append(["[.] Waehlhebelposition P aktiviert ", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    testresult.append(["[.] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 1 (VPE_PRODUCTION)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 0 (IDLE)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 0 (IDLE)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 2
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 3
    testresult.append(["[.] Lese aktuelle Extended Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 4
    testresult.append(["[.] Wechsel in Programming Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))

    # test step 5
    testresult.append(["[.] Lese aktuelle Extended Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # test step 6
    testresult.append(["[.] Seed anfragen: 0x2711", ""])
    seed, result= canape_diag.requestSeed(special=True)
    testresult.extend(result)
    wrong_key = [0x10, 0xA3, 0x1B, 0x03]

    # test step 6.1
    testresult.append(["\x0a Key berechnen", ""])
    key_calculated, ver = canape_diag.calculateKey(seed)
    testresult.extend(ver)

    # test step 7
    if key_calculated!= wrong_key:
        testresult.append(["[.] Falschen Key senden: 0x2712 + <wrong key 1> "])
        verdict, res4 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x35, special=True)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2735", ""])
        testresult.append(res4)
    else:
        testresult.append(["[.] Falschen Key senden: 0x2712 + <wrong key 1>"])
        verdict, res4 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x35, special=True)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2735", ""])
        testresult.append(res4)

    # test step 8
    testresult.append(["[.] Seed anfragen: 0x2711"])
    seed, result= canape_diag.requestSeed(special=True,ticket_id='188')
    testresult.append(["\xa0 Prüfe Positive Response: 0x6711 + <seed 2> ist", ""])
    testresult.extend(result)

    wrong_key = [0x10, 0xA3, 0x1B, 0x04]
    testresult.append(["\x0a Key berechnen", ""])
    key_calculated, ver = canape_diag.calculateKey(seed)
    testresult.extend(ver)

    # test step 9
    if key_calculated != wrong_key:
        testresult.append(["[.] Falschen Key senden: 0x2712 + <wrong key 2> "])
        verdict, res5 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x36, special=True)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2736", ""])
        testresult.append(res5)
    else:
        testresult.append(["[.] Falschen Key senden: 0x2712 + <wrong key 2>"])
        verdict, res5 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x36, special=True)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2736", ""])
        testresult.append(res5)

    # test step 10
    testresult.append(["[.] Seed anfragen: 0x2711"])
    seed, result= canape_diag.requestSeed(pos_response=False, exp_nrc=0x37, special=True)
    testresult.append(["\x0aPrüfe Negative Response: 0x7F2737", ""])
    testresult.extend(result)

    wrong_key = [0x10, 0xA3, 0x1B, 0x05]
    testresult.append(["\x0a Key berechnen", ""])
    key_calculated, ver = canape_diag.calculateKey(seed)
    testresult.extend(ver)

    # test step 11
    if key_calculated != wrong_key:
        testresult.append(["[.] Falschen Key senden: 0x2712 + <wrong key 3> "])
        verdict, res6 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x24, special=True)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2724", ""])
        testresult.append(res6)
    else:
        testresult.append(["[.] Falschen Key senden: 0x2712 + <wrong key 3>"])
        verdict, res6 = canape_diag.sendKey(wrong_key, pos_response=False, exp_nrc=0x37, special=True)
        testresult.append(["\x0aPrüfe Negative Response: 0x7F2724", ""])
        testresult.append(res6)

    # test step 12
    testresult.append(["\xa0Zugriffsversuch während Sperrzeit:"])
    testresult.append(["[.] Warte 5 Minute"])
    time.sleep(300)

    # test step 13
    testresult.append(["[.] Seed anfragen: 0x2711", ""])
    seed, result = canape_diag.requestSeed(pos_response=False, exp_nrc=0x37, special=True)
    testresult.append(["Prüfe Negative Response: 0x7F277F", ""])
    testresult.extend(result)

    # test step 14
    testresult.append(["\xa0Zugriffsversuch während Sperrzeit:"])
    testresult.append(["[.] Warte 5 Minute + 30 Sekunde"])
    time.sleep(330)

    # test step 15
    testresult.append(["[.] Wechsel in Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # test step 16
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 17
    testresult.append(["[.] Wechsel in extended Session:  0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 17.1
    testresult.append(["[+] Warte 1 Sekunde ", ""])
    time.sleep(1)

    # test step 17.2
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))
    testresult.append(["[-0]", ""])

    # test step 18
    testresult.append(["[.] Wechsel in Programming Session:  0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming', ticket_id='Fehler-Id: EGA-PRM-188'))

    # test step 18.1
    testresult.append(["[+] Warte 1 Sekunde ", ""])
    time.sleep(1)

    # test step 18.2
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming', ticket_id='Fehler-Id: EGA-PRM-188'))
    testresult.append(["[-0]", ""])

    # test step 19
    testresult.append(["[.] Seed anfragen: 0x2711"])
    seed1, result = canape_diag.requestSeed(special=True)
    testresult.append(["\xa0 Prüfe Positive Response: 0x6711 + <seed> ist", ""])
    testresult.extend(result)

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print ("Done.")
