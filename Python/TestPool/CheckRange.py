# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : NM_State_RS_to_PBSM_Timeout_Airbag.py
# Task    : check that no Wakeup of Application from RS Mode if message too short
#
# Author  : An3Neumann
# Date    : 15.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 15.06.2021 | An3Neumann | initial
# ******************************************************************************
from _automation_wrapper_ import TestEnv

testenv = TestEnv()

import functions_gearselection
import functions_common
import functions_nm
from ttk_checks import basic_tests
import time
from ttk_daq import eval_signal
from result_list import ResultList  # @UnresolvedImport (in .pyz)

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    #daq = testenv.getGammaDAQ()
    #func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    #func_com = functions_common.FunctionsCommon(testenv)
    #func_nm = functions_nm.FunctionsNM(testenv, hil)

    # Initialize variables ####################################################

    # set Testcase ID #########################################################
    testresult.setTestcaseId('TestSpec_xxx')

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte KL30 an (KL15 aus), warte 150ms", ""])
    testresult.append(["Setze KL30 auf 1", "INFO"])
    hil.cl30_on__.set(1)
    testresult.append(["Warte 150ms", "INFO"])
    time.sleep(0.15)
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present und Warte 100ms", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(
        basic_tests.checkRange(
            value=hil.vbat_cl30__V.get(),  # letzer Sendetimestamp
            min_value=5.7,
            max_value=16,
            descr="Check that value is in range"
        )
    )

    testresult.append(["[.] Auslesen DID: 0xF1F2 (KL30 Signal Read)", ""])
    res, verdict = canape_diag.sendDiagRequest([0x22, 0xF1, 0xF2])
    testresult.append(["\xa0 raw output from DID F1F2 %s -" % (res), ""])
    testresult.append(["\xa0 voltage = %s mV -" % (int(hex((res[3] << 8) | res[4]), 16)), "PASSED"])

    testresult.append(["[.] Auslesen DID: 0xF1F3 (Temeprature Sensor Read) zwischen -40 to 90 Grad ", ""])
    res, verdict = canape_diag.sendDiagRequest([0x22, 0xF1, 0xF3])
    x= testresult.append(["\xa0 Prüfe Temeprature zwischen -40 to 90 Grad = %s degree" % (int(hex(res[3]), 16)), "INFO"])

    testresult.append(
        basic_tests.checkRange(
            value=canape_diag.sendDiagRequest([0x22, 0xF1, 0xF3]),  # letzer Sendetimestamp
            min_value=40,
            max_value=90,
            descr="Check that value is in range"
        )
    )

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup #################################################################
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

print "Done."
