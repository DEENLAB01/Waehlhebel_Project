#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Fehlerablage_Klemmenstatus.py
# Title   : Fehlerablage_Klemmenstatus
# Task    : Fehlerablage Klemmenstatus

# Author  : Mohammed Abdul Karim
# Date    : 05.11.2021
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 05.11.2021  | Mohammed   | initial
# 1.1  | 11.01.2022  | Mohammed   | Rework
# 1.2  | 27.01.2022  | Mohammed   | Rework after TestSpec Updated
# 1.3  | 24.02.2022  | Mohammed   | Updated DTC
# 1.4  | 17.08.2022  | Mohammed   | Added Fehler ID
#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()

# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
import time
import data_common as dc
import functions_hil

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()
    testenv.startupECU()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_hil = functions_hil.FunctionsHil(testenv, hil)
    canape_diag = testenv.getCanapeDiagnostic()

    # Initialize variables ####################################################
    failure_set_time = 1  # CAN_3244
    voltage_ov = dc.voltage_range['Overvoltage']
    set_voltage_invalid_ov = float(voltage_ov['voltage']) + float(voltage_ov['voltage']) * float(voltage_ov['tol_perc'] / 100.0) + float(voltage_ov['hil_tol_ma'])
    active_dtcs = [(0x800100, 0x27), (0x800101, 0x27)]
    passiv_dtcs = [(0x800100, 0x26), (0x800101, 0x26)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_210")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte KL30 an (KL15 aus)", ""])
    hil.cl15_on__.set(0)

    testresult.append(["[.] Lese Fehlerspeicher (muss leer sein)", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[.] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    testresult.append(["[.] Setze Spannung auf %sV (Überspannung)" % set_voltage_invalid_ov, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_invalid_ov, 0.1, 0.02)
    testresult.append([descr, verdict])

    # test step 2
    testresult.append(["[.] Lese Fehlerspeicher (leer)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # test step 3
    testresult.append(["[.] KL15 ein", ""])
    hil.cl15_on__.set(1)

    # test step 4
    testresult.append(["[.] Warte %ss - Fehlererkennungszeit" % failure_set_time, ""])
    time.sleep(failure_set_time)

    # test step 5
    testresult.append(["[.] Lese Fehlerspeicher ", ""])
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='Fehler Id:EGA-PRM-276'))

    # test step 6
    testresult.append(["[.] hil.vbat_cl30__V == 13V (gültiger Bereich)" , ""])
    hil.vbat_cl30__V.set(13.0)

    testresult.append(["[.] Warte 1 Sekunde", ""])
    time.sleep(1.0)

    testresult.append(["[.] Lese Fehlerspeicher ", ""])
    testresult.append(canape_diag.checkEventMemory(passiv_dtcs, ticket_id='Fehler Id:EGA-PRM-276'))
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

