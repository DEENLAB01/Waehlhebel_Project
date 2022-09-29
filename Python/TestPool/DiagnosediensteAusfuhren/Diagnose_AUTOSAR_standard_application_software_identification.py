# *****************************************************************************
# -*- coding: latin-1 -*-
# File    : Diagnose_AUTOSAR_standard_application_software_identification.py
# Task    : Test for Diagnosejob 0x22 F1AF
#
# Author  : An3Neumann
# Date    : 17.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 17.06.2021 | An3Neumann   | initial
# 1.1  | 23.08.2021 | Mohammed     | Added Ticket Id
# 1.2  | 21.12.2021 | H. Förtsch   | reworked test script by test spec
# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests

from functions_diag import ResponseDictionaries
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
from functions_common import calcBytes2Value

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_141")

    # Initialize functions ####################################################
    rd = ResponseDictionaries()

    # Initialize variables ####################################################
    test_data = identifier_dict['AUTOSAR_standard_application_software_identification']
    exp_ssw_dict, all_ssw, vendor = rd.AUTOSAR_standard_application_software_identification()

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Diagnose Request schicken: 0x22 {} (Lese {})"
                      .format(HexList(test_data['identifier']), test_data['name']),
                       ""])
    request = [0x22] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    # test step 2
    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 3
    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response,
                                                  test_data['exp_data_length'],
                                                  ticket_id='Fehler Id:EGA-PRM-22'))

    # test step 4
    testresult.append(["[.] Prüfe SSW Module und deren Inhalte", ""])

    # split the response content into 7 Bytes each
    content_ssw = [response[(i * 7 + 3):(i * 7 + 10)] for i in range(len(response) // 7)]

    # test steps 4.x
    # silently go one chapter level down
    testresult.append(["[+0]", ""])
    exp_ssw = exp_ssw_dict.keys()  # required for test step 5
    for content in content_ssw:
        try:
            ssw_modul_id = calcBytes2Value(content[0:2])
            vendor_id = calcBytes2Value(content[2:4])
            ssw_version = calcBytes2Value(content[4:7])
        except IndexError:
            ssw_modul_id = None
            vendor_id = None
            ssw_version = None

        if ssw_modul_id in exp_ssw:
            # required for test step 5
            exp_ssw.remove(ssw_modul_id)

        testresult.append(["[.] Prüfe Inhalt der Response {}"
                          .format(HexList(content)),
                           ""])

        # test step 4.1
        testresult.append(["[+] Prüfe auf gültige SSW-Modul-ID", ""])
        if ssw_modul_id in exp_ssw_dict:
            testresult.append(["Gültige SSW-Modul-ID gefunden: 0x{:04X}"
                              .format(ssw_modul_id),
                               "PASSED"])
        else:
            testresult.append(["Undefinierte SSW-Modul-ID: 0x{:04X}"
                              .format(ssw_modul_id),
                               "FAILED"])

        sw_module_name = all_ssw.get(ssw_modul_id, 'unbekannt')
        testresult.append(["\xa0 SSW Modul name: {}".format(sw_module_name), "INFO"])

        exp_version, exp_vendor = exp_ssw_dict.get(ssw_modul_id, [None, None])

        # test step 4.2
        testresult.append(["[.] Prüfe auf Vendor-ID {}".format(exp_vendor), ""])
        if exp_vendor is None:
            testresult.append(["Keine erwartete Vendor-ID für unbekanntes SW-Modul!", "FAILED"])
        else:
            if isinstance(vendor_id, (int, long)):
                testresult.append(
                    basic_tests.checkStatus(
                        current_status=vendor_id,
                        nominal_status=exp_vendor))
            else:
                testresult.append(["Ungültige Vendor-ID!", "FAILED"])

        # test step 4.3
        testresult.append(["[.] Prüfe auf SSW-Version {}".format(exp_version), ""])
        if exp_version is None:
            testresult.append(["Keine erwartete SSW-Version für unbekanntes SW-Modul!", "FAILED"])
        else:
            if isinstance(ssw_version, (int, long)):
                testresult.append(
                    basic_tests.checkStatus(
                        current_status=ssw_version,
                        nominal_status=exp_version))
            else:
                testresult.append(["Ungültige SSW-Version!", "FAILED"])

        # test step 4.4
        testresult.append(["[.] Prüfe, dass SSW Modul durch VW AG zur Verfügung gestellt wurde", ""])
        if None in [ssw_modul_id, vendor_id, ssw_version]:
            testresult.append(["Ungültiger Inhalt der Response:\n{}".format(HexList(content)), "FAILED"])
        else:
            testresult.append(["0x{:04X} 0x{:04X} 0x{:06X}"
                              .format(ssw_modul_id, vendor_id, ssw_version),
                               "PASSED"])

        # silently go one chapter level up
        testresult.append(["[-0]", ""])

    testresult.append(["[-] Prüfe, dass alle implementierten SSW Module ausgegeben wurden", ""])
    if exp_ssw:
        testresult.append(["Nicht alle implementierten SSW Module wurden ausgegeben"
                           "Es fehlen folgende Module:\n- "
                           "\n- ".join([all_ssw[ssw] for ssw in exp_ssw]),
                           "FAILED"])
    else:
        testresult.append(["Alle implementierten SSW Module wurden ausgegeben", "PASSED"])

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
