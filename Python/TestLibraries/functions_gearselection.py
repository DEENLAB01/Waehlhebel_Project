#******************************************************************************
# -*- coding: latin-1 -*-
# File    : functions_gearselection.py
# Task    : functions to work with gear selection
#
# Author  : An3Neumann
# Date    : 18.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 18.05.2021 | An3Neumann | initial
#******************************************************************************
from ttk_daq import eval_signal
from ttk_checks import basic_tests
import time

class FunctionsGearSelection(object):
    
    def __init__(self, testenv, hil):
        """
         init constructor
         testenv    - testenn instance
         hil        - hil instance for gamma variables
         daq        - daq instance (functions_daq.py) if needed for functions
        """
        self.testenv = testenv
        self.hil = hil

        # cycltetimes in ms
        self.messages_tx_cycletimes = { # Only signals with cycletime
            'self.hil.DS_Waehlhebel': 1000,
            'self.hil.KN_Waehlhebel': 500,
            'self.hil.Waehlhebel_04': 10,
            'self.hil.NM_Waehlhebel': 200,
        }

        self.messages_tx = [
            'self.hil.DEV_Waehlhebel_Req_00',
            'self.hil.DEV_Waehlhebel_Resp_FF',
            'self.hil.DS_Waehlhebel',
            'self.hil.KN_Waehlhebel',
            'self.hil.Waehlhebel_04',
            'self.hil.NM_Waehlhebel',
        ]
        self.messages_rx = [
            'self.hil.ClampControl_01',
            #'self.hil.DIA_SAAM_Req',
            #'self.hil.DPM_01',
            'self.hil.Diagnose_01',
            'self.hil.Dimmung_01',
            #'self.hil.ISOx_Funkt_Req_All_FD',
            'self.hil.NM_Airbag',
            'self.hil.NM_HCP1',
            'self.hil.NVEM_12',
            #'self.hil.OBDC_Funktionaler_Req_All_FD',
            #'self.hil.OBDC_Waehlhebel_Req_FD',
            'self.hil.OBD_03',
            'self.hil.OBD_04',
            'self.hil.ORU_01',
            'self.hil.ORU_Control_A_01',
            'self.hil.ORU_Control_D_01',
            #'self.hil.OTAMC_01',
            'self.hil.OTAMC_D_01',
            'self.hil.SiShift_01',
            'self.hil.Systeminfo_01',
            'self.hil.VDSO_05',
        ]


    def getAllRXPeriods(self, type = 'all'):
        """
        Args:
            type:       all or cycletimes, then only cycletime signales are used
        Returns: list with all RX period signals

        """
        signals = self.messages_rx if type == 'all' else self.messages_tx_cycletimes.keys()
        def addPeriod(x):
            return x+"__period"
        period_signals = map(addPeriod, signals)
        return map(eval, period_signals)

    def getAllTimestamps(self, direction, type = 'all'):
        """
        Args:
            direction: RX or TX
            type:  all or cycletimes, then only cycletime signales are used (only for RX!!)

        Returns: list with all RX or TX timestamp signals
        """
        if direction.upper() == "TX":
            signals = self.messages_tx if type == 'all' else self.messages_tx_cycletimes.keys()
        else:
            signals = self.messages_rx
        def addTimestamp(x):
            return x+"__timestamp"
        timestamp_signals = map(addTimestamp, signals)
        return map(eval, timestamp_signals)

    def switchAllRXMessagesOff(self):
        """
        normally the variable can0_HIL__HIL_TX__enable can used
        but if a single message shall switched on during "off", this function should be used
        switch all messages, which are received from ECU (HIL --> ECU) off
        """

        messages_rx = self.getAllRXPeriods()

        for message in messages_rx:
            message.setState("aus")

        return "Schalte Periode von empfangenen Signalen auf 0 (HiL -> ECU)", "INFO"

    def switchAllRXMessagesOn(self):
        """
        normally the variable can0_HIL__HIL_TX__enable can used
        but if a single message shall switched on during "off", this function should be used
        switch all messages, which are received from ECU (HIL --> ECU) off
        """
        messages_rx = self.getAllRXPeriods()

        for message in messages_rx:
            message.setState("an")

        return "Schalte Periode von empfangenen Signalen an (HiL -> ECU)", "INFO"

    def changeDrivePosition(self, position, switch_on = False, timer_s = None):
        """
        Parameter:
            position        - new position (Init, D, N, R, P, Sonderfahrprogramm, Fehler)
            switch_on       - if period has to be switched on (in case all messages switched off)
            timer_s         - switch off period again, after timer (else None)
        Info:
           set new drive position for Signal SIShift_StLghtDrvPosn
        Return:
            description, verdict
        """
        
        pos_variable = self.hil.SiShift_01__SIShift_StLghtDrvPosn__value
        period_var = self.hil.SiShift_01__period
        pos_variable.alias = "SiShift_01:SIShift_StLghtDrvPosn"
        drive_position_dict = {
            'Init': 0,
            'D': 5,
            'N': 6,
            'R': 7,
            'P': 8,
            'Sonderfahrprogramm': 12,
            'Fehler': 15
            }
        
        if position in drive_position_dict.keys():
            set_pos = drive_position_dict[position]
            description = "Setze %s auf %s (%s)"%(pos_variable.alias, set_pos, position)
            pos_variable.set(set_pos)
            if switch_on:
                description += "\nSchalte zyklisches Senden an"
                period_var.setState('an')
                if timer_s:
                    description += " für %ss" % timer_s
                    time.sleep(timer_s)
                    period_var.setState('aus')
        else:
            raise ValueError("Unkown position (%s)"%position)
        
        return description, "INFO"
    
    def setVelocity_kmph(self, velocity_kmph, switch_on = False, timer_s = None):
        """
        Parameter:
            velocity_kmph        - new velocity in km/h
            switch_on            - switch period on (in case message sending is off)
            timer_s              - switch off period again, after timer (else None)
        Info:
           set new velocity for Signal VDSO_05:VDSO_Vx3d
           Signal has unit Meter per Seconds. the input will calculated into the 
           expected input format
        Return:
            description, verdict
        """
        
        vel_variable = self.hil.VDSO_05__VDSO_Vx3d__value
        vel_variable.alias = "VDSO_05:VDSO_Vx3d"
        period_var = self.hil.VDSO_05__period
        # informations from KMatrix (Stand: 26.02.2021)
        offset = -127.7874
        skalierung = 0.0039
        
        kmph2mps = 1/3.6
                
        set_value = int(( (velocity_kmph*kmph2mps) - offset ) / skalierung)
        
        description = "Setze %s auf %s (%s km/h)"%(vel_variable.alias, set_value, velocity_kmph)
        vel_variable.set(set_value)

        if switch_on:
            description += "\nSchalte zyklisches Senden an"
            period_var.setState('an')
            if timer_s:
                description += " für %ss"%timer_s
                time.sleep(timer_s)
                period_var.setState('aus')
        
        return description, "INFO"
    
    def setVelocity_mps(self, velocity_mps, switch_on = False, timer_s = None):
        """
        Parameter:
            velocity_ms        - new velocity in m/s
            switch_on          - switch period on (in case message sending is off)
            timer_s              - switch off period again, after timer (else None)
        Info:
           set new velocity for Signal VDSO_05:VDSO_Vx3d
           Signal has unit Meter per Seconds. the input will calculated into the 
           expected input format
        Return:
            description, verdict
        """
        
        vel_variable = self.hil.VDSO_05__VDSO_Vx3d__value
        vel_variable.alias = "VDSO_05:VDSO_Vx3d"
        period_var = self.hil.VDSO_05__period
        # informations from KMatrix (Stand: 26.02.2021)
        offset = -127.7874
        skalierung = 0.0039
                       
        set_value = int(( velocity_mps - offset ) / skalierung)
        
        description = "Setze %s auf %s (%s m/s)"%(vel_variable.alias, set_value, velocity_mps)
        vel_variable.set(set_value)

        if switch_on:
            description += "\nSchalte zyklisches Senden an"
            period_var.setState('an')
            if timer_s:
                description += " für %ss"%timer_s
                time.sleep(timer_s)
                period_var.setState('aus')

        
        return description, "INFO"

    def measureZustandNHaltephase(self, daq, change_value, exp_time_ms = None, operator = "<=", duration_s = 2):
        """
        Parameter:
            daq           - daq instance to measure
            change_value  - search for value (0, 1, 2, 3, 5)
            exp_time_ms   - time where the value shall changed --> None: no time to compare
            operator      - compare measured time and expected time
            duration_s    - duration of measurement
        Info:
            measure the Waehlhebel_04:WH_Zustand_N_Haltephase_2 for duration X
            - search for changevalue and check the time
            - the measured time has to be "operator" then the expected time
        Returns:
            description, verdict

        """
        if operator not in ["==", ">=", ">", "<", "<="]:
            raise ValueError("Incorrect Operator: %s"%operator)
        if exp_time_ms > duration_s*1000:
            raise ValueError("expected time is outside measurement duration")

        meas_var = [self.hil.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value]

        daq.startMeasurement(meas_var)
        time.sleep(duration_s)
        daq_data = daq.stopMeasurement()

        signal_data = daq_data[str(meas_var[0])]
        analyse_signal_data = eval_signal.EvalSignal(signal_data)
        analyse_signal_data.clearAll()

        start_time = analyse_signal_data.getTime()
        change_time = analyse_signal_data.find("==", change_value)
        if change_time:
            if exp_time_ms:
                descr, verdict = basic_tests.compare(change_time, operator, start_time)
            else:
                descr = "Signal änderte sich nach %s auf den Wert %s"%((change_time - start_time), change_value)
                verdict = "PASSED"
        else:
            descr = "Signal ändert sich während der Messung (%ss) nicht auf den Wert %s"%(duration_s, change_value)
            verdict = "FAILED"

        return descr, verdict

    def checkBusruhe(self, daq, meas_time = 5):
        """
        Parameter:
            daw - daq instance to measure
        Info:
           check that ecu is in bus sleep mode
        Return:
            description, verdict
        """
        vars_tx = self.getAllTimestamps("TX")
        vars_rx = self.getAllTimestamps("RX")
        meas_vars_tx = []
        for m in vars_tx:
            meas_vars_tx.append(m)
        meas_vars_rx = []
        for m in vars_rx:
            meas_vars_rx.append(m)

        meas_vars = meas_vars_tx + meas_vars_rx
        daq.startMeasurement(meas_vars)
        time.sleep(meas_time)
        daq_data = daq.stopMeasurement()

        verdict = "PASSED"
        description = ""
        # initialiaze measurement data for analyse ################################
        for message in meas_vars_tx:
            message_data = daq_data[str(message)]
            analyse_message_data = eval_signal.EvalSignal(message_data)
            analyse_message_data.clearAll()

            change = analyse_message_data.findChanged()

            if change:
                verdict = "FAILED"
                description += ">> Botschaft %s sendet noch\n"%message.split('.')[-2]
            else:
                description += "Botschaft %s sendet nicht mehr\n" %message.split('.')[-2]

        for message in meas_vars_rx:
            message_data = daq_data[str(message)]
            analyse_message_data = eval_signal.EvalSignal(message_data)
            analyse_message_data.clearAll()

            change = analyse_message_data.findChanged()

            if change:
                verdict = "FAILED"
                description += ">> Botschaft %s wird noch empfangen\n"%message.split('.')[-2]
            else:
                description += "Botschaft %s wird nicht mehr empfangen\n"%message.split('.')[-2]

        
        return description, verdict