#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Fehlerablage_Netzwerkdiagnosefreigabe.py
# Title   : Fehlerablage_Netzwerkdiagnosefreigabe
# Task    : Fehlerablage Netzwerkdiagnosefreigabe

# Author  : Mohamed Abdul Karim
# Date    : 03.03.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 27.07.2021 | Mohammed | initial

#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()

# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
import time
import data_common as dc

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()

    # Initialize variables ####################################################
    period_var = hil.Systeminfo_01__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 5000  # CAN_3244

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_198")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: KL15 und KL30 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    # test step 1, 1.1
    testresult.append(["[+] Prüfe, dass kein Fehler gesetzt wird bei gültiger Zyklusveränderung", ""])
    testresult.append(["[+] Ändere Zykluszeit und prüfe Fehlerspeicher", ""])
    testresult.append(["Setze Zykluszeit auf %sms" % max_valid_cycletime, "INFO"])
    period_var.set(max_valid_cycletime)

    testresult.append(["[.] Setze Systeminfo_01_SI_NWDF_30 =1", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    # test step 1.2
    testresult.append(["Warte maximum tMSG_CYCLE (%sms)" % (wait_time), "INFO"])
    time.sleep(float(wait_time) / 1000)

    # test step 2
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 3
    testresult.append(["[-] Prüfe, dass ein Fehler gesetzt wird bei Timeout", ""])
    testresult.append(["[+] Ändere Zykluszeit und prüfe Fehlerspeicher", ""])
    testresult.append(["Setze Zykluszeit auf 0ms", "INFO"])
    period_var.set(0)
    testresult.append(["Warte maximum tMSG_CYCLE (%sms)" % (wait_time), "INFO"])
    time.sleep(float(wait_time) / 1000)

    # test step 3.1
    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    active_dtcs = [(0xE00106, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs))

    # test step 4
    testresult.append(["[-] Prüfe, dass Fehler zurückgesetzt wird bei erneutem richtigen Empfangen", ""])
    testresult.append(["[+] Ändere Zykluszeit und prüfe Fehlerspeicher", ""])
    testresult.append(["Setze Zykluszeit auf %sms" % cycle_time, "INFO"])
    period_var.set(cycle_time)
    testresult.append(["Warte maximum tMSG_CYCLE (%sms)" % (wait_time), "INFO"])
    time.sleep(float(wait_time) / 1000)

    # test step 4.1
    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC passiv)", ""])
    passive_dtcs = [(0xE00106, 0x26)]
    testresult.append(canape_diag.checkEventMemory(passive_dtcs))

    # test step 5
    testresult.append(["[-] Prüfe, Ausblendbedingung:Unterschreitung der Unterspannungsgrenze erfüllt ist", ""])
    testresult.append(["[+] Ändere Zykluszeit und prüfe Fehlerspeicher", ""])

    # test step 5.1
    testresult.append(["Setze Zykluszeit auf 0ms", "INFO"])
    period_var.set(0)
    testresult.append(["Warte maximum tMSG_CYCLE (%sms)" % (wait_time), "INFO"])
    time.sleep(float(wait_time) / 1000)

    # test step 5.2
    testresult.append(["[.] Setze hil.vbat_cl30__V == 5.7V", ""])
    hil.vbat_cl30__V.set(5.7)
    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    active_dtcs = [(0xE00106, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs))

    # test step 5.4
    testresult.append(["[.] Setze hil.vbat_cl30__V == 13V", ""])
    hil.vbat_cl30__V.set(13)
    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    active_dtcs = [(0xE00106, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs))

    # test step 6
    testresult.append(["[-] Prüfe, Ausblendbedingung: Überschreitung der Überspannungsgrenze erfüllt ist", ""])
    testresult.append(["[+] Ändere Zykluszeit und prüfe Fehlerspeicher", ""])

    # test step 6.1
    testresult.append(["Setze Zykluszeit auf 0ms", "INFO"])
    period_var.set(0)
    testresult.append(["Warte maximum tMSG_CYCLE (%sms)" % (wait_time), "INFO"])
    time.sleep(float(wait_time) / 1000)

    # test step 6.2
    testresult.append(["[.] Setze hil.vbat_cl30__V == 5.7V", ""])
    hil.vbat_cl30__V.set(18)
    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    active_dtcs = [(0xE00106, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs))

    # test step 5.4
    testresult.append(["[.] Setze hil.vbat_cl30__V == 13V", ""])
    hil.vbat_cl30__V.set(13)
    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    active_dtcs = [(0xE00106, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs))

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    cal = None
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()

