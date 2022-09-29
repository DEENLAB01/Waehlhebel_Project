# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_TesterPresent.py
# Title   : Diagnose Tester Present
# Task    : Tests if enable tester present is working correctly
#
# Author  : S. Stenger
# Date    : 21.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 21.05.2021 | StengerS     | initial
# 1.1  | 09.12.2021 | H. Förtsch   | reworked test script by test spec
# 1.3  | 28.01.2021 | Mohammed     | reworked test script after Adding preconditions
# 1.4  | 23.05.2022 | Mohammed     | Aktualisiert  Vorbedingungen
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import time
from data_common import s3_timeout
import functions_gearselection
# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_131")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    ############################
    hil.Diagnose_01__period.setState("aus")
    hil.NVEM_12__period.setState("aus")
    hil.Dimmung_01__period.setState("aus")
    hil.NM_Airbag__period.setState("aus")
    hil.OBDC_Funktionaler_Req_All_FD__period.setState("aus")
    hil.OBD_03__period.setState("aus")
    hil.Systeminfo_01__period.setState("aus")
    hil.NM_HCP1__period.setState("aus")
    hil.ORU_01__period.setState("aus")
    hil.OBDC_Waehlhebel_Req_FD__period.setState("aus")
    hil.OTAMC_01__period.setState("aus")
    hil.ISOx_Waehlhebel_Req_FD__period.setState("aus")
    hil.DIA_SAAM_Req__period.setState("aus")
    hil.ISOx_Funkt_Req_All_FD__period.setState("aus")
    hil.DPM_01__period.setState("aus")

    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    testresult.append(["[+] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 1 (VPE_PRODUCTION)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 0 (IDLE)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 0 (IDLE)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    #testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 2
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended', read_active_session=False))

    # test step 3
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 4
    testresult.append(["[.] Tester Present aktivieren", ""])
    canape_diag.enableTesterPresent()

    # test step 5
    testresult.append(["[.] Warte {} Sekunden (2 * S3 timeout)".format(2 * s3_timeout), ""])
    time.sleep(2 * s3_timeout)

    # test step 6
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 7
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming', read_active_session=False))

    # test step 8
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # test step 9
    testresult.append(["[.] Warte {} Sekunden (2 * S3 timeout)".format(2 * s3_timeout), ""])
    time.sleep(2 * s3_timeout)

    # test step 10
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('programming'))

    # test step 2
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default', read_active_session=False))

    # test step 3
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    del(testenv)
    # #########################################################################

print "Done."
