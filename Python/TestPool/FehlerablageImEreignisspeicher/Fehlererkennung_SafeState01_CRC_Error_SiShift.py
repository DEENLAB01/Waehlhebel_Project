#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Fehlererkennung_CRC_Error_SiShift.py
# Title   : Fehlererkennung_SafeState01_CRC_Error_SiShift
# Task    : Fehlererkennung  CRC_Error_SiShift für Confirmed DTC im Fehlerspeicher

# Author  : Mohammed Abdul Karim
# Date    : 17.05.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 17.05.2022  | Mohammed  | initial
# 1.1  | 11.07.2022  | Mohammed  | Reworked
# 1.3  | 14.07.2022  | Mohammed  | 3 OP-PowerCycle
# 1.4  | 20.07.2022  | Mohammed  | Added Fehler Id
# 1.4  | 27.07.2022  | Mohammed  | Added waiting time during ECU_Sleep
# 1.5  | 15.08.2022  | Mohammed  | Added Toleranz
#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()

# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
from ttk_checks import basic_tests
import functions_gearselection
import functions_hil
from time import time as t
from functions_diag import HexList  # @UnresolvedImport
import time
import functions_nm
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
    aktiv_dtc = [(0xE00103, 0x27)]
    passiv_dtc = [(0xE00103, 0x24)]
    confirm_dtc = [(0xE00103, 0x2F)]
    curr_value = func_nm.low_current()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_110")

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
    testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    testresult.append(
        _checkStatus(current_status = wh_fahrstufe,
                     nominal_status= 4,
                     descr="Prüfe WH_Fahrstufe = 4 ist",
                     ticket_id='FehlerId:EGA-PRM-260'))

    # test step 2-2.3
    testresult.append(["[.] Sende ersten CRC-Fehler für  SiShift_01::SiShift_01_CRC", ""])
    sec = 0.019
    timeout = sec + t()
    hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)
    hil.SiShift_01__period.setState("an")
    while timeout > t():
        hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)

    testresult.append(["[+] Warte für 0ms (FR=Fehlerreaktionszeit) + 20ms (Toleranz)", ""])
    time.sleep(0.020)

    testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    testresult.append(
        _checkStatus(current_status=wh_fahrstufe,
                     nominal_status=15,
                     descr="Prüfe WH_Fahrstufe = 15 ist",
                     ticket_id='FehlerId:EGA-PRM-260'))

    testresult.append(["[.] Prüfe, dass Fehler Leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())
    testresult.append(["[-0]", ""])

    # test step 3-3.3
    testresult.append(["[.] Sende zweite CRC-Fehler für  SiShift_01::SiShift_01_CRC", ""])
    sec = 0.019
    timeout = sec + t()
    while timeout > t():
        hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)

    testresult.append(["[+] Warte für 0ms (FR=Fehlerreaktionszeit) + 15ms (Toleranz)", ""])
    time.sleep(0.015)

    testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = wh_fahrstufe_fehlerwert,
            current_value= current_fahrstufe,
            descr="Prüfe WH_Fahrstufe = 15 ist"
        )
    )

    testresult.append(["[.] Lese Fehlerspeicher (0xE00103 DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc))
    testresult.append(["[-0]", ""])

    # test step 4-4.3
    testresult.append(["[.] Sende keinen CRC-Fehler mehr für SiShift_01::SiShift_01_CRC", ""])
    testresult.append(["[+] Warte 40ms (2x tMSG_CYCLE )+ 10ms (Toleranz)", ""])
    time.sleep(0.05)

    testresult.append(["[.] Lese Botschaft Waehlhebel_04::WH_Fahrstufe", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values=wh_fahrstufe_fehlerwert,
            current_value=current_fahrstufe,
            descr="Prüfe WH_Fahrstufe = 15 ist"
        )
    )

    testresult.append(["[.] Lese Fehlerspeicher (0xE00103 DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc))
    testresult.append(["[-0]", ""])

    # test step 5-5.6
    testresult.append(["\x0a Führe 3 OP-PowerCycle (ECU_Sleep (Ruhestrom auswerten) -> ECU_WakeUp) durch:", ""])
    testresult.append(["[.] Führe ersten OP-PowerCycle (ECU_Sleep  -> ECU_WakeUp) durch", ""])
    hil.cl15_on__.set(0)
    time.sleep(.200)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(14)
    testresult.append(["[+] Warte 14 Sekunde während ECU_Sleep und Prüfe Ruhestrom ", ""])
    testresult.append(basic_tests.checkRange(value=hil.cc_mon__A,
                                             min_value=0.0,  # 0mA
                                             max_value=0.006,  # 6mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt", ))

    testresult.append(["[.] Bus WakeUp und Warte 2 Sekunde  ", ""])
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(2)

    testresult.append(["[.] Lese Fehlerspeicher Passiv ", ""])
    testresult.append(canape_diag.checkEventMemory(passiv_dtc, mode="ONE_OR_MORE"))

    testresult.append(["[.] Sende zwei SiShift_01-CRC Fehler hintereinander ", ""])
    sec = 0.04
    timeout = sec + t()
    while timeout > t():
        hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)

    testresult.append(["[.] Warte für 0ms (FR=Fehlerreaktionszeit) + 15ms (Toleranz)", ""])
    time.sleep(0.015)
    testresult.append(["[.] Lese Fehlerspeicher (0xE00103 DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc, mode="ONE_OR_MORE"))
    testresult.append(["[-0]", ""])

    # test step 6-6.6
    testresult.append(["[.] Führe zweiten OP-PowerCycle (ECU_Sleep -> ECU_WakeUp)", ""])
    hil.cl15_on__.set(0)
    time.sleep(.200)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(14)
    testresult.append(["[+] Warte 14 Sekunde während ECU_Sleep und Prüfe Ruhestrom ", ""])
    testresult.append(basic_tests.checkRange(value=hil.cc_mon__A,
                                             min_value=0.0,  # 0mA
                                             max_value=0.006,  # 6mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt", ))

    testresult.append(["[.] Bus WakeUp und Warte 2 Sekunde  ", ""])
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(2)

    testresult.append(["[.] Lese Fehlerspeicher Passiv ", ""])
    testresult.append(canape_diag.checkEventMemory(passiv_dtc, mode="ONE_OR_MORE", ticket_id='FehlerId: EGA-PRM-219'))

    testresult.append(["[.] Sende zwei SiShift_01-CRC Fehler hintereinander ", ""])
    sec = 0.04
    timeout = sec + t()
    while timeout > t():
        hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)

    testresult.append(["[.] Warte für 0ms (FR=Fehlerreaktionszeit) + 15ms (Toleranz)", ""])
    time.sleep(0.015)
    testresult.append(["[.] Lese Fehlerspeicher (0xE00103 DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc, mode="ONE_OR_MORE"))
    testresult.append(["[-0]", ""])

    # test step 7-7.6
    testresult.append(["[.] Führe dritten OP-PowerCycle (ECU_Sleep -> ECU_WakeUp)", ""])
    hil.cl15_on__.set(0)
    time.sleep(.200)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(14)
    testresult.append(["[+] Warte 14 Sekunde während ECU_Sleep und Prüfe Ruhestrom ", ""])
    testresult.append(basic_tests.checkRange(value=hil.cc_mon__A,
                                             min_value=0.0,  # 0mA
                                             max_value=0.006,  # 6mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt", ))

    testresult.append(["[.] Bus WakeUp und Warte 2 Sekunde  ", ""])
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(2)

    testresult.append(["[.] Lese Fehlerspeicher Passiv ", ""])
    testresult.append(canape_diag.checkEventMemory(passiv_dtc, mode="ONE_OR_MORE"))
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(5)

    testresult.append(["[.] Sende zwei SiShift_01-CRC Fehler hintereinander ", ""])
    sec = 0.04
    timeout = sec + t()
    while timeout > t():
        hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)

    testresult.append(["[.] Warte für 0ms (FR=Fehlerreaktionszeit) + 15ms (Toleranz)", ""])
    time.sleep(0.015)
    testresult.append(["[.] Lese Fehlerspeicher (Aktiv und Confirme DTC)", ""])
    testresult.append(canape_diag.checkEventMemory(confirm_dtc, mode="ONE_OR_MORE", ticket_id='FehlerId: EGA-PRM-219'))
    testresult.append(["[-0]", ""])

    # test step 9
    testresult.append(["[.] Lösche Fehlerspeicher, warte 1000 ms", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    time.sleep(1)

    # test step 10
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

