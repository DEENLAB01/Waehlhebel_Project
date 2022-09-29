#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Timeouterkennung_SiShift_01_nach_Ende_Timer4.py
# Title   : Timeouterkennung N-Haltephase SiShift Timer4 Ende
# Task    : Timeouterkennung der N-Haltephase SiShift Timer4 nach Ende
#
# Author  : Mohammed Abdul Karim
# Date    : 22.07.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 22.07.2021 | Mohammed    | initial
# 1.1  | 26.07.2021 | Mohammed    | Rework
# 1.2  | 16.12.2021 | Devangbhai  | Added DAQ evaluation / Rework
# 1.3  | 26.01.2022 | Mohammed    | Corrected DTC and added reset event memory
# 1.4  | 07.02.2022 | Mohammed    | Added Strommonitoring
# 1.5  | 17.02.2022 | Mohammed    | Rework
# 1.6  | 17.02.2022 | Mohammed    | Added NWDF_30 Signal
# 1.7  | 25.03.2022 | Mohammed    | Added Fehler ID
# 1.8  | 22.04.2022 | Devangbhai  | Corrected the evaluation method and added 4 sec extra in test step 14 and 15
# 1.9  | 22.04.2022 | Devangbhai  | Added 20 sec insted of 1min in test step 16
# 1.10 | 22.04.2022 | Devangbhai  | Added Ticket ID
# 1.11 | 14.06.2022 | Devanhbhai  | Added ticket number 232
# 1.12 | 26.07.2022 | Mohammed    | test step 3,7 und 10 Testschritte aktualisiert
# 1.13 | 21.08.2022 | Devangbhai  | Sending of Park Position P added in test step 13
#******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
import functions_common
import functions_nm
import time
import data_common as dc
from ttk_daq import eval_signal
from functions_nm import _checkStatus, _checkRange
from time import time as t

# Instantiate test environment
testenv = TestEnv()


