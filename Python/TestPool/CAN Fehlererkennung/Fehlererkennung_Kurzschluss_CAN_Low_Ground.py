#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Fehlererkennung_Kurzschluss_CAN_Low_Ground.py
# Task    : Eindrahtfehler und Fehlererkennung am CAN Low (Kurzschluss Can Low gegen Masse)

# Author  : A.Neumann
# Date    : 01.07.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.1  | 01.07.2021  | A. Neumann | initial
# 1.2  | 01.07.2021  | Mohammed | Added TestSpec Id
# 1.3  | 19.11.2021  | Mohammed | Rework
#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()

# Imports #####################################################################
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
    daq = testenv.getGammaDAQ()
    func_hil = functions_hil.FunctionsHil(testenv, hil)

    # Initialize variables ####################################################
    exp_dtc = 1111 # Todo
    failure_set_time = 1.0 # Todo
    failure_reset_time = 1.0 # Todo
    can_location = 'LOW'
    failure_type = 'SHORT_TO_GROUND'

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_90")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["[+] Setze Fehler %s an CAN %s"%(failure_type, can_location), ""])
    descr, verdict = func_hil.setCANFiuFailureHil(can_location, failure_type)
    testresult.append([descr, verdict])

    testresult.append(["Warte Fehlererkennungszeit: %ss" % (failure_set_time), "INFO"])
    time.sleep(failure_set_time)

    testresult.append(["[.] Lese Fehlerspeicher (CAN %s %s DTC aktiv)" % (can_location, failure_type), ""])
    testresult.append(canape_diag.checkEventMemory([[exp_dtc, dc.DTCactive]]))

    testresult.append(["[.] Prüfe, dass Fehler nicht löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemory([[exp_dtc, dc.DTCactive]]))

    testresult.append(["[.] Setze Fehler %s an CAN %s zurück"%(failure_type, can_location), ""])
    descr, verdict = func_hil.resetCANFiuFailureHil()
    testresult.append([descr, verdict])

    testresult.append(["Warte Fehlerrücksetzzeit: %ss" % (failure_reset_time), "INFO"])
    time.sleep(failure_reset_time)

    testresult.append(["[.] Lese Fehlerspeicher (CAN %s %s DTC passiv)"%(can_location, failure_type), ""])
    testresult.append(canape_diag.checkEventMemory([[exp_dtc, dc.DTCpassive]]))

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
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

