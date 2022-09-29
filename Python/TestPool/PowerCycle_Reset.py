#******************************************************************************
# -*- coding: latin1 -*-
# File    : WakeUp_Applikation_NM_Airbag_aus_PBSM_77.py
# Title   : WakeUp Applikation NM_Airbag aus PBSM
# Task    : A minimal "WakeUp_Applikation_NM_Airbag_aus_PBSM!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 21.01.2021 | Mohammed     | initial
# 1.1  | 02.06.2021 | StengerS     | reworked
# 1.2  | 30.06.2021 | NeumannA     | evaluation of FCAB Value updated
# 1.3  | 30.07.2021 | Mohammed     | Added 2.1 and 2.2 TestSteps
# 1.4  | 09.09.2021 | Mohammed     | Added Fehler Id
#******************************************************************************

import time
from _automation_wrapper_ import TestEnv
from ttk_daq import eval_signal
from ttk_checks import basic_tests
import functions_nm
import functions_gearselection
import functions_common
import copy
from time import time as t
from functions_nm import _checkStatus

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_47")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_com = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_nm = functions_nm.FunctionsNM(testenv)


    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten und 4 Sekunden warten (T_aktiv_min)", ""])
    testenv.startupECU()

    while True:
        hil.cl15_on__.set(1)
        func_nm.hil_ecu_tx_off_state("an")
        print "...wait for init... . . . . . . . . . . . . . ...done"
        time.sleep(1)
        # testresult.append(
        #     basic_tests.checkRange(
        #         value=hil.cc_mon__A.get(),
        #         min_value=0.040,  # 2mA
        #         max_value=0.100,  # 100mA
        #         descr="Prüfe, dass Strom zwischen 40mA und 100mA liegt"
        #     )
        # )

        hil.cl15_on__.set(0)
        func_nm.hil_ecu_tx_off_state("aus")
        time.sleep(7)
        print "...wait for busruhe... . . . . . . . . . . . . . ...done"
        # testresult.append(
        #     basic_tests.checkRange(
        #         value=hil.cc_mon__A.get(),
        #         min_value=0.00,  # 0mA
        #         max_value=0.006,  # 7MA
        #         descr="Prüfe, dass Strom zwischen 0mA und 6mA liegt"
        #     )
        # )


finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################
