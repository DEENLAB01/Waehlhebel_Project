#******************************************************************************
# -*- coding: latin1 -*-
# File    : SichereErkennung_Magnet_nicht_verbaut.py
# Title   : SichereErkennung Magnet_nicht_verbaut
# Task    : SichereErkennung Magnet nicht verbaut
#
# Author  : Devangbhai Patel
# Date    : 23.07.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 23.07.2021 | Devangbhai | initial
#******************************************************************************
# Imports #####################################################################
import time
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
import functions_common
from time import time as t

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_71")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_com = functions_common.FunctionsCommon(testenv)

    # Initialize variables ####################################################
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    sishift_stlfgtDrvPos = hil.SiShift_01__SIShift_StLghtDrvPosn__value

    wh_fahrstufe_fehlerwert = 15
    meas_vars = [sishift_stlfgtDrvPos, wh_fahrstufe]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    ## Cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################