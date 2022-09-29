# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : DiagnoseFingerprint_and_ProgramDateOf_LogicalSoftwareBlocksRead.py
# Task    : Diagnosejob 0x22 0xF15B
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
# 1.1  | 16.02.2022 | Mohammed   | Added Security Method
# 1.3  | 23.05.2022 | Mohammed     | Aktualisiert  Vorbedingungen
# 1.4  | 25.07.2022 | Mohammed     | Testschritte Aktualisiert
# ******************************************************************************
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import functions_common
from ttk_checks import basic_tests
import data_common as dc
import time
import functions_gearselection

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_147")

    # Initialize functions ####################################################
    func_common = functions_common.FunctionsCommon(testenv)
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    write_value = [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09]
    number_softwareblocks_n = 1
    programming_date = dc.programming_date
    vw_device_number = 403014  # 0 - 1F FFFF (2097151)
    importer_number = 410  # 0 - 3FF (1023)
    workshop_number = 13622  # 0 - 1 FFFF (131071)
    programming_state = 0x00  # correct

    # Initialize variables ####################################################
    diag_ident = identifier_dict['Fingerprint And Programming Date Of Logical Software Blocks']

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: KL15 und KL30 an", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    testresult.append(["[.] Waehlhebelposition P aktiviert und VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append([" \x0aSetze PropulsionSystemActive auf 0 (NotAktiv) ", "INFO"])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    testresult.append(["[.] Setze OTAMC_D_01::VehicleProtectedEnvironment_D = 1 (VPE_PRODUCTION)", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    testresult.append(["[.] Setze ORU_Control_A_01::OnlineRemoteUpdateControlA = 0 (IDLE)", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    testresult.append(["[.] Setze ORU_Control_D_01::OnlineRemoteUpdateControlD = 0 (IDLE)", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)
    testresult.append(["[-0]"])

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["[.] '%s' auslesen: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x22] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[+] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Datenlänge überprüfen", ""])
    testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length'] * number_softwareblocks_n))
    testresult.append(["[-0]"])

    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    response_content = response[3:]

    testresult.append(["[+] Prüfe Byte 0 (Jahr)", ""])
    year = int(str(programming_date[0]), 16) if len(str(programming_date[0])) == 2 else int(
        str(programming_date[0])[2:], 16)
    testresult.append(
        basic_tests.checkStatus(
            current_status=response_content[0],
            nominal_status=year,
            descr="Prüfe, dass Programming Date - Jahr korrekt ist: %s (0x%2X)" % (year, year)
        ))

    testresult.append(["[.] Prüfe Byte 1 (Monat)", ""])
    month = int(str(programming_date[1]), 16)
    testresult.append(
        basic_tests.checkStatus(
            current_status=response_content[1],
            nominal_status=month,
            descr="Prüfe, dass Programming Date - Monat korrekt ist: %s (0x%2X)" % (month, month)
        ))

    testresult.append(["[.] Prüfe Byte 2 (Tag)", ""])
    day = year = int(str(programming_date[2]), 16)
    testresult.append(
        basic_tests.checkStatus(
            current_status=response_content[2],
            nominal_status=day,
            descr="Prüfe, dass Programming Date - Tag korrekt ist: %s (0x%2X)" % (day, day)
        ))

    testresult.append(["[.] Prüfe Byte 3 - 8", ""])
    bin_content = map(bin, response_content[3:9])
    bin_value = ""
    for bc in bin_content:
        value = bc[2:]
        while len(value) < 8: value = "0" + value
        bin_value += value

    testresult.append(["[+] Prüfe Bit 0 - 20 (VW Device Number)", ""])
    vw_device_number_bit = int(bin_value[:21], 2)
    testresult.append(
        basic_tests.checkStatus(
            current_status=vw_device_number_bit,
            nominal_status=vw_device_number,
            descr="Prüfe, dass VW Device Number korrekt ist"
        ))

    testresult.append(["[.] Prüfe Bit 21 - 30 (Importer Number)", ""])
    importer_number_bit = int(bin_value[21:31], 2)
    testresult.append(
        basic_tests.checkStatus(
            current_status=importer_number_bit,
            nominal_status=importer_number,
            descr="Prüfe, dass Importer Number korrekt ist"
        ))

    testresult.append(["[.] Prüfe Bit 31 - 48 (Workshop Number)", ""])
    workshop_number_bit = int(bin_value[31:], 2)
    testresult.append(
        basic_tests.checkStatus(
            current_status=workshop_number_bit,
            nominal_status=workshop_number,
            descr="Prüfe, dass Workshop Number korrekt ist"
        ))
    testresult.append(["[-0]"])

    testresult.append(["[.] Prüfe Byte 9 (Programming State)", ""])
    #testresult.append(["[-0]"])
    testresult.append(
        basic_tests.checkStatus(
            current_status=response_content[9],
            nominal_status=programming_state,
            descr="Prüfe, dass Programming State korrekt ist"
        ))
    testresult.append(["[-0]"])

    # SCHREIBEN NEUER WERTE UND ANSCHLIESSEND LESEN
    # Wechsel in Extended Session: 0x1003
    testresult.append(["[.] In die Extended Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))
    time.sleep(1)

    # Wechsel in Programming Session: 0x1002
    testresult.append(["[.] In die Programming Session wechseln", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('programming'))
    time.sleep(1)

    testresult.append(["[.] Security Access aktivieren", ""])
    testresult.extend(canape_diag.SecurityAccessProg())

    testresult.append(["[.] Fingerprint And Programming Date Of Logical Software Blocks' schreiben: [0xF1, 0x5A]", ""])
    request = [0x2E] + [0xF1, 0x5A] + write_value
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] '%s' auslesen: %s" % (diag_ident['name'], str(HexList(diag_ident['identifier']))), ""])
    request = [0x22] + diag_ident['identifier']
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    testresult.append(["[+] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[.] Datenlänge überprüfen: exp_data_length * number_softwareblocks", ""])
    #testresult.append(canape_diag.checkDataLength(response, diag_ident['exp_data_length'] * number_softwareblocks_n))
    testresult.append(canape_diag.checkDataLength(response, 20))

    write_value1 = [0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x22, 0x09, 0x05, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x00]
    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    expected_response = [0x62] + diag_ident['identifier'] + write_value1
    testresult.append(canape_diag.checkResponse(response, expected_response, ticket_id='FehlerId:EGA-PRM-168'))

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
