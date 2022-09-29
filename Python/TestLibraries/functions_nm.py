# ******************************************************************************
# -*- coding: latin-1 -*-
# File    : functions_nm.py
# Task    : functions to work with network management
#
# Author  : An3Neumann
# Date    : 28.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 28.05.2021 | An3Neumann       | initial
# 1.1  | 21.07.2021 | Mohammed         | Rework for N-Haltphase Timer values
# 1.2  | 08.09.2021 | Devangbhai Patel | Trying to write failure ID in the verdict
# 1.3  | 24.11.2021 | Devangbhai Patel | Added evaluation method to check if the NM and Application messages are sending/stopped
# 1.4  | 07.02.2022 | Devangbhai Patel | Added low_current method
# 1.5  | 08.02.2022 | Devangbhai Patel | Added addidtional method to stop the signal for knockout
# 1.6  | 08.02.2022 | Mohammed         | Added  checkFcibBitwise method
# 1.7  | 18.07.2022 | DEvangbhai       | Added send and get methof for ISOx request
#1.7   | 18.07.2022 | Mohammed         | Added checkNMFcabBitwise for

# ******************************************************************************
from ttk_daq import eval_signal
import functions_gearselection
import functions_common
import data_common
import time
from ttk_checks.basic_tests import *
from ttk_checks import _basic_tests
from ttk_checks.basic_checks import CHECKBITMASK_DEFAULT_BIT_LENGTH
import re
from time import time as t
DTCwhitelist = []


class FunctionsNM(object):

    def __init__(self, testenv, hil=None):
        """
            TODO
        """
        self.testenv = testenv

        if hil is None:
            self.hil = self.testenv.getHil()
        else:
            self.hil = hil

        self.func_gs = functions_gearselection.FunctionsGearSelection(testenv, self.hil)
        self.func_com = functions_common.FunctionsCommon(testenv)

        self.fcab_bit_mapping = {
            56: "Charging_Status",  # 56_ChargingStatus
            55: "Dimming",  # 55_Dimming
            54: "<reserved>",  # 54_<reserved>
            53: "Lock_Unlock",  # 53_Lock_Unlock
            52: "not definded",  #
            51: "not definded",  #
            50: "not definded",  #
            49: "<reserved>",  # 49_<reserved>
            48: "Diagnosis_ClimateTmeLINs",  # 48_Diagnosis_ClimateTmeLINs
            47: "Diagnosis_ComfortLINs",  # 47_Diagnosis_ComfortLINs
            46: "Diagnosis_Light",  # 46_Diagnosis_Light
            45: "Diagnosis_Comfort",  # 45_Diagnosis_Comfort
            44: "Diagnosis_Infotainment",  # 44_Diagnosis_Infotainment
            43: "Diagnosis_DrivingAssistance",  # 43_Diagnosis_DrivingAssistance
            42: "Diagnosis_FlexRay",  # 42_Diagnosis_FlexRay
            41: "Diagnosis_Powertrain",  # 41_Diagnosis_Powertrain
            40: "Diagnosis_Energy",  # 40_Diagnosis_Energy
            39: "not definded",  #
            38: "not definded",  #
            37: "HighVoltage_WirelessChargingStation",  # 37_HighVoltage_WirelessChargingStation
            36: "PreHeater",  # 36_Preheater
            35: "ExteriorSound",  # 35_ExteriorSound
            34: "GPS_Localization",  # 34_GPS_Localization
            33: "ExternalWirelessCommunication",  # 33_ExternalWirelessCommunication
            32: "OnlineAccess",  # 32_OnlineAccess
            31: "MultifunctionalSteeringWheel",  # 31_MultifunctionalSteeringWheel
            30: "EnergyManagement",  # 30_EnergyManagement
            29: "SteeringColumnLock",  # 29_SteeringColumnLock
            28: "OnboardTester_DataCollector",  # 28_OnboardTester_DataCollector
            27: "Timemaster_Timer",  # 27_Timemaster_Timer
            26: "HighVoltage_Charging",  # 26_HighVoltage_Charging
            25: "AccessSystemSensors",  # 25_AccessSystemSensors
            24: "ThermoManagement",  # 24_ThermoManagement
            23: "Climate",  # 23_Climate
            22: "ExteriorLights",  # 22_ExteriorLights
            21: "AirSuspension",  # 21_AirSuspension
            20: "OptionalComfort",  # 20_OptionalComfort
            19: "Doors_Hatches",  # 19_Doors_Hatches
            18: "VirtualSideMirrors",  # 18_VirtualSideMirrors
            17: "Audio",  # 17_Audio
            16: "InfotainmentDisplay",  # 16_InfotainmentDisplay
            15: "InstrumentclusterDisplay",  # 15_InstrumentclusterDisplay
            14: "InfotainmentExtensions",  # 14_InfotainmentExtensions
            13: "Airbag",  # 13_Airbag
            12: "GearSelector",  # 12_GearSelector
            11: "Chassis",  # 11_Chassis
            10: "Powertrain",  # 10_Powertrain
            9: "<reserved>",  # 09_<reserved>
            8: "Basefunction_Connectivity",  # 08_Basefunction_Connectivity
            7: "Basefunction_CrossSection",  # 07_Basefunction_CrossSection
            6: "Basefunction_ComfortLight",  # 06_Basefunction_ComfortLight
            5: "Basefunction_Infotainment",  # 05_Basefunction_Infotainment
            4: "Basefunction_DrivingAssistance",  # 04_Basefunction_DrivingAssistance
            3: "Basefunction_Chassis",  # 03_Basefunction_Chassis
            2: "Basefunction_Powertrain",  # 02_Basefunction_Powertrain
            1: "CarWakeUp",  # 01_CarWakeUp
        }

    def anylysisCycletime_start_stop(self, start_time, stop_time, daq_data):
        
        signal_data = daq_data
        analyse_signal_data = eval_signal.EvalSignal(signal_data)
        analyse_signal_data.clearAll()
        analyse_signal_data.seek(start_time)

        # analyse_signal_data.markEvalRangeStart()
        analyse_signal_data.setEvalRange(start_time, stop_time)

        cycle_times = []
        sleep_start = analyse_signal_data.findChanged()
        sleep_time = None
        t_start = analyse_signal_data.getData()
        while t_start:
            analyse_signal_data.findChanged()
            t_next = analyse_signal_data.getData()
            if t_next:
                sleep_start = analyse_signal_data.getTime()
                cycle_times.append((t_next - t_start) / 1000)
            else:
                sleep_time = sleep_start - start_time
            t_start = t_next

        return cycle_times, sleep_time

    def analyseCycleSleepTimes(self, start_time, daq_data):
        """
        Parameter:
            start_time:         time where analyse start (e.g. cl 15 off)
            daq_data:           daq data of the signal
        Info:
            read all cycle times and create a list
            last measure timestamp is the sleep time
        Returns:
            cyle_times, sleep_time
        """
        signal_data = daq_data
        analyse_signal_data = eval_signal.EvalSignal(signal_data)
        analyse_signal_data.clearAll()
        analyse_signal_data.seek(start_time)

        cycle_times = []
        sleep_start = analyse_signal_data.findChanged()
        sleep_time = None
        t_start = analyse_signal_data.getData()
        while t_start:
            analyse_signal_data.findChanged()
            t_next = analyse_signal_data.getData()
            if t_next:
                sleep_start = analyse_signal_data.getTime()
                cycle_times.append((t_next - t_start) / 1000)
            else:
                sleep_time = sleep_start - start_time
            t_start = t_next

        return cycle_times, sleep_time

    def analyseCycleWakeupTimes(self, start_time, daq_data):
        """
        Parameter:
            start_time:         time where analyse start (e.g. cl 15 on)
            daq_data:           daq data of the signal
        Info:
            read all cycle times and create a list
            last measure timestamp is the wakeup time
        Returns:
            cyle_times, wakeup_time
        """
        cycle_times = []
        signal_data = daq_data
        analyse_signal_data = eval_signal.EvalSignal(signal_data)
        analyse_signal_data.clearAll()
        analyse_signal_data.seek(start_time)

        wakeup_start = analyse_signal_data.findChanged()
        wakeup_time = wakeup_start - start_time

        t_start = analyse_signal_data.getData()
        while t_start:
            analyse_signal_data.findChanged()
            t_next = analyse_signal_data.getData()
            if t_next:
                cycle_times.append((t_next - t_start) / 1000)

            t_start = t_next

        return cycle_times, wakeup_time

    def analysisCycleTime(self, start_time, daq_data):
        signal_data = daq_data
        analyse_signal_data = eval_signal.EvalSignal(signal_data)
        analyse_signal_data.clearAll()
        analyse_signal_data.seek(start_time)

        cycle_times = []
        sleep_start = analyse_signal_data.findChanged()
        t_start = analyse_signal_data.getData()
        while t_start:
            analyse_signal_data.findChanged()
            t_next = analyse_signal_data.getData()
            if t_next:
                sleep_start = analyse_signal_data.getTime()
                cycle_times.append((t_next - t_start) / 1000)
            t_start = t_next

        return cycle_times

    def analysisSigWithinTime(self, start_time, end_time, daq_data):
        signal_data = daq_data
        analyse_signal_data = eval_signal.EvalSignal(signal_data)
        analyse_signal_data.clearAll()
        analyse_signal_data.seek(start_time)
        analyse_signal_data.setEvalRange(start_time, end_time)
        # analyse_signal_data.getEvalRangeData()

        cycle_times = []
        sleep_start = analyse_signal_data.findChanged()
        sleep_time = None
        t_start = analyse_signal_data.getData()
        while t_start:
            analyse_signal_data.findChanged()
            t_next = analyse_signal_data.getData()
            if t_next:
                sleep_start = analyse_signal_data.getTime()
                cycle_times.append((t_next - t_start) / 1000)
            else:
                sleep_time = sleep_start - start_time
            t_start = t_next

        return cycle_times, sleep_time

    def analysisNmMessageSent(self, start_time, daq_data, name=None,NMAreSending=False):
        signal_data = daq_data
        analyse_signal_data = eval_signal.EvalSignal(signal_data)
        analyse_signal_data.clearAll()
        analyse_signal_data.seek(start_time)

        change = analyse_signal_data.findChanged()

        if NMAreSending:
            if change is not None:
                verdict_nm = "PASSED"
                description_nm = "\xa0 %s Botschaft sendet noch" %name
            else:
                verdict_nm = "FAILED"
                description_nm = "\xa0 %s Botschaft sendet nicht mehr " %name
        else:
            if change is not None:
                verdict_nm = "FAILED"
                description_nm = "\xa0 %s Botschaft sendet noch" %name
            else:
                verdict_nm = "PASSED"
                description_nm = "\xa0 %s Botschaft sendet nicht mehr" %name
        return verdict_nm, description_nm

    def analysisApplicationMessageSent(self, start_time, daq_data, name=None, ApplicationsAreSending=False):
        signal_data = daq_data
        analyse_signal_data = eval_signal.EvalSignal(signal_data)
        analyse_signal_data.clearAll()
        analyse_signal_data.seek(start_time)

        change = analyse_signal_data.findChanged()

        if ApplicationsAreSending:
            if change is not None:
                verdict_application_message = "PASSED"
                description_aapl = "\xa0 %s Botschaft sendet noch" %name
            else:
                verdict_application_message = "FAILED"
                description_aapl = "\xa0 %s Botschaft sendet nicht mehr" %name
        else:
            if change is not None:
                verdict_application_message = "FAILED"
                description_aapl = "\xa0 %s Botschaft sendet noch" %name
            else:
                verdict_application_message = "PASSED"
                description_aapl = "\xa0 %s Botschaft sendet nicht mehr" %name

        return verdict_application_message, description_aapl

    def checkFcabBitwise(self, fcab_value, bit_exp_one, bit_exp_zero, descr="", dont_care_info=False, ticket_id=''):
        """
        Args:
            fcab_value: read out value of fcab variable
            bit_exp_one: list with all bit, which shall be 1
            bit_exp_zero:  list with all bit, which shall be 0
            descr: (optional)
            dont_care_info: if True also "don't care bits are in result"

        Info:
            check that all exp one are one, all zero are zero... all other don't care

        Returns:
            description, verdict
        """
        exp_value = ""
        for bit in range(1, len(self.fcab_bit_mapping) + 1):

            if bit in bit_exp_one:
                exp_value = "1" + exp_value
            elif bit in bit_exp_zero:
                exp_value = "0" + exp_value
            else:
                exp_value = "X" + exp_value

        return self.checkFCABValue(fcab_value=fcab_value, exp_value=exp_value, descr=descr, dont_care_info=dont_care_info,ticket_id=ticket_id)

    def checkNMFcabBitwise(self, fcab_value, bit_exp_one, bit_exp_zero, descr="", dont_care_info=False, ticket_id= False):
        """
        Args:
            fcab_value: read out value of fcab variable
            bit_exp_one: list with all bit, which shall be 1
            bit_exp_zero:  list with all bit, which shall be 0
            descr: (optional)
            dont_care_info: if True also "don't care bits are in result"

        Info:
            check that all exp one are one, all zero are zero... all other don't care

        Returns:
            description, verdict
        """
        #verdict = "PASSED"
        exp_value = ""
        for bit in range(1, len(self.fcab_bit_mapping) + 1):

            if bit in bit_exp_one:
                exp_value = "1" + exp_value
            else:
                exp_value = "0" + exp_value

            # if bit in bit_exp_one:
            #     exp_value = "1" + exp_value
            # elif bit in bit_exp_zero:
            #     exp_value = "0" + exp_value
            # else:
            #     exp_value = "X" + exp_value

        return self.checkFCABValue(fcab_value=fcab_value, exp_value=exp_value, descr=descr, dont_care_info=dont_care_info,ticket_id=ticket_id)

