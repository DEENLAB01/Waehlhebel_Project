# *****************************************************************************
# -*- coding: latin1 -*-
# File    : Diagnose_OBD_Driving_Cycle_set_once_Empfang_DTC.py
# Title   : Diagnose OBD Driving Cycle set once Empfang DTC
# Task    : A minimal "Diagnose_OBD_Driving_Cycle_set_once_Empfang_DTC!" test script
#
# Author  : Mohammed Abdul Karim
# Date    : 17.03.2022
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ******************************** Version ************************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 17.03.2022 | Mohammed     | initial
# 1.1  | 25.07.2022 | Mohammed     | Testschritte aktualisiert

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList  # @UnresolvedImport
from diag_identifier import identifier_dict  # @UnresolvedImport
import time
from ttk_checks import basic_tests
# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_383")
    # Initialize functions ####################################################
    hil = testenv.getHil()

    # Initialize variables ####################################################
    test_data = identifier_dict['OBD Driving Cycle set once']
    active_dtcs = [(0x800100, 0x27), (0x800101, 0x27)]
    passiv_dtcs = [(0x800100, 0x26), (0x800101, 0x26)]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: KL30 und KL15 an", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()
    testresult.append(canape_diag.resetEventMemory(wait=False))

    testresult.append(["[.] NWDF ist freigegeben:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)


    # TEST PROCESS ############################################################
    testresult.append(["\nStarte Testprozess: %s"%testenv.script_name.split('.py')[0], ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    #testresult.append(["[.] '%s' auslesen: %s" %(test_data['name'], HexList(test_data['identifier'])), ""])
    testresult.append(["[.] OBD_03::OBD_Driving_Cycle_set_once = 1 senden", ""])
    hil.OBD_03__OBD_Driving_Cycle__value.set(1)

    # test step 2
    testresult.append(["[.] Diagnose Request schicken: 0x220261 ", ""])
    request = [0x22] + test_data['identifier']
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)

    obd_driving_cycle_orig = response[3:]

    # test step 3
    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 4
    testresult.append(["[.] Prüfe Länge der Response", ""])
    testresult.append(canape_diag.checkDataLength(response, test_data['exp_data_length']))

    # test step 5
    testresult.append(["[.] Inhalt auf Korrektheit überprüfen", ""])
    testresult.append(canape_diag.checkResponse(obd_driving_cycle_orig, test_data['expected_response']))

    # test step 6
    testresult.append(["[.] OBD_03::OBD_Driving_Cycle_set_once = 0 senden", ""])
    hil.OBD_03__OBD_Driving_Cycle__value.set(0)

    # test step 7
    testresult.append(["[.] Wechsel in Factory Mode: 0x1060", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('factory_mode', read_active_session=False))

    # test step 8
    testresult.append(["[.] Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('factory_mode'))

    # test step 9
    testresult.append(["[.] Security Access aktivieren", ""])

    # test step 9.1
    testresult.append(["[+] Seed anfragen: 0x2761", ""])
    seed, result = canape_diag.requestSeed()
    testresult.extend(result)

    # test step 9.2
    testresult.append(["[.] Key berechnen: <key 1>", ""])
    key, result = canape_diag.calculateKey(seed)
    testresult.extend(result)

    # test step 9.3
    testresult.append(["[.] Key senden: 0x2762 + <key 1>", ""])
    verdict = canape_diag.sendKey(key)
    testresult.extend(verdict)
    testresult.append(["[-0]", ""])

    # test step 10
    #testresult.append(["[.] Schreiben der OBD_Driving_Cycle: 0x2E0261 + 00", ""])
    obd_driving_cycle = [0x00]
    request = [0x2E, 0x02, 0x61]
    testresult.append(["[.] Schreibe OBD_Driving_Cycle: 0x{} + 0x{}"
                       .format("".join("{:02X}".format(x) for x in request),
                               "".join("{:02X}".format(x) for x in obd_driving_cycle)),
                       ""])
    response, result = canape_diag.sendDiagRequest(request + obd_driving_cycle)

    testresult.append(["\xa0Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request, ticket_id='FehlerId:EGA-PRM-236'))

    # test step 11
    testresult.append(["[.] Diagnose Request schicken: 0x220261", ""])
    testresult.append([" Prüfe Inhalt: 0x{}"
                       .format(" ".join("{:02X}".format(x) for x in obd_driving_cycle)),
                       ""])
    request = [0x22, 0x02, 0x61]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response[3:], obd_driving_cycle))

    # test step 12
    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkResponse(response, [0x62, 0x02, 0x61, 0x00]))
    #testresult.append(canape_diag.checkPositiveResponse(response, request))

    # test step 13
    testresult.append(["[.] Setze Überspannung: hil.vbat_cl30__V == 16.656V ", ""])
    hil.vbat_cl30__V.set(16.656)

    # test step 14
    testresult.append(["[.] Warte 20ms (voltage settle down time)", ""])
    time.sleep(0.02)

    # test step 15
    testresult.append(["[.] Lese Fehlerspeicher (leer)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 16
    testresult.append(["[.] OBD_03::OBD_Driving_Cycle_set_once = 1 senden", ""])
    hil.OBD_03__OBD_Driving_Cycle__value.set(1)

    # test step 17
    testresult.append(["[.] Diagnose Request schicken: 0x220261", ""])
    request = [0x22, 0x02, 0x61]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkResponse(response[3:], obd_driving_cycle))

    # test step 18
    testresult.append(["[.] Überprüfen, dass Request positiv beantwortet wird", ""])
    testresult.append(canape_diag.checkPositiveResponse(response, request))

    testresult.append(["[+] Warte 500ms", ""])
    time.sleep(.500)
    testresult.append(["[-0]", ""])

    # test step 19
    testresult.append(["[.] Lese Fehlerspeicher (Überspannungs-DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(active_dtcs))

    # test step 20
    testresult.append(["[.] Setze Überspannung: hil.vbat_cl30__V == 13.0V ", ""])
    hil.vbat_cl30__V.set(13.0)

    # test step 21
    testresult.append(["[.] Warte 20ms(voltage settle down time)", ""])
    time.sleep(0.02)

    # test step 22
    testresult.append(["[.] Überprüfe gemessene Spannung mit DID 0x22F1F2", ""])
    request = [0x22] + [0xF1, 0xF2]
    response, result = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    testresult.append(canape_diag.checkDataLength(response, 2))

    testresult.append(["\x0a Prüfe Spannung <= 16 V", ""])
    #testresult.append(["[.] Prüfe Voltage : 13-16 V", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.vbat_cl30__V.get(),  # letzer Sendetimestamp
            min_value=6.0,
            max_value=16.0,
            descr="Check that value is in range"
        )
    )


    # test step 23
    testresult.append(["[.] Warte 500ms ", ""])
    time.sleep(0.500)

    # test step 24
    testresult.append(["[.] Lese Fehlerspeicher (Überspannungs-DTC passiv und confirmed)", ""])
    testresult.append(canape_diag.checkEventMemory(passiv_dtcs))

    # test step 25
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=False))

    # test step 26
    testresult.append(["[.] Lese Fehlerspeicher (leer)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

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
