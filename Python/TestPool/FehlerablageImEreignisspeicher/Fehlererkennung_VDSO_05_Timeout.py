# #*******************************************************************************
# # -*- coding: latin-1 -*-
# #
# # File    : Fehlererkennung_VDSO_05_Timeout.py
# # Title   : Fehlererkennung_VDSO_05_Timeout
# # Task    : Timeouttest für VDSO_05  Message
#
# Author  : Mohammed Abdul Karim
# Date    : 28.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 28.05.2021  | A. Neumann | initial created Timeout Test
# 1.1  | 27.07.2021  | Mohammed   | Added TestSpec_ID
# 1.2  | 22.11.2021  | Mohammed   | Rework
# 1.3  | 21.12.2021  | Mohammed   | Added Fehler Id
# 1.4  | 13.01.2022  | Mohammed   | Added Precontion Systeminfo_01__SI_NWD, Systeminfo_01__SI_NWDF_30
# 1.5  | 27.01.2022  | Mohammed   | Corrected Timing
# 1.9  | 04.08.2022 | Mohammed     | Change TestSpec Name
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
    period_var = hil.VDSO_05__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 5000  # CAN_3244

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_171")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[-] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["[+] Prüfe, dass kein Fehler gesetzt wird bei gültiger Zyklusveränderung", ""])
    testresult.append(["[+] Ändere Zykluszeit und prüfe Fehlerspeicher", ""])
    testresult.append(["Setze Zykluszeit auf %sms" % max_valid_cycletime, "INFO"])
    hil.VDSO_05__period.set(400)

    testresult.append(["Warte maximum tMSG_CYCLE (%sms)" % (wait_time), "INFO"])
    time.sleep(5)
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["[-] Prüfe, dass ein Fehler gesetzt wird bei Timeout", ""])
    testresult.append(["[+] Ändere Zykluszeit und prüfe Fehlerspeicher", ""])
    testresult.append(["Setze Zykluszeit auf 0ms", "INFO"])
    hil.VDSO_05__period.set(0)
    testresult.append(["Warte maximum tMSG_CYCLE (%sms)" % (wait_time), "INFO"])
    time.sleep(5)
    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory([(0xE00104, 0x27)], ticket_id='FehlerId:EGA-PRM-145'))

    testresult.append(["[-] Prüfe, dass Fehler zurückgesetzt wird bei erneutem richtigen Empfangen", ""])
    testresult.append(["[+] Ändere Zykluszeit und prüfe Fehlerspeicher", ""])
    testresult.append(["Setze Zykluszeit auf 5ms", "INFO"])
    hil.VDSO_05__period.set(5)
    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC passiv)", ""])
    testresult.append(canape_diag.checkEventMemory([(0xE00104, 0x27)], ticket_id='FehlerId:EGA-PRM-145'))
    testresult.append(["Warte maximum tMSG_CYCLE (%sms)" % (wait_time), "INFO"])
    time.sleep(5)

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(["Warte  1000ms)", "INFO"])
    time.sleep(1)
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