#################################################################################################
    def checkFcibBitwise(self, fcab_value, bit_exp_one, bit_exp_zero, descr="", dont_care_info=False):
        """
        Args:
            fcab_value: read out value of fcab variable
            bit_exp_one: list with all bit, which shall be 1
            bit_exp_zero:  list with all bit, which shall be 0
            descr: (optional)
            dont_care_info: if True also "don't care bits are in result"

        Info:
            check that all exp one are one, all zero are zero... all other don't care

        Returns:
            description, verdict
        """
        exp_value = ""
        for bit in range(1, len(self.fcab_bit_mapping) + 1):

            if bit in bit_exp_one:
                exp_value = "1" + exp_value
            elif bit in bit_exp_zero:
                exp_value = "0" + exp_value
            else:
                exp_value = "X" + exp_value

        return self.checkFCABValue(fcab_value=fcab_value, exp_value=exp_value, descr=descr, dont_care_info=dont_care_info)

#########################################################################

    def checkFCABValue(self, fcab_value, exp_value, descr="", dont_care_info=False,ticket_id=''):
        """
        Args:
            fcab_value: read out value of fcab variable
            exp_value: expected value of fcab
            descr: (optional)
            dont_care_info: if True also "don't care bits are in result"

        Returns:
            description, verdict
        """

        temp_str = ''
        if ticket_id:
            temp_str = '[[COMMENT]]'

        bit_value = bin(int(fcab_value))[2:] if isinstance(fcab_value, (int, float, long)) else fcab_value
        exp_bit_value = bin(int(exp_value))[2:] if isinstance(exp_value, int) else exp_value

        i = len(self.fcab_bit_mapping)
        while len(bit_value) < i:
            bit_value = "0" + bit_value
        while len(exp_bit_value) < i:
            exp_bit_value = "0" + exp_bit_value

        verdict = "PASSED"
        info = "%s\nAusgelesen: %s (%s), \nErwartet: %s\n" % (descr, bit_value, int(bit_value, 2), exp_bit_value)

        for bit, e_bit in zip(bit_value, exp_bit_value):
            if e_bit != "X":
                if self.fcab_bit_mapping[i] != "not definded":
                    if bit == e_bit:
                        if bit == "1":
                            info += "Bit %s ist wie erwartet aktiviert = 1 (%s)\n" % (i, self.fcab_bit_mapping[i])
                        else:
                            info += "Bit %s ist wie erwartet deaktiviert = 0 (%s)\n" % (i, self.fcab_bit_mapping[i])
                    else:
                        verdict = "FAILED"
                        if e_bit == "0":
                            info += ">> Bit %s sollte deaktiviert = 0 sein (%s)\n" % (i, self.fcab_bit_mapping[i])
                        else:
                            info += ">> Bit %s sollte aktiviert = 1  sein (%s)\n" % (i, self.fcab_bit_mapping[i])
                        temp_str += '%s' % (ticket_id)
            else:
                if dont_care_info:
                    info += "Bit %s wird nicht ausgewertet - don't care (%s)\n" % (i, self.fcab_bit_mapping[i])
                    temp_str += '%s' % (ticket_id)
            i -= 1

        return [info,temp_str, verdict]

    def waitTillChangeIntoRS(self, timeout_s=3, nm_cycletime_s=0.200):
        '''
        Parameter:
            timeout        - timeout in seconds if no change will done
            nm_cycletime_s - cycletime of NM Message in seconds

        Info:
            read out timestamp of NM message. if timestamp didn't change for
            time = 1.5*cycletime sending stopped and NM State should change
            to Ready Sleep. Return PASSED if this happend before timeout come

        Return:
            verdict
        '''
        nm_sending_message = self.hil.NM_Waehlhebel__timestamp
        start_time = time.time()
        time_old = time.time()
        timestamp_old = 0
        verdict = 'FAILED'
        while timeout_s > (time.time() - start_time):
            time.sleep(0.01)
            timestamp_new = nm_sending_message.get()
            time_new = time.time()
            if timestamp_new == timestamp_old:
                if (time_new - time_old) > nm_cycletime_s * 1.5:
                    verdict = 'PASSED'
                    break
            else:
                time_old = time_new
                timestamp_old = timestamp_new

        return verdict

    def waitTillTimerEnds(self, timer, wait_time=None, switch_rx_signals=True):
        """

        Args:
            timer:          - 1, 2, 3, 4, "ende"
            wait_time:      - max. wait time in seconds
                                if None, max times are:
                                timer 1 = 25min = 1500s
                                timer 2 = 1min = 60s
                                timer 3 = 3min = 180s
                                timer 4 = 1min = 60s
            switch_rx_signals: if True RX signals from HiL to ECU will switched off/on
                                Timer 1 Passed - switch on
                                After Timer 2 - switch off
                                Timer 4 Passed - switch on

        Info:
            Diese Abläufe und Analyse erfolgt nach dem Dokument LAH_WH_N-Haltephase, Version 0.0, vom 22.02.2021
            Siehe Ablauf Seite 10 von 10
        Returns:
                description, verdict
        """

        waiting_times_timer = {1: 1500, 2: 60, 3: 180, 4: 60, "ende": 0}
        wait_time = wait_time if wait_time else waiting_times_timer[timer]
        # timer parameter
        wait_intervall = 0.1 # 1/2 Cycletime to check changes
        number_loops = int(float(wait_time) / wait_intervall)
        nm_timestamp = self.hil.NM_Waehlhebel__timestamp
        fcab_signal = self.hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value
        zustand_signal = self.hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value
        tmin_signal = self.hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value
        cbv_awb_signal = self.hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value
        nm_aktiv_signal = self.hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value

        change_time = None
        verdict = None

        def checkSignalValues(carwakeup, t_min, cbv_awb, zustand, n_haltephase_abgelaufen):
            info = ''
            verdict = 'PASSED'
            if carwakeup is not None:
                read_value = fcab_signal.get()
                if carwakeup == 1:
                    _, _, verdict = self.checkFcabBitwise(fcab_value=read_value, bit_exp_one=[1], bit_exp_zero=[])
                else:
                    _, _, verdict = self.checkFcabBitwise(fcab_value=read_value, bit_exp_one=[], bit_exp_zero=[1])
                info += "CarWakeUp ist korrekt (erw/akt: %s)"%read_value if verdict == "PASSED" else "> CarWakeUp ist falsch (erw: %s / akt: %s)"%(carwakeup, read_value)
            if t_min is not None:
                read_value = tmin_signal.get()
                if read_value != t_min:
                    verdict = "FAILED"
                    info += "\n> NM_aktiv_Tmin ist falsch (erw: %s / akt: %s)"%(t_min, read_value)
                else:
                    info += "\nNM_aktiv_Tmin ist korrekt (erw/akt: %s)"%read_value
            if cbv_awb is not None:
                read_value = cbv_awb_signal.get()
                if read_value != cbv_awb:
                    verdict = "FAILED"
                    info += "\n> CBV_AWB ist falsch (erw: %s / akt: %s)"%(cbv_awb, read_value)
                else:
                    info += "\nCBV_AWB ist korrekt (erw/akt: %s)"%read_value
            if zustand is not None:
                read_value = zustand_signal.get()
                if read_value != zustand:
                    verdict = "FAILED"
                    info += "\n> WH_Zustand_N_Haltephase_2 ist falsch (erw: %s / akt: %s)"%(zustand, read_value)
                else:
                    info += "\nWH_Zustand_N_Haltephase_2 ist korrekt (erw/akt: %s)"%read_value
            if n_haltephase_abgelaufen is not None:
                read_value = nm_aktiv_signal.get()
                if read_value != n_haltephase_abgelaufen:
                    verdict = "FAILED"
                    info += "\n> NM_Aktiv_N_Haltephase_abgelaufen ist falsch (erw: %s / akt: %s)"%(n_haltephase_abgelaufen, read_value)
                else:
                    info += "\nNM_Aktiv_N_Haltephase_abgelaufen ist korrekt (erw/akt: %s)"%read_value

            return verdict, info

        # timer 1
        car_wakeup_t1 = 1
        t_min_t1 = cbv_awb_t1 = 1
        zustand_t1 = 1 ## Added zustand_t1
        n_haltephase_abgelaufen_1 = 0 ## Added n_haltephase_abgelaufen_1

        # timer 2
        cbv_awb_t2 = 1
        zustand_t2 = 1  ## Added zustand_t2
        t_min_t2 = 0  ## Added  t_min_t2
        n_haltephase_abgelaufen_2 = 0 ##  Added n_haltephase_abgelaufen_2

        # timer 3
        car_wakeup_t3 = 1   ## replace 0 to 1
        zustand_t3 = 5      ##  replace 1 to 5
        t_min_t3 = cbv_awb_t3 = 1
        n_haltephase_abgelaufen_3 = 0  ##  Added n_haltephase_abgelaufen_2

        # timer 4
        car_wakeup_t4 = 1
        zustand_t4 = 2     ##  replace 5 to 2
        cbv_awb_t4 = 1     ##  Added cbv_awb_t4
        n_haltephase_abgelaufen_4 = 0  ##  Added n_haltephase_abgelaufen_4

        # timer ende
        zustand_tende = 2
        sishift_tende = 'P' # 8
        car_wakeup_tende = 0
        t_min_tende = cbv_awb_tende = 1
        n_haltephase_abgelaufen_tende = 1

        if timer == 1:
            # Prüfe, dass in der vorgegebenen wait time eine Botschaft gesendet wird:
            # - timestamp muss ich ändern --> timestamp_change wird auf True geändert
            # wenn timestamp sich ändert, wird CarWakeUp geprüft_
            # - CarWakeUp == 1, CBV_AWB = 1, NM_aktiv_Tmin = 1 --> verdict wird auf 'PASSED' geändert und change_time wird eingetragen
            # wenn timestamp_change == True, verdict == 'PASSED' und switch_rx_signals == True:
            # - Senden von RX Signalen (Botschaften von HiL -> ECU) wird angeschaltet
            # Wenn verdict == 'PASSED':
            # - wird timestamp und CarWakeUp nicht mehr geprüft, Wartezeit läuft noch zuende ab
            # Wenn nach Ablauf des Timers change_time == None, wird verdict auf 'FAILED' geändert
            # In der description wird unterschieden zwischen:
            # - Es wurde keine Botschaft gesendet (timestamp_change == False)
            # - Es wurde eine Botschaft gesendet (timestamp_change == True), aber CarWakeUp Bit ist nicht 1
            timestamp_change = False
            start_timestamp = nm_timestamp.get()
            for i in range(1,number_loops+1):
                time.sleep(wait_intervall)
                if verdict != "PASSED":
                    curr_timestamp = nm_timestamp.get()
                    if start_timestamp != curr_timestamp:
                        timestamp_change = True
                        verdict, info = checkSignalValues(car_wakeup_t1, t_min_t1, cbv_awb_t1, zustand_t1, n_haltephase_abgelaufen_1) ## Added zustand_t1 and n_haltephase_abgelaufen_1
                        if verdict == "PASSED":
                            change_time = i*wait_time
                            descr = "NM_Waehlhaebel Botschaft wurde nach %ss empfangen und Werte sind korrekt %s"%(change_time/1000.0, info)
                            if switch_rx_signals:
                                # start sending of hil signals
                                self.func_gs.switchAllRXMessagesOn()
                                descr += "\nSenden von RX Signalen (HiL --> ECU) wurde gestartet"
                            else:
                                descr += "\nSenden von RX Signalen (HiL --> ECU) wurde nicht gestartet"
            if change_time is None:
                verdict = "FAILED"
                if timestamp_change:
                    _, info = checkSignalValues(car_wakeup_t1, t_min_t1, cbv_awb_t1, zustand_t1, n_haltephase_abgelaufen_1)  ## Added zustand_t1 and n_haltephase_abgelaufen_1
                    descr = "Signale wurden während Timer 1 Zeit nicht korrekt gesetzt %s"%(info)
                else:
                    descr = "NM_Waehlhaebel Botschaft hat nichts gesendet (Keine Änderung des Timestamps)"
                descr += "\nSenden von RX Signalen (HiL --> ECU) wurde NICHT gestartet"

        elif timer == 2:
            # Es wird geprüft, dass nach Ablauf der wait_time das Signal WH_Zustand_N_Haltephase_2 == 1 ist
            # Ist WH_Zustand_N_Haltephase_2 == 1 wird verdict auf "PASSED" gesetzt (sonst "FAILED")
            # Wenn switch_rx_signals == True:
            # - Senden von RX Signalen (Botschaften von HiL -> ECU) wird ausgeschaltet
            self.func_com.waitSecondsWithResponse(wait_time)
            _, info = checkSignalValues(cbv_awb_t2, zustand_t2, None, t_min_t2, n_haltephase_abgelaufen_2) ### ## Added zustand_t2, n_haltephase_abgelaufen_2
            descr = "Warte bis Timer %s abgelaufen ist - %ss"%(timer, wait_time)
            descr += "\n" + info
            if switch_rx_signals:
                self.func_gs.switchAllRXMessagesOff()
                descr += "\nSenden von RX Signalen (HiL --> ECU) wurde gestoppt"
            else:
                descr += "\nSenden von RX Signalen (HiL --> ECU) wurde nicht gestoppt"

        elif timer == 3:
            # Es wird geprüft, dass in der vorgegebenen wait_time eine Botschaft empfangen wird
            # - timestamp muss ich ändern --> timestamp_change wird auf True geändert
            # wenn timestamp sich ändert, wird CarWakeUp geprüft_
            # - CarWakeUp == 1, CBV_AWB = 1, NM_aktiv_Tmin = 1 WH_Zustand_N_Haltephase_2 muss 1 sein
            #  --> verdict wird auf 'PASSED' geändert und change_time wird eingetragen
            # Wenn verdict == 'PASSED':
            # - wird timestamp und CarWakeUp nicht mehr geprüft, Wartezeit läuft noch zuende ab
            # Wenn nach Ablauf des Timers change_time == None, wird verdict auf 'FAILED' geändert
            # In der description wird unterschieden zwischen:
            # - Es wurde keine Botschaft gesendet (timestamp_change == False)
            # - Es wurde eine Botschaft gesendet (timestamp_change == True), aber einer oder beide geprüften Werte falsch
            timestamp_change = False
            start_timestamp = nm_timestamp.get()
            for i in range(1, number_loops + 1):
                time.sleep(wait_intervall)
                if verdict != "PASSED":
                    curr_timestamp = nm_timestamp.get()
                    if start_timestamp != curr_timestamp:
                        timestamp_change = True
                        verdict, info = checkSignalValues(car_wakeup_t3, t_min_t3, cbv_awb_t3, zustand_t3, n_haltephase_abgelaufen_3) ### Added n_haltephase_abgelaufen_3
                        if verdict == 'PASSED':
                            # start sending of hil signals
                            change_time = i * wait_time
                            descr = "NM_Waehlhaebel Botschaft wurde nach %ss empfangen und Werte sind korrekt %s"%(change_time/1000.0, info)

            if change_time is None:
                verdict = "FAILED"
                if timestamp_change:
                    _, info = checkSignalValues(car_wakeup_t3, t_min_t3, cbv_awb_t3, zustand_t3, None)
                    descr = "Werte wurden nicht wie erwartet gesetzt. \n%s"%(info)
                else:
                    descr = "NM_Waehlhaebel Botschaft hat nichts gesendet (Keine Änderung des Timestamps)"

        elif timer == 4:
            # Es wird geprüft, dass in der vorgegebenen wait_time eine Botschaft empfangen wird
            # - timestamp muss ich ändern --> timestamp_change wird auf True geändert
            # wenn timestamp sich ändert, wird CarWakeUp geprüft_
            # - CarWakeUp muss auf 1 sein und WH_Zustand_N_Haltephase_2 muss 5 sein
            #  --> verdict wird auf 'PASSED' geändert und change_time wird eingetragen
            # sobald verdict == 'PASSED' ist und change_time existiert, werden Werte nicht mehr geprüft
            # und der timer 4 wird gestartet:
            # - wenn switch_rx_signals == True wird Senden von RX Signalen (Botschaften von HiL -> ECU) gestartet
            # Wenn nach Ablauf der wait_time die change_time == None, wird verdict auf 'FAILED' geändert
            # In der description wird unterschieden zwischen:
            # - Es wurde keine Botschaft gesendet (timestamp_change == False)
            # - Es wurde eine Botschaft gesendet (timestamp_change == True), aber einer oder beide geprüften Werte falsch
            timestamp_change = False
            # first loop to check that values are changing
            start_timestamp = nm_timestamp.get()
            for i in range(1, number_loops + 1):
                time.sleep(wait_intervall)
                if verdict != "PASSED":
                    curr_timestamp = nm_timestamp.get()
                    if start_timestamp != curr_timestamp:
                        timestamp_change = True
                        verdict, info = checkSignalValues(car_wakeup_t4, cbv_awb_t4, None, zustand_t4, n_haltephase_abgelaufen_4) ## Added cbv_awb_t4 and n_haltephase_abgelaufen_4
                        if verdict == 'PASSED':
                            # start sending of hil signals
                            change_time = i * wait_time
                            descr = "NM_Waehlhaebel Botschaft wurde nach %ss empfangen und Werte sind korrekt %s"%(change_time/1000.0, info)
                            if switch_rx_signals:
                                self.func_gs.switchAllRXMessagesOn()
                                descr += "\nSenden von RX Signalen (HiL --> ECU) wurde gestartet"
                            else:
                                descr += "\nSenden von RX Signalen (HiL --> ECU) wurde nicht gestartet"
                            break
                        else:
                            verdict = "FAILED"

            if change_time is None:
                verdict = "FAILED"
                if timestamp_change:
                    _, info = checkSignalValues(car_wakeup_t4, None, cbv_awb_t4, zustand_t4, n_haltephase_abgelaufen_4) ## Todo: Added cbv_awb_t4 and n_haltephase_abgelaufen_4
                    descr = "Werte wurden nicht wie erwartet gesetzt. \n%s \nTimer 4 nicht gestartet" % (info)
                else:
                    descr = "NM_Waehlhaebel Botschaft hat nichts gesendet (Keine Änderung des Timestamps)"
                descr += "\nSenden von RX Signalen (HiL --> ECU) wurde NICHT gestartet"
            else:
                descr += "\nStarte Timer 4 - warte %ss"%wait_time
                self.func_com.waitSecondsWithResponse(wait_time)

        elif timer == "ende":
            # Es wird geprüft, das nach Ende der Timer (nach Timer 4) folgende Werte gesetzt sind:
            # - CarWakeUp muss auf 0 sein und WH_Zustand_N_Haltephase_2 muss 2 sein
            # - SiShift_StLghtDrvPosn muss auf P gesetzt werden
            # --> verdict wird auf 'PASSED' geändert (sonst 'FAILED') und change_time wird eingetragen
            verdict, descr = checkSignalValues(car_wakeup_tende, t_min_tende, cbv_awb_tende, zustand_tende, n_haltephase_abgelaufen_tende)
            descr += "\nSIShift_StLghtDrvPosn auf %s gesetzt"%sishift_tende
            self.func_gs.changeDrivePosition(sishift_tende)

        return descr, verdict

    def hil_ecu_tx_off(self, period_sec):
        period_sec = period_sec * 1000

        self.hil.SiShift_01__period.set(period_sec)
        self.hil.VDSO_05__period.set(period_sec)
        self.hil.Diagnose_01__period.set(period_sec)
        self.hil.ClampControl_01__period.set(period_sec)
        self.hil.NVEM_12__period.set(period_sec)
        self.hil.Dimmung_01__period.set(period_sec)
        self.hil.NM_Airbag__period.set(period_sec)
        self.hil.OBD_03__period.set(period_sec)
        self.hil.OBD_04__period.set(period_sec)
        self.hil.ORU_Control_A_01__period.set(period_sec)
        self.hil.ORU_Control_D_01__period.set(period_sec)
        self.hil.OTAMC_D_01__period.set(period_sec)
        self.hil.Systeminfo_01__period.set(period_sec)
        self.hil.NM_HCP1__period.set(period_sec)

    def hil_ecu_tx_off_state(self, state):
        self.hil.SiShift_01__period.setState(state)
        self.hil.ClampControl_01__period.setState(state)
        self.hil.VDSO_05__period.setState(state)
        self.hil.Diagnose_01__period.setState(state)
        self.hil.NVEM_12__period.setState(state)
        self.hil.Dimmung_01__period.setState(state)
        self.hil.NM_Airbag__period.setState(state)
        self.hil.OBD_03__period.setState(state)
        self.hil.OBD_04__period.setState(state)
        self.hil.ORU_Control_A_01__period.setState(state)
        self.hil.ORU_Control_D_01__period.setState(state)
        self.hil.OTAMC_D_01__period.setState(state)
        self.hil.Systeminfo_01__period.setState(state)
        self.hil.NM_HCP1__period.setState(state)

    def hil_ecu_e2e(self, allstate=0, sisft=0, otamc=0, oruA=0, ourD= 0):
        state= None
        if allstate == 0:
            state= "aus"
        else:
            state= "an"
        self.hil.ClampControl_01__period.setState(state)
        self.hil.VDSO_05__period.setState(state)
        self.hil.Diagnose_01__period.setState(state)
        self.hil.NVEM_12__period.setState(state)
        self.hil.Dimmung_01__period.setState(state)
        self.hil.NM_Airbag__period.setState(state)
        self.hil.OBD_03__period.setState(state)
        self.hil.OBD_04__period.setState(state)
        self.hil.Systeminfo_01__period.setState(state)
        self.hil.NM_HCP1__period.setState(state)
        self.hil.SiShift_01__period.setState("aus") if sisft == 0 else self.hil.SiShift_01__period.setState("an")
        self.hil.ORU_Control_A_01__period.setState("aus") if oruA == 0 else self.hil.ORU_Control_A_01__period.setState("an")
        self.hil.ORU_Control_D_01__period.setState("aus") if ourD == 0 else self.hil.ORU_Control_D_01__period.setState("an")
        self.hil.OTAMC_D_01__period.setState("aus") if otamc == 0 else self.hil.OTAMC_D_01__period.setState("an")

    def hil_ecu_tx_signal_state_for_Knockout(self, NM_Clampcontrol_send= True,all_other_send= False):
        """

        Args:
            NM_Clampcontrol_send: Sets the state of the NM_Airbag, NM_HCP1 and Clampcontrol messages to "an" ff set to true else "aus"
            all_other_send: State of the remaining messages to "an" If set to true else "aus"

        Returns: sets the state of the messages

        """
        if NM_Clampcontrol_send == False:
            self.hil.ClampControl_01__period.setState("aus")
            self.hil.NM_HCP1__period.setState("aus")
            self.hil.NM_Airbag__period.setState("aus")
        else:
            self.hil.ClampControl_01__period.setState("an")
            self.hil.NM_HCP1__period.setState("an")
            self.hil.NM_Airbag__period.setState("an")
        if all_other_send == False:
            self.hil.SiShift_01__period.setState("aus")
            self.hil.VDSO_05__period.setState("aus")
            self.hil.Diagnose_01__period.setState("aus")
            self.hil.NVEM_12__period.setState("aus")
            self.hil.Dimmung_01__period.setState("aus")
            # self.hil.OBDC_Funktionaler_Req_All_FD__period.setState("aus")
            self.hil.OBD_03__period.setState("aus")
            self.hil.OBD_04__period.setState("aus")
            self.hil.ORU_Control_A_01__period.setState("aus")
            self.hil.ORU_Control_D_01__period.setState("aus")
            self.hil.OTAMC_D_01__period.setState("aus")
            self.hil.Systeminfo_01__period.setState("aus")
            self.hil.ORU_01__period.setState("aus")
        else:
            self.hil.SiShift_01__period.setState("an")
            self.hil.VDSO_05__period.setState("an")
            self.hil.Diagnose_01__period.setState("an")
            self.hil.NVEM_12__period.setState("an")
            self.hil.Dimmung_01__period.setState("an")
            # self.hil.OBDC_Funktionaler_Req_All_FD__period.setState("an")
            self.hil.OBD_03__period.setState("an")
            self.hil.OBD_04__period.setState("an")
            self.hil.ORU_Control_A_01__period.setState("an")
            self.hil.ORU_Control_D_01__period.setState("an")
            self.hil.OTAMC_D_01__period.setState("an")
            self.hil.Systeminfo_01__period.setState("an")
            self.hil.ORU_01__period.setState("an")

    def low_current(self):
        self.hil.error_type.set(5)
        time.sleep(2)
        self.hil.N1SRC_ReqData__trigger.set(0)
        self.hil.N1SRC_ReqData__trigger.set(1)
        time.sleep(.100)
        temp_value = abs(self.hil.N1SRC_Measurement_Low__CurrentLow__value.get() * (0.00847711))
        self.hil.error_type.set(0)
        return temp_value

    def is_bus_started(self):
        """

        Returns: Which message is getting sent form WH first

        """
        WH_Sends_data = None
        flag = False
        nm_timestamp = self.hil.NM_Waehlhebel__timestamp.get()
        ds_timestamp = self.hil.DS_Waehlhebel__timestamp.get()
        kn_timestamp = self.hil.KN_Waehlhebel__timestamp.get()
        wh04_timestamp = self.hil.Waehlhebel_04__timestamp.get()
        timeout = 2
        t_out = timeout + t()
        while t_out > t():
            # curr_nm_timestamp = self.hil.NM_Waehlhebel__timestamp.get()
            # curr_ds_timestamp = self.hil.DS_Waehlhebel__timestamp.get()
            # curr_kn_timestamp = self.hil.KN_Waehlhebel__timestamp.get()
            # curr_wh04_timestamp = self.hil.Waehlhebel_04__timestamp.get()
            if nm_timestamp != self.hil.NM_Waehlhebel__timestamp.get():
                flag = True
                WH_Sends_data = ["WH Sends NM_Waehlhebel message first on Bus", "INFO"]
                break
            if ds_timestamp != self.hil.DS_Waehlhebel__timestamp.get():
                flag = True
                WH_Sends_data = ["WH Sends DS_Waehlhebel message first on Bus", "INFO"]
                break
            if kn_timestamp != self.hil.KN_Waehlhebel__timestamp.get():
                flag = True
                WH_Sends_data = ["WH Sends KN_Waehlhebel message first on Bus", "INFO"]
                break
            if wh04_timestamp != self.hil.Waehlhebel_04__timestamp.get():
                flag = True
                WH_Sends_data = ["WH Sends Waehlhebel_04 message first on Bus", "INFO"]
                break

        if flag:
            return WH_Sends_data
        else:
            return ["WH do not wake op in %s ms" %(timeout*1000), "INFO"]

    def send_CRC_error(self, message=None, no_CRC= None, period_on=False, wait= 0, period_off= False):
        """
        Args:
            message: Trigger for "SiShift_01" or "ORU_Control_A_01" or "ORU_Control_D_01" or "OTAMC_D_01"
            no_CRC: How many times CRC failure needs to be trigger
            period_on: Start the Cycle of the message
            wait: wait(in Sec) after triggering the failure
            period_off: set the cycletime of 0 after triggering the failure
        Returns: None
        """
        if message == "SiShift_01":
            trigger = 0
            SiShift_timestamp = self.hil.SiShift_01__timestamp.get()
            while True:
                self.hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0)
                self.hil.SiShift_01__period.setState("an") if period_on else None
                new_timestamp = self.hil.SiShift_01__timestamp.get()
                if SiShift_timestamp != new_timestamp:
                    SiShift_timestamp = new_timestamp
                    trigger = trigger + 1
                    if trigger == no_CRC:
                        break

        if message == "ORU_Control_A_01":
            trigger = 0
            ORUA_timestamp = self.hil.ORU_Control_A_01__timestamp.get()
            # self.hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0)
            # self.hil.ORU_Control_A_01__period.setState("an")
            while True:
                self.hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0)
                self.hil.ORU_Control_A_01__period.setState("an") if period_on else None
                new_timestamp = self.hil.ORU_Control_A_01__timestamp.get()
                if ORUA_timestamp != new_timestamp:
                    ORUA_timestamp = new_timestamp
                    trigger = trigger + 1
                    if trigger == no_CRC:
                        break

        if message == "ORU_Control_D_01":
            trigger = 0
            ORUD_timestamp = self.hil.ORU_Control_D_01__timestamp.get()
            # self.hil.ORU_Control_D_01__ORU_Control_D_01_CRC__value.set(0)
            # self.hil.ORU_Control_D_01__period.setState("an") if period_on else None
            while True:
                self.hil.ORU_Control_D_01__period.setState("an") if period_on else None
                self.hil.ORU_Control_D_01__ORU_Control_D_01_CRC__value.set(0)
                new_timestamp = self.hil.ORU_Control_D_01__timestamp.get()
                if new_timestamp != ORUD_timestamp:
                    ORUD_timestamp = new_timestamp
                    trigger = trigger + 1
                    if trigger == no_CRC:
                        break

        if message == "OTAMC_D_01":
            trigger = 0
            OTAMC_timestamp = self.hil.OTAMC_D_01__timestamp.get()
            # self.hil.OTAMC_D_01__OTAMC_D_01_CRC__value.set(0)
            # self.hil.OTAMC_D_01__period.setState("an")
            while True:
                self.hil.OTAMC_D_01__OTAMC_D_01_CRC__value.set(0)
                self.hil.OTAMC_D_01__period.setState("an") if period_on else None
                new_timestamp = self.hil.OTAMC_D_01__timestamp.get()
                if new_timestamp != OTAMC_timestamp:
                    OTAMC_timestamp = new_timestamp
                    trigger = trigger + 1
                    if trigger == no_CRC:
                        break

        #
        #
        # self.hil.SiShift_01__period.setState(
        #     "an") if period_on and message == "SiShift_01" else self.hil.ORU_Control_A_01__period.setState(
        #     "an") if period_on and message == "ORU_Control_A_01" else self.hil.ORU_Control_D_01__period.setState(
        #     "an") if period_on and message == "ORU_Control_D_01" else self.hil.OTAMC_D_01__period.setState(
        #     "an") if period_on and message == "OTAMC_D_01" else None
        #
        # timestamp = self.hil.SiShift_01__timestamp.get() if message == "SiShift_01" else self.hil.ORU_Control_A_01__timestamp.get() if message == "ORU_Control_A_01" else  self.hil.ORU_Control_D_01__timestamp.get() if message == "ORU_Control_D_01" else self.hil.OTAMC_D_01__timestamp.get() if message == "OTAMC_D_01" else None
        # self.hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0) if message == "SiShift_01"
        # self.hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0) if message == "ORU_Control_A_01"
        # self.hil.ORU_Control_D_01__ORU_Control_D_01_CRC__value.set(0) if message == "ORU_Control_D_01"
        # self.hil.OTAMC_D_01__OTAMC_D_01_CRC__value.set(0) if message == "OTAMC_D_01"
        # self.hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0) if message == "SiShift_01" else self.hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0) if message == "ORU_Control_A_01" else self.hil.ORU_Control_D_01__ORU_Control_D_01_CRC__value.set(0) if message == "ORU_Control_D_01" else  self.hil.OTAMC_D_01__OTAMC_D_01_CRC__value.set(0) if message == "OTAMC_D_01" else None
        # self.hil.SiShift_01__period.setState("an") if period_on and message == "SiShift_01"
        # self.hil.ORU_Control_A_01__period.setState("an") if period_on and message == "ORU_Control_A_01"
        # self.hil.ORU_Control_D_01__period.setState("an") if period_on and message == "ORU_Control_D_01"
        # self.hil.OTAMC_D_01__period.setState("an") if period_on and message == "OTAMC_D_01"
        # while timeout > t():
        #     self.hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0) if message== "SiShift_01"
        #     self.hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0) if message == "ORU_Control_A_01"
        #     self.hil.ORU_Control_D_01__ORU_Control_D_01_CRC__value.set(0) if message == "ORU_Control_D_01"
        #     self.hil.OTAMC_D_01__OTAMC_D_01_CRC__value.set(0) if message == "OTAMC_D_01"
        #
            # self.hil.SiShift_01__SiShift_01_20ms_CRC__value.set(0) if message == "SiShift_01" else  self.hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(0) if message == "ORU_Control_A_01" else  self.hil.ORU_Control_D_01__ORU_Control_D_01_CRC__value.set(0) if message == "ORU_Control_D_01" else  self.hil.OTAMC_D_01__OTAMC_D_01_CRC__value.set(0) if message == "OTAMC_D_01" else None
            # self.hil.SiShift_01__period.setState( "an") if period_on and message == "SiShift_01" else self.hil.ORU_Control_A_01__period.setState( "an") if period_on and message == "ORU_Control_A_01" else self.hil.ORU_Control_D_01__period.setState( "an") if period_on and message == "ORU_Control_D_01" else self.hil.OTAMC_D_01__period.setState("an") if period_on and message == "OTAMC_D_01" else None
            # new_timestamp = self.hil.SiShift_01__timestamp.get() if message== "SiShift_01" else self.hil.ORU_Control_A_01__timestamp.get() if message== "ORU_Control_A_01" else self.hil.ORU_Control_D_01__timestamp.get() if message== "ORU_Control_D_01" else self.hil.OTAMC_D_01__timestamp.get() if message== "OTAMC_D_01" else None
            # if timestamp != new_timestamp:
            #     timestamp = new_timestamp
            #     print timestamp, "The change of the timesatamp"
            #     trigger = trigger + 1
            #     print trigger, "this many times the error is sent"
            #     if trigger == no_CRC:
            #         print trigger, "this many times the error is sent"
            #         break
        time.sleep(wait)
        self.hil.SiShift_01__period.setState("aus") if period_off and message == "SiShift_01" else self.hil.ORU_Control_A_01__period.setState("aus") if period_off and message == "ORU_Control_A_01" else self.hil.ORU_Control_D_01__period.setState("aus") if period_off and message == "ORU_Control_D_01" else self.hil.OTAMC_D_01__period.setState("aus") if period_off and message == "OTAMC_D_01" else None


    ###################################################################################################################
    ###################################################################################################################
    ########################## FROM HERE STARTS THE USE OF ISOX WH MESSAGES   #########################################
    ########################## FROM HERE STARTS THE USE OF ISOX WH MESSAGES   #########################################
    ###################################################################################################################
    ###################################################################################################################
    def send_ISOx_req(self, requestlist, job_len=None, msg_length=None):
        """

        Args:
            requestlist: request in str
            job_len: byte length of req
            msg_length: msg length of request
        Returns:response, len_response
        """
        self.hil.ISOx_Waehlhebel_Req_FD__length.set(msg_length)
        request = job_len+ requestlist
        # request = hex(int(requestlist + lenReq, 16)).split("x")[-1]
        dec_num = self.hex_dec_rev(request)
        self.hil.ISOx_Waehlhebel_Req_FD__ISOx_Waehlhebel_Req_FD_Data__value.set(dec_num)

        # send one request
        time_stamp = self.hil.ISOx_Waehlhebel_Resp_FD__timestamp.get()
        self.hil.ISOx_Waehlhebel_Req_FD__period.set(300)
        t_out = 5 + t()
        while t_out > t():
            curr_timestamp = self.hil.ISOx_Waehlhebel_Resp_FD__timestamp.get()
            if time_stamp != curr_timestamp:
                break
        self.hil.ISOx_Waehlhebel_Req_FD__period.set(0)
        result = self.hil.ISOx_Waehlhebel_Resp_FD__ISOx_Waehlhebel_Resp_FD_Data__value.get()
        result_dl = self.hil.ISOx_Waehlhebel_Resp_FD__length.get()
        response, res_length, hex_l = self.toHex(result, result_dl)
        return response, result_dl, hex_l

    def hex_dec_rev(self, request):
        little_hex = bytearray.fromhex(request)
        little_hex.reverse()
        str_little = ''.join(format(x, '02x') for x in little_hex)
        return int(str_little, 16)

    def toHex(self, response, dl):
        print response, "THE DECIMAL RESPONSE"
        result = hex(response)[2:].rstrip("L")
        print result, "THE HEX RESPONSE"
        little_hex = bytearray.fromhex(result.zfill(dl*2))
        print little_hex, "THE LITTLE HEX VALUE"
        little_hex.reverse()
        str_little = ''.join(format(x, '02x') for x in little_hex)
        split_by = self.split_bytes(str_little)
        d = [int(i, 16) for i in split_by]
        # str_to_list = map(int, split_by)
        hex_l= HexList(d)
        print hex_l, "PRINT HEX LIST"
        return d[1:], d[0], d

    def split_bytes(self, s):
        return re.split("(\w\w)", s[:])[1::2]

    def crc_trigger(self, message, number_of_trigger, cycletime):
        pass


    def checkResponse(self, diag_response, diag_expected_response, ticket_id=None):
        """
        Parameter:
            diag_response            - raw response, e.g. returned by function sendDiagRequest
            diag_expected_response   - a list with diagnosis job, e.g. [0x62, 0xF1, 0x97, 0x54, 0x75]
            ticket_id                - to add the ticket ID as Comment to verdict
        Info:
           Checks if response is as expected.
        Return:
            description, verdict
        """
        actual_response_str = str(HexList(diag_response))
        expected_response_str = str(HexList(diag_expected_response))
        if (len(diag_response) > 0):
            description = (
                              "Erwartete Response: %s\n"
                              "Aktuelle Response: %s"
                          ) % (expected_response_str, actual_response_str)

            if actual_response_str == expected_response_str:
                verdict = "PASSED"
            else:
                verdict = "FAILED"

        else:
            description = (
                              "Keine Response erhalten\n"
                              "Aktuelle Response: %s\n"
                              "Erwartete Response: %s"
                          ) % (actual_response_str, expected_response_str)
            verdict = "FAILED"

        if ticket_id:
            return [description, "[[COMMENT]] %s" % ticket_id, verdict]
        else:
            return [description, verdict]

    def checkPositiveResponse(self, diag_response, diag_request, job_length=3, ticket_id=None):
        """
        Parameter:
            diag_response     - raw response, e.g. returned by function sendDiagRequest
            diag_request      - original request, e.g. [0x22, 0xF1, 0x97]
            job_length        - job length (default = 3, 2..4 are known values)
            ticket_id                - to add the ticket ID as Comment to verdict
        Info:
           Just checks if response is positive. The expected response calculated from the
           job request and length (value 0x40 is added to the first byte).
        Return:
            description, verdict
        """
        actual_response_str = diag_response
        actual_response_str = str(actual_response_str)
        add_info = ""

        if (
                (len(diag_response) >= job_length) and
                (len(diag_request) >= job_length)
        ):
            actual_response_job = diag_response[:job_length]
            expected_response_job = diag_request[:job_length]
            expected_response_job[0] += 0x40  # add 0x40 to first byte
            actual_response_job_str = str(
                HexList(actual_response_job))
            expected_response_job_str = str(
                HexList(expected_response_job))

            if actual_response_job == expected_response_job:  # compare lists
                verdict = "PASSED"
            else:
                verdict = "FAILED"
                if diag_response[0] == 0x7F:  # negative response
                    if diag_response[-1] in self.nrc_dict.keys():
                        add_info = "(%s)" % self.nrc_dict[diag_response[-1]]

            description = (
                              "Aktuelle Response: %s %s\n"
                              "Erste Bytes der aktuellen Response (Job): %s\n"
                              "Erste Bytes der erwarteten Response (Job): %s"
                          ) % (
                              actual_response_str, add_info,
                              actual_response_job_str,
                              expected_response_job_str
                          )


        else:
            request_str = str(HexList(diag_request))
            verdict = "FAILED"
            if diag_response:
                if diag_response[0] == 0x7F:  # negative response
                    if diag_response[-1] in self.nrc_dict.keys():
                        add_info = "(%s)" % self.nrc_dict[diag_response[-1]]

            description = (
                              "Keine oder falsche Response erhalten\n"
                              "Aktuelle Response: %s %s\n"
                              "Job-Länge: %s\n"
                              "Request: %s"
                          ) % (actual_response_str, add_info, job_length, request_str)

        if ticket_id:
            return [description, "[[COMMENT]] %s" % ticket_id, verdict]
        else:
            return [description, verdict]

    def checkNegativeResponse(self, diag_response, diag_request, exp_nrc, ticket_id=None):
        """
        Parameter:
            diag_response     - raw response, e.g. returned by function sendDiagRequest
            diag_request      - original request, e.g. [0x22, 0xF1, 0x97]
            exp_nrc           - expected NRC, e.g. 0x7E
            ticket_id                - to add the ticket ID as Comment to verdict
        Info:
           Just checks if response is negative. The expected response created from the
           job request and nrc.
        Return:
            description, verdict
        """

        actual_response_str = str(HexList(diag_response))
        # diag_request_hex = HexList(diag_request)
        expected_response = [0x7F] + [diag_request[0]] + [exp_nrc]
        expected_response_str = str(HexList(expected_response))
        curr_nrc = '-'
        if len(diag_response) >= 3:
            if diag_response[0] == 0x7F:  # negative response
                curr_nrc = self.nrc_dict[diag_response[-1]] if diag_response[
                                                                   -1] in self.nrc_dict.keys() else "unkown NRC"

            description = (
                              "Aktuelle Response: %s (%s)\n"
                              "Erwartete Response: %s (%s)\n"
                          ) % (
                              actual_response_str, curr_nrc,
                              expected_response_str, self.nrc_dict[exp_nrc]
                          )
            if diag_response == expected_response:  # compare lists
                verdict = "PASSED"
            else:
                verdict = "FAILED"

        else:
            #             request_str = str(HexList(diag_request))
            description = (
                              "Keine oder falsche Response erhalten\n"
                              "Aktuelle Response: %s\n"
                              "Erwartete Response: %s (%s)"
                          ) % (actual_response_str, expected_response_str, self.nrc_dict[exp_nrc])
            verdict = "FAILED"

        if ticket_id:
            return [description, "[[COMMENT]] %s" % ticket_id, verdict]
        else:
            return [description, verdict]

    def checkDataLength(self, diag_response, exp_data_length, job_length=3, ticket_id=None):
        """
        Parameter:
            diag_response     - raw response, e.g. returned by function sendDiagRequest
            exp_data_length   - expected data length (bytes of diag job not included)
            job_length        - job length (default = 3; 2..4 are known values)
            ticket_id                - to add the ticket ID as Comment to verdict
        Info:
           Checks that the data length of the received response is as expected.
        Return:
            description, verdict
        """
        actual_response_str = str(HexList(diag_response))
        if (len(diag_response) >= job_length):
            actual_data_length = len(diag_response[job_length:])
            description = (
                              "Aktuelle Response: %s\n"
                              "Aktuelle Datenlänge: %s\n"
                              "Erwartete Länge: %s"
                          ) % (actual_response_str, actual_data_length, exp_data_length)
            if actual_data_length == exp_data_length:
                verdict = "PASSED"
            else:
                verdict = "FAILED"

        else:
            description = (
                              "Response enthält keine Daten!\n"
                              "Aktuelle Response: %s\n"
                              "Erwartete Länge: %s"
                          ) % (actual_response_str, exp_data_length)
            verdict = "FAILED"

        if ticket_id:
            return [description, "[[COMMENT]] %s" % ticket_id, verdict]
        else:
            return [description, verdict]

    def checkDataRange(self, diag_response, min_data_length, max_data_length, job_length=3, ticket_id=None):
        """
        Parameter:
            diag_response     - raw response, e.g. returned by function sendDiagRequest
            min_data_length   - minimum expected data length (bytes of diag job not included)
            max_data_length   - maximum expected data length (bytes of diag job not included)
            job_length        - job length (default = 3; 2..4 are known values)
            ticket_id                - to add the ticket ID as Comment to verdict
        Info:
           Checks that the data length of the received response is as expected.
        Return:
            description, verdict
        """
        actual_response_str = str(HexList(diag_response))
        if (len(diag_response) >= job_length):
            actual_data_length = len(diag_response[job_length:])
            description = (
                              "Aktuelle Response:\n"
                              "Aktuelle Datenlänge: %s\n"
                              "Erwartete Länge: %s >= n >= %s"
                          ) % (actual_data_length, min_data_length, max_data_length)
            if min_data_length <= actual_data_length <= max_data_length:
                verdict = "PASSED"
            else:
                verdict = "FAILED"

        else:
            description = (
                              "Response enthält keine Daten!\n"
                              "Aktuelle Response: %s\n"
                              "Erwartete Länge: %s >= n >= %s"
                          ) % (actual_response_str, min_data_length, max_data_length)
            verdict = "FAILED"

        if ticket_id:
            return [description, "[[COMMENT]] %s" % ticket_id, verdict]
        else:
            return [description, verdict]

    def checkResponseBitMask(self, diag_response, bit_mask, job_length=3, ticket_id=None):
        """
        Parameter:
            diag_response     - raw response, e.g. returned by function sendDiagRequest
            bit_mask          - expected bit mask as a string, 'x' or 'X' for 'don't care', e.g. 'XX101X11'
            job_length        - job length (default = 3; 2..4 are known values)
            ticket_id                - to add the ticket ID as Comment to verdict
        Info:
           Checks that the given bit mask match the response.
        Return:
            description, verdict
        """
        bit_mask = bit_mask.upper()

        if len(diag_response) > job_length:
            data = diag_response[job_length:]  # just take data of complete response
            value_dec = 0
            i = len(diag_response) - job_length - 1
            for value in data:
                value_dec += value << (i * 8)  # set all bytes together
                i -= 1

            response_length = len(diag_response) - job_length  # in bytes
            binary_response = bin(value_dec)[2:].zfill(response_length * 8)

            if len(binary_response) == len(bit_mask):
                verdict = "PASSED"
                description = ("Einzelne Bits der Response stimmen überein!\n"
                               "Erwartete Bitmaske: %s\n"
                               "Response (Bits): %s" % (bit_mask, binary_response))
                for bit in range(0, len(binary_response)):

                    if (binary_response[bit] != bit_mask[bit]) and (bit_mask[bit] != 'X'):
                        verdict = "FAILED"
                        description = ("Einzelne Bits der Response stimmen NICHT überein!\n"
                                       "Erwartete Bitmaske: %s\n"
                                       "Response (Bits): %s" % (bit_mask, binary_response))
            else:
                verdict = "FAILED"
                description = "Länge der erwarteten Bitmaske stimmt nicht mit der Länge der Response ein!"
        else:
            verdict = "FAILED"
            description = "Keine oder falsche Antwort erhalten!"

        if ticket_id:
            return [description, "[[COMMENT]] %s" % ticket_id, verdict]
        else:
            return [description, verdict]

    def readDiagSession(self, ticket_id=None):
        """
        Parameter:
            ticket_id                - to add the ticket ID as Comment to verdict
        Info:
           Reads out the current diagnostic session.
        Return:
            testresult
        """
        session_dict = {
            '[0x62, 0xF1, 0x86, 0x01]': 'default',
            '[0x62, 0xF1, 0x86, 0x02]': 'programming',
            '[0x62, 0xF1, 0x86, 0x03]': 'extended',
            '[0x62, 0xF1, 0x86, 0x60]': 'factory_mode'
        }

        testresult = []
        diag_request = [0x22, 0xF1, 0x86]
        diad_re= "22F186"
        len_re = "03"
        response, len_res, result_list = self.send_ISOx_req(diad_re, len_re, msg_length=8)
        testresult.append(response)
        actual_response_str = str(HexList(response[0:4]))

        if actual_response_str in session_dict:
            current_session = session_dict[actual_response_str]
            description = "Aktuelle Diagnose Session: '%s session'" % (current_session)
            verdict = "INFO"
        else:
            description = "Unbekannte Diagnose Session: %s" % (actual_response_str)
            verdict = "FAILED"
        if ticket_id:
            testresult.append([description, "[[COMMENT]] %s" % ticket_id, verdict])
        else:
            testresult.append([description, verdict])

        return testresult

    def checkEventMemoryEmpty(self, ticket_id=None):
        '''
        Args:
            ticket_id                - to add the ticket ID as Comment to verdict
        Returns:
        '''

        return self.checkEventMemory([], ticket_id=ticket_id)

    def checkEventMemory(self, error_list, mode='EQUAL', ticket_id=None):
        """
        Parameter:
            error_list:      all expected DTC in a list [(DTCNumber, State), (DTCNumber, State),...]
            mode:            'EQUAL':   given DTCs (error_list) are equal to the DTCs found in
                                        error memory (dtc_list), no unexpected DTC is allowed
                             'ALL':     all DTCs given in the error_list are found in error memory
                                        (error memory can have more entries)
                             'NONE':    none of the given DTCs is found in error memory
                             'ONE_OR_MORE': at least one of the given (dtc, status) tuples is found
            ticket_id                - to add the ticket ID as Comment to verdict
        Returns:
            description, verdict
        """

        self.dtc_whitelist = data_common.DTCwhitelist[:]
        read_event_memory = "19022f"
        read_event_memory_len = "03"
        diag_response, len_res, response = self.send_ISOx_req(read_event_memory, read_event_memory_len, msg_length=8)

        if len_res == 8:
            diag_response = response[1: response[0]+1]
            print diag_response, "IN 6 BYTE LOOP"
        elif len_res == 16 or len_res == 32:
            diag_response = response[1: response[0]+ response[0] + 1]
            print diag_response, "IN 16 BYTE LOOP"

        diag_response = HexList(diag_response)

        err_msg_list = []
        description = None  # initial

        if diag_response is None or diag_response == []:
            description = "No error memory response, can't check DTC",
            verdict = "FAILED"
            print "IN IF LPPPPPPP"
        else:  # regular case
            dtc_list = self.getEventMemoryList(diag_response)
            if dtc_list is None:  # NOTE: empty list is not an error here
                description = "No error memory response, can't check DTC",
                verdict = "FAILED"
                print "IN ELSE LPPPPPPP", diag_response
            else:
                # copy dtc list (unmodified) to class member variable
                self.dtc_list = dtc_list[:]
                success = self._verifyMain(
                    dtc_list, error_list, err_msg_list, mode
                )
                # ---------------------------------------------------------------------
                # OUTPUT: DTC check evaluation
                # ---------------------------------------------------------------------
                verdict = "PASSED" if success else "FAILED"

                if description is None:  # if it still has its inital value (case where _verifyMain() is executed)
                    # create a single test result entry from err_msg_list
                    description = '\n'.join(err_msg_list)

        if ticket_id:
            return [description, "[[COMMENT]] %s" % ticket_id, verdict]
        else:
            return [description, verdict]

    def getEventMemoryList(self, canape_diag_responses):
        """
            Parameter:
                canape_diag_responses - the response from canape of read event memory
            Info:
                read if DTCs are returned and create a list with all dtcs (dtcnumber as integer, state)
            Return:
                dtc_list
        """
        dtc_list = None  # initial
        # other responses couldn't be handled at the moment
        if len(canape_diag_responses) == 1:
            response = canape_diag_responses[0]
            res_len = len(response)
            if res_len < 3:  # "Liste mit Fehlerspeicherinhalt zu klein"
                pass
            elif ((res_len > 3) and (((res_len - 3) % 4) != 0)):  # "Liste mit Fehlerspeicherinhalt fehlerhaft"
                pass
            else:  # response format checked successfully
                # negative response:
                if ((response[0] == 0x7F) and (response[1] == 0x19)):
                    pass
                # positive response:
                else:
                    i = 3
                    dtc_list = []  # list of (dtc, status)-tuples
                    while i <= (res_len - 4):
                        dtc_list.append(
                            (  # IMPORTANT: use tuple type (2 elements)
                                (  # DTC as number (integer)
                                        (response[i] << 16) +
                                        (response[i + 1] << 8) +
                                        (response[i + 2])
                                ),
                                response[i + 3]  # status byte
                            )
                        )
                        i += 4  # goto start of next dtc entry
        return dtc_list

    def _verifyMain(self, dtc_list, error_list, err_msg_list, mode):
        """
        Parameter:
            dtc_list:         all received DTCs in a list [(dtcnum as int, state), (), ..]
            error_list:       list with all expected DTCs + State
            err_msg_list:     list for all evaluated results
            mode:            "EQUAL", "ALL", "NONE"--- see CheckEventMemory

        Info: create new modified dtc list -> variable: dtc_list_mod
              remove whitelist-entries from dtc_list,
              if they can't be found in error_list
             (compare only DTC numbers, ignore status values in error_list)
        Returns:
            success (PASSED or FAILED)
        """
        error_list_dtc_numbers = []  # list of dtc numbers in error_list (without state)
        for err_el in error_list:
            err_dtc = err_el[0]
            error_list_dtc_numbers.append(err_dtc)

        dtc_list_mod = []
        for el in dtc_list:
            dtc = el[0]  # extract dtc from (dtc,status)-tuple (without state)
            # only dtc number comparisons (no status)
            if (dtc in self.dtc_whitelist and dtc not in error_list_dtc_numbers):
                err_msg_list.append(  # hint for DTC from Whitelist
                    "(No validation: DTC 0x%06X in error memory)" % (dtc))
            else:
                dtc_list_mod.append(el)  # element should be evaluated
        # NOTE:
        # from this position on modified (dtc_list_mod) dtc list is used for
        # evaluation and call of subfunctions
        self.dtc_list_mod = dtc_list_mod[:]  # copy in member variables

        # ---------------------------------------------------------------------
        # output: display check mode (exception: 'EQUAL'= default method)
        # ---------------------------------------------------------------------
        """
        if self.dtc_output_check_mode:
            if mode != 'EQUAL':
                err_msg_list.append("CHECK [%s]: %s"
                                    % (mode, self.check_mode_description.get(mode, '')))
        """

        # Evaluate count of DTCs
        # NOTE: 'success' is set to True if the error memory is empty as
        # expected, otherwise False is set and a further, individual DTC
        # check is required, consider that as an initialization of 'success'
        # variable
        success = self._verifySub_ErrorCount(
            dtc_list_mod, error_list, err_msg_list, mode)
        if not success:
            # 2 different comparing methods are supported (in pricipible)
            if self.check_dtc_order:  # check correct order
                success = self._verifySub_InOrder(
                    dtc_list_mod, error_list, err_msg_list, mode)
            else:  # ordner will not checked
                success = self._verifySub_IgnoreOrder(
                    dtc_list_mod, error_list, err_msg_list, mode)

        return success

    def _verifySub_IgnoreOrder(self, dtc_list, error_list, err_msg_list, mode):
        """
        Parameter:
                 dtc_list:       all received DTCs in a list [(dtcnum as int, state), (), ..]
                                 (without whitlist DTCs)
                error_list:      list with all expected DTCs + State
                err_msg_list:    list for all evaluated results
                mode:            "EQUAL", "ALL", "NONE"--- see CheckEventMemory
            Info:
                helper function called in _verifyMain()
                This function handles of DTCs found in error memory
            Return:
                True or False
        """
        dtc_found_in_error_list = []
        dtc_not_in_error_list = []
        error_not_in_dtc_list = []

        # loop over error memory DTC list
        for el in dtc_list:
            dtc = el[0]
            status = el[1]
            found_flag = False
            for error_el in error_list:
                # dtc_found_in_error_list (expected DTCs)
                if (error_el == el):  # dtc and status
                    dtc_found_in_error_list.append(error_el)
                    found_flag = True
            # dtc_not_in_error_list (unexpected DTCs)
            if not found_flag:
                dtc_not_in_error_list.append(el)  # append tuple (dtc, status)

        # error_not_in_dtc_list (missing DTCs)
        for error_el in error_list:
            if error_el not in dtc_list:
                error_not_in_dtc_list.append(error_el)

        # copy these lists to member variables
        self.dtc_found_in_error_list = dtc_found_in_error_list[:]
        self.dtc_not_in_error_list = dtc_not_in_error_list[:]
        self.error_not_in_dtc_list = error_not_in_dtc_list[:]

        # ---------------------------------------------------------------------
        # OUTPUT: DTC evaluation, 3 different cases (1)-(3)
        # NOTE: output slightly differs depending on check mode
        # ---------------------------------------------------------------------
        if self.dtc_output_detail:  # show following messages (normally=True)
            # (1) Expected DTC
            if len(dtc_found_in_error_list) > 0:
                err_msg_list.append("> Given DTCs found in error memory:")
                for el in dtc_found_in_error_list:
                    dtc = el[0]
                    status = el[1]
                    if mode in ['EQUAL', 'ALL', 'ONE_OR_MORE']:
                        extra_str = " (expected)"
                    else:
                        extra_str = ""
                    err_msg_list.append("DTC%s: 0x%06X, Status: 0x%02X"
                                        % (extra_str, dtc, status))
                    # ---------------------------------------------------------
                    # special: display status splitted in bits
                    # ---------------------------------------------------------
                    if self.dtc_output_status:
                        # use extend(), because getStatusInfo returns a list
                        # of strings
                        err_msg_list.extend(self.getStatusInfo(status))

            # (2) Missing DTC
            if len(error_not_in_dtc_list) > 0:
                err_msg_list.append("> Given DTCs not found in error memory:")
                for el in error_not_in_dtc_list:
                    dtc = el[0]
                    status = el[1]
                    extra_str = " (missing)" if mode in ['EQUAL', 'ALL'] else ""
                    err_msg_list.append(
                        "DTC%s: 0x%06X, Status: 0x%02X" % (
                            extra_str,
                            dtc,
                            status
                        )
                    )

            # (3) Unexpected DTC
            if len(dtc_not_in_error_list) > 0:
                err_msg_list.append("> Not given DTCs found in error memory:")
                for el in dtc_not_in_error_list:
                    dtc = el[0]
                    status = el[1]
                    extra_str = " (unexpected)" if mode in ['EQUAL', 'ALL', 'ONE_OR_MORE'] else ""

                    # ---------------------------------------------------------
                    # display dtc and status
                    # ---------------------------------------------------------
                    err_msg_list.append(
                        "DTC%s: 0x%06X, Status: 0x%02X" % (
                            extra_str,
                            dtc,
                            status
                        )
                    )
                    # -----------------------------------------------------
                    # special: display status splitted in bits
                    # -----------------------------------------------------
                    if self.dtc_output_status:
                        # use extend(), because getStatusInfo returns a
                        # list of strings
                        err_msg_list.extend(self.getStatusInfo(status))

        # ---------------------------------------------------------------------
        # OUTPUT: result of DTC check,
        #         dependend on the 'mode' parameter
        # Description of check modes: see dictionary variable
        self.check_mode_description = {}
        # ---------------------------------------------------------------------
        if mode == 'EQUAL':  # default case
            success = (
                    (len(error_not_in_dtc_list) == 0) and  # no missing DTC
                    (len(dtc_not_in_error_list) == 0)  # no unexpected DTC
            )
        elif mode == 'ALL':
            success = (len(dtc_found_in_error_list) >= len(error_list))
        elif mode == 'NONE':
            success = (len(dtc_found_in_error_list) == 0)
        elif mode == 'ONE_OR_MORE':
            success = (len(dtc_found_in_error_list) > 0)
        else:
            success = False
            err_msg_list.append(
                "ERROR: Unsupported check mode (%s) has been chosen" % (mode)
            )

        return success

    def _verifySub_InOrder(self, dtc_list, error_list, err_msg_list, mode):
        """
        Parameter:
                 dtc_list:       all received DTCs in a list [(dtcnum as int, state), (), ..]
                                 (without whitlist DTCs)
                error_list:      list with all expected DTCs + State
                err_msg_list:    list for all evaluated results
                mode:            "EQUAL", "ALL", "NONE"--- see CheckEventMemory
            Info:
                helper function called in _verifyMain()
                This function handles the DTCs found in error memory
            Return:
                True, False
        """

        err_msg_list.append(
            (
                "The order of entries in error memory must be the same"
                "as in the given DTC list"
            )
        )
        # check length of lists, same length is required
        success = True if len(dtc_list) == len(error_list) else False

        # go throug dtc_list and error_list and compare corresponding elements
        idx = 0
        for el in dtc_list:
            dtc = el[0]
            status = el[1]
            if len(error_list) <= idx:
                success = False
                break

            err_dtc = error_list[idx][0]
            err_status = error_list[idx][1]
            err_msg_list.append(
                (
                    "%s.: expected: (0x%06X, 0x%02X, %s), "
                    "actual: (0x%06X, 0x%02X, %s)"
                ) % ((idx + 1), err_dtc, err_status, self.d2t.getDTCText(err_dtc),
                     dtc, status, self.d2t.getDTCText(dtc))
            )
            if not ((dtc == err_dtc) and (status == err_status)):
                success = False
            idx += 1  # increment (error_list) counter idx

        if success:
            err_msg_list.append(
                (
                    "The error memory is equal to the given DTC list "
                    "(in same order)"
                )
            )
        else:
            err_msg_list.append(
                "The error memory is different from the given DTC list"
            )
        return success


    def _verifySub_ErrorCount(self, dtc_list, error_list, err_msg_list, mode):
        """
            Parameter:
                 dtc_list:       all received DTCs in a list [(dtcnum as int, state), (), ..]
                                 (without whitlist DTCs)
                error_list:      list with all expected DTCs + State
                err_msg_list:    list for all evaluated results
                mode:            "EQUAL", "ALL", "NONE"--- see CheckEventMemory
            Info:
                helper function called in _verifyMain()
                This function handles the count of DTCs found in error memory
            Return:
                'True' signals an 'empty memory as expected'
                'False' usually mean: further evaluation is needed
        """
        err_mem_empty = False
        sollAnzahl = len(error_list)
        aktuelleAnzahl = len(dtc_list)  # after white list modification

        if mode in ['EQUAL']:
            ERR_CNT_MSG = "> Count of DTCs: (expected: %i / actual: %i)" % (
                sollAnzahl, aktuelleAnzahl)
        else:  # expected count can't be given
            ERR_CNT_MSG = "> Count of DTCs: %s" % (aktuelleAnzahl)

        if aktuelleAnzahl == sollAnzahl:
            if aktuelleAnzahl == 0:
                err_msg_list.append("The error memory is empty as expected")
                err_mem_empty = True
            else:
                err_msg_list.append(ERR_CNT_MSG)

        # less DTC errors than expected
        elif aktuelleAnzahl < sollAnzahl:
            err_msg_list.append(ERR_CNT_MSG)

        # more DTC errors than expected
        else:
            err_msg_list.append(ERR_CNT_MSG)

        # return True if error memory is empty as expected
        return err_mem_empty

    def checkDTCConfig(
            self,
            count=True, detail=True, descr=True, status=False, check_mode=True, order=False
    ):
        self.dtc_output_descr = descr  # DTC description
        self.dtc_output_check_mode = check_mode
        self.dtc_output_count = count  # expected/actual DTC count
        self.dtc_output_detail = detail  # expected/missing/unexpected DTCs
        self.dtc_output_status = status  # status details
        self.check_dtc_order = order  # Reihenfolge


