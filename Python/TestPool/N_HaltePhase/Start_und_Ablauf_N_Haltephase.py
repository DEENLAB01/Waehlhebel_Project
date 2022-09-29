# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : Start_und_Ablauf_N_Haltephase.py
# Title   : Start und Ablauf der N-Haltephase
# Task    : Test Start und Ablauf der N-Haltephase
#
# Author  : Mohammed Abdul Karim
# Date    : 23.06.2021
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 23.09.2021 | Mohammed    | Initial
# 1.1  | 11.11.2021 | Mohammed    | Rework
# 1.2  | 10.12.2021 | Mohammed    | Added Fehler Id
# 1.3  | 15.12.2021 | Devangbhai  | Corrected current value and added busruhe
# 1.4  | 15.12.2021 | Mohammed    | Corrected NM_aktiv_Tmin and NM_Aktiv_N_Haltephase_abgelaufen value
# 1.5  | 07.02.2022 | Mohammed    | Added Strommonitoring
# 1.6  | 13.04.2022 | Devangbhai  | Corrected the evaluation method.Added checking of fast NM cycle method
# 1.7  | 22.04.2022 | Devangbhai  | Added Ticket ID
# 1.8  | 09.06.2022 | Devanhbhai  | Added FCAB value check method in the test step 6
# 1.9  | 09.06.2022 | Devanhbhai  | Added ticket number 232
# 1.10 | 26.07.2022 | Mohammed    | test step 5,8,9 und 10 Testschritte aktualisiert
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
from functions_nm import _checkStatus
import functions_gearselection
import functions_common
import functions_nm
import time
from time import time as t

# Instantiate test environment
testenv = TestEnv()

