# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : Partial_Programming_logical_block_layer.py
# Title   : Partial_Programming_logical_block_layer
# Task    : Diagnosejob 0x22 0xF1AB
#
# Author  : Mohammed Abdul Karim
# Date    : 06.05.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 06.05.2022 | Mohammed  | Initial
# 1.1  | 05.07.2022 | Mohammed  | Added Fehler ID
# ******************************************************************************
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
from ttk_checks import basic_tests
from functions_nm import _checkStatus

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_367")

    # Initialize functions ####################################################
    func_common = functions_common.FunctionsCommon(testenv)

    # Initialize variables ####################################################
    hil = testenv.getHil()
    diag_ident = identifier_dict['VW Logical Software Block Version']
    exp_sw_versions = {
        1: {'Block name': 'Bootloader', 'version': 187},
        2: {'Block name': 'Application', 'version': 111},
      #  3: {'Block name': 'Datensatz', 'version': None},
    }
    number_softwareblocks_n = len(exp_sw_versions)

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] aktiviere Tester Present", ""])
    canape_diag.enableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Setze ORU Signale", ""])
    testresult.append(["[+] Setze VehicleProtectedEnvironment_D auf 0 (VPE_none)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)
    testresult.append(["[.] Setze ORU_01.ORU_Status auf  (0) IDLE", ""])
    hil.ORU_01__ORU_Status__value.set(0)
    testresult.append(["[.] Setze ORU_Control_A_01.OnlineRemoteUpdateControlA auf (0) IDLE", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_Control_D_01.OnlineRemoteUpdateControlD  auf (0) IDLE", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)
    testresult.append(["[-0]", ""])

    # test step 2
    testresult.append(["[.] Wechsel in Extended Session: 0x1003", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 3
    testresult.append(["[.] Lese aktuelle Diagnose Session aus", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 4
    testresult.append(["[.] {}".format(diag_ident['name']), ""])
    testresult.append(["[+] Diagnose Request schicken: 0x22 {} (Lese {})"
                      .format(HexList(diag_ident['identifier']), diag_ident['name']),
                       ""])
    request = [0x22] + diag_ident['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length'], ticket_id= 'Fehler Id:EGA-PRM-130'))

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

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup #################################################################
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

print "Done."
