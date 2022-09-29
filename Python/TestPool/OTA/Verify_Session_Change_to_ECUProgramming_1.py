# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : Verify_Session_Change_to_ECUProgramming_1.py
# Title   : Verify_Session_Change_to_ECUProgramming_1
# Task    : A minimal "Diagnosejob 0x22 0xF1AB!" test script
#
# Author  : Mohammed Abdul Karim
# Date    : 29.04.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 29.04.2022 | Mohammed | initial
# 1.1  | 02.05.2022 | Mohammed | Reworked
# 1.2  | 25.05.2022 | Mohammed | Aktualisiert  Vorbedingungen
# 1.3  | 05.07.2022 | Mohammed | Added Fehler ID
# ******************************************************************************
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
from ttk_checks import basic_tests
import functions_gearselection
from functions_nm import _checkStatus
import time

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_360")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_common = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    diag_ident = identifier_dict['VW Logical Software Block Version']
    exp_sw_versions = {
        1: {'Block name': 'Bootloader', 'version': 187},
        2: {'Block name': 'Application', 'version': 111},
      #  3: {'Block name': 'Datensatz', 'version': None},
    }
    number_softwareblocks_n = len(exp_sw_versions)

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: KL30 an und KL15 aus", ""])
    testenv.startupECU()

    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    # test step 1
    testresult.append(["[.] Setze OTAMC_D_01 auf VPE_None", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)

    # test step 2
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 3
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 4
    testresult.append(["[.] Setze  ORU_Controls , ODB_04 und VDSO_3d Signale", ""])
    testresult.append(["[+] Setze vbat_cl30__V auf 13 ", ""])
    hil.vbat_cl30__V.set(13)
    #testresult.append(["[.] Setze OTAMC_D_01 setze auf VPE_None", ""])
    #hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_CONTROL_A auf RUNNING ", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)
    testresult.append(["[.] Setze ORU_CONTROL_D auf  RUNNING ", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)
    testresult.append(["[.] Setze VDSO_Vx3d auf 0 km/h (37766)", ""])
    testresult.append(func_gs.setVelocity_kmph(0))
    testresult.append(["[.] Setze Waehlhebelposition P aktiviert", ""])
    testresult.append(func_gs.changeDrivePosition('P'))
    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)
    testresult.append(["[.] Setze ORU_01_Status  auf RUNNING", ""])
    hil.ORU_01__ORU_Status__value.set(4)
    testresult.append(["[.] Wartet 4100ms to fill buffer.", ""])
    time.sleep(4.1)
    testresult.append(["[-0]", ""])

    # test step 5
    testresult.append(["[.] Wechsel in Programming Session: 0x1002", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming', read_active_session=False, ticket_id='FehlerId:EGA-PRM-216'))

    # test step 6
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('programming', ticket_id='FehlerId:EGA-PRM-216'))

    # test step 7
    testresult.append(["[.] Wechsel in Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # test step 8
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 9
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 10
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 11
    testresult.append(["[.] System wartet 5000 ms.", ""])
    time.sleep(5.0)

    # test step 12
    testresult.append(["[.] '%s' auslesen: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x22] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 12.1
    testresult.append(["[+] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 12.2
    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length']))

    # test step 12.3
    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    response_content = response[3:]
    content_sw_blocks = []
    while len(response_content) > 0:
        if len(response_content) >= 4:
            content_sw_blocks.append(response_content[:4])
            del response_content[0:4]
        else:
            break
    i = 1
    sw_block_list = exp_sw_versions.keys()
    for sw_block in content_sw_blocks:
        testresult.append(["\xa0Prüfe Software Block Version (Block Nr. %s): 0x%02X 0x%02X 0x%02X 0x%02X" % (
        i, sw_block[0], sw_block[1], sw_block[2], sw_block[3]), "Info"])
        if i in exp_sw_versions.keys():
            testresult.append(["SW Block %s" % exp_sw_versions[i]['Block name'], "INFO"])
            readout_version = ""
            if exp_sw_versions[i]['version']:
                for r in sw_block: readout_version += str(r - 0x30)
                exp_version = exp_sw_versions[i]['version']
            else:
                for r in sw_block: readout_version += str(r)
                exp_version = 45454545 # 0x2D 0x2D 0x2D 0x2D
            testresult.append(
                _checkStatus(
                    current_status=int(readout_version),
                    nominal_status=exp_version,
                    descr="Prüfe, dass SW Block Version für Block %s wie erwartet ist" % i,
                    ticket_id='FehlerId:EGA-PRM-233'
                )
            )
            sw_block_list.remove(i)
        else:
            testresult.append(["Dieser Software Block wird nicht erwartet", "FAILED"])
        i += 1

    if len(sw_block_list) > 0:
        for sw_block in sw_block_list:
            testresult.append(["Software Block Version für Block %s fehlt" % sw_block, "FAILED"])
    testresult.append(["[-0]", ""])

    # test step 13
    testresult.append(["[.] System wartet 5000 ms.", ""])
    time.sleep(5.0)

    # test step 14
    testresult.append(["[.] Wechsel in Default Session: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # test step 15
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 16
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 17
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 18-18.
    testresult.append(["[.] Setze ORU_Control_A_01.OnlineRemoteUpdateControlA auf 6 (PENDING_NOT_READY)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(6)

    # testresult.append(["[+] Setze vbat_cl30__V auf 5.7 ", ""])
    # hil.vbat_cl30__V.set(5.7)

    testresult.append(["[+] System wartet 3300 ms ", ""])
    time.sleep(3.3)

    testresult.append(["[.] Wechsel in die Programming Session: 0x1002", ""])
    request_programming = [0x10, 0x02]
    testresult.append(["\xa0Versuchen, in 'programming session' zu wechseln", ""])
    [response, result] = canape_diag.sendDiagRequest(request_programming)
    testresult.append(result)

    testresult.append(["[.] Auf negative Response überprüfen", ""])
    testresult.append(canape_diag.checkNegativeResponse(response, request_programming, 0x22))
    testresult.append(["[-0]", ""])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup #################################################################
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

print "Done."