def check_cycletime(sec, nm_msg=True):
    NM_Waehlhebel__timestamp_list = []

    timeout = sec + t()

    while timeout > t():
        timestamp_NM_Waehlhebel = hil.NM_Waehlhebel__timestamp.get()
        if len(NM_Waehlhebel__timestamp_list) == 0 or NM_Waehlhebel__timestamp_list[-1] != timestamp_NM_Waehlhebel:
            NM_Waehlhebel__timestamp_list.append(timestamp_NM_Waehlhebel)

    new_sec = sec * 1000

    NM_Waehlhebel_timestamp = 20

    testresult.append(basic_tests.checkRange((len(NM_Waehlhebel__timestamp_list)) if nm_msg else (len(NM_Waehlhebel__timestamp_list) - 1), ((new_sec / NM_Waehlhebel_timestamp) - 2) if nm_msg else 0, ((new_sec / NM_Waehlhebel_timestamp) + 2) if nm_msg else 0, "Prüfen, ob die Applikation Botschaft NM_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (NM_Waehlhebel_timestamp, sec)))


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

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_115")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    testresult.append(["[.]Initialisierungsphase abgeschlossen und Waehlhebelposition D aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('D')
    testresult.append(["\xa0" + descr, verdict])

    # canape_diag = testenv.getCanapeDiagnostic()
    # canape_diag.disableTesterPresent()

    # testresult.append(["[.] Fehlerspeicher löschen", ""])
    # testresult.append(canape_diag.resetEventMemory())

    # TEST PROCESS ############################################################
    testresult.append([" Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    #test step 1
    testresult.append(["\x0a1. CAN-Trace auswerten", ""])
    testresult.append([" Prüfe 1. WH_Zustand_N_Haltephase_2 = 0", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=0,
            descr="Prüfe, dass Wert 0 (inaktiv) ist",
        )
    )

    # test step 2
    testresult.append(["\xa02 Setze SiShift_FlgStrtNeutHldPha = 1,VDSO_Vx3d = 32766 (0 km/h),SIShift_StLghtDrvPosn = 6 und KL15 aus, ", "INFO"])
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(1)

    descr, verdict = func_gs.setVelocity_kmph(0)
    testresult.append(["\xa0" + descr, verdict])

    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["Setze KL15 auf 0 (inactive) und 150ms warten", "INFO"])
    hil.cl15_on__.set(0)
    time.sleep(0.15)

    testresult.append(["\x0a2.1 Schalte Senden von RX Signalen (HiL --> ECU) aus", "INFO"])
    func_nm.hil_ecu_tx_off_state("aus")

    testresult.append(["\x0a2.2 Prüfe WH_Zustand_N_Haltephase_2 = 1 ", "INFO"])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 (aktiv_Timer_laeuft) ist",
        )
    )

    ### test step 3
    testresult.append(["\x0a3.1 min warten...nach 1 min CAN-Trace auswerten", ""])
    time.sleep(60)
    time_1 = time.time()
    testresult.append(["\x0a3. Prüfe, Kein Senden und Empfangen von Botschaften (WH im lokalen Nachlauf)", ""])
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    testresult.append([descr, verdict])

    time_2 = time.time()
    time_difference =time_2 - time_1
    testresult.append(["\x0aPrüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )
    nm_timestamp = hil.NM_Waehlhebel__timestamp
    start_timestamp = nm_timestamp.get()

    ### test step 4
    hil.SiShift_01__SIShift_FlgStrtNeutHldPha__value.set(0)

    testresult.append(["\x0a4. 23 min warten...nach 24 min CAN-Trace auswerten", ""])
    time.sleep(1380-time_difference)
    testresult.append(["\x0a. Prüfe, Kein Senden und Empfangen von Botschaften (WH im lokalen Nachlauf)", ""])
    time_5 = time.time()
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    time_6= time.time()
    time_difference3 = time_6 - time_5
    testresult.append([descr, verdict])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"))

    ## test step 5
    testresult.append(["\x0a5. 1 min warten...nach 25 min CAN-Trace auswerten", ""])
    wait_time = 60-time_difference3 + 2
    #
    WH_Sends_data = False
    t_out = wait_time + t()
    while t_out > t():
        curr_timestamp = nm_timestamp.get()
        if start_timestamp != curr_timestamp:
            testresult.append(["\xa0 WH starts sending the message after %s microsec" %(curr_timestamp-start_timestamp), "INFO"])
            WH_Sends_data = True
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 WH not sending the message ", "FAILED"])
            break
    if WH_Sends_data == False:
        testresult.append(
            ["\xa0 WH sendet keine Botschaften nach 25 min ", "FAILED"])

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

    testresult.append(["Prüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    ### test step 6
    testresult.append(["\x0a6. Schalte Senden von RX Signalen (HiL -->ECU) ein", ""])
    func_nm.hil_ecu_tx_off_state("an")
    check_cycletime(sec=0.100, nm_msg=True)


    ### test step 6.1
    testresult.append(["\x0a6.1 1 min warten...nach 26 min CAN-Trace auswerten und schalte das Senden von RX Signalen (HiL --> ECU) aus", ""])
    time.sleep(60)
    # checktime = 60
    # t_out = checktime + t()
    #
    # nm_timestamp = hil.NM_Waehlhebel__timestamp
    # start_timestamp_1 = nm_timestamp.get()
    #
    # result= False
    #
    # while t_out > t():
    #     curr_timestamp_1 = nm_timestamp.get()
    #     description, ticket_id, verdict= func_nm.checkFcabBitwise(fcab_value=hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), bit_exp_one=[], bit_exp_zero=[11])
    #     if verdict == "PASSED":
    #         testresult.append(["\xa0 NM_Waehlhebel_FCAB:11_Chassis bit is set to 0 in %s s" %(curr_timestamp_1 - start_timestamp_1), "PASSED"])
    #         result= True
    #         break
    #     elif verdict== "FAILED":
    #         result = False
    #
    # if result is False:
    #     curr_timestamp_1 = nm_timestamp.get()
    #     testresult.append(
    #         ["\xa0 NM_Waehlhebel_FCAB:11_Chassis bit is not set to 0 in %s sec" % (checktime), "INFO"])

    testresult.append(["\x0aPrüfe folgende Signale werden vom Wählhebel nach Ablauf Timer2 gesendet ", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="NM_Waehlhebel_CBV_AWB: Aktiver_WakeUp"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 1,
                                descr="WH_Zustand_N_Haltephase_2: aktiv_Timer_laeuft"),
        _checkStatus(current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, nominal_status=0,
                     descr="NM_aktiv_Tmin:Inaktiv ist", ticket_id='Fehler Id:EGA-PRM-214'),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv"),
        func_nm.checkFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [], [1],
                                 descr="NM_Waehlhebel_FCAB:CAR wakeup = 0", ticket_id='Fehler-Id: EGA-PRM-232')
    ]

    # testresult.append(["\x0a Lese Fehlerspeicher", ""])
    # testresult.append(canape_diag.checkEventMemoryEmpty())

    func_nm.hil_ecu_tx_off_state("aus")

    ##
    testresult.append(["Prüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    ## test step 7
    testresult.append(["\x0a7. 1 min warten...nach 27 min CAN-Trace auswerten", ""])
    time.sleep(60)
    time3 =time.time()
    testresult.append(["\x0aPrüfe, Kein Senden und Empfangen von Botschaften (WH im lokalen Nachlauf", ""])
    descr, verdict = func_gs.checkBusruhe(daq, 1)
    testresult.append([descr, verdict])
    time4 = time.time()
    time_difference2 = time4 - time3

    testresult.append(["Prüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    nm_timestamp = hil.NM_Waehlhebel__timestamp
    start_timestamp = nm_timestamp.get()

    ### test step 8
    testresult.append(["\x0a8. 2 min warten...nach 29 min CAN-Trace auswerten. Schalte Senden von RX Signalen (HiL -->ECU) ein. ", ""])
    # time.sleep(120)
    WH_Sends_data = False

    wait_time= 120-time_difference2 + 7
    t_out = wait_time + t()
    while t_out > t():
        curr_timestamp = nm_timestamp.get()
        if start_timestamp != curr_timestamp:
            testresult.append(
                ["\xa0 WH starts sending the message after %sec" % (curr_timestamp - start_timestamp), "INFO"])
            WH_Sends_data = True
            break
        elif t_out > t() == False:
            testresult.append(
                ["\xa0 WH not sending the message ", "FAILED"])
            break
    if WH_Sends_data == False:
        testresult.append(
            ["\xa0 WH sendet keine Botschaften nach 29 min ", "FAILED"])


    testresult.append(["\x0aPrüfe folgende Signale werden vom Wählhebel nach Ablauf Timer3 gesendet ", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1, descr="NM_Waehlhebel_CBV_AWB: Aktiver_WakeUp"),
        _checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 5, descr="WH_Zustand_N_Haltephase_2: aktiv_Hinweismeldung", ticket_id='Fehler-Id: EGA-PRM-232'),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 1, descr="NM_Waehlhebel_NM_aktiv_Tmin:Mindestaktivzeit"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0, descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv")
    ]
    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]
    func_nm.hil_ecu_tx_off_state("an")
    check_cycletime(sec=0.100, nm_msg=True)



    testresult.append(["Prüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    ### test step 9
    testresult.append(["\x0a9. 1 min warten...nach 30 min CAN-Trace auswerten", ""])
    time.sleep(60)


    testresult.append(["\x0aPrüfe folgende Signale werden vom Wählhebel nach Ablauf Timer4 gesendet:", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="NM_Waehlhebel_CBV_AWB: Aktiver_WakeUp"),
        _checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 2,
                                descr="WH_Zustand_N_Haltephase_2: beendet_Timer_abgelaufen",  ticket_id='Fehler Id:EGA-PRM-232'),
        _checkStatus(current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, nominal_status=0,
                     descr="NM_Waehlhebel_NM_aktiv_Tmin:inaktiv", ticket_id='Fehler Id:EGA-PRM-15'),
        _checkStatus(current_status=hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, nominal_status=1,
                     descr="NM_Aktiv_N_Haltephase_abgelaufen:Aktiv ist", ticket_id='Fehler Id:EGA-PRM-15')

    ]

    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    testresult.append(["Prüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    ### test step 10
    testresult.append(["\x0a10. 1 min warten...nach 31 min CAN-Trace auswerten", ""])
    time.sleep(60)

    testresult.append(["\x0aPrüfe Werte der Botschaft vom NM_Waehlhebel", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="NM_Waehlhebel_CBV_AWB: Aktiver_WakeUp"),
        _checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 2,
                                descr="WH_Zustand_N_Haltephase_2: beendet_Timer_abgelaufen",  ticket_id='Fehler Id:EGA-PRM-15'),
        _checkStatus(current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, nominal_status=0,
                     descr="NM_Waehlhebel_NM_aktiv_Tmin:inaktiv", ticket_id='Fehler Id:EGA-PRM-15'),
        _checkStatus(current_status=hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, nominal_status=1,
                     descr="NM_Aktiv_N_Haltephase_abgelaufen:Aktiv ist", ticket_id='Fehler Id:EGA-PRM-15')
    ]
    testresult += [
        func_nm.checkNMFcabBitwise(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), [10, 11], [],
                                   descr="Prüfe NM_Waehlhebel_FCAB:10_Powertrain, NM_Waehlhebel_FCAB:11_Chassis == 1, andere sind 0"),
    ]

    testresult.append(["Prüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    ### test step 11
    testresult.append(["\x0a11. Setze SiShift_StLghtDrvPosn = 8 senden, nach 300 ms CAN-Trace auswerte", ""])
    descr, verdict = func_gs.changeDrivePosition('P')

    time.sleep(.300)  ## Replace 50 ms to 300 ms
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Prüfe Werte der Botschaft vom NM_Waehlhebel", ""])
    testresult += [
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value, 1,
                                descr="NM_Waehlhebel_CBV_AWB: Aktiver_WakeUp"),
        basic_tests.checkStatus(hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value, 0,
                                descr="WH_Zustand_N_Haltephase_2: inaktiv"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value, 0,
                                descr="NM_Waehlhebel_FCAB: Init"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value, 0,
                                descr="NM_Waehlhebel_NM_aktiv_Tmin:inaktiv"),
        basic_tests.checkStatus(hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value, 0,
                                descr="NM_Aktiv_N_Haltephase_abgelaufen:Inaktiv")
    ]

    testresult.append(["Prüfe Strommonitoring (2 mA<I<100mA)", ""])
    testresult.append(
        basic_tests.checkRange(
            value=hil.cc_mon__A.get(),
            min_value=0.002,  # 2mA
            max_value=0.100,  # 100mA
            descr="Prüfe, dass Strom zwischen 2mA und 100mA liegt"
        )
    )

    ### test step 12.1
    testresult.append(["\x0a12.1 Schalte Senden von empfangenen Signalen aus (HiL -> ECU)", "INFO"])
    func_nm.hil_ecu_tx_off_state("aus")


    ### test step 12.2
    testresult.append(["\x0a12.2 1 min warten...nach 32 min CAN-Trace auswerten", ""])
    time.sleep(60)
    testresult.append(["Prüfe  Busruhe (0mA<I<2mA)", ""])
    temp_value = func_nm.low_current()
    testresult.append(basic_tests.checkRange(value=temp_value / 1000,
                                             min_value=0.0,  # 0mA
                                             max_value=0.002,  # 2mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt"))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    func_nm.hil_ecu_tx_off_state("an")
    time.sleep(5)
    testenv.shutdownECU()

    # cleanup #################################################################
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
