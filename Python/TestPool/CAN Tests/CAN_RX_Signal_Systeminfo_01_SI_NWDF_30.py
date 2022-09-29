# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CAN_RX_Signal_Systeminfo_01_SI_NWDF_30.py
# Title   : CAN Rx Signals Systeminfo_01_NWDF_30
# Task    : Test of HIL-Tx => ECU-Rx Signals of CAN Message Systeminfo_01_SI_NWDF_30
#
# Author  : Mohammed Abdul Karim
# Date    : 14.02.2022
# Copyright 2022 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 14.02.2022 | Mohammed | initial
# ******************************************************************************
from _automation_wrapper_ import TestEnv

testenv = TestEnv()
# Imports #####################################################################
from simplified_bus_tests import testRxSigSeq, setTestcaseId

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("CAN_314")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    testenv.startupECU()  # startup before cal vars are called
    cal = testenv.getCal()
    can_bus = testenv.getCanBus()
    canape_diag = testenv.getCanapeDiagnostic()

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten: Kl15 und Kl30 an", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    # TEST PROCESS ############################################################

    # set Testcase ID #########################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # #########################################################################
    # Systeminfo_01:SI_NWDF_30
    #
    # Bit weight (resolution):   1/bit
    # Bit length:                1 bits
    # Lookup (raw):
    #   0x0: Ueberwachung_nicht_freigegeben
    #   0x1: Ueberwachung_freigegeben
    # Valid range (raw+phys):    [0x0..0x1]
    # Invalid range (raw+phys):  n/a
    # Valid states (raw+phys):   [0x0, 0x1]
    # Total range (raw+phys):    [0x0..0x1]
    testresult.append(testRxSigSeq(
        set_sig=can_bus.Systeminfo_01__SI_NWDF_30__value,
        check_var=cal.Swc_GSL_Diag_Swc_GSL_Diag_Run_SI_NWDF_30_SI_NWDF_30,
        set_values=[0x0, 0x1],
        check_values=[0x0, 0x1],
    ))
    testresult.append(["\xa0Pruefe, dass Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST POST CONDITIONS ####################################################
    testresult.append(["\nTest Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    cal = None
    hil = None
    can_bus = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
