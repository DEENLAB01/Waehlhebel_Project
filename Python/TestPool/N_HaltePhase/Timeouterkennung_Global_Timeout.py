#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Timeouterkennung_Global_Timeout.py
# Title   : Timeouterkennung Global Timeout
# Task    : Timeouterkennung der N-Haltephase durch Global-Timeout
#
# Author  : A. Abdul Karim
# Date    : 22.07.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 22.07.2021 | Mohammed Abdul Karim | initial
# 1.1  | 30.07.2021 | Mohammed Abdul Karim | Rework
# 1.2  | 16.12.2021 | Devangbhai  | Added DAQ evaluation / Rework
# 1.3  | 26.01.2022 | Mohammed    | Corrected DTC and added resetevent memory
# 1.4  | 07.02.2022 | Mohammed    | Added Strommonitoring
# 1.5  | 17.02.2022 | Mohammed    | Rework
# 1.6  | 24.02.2022 | Mohammed    | Added NWDF_30 Signal
# 1.7  | 24.03.2022 | Devangbhai  | Added teste present disable in precondition
# 1.8  | 25.03.2022 | Mohammed    | Added Fehler ID
# 1.9  | 13.04.2022 | Devangbhai  | Added method to check if the WH actively wakes up
# 1.10 | 21.04.2022 | Devangbhai  | Added 4 sec in test step 9
# 1.11 | 21.04.2022 | Devangbhai  | Added 520ms insted of 500 ms in test step 4
# 1.12  | 25.07.2022 | Mohammed   | test step 3 und Testschritte aktualisiert
# 1.13 | 21.08.2022 | Devangbhai  | Added 1150ms insted of 520ms in test step 4

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
from time import time as t

