#*******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Fehlererkennung_SafeState_02_Confirmation.py
# Title   : Fehlererkennung_SafeState_02_Confirmation
# Task    : Fehlererkennung SafeState_02 für Confirmed DTC im Fehlerspeicher

# Author  : Mohammed Abdul Karim
# Date    : 19.08.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************** Version ***********************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 19.08.2022  | Mohammed | initial
#******************************************************************************

from _automation_wrapper_ import TestEnv
testenv = TestEnv()

# Imports #####################################################################
from simplified_bus_tests import getMaxValidPeriod, setTestcaseId
from ttk_checks import basic_tests
import functions_gearselection
import time
import functions_hil

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_hil = functions_hil.FunctionsHil(testenv, hil)
    testenv.startupECU()  # startup before cal vars are called
    canape_diag = testenv.getCanapeDiagnostic()

    # Initialize variables ####################################################
    wait_time = 5000  # CAN_3244
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    wh_fahrstufe_fehlerwert = 15
    allowed_fahrstufe = [4, 5, 6, 7]  # Nicht betigt, D, N, R
    active_dtcs = [(0x800013, 0x27)]
    confirme_dtcs = [(0x800013, 0x2F)]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_420")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen: LK30 und Kl15 an", ""])
    testresult.append(["[+] Lese Fehlerspeicher (muss leer sein)", ""])

    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[.] Prüfe Waehlhebel_04:WH_Fahrstufe != 15", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = allowed_fahrstufe,
            current_value= current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe korrekt ist"
        )
    )
    testresult.append(["[.] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    # TEST PROCESS ############################################################
    testresult.append(["[#0] Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    #testresult.append(["[-0]", ""])

    # test step 1-1.2
    testresult.append(["[.] Sende SiShift_01 = 15 (Fehler)", ""])
    descr, verdict = func_gs.changeDrivePosition('Fehler')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[+] Warte 260ms ", ""])
    time.sleep(0.260)

    testresult.append(["[.] Prüfe Waehlhebel_04:WH_Fahrstufe = 15", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = wh_fahrstufe_fehlerwert,
            current_value= current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe korrekt ist"
        )
    )
    testresult.append(["[-0]", ""])

    # test step 2
    testresult.append(["[.] Lese Fehlerspeicher (0x800013 DTC aktiv)", ""])
    testresult.append(canape_diag.checkEventMemory(active_dtcs))

    # test step 3
    testresult.append(["[.] Perform 3 OCY: DEM_OPCYC_IGNITION", ""])
    func_hil.perform3OYC()

    # test step 4
    testresult.append(["[.] Lese Fehlerspeicher (Aktiv und Confirme DTC)", ""])
    testresult.append(canape_diag.checkEventMemory(confirme_dtcs))

    # test step 5-5.2
    testresult.append(["[.] Sende  SiShift_01 = P zurück", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[+] Warte 300ms ", ""])
    time.sleep(0.300)

    testresult.append(["[.] Prüfe Waehlhebel_04:WH_Fahrstufe != 15", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = allowed_fahrstufe,
            current_value= current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe korrekt ist"
        )
    )
    testresult.append(["[-0]", ""])

    # test step 6
    testresult.append(["[.] Fehlerspeicher löschen", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # test step 7
    testresult.append(["[.] Warte 1000ms", ""])
    time.sleep(1)

    # test step 8
    testresult.append(["[.] Prüfe, dass Fehler löschbar ist", ""])
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

