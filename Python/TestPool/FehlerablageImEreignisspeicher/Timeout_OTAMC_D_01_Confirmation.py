#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Timeout_OTAMC_D_01_Confirmation.py
# Title   : Timeout_OTAMC_D_01_Confirmation
# Task    : Timeout_OTAMC_D_01 Fehlererkennung für Confirmed DTC im Fehlerspeicher
#
# Author  : Mohammed Abdul Karim
# Date    : 04.08.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 04.08.2022  | Mohammed | initial
#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()

# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
from ttk_checks import basic_tests
import functions_gearselection
import time
from time import time as t
import functions_hil
from functions_diag import HexList  # @UnresolvedImport
import functions_nm

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_hil = functions_hil.FunctionsHil(testenv, hil)
    func_nm = functions_nm.FunctionsNM(testenv)
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    period_var = hil.OTAMC_D_01__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 15000  # CAN_3244
    aktiv_dtc = [(0xE00109, 0x27)]
    passiv_dtc = [(0xE00109, 0x24)]
    confirme_dtcs = [(0xE00109, 0x2F)]
    curr_value = func_nm.low_current()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_404")

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
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    #testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Setze Zykluszeit der Botschaft OTAMC_D auf 320ms (gültig)", ""])
    testresult.append(["\xa0 Setze Zykluszeit auf %sms" % cycle_time, ""])
    period_var.set(cycle_time)

    # test step 2
    testresult.append(["[.] Warte 1000 ms", ""])
    time.sleep(1.0)

    # test step 3
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 4
    testresult.append(["[.] Setze Zykluszeit der Botschaft OTAMC_D auf 0ms (ungültig)", ""])
    period_var.set(0)

    # test step 5
    testresult.append(["[.] Warte 2880 ms (tMSG_Timeout: n-q+1, n=10, q=2) + 300ms (Tollerenz)", ""])
    time.sleep(3.18)

    # test step 6
    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc))

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
                                  descr="\x0aPrüfe, dass Strom zwischen 0mA und 6mA liegt",))

    testresult.append(["[.] Warte 2 s nach WakeUp", ""])
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(2)

    testresult.append(["[.] Setze Zykluszeit der Botschaft OTAMC_D auf 0ms (ungültig)", ""])
    hil.OTAMC_D_01__period.setState('aus')

    testresult.append(["[.] Warte 2880 ms (tMSG_Timeout: n-q+1, n=10, q=2) + 300ms (Tollerenz)", ""])
    time.sleep(3.18)

    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc, mode="ONE_OR_MORE"))
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
                                  descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt",))

    testresult.append(["[.] Warte 2 s nach WakeUp", ""])
    descr, verdict = func_gs.switchAllRXMessagesOn()
    hil.cl15_on__.set(1)
    time.sleep(2)

    testresult.append(["[.] Setze Zykluszeit der Botschaft OTAMC_D auf 0ms (ungültig)", ""])
    hil.OTAMC_D_01__period.setState('aus')

    testresult.append(["[.] Warte 2880 ms (tMSG_Timeout: n-q+1, n=10, q=2) + 300ms (Tollerenz)", ""])
    time.sleep(3.18)

    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc, mode="ONE_OR_MORE"))
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

    testresult.append(["[.] Setze Zykluszeit der Botschaft OTAMC_D auf 0ms (ungültig)", ""])
    hil.OTAMC_D_01__period.setState('aus')

    testresult.append(["[.] Warte 2880 ms (tMSG_Timeout: n-q+1, n=10, q=2) + 300ms (Tollerenz)", ""])
    time.sleep(3.18)

    testresult.append(["[.] Lese Fehlerspeicher (Aktiv und Confirme DTC )", ""])
    testresult.append(canape_diag.checkEventMemory(confirme_dtcs, mode="ONE_OR_MORE"))

    testresult.append(["[.] Setze Zykluszeit der Botschaft OTAMC_D_01 auf 500ms (gültig)", ""])
    testresult.append(["\xa0 Setze Zykluszeit auf %sms" % cycle_time, ""])
    period_var.set(cycle_time)
    testresult.append(["[-0]", ""])

    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(2.0)

    # test step 12
    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # test step 13
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1.0)

    # test step 14
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