#### Using Ref TestSpec_117
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
    ###

    # Initialize variables ####################################################
    test_variable = hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value
    test_variable.alias = "Waehlhebel_04:WH_Zustand_N_Haltephase_2"
    SiShift_period = hil.SiShift_01__period
    failure_reset_time = 1.0  #

    meas_vars = [hil.cl15_on__, hil.Waehlhebel_04__timestamp,
                 hil.DS_Waehlhebel__timestamp, hil.KN_Waehlhebel__timestamp,
                 hil.NM_Waehlhebel__timestamp, hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value]


    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_183")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["[.] Waehlhebelposition D aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('D')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Tester Present disabled", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+] Prüfe, dass %s zum Teststart wie erwartet gesetzt ist (=0)" % test_variable.alias, ""])

    testresult.append(["Starte DAQ Messung für Applikations- und NM-Botschaften und warte 1 sekund", "INFO"])
    testresult.append(["Folgende Signale werden mitgemessen:\n%s" % meas_vars, ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["\x0a1. Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 ist",
        )
    )

    testresult.append(["\x0a2. Setze SiShift_FlgStrtNeutHldPha = 1, VDSO_Vx3d  = 32766, SIShift_StLghtDrvPosn  = 6 und KL15 aus -  Prüfe, dass %s auf 1 wechselt" % test_variable.alias, ""])
    testresult.append(["\xa0Setze SiShift FlgStrtNeutHldPha auf 1 (StartNeutralHoldPhase)", ""])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(1)

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["\xa0Setze KL15 auf 0 (inactive)", ""])
    hil.cl15_on__.set(0)
    time1 = time.time()
    testresult.append(["\xa0 Warte 205ms", ""])
    time.sleep(0.205)

    testresult.append(["\x0a2.1 Schalte Senden von RX Signalen (HiL --> ECU) aus", ""])
    # descr, verdict = func_gs.switchAllRXMessagesOff()
    # testresult.append([descr, verdict])
    func_nm.hil_ecu_tx_off_state("aus")
    time.sleep(0.1)

    testresult.append(["\xa0Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",))

    testresult.append(["\x0a3. 25 min warten...auf empfangene Botschaften prüfen", ""])
    time.sleep(65)
    wait_time= 24*60
    t_out = wait_time + t()
    nm_timestamp = hil.NM_Waehlhebel__timestamp
    start_timestamp = nm_timestamp.get()
    while t_out > t():
        curr_timestamp = nm_timestamp.get()
        if start_timestamp != curr_timestamp:
            testresult.append(
                ["\xa0 WH starts sending the message after %s microsec" % (curr_timestamp - start_timestamp), "PASSED"])
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 WH not sending the message ", "FAILED"])
            break

    testresult.append(["\x0a Prüfe folgende Signale werden vom Wählhebel nach Ablauf Timer1 gesendet", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="NM_Waehlhebel_CBV_AWB: Aktiver_WakeUp"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1,
                                descr="WH_Zustand_N_Haltephase_2: aktiv_Timer_laeuft"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1,
                                descr="NM_Waehlhebel_NM_aktiv_Tmin:Mindestaktivzeit"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv")
    ]

    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]


    testresult.append(["\x0a4. Warte 1150 ms (initial Timeout)", ""])
    time.sleep(1.150)

    testresult.append(["\x0a5. Lese Fehlerspeicher aus (0xE00100 -DTC aktiv)", ""])
    active_dtcs = [(0xE00100, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='Fehler Id:EGA-PRM-279'))

    testresult.append(["\x0a6. Lösche Fehlerspeicher", ""])
    testresult.append(canape_diag.resetEventMemory(ticket_id='Fehler Id:EGA-PRM-208'))
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='Fehler Id:EGA-PRM-208'))
    time2 = time.time()
    time3 = time2 - time1

    testresult.append(["\x0a7. Warte TTimeout 1000 ms (RS-->PBSM)", ""])
    time.sleep(1)

    testresult.append(["\x0a8. Warte TWaitBusSleep 750 ms (PBSM-->BSM)", ""])
    time.sleep(0.750)

    testresult.append(["\xa09 Warte 11 Sekunde und Prüfe  Busruhe (0mA<I<2mA)", ""])
    testresult.append(["Prüfe, Es werden keine Botschaften versendet oder empfangen", ""])
    time.sleep(11)
    temp_value = func_nm.low_current()
    testresult.append(basic_tests.checkRange(value=temp_value / 1000,
                                             min_value=0.0,  # 0mA
                                             max_value=0.002,  # 2mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt"))

    testresult.append(["\xa0 Siehe DAQ Analysis", "INFO"])

    testresult.append(["2 sekund warten und Stoppe DAQ Messung", "INFO"])
    time.sleep(2)
    daq_data = daq.stopMeasurement()
    time.sleep(0.1)

    cl15_data = daq_data[str(hil.cl15_on__)]
    analyse_cl15_data = eval_signal.EvalSignal(cl15_data)
    analyse_cl15_data.clearAll()
    time_zero = analyse_cl15_data.getTime()
    cl15_off_time = analyse_cl15_data.find(operator="==", value=0)  # KL15 aus
    cl15_off_idx = analyse_cl15_data.cur_index
    if cl15_off_time is not None:
        testresult.append(["KL15 aus Zeitpunkt: %ss" % (round(cl15_off_time - time_zero, 4)), "INFO"])

        # testresult.append(["\x0a7. Es werden nur Applikation Botschaften versendet. NM Botschaften sendet nicht mehr.", ""])
        # testresult.append(["Prüf nach %s, dass kein NM Botschaften gesendet. Nur Applikation Botschaften versendet " % ( (cl15_off_time - time_zero) + time3+ 4), "INFO"])
        # print "This is the time 3 %s s , cloff time %s s, timedifference beetween CL off and time zero %s s" % (time3, cl15_off_time,(cl15_off_time - time_zero) )
        #
        # for var in meas_vars:
        #     if var == hil.NM_Waehlhebel__timestamp:
        #
        #         verdict, discription = func_nm.analysisNmMessageSent(start_time=cl15_off_time + time3 + 4, name=str(var), daq_data=daq_data[str(var)], NMAreSending=False)
        #         testresult.append([discription, verdict])
        #
        #     elif (var != hil.cl15_on__) and (var != hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value) and (var != hil.NM_Waehlhebel__timestamp):
        #         verdict, discription = func_nm.analysisApplicationMessageSent(start_time= cl15_off_time + time3+ 4, name=str(var), daq_data=daq_data[str(var)], ApplicationsAreSending=True)
        #         testresult.append([discription, verdict])
        #         print "In else opp and printing out the signals that are getting evaluated ", var
        #
        # testresult.append(["\x0a9 Busruhe: Es werden keine Botschaften versendet oder empfangen (0mA<I<2mA)", ""])
        testresult.append(["Prüf nach %s, dass kein Botschaften gesendet oder empfangen" % (cl15_off_time + time3 + 1+ 0.750+ 10), "INFO"])

        for var in meas_vars:
            if var == hil.NM_Waehlhebel__timestamp:
                verdict, discription = func_nm.analysisNmMessageSent(start_time=cl15_off_time + time3 + 1 + 0.750+ 11, name=str(var), daq_data=daq_data[str(var)], NMAreSending=False)
                testresult.append([discription, verdict])

            elif (var != hil.cl15_on__) and (var != hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value) and (var != hil.NM_Waehlhebel__timestamp):
                verdict, discription = func_nm.analysisApplicationMessageSent(start_time=cl15_off_time + time3 + 1 + 0.750 + 11, name=str(var), daq_data=daq_data[str(var)], ApplicationsAreSending=False)
                testresult.append([discription, verdict])

    else:
        testresult.append(["KL15 aus Zeitpunkt nicht gefunden", "FAILED"])

    testresult.append(["\xa0Werte Waehlhebel_04__WH_Zustand_N_Haltephase_2 Signal aus", "INFO"])
    descr, plot, verdict = daq.plotSingleShot(
        daq_data=daq_data[str(meas_vars[5])],
        filename="Timeouterkennung_SiShift_01_nach_Ende_Timer4",
        label_signal="WH_Zustand_N_Haltephase_2_Testspec_181")
    testresult.append([descr, plot, verdict])


    # TEST POST CONDITIONS ####################################################
    func_nm.hil_ecu_tx_off_state("an")
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()

