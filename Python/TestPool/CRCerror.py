# ******************************************************************************
# -*- coding: latin1 -*-
# File    : CRC.py
# Title   : CRC.py
# Task    : CRC roor test
#
# Author  : Devangbhai Patel
# Date    : 29.06.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 29.06.2022 | Devangbhai   | initial
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from functions_diag import HexList
from diag_identifier import identifier_dict
import functions_common
from ttk_checks import basic_tests
from ttk_daq import eval_signal
import functions_gearselection
import time
import functions_nm
# from functions_nm import hil_ecu_tx_signal_state_for_Knockout
from time import time as t
import os
from functions_nm import _checkStatus

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_com = functions_common.FunctionsCommon(testenv)
    func_nm = functions_nm.FunctionsNM(testenv)

    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()

    testresult.append(["[+]Warte 10 sec", ""])
    time.sleep(10)



    sec = 5
    timeout = sec + t()
    testresult.append(["[+]Set the ORU control A CRC to 0 for 5sec", ""])
    while timeout > t():
        hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0)
        time.sleep(0.01)

    time.sleep(5)
    testresult.append(["[+]Set the ORU control A BZ for 5 sec", ""])
    hil.ORU_Control_A_01__ORU_Control_A_01_BZ__switch.set(1)
    time.sleep(5)
    testresult.append(["[+]Set the ORU control A BZ reset and wait 5 sec", ""])
    hil.ORU_Control_A_01__ORU_Control_A_01_BZ__switch.set(0)
    time.sleep(5)

    sec = 5
    timeout = sec + t()
    testresult.append(["[+]Set the D CRC to 0 for 5 sec", ""])
    while timeout > t():
        hil.ORU_Control_D_01__ORU_Control_D_01_CRC__value.set(0)
        time.sleep(0.01)
    time.sleep(5)

    testresult.append(["[+]Set the ORU control D BZ for 5 sec", ""])
    hil.ORU_Control_D_01__ORU_Control_D_01_BZ__switch.set(1)
    time.sleep(5)

    testresult.append(["[+]Set the ORU control D BZ reset and wait 5 sec ", ""])
    hil.ORU_Control_D_01__ORU_Control_D_01_BZ__switch.set(0)
    time.sleep(5)

    sec = 5
    timeout = sec + t()
    testresult.append(["[+]Set the OTAMC D CRC to 0 for 5 sec", ""])
    while timeout > t():
        hil.OTAMC_D_01__OTAMC_D_01_CRC__value.set(0)
        time.sleep(0.01)

    time.sleep(5)

    testresult.append(["[+]Set the  OTAMC D BZ for 5 sec", ""])
    hil.OTAMC_D_01__OTAMC_D_01_BZ__switch.set(1)
    time.sleep(5)

    testresult.append(["[+]Set the OTAMC D BZ reset and wait 5 sec ", ""])
    hil.OTAMC_D_01__OTAMC_D_01_BZ__switch.set(0)
    time.sleep(5)



    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)