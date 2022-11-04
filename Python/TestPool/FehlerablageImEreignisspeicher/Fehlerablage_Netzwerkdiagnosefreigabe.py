# *******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Fehlerablage_Netzwerkdiagnosefreigabe.py
# Title   : Fehlerablage_Netzwerkdiagnosefreigabe
# Task    : Fehlerablage Netzwerkdiagnosefreigabe

# Author  : Mohamed Abdul Karim
# Date    : 03.03.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************** Version ***********************************
# ******************************************************************************
# Rev. | Date        | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 27.07.2021 | Mohammed | initial
# 1.1  | 08.08.2021 | Mohammed | Update TestStep
# 1.2  | 10.08.2021 | Mohammed | Rework
# 1.3  | 17.08.2022  | Mohammed   | Added Fehler ID
# 1.4  | 19.10.2022 | Devangbhai | Rework according to new specification.
# 1.5  | 04.11.2022 | Devangbhai | Added Ticket ID
# ******************************************************************************

from _automation_wrapper_ import TestEnv

testenv = TestEnv()

# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
import functions_gearselection
import time
import data_common as dc

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    # testenv.startupECU()  # startup before cal vars are called
    # canape_diag = testenv.getCanapeDiagnostic()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)


    # Initialize variables ####################################################
    period_var = hil.Systeminfo_01__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 5000  # CAN_3244
    active_dtcs = [(0xE00106, 0x27)]
    passive_dtcs = [(0xE00106, 0x26)]
    active_dtcs_uv = [(0xE00106, 0x26), (0x800100, 0x27), (0x800102, 0x27)]
    Passiv_dtcs_uv = [(0xE00106, 0x26), (0x800100, 0x26), (0x800102, 0x26)]
    active_dtcs_ov = [(0x800100, 0x27), (0x800101, 0x27)]
    Passiv_dtcs_ov = [(0x800100, 0x26), (0x800101, 0x26)]
    ORU_A_DTC_Aktiv = [(0xE00107, 0x27)]
    SySInfo_DTC_Aktiv = [(0xE00106, 0x27)]



    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_209")

    # TEST PRE CONDITIONS #####################################################
    # testresult.append(["[#0] Test Vorbedingungen: KL15 und KL30 an", ""])
    # testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])
    #
    # testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    # testresult.append(canape_diag.resetEventMemory(wait=True))
    #
    # # TEST PROCESS ############################################################
    # testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # # silently go one chapter level up
    #
    # testresult.append(["[-0]", ""])
    #
    # # test step 1- 1.3
    # testresult.append(["[.] Fehlerspeichereinträge sind nicht vom NWDF-Master freigegeben", ""])
    # testresult.append(["[+]  Setze Zykluszeit der Botschaft Systeminfo_01 auf 7000ms (gültig)", ""])
    # testresult.append(["Setze Zykluszeit auf %sms" % max_valid_cycletime, "INFO"])
    # period_var.set(max_valid_cycletime)
    #
    # testresult.append(["[.] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    # time.sleep(float(wait_time) / 1000)
    #
    # testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    # testresult.append(canape_diag.checkEventMemoryEmpty())
    # testresult.append(["[-0]", ""])
    #
    # # # test step 2-2.3
    # testresult.append(["[.] Fehlerspeichereinträge sind vom NWDF-Master freigegeben:Systeminfo_01_SI_NWDF_30 =1 ", ""])
    # hil.Systeminfo_01__SI_NWDF_30__value.set(1)
    #
    # testresult.append(["[+] Setze Zykluszeit der Botschaft Systeminfo_01  auf 0ms (ungültig)", ""])
    # period_var.set(0)
    #
    # testresult.append(["[.] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    # time.sleep(float(wait_time) / 1000)
    #
    # testresult.append(["[.] Lese Fehlerspeicher (Netzwerkdiagnosefreigabe DTC aktiv)", ""])
    # testresult.append(canape_diag.checkEventMemory(active_dtcs))
    # testresult.append(["[-0]", ""])
    #
    # # test step 3-3.2
    # testresult.append(["[.] Setze Zykluszeit der Botschaft Systeminfo_01 auf 1000ms (original)", ""])
    # testresult.append(["Setze Zykluszeit auf %sms" % cycle_time, ""])
    # period_var.set(cycle_time)
    #
    # testresult.append(["[+] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    # time.sleep(float(wait_time) / 1000)
    #
    # testresult.append(["[.] Lese Fehlerspeicher (Netzwerkdiagnosefreigabe DTC passiv)", ""])
    # testresult.append(canape_diag.checkEventMemory(passive_dtcs))
    # testresult.append(["[-0]", ""])
    #
    # # test step 4-4.8
    # testresult.append(["[.] Ausblendbedingung Unterschreitung der Unterspannungsgrenze erfüllt ist", ""])
    # testresult.append(["[+] Fehlerspeichereinträge sind nicht vom NWDF-Master freigegeben:Systeminfo_01_SI_NWDF_30 =0", ""])
    # hil.Systeminfo_01__SI_NWDF_30__value.set(0)
    #
    # testresult.append(["[.] Setze hil.vbat_cl30__V == 5.7V", ""])
    # hil.vbat_cl30__V.set(5.7)
    #
    # testresult.append(["[.] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    # time.sleep(float(wait_time) / 1000)
    #
    # testresult.append(["[.] Lese Fehlerspeicher (Netzwerkdiagnosefreigabe aktiv DTC)", ""])
    # testresult.append(canape_diag.checkEventMemory(active_dtcs_uv, ticket_id='Fehler Id:EGA-PRM-275'))
    #
    # testresult.append(["[.] Setze hil.vbat_cl30__V == 13V zurück", ""])
    # hil.vbat_cl30__V.set(13)
    #
    # testresult.append(["[.] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    # time.sleep(float(wait_time) / 1000)
    #
    # testresult.append(["[.] Lese Fehlerspeicher (Netzwerkdiagnosefreigabe passiv DTC)", ""])
    # testresult.append(canape_diag.checkEventMemory(Passiv_dtcs_uv, ticket_id='Fehler Id:EGA-PRM-275'))
    #
    # testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    # testresult.append(canape_diag.resetEventMemory(wait=True))
    # testresult.append(["[-0]", ""])
    #
    # # test step 5-5.7
    # testresult.append(["[.] Ausblendbedingung Überschreitung der Überspannungsgrenze erfüllt ", ""])
    # testresult.append(["[+] Fehlerspeichereinträge sind nicht vom NWDF-Master freigegeben:Systeminfo_01_SI_NWDF_30 =0", ""])
    #
    # testresult.append(["[.] Setze hil.vbat_cl30__V == 18V", ""])
    # hil.vbat_cl30__V.set(18)
    #
    # testresult.append(["[.] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    # time.sleep(float(wait_time) / 1000)
    #
    # testresult.append(["[.] Lese Fehlerspeicher (Netzwerkdiagnosefreigabe aktiv DTC)", ""])
    # testresult.append(canape_diag.checkEventMemory(active_dtcs_ov, ticket_id='Fehler Id:EGA-PRM-276'))
    #
    # testresult.append(["[.] Setze hil.vbat_cl30__V == 13V zurück", ""])
    # hil.vbat_cl30__V.set(13)
    #
    # testresult.append(["[.] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    # time.sleep(float(wait_time) / 1000)
    #
    # testresult.append(["[.] Lese Fehlerspeicher (Netzwerkdiagnosefreigabe passiv DTC )", ""])
    # testresult.append(canape_diag.checkEventMemory(Passiv_dtcs_ov, ticket_id='Fehler Id:EGA-PRM-276'))
    # testresult.append(["[-0]", ""])
    #
    # # test step 7
    # testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    # testresult.append(canape_diag.resetEventMemory(wait=True, ticket_id='Fehler Id:EGA-PRM-276'))
    #
    # # test step 8
    # testresult.append(["[.] Warte 1000ms", ""])
    # time.sleep(1)
    #
    # # test step 9
    # testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    # testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-276'))

    # TEST POST CONDITIONS ####################################################

    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    hil.cl30_on__.set(1)
    hil.cl15_on__.set(1)

    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Setze Systeminfo_01_SI_NWDF_30 auf 1", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["[.] Setze OTAMC_D_01 VehicleProtectedEnvironment auf 0", ""])
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(0)

    testresult.append(["[.] Setze ORU_Control_A_01 OnlineRemoteUpdateControlA auf 4", ""])
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(4)

    testresult.append(["[.] setze ORU_Control_D_01 OnlineRemoteUpdateControlD auf 4", ""])
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(4)

    testresult.append(["[.] VDSO_Vx3d = 32766 (0 km/h) Senden", ""])
    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag = testenv.getCanapeDiagnostic()
    canape_diag.disableTesterPresent()

    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(canape_diag.resetEventMemory())
    testresult.append(canape_diag.checkEventMemoryEmpty())

    ####################################################################################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])

    # test step 1
    testresult.append(["[.] Warte maximum tMSG_CYCLE (5000ms)", ""])
    time.sleep(5)

    # test step 2
    testresult.append(["[.] Setze Systeminfo_01_SI_NWDF_30 = 0", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(0)

    # test step 3
    testresult.append(["[.] Warte 2000ms)", ""])
    time.sleep(2)

    # test step 4
    testresult.append(["[.] Setze  ORU_Control_A_01 Zykluszeit auf 0.", ""])
    hil.ORU_Control_A_01__period.setState("aus")

    # test step 5
    testresult.append(["[.] Warte 4500ms (tMSG_Timeout)", ""])
    time.sleep(4.500)

    # test step 6
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 7
    testresult.append(["[.] Setze Zykluszeit der Botschaft Systeminfo_01 auf 0 ms", ""])
    hil.Systeminfo_01__period.set(2)
    hil.Systeminfo_01__period.setState("aus")

    # test step 8
    testresult.append(["[.] Warte 5000ms (tMSG_CYCLE)", ""])
    time.sleep(5)

    # test step 9
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 10
    testresult.append(["[.] Warte 500 ms (tDiagStart) + 200 ms (Toleranz)", ""])
    time.sleep(0.700)

    # test step 11
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 12
    testresult.append(["[.] Warte 4500ms (Rest tMSG_Timeout)", ""])
    time.sleep(4.5)

    # test step 13
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemory(ORU_A_DTC_Aktiv, ticket_id="EGA-PRM-300"))

    # test step 14
    testresult.append(["[.]  Warte 500 ms (Rest von tMSG_Timeout)", ""])
    time.sleep(0.500)

    # test step 15
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(canape_diag.checkEventMemory(ORU_A_DTC_Aktiv + SySInfo_DTC_Aktiv))

    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    cal = None
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print "Done."
