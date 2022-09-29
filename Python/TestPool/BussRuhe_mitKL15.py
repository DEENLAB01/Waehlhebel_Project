#******************************************************************************
# -*- coding: latin1 -*-
# File    : BussRuhe_mitKL15.py
# Task    : A minimal "BussRuhe_mitKL15!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 29.03.2021 | Abdul Karim  | initial
#******************************************************************************
import time
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
from ttk_base.variables_base import Snapshot
import os
import time
import plot_utils
testenv = TestEnv()

## Buss Ruhe
try:
## Pre-condition: aktiv Prüfling elektrisch angeschlossen PowerOn nach Kl.15 ein
    testenv.setup()
    testresult = testenv.getResults()
    hil = testenv.getHil()
    testenv.startupECU()
    time.sleep(.200)
## 4. CAN-Trace auswerten
## 4. Busruhe
    hil.cl15_on__.set(0)
#### Periodic Botschaft 0 set
    hil.ClampControl_01__KST_KL_15__value.set(0)
    hil.ClampControl_01__KST_aut_Abschaltung_Zuendung__value.set(0)
    hil.NM_Airbag__NM_Airbag_01_FCAB__value.set(0)
    hil.SiShift_01__SIShift_StLghtDrvPosn__value.set(0)
    hil.SiShift_01__period.set(0)
    hil.NM_Airbag__period.set(0)
    hil.NM_HCP1__period.set(0)
    hil.ClampControl_01__period.set(0)
    hil.NM_HCP1__NM_HCP1_FCAB__value.set(0)
    hil.DPM_01__period.set(0)
    hil.Dimmung_01__period.set(0)
    hil.OTAMC_01__period.set(0)
    hil.VDSO_05__period.set(0)
    hil.NVEM_12__period.set(0)
    #hil.OBD_03__period.set(0)
   # hil.Diagnose_01__period.set(0)
    #hil.OBD_04__period.set(0)
    #hil.Systeminfo_01__period.set(0)
    #hil.cl15_on__.set(0)
    time.sleep(30.0)
    testresult += [basic_tests.checkTolerance(hil.Waehlhebel_04__Waehlhebel_04_BZ__value, 6,1, descr="Waehlhebel_04_BZ=0 ->Busruhe")]

#####
    #testresult += [basic_tests.checkTolerance(hil.Waehlhebel_04__Waehlhebel_04_BZ__value,6, 1,descr="Waehlhebel_04_BZ=0 ->Busruhe")]

## Cleanup
    hil=None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

