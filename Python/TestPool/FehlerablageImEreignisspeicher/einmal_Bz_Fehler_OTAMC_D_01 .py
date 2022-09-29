#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : einmal_Bz_Fehler_OTAMC_D_01.py
# Title   : einmal_Bz_Fehler_OTAMC_D_01
# Task    : Fehlererkennung einamal BZ-Fehler OTAMC_D_01 und Ablage im Fehlerspeicher

# Author  : Mohammed Abdul Karim
# Date    : 19.05.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 19.05.2022 | Mohammed | initial created Timeout Test
# 1.1  | 10.06.2022 | Mohammed | TestSpec Aktualisiert
# 1.2  | 29.06.2022 | Mohammed | tMSG_Botschaftszählers Aktualisiert
# 1.3  | 15.08.2022 | Mohammed | Added Tollerenz
#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()
import functions_gearselection
# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
from ttk_checks import basic_tests
from functions_diag import HexList  # @UnresolvedImport
import time

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()

    # Initialize variables ####################################################
    period_var = hil.OTAMC_D_01__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 1500
    passive_dtcs = [(0xE0010C, 0x26)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_198")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: LK30 und Kl15 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[.] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["[.] Prüfe Raumtemperatur zwischen -40 to 90 Grad", ""])
    request = [0x22] + [0xF1, 0xF3]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(result)
    # testresult.append(["[+] Auf positive Response überprüfen", ""])
    # testresult.append(canape_diag.checkPositiveResponse(response, request))
    if len(response) > 3:
        data = response[3:]  # just take data of complete response
        temp_value_dec = 0
        i = len(response) - 3 - 1
        for temp_value in data:
            temp_value_dec += temp_value << (i * 8)  # set all bytes together
            i -= 1

        testresult.append(["Empfangene Daten (Rohwert): {}\nEntspricht dem Temeprature Sensor Wert : {} Grad"
                          .format(str(HexList(data)), temp_value_dec),
                           "INFO"])
        testresult.append(basic_tests.checkRange(temp_value_dec, 0, 0x5A))

    else:
        testresult.append(["Keine Auswertung möglich, da falsche oder keine Response empfangen wurde!", "FAILED"])

    testresult.append(["[.] Prüfe Betriebsspannung : 6-16 V", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.vbat_cl30__V.get(),  # letzer Sendetimestamp
            min_value=6.0,
            max_value=16.0,
            descr="Check that value is in range"
        )
    )

    testresult.append(["[.] Waehlhebelposition P aktiviert ", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze PropulsionSystemActive_switch = 0", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    # test step 1
    testresult.append(["[.] Setze Zykluszeit der Botschaft OTAMC_D_01 auf 320ms (gültig)", ""])
    testresult.append(["\xa0 Setze Zykluszeit auf %sms" % cycle_time, ""])
    period_var.set(cycle_time)

    # test step 2
    testresult.append(["[.] Warte 1000 ms", ""])
    time.sleep(1.0)

    # test step 3
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 4
    testresult.append(["[.] Halte OTAMC_D_01:OTAMC_D_01_BZ an (Setze Inkrementierung des Botschaftszählers aus)", ""])
    hil.OTAMC_D_01__OTAMC_D_01_BZ__switch.set(1)

    # test step 5
    testresult.append(["[.] Warte 2880ms (tMSG_Timeout: n-q+1, n=10, q=2) + 220ms (Tollerenz)", ""])
    time.sleep(3.1)

    # test step 6
    testresult.append(["[.] Setze OTAMC_D_01:OTAMC_D_01_BZ wieder fort)", ""])
    hil.OTAMC_D_01__OTAMC_D_01_BZ__switch.set(0)

    # test step 7
    testresult.append(["[.] Warte 1600 ms (tMSG_Timeout: n/2, n=10, q=2) + 220ms", ""])
    time.sleep(1.82)

    # test step 8
    testresult.append(["[.] Lese Fehlerspeicher (0xE0010C DTC passiv)", ""])
    testresult.append(canape_diag.checkEventMemory(passive_dtcs))

    # test step 9
    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # test step 10
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1)

    # test step 11
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[.] Bus Reset", ""])
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(0.5)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    cal = None
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()

