#******************************************************************************
# -*- coding: latin1 -*-
# File    : PBSM_NM_State_2.py
# Task    : A minimal "PBSM_NM_State_2!" test script
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
    time.sleep(.100)
## 4. CAN-Trace auswerten
## 4. Busruhe
    hil.cl15_on__.set(0)
#### Period Botschaft 0 set

    hil.ClampControl_01__KST_KL_15__value.set(0)
    hil.NM_Airbag__NM_Airbag_01_FCAB__value.set(0)
    hil.NM_HCP1__NM_HCP1_FCAB__value.set(0)
    hil.SiShift_01__period.set(0)
    hil.NM_Airbag__period.set(0)
   # hil.Dimmung_01__period.set(0)
    hil.NM_HCP1__period.set(0)
    hil.ClampControl_01__period.set(0)
   # hil.OTAMC_01__period.set(0)
  #  hil.VDSO_05__period.set(0)
  #  hil.NVEM_12__period.set(0)
  #  hil.OBD_03__period.set(0)
    hil.DPM_01__period.set(0)
   # hil.Diagnose_01__period.set(0)
  #  hil.OBD_04__period.set(0)
  #  hil.Systeminfo_01__period.set(0)

    hil.cl15_on__.set(1)
    time.sleep(1.50)

## 4.  NM- und Applikationsbotschaften gesendet, NM-Botschaft wird als erste Botschaft gesendet:
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1, descr="Aktiver_WakeUp"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value, 1, descr="NM_mit_Clusteranforderungen"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value, 58827857815666431, descr="nicht define"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_SNI_10__value, 83, descr="Waehlhebel_SNI"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value, 2, descr="NM_RM_aus_PBSM"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value, 0, descr="Inaktiv"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value, 1, descr="Bus_Wakeup"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value, 1, descr="KL15_EIN"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value, 0, descr="Inaktiv"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1, descr="Mindestaktivzeit"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0, descr="Inaktiv")
    ]

         #          basic_tests.checkStatus(hil.Waehlhebel_04__Waehlhebel_04_BZ__value, 0,descr="Waehlhebel_04_BZ=0 ->Busruhe")]
# a little lead-out delay
# store plot to results folder (and base name on single test results name)

## Cleanup
    hil=None
    #testenv.shutdownECU()

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

