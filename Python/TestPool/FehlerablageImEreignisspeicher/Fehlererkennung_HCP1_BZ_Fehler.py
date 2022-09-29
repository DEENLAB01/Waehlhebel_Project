#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Fehlererkennung_HCP1_BZ_Fehler.py
# Title   : Fehlererkennung_HCP1_BZ_Fehler
# Task    : Fehlererkennung für BZ-Fehler HCP1 und Ablage im Fehlerspeicher

# Author  : Mohammed Abdul Karim
# Date    : 17.05.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 17.05.2022  | Mohammed | initial
# 1.1  | 14.07.2022 | Mohammed | Added tMSG_Timeout: n-q+1, n=10, q=2
# 1.3  | 20.07.2022  | Mohammed  | Added Fehler Id
#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()

# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
from ttk_checks import basic_tests
import functions_gearselection
from functions_diag import HexList  # @UnresolvedImport
import time
from functions_nm import _checkStatus

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()

    # Initialize variables ####################################################
    wait_time = 5000  # CAN_3244
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    wh_fahrstufe_fehlerwert = 15
    allowed_fahrstufe = [4, 5, 6, 7]  # Nicht betigt, D, N, R
    bz_signal = hil.SiShift_01__SiShift_01_20ms_BZ__value
    sishift_04_timestamp = hil.SiShift_01__timestamp
    meas_vars = [bz_signal, wh_fahrstufe, sishift_04_timestamp]
    aktiv_dtc = [(0xE00102, 0x27)]
    passiv_dtc = [(0xE00102, 0x26)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_186")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: LK30 und Kl15 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[.] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    request = [0x22] + [0xF1, 0xF3]
    [response, result] = canape_diag.sendDiagRequest(request)
    testresult.append(["[.] Prüfe Raumtemperatur zwischen -40 to 90 Grad", ""])
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

    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze PropulsionSystemActive auf 0 (NotAktiv) ", ""])
    hil.OBD_04__MM_PropulsionSystemActive__value.set(0)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up

    # test step 1
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 2
    testresult.append(["[.] Halte SiShift_01::SiShift_01_BZ an (Setze Inkrementierung des Botschaftszählers aus)", ""])
    hil.SiShift_01__SiShift_01_20ms_BZ__switch.set(1)

    # test step 3
    testresult.append(["[.] Warte 260ms (tMSG_Timeout: n-q+1, n=14, q=2) + 10ms(Tolerenz)", ""])
    time.sleep(0.270)

    # test step 4
    testresult.append(["[.] Lese Botschaft Wahlhebel_04::WH_Fahrstufe", ""])
    testresult.append(
        _checkStatus(current_status=wh_fahrstufe,
                     nominal_status=15,
                     descr="Prüfe WH_Fahrstufe = 15 ist",
                     ticket_id='FehlerId:EGA-PRM-261'))
    # test step 5
    testresult.append(["[.] Lese Fehlerspeicher (0xE00102 DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc))

    # test step 6
    testresult.append(["[.] Setze SiShift_01::SiShift_01_BZ wieder fort)", ""])
    hil.SiShift_01__period.setState("an")
    hil.SiShift_01__SiShift_01_20ms_BZ__switch.set(0)

    # test step 7
    testresult.append(["[.] Warte 140ms  (tMSG_Timeoutn: n/2, n=14) + 10ms (Toleranz)", ""])
    time.sleep(0.160)

    # test step 8
    testresult.append(["[.] Lese Botschaft Wahlhebel_04::WH_Fahrstufe", ""])
    testresult.append(
        _checkStatus(current_status=wh_fahrstufe,
                     nominal_status=4,
                     descr="Prüfe WH_Fahrstufe != 15 ist",
                     ticket_id='FehlerId:EGA-PRM-261'))

    # test step 9
    testresult.append(["[.] Lese Fehlerspeicher (0xE00102  DTC Passiv)", ""])
    testresult.append(canape_diag.checkEventMemory(passiv_dtc))

    # test step 10
    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # test step 11
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1)

    # test step 12
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["[+] Bus Reset", ""])
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

