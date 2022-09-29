#******************************************************************************
# -*- coding: latin1 -*-
# File    : WakeUp_Applikation_NM_HCP1_aus_BSM_75.py
# Task    : A minimal "WakeUp_Applikation_NM_HCP1_aus_BSM!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 19.01.2021 | Abdul Karim  | initial
# 1.1  | 13.04.2021 | Abdul Karim  | added Busruhe Signals
#******************************************************************************
import time
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
testenv = TestEnv()
## Test Case: Wake Up verursacht durch die Applikation (Empfang NM_HCP1 Botschaft) aus BSM

try:
    ## Pre-Conditions:
    testenv.setup()
    testresult = testenv.getResults()
    ## HiL Start
    hil = testenv.getHil()
    testenv.startupECU()
    time.sleep(.200)
## Aktion: 1. NM_HCP1-Botschaft 5,0x senden, CAN-Traceverlauf auswerten und 4000 ms warten
## 1. Nach erfolgter Plausibilisierung werden NM- und Applikationsbotschaften gesendet, NM-Botschaft wird als erste Botschaft gesendet

    hil.NM_Airbag__NM_Airbag_01_FCAB__value.set(0)
    hil.ClampControl_01__KST_KL_15__value.set(0)
    hil.cl15_on__.set(0)
    hil.NM_HCP1__NM_HCP1_FCAB__value.set(1)
    hil.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value.set(1)
    time.sleep(0.1)
    ## Set Testcas ID
    testresult.setTestcaseId("TestSpec_75")
    ##
    testresult.append(["1. NM_HCP1-Botschaft 5x senden, CAN-Traceverlauf auswerten", "Aktion"])
    ## 1. Nach erfolgter Plausibilisierung werden NM-Botschaft wird als erste Botschaft gesendet
    testresult.append(["Nach erfolgter Plausibilisierung NM-Botschaft wird als erste Botschaft gesendet", "Result"])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1, descr="NM_Waehlhebel_CBV_AWB:Aktiver_WakeUp"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value, 1, descr="NM_Waehlhebel_CBV_CRI:NM_mit_Clusteranforderungen"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value, 58827857815666415, descr="NM_Waehlhebel_FCAB:12_GearSelector"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_SNI_10__value, 83, descr="NM_Waehlhebel_SNI_10:Waehlhebel_SNI"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value, 1, descr="NM_Waehlhebel_NM_State:NM_RM_aus_BSM"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value, 0, descr="NM_Waehlhebel_UDS_CC:Inaktiv"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value, 1, descr="NM_Waehlhebel_Wakeup_V12:Bus_Wakeup"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value, 0, descr="NM_Waehlhebel_NM_aktiv_KL15:Inaktiv"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value, 0, descr="NM_Waehlhebel_NM_aktiv_Diag:NM_Waehlhebel_NM_aktiv_Diag:Inaktiv"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1, descr="Mindestaktivzeit"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0, descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv")
    ]
    #### 1. Nach erfolgter Plausibilisierung werden Applikationsbotschaften gesendet.
    testresult.append(["Nach erfolgter Plausibilisierung Applikationsbotschaften gesendet", "Result"])
    testresult += [
        basic_tests.checkTolerance(hil.Waehlhebel_04__Waehlhebel_04_BZ__value, 15, 1, descr="Waehlhebel_04_BZ"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Fahrstufe__value, 4, descr="WH_Fahrstufe")
    ]
    ##
    ##  4000 ms warten und
    # 2. CAN-Traceverlauf erneut auswerten
    ## NM-Botschaft wird nicht gesendet
    time.sleep(4.0)
    ##
    testresult.append(["4000 ms warten und CAN-Traceverlauf erneut auswerten", "Aktion"])
    testresult.append(["NM-Botschaft wird nicht gesendet ", "Result"])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 0, descr="NM_Waehlhebel_CBV_AWB:Passiver_WakeUp"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value, 0, descr="NM_Waehlhebel_FCAB:Init"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value, 0, descr="NM_Waehlhebel_UDS_CC:Inaktiv"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value, 0, descr="NM_Waehlhebel_NM_aktiv_KL15:Inaktiv"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value, 0, descr="NM_Waehlhebel_NM_aktiv:Inaktiv")
        ]

    ## Expect:2. Applikationsbotschaft Waehlhebel_04  wird gesendet
    testresult.append(["Applikationsbotschaften gesendet", "Result"])
    testresult += [
        basic_tests.checkTolerance(hil.Waehlhebel_04__Waehlhebel_04_BZ__value, 15, 0.1, descr="Waehlhebel_04_BZ"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Fahrstufe__value, 4, descr="WH_Fahrstufe")
    ]

    ### 100 ms warten und
    ### 3. CAN-Traceverlauf erneut auswerten
    ##3. CAN-ACK wird nur noch bedient, keine Botschaften werden gesendet
    testresult.append(["3. CAN-Traceverlauf erneut auswerten", "Aktion"])
    time.sleep(1.0)
    testresult += [
        basic_tests.checkTolerance(hil.Waehlhebel_04__Waehlhebel_04_BZ__value, 15, 0.1, descr="Waehlhebel_04_BZ")]

    time.sleep(.750)
    ##4. CAN-Traceverlauf erneut auswerten
    ## Busruhe
    ## 4. Busruhe
    ## 4. CAN-Traceverlauf erneut auswerten
    testresult.append(["4. Busruhe", "Aktion"])
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
######
    time.sleep(15.0)
    testresult += [basic_tests.checkTolerance(hil.Waehlhebel_04__Waehlhebel_04_BZ__value, 6, 1,descr="Waehlhebel_04_BZ=0 ->Busruhe")]
## Cleanup
    hil=None
finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################