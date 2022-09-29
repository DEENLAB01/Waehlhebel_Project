#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Fehlererkennung_CRC_Error_SiShift.py
# Title   : Fehlererkennung_SafeState01_CRC_Error_SiShift
# Task    : Fehlererkennung für CRC_Error_SiShift und Ablage im Fehlerspeicher

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
# 1.0  | 11.07.2022  | Mohammed | Reworked
#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()

# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
from ttk_checks import basic_tests
import functions_gearselection
import functions_hil
from time import time as t
import time
import functions_nm
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
    func_hil = functions_hil.FunctionsHil(testenv, hil)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    wait_time = 5000  # CAN_3244
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    wh_fahrstufe_fehlerwert = 15
    allowed_fahrstufe = [4, 5, 6, 7]  # Nicht betigt, D, N, R
    crc_signal = hil.SiShift_01__SiShift_01_20ms_CRC__value
    sishift_04_timestamp = hil.SiShift_01__timestamp
    meas_vars = [crc_signal, wh_fahrstufe, sishift_04_timestamp]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_110")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: LK30 und Kl15 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[.] Waehlhebelposition = P Senden ", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["[.] Setze OBD_Driving_Cycle auf 1", ""])
    hil.OBD_03__OBD_Driving_Cycle__value.set(1)

    testresult.append(["[.] Auslesen Raumtemperatur DID: 0xF1F3 (Temeprature Sensor Read)", ""])
    res, verdict = canape_diag.sendDiagRequest([0x22, 0xF1, 0xF3])
    testresult.append(["[.] Raumtemperatur zwischen -40 to 90 Grad = %s degree" % (int(hex(res[3]), 16)), ""])

    testresult.append(["[.] Prüfe Betriebsspannung : 6-16 V", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.vbat_cl30__V.get(),  # letzer Sendetimestamp
            min_value=6.0,
            max_value=16.0,
            descr="Check that value is in range"
        )
    )

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up

    # test step 1
    testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    testresult.append(["\xa0 Prüfe Waehlhebel_04:WH_Fahrstufe = 4", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = allowed_fahrstufe,
            current_value= current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe korrekt ist"
        )
    )

    # test step 2-2.1
    testresult.append(["[.] Sende Erste SiShift-CRC Fehler und warte 50 ms", ""])
    sec = 0.019
    timeout = sec + t()
    while timeout > t():
        hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)
    time.sleep(0.05)

    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Fahrstufe = 15", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = wh_fahrstufe_fehlerwert,
            current_value= current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe korrekt ist"
        )
    )

    testresult.append(["[+] Prüfe, dass Fehler Leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())
    testresult.append(["[-0]", ""])

    # test step 3-3.1
    testresult.append(["[.] Sende zweite SiShift-CRC Fehler und warte 50 ms", ""])
    sec = 0.019
    timeout = sec + t()
    while timeout > t():
        hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)
    time.sleep(0.05)

    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Fahrstufe = 15", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = wh_fahrstufe_fehlerwert,
            current_value= current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe korrekt ist"
        )
    )

    testresult.append(["[+] Lese Fehlerspeicher (0xE00103 DTC aktiv)", ""])
    active_dtcs = [(0xE00103, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs))
    testresult.append(["[-0]", ""])

    # test step 4
    testresult.append(["[.] Setze SiShift-CRC_Error zurück, warte 50 ms, lese Botschaft", ""])
    time.sleep(0.05)

    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Fahrstufe = 15", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values=wh_fahrstufe_fehlerwert,
            current_value=current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe korrekt ist"
        )
    )

    # test step 5
    testresult.append(["[.] Lese Fehlerspeicher (0xE00103 DTC aktiv)", ""])
    active_dtcs = [(0xE00103, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs))

    testresult.append(["\x0a Führe erneuten 3 OP-PowerCycle (ECU_Sleep -> ECU_WakeUp) ", ""])
    testresult.append(["[.] Führe erneuten 1 OP-PowerCycle (ECU_Sleep -> ECU_WakeUp) ", ""])
    hil.cl15_on__.set(0)
    time.sleep(.200)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(30)

    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(5)

    testresult.append(["[+] Lese Fehlerspeicher Passiv ", ""])
    passive_dtcs = [(0xE00103, 0x24)]
    testresult.append(canape_diag.checkEventMemory(passive_dtcs, mode="ONE_OR_MORE"))

    testresult.append(["[.] Sende zweite SiShift-CRC Fehler und warte 200 ms", ""])
    sec = 0.04
    timeout = sec + t()
    while timeout > t():
        hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)
    time.sleep(0.200)
    testresult.append(["[-0]", ""])

    testresult.append(["[.] Führe erneuten 2 OP-PowerCycle (ECU_Sleep -> ECU_WakeUp) ", ""])
    hil.cl15_on__.set(0)
    time.sleep(.200)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    hil.cl15_on__.set(1)
    time.sleep(30)

    descr, verdict = func_gs.switchAllRXMessagesOn()
    time.sleep(5)

    testresult.append(["[+] Lese Fehlerspeicher Passiv ", ""])
    passive_dtcs = [(0xE00103, 0x24)]
    testresult.append(canape_diag.checkEventMemory(passive_dtcs, mode="ONE_OR_MORE", ticket_id='FehlerId: EGA-PRM-219'))

    testresult.append(["[.] Sende zweite SiShift-CRC Fehler und warte 200 ms", ""])
    sec = 0.04
    timeout = sec + t()
    while timeout > t():
        hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)
    time.sleep(0.200)
    testresult.append(["[-0]", ""])

    testresult.append(["[.] Führe erneuten 3 OP-PowerCycle (ECU_Sleep -> ECU_WakeUp) ", ""])
    hil.cl15_on__.set(0)
    time.sleep(.200)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(30)
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(5)

    testresult.append(["[+] Lese Fehlerspeicher Passiv ", ""])
    passive_dtcs = [(0xE00103, 0x24)]
    testresult.append(canape_diag.checkEventMemory(passive_dtcs, mode="ONE_OR_MORE"))
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(5)

    testresult.append(["[.] Sende zweite SiShift-CRC Fehler und warte 200 ms", ""])
    sec = 0.040
    timeout = sec + t()
    while timeout > t():
        hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)
    time.sleep(0.200)

    testresult.append(["[.] Lese Fehlerspeicher (Confirme DTC )", ""])
    passive_dtcs = [(0xE00103, 0x2F)]
    testresult.append(canape_diag.checkEventMemory(passive_dtcs, mode="ONE_OR_MORE"))
    testresult.append(["[-0]", ""])

    # test step 11
    testresult.append(["[.] Lösche Fehlerspeicher, warte 1000 ms", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
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

