# *******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : TimeOut_SystemInfo_01_Confirmation.py
# Title   : TimeOut_SystemInfo_01_Confirmation
# Task    : Timeout_SystemInfo_01 Fehlererkennung für Confirmed DTC im Fehlerspeicher

# Author  : Mohamed Abdul Karim
# Date    : 03.03.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************** Version ***********************************
# ******************************************************************************
# Rev. | Date        | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 22.08.2022 | Mohammed | initial

# ******************************************************************************

from _automation_wrapper_ import TestEnv

testenv = TestEnv()

# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
import time
import functions_hil

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()
    func_hil = functions_hil.FunctionsHil(testenv, hil)

    # Initialize variables ####################################################
    period_var = hil.Systeminfo_01__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 5000  # CAN_3244
    active_dtcs = [(0xE00106, 0x27)]
    passive_dtcs = [(0xE00106, 0x26)]
    confirme_dtcs = [(0xE00106, 0x2F)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_209xx")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: KL15 und KL30 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1- 1.3
    testresult.append(["[.] Fehlerspeichereinträge sind nicht vom NWDF-Master freigegeben", ""])
    testresult.append(["[+]  Setze Zykluszeit der Botschaft Systeminfo_01 auf 7000ms (gültig)", ""])
    testresult.append(["Setze Zykluszeit auf %sms" % max_valid_cycletime, "INFO"])
    period_var.set(max_valid_cycletime)

    testresult.append(["[.] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    time.sleep(float(wait_time) / 1000)

    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())
    testresult.append(["[-0]", ""])

    # # test step 2-2.3
    testresult.append(["[.] Fehlerspeichereinträge sind vom NWDF-Master freigegeben:Systeminfo_01_SI_NWDF_30 =1 ", ""])
    # hil.Systeminfo_01__SI_NWDF_30__value.set(1)
     ###############################################################
    # state = "aus"
    # hil.Diagnose_01__period.setState(state)
    # hil.NVEM_12__period.setState(state)
    # hil.Dimmung_01__period.setState(state)
    # hil.NM_Airbag__period.setState(state)
    # hil.OBD_03__period.setState(state)
    # hil.OBD_04__period.setState(state)
    # hil.ORU_Control_A_01__period.setState(state)
    # hil.ORU_Control_D_01__period.setState(state)
    # hil.OTAMC_D_01__period.setState(state)
    # #hil.Systeminfo_01__period.setState(state)
    # hil.NM_HCP1__period.setState(state)

    testresult.append(["[+] Setze Zykluszeit der Botschaft Systeminfo_01  auf 0ms (ungültig)", ""])
    period_var.set(0)

    testresult.append(["[.] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    time.sleep(float(wait_time) / 1000)

    testresult.append(["[.] Lese Fehlerspeicher (Netzwerkdiagnosefreigabe DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(active_dtcs))
    testresult.append(["[-0]", ""])

    # test step 3
    testresult.append(["[.] Perform 3 OCY: DEM_OPCYC_IGNITION", ""])
    func_hil.perform3OYC()

    # test step 4
    testresult.append(["[.] Lese Fehlerspeicher (Aktiv und Confirme DTC)", ""])
    testresult.append(canape_diag.checkEventMemory(confirme_dtcs))

    # test step 7
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # test step 8
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1)

    # test step 9
    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST POST CONDITIONS ####################################################
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
