# *****************************************************************************
# -*- coding: latin1 -*-
# File    : PFIFF_338731.py
# Title   : PFIFF_338731
# Task    : A minimal "PFIFF 338731 !" test script

# Author  : Devangbhai Patel
# Date    : 08.04.2022
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# *****************************************************************************
# ********************************* Version ***********************************
# *****************************************************************************
# Rev. | Date       | Name         | Description
# -----------------------------------------------------------------------------
# 1.0  | 08.04.2022 | Devangbhai     | initial

# *****************************************************************************

# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList
from diag_identifier import identifier_dict
import time

# #############################################################################

testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    hil = testenv.getHil()
    testresult = testenv.getResults()

    # Initialize variables ####################################################

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_338731")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()
    time.sleep(5)

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    # test step 1
    time.sleep(5)
    testresult.append(["[.] Make can High and CAN low shortcircuit. and wait 200ms", ""])
    hil.bus_physical_error.set(5)
    time.sleep(0.500)

    testresult.append(["[.]. Lese Fehlerspeicher aus (0xE00100 -DTC aktiv)", ""])
    active_dtcs = [(0xE00100, 0x27)]
    request = [0x19, 0x02, 0x2F]
    result ,verdict = canape_diag.sendDiagRequest(request)
    testresult.append(verdict)
    testresult.append(canape_diag.checkEventMemory(active_dtcs))

    testresult.append(["[.] Remove can High and CAN low shortcircuit. and wait 200ms", ""])
    hil.bus_physical_error.set(0)
    time.sleep(0.200)

    testresult.append(["[.]  ECU ausschalten", ""])
    testenv.canape_Diagnostic = None
    testenv.asap3 = None
    testenv.canape_Diagnostic = None
    del (canape_diag)
    # testenv.shutdownECU()

    testresult.append(["[.]  Warte 10sekund", ""])
    time.sleep(10)

    testresult.append(["[.] Starte ECU (KL30 an, KL15 an)", ""])
    # testenv.startupECU()

    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["Tester Present deaktivieren", ""])
    canape_diag.disableTesterPresent()
    time.sleep(5)


    testresult.append(["[.]. Lese Fehlerspeicher aus (0xE00100 -DTC Passiv)", ""])
    active_dtcs = [(0xE00100, 0x26)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs))
    time.sleep(1)
    request = [0x19, 0x02, 0x2F]
    result, verdict = canape_diag.sendDiagRequest(request)
    testresult.append(verdict)

    testresult.append(["[.]. Lösche Fehlerspeicher", ""])
    testresult.append(canape_diag.resetEventMemory())
    testresult.append(canape_diag.checkEventMemoryEmpty())

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

print "Done."