def _checkStatus(current_status, nominal_status, equal=True, descr="", format=None, ticket_id=None):
    result = checkStatus(current_status, nominal_status, equal=equal, descr=descr, format=format)
    if ticket_id is None:
        for i in range(len(result)):
            return [result[0], result[-1]]
    else:
        return [(result)[0],"[[COMMENT]] %s" % ticket_id, (result)[-1]]


def _checkRange(value, min_value, max_value, descr="", format=None, ticket_id=None):
    result = checkRange(value, min_value, max_value, descr=descr, format=format)
    if ticket_id is None:
        for i in range(len(result)):
            return [result[0], result[-1]]
    else:
        return [(result)[0], "[[COMMENT]] %s" % ticket_id, (result)[-1]]


def _compare(left_value, operator, right_value, abs_tol=0, descr="", format=None, ticket_id=None):
    result= compare(left_value, operator, right_value, abs_tol=abs_tol, descr=descr, format=format)
    if ticket_id is None:
        for i in range(len(result)):
            return [result[0], result[-1]]
    else:
        return [(result)[0], "[[COMMENT]] %s" % ticket_id, (result)[-1]]


def _checkBitMask(value, mask, operator="AND", bit_length=CHECKBITMASK_DEFAULT_BIT_LENGTH,pass_on_true=True,descr="", format=None, ticket_id=None):
    result = checkBitMask(value, mask, operator=operator, bit_length=bit_length, pass_on_true=pass_on_true, descr=descr, format=format)
    if ticket_id is None:
        for i in range(len(result)):
            return [result[0], result[-1]]
    else:
        return [(result)[0], "[[COMMENT]] %s" % ticket_id, (result)[-1]]


