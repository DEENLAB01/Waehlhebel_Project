#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_EI_Rx_Signals_ORU_01_Timeout.py
# Title   : CAN_EI_Rx_Signals_ORU_01_Timeout
# Task    : Timeouttest of HIL-Tx => ECU-Rx Signals of CAN Message ORU_01

# Author  : A.Neumann
# Date    : 28.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.1  | 28.05.2021  | A. Neumann | initial created Timeout Test
# 1.1  | 27.07.2021 | Mohammed | Added TestSpec_ID
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
    period_var = hil.ORU_01__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 5000  # CAN_3244
    exp_dtc = 12345  # TODO

    # set Testcase ID #########################################################
    #setTestcaseId(testresult, "TestSpec_196")
    testresult.setTestcaseId("TestSpec_196")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["[+] Prüfe, dass kein Fehler gesetzt wird bei gültiger Zyklusveränderung", ""])
    testresult.append(["[+] Ändere Zykluszeit und prüfe Fehlerspeicher", ""])
    testresult.append(["Setze Zykluszeit auf %sms" % max_valid_cycletime, "INFO"])
    period_var.set(max_valid_cycletime)
    testresult.append(["Warte maximum tMSG_CYCLE (%sms)" % (wait_time), "INFO"])
    time.sleep(float(wait_time) / 1000)
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["[-] Prüfe, dass ein Fehler gesetzt wird bei Timeout", ""])
    testresult.append(["[+] Ändere Zykluszeit und prüfe Fehlerspeicher", ""])
    testresult.append(["Setze Zykluszeit auf 0ms", "INFO"])
    period_var.set(0)
    testresult.append(["Warte maximum tMSG_CYCLE (%sms)" % (wait_time), "INFO"])
    time.sleep(float(wait_time) / 1000)
    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory([[exp_dtc, dc.DTCactive]]))

    testresult.append(["[-] Prüfe, dass Fehler zurückgesetzt wird bei erneutem richtigen Empfangen", ""])
    testresult.append(["[+] Ändere Zykluszeit und prüfe Fehlerspeicher", ""])
    testresult.append(["Setze Zykluszeit auf %sms" % cycle_time, "INFO"])
    period_var.set(cycle_time)
    testresult.append(["Warte maximum tMSG_CYCLE (%sms)" % (wait_time), "INFO"])
    time.sleep(float(wait_time) / 1000)
    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC passiv)", ""])
    testresult.append(canape_diag.checkEventMemory([[exp_dtc, dc.DTCpassive]]))

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

