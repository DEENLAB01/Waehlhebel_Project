#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Timeouterkennung_SiShift_01_nach_Start_Timer2.py
# Title   : Timeouterkennung SiShift nach Start Timer2
# Task    : Timeouterkennung der SiShift Start Timer2
#
# Author  : Mohammed Abdul Karim
# Date    : 04.11.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 04.11.2021 | Mohammed    | initial
# 1.1  | 13.12.2021 | Devangbhai  | Rework
# 1.2  | 26.01.2022 | Mohammed    | Corrected DTC and added resetevent memory
# 1.3  | 07.02.2022 | Mohammed    | Added Strommonitoring
# 1.4  | 17.02.2022 | Mohammed    | Rework
# 1.5  | 17.02.2022 | Mohammed    | Added NWDF_30 Signal
# 1.6  | 25.03.2022 | Mohammed    | Added Fehler ID
# 1.7  | 14.06.2022 | Devangbhai  | changed the value of the signals according to the specification update, added tester present deactivate in precondition
# 1.8  | 25.07.2022 | Mohammed    | test step 10 und Testschritte aktualisiert
# 1.9  | 26.07.2022 | Mohammed    | test step 3 und Testschritte aktualisiert
#******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
import functions_common
import functions_nm
import time
import functions_hil
import data_common as dc
from ttk_daq import eval_signal
import copy
from functions_nm import _checkStatus, _checkRange
from time import time as t
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
    func_hil = functions_hil.FunctionsHil(testenv, hil)
    period_var = hil.SiShift_01__period ### Added

    # Initialize variables ####################################################
    test_variable = hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value
    #test_variable.alias = "Waehlhebel_04:WH_Zustand_N_Haltephase_2"
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    SiShift_period = hil.SiShift_01__period
    allowed_fahrstufe = [4, 5, 6, 7, 8]  # nicht_betaetigt, D, N, R, P,
    #exp_dtc = 0X200101

    meas_vars = [hil.cl15_on__, hil.Waehlhebel_04__timestamp,
                 hil.DS_Waehlhebel__timestamp, hil.KN_Waehlhebel__timestamp,
                 hil.NM_Waehlhebel__timestamp, hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value]

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_180")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    time.sleep(1)
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[-] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["[-] Testep Present disabled", ""])
    canape_diag.disableTesterPresent()

    testresult.append(["[.] Prüfe Waehlhebel_04:WH_Fahrstufe != 15", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = allowed_fahrstufe,
            current_value= current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe: WH_Fahrstufe != 15 ist"
        )
    )

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["Starte DAQ Messung für Applikations- und NM-Botschaften", "INFO"])
    testresult.append(["Folgende Signale werden mitgemessen:\n%s" % meas_vars, ""])
    daq.startMeasurement(meas_vars)

    # test step 1
    testresult.append(["\x0a1. Lese Signal Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 (inaktiv) ist",
        )
    )

    # test step 2
    testresult.append(["\x0a 2.Setze SIShift_FlgStrtNeutHldPha = 1,VDSO_Vx3d = 32766 (0 km/h),SIShift_StLghtDrvPosn = 6, Kl.15 = 0 , warte 150 ms", ""])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(1)

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["\xa0 Setze KL15 auf 0 (inactive) und 150ms warten", ""])
    hil.cl15_on__.set(0)
    testresult.append(["\xa0 Warte 150ms", ""])
    time1 = time.time()
    time.sleep(0.15)

    # test step 2.1
    testresult.append(["\x0a 2.1 Schalte Senden von RX Signalen (HiL --> ECU) aus", ""])
    func_nm.hil_ecu_tx_off_state("aus")

    # test step 2.2
    testresult.append(["\x0a 2.2 Prüfe WH_Zustand_N_Haltephase_2 = 1 ", "INFO"])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 (aktiv_Timer_laeuft) ist",
        )
    )

    # test step 3
    testresult.append(["\x0a3. nach 25 min CAN-Trace auswerten und auf empfangene Botschaften prüfen (Signale auswerten)", ""])
    time.sleep(61)

    # storing the last time stamp
    nm_timestamp = hil.NM_Waehlhebel__timestamp
    start_timestamp = nm_timestamp.get()

    wait_time = 24*60
    t_out = wait_time + t()
    WH_Sends_data = False
    while t_out > t():
        curr_timestamp = nm_timestamp.get()
        if start_timestamp != curr_timestamp:
            testresult.append( ["\xa0 WH starts sending the message after %sec" % (curr_timestamp - start_timestamp), "INFO"])
            WH_Sends_data = True
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 WH not sending the message ", "FAILED"])
            break

    if WH_Sends_data == False:
        testresult.append(
            ["\xa0 WH sendet keine Botschaften nach 25 min ", "FAILED"])


    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="NM_Waehlhebel_CBV_AWB = 1 "),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1,
                                descr="WH_Zustand_N_Haltephase_2= 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1,
                                descr="NM_Waehlhebel_NM_aktiv_Tmin = 1 "),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="NM_Aktiv_N_Haltephase_abgelaufen= 0")
    ]
    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    # test step 4
    testresult.append(["\x0a 4. Setze  Zykluszeit der Botschaft SiShift_01 auf 0ms und schalte Senden von RX Signalen (HiL -->ECU) ein", ""])
    testresult.append(["Schalte Senden von empfangenen Signalen ein (HiL -> ECU) ein", "INFO"])
    hil.VDSO_05__period.setState('an')
    hil.Diagnose_01__period.setState('an')
    hil.ClampControl_01__period.setState('an')
    hil.NVEM_12__period.setState('an')
    hil.Dimmung_01__period.setState('an')
    hil.NM_Airbag__period.setState('an')
    hil.OBD_03__period.setState('an')
    hil.OBD_04__period.setState('an')
    hil.ORU_Control_A_01__period.setState('an')
    hil.ORU_Control_D_01__period.setState('an')
    hil.OTAMC_D_01__period.setState('an')
    hil.Systeminfo_01__period.setState('an')
    hil.NM_HCP1__period.setState('an')

    testresult.append(["Setze  Zykluszeit der Botschaft SiShift_01 auf 0ms", "INFO"])
    hil.SiShift_01__period.set(0)

    # test step 5
    testresult.append(["\x0a 5. Warte 4950ms (tMSG_CYCLE)", ""])
    time.sleep(4.950)

    # test step 6
    testresult.append(["\x0a 6. Lese Fehlerspeicher aus", ""])
    active_dtcs = [(0xE00101, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='FehlerId:EGA-PRM-225'))

    # test step 7
    testresult.append(["\x0a7. Schalte Senden von RX Signalen (HiL --> ECU) aus", ""])
    func_nm.hil_ecu_tx_off_state("aus")


    ## test step 7.1
    time2 = time.time()
    testresult.append(["\x0a7.1 Lese Signal Waehlhebel_04:WH_Zustand_N_Haltephase_2, prüfe Timestamps", ""])
    time3= time2-time1
    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(basic_tests.checkStatus(current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,nominal_status=0,descr="Prüfe, dass Wert 0 ist",))

    testresult.append(["\xa0Siehe DAQ Messung ", ""])

    ## test step 8
    testresult.append(["\x0a8.Warte TTimeout 1000 ms (RS-->PBSM)", ""])
    time.sleep(1)

    ##
    testresult.append(["\x0a9.Warte TWaitBusSleep 750 ms (PBSM-->BSM)", ""])
    testresult.append(["Warte 60 Sekunde und Prüfe  Busruhe (0mA<I<2mA)", ""])
    time.sleep(60)
    temp_value = func_nm.low_current()
    testresult.append(basic_tests.checkRange(value=temp_value / 1000,
                                             min_value=0.0,  # 0mA
                                             max_value=0.002,  # 2mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt"))

    testresult.append(["\xa0Prüfe, Es werden keine Botschaften versendet oder empfangen", ""])
    time.sleep(0.750)
    time4 = time.time()
    time5 = time4 - time2
    testresult.append(["2 sekund warten und Stoppe DAQ Messung", "INFO"])
    time.sleep(2)
    daq_data = daq.stopMeasurement()
    time.sleep(0.1)

    testresult.append(["\xa0Werte Waehlhebel_04__WH_Zustand_N_Haltephase_2 Signal aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data[str(meas_vars[5])],
        filename="Timeouterkennung_SiShift_01_nach_Start_Timer2",
        label_signal="WH_Zustand_N_Haltephase_2_Testspec_180")
    testresult.append([descr, plot, verdict])

    cl15_data = daq_data[str(hil.cl15_on__)]
    analyse_cl15_data = eval_signal.EvalSignal(cl15_data)
    analyse_cl15_data.clearAll()
    time_zero = analyse_cl15_data.getTime()
    cl15_off_time = analyse_cl15_data.find(operator="==", value=0)  # KL15 aus
    cl15_off_idx = analyse_cl15_data.cur_index
    if cl15_off_time is not None:
        testresult.append(["KL15 aus Zeitpunkt: %ss" % (round(cl15_off_time - time_zero, 4)), "INFO"])

        testresult.append(["\x0a7.1 Es werden nur Applikation Botschaften versendet. NM Botschaften sendet nicht mehr.", ""])
        testresult.append(["Prüf nach %s, dass kein NM Botschaften gesendet. Nur Applikation Botschaften versendet "%((cl15_off_time- time_zero) + time3), "INFO"])
        for var in meas_vars:
            if var == hil.NM_Waehlhebel__timestamp:
                verdict, discription = func_nm.analysisNmMessageSent(start_time=cl15_off_time + time3, name=str(var),
                                                                     daq_data=daq_data[str(var)], NMAreSending=False)
                testresult.append([discription, verdict])

            elif (var != hil.cl15_on__) and (var != hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value) and (
                    var != hil.NM_Waehlhebel__timestamp):
                verdict, discription = func_nm.analysisApplicationMessageSent(start_time=cl15_off_time + time3, name=str(var),
                                                                              daq_data=daq_data[str(var)],
                                                                              ApplicationsAreSending=True)
                testresult.append([discription, verdict])

        testresult.append(["\x0a9. Busruhe: Es werden keine Botschaften versendet oder empfangen (0mA<I<2mA)", ""])
        testresult.append(["Prüf nach %s, dass kein Botschaften gesendet oder empfangen"
                           ". " %((cl15_off_time- time_zero) + time3+ time5), "INFO"])

        for var in meas_vars:
            if var == hil.NM_Waehlhebel__timestamp:
                verdict, discription = func_nm.analysisNmMessageSent(start_time=cl15_off_time + time3 + time5, name=str(var),
                                                                     daq_data=daq_data[str(var)], NMAreSending=False)
                testresult.append([discription, verdict])

            elif (var != hil.cl15_on__) and (var != hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value) and (
                    var != hil.NM_Waehlhebel__timestamp):
                verdict, discription = func_nm.analysisApplicationMessageSent(start_time=cl15_off_time + time3 + time5, name=str(var),
                                                                              daq_data=daq_data[str(var)],
                                                                              ApplicationsAreSending=False)
                testresult.append([discription, verdict])

    else:
        testresult.append(["KL15 aus Zeitpunkt nicht gefunden", "INFO"])


    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    func_nm.hil_ecu_tx_off_state("an")
    time.sleep(5)
    testenv.shutdownECU()

    # cleanup
    hil = None


finally:
    # #########################################################################
    testenv.breakdown()
    del(testenv)