#******************************************************************************
# -*- coding: latin1 -*-
# File    : Fehlerspeicher_Uberspannung_89.py
# Task    : A minimal "Fehlerspeicher_Uberspannung!" test script
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
# 1.1  | 07.07.2021 | Mohammed | Added Fehler ID
# 1.2  | 16.11.2021 | Mohammed | Rework
# 1.3  | 21.01.2022 | Mohammed | Rework after TestSpec Changed
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
    voltage_ov = dc.voltage_range['Overvoltage']
    set_voltage_valid_ov = float(voltage_ov['voltage']) - float(voltage_ov['voltage']) * float(voltage_ov['tol_perc'] / 100.0) - float(voltage_ov['hil_tol_ma'])
    set_voltage_invalid_ov = float(voltage_ov['voltage']) + float(voltage_ov['voltage']) * float(voltage_ov['tol_perc'] / 100.0) + float(voltage_ov['hil_tol_ma'])

    exp_dtc = voltage_ov['DTCs']
    failure_set_time = 5.0 #
    failure_reset_time = 0.500 #

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_89")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: KL30 und KL15 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=False))

    testresult.append(["[-] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    # hil.Systeminfo_01__SI_NWDF__value.set(1)
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["[+] Setze Spannung auf %sV (unterhalb Überspannung)" % set_voltage_valid_ov, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_valid_ov, 0.1, 0.08)
    testresult.append([descr, verdict])

    testresult.append(["Warte %ss - Fehlererkennungszeit" % failure_set_time, "INFO"])
    time.sleep(failure_set_time)

    testresult.append(["[.] Lese Fehlerspeicher (leer)", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["[.] Setze Spannung auf %sV (oberhalb Überspannung)" % set_voltage_invalid_ov, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_invalid_ov, 0.1, 0.03)
    testresult.append([descr, verdict])

    testresult.append(["Warte %ss - Fehlererkennungszeit" % failure_set_time, "INFO"])
    time.sleep(failure_set_time)

    testresult.append(["[.] Lese Fehlerspeicher (Überspannungs-DTC aktiv)", ""])
    active_dtcs= [(0x800100, 0x27), (0x800101, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='Fehler Id:EGA-PRM-276'))

    testresult.append(["[.] Setze Spannung zurück auf %sV (unterhalb Überspannung)" % set_voltage_valid_ov, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_valid_ov, 0.1, 0.03)
    testresult.append([descr, verdict])

    testresult.append(["Warte %ss - Fehlerrücksetzzeit" % failure_reset_time, "INFO"])
    time.sleep(failure_reset_time)

    testresult.append(["[.] Lese Fehlerspeicher (Überspannungs-DTC passiv)", ""])
    passive_dtcs = [(0x800100, 0x26), (0x800101, 0x26)]
    testresult.append(canape_diag.checkEventMemory(passive_dtcs, ticket_id='Fehler Id:EGA-PRM-276'))

    testresult.append(["[.] Lösche Fehlerspeicher und warte 1s", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True, ticket_id='Fehler Id:EGA-PRM-276'))
    time.sleep(1)

    testresult.append(["[.] Setze Spannung zurück auf 13V (Default)", ""])
    descr, verdict = func_hil.setVoltage(13, 0.1, 0.05)
    testresult.append([descr, verdict])

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-276'))



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
