#******************************************************************************
# -*- coding: latin1 -*-
# File    : Fehlerspeicher_Unterspannung_88.py
# Task    : A minimal "Fehlerspeicher_Unterspannung!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 14.04.2021 | Mohammed | initial
# 1.1  | 07.07.2021 | NeumannA | reworked to automate test
# 1.2  | 07.07.2021 | Mohammed | Added Pre: Prüfe, dass Fehler löschbar ist
# 1.3  | 16.11.2021 | Mohammed | Rework
# 1.4  | 24.02.2022 | Mohammed | Updated Passiv DTC
# 1.5  | 17.08.2022 | Mohammed | Added Fehler ID
#******************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
testenv = TestEnv()
import time
import functions_hil
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
    func_hil = functions_hil.FunctionsHil(testenv, hil)

    # Initialize variables ####################################################
    voltage_uv = dc.voltage_range['Undervoltage']
    set_voltage_valid_uv = float(voltage_uv['voltage']) + float(voltage_uv['voltage']) * float(voltage_uv['tol_perc'] / 100.0) + float(voltage_uv['hil_tol_ma'])
    set_voltage_invalid_uv = float(voltage_uv['voltage']) - float(voltage_uv['voltage']) * float(voltage_uv['tol_perc'] / 100.0) - float(voltage_uv['hil_tol_ma'])

    exp_dtc = voltage_uv['DTCs']
    failure_set_time = 5.0
    failure_reset_time = 0.500

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_88")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: KL30 und KL15 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[-] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["[+] Setze Spannung auf %sV (oberhalb Unterspannung)" % set_voltage_valid_uv, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_valid_uv, 0.1, 0.02)
    testresult.append([descr, verdict])

    testresult.append(["Warte %ss - Fehlererkennungszeit" % failure_set_time, "INFO"])
    time.sleep(failure_set_time)

    testresult.append(["[.] Lese Fehlerspeicher (leer)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-275'))

    testresult.append(["[.] Setze Spannung auf %sV (unterhalb Unterspannung)" % set_voltage_invalid_uv, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_invalid_uv, 0.1, 0.02)
    testresult.append([descr, verdict])

    testresult.append(["Warte %ss - Fehlererkennungszeit" % failure_set_time, "INFO"])
    time.sleep(failure_set_time)

    testresult.append(["[.] Lese Fehlerspeicher (Unterspannungs-DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory([(0x800100, 0x27), (0x800102, 0x27)], ticket_id='Fehler Id:EGA-PRM-275'))

    testresult.append(["[.] Setze Spannung zurück auf %sV (oberhalb Unterspannung)" % set_voltage_valid_uv, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_valid_uv, 0.1, 0.05)
    testresult.append([descr, verdict])

    testresult.append(["Warte %ss - Fehlerrücksetzzeit" % failure_reset_time, "INFO"])
    time.sleep(failure_reset_time)

    testresult.append(["[.] Lese Fehlerspeicher (Unterspannungs-DTC passiv)", ""])
    testresult.append(canape_diag.checkEventMemory([(0x800100, 0x26), (0x800102, 0x26)], ticket_id='Fehler Id:EGA-PRM-275'))

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-275'))

    testresult.append(["[.] Setze Spannung zurück auf 13V (Default)", ""])
    descr, verdict = func_hil.setVoltage(13, 0.1, 0.05)
    testresult.append([descr, verdict])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

## Cleanup
    hil=None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################