def check_cycletime(sec, application_msg=True, nm_msg=True):
    Waehlhebel_04__timestamp_list = []
    DS_Waehlhebel__timestamp_list = []
    KN_Waehlhebel__timestamp_list = []
    NM_Waehlhebel__timestamp_list = []

    timeout = sec + t()

    while timeout > t():
        timestamp_Waehlhebel_04 = hil.Waehlhebel_04__timestamp.get()
        timestamp_DS_Waehlhebel = hil.DS_Waehlhebel__timestamp.get()
        timestamp_KN_Waehlhebel = hil.KN_Waehlhebel__timestamp.get()
        timestamp_NM_Waehlhebel = hil.NM_Waehlhebel__timestamp.get()

        if len(Waehlhebel_04__timestamp_list) == 0 or Waehlhebel_04__timestamp_list[-1] != timestamp_Waehlhebel_04:
            Waehlhebel_04__timestamp_list.append(timestamp_Waehlhebel_04)

        elif len(DS_Waehlhebel__timestamp_list) == 0 or DS_Waehlhebel__timestamp_list[-1] != timestamp_DS_Waehlhebel:
            DS_Waehlhebel__timestamp_list.append(timestamp_DS_Waehlhebel)

        elif len(KN_Waehlhebel__timestamp_list) == 0 or KN_Waehlhebel__timestamp_list[-1] != timestamp_KN_Waehlhebel:
            KN_Waehlhebel__timestamp_list.append(timestamp_KN_Waehlhebel)

        elif len(NM_Waehlhebel__timestamp_list) == 0 or NM_Waehlhebel__timestamp_list[-1] != timestamp_NM_Waehlhebel:
            NM_Waehlhebel__timestamp_list.append(timestamp_NM_Waehlhebel)

    new_sec = sec * 1000
    Waehlhebel_04__timestamp = 10
    DS_Waehlhebel__timestamp = 1000
    KN_Waehlhebel__timestamp = 500
    NM_Waehlhebel_timestamp = 200

    testresult.append(basic_tests.checkRange((len(Waehlhebel_04__timestamp_list)) if application_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / Waehlhebel_04__timestamp) - 5) if application_msg else 0, ((new_sec / Waehlhebel_04__timestamp) + 5) if application_msg else 0, "Prüfen, ob die Applikation Botschaft Waehlhebel_04 mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (Waehlhebel_04__timestamp, sec) if application_msg else "Prüfen, ob die Applikation Botschaft Waehlhebel_04 sendet nicht"))
    testresult.append(basic_tests.checkRange((len(DS_Waehlhebel__timestamp_list)) if application_msg else (len(DS_Waehlhebel__timestamp_list) - 1), ((new_sec / DS_Waehlhebel__timestamp) - 2) if application_msg else 0, ((new_sec / DS_Waehlhebel__timestamp) + 2) if application_msg else 0, "Prüfen, ob die Applikation Botschaft DS_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % ( DS_Waehlhebel__timestamp, sec) if application_msg else "Prüfen, ob die Botschaft DS_Waehlhebel sendet nicht"))
    testresult.append(basic_tests.checkRange((len(KN_Waehlhebel__timestamp_list)) if application_msg else (len(KN_Waehlhebel__timestamp_list) - 1), ((new_sec / KN_Waehlhebel__timestamp) - 2) if application_msg else 0,((new_sec / KN_Waehlhebel__timestamp) + 2) if application_msg else 0, "Prüfen, ob die Applikation Botschaft KN_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % ( KN_Waehlhebel__timestamp, sec) if application_msg else "Prüfen, ob die Botschaft KN_Waehlhebel sendet nicht"))
    testresult.append(basic_tests.checkRange((len(NM_Waehlhebel__timestamp_list)) if nm_msg else (len(NM_Waehlhebel__timestamp_list) - 1), ((new_sec / NM_Waehlhebel_timestamp) - 2) if nm_msg else 0, ((new_sec / NM_Waehlhebel_timestamp) + 2) if nm_msg else 0, "Prüfen, ob die  Botschaft NM_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (NM_Waehlhebel_timestamp, sec) if nm_msg else "Prüfen, ob die Applikation Botschaft NM_Waehlhebel sendet nicht"))


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

    # Initialize variables ####################################################
    test_variable = hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value
    test_variable.alias = "Waehlhebel_04:WH_Zustand_N_Haltephase_2"
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    allowed_fahrstufe = [4, 5, 6, 7, 8 ]  # nicht_betaetigt, D, N, R, P,
    wh_fahrstufe_fehlerwert = 15 # 'Fehler'
    failure_reset_time = 1.0  # Todo

    meas_vars = [hil.cl15_on__, hil.Waehlhebel_04__timestamp,
                 hil.DS_Waehlhebel__timestamp, hil.KN_Waehlhebel__timestamp,
                 hil.NM_Waehlhebel__timestamp, hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value]

    period_var = hil.SiShift_01__period  ### Added

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_182")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    testresult.append(["[.] Warte 200ms", ""])
    time.sleep(0.200)
    canape_diag = testenv.getCanapeDiagnostic()

    testresult.append(["[-] Prüfe, dass Fehler löschbar ist", ""])
    testresult.append(canape_diag.resetEventMemory(wait=True))

    testresult.append(["[-] Systeminfo_01:Systeminfo_01__SI_NWDF_30 = 1 senden ", ""])
    hil.Systeminfo_01__SI_NWDF_30__value.set(1)

    testresult.append(["[.] Prüfe Waehlhebel_04:WH_Fahrstufe != 15", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = allowed_fahrstufe,
            current_value= current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe: WH_Fahrstufe != 15 ist"
        )
    )
    testresult.append(["[.] Tester Present disabled", ""])
    canape_diag.disableTesterPresent()

    #############################################
    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["[+] Prüfe, dass %s zum Teststart wie erwartet gesetzt ist (=0)" % test_variable.alias, ""])

    # testresult.append(["Starte DAQ Messung für Applikations- und NM-Botschaften und warte 1 sekund", "INFO"])
    # testresult.append(["Folgende Signale werden mitgemessen:\n%s" % meas_vars, ""])
    # daq.startMeasurement(meas_vars)
    # time.sleep(1)

    # test step 1
    testresult.append(["\x0a 1. Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,nominal_status=0,descr="Prüfe, dass Wert 0 ist",))

    # test step 2
    testresult.append(["\x0a 2. Setze SiShift_FlgStrtNeutHldPha = 1, VDSO_Vx3d  = 32766, SIShift_StLghtDrvPosn  = 6 und KL15 aus -  Prüfe, dass %s auf 1 wechselt" % test_variable.alias, ""])
    testresult.append(["\xa0Setze SiShift FlgStrtNeutHldPha auf 1 (StartNeutralHoldPhase)", ""])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(1)

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["\xa0 Setze KL15 auf 0 (inactive)", ""])
    hil.cl15_on__.set(0)
    testresult.append(["\xa0  Warte 150ms", ""])
    time.sleep(0.15)
    time1 = time.time()

    # test step 2.1
    testresult.append(["\x0a2.1 Schalte Senden von RX Signalen (HiL --> ECU) aus", ""])
    func_nm.hil_ecu_tx_off_state("aus")

    # test step 2.2
    testresult.append(["\x0a2.2 Prüfe Waehlhebel_04:WH_Zustand_N_Haltephase_2", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",))

    # test step 3
    testresult.append(["\x0a3. 25 min warten...auf empfangene Botschaften prüfen", ""])
    wait_time = 24 * 60

    time.sleep(62)
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(0)  # making the Nhaltphase flake inactive
    nm_timestamp = hil.NM_Waehlhebel__timestamp
    start_timestamp = nm_timestamp.get()
    WH_Sends_data = False

    t_out = wait_time + t()
    while t_out > t():
        curr_timestamp = nm_timestamp.get()
        if start_timestamp != curr_timestamp:
            testresult.append(["\xa0 WH starts sending the message after %s microsec" % (curr_timestamp - start_timestamp), "INFO"])
            WH_Sends_data = True
            break
        elif t_out > t() == False:
            testresult.append(["\xa0 WH not sending the message ", "FAILED"])
            break
    if not WH_Sends_data:
        testresult.append(
            ["\xa0 WH sendet keine Botschaften nach 25 min ", "FAILED"])

    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1,
                                descr="Prüf dass NM_aktiv_Tmin = 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="Prüf dass NM_Waehlhebel_CBV_AWB= 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="Prüf dass NM_Aktiv_N_Haltephase_abgelaufen= 0"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1,
                                descr="Prüf dass WH_Zustand_N_Haltephase_2 = 1")
    ]

    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    # test step 4
    testresult.append(["\x0a4. Schalte Senden von RX Signalen (HiL --> ECU) ein", ""])
    func_nm.hil_ecu_tx_off_state("an")

    # test step 5
    testresult.append(["\x0a5.  1 min warten...nach 26 min auf empfangene Botschaften prüfen ", ""])
    time.sleep(1 * 60)
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 0,
                                descr="Prüf dass NM_aktiv_Tmin = 0"),
        func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [], [1],
                                 descr="NM_Waehlhebel_FCAB:CAR wakeup = 0", ticket_id='Fehler-Id: EGA-PRM-232'),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="Prüf dass NM_Waehlhebel_CBV_AWB= 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="Prüf dass NM_Aktiv_N_Haltephase_abgelaufen= 0"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1,
                                descr="Prüf dass WH_Zustand_N_Haltephase_2 = 1")
    ]

    # test step 6
    testresult.append(["\x0a6 Schalte Senden von RX Signalen (HiL --> ECU) aus", "INFO"])
    func_nm.hil_ecu_tx_off_state("aus")

    # test step 7
    testresult.append(["\x0a7.  3 min warten...nach 29 min auf empfangene Botschaften prüfen ", ""])
    time.sleep(61)
    nm_timestamp = hil.NM_Waehlhebel__timestamp
    start_timestamp = nm_timestamp.get()
    WH_Sends_data = False
    wait_time = 120
    t_out = wait_time + t()
    while t_out > t():
        curr_timestamp = nm_timestamp.get()
        if start_timestamp != curr_timestamp:
            testresult.append(["\xa0 WH starts sending the message after %s microsec" % (curr_timestamp - start_timestamp), "PASSED"])
            WH_Sends_data = True
            break
        elif t_out > t() == False:
            testresult.append(["\xa0 WH not sending the message ", "FAILED"])
            break
    if WH_Sends_data == False:
        testresult.append(
            ["\xa0 WH sendet keine Botschaften nach 29 min ", "FAILED"])

    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1,
                                descr="Prüf dass NM_aktiv_Tmin = 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="Prüf dass NM_Waehlhebel_CBV_AWB= 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="Prüf dass NM_Aktiv_N_Haltephase_abgelaufen= 0"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 5,
                                descr="Prüf dass WH_Zustand_N_Haltephase_2 = 5")
    ]

    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    # test step 8
    testresult.append(["\x0a8. Schalte Senden von RX Signalen (HiL --> ECU) ein", ""])
    func_nm.hil_ecu_tx_off_state("an")

    # test step 9
    testresult.append(["\x0a9.  1 min warten...nach 30 min auf empfangene Botschaften prüfen ", ""])
    time.sleep(60 + 0.200)
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 0,
                                descr="Prüf dass NM_aktiv_Tmin = 0"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="Prüf dass NM_Waehlhebel_CBV_AWB= 1"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 1,
                                descr="Prüf dass NM_Aktiv_N_Haltephase_abgelaufen= 1"),
        _checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 2,
                     descr="Prüf dass WH_Zustand_N_Haltephase_2 = 2", ticket_id='Fehler Id:EGA-PRM-232')
    ]
    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    # test step 10
    testresult.append(["\x0a10. Setze Zykluszeit der Botschaft SiShift_01 auf 0ms ", ""])
    hil.SiShift_01__period.set(0)

    # test step 11
    testresult.append(["\x0a11. 5000ms (tMSG_CYCLE)", ""])
    time.sleep(5)

    # test step 12
    testresult.append(["\x0a12. Lese Fehlerspeicher aus (0xE00101 -DTC aktiv)", ""])
    active_dtcs = [(0xE00101, 0x27)]
    testresult.append(canape_diag.checkEventMemory(active_dtcs, ticket_id='Fehler Id:EGA-PRM-184'))

    # test step 13
    testresult.append(["\x0a13. Sende mindest 8 mal SiShift_01:SIShift_StLghtDrvPosn = P. Schalte Senden von RX Signalen (HiL --> ECU) aus", "INFO"])
    hil.SiShift_01__period.set(20)
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])
    time.sleep(0.180)
    func_nm.hil_ecu_tx_off_state("aus")

    # test step 14
    testresult.append(["\x0a14. Warte TTimeout 1000 ms (RS-->PBSM)", ""])
    time.sleep(1)

    # test step 15
    testresult.append(["\x0a15. Warte TWaitBusSlep 750ms(PBSM-->BSM)",""])
    time.sleep(0.750)
    time2 = time.time()
    time3 = time2 - time1

    # test step 16
    testresult.append(["\x0a16. Warte 20 Sekund und Prüfe  Busruhe (0mA<I<2mA)", ""])
    time.sleep(20)
    testresult.append(["Prüfe, Es werden keine Botschaften versendet oder empfangen", ""])
    temp_value = func_nm.low_current()
    testresult.append(_checkRange(value=temp_value / 1000,
                                             min_value=0.0,
                                             max_value=0.002,
                                             descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt", ticket_id='Fehler Id:EGA-PRM-213'))

    # testresult.append(["\xa0 Siehe DAQ Analysis", "INFO"])
    #
    # testresult.append(["2 sekund warten und Stoppe DAQ Messung", "INFO"])
    # time.sleep(2)
    # daq_data = daq.stopMeasurement()
    # time.sleep(0.1)

    check_cycletime(sec=3, application_msg=False, nm_msg=False)

    # testresult.append(["\xa0Werte Waehlhebel_04__WH_Zustand_N_Haltephase_2 Signal aus", "INFO"])
    # descr, plot, verdict = daq.plotSingleShot(
    #     daq_data=daq_data[str(meas_vars[5])],
    #     filename="Timeouterkennung_SiShift_01_nach_Ende_Timer4",
    #     label_signal="WH_Zustand_N_Haltephase_2_Testspec_181")
    # testresult.append([descr, plot, verdict])
    # cl15_data = daq_data[str(hil.cl15_on__)]
    # analyse_cl15_data = eval_signal.EvalSignal(cl15_data)
    # analyse_cl15_data.clearAll()
    # time_zero = analyse_cl15_data.getTime()
    # cl15_off_time = analyse_cl15_data.find(operator="==", value=0)  # KL15 aus
    # cl15_off_idx = analyse_cl15_data.cur_index
    # if cl15_off_time is not None:
    #     testresult.append(["KL15 aus Zeitpunkt: %ss" % (round(cl15_off_time - time_zero, 4)), "INFO"])
    #
    #     # testresult.append( ["\x0a14 Es werden nur Applikation Botschaften versendet. NM Botschaften sendet nicht mehr.", ""])
    #     # testresult.append(["Prüf nach %s, dass kein NM Botschaften gesendet. Nur Applikation Botschaften versendet " % ( (cl15_off_time - time_zero) + time3), "INFO"])
    #     #
    #     # for var in meas_vars:
    #     #     if var == hil.NM_Waehlhebel__timestamp:
    #     #         verdict, discription = func_nm.analysisNmMessageSent(start_time=cl15_off_time + time3 + 4, name=str(var), daq_data=daq_data[str(var)], NMAreSending=False)
    #     #         testresult.append([discription, verdict])
    #     #
    #     #     elif (var != hil.cl15_on__) and (var != hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value) and ( var != hil.NM_Waehlhebel__timestamp):
    #     #         verdict, discription = func_nm.analysisApplicationMessageSent(start_time=cl15_off_time + time3 + 4, name=str(var), daq_data=daq_data[str(var)], ApplicationsAreSending=True)
    #     #         testresult.append([discription, verdict])
    #     #         print "In else opp and printing out the signals that are getting evaluated ", var
    #
    #     testresult.append(["\x0a16 Busruhe: Es werden keine Botschaften versendet oder empfangen (0mA<I<2mA)", ""])
    #     testresult.append(["Prüf nach %s, dass kein Botschaften gesendet oder empfangen" % ((cl15_off_time - time_zero) + time3 + 20 ), "INFO"])
    #
    #     for var in meas_vars:
    #         if var == hil.NM_Waehlhebel__timestamp:
    #             verdict, discription = func_nm.analysisNmMessageSent(start_time=cl15_off_time + time3 + 20, name=str(var), daq_data=daq_data[str(var)], NMAreSending=False)
    #             testresult.append([discription, verdict])
    #
    #         elif (var != hil.cl15_on__) and (var != hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value) and ( var != hil.NM_Waehlhebel__timestamp):
    #             verdict, discription = func_nm.analysisApplicationMessageSent(start_time=cl15_off_time + time3 + 20, name=str(var), daq_data=daq_data[str(var)], ApplicationsAreSending=False)
    #             testresult.append([discription, verdict])
    #
    # else:
    #     testresult.append(["KL15 aus Zeitpunkt nicht gefunden", "FAILED"])



    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
