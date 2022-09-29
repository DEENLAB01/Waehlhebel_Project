#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : functions_hil.py
# Task    : functions for hil environment
#
# Author  : A.Neumann
# Date    : 30.06.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date        | Name       | Description
#------------------------------------------------------------------------------
# 1.1   | 30.06.2021 | NeumannA   | initial
# 1.2   | 30.06.2022 | Mohammed   | Added performDEM3OYC method
#******************************************************************************
import time


class FunctionsHil(object):
    def __init__(self,testenv, hil = None):
        """ Constructor

            Parameters:
                testenv  - test environment object

            Return:
                -
        """
        self.testenv = testenv
        if hil:
            self.hil = hil
        else:
            self.hil = self.testenv.getHil()

        self.failure_types = ['BREAK', 'SHORT_TO_GROUND', 'SHORT_TO_UBAT']

        self.failurelocations = {
                'BREAK': {
                            'error_type': 1,
                            'second_last_number': None
                            },
                'SHORT_TO_GROUND': {
                            'error_type': 2,
                            'second_last_number': 102 # FIU Card 1 - Load 2 (KL31)
                            },
                'SHORT_TO_UBAT': {
                            'error_type': 2,
                            'second_last_number': 101 # FIU Card 1 - Load 1 (KL30)
                            },
                'VALVE_SHORTED': {
                            'error_type': 3,
                            'second_last_number': None
                            }
                }

        self.can_failure_locations = {
            'CAN1 HIGH': {"BREAK": 1, "EI1": 3},  # FIU CAN_FR - Load 1
            'CAN1 LOW': {"BREAK": 2, "EI1": 4},  # FIU CAN_FR - Load 2
        }
        self.can_no_error = 0

    #**************************************************************************
    # function: setFiuFailureHil
    #**************************************************************************
    def setCANFiuFailureHil(self, can, failure_type):
        """ set failure on HIL via FIU Card CAN_FR

            Parameters:
                can                 - low or high
                failure_type        - 'BREAK', 'SHORT_TO_GROUND', 'SHORT_TO_UBAT', 'VALVE_SHORTED'
                report              - Output to testreport will be created
                                      (should be always True - only in exeptional cases to False)
            Info:
                -
            Return:
                description, verdict
        """

        if can.upper() not in ['HIGH', 'LOW']:
            raise NameError("Wrong CAN selected - Choose 'Low' or 'High'")

        failure_location = "CAN1 "+can.upper()

        if failure_type in self.failure_types:
            if failure_location in self.can_failure_locations.keys():
                description = "Setze HIL Failure %s an %s" % (failure_type, failure_location)
                failure = self.failurelocations[failure_type]

                #set error type
                description += "\nSetze Error Type: %s (%s)"%(failure["error_type"], failure_type)
                self.hil.error_type.set(failure['error_type'])

                #set EI1 if failure is Ubat/Ground
                if failure['second_last_number']: # for EI1
                    description += "\nSetze Second Last Number: %s (EI1)" % (failure['second_last_number'])
                    self.hil.load_number_select.set(failure['second_last_number'])
                    can_number = self.can_failure_locations[failure_location]['EI1']
                else:
                    can_number = self.can_failure_locations[failure_location][failure_type]
                #set can
                description += "\nSetze CAN: %s (%s)" % (can_number, failure_location)
                self.hil.bus_physical_error.set(can_number)
                time.sleep(0.1)

                return description,"INFO"

            else:
                raise NameError('Unknown Failurelocation!')
        else:
            raise NameError('Unknown FailureType!')


    #**************************************************************************
    # function: resetFiuFailureHil
    #**************************************************************************
    def resetCANFiuFailureHil(self):
        """ reset failure on HIL via FIU Card CAN_FR

            Parameters:
                -
            Info:
                no parameter necessary - reset failure on HIL
                set location and type to zero

            Return:
                description, verdict
        """

        # Parameter 2 - variable for location
        no_error = self.can_no_error

        #reset Failure CAN
        self.hil.bus_physical_error.set(no_error)

        #reset Failure location - last number
        self.hil.load_number_select.set(no_error)

        #reset Failure Type
        self.hil.error_type.set(no_error)
        time.sleep(0.1)

        description = "Reset HIL Failure"
        return description,"INFO"


    def setVoltage(self, set_voltage, step_size=None, wait_time_s=None):
        """

        Args:
            set_voltage:    end_voltage
            step_size:      stepsize of voltage setting, if None voltage will set directly
            wait_time:      wait time between steps in seconds

        Returns:

        """
        voltage_var = self.hil.vbat_cl30__V
        if step_size:
            current_voltage = voltage_var.get()
            if set_voltage > current_voltage: # increase voltage gradually
                descr = "Schrittweise Erhöhung der Spannung von %sV auf %sV in %sV Schritten "%(current_voltage, set_voltage, step_size)
                if wait_time_s: descr = descr + "(Wartezeit zwischen Schritten %ss)"%wait_time_s
                while True:
                    if (set_voltage-current_voltage) > step_size:
                        current_voltage += step_size
                        voltage_var.set(current_voltage)
                        if wait_time_s:
                            time.sleep(wait_time_s)
                    else:
                        current_voltage = set_voltage
                        voltage_var.set(current_voltage)
                        break

            elif set_voltage < current_voltage: # decrease voltage gradually
                descr = "Schrittweises Absenken der Spannung von %sV auf %sV in %sV Schritten " % (
                current_voltage, set_voltage, step_size)
                if wait_time_s: descr = descr + "(Wartezeit zwischen Schritten %ss)" % wait_time_s
                while True:
                    if (current_voltage - set_voltage) > step_size:
                        current_voltage -= step_size
                        voltage_var.set(current_voltage)
                        if wait_time_s:
                            time.sleep(wait_time_s)
                    else:
                        current_voltage = set_voltage
                        voltage_var.set(current_voltage)
                        break
            else:
                descr = "Aktuelle Spannung ist bereits wie gewünscht"
        else:
            descr = "Setze Spannung auf %sV"%set_voltage
            voltage_var.set(set_voltage)

        return descr, "INFO"

    def perform3OYC(self):
        """ make a 3 operation cycle

            Parameters:
                -
            Info:
                no parameter necessary - set kl.15 on and off with delay
                for 3 time.

            Return:
                nothing
        """
        kl_15_switch = self.hil.cl15_on__
        for i in range(4):
            kl_15_switch.set(0)
            time.sleep(2)
            kl_15_switch.set(1)
            time.sleep(2)  # atleast one cycle time

    def performDEM3OYC(self):
        """ make a 3 operation cycle

            Parameters:
                -
            Info:
                no parameter necessary - set Bus on and off with delay
                for 3 time.

            Return:
                nothing
        """
        kl_15_switch = self.hil.ClampControl_01__KST_KL_15__value
        TX_Switch = self.hil.can0_HIL__HIL_TX__enable
        #self.hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(1)
        for i in range(2):
            kl_15_switch.set(0)
            TX_Switch.set(0)
            time.sleep(30)
            kl_15_switch.set(1)
            TX_Switch.set(1)
            time.sleep(1)  # atleast one cycle time
            self.hil.ORU_Control_A_01__ORU_Control_A_01_CRC__value.set(1)
            time.sleep(.500)

