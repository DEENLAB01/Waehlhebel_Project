# *******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : PFIFF_Ticket_9064250.py
# Title   : PFIFF_Ticket_9064250
# Task    : der Messung wechselt das NWDF-Bit von 1 auf 0

# Author  : Mohamed Abdul Karim
# Date    : 10.08.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************** Version ***********************************
# ******************************************************************************
# Rev. | Date        | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 10.08.2022 | Mohammed | initial

# ******************************************************************************

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
    period_var = hil.ORU_Control_A_01__period
    cycle_time = period_var.value_lookup["an"]
    max_valid_cycletime = getMaxValidPeriod(cycletime_ms=cycle_time)
    wait_time = 5000  # CAN_3244
    aktiv_dtc = [(0xE00107, 0x27)]
    passiv_dtc = [(0xE00107, 0x26)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("PFIFF_9064250")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: KL15 und KL30 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1- 1.5
    testresult.append(["[.] Fehlerspeichereinträge sind vom NWDF-Master freigegeben", ""])
    testresult.append(["[+]  Setze Zykluszeit der Botschaft ORU_Control_A auf 500ms (gültig)", ""])
    testresult.append(["\xa0 Setze Zykluszeit auf %sms" % cycle_time, ""])
    period_var.set(cycle_time)

    testresult.append(["[.] Setze hil.cl15_on__ auf 0", ""])
    hil.cl15_on__.set(0)

    testresult.append(["[.] Fehlerspeichereinträge sind nicht vom NWDF-Master freigegeben:Systeminfo_01_SI_NWDF_30 =0", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(0)

    testresult.append(["[.] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    time.sleep(float(wait_time) / 1000)

    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())
    testresult.append(["[-0]", ""])

    # test step 2- 2.3
    t1 = time.time() #####
    print ("T1", t1)
    testresult.append(["[.] Fehlerspeichereinträge sind vom NWDF-Master freigegeben:Systeminfo_01_SI_NWDF_30 =1", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["[.] Setze hil.cl15_on__ auf 1 ", ""])
    hil.cl15_on__.set(1)

    testresult.append(["[.] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    time.sleep(float(wait_time) / 1000)

    testresult.append(["[.] Lese Fehlerspeicher (Timeout DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(aktiv_dtc))
    testresult.append(["[-0]", ""])

    # test step 3-3.3
    t2 = time.time()
    print ("T2", t2)
    testresult.append(["[.] Fehlerspeichereinträge sind vom NWDF-Master freigegeben:Systeminfo_01_SI_NWDF_30 =0 ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(0)

    testresult.append(["[+] Setze Zykluszeit der Botschaft ORU_Control_A_01 auf 0ms (ungültig)", ""])
    period_var.setState('aus')

    testresult.append(["[.] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    time.sleep(float(wait_time) / 1000)

    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())
    testresult.append(["[-0]", ""])
    t3=time.time()
    print ("T3", t3)

    tNWDF_Timeout = t1-t2-t3
    print ("tNWDF_Timeout", tNWDF_Timeout)

    # test step 3-3.3
    testresult.append(["[.] Fehlerspeichereinträge sind nicht vom NWDF-Master freigegeben:Systeminfo_01_SI_NWDF_30 =0 ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(0)

    testresult.append(["[.] Warte maximum tMSG_CYCLE (%sms)" % (wait_time), ""])
    time.sleep(float(wait_time) / 1000)

    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())
    testresult.append(["[-0]", ""])

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
