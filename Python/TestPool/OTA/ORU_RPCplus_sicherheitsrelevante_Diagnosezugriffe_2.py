# *****************************************************************************
# -*- coding: latin1 -*-
# File    : ORU_RPCplus_sicherheitsrelevante_Diagnosezugriffe_2.py
# Title   : OTA ORU_RPCplus sicherheitsrelevante Diagnosezugriffe 2
# Task    : A minimal "ORU_RPCplus_sicherheitsrelevante_Diagnosezugriffe_2!" test script
#
# Author  : Mohammed Abdul Karim
# Date    : 07.03.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 07.03.2022 | Mohammed     | initial
# 1.1  | 14.04.2022 | Mohammed     | Rework
# 1.2  | 10.05.2022 | Mohammed     | Added Testschritte
# 1.3  | 05.07.2022 | Mohammed | Added Fehler ID
# ******************************************************************************

# ******************************************************************************
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
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

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_347")
    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    test_data = identifier_dict['Active Diagnostic Session']

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: KL30 und KL15 an", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Setze  OTAMC_D_01.Setze VehicleProtectedEnvironment_D auf 0 (VPE_none)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)

    # test step 2
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 3
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 4
    testresult.append(["[.] Setze Signale ORU, OBD_04 und VDSO_05 Signale:", ""])
    testresult.append(["[+] Setze PropulsionSystemActive auf 0 (NotAktive)", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append(["[.] Setze VDSO_3d auf 0 km/h", ""])
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])
    testresult.append(["[.] Setze ORU_01_Status auf 4 (RUNNING)", ""])
    hil.ORU_01__ORU_Status__value.set(4)
    testresult.append(["[.] Setze RU_Control_A_01__OnlineRemoteUpdateControlA auf 4 (RUNNING)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze RU_Control_D_01__OnlineRemoteUpdateControlD auf 4 (RUNNING)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    testresult.append(["[-0]", ""])

    # test step 5
    testresult.append(["[.] Wartet 5100ms to fill buffer", ""])
    time.sleep(5.1)

    # test step 6
    testresult.append(["[.] Setze Signale ORU und OTAMC_D_1 Signale:", ""])
    testresult.append(["[+] Setze ORU_01_Status auf 0 (IDLE)", ""])
    hil.ORU_01__ORU_Status__value.set(0)
    testresult.append(["[.] Setze OTAMC_D_01::VehicleProtectedEnvironment_D auf 0 (VPE_aNone)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze RU_Control_A_01__OnlineRemoteUpdateControlA auf 0 (IDLE)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze RU_Control_D_01__OnlineRemoteUpdateControlD auf 0 (IDLE)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)
    testresult.append(["[.] Warte tMSG_CYCLE: 500ms", ""])
    time.sleep(0.500)
    testresult.append(["[-0]", ""])

    # test step 7
    testresult.append(["[.] Setze OTAMC_D_01::VehicleProtectedEnvironment_D= 2 (VPE_aftersales)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(2)

    # test step 8
    testresult.append(["[.] Warte Warte (cylcetime: 320ms und System Zeit: 5100ms)", ""])
    time.sleep(4.42)

    # test step 9
    testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming', ticket_id='FehlerID:EGA-PRM-226'))

    # test step 10
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming', ticket_id='FehlerID:EGA-PRM-226'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    del testenv
    # #########################################################################

print "Done."