def _checkBitPattern(value, pattern, descr="", format=None, ticket_id=None):  # @ReservedAssignment: format
    result = checkBitPattern(value, pattern, descr=descr, format=format)
    if ticket_id is None:
        for i in range(len(result)):
            return [result[0], result[-1]]
    else:
        return [(result)[0], "[[COMMENT]] %s" % ticket_id, (result)[-1]]


# #############################################################################
def _checkBit(value, offset, status=1, descr="", format=None, ticket_id=None):
    result = checkBit(value, offset, status=status, descr=descr, format=format)
    if ticket_id is None:
        for i in range(len(result)):
            return [result[0], result[-1]]
    else:
        return [(result)[0], "[[COMMENT]] %s" % ticket_id, (result)[-1]]


def _checkTolerance(current_value, rated_value, rel_pos=0, abs_pos=0, rel_neg=None, abs_neg=None, descr="", format=None, ticket_id=None):
    result = checkTolerance(current_value, rated_value, rel_pos=rel_pos, abs_pos=abs_pos, rel_neg=rel_neg, abs_neg=abs_neg, descr=descr, format=format)
    if ticket_id is None:
        for i in range(len(result)):
            return [result[0], result[-1]]
    else:
        return [(result)[0], "[[COMMENT]] %s" % ticket_id, (result)[-1]]


def _compareCE(current_value, operator, expected_value, abs_tol=0, descr="", ticket_id=None):
    result = compareCE(current_value, operator, expected_value, abs_tol=abs_tol, descr=descr)
    if ticket_id is None:
        for i in range(len(result)):
            return [result[0], result[-1]]
    else:
        return [(result)[0], "[[COMMENT]] %s" % ticket_id, (result)[-1]]


def _contains(defined_values, current_value, mode="all", descr="", format=None, ticket_id=None):
    result = contains(defined_values, current_value, mode=mode, descr=descr, format= format)
    if ticket_id is None:
        for i in range(len(result)):
            return [result[0], result[-1]]
    else:
        return [(result)[0], "[[COMMENT]] %s" % ticket_id, (result)[-1]]


class HexList(list):
    """
        This Class returns a representation in hexadecimal notation (for easier reading)
    """

    def __getitem__(self, index):
        item = list.__getitem__(self, index)
        if isinstance(item, str): return ord(item)
        return item

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        seq = []
        for item in self:
            if isinstance(item, str): item = ord(item)
            seq.append("0x%.2X" % (int(item)))
        return '[' + ', '.join(seq) + ']'




