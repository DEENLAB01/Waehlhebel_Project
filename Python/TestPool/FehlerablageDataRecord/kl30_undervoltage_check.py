# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : KL30_undervoltage_check.py
# Title   : KL30 undervoltage check DTC after 3 ocy
# Task    : Set KL30 undervoltage error 
#           --> check DTC is active after debounce time 
#           --> set Normal voltage
#           --> verfiy if dtc is healed and confirmed after 3 OCY
#
# Author  : M.A. Mushtaq
# Date    : 23.02.2022
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 23.02.2022 | M.A. Mushtaq | initial
# 1.1  | 28.03.2022 | Mohammed     | Changed Passive DTC Status
# 1.2  | 17.08.2022 | Mohammed     | Added Fehler ID
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import functions_hil
import data_common as dc
import time

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    
    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()
    func_hil = functions_hil.FunctionsHil(testenv, hil)
    # Initialize variables ####################################################
    voltage_uv = dc.voltage_range['Undervoltage']
    set_voltage_invalid_uv = float(voltage_uv['voltage']) - float(voltage_uv['voltage']) * float(voltage_uv['tol_perc'] / 100.0) - float(voltage_uv['hil_tol_ma'])
    set_voltage_back_valid = float(dc.voltage_range['Normal']['voltage'])
    exp_dtc = [voltage_uv['DTCs']] #voltage_uv['DTCs']
    activ_dtcs = [(voltage_uv['DTCs'][0], 0x27), (0x800100, 0x27)]
    pasiv_dtcs = [(voltage_uv['DTCs'][0], 0x2E), (0x800100, 0x2E)]
    failure_set_time = 0.500
    voltage_settle_time = 0.05  # do not know the exect time
    failure_reset_time = 0.500

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_371")
    
    # TEST PRE CONDITIONS #####################################################

    testresult.append(["[-] Test Vorbedingungen", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append([" set Systeminfo_01_SI_NWDF_30 =1  ",  "INFO"])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(["[+0]", ""])
    testresult.append(canape_diag.resetEventMemory())
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["[.] Setze Spannung auf %sV (unterspannung)"%set_voltage_invalid_uv, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_invalid_uv)
    testresult.append([descr, verdict])
    #hil.vbat_cl30__V.set(8.0)

    testresult.append(["Warte %ss - Fehlererkennungszeit"%(failure_set_time+voltage_settle_time), "INFO"])
    time.sleep(failure_set_time+voltage_settle_time)
    testresult.append(["[.] Lese Fehlerspeicher (ADC-Plausibility-DTC aktiv und KL-30 unterspannung)", ""])
    testresult.append(canape_diag.checkEventMemory(activ_dtcs, ticket_id='Fehler Id:EGA-PRM-275' ))
    
    testresult.append(["[+0]", ""])
    testresult.append(["[-] perform 3 OCY", ""])
    func_hil.perform3OYC()
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Setze Spannung zurück auf %s (gültiger Bereich)" % set_voltage_back_valid, ""])
    descr, verdict = func_hil.setVoltage(set_voltage_back_valid)
    testresult.append([descr, verdict])
    
    time.sleep(voltage_settle_time)
    testresult.append(["[-] voltage check with DID F1F2 " , "INFO"])
    res, verdict = canape_diag.sendDiagRequest([0x22, 0xF1, 0xF2])
    
    testresult.append(["raw output from DID F1F2 %s -" % (res), "INFO"])
    testresult.append(["voltage = %s mV -" %(int(hex((res[3] << 8) | res[4]), 16)), "INFO"])

    testresult.append(["Warte %ss - Fehlererkennungszeit"%(failure_set_time+voltage_settle_time), "INFO"])
    time.sleep(failure_set_time+voltage_settle_time)
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Lese Fehlerspeicher (unterspannung-DTC Pasiv)", ""])

    testresult.append(canape_diag.checkEventMemory(pasiv_dtcs, mode="ONE_OR_MORE", ticket_id='Fehler Id:EGA-PRM-275'))

    testresult.append(["[+0]", ""])
    testresult.append(["[-] Lösche Fehlerspeicher", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())
    
    # TEST POST CONDITIONS ####################################################
    testresult.append(["[+0]", ""])
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
