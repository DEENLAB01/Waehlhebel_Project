# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : Diagnose_VW_Logical_Software_Block_Version.py
# Task    : Diagnosejob 0x22 0xF1AB
#
# Author  : An3Neumann
# Date    : 21.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 21.06.2021 | An3Neumann | initial
# 1.1  | 28.10.2021 | Mohammed | Added   Bootloader/ Application version
# 1.2  | 06.12.2021 | Mohammed | Corrected Data length
# ******************************************************************************
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
from ttk_checks import basic_tests

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_148")

    # Initialize functions ####################################################
    func_common = functions_common.FunctionsCommon(testenv)

    # Initialize variables ####################################################
    diag_ident = identifier_dict['VW Logical Software Block Version']
    exp_sw_versions = {
        1: {'Block name': 'Bootloader', 'version' : 187},
        2: {'Block name': 'Application', 'version': 111},
      #  3: {'Block name': 'Datensatz', 'version': None},
    }
    number_softwareblocks_n = len(exp_sw_versions)

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["[+] '%s' auslesen: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x22] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length'], ticket_id= 'Fehler Id:EGA-PRM-130'))
    #testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length'] * number_softwareblocks_n))

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
                basic_tests.checkStatus(
                    current_status=int(readout_version),
                    nominal_status=exp_version,
                    descr="Prüfe, dass SW Block Version für Block %s wie erwartet ist" % i
                )
            )
            sw_block_list.remove(i)
        else:
            testresult.append(["Dieser Software Block wird nicht erwartet", "FAILED"])
        i += 1

    if len(sw_block_list) > 0:
        for sw_block in sw_block_list:
            testresult.append(["Software Block Version für Block %s fehlt" % sw_block, "FAILED"])

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
