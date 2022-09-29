#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Fehlererkennung_Timeout_Bus_off.py
# Title   : Fehlererkennung Timeout Bus Off
# Task    : Timeouttest of HIL-Tx => ECU-Rx Signals of CAN Message Timeout Bus Off

# Author  : Mohammed Abdul Karim
# Date    : 24.08.2021
# # Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name        | Description
#------------------------------------------------------------------------------
# 1.0  | 24.08.2021  | Mohammed    | initial
# 1.1  | 04.11.2021  | Mohammed    | Rework
# 1.2  | 21.12.2021  | Mohammed    | Added Fehler Id
# 1.3  | 21.12.2021  | Mohammed    | Added Sishift_01 DTC
# 1.4  | 30.08.2022  | Mohammed    | Added t_diag time
#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()

# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
import time
import data_common as dc
import functions_gearselection
import functions_nm

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    testenv.startupECU()  # startup before cal vars are called
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    canape_diag = testenv.getCanapeDiagnostic()
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    wait_time = 0.500  # CAN_3244
    active_dtcs = [(0xE00100, 0x27), (0xE00101, 0x27)]
    passive_dtcs = [(0xE00100, 0x26), (0xE00101, 0x26)]
    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_207")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen:KL30 und KL15 an ", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[.] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    #test step 1
    testresult.append(["[.] Starte zyklisches Senden von Botschaften", ""])
    hil.can0_HIL__HIL_TX__enable.set(1)

    # test step 2-2.1
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(["\x0aPrüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["[+] Warte 2s (tDiagStart=500ms sollte abgelaufen sein, Systeminfo_01 Zykluszeit = 1000ms)", ""])
    time.sleep(2)
    testresult.append(["[-0]", ""])

    # test step 3
    testresult.append(["[.] Schalte Senden von RX Signalen (HiL --> ECU) aus", ""])
    #func_nm.hil_ecu_tx_off_state("aus")
    hil.can0_HIL__HIL_TX__enable.set(0)

    # test step 4
    testresult.append(["[.] Warte 500ms (Initial Timeout) (%sms)" % (wait_time), ""])
    time.sleep(wait_time)

    # test step 5
    testresult.append(["[.] Lese Fehlerspeicher aus ", ""])
    testresult.append(["\x0aPrüfe Aktiv DTC:  0xE00100 und 0xE00101 im Fehlerspeicher", ""])
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='FehlerId:EGA-PRM-230'))

    # test step 6
    testresult.append(["[.] Sende erneut zyklisch Botschaften", ""])
    hil.can0_HIL__HIL_TX__enable.set(1)

    # test step 7
    testresult.append(["[.] Warte 500 ms (Initial Timeout) (%sms)" % (wait_time), ""])
    time.sleep(wait_time)

    # test step 8
    testresult.append(["[.] Lese Fehlerspeicher aus", ""])
    testresult.append(["\x0aPrüfe Passiv DTC:  0xE00100 und 0xE00101 im Fehlerspeicher", ""])
    testresult.append(canape_diag.checkEventMemory(passive_dtcs, ticket_id='FehlerId:EGA-PRM-230'))

    # test step 9
    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # test step 10
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1)

    # test step 11
    testresult.append(["[.] Lese Fehlerspeicher aus ", ""])
    testresult.append(["\x0aPrüfe Fehlerspeicher leer ist", ""])
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

