#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Bz_Fehler_ORU_Control_A_Confirmation.py
# Title   : Bz_Fehler_ORU_Control_A_Confirmation
# Task    : Fehlererkennung BZ-Fehler ORU_Control_A für Confirmed DTC im Fehlerspeicher

# Author  : Mohammed Abdul Karim
# Date    : 04.08.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 04.08.2022 | Mohammed | initial created BZ-Fehler Test for Confirmed DTC
#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()
import functions_gearselection
# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
from ttk_checks import basic_tests
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
    period_var = hil.ORU_Control_A_01__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 1500
    activ_dtc = [(0xE0010A, 0x27)]
    confirme_dtc = [(0xE0010A, 0x2F)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_416")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: LK30 und Kl15 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    # test step 1
    testresult.append(["[.] Setze Zykluszeit der Botschaft ORU_Control_A_01 auf 500ms " ""])
    testresult.append(["\xa0 Setze Zykluszeit auf %sms" % cycle_time, ""])
    period_var.set(cycle_time)

    # test step 2
    testresult.append(["[.] Warte 1500 ms", ""])
    time.sleep(1.5)

    # test step 3
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 4
    testresult.append(["[.] Halte ORU_Control_A_01:ORU_Control_A_01_BZ an (Setze Inkrementierung des Botschaftszählers aus)", ""])
    hil.ORU_Control_A_01__ORU_Control_A_01_BZ__switch.set(1)

    # test step 5
    testresult.append(["[.] Warte 4500 ms (tMSG_Timeout: n-q+1, n=10, q=2) + 420ms (Tollerenz)", ""])
    time.sleep(4.92)

    # test step 6
    testresult.append(["[.] Lese Fehlerspeicher (0xE0010A DTC activ)", ""])
    testresult.append(canape_diag.checkEventMemory(activ_dtc))

    # test step 7-7.6
    testresult.append(["\x0a Führe 3 OP-PowerCycle (ECU_Sleep (Ruhestrom auswerten) -> ECU_WakeUp) durch:", ""])
    testresult.append(["[.] Führe ersten OP-PowerCycle (ECU_Sleep  -> ECU_WakeUp) durch", ""])
    hil.cl15_on__.set(0)
    time.sleep(.200)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(14)

    testresult.append(["[+] Prüfe Ruhestrom während ECU_Sleep", ""])
    testresult.append(basic_tests.checkRange(value=hil.cc_mon__A,
                                             min_value=0.0,  # 0mA
                                             max_value=0.006,  # 6mA
                                             descr="\x0aPrüfe, dass Strom zwischen 0mA und 6mA liegt", ))

    testresult.append(["[.] Warte 2 s nach WakeUp", ""])
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(2)

    testresult.append(["[.] Halte ORU_Control_A_01:ORU_Control_A_01_BZ an (Setze Inkrementierung des Botschaftszählers aus)", ""])
    hil.ORU_Control_A_01__ORU_Control_A_01_BZ__switch.set(1)

    testresult.append(["[.] Warte 4500 ms (tMSG_Timeout: n-q+1, n=10, q=2) + 420ms (Tollerenz)", ""])
    time.sleep(4.92)

    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(activ_dtc, mode="ONE_OR_MORE"))
    testresult.append(["[-0]", ""])

    # test step 8-8.5
    testresult.append(["[.] Führe zweiten OP-PowerCycle (ECU_Sleep -> ECU_WakeUp)", ""])
    hil.cl15_on__.set(0)
    time.sleep(.200)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(14)

    testresult.append(["[+] Prüfe Ruhestrom während ECU_Sleep", ""])
    testresult.append(basic_tests.checkRange(value=hil.cc_mon__A,
                                             min_value=0.0,  # 0mA
                                             max_value=0.006,  # 6mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt", ))

    testresult.append(["[.] Warte 2 s nach WakeUp", ""])
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(2)

    testresult.append(["[.] Halte ORU_Control_A_01:ORU_Control_A_01_BZ an (Setze Inkrementierung des Botschaftszählers aus)", ""])
    hil.ORU_Control_A_01__ORU_Control_A_01_BZ__switch.set(1)

    testresult.append(["[.] Warte 4500 ms (tMSG_Timeout: n-q+1, n=10, q=2) + 420ms (Tollerenz)", ""])
    time.sleep(4.92)

    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(activ_dtc, mode="ONE_OR_MORE"))
    testresult.append(["[-0]", ""])

    # test step 9-9.5
    testresult.append(["[.] Führe dritten OP-PowerCycle (ECU_Sleep -> ECU_WakeUp)", ""])
    hil.cl15_on__.set(0)
    time.sleep(.200)
    descr, verdict = func_gs.switchAllRXMessagesOff()
    testresult.append([descr, verdict])
    time.sleep(14)

    testresult.append(["[+] Prüfe Ruhestrom während ECU_Sleep", ""])
    testresult.append(basic_tests.checkRange(value=hil.cc_mon__A,
                                             min_value=0.0,  # 0mA
                                             max_value=0.006,  # 6mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt", ))

    testresult.append(["[.] Warte 2 s nach WakeUp", ""])
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(2)

    testresult.append(["[.] Halte ORU_Control_A_01:ORU_Control_A_01_BZ an (Setze Inkrementierung des Botschaftszählers aus)", ""])
    hil.ORU_Control_A_01__ORU_Control_A_01_BZ__switch.set(1)

    testresult.append(["[.] Warte 4500 ms (tMSG_Timeout: n-q+1, n=10, q=2) + 420ms (Tollerenz)", ""])
    time.sleep(4.92)

    testresult.append(["[.] Lese Fehlerspeicher (Aktiv und Confirme DTC )", ""])
    testresult.append(canape_diag.checkEventMemory(confirme_dtc, mode="ONE_OR_MORE"))

    testresult.append(["[.] Setze ORU_Control_A_01::ORU_Control_A_01_BZ fort (Setze Inkrementierung des Botschaftszählers wieder fort)", ""])
    hil.ORU_Control_A_01__ORU_Control_A_01_BZ__switch.set(0)
    testresult.append(["[-0]", ""])

    # test step 10
    testresult.append(["[.] Warte 3000ms", ""])
    time.sleep(3.0)

    # test step 11
    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # test step 12
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1.5)

    # test step 13
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

