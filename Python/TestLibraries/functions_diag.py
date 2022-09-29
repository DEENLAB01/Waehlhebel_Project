# ******************************************************************************
# -*- coding: latin1 -*-
#
# File    : functions_diag.py
# Task    : includes high-level functions for diagnosis
# Author  : Sabine Stenger
# Date    : 17.05.2021
#
# Copyright 2012 - 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 17.05.2021 | StengerS     | initial
# 1.1  | 21.05.2021 | StengerS     | added super constructor
# 1.2  | 27.05.2021 | NeumannA     | add functions to read and analyze EventMemory
# 1.3  | 31.05.2021 | StengerS     | added functions for SecurityAccess
# 1.4  | 01.06.2021 | StengerS     | added function for ECU reset
# 1.5  | 02.06.2021 | StengerS     | added function for Bit Mask
# 1.6  | 17.06.2021 | NeumannA     | add class for response dictionaries
# 1.7  | 22.06.2021 | NeumannA     | add ticket id for testresult to functions
# 1.8  | 23.06.2021 | StengerS     | added factory mode
# 1.9  | 10.09.2021 | Mohammed     | added 0x09 mode in Programming_preconditions
# 2.0  | 03.11.2021 | Devangbhai   | Added extra def for the request the seed and calculate the key
# 2.1  | 06.12.2021 | Mohammed     | Added Precondition Response
# 2.2  | 06.12.2021 | Mohammed     | Added New Precondition Response
# 2.3  | 02.12.2021 | H. Förtsch   | bugfixes
# 2.4  | 02.02.2022 | Mohammed     | IVD Module
# 2.5  | 24.02.2022 | Mohammed     | Reworked _readEventMemory method
# 2.6  | 29.06.2022 | Mohammed     | Programming_preconditions Aktualisiert
# ******************************************************************************
import os
import data_common
import time
import string

if os.getenv('COMPUTERNAME') in data_common.CONTROL_COMPUTER_NAMES:
    # "online" libs ###############################################################
    from ttk_tools.vector import canapeapi
else:
    # offline stubs ###############################################################
    import ttk_tools.vector.canapeapi_offline_stub as canapeapi
from ttk_tools.vector.canapeapi_common import DEV
from ttk_tools.vector.canapeapi_common import DRIVER
import numpy as np
from ttk_base.values_base import meta
from ttk_checks import basic_tests


def calcVersionString(byte_list):
    """ Calculates the version string from Bytes """
    return ".".join(str(i) for i in byte_list)


class CANapeDiagnosis(canapeapi.CANapeDiag):
    """
        This Class includes high-level functions for diagnosis interface
    """

    # def __init__(self, canape_asap3, db_filename, comm_channel, driver_type,
    #              module_name, request_timeout, enable_tp, restore_tp):
    def __init__(self, canape_asap3,
                 db_filename="hil.cdd",
                 comm_channel=DEV.CAN1,
                 driver_type=DRIVER.CANDELA,
                 module_name="DIAG",
                 connect=True,
                 enable_cache=None,
                 request_timeout=30000,  # ms
                 enable_tp=None,
                 restore_tp=True,
                 ):

        super(CANapeDiagnosis, self).__init__(canape_asap3, db_filename, comm_channel, driver_type,
                                              module_name, connect, enable_cache, request_timeout, enable_tp,
                                              restore_tp)

        self.HANDLE_NO_RESPONSE_FROM_ECU = []
        self.checkDTCConfig()

        self.wait_reset_event_memory_time = 1  # 1 second

        self.nrc_dict = {
            0x00: 'positiveResponse',
            0x10: 'generalReject',
            0x11: 'serviceNotSupported',
            0x12: 'subFunctionNotSupported',
            0x13: 'incorrectMessageLengthOrInvalidFormat',
            0x14: 'responseTooLong',
            0x21: 'busyRepeatReques',
            0x22: 'conditionsNotCorrect',
            0x24: 'requestSequenceError',
            0x31: 'requestOutOfRange',
            0x33: 'securityAccessDenied',
            0x35: 'invalidKey',
            0x36: 'exceedNumberOfAttempts',
            0x37: 'requiredTimeDelayNotExpired',
            0x70: 'uploadDownloadNotAccepted',
            0x71: 'transferDataSuspended',
            0x72: 'generalProgrammingFailure',
            0x73: 'wrongBlockSequenceCounter',
            0x78: 'requestCorrectlyReceived-ResponsePending',
            0x7E: 'subFunctionNotSupportedInActiveSession',
            0x7F: 'serviceNotSupportedInActiveSession',
            0x81: 'rpmTooHigh',
            0x82: 'rpmTooLow',
            0x83: 'engineIsRunning',
            0x84: 'engineIsNotRunning',
            0x85: 'engineRunTimeTooLow',
            0x86: 'temperatureTooHigh',
            0x87: 'temperatureTooLow',
            0x88: 'vehicleSpeedTooHigh',
            0x89: 'vehicleSpeedTooLow',
            0x8A: 'throttle/PedalTooHigh',
            0x8B: 'throttle/PedalTooLow',
            0x92: 'voltageTooHigh',
            0x93: 'voltageTooLow',
        }

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

    def sendDiagRequest(self, diag_request):
        """
        Parameter:
            diag_request     - a list with diagnosis job, e.g. [0x22, 0xF1, 0x97]
        Info:
           Sends a request.
        Return:
            res(ponse), description, verdict
        """
        request_str = str(HexList(diag_request))
        description = "Sende Diagnose Job - %s" % (request_str)

        try:
            res = self.sendHexRequest(diag_request)

            if isinstance(res[0], list):
                pass
            else:
                res = [res]

            res = res[0]  # make list out of convoluted list
        except:
            print "DEBUG: Fehler in sendDiagRequest()"
            res = []

        # handle None or empty list
        if not res:
            print "Keine Response erhalten: %s" % (
                request_str)
            res = []
        return res, [description, "INFO"]

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
        actual_response_str = str(HexList(diag_response))
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
        response, result_list = self.sendDiagRequest(diag_request)
        testresult.append(result_list)
        actual_response_str = str(HexList(response))

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

    def checkDiagSession(self, exp_diag_session, ticket_id=None):
        """ Checks the current diagnose session
        Parameter:
            exp_diag_session - session which shall be set, valid values are:
                                    'default'
                                    'programming'
                                    'extended'
                                    'factory_mode'
            ticket_id        - to add the ticket ID as Comment to verdict
        Return:
            testresult
        """
        exp_diag_session = 'factory_mode' if exp_diag_session == 'factory' else exp_diag_session
        session_dict = {
            'default': {
                'response_active_session': [0x62, 0xF1, 0x86, 0x01]
            },
            'programming': {
                'response_active_session': [0x62, 0xF1, 0x86, 0x02]
            },
            'extended': {
                'response_active_session': [0x62, 0xF1, 0x86, 0x03]
            },
            'factory_mode': {
                'response_active_session': [0x62, 0xF1, 0x86, 0x60],
            }
        }

        testresult = []
        diag_request = [0x22, 0xF1, 0x86]
        expected_response = session_dict[exp_diag_session]['response_active_session']
        # read out session
        testresult.append(["\xa0Überprüfen, dass aktuelle Session korrekt ist", ""])
        response, [description, verdict] = self.sendDiagRequest(diag_request)
        testresult.append([description, verdict])
        # check response:
        description, verdict = self.checkResponse(response, expected_response)
        if ticket_id:
            testresult.append([description, "[[COMMENT]] %s" % ticket_id, verdict])
        else:
            testresult.append([description, verdict])

        return testresult

    def changeAndCheckDiagSession(self, diag_session, read_active_session=True, ticket_id=None):
        """ Changes in the requested session and checks the response.
        Parameter:
            diag_session        - session which shall be set, valid values are:
                                    'default'
                                    'programming'
                                    'extended'
                                    'factory_mode'
            read_active_session - if True, active session is checked with 0x22 F1 86, otherwise not
            ticket_id           - to add the ticket ID as Comment to verdict
        Return:
            testresult
        """
        diag_session = 'factory_mode' if diag_session == 'factory' else diag_session
        session_dict = {
            'default': {
                'request_change_session': [0x10, 0x01],
            },
            'programming': {
                'request_change_session': [0x10, 0x02],
            },
            'extended': {
                'request_change_session': [0x10, 0x03],
            },
            'factory_mode': {
                'request_change_session': [0x10, 0x60],
            }
        }

        testresult = []
        diag_request = session_dict[diag_session]['request_change_session']

        # change session:
        testresult.append(["\xa0In '%s session' wechseln" % diag_session, ""])
        response, result_list = self.sendDiagRequest(diag_request)
        testresult.append(result_list)

        # check response:
        description, verdict = self.checkPositiveResponse(response, diag_request, 2)
        if ticket_id:
            testresult.append([description, "[[COMMENT]] %s" % ticket_id, verdict])
        else:
            testresult.append([description, verdict])

        if read_active_session:
            testresult.extend(self.checkDiagSession(diag_session, ticket_id=ticket_id))

        return testresult

    def requestSeed(self, pos_response=True, exp_nrc=None, special=False,ticket_id=''):
        """ Requests a seed for Security Access.
        Parameter:
           pos_response - (optional, default: True)
                              True:  a positive response is expected
                              False: a negative response is expected
           exp_nrc      - expected negative response code
           special      - (optional, default: False)
        Return:
            seed, testresult
        """
        if special:
            request = [0x27, 0x11] #### Todo
        else:
            request = [0x27, 0x61]

        temp_str = ''
        if ticket_id:
            temp_str = "[[COMMENT]] %s" % ticket_id
        testresult = []
        testresult.append(["\xa0Seed anfragen: {}".format(HexList(request)), "INFO"])
        response, result_list = self.sendDiagRequest(request)
        testresult.append(result_list)

        if pos_response:
            testresult.append(self.checkPositiveResponse(response, request, job_length=2))
            seed = response[2:]
            if len(seed) == 4:
                testresult.append(["Seed: {}".format(HexList(seed)), "INFO"])
            else:
                testresult.append(["Invalid seed: {}".format(HexList(seed)),temp_str+'%s'%(ticket_id), "FAILED"])
        else:
            testresult.append(self.checkNegativeResponse(response, request, exp_nrc))
            seed = []

        return seed, testresult

    @staticmethod
    def calculateKey(seed):
        """ Calculates the key for Security Access.
        Parameter:
            seed - 4 Byte, e.g. [0x34, 0x7A, 0x26, 0xF4]
        Return:
            key, testresult
        """
        testresult = []
        seed = seed
        compare_xor = [0xFF, 0xFF, 0xFF, 0xFF]
        key = list(a ^ b for a, b in zip(seed, compare_xor))

        testresult.append(["\xa0 Key berechnen: %s" % str(HexList(key)), "INFO"])
        return key, testresult

    def sendKey(self, key, pos_response=True, exp_nrc=None, special=False,ticket_id=''):
        """ Sends key for Security Access.
        Parameter:
            key          - key, 4 Byte, e.g. [0x67, 0xBA, 0x8C, 0x12]
            pos_response - if True a positive response is expected, otherwise a negative
            exp_nrc      - expected negative response code
            special      - (optional, default: False)
        Return:
            testresult
        """
        if special:
            request = [0x27, 0x12] + key
        else:
            request = [0x27, 0x62] + key

        testresult = []
        response, result_list = self.sendDiagRequest(request)
        testresult.append(result_list)

        if pos_response:
            testresult.append(self.checkPositiveResponse(response, request, job_length=2))
        else:
            testresult.append(self.checkNegativeResponse(response, request, exp_nrc))

        return testresult

    def performSecurityAccess(self):
        """ Performs a complete Security Access.
        Return:
            seed, key, testresult
        """
        testresult = []

        seed, result = self.requestSeed()
        testresult.extend(result)

        key, result = self.calculateKey(seed)
        testresult.append(result)

        result = self.sendKey(key)
        testresult.extend(result)

        return seed, key, testresult
    
    def d2b(self, n):
        bStr = ''
        if n < 0: raise ValueError, "must be a positive integer"
        if n == 0: return '0'
        while n > 0:
            bStr = str(n % 2) + bStr
            n = n >> 1    
        return bStr


    def h2b(self, hex):
        return self.d2b(long(hex, 16))
    
    def bintohex(self, s):
        return ''.join([ "%x" % string.atol(bin, 2) for bin in s.split() ])
    
#-------------------------------------------------------------------------------
# #    Rotate counter-clockwise [RSL]
    def ROL (self, key):
        binary_key = self.h2b(key)
        l = len(binary_key)
        if l <= 31:
            carry = 0
        else:                                       
            carry = 1
            
        a = str(binary_key) + str(carry)
        if carry == 1:
            b = a[1:l + 1]
        else:
            b = a[0:l + 1]
        c = self.bintohex(b)
        
        return c

#-------------------------------------------------------------------------------
    def Carry(self, key):
        binary_key = self.h2b(key)
        l = len(binary_key)
        if l <= 31:
            carry = 0
        else:
            carry = 1
        return carry
#-------------------------------------------------------------------------------
    def SecurityAccessProg(self):
        """ checks security access using the Algorithm
        Return:
            seed, key, testresult
        """
        testresult = []

        seed, result = self.requestSeed(special=True)
        testresult.extend(result)
        key = seed
        bytes = ''.join([str(hex(c)) for c in seed])
        key ="0x" + bytes.replace('0x', '')

        if result[-1][-1] != 'FAILED':
            factor = '0x0F462D91' # 0x2C51A427 AC13491B 0A221289
            for i in range(7):    # from 0--6
                carry = self.Carry(key)
                key = self.ROL(key)
                if carry != 0:
                    key = hex(long(key, 16) ^ long(factor, 16))

            if len(key) > 10:
                key = key[2:10]

            testresult.append(["\xa0 Key: %s" % (key), "INFO"])
            key = [int(('0x' + key[0:2]), 16),
                   int(('0x' + key[2:4]), 16),
                   int(('0x' + key[4:6]), 16),
                   int(('0x' + key[6:8]), 16)
                   ]
            result = self.sendKey(key,special=True)
            testresult.extend(result)
        else:
            testresult.append(["invalid Seed: Security Access cannot be performed" , "FAILED"])
        #
 #seed, key,
        return testresult


    def _readEventMemory(self):
        '''Executes Diagnose Service 19 02 2F'''
        # Ausführen des Diagnoseservices mit den oben gesetzten Parametern
        try:
            res = self.sendHexRequest([0x19, 0x02, 0x2F]) #### changed 0x09 to 0x2F
        except:
            print "DEBUG: Handled exception in _readErrorMemory()"
            res = self.HANDLE_NO_RESPONSE_FROM_ECU
        return res

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

    def resetEventMemory(self, wait=False, ticket_id=None):
        """
            wait                     - if wait = True, after reset a defined time will wait
            ticket_id                - to add the ticket ID as Comment to verdict
        """
        try:
            res = self.sendHexRequest([0x14, 0xFF, 0xFF, 0xFF])
        except:
            print "DEBUG: Handled exception in resetEventMemory()"
            res = self.HANDLE_NO_RESPONSE_FROM_ECU  # defined result

        print "Clear error memory, Response: %s" % (res)
        # handle None or empty list
        # if returned by CANape-API function -> is that possible?
        if not res:
            descr = "Keine Antwort auf die Diagnoseanfrage"
            verdict = "FAILED"
        else:
            if res == [[0x54]]:
                descr = "Fehlerspeicher löschen war erfolgreich"
                verdict = "PASSED"
            else:
                descr = "Unerwartete Antwort auf Diagnosejob (%s)" % res
                verdict = "FAILED"

        if wait:
            descr += "\nWarte %sms" % (self.wait_reset_event_memory_time * 1000)
            time.sleep(self.wait_reset_event_memory_time)

        if ticket_id:
            return [descr, "[[COMMENT]] %s" % ticket_id, verdict]
        else:
            return [descr, verdict]

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
        diag_response = self._readEventMemory()
        err_msg_list = []
        description = None  # initial

        if diag_response is None or diag_response == []:
            description = "No error memory response, can't check DTC",
            verdict = "FAILED"
        else:  # regular case
            dtc_list = self.getEventMemoryList(diag_response)
            if dtc_list is None:  # NOTE: empty list is not an error here
                description = "No error memory response, can't check DTC",
                verdict = "FAILED"
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

    def performEcuReset(self, reset_type, pos_response=True, exp_nrc=None):
        """
        Parameter:
           reset_type    - type of ECU reset ('HardReset' or 'KeyOffOnReset')
           pos_response  - if True a positive response is expected, otherwise a negative
           exp_nrc       - expected negative response code
        Info:
           Perform Ecu Reset (0x11).
           Perform Ecu Reset (0x11).
        Return:
            testresult
        """
        testresult = []

        sub_function = {'HardReset': 0x01,
                        'KeyOffOnReset': 0x02}
        request = [0x11] + [sub_function[reset_type]]

        testresult.append(["\xa0ECU Reset - %s: %s" % (reset_type, str(HexList(request))), "INFO"])
        res, [descr, verdict] = self.sendDiagRequest(request)
        testresult.append([descr, verdict])

        if pos_response:
            testresult.append(self.checkPositiveResponse(res, request, job_length=2))
        else:
            testresult.append(self.checkNegativeResponse(res, request, exp_nrc))

        return testresult

    def analysisExtendedDataRecordResponse(self, response, exp_value, parameter_name, ticket_id=' '):
        """
        Parameter:
           reset_type    - type of ECU reset ('HardReset' or 'KeyOffOnReset')
           pos_response  - if True a positive response is expected, otherwise a negative
           exp_nrc       - expected negative response code Occurrence counter
        Info:
           Perform Ecu Reset (0x11).
        Return:
            testresult
        """
        temp_str = ''
        if ticket_id:
            temp_str = '[[COMMENT]]'
        testresult = []
        parameter_name = parameter_name
        parameter_name_list = {'StatusOfDTC': 5,
                               'DTCExtendedDataRecordNumber': 6,
                               'DTCPriority': 7,
                               'OCC': 8,
                               'Aging_counter': 7,
                               'Km-Mileage': 8,
                               'Timestamp': 13,
                               'Trip_counter': 7,
                               'Healing_counter': 8,
                               'Confirmation_Threshold': 9}

        exp_value = exp_value
        if response:
            EDRN_Val = response[parameter_name_list['DTCExtendedDataRecordNumber']]
            expected_EDRN_resp_length = [9, 17, 10]
            if EDRN_Val == 2:
                if len(response) >= expected_EDRN_resp_length[EDRN_Val-1]:
                    pass
                    # testresult.append(["Response length is Not correct", '', 'FAILED']) ### todo
                else:
                    testresult.append(["Response length is Not correct \n "
                                       "Actual length = %s\n  "
                                       "Expected length= %s" %(
                                        len(response), expected_EDRN_resp_length[EDRN_Val - 1]),
                                       temp_str+'%s'%(ticket_id), 'FAILED'])
                for index, par_name in enumerate(parameter_name):
                    if len(response) >= expected_EDRN_resp_length[EDRN_Val - 1]:
                        if 'Km-Mileage' == par_name:
                            actl_rep = (response[8] << 16) | (response[9] << 8) | response[10]
                            if actl_rep == exp_value[index]:
                                testresult.append(["%s Actual Value = %s\n %s Expected Value= %s" % (
                                parameter_name[index], exp_value[index], parameter_name[index], exp_value[index]), '',
                                                   'PASSED'])
                            else:
                                testresult.append(["%s Actual Value = %s\n %s Expected Value= %s" % (
                                parameter_name[index], response[parameter_name_list[parameter_name[index]]],
                                parameter_name[index], exp_value[index]), '', 'FAILED'])

                        elif 'Timestamp' == par_name:
                            actl_rep = (response[12] << 64) | (response[13] << 32) | response[14] << 16 | (
                                         response[15] << 8) | response[16]
                            # if actl_rep == exp_value[index]:
                            #     testresult.append(["%s Actual Value = %s\n %s Expected Value= %s" % (
                            #     parameter_name[index], exp_value[index], parameter_name[index], exp_value[index]), '',
                            #                        'PASSED'])
                            # else:
                            #     testresult.append(["%s Actual Value = %s\n %s Expected Value= %s" % (
                            #     parameter_name[index], response[parameter_name_list[parameter_name[index]]],
                            #     parameter_name[index], exp_value[index]), '', 'FAILED'])
                        else:
                            if response[parameter_name_list[parameter_name[index]]] == exp_value[index]:
                                testresult.append(["%s\n Actual Value = %s\n Expected Value= %s" % (
                                parameter_name[index], exp_value[index], exp_value[index]), '',
                                                   'PASSED'])
                            else:
                                testresult.append(["%s\n Actual Value = %s\n Expected Value= %s" % (
                                parameter_name[index], response[parameter_name_list[parameter_name[index]]],
                                exp_value[index]), '', 'FAILED'])

                    else:
                        if 'Aging_counter' == par_name:
                            if response[parameter_name_list[parameter_name[index]]] == exp_value[index]:
                                testresult.append(["%s\n Actual Value = %s\n %s Expected Value= %s" % (
                                    parameter_name[index], exp_value[index], parameter_name[index], exp_value[index]),
                                                   '',
                                                   'PASSED'])
                            else:
                                testresult.append(["%s\n Actual Value = %s\n Expected Value= %s" % (
                                    parameter_name[index], response[parameter_name_list[parameter_name[index]]],
                                     exp_value[index]), temp_str+'%s'%(ticket_id), 'FAILED'])
                        else:
                            #testresult.append(["Response length is Not correct", '', 'FAILED'])
                            testresult.append(["%s\n Actual Value = [] \n Expected Value= %s" % (
                            parameter_name[index], exp_value[index]), temp_str+'%s'%(ticket_id), 'FAILED'])
            else:
                if len(response) >= expected_EDRN_resp_length[EDRN_Val - 1]:
                    for i in range(len(parameter_name)):
                        #testresult.append(["DTCExtendedDataRecordNumber is %s" % (EDRN_Val), '', 'INFO'])
                        if response[parameter_name_list[parameter_name[i]]] == exp_value[i]:
                            testresult.append(["%s\n Actual Value = %s\n Expected Value= %s" % (
                            parameter_name[i], exp_value[i], exp_value[i]), '', 'PASSED'])
                        else:
                            testresult.append(["%s\n Actual Value = %s\n Expected Value= %s" % (
                            parameter_name[i], response[parameter_name_list[parameter_name[i]]],
                            exp_value[i]),   temp_str+'%s'%(ticket_id), 'FAILED'])
                else:
                    testresult.append(["Response length is Not correct", '', 'FAILED'])
        else:
            testresult.append(["Response is Empty", '', 'FAILED'])

        return testresult

    def check_programming_precondition(self, exp_content):

        pre_cond_list = {
            '': 'List ist 00',
            0x05: 'Fahrzeuggeschwindigkeit ist nicht Null',
            0x0A: 'Versorgungsspannung zu niedrig',
            0x0B: 'Temperatur zu hoch',
            0x0C: 'Temperatur zu niedrig',
            0x81: 'Sperrzeit für Programmierung ist aktiv',
            0x83: 'Maximale Anzahl der Programmierungen erreicht',
            0x95: 'Elektrische Fahrbereitschaft ist nicht aus',
            0xA5: 'Feststellbremse nicht geschlossen',
            0xA7: 'Sicherer Zustand für Updateprogrammierung nicht hergestellt',
            0x9A: 'Versorgungsspannung zu hoch'
        }
        testresult = []
        diag_request = [0x31, 0x01, 0x02, 0x03]
        response, result_list = self.sendDiagRequest(diag_request)
        testresult.append(result_list)
        if exp_content:
            testresult.extend(basic_tests.checkStatus(meta(len(response[4:]),
                                                           alias="Länge des Inhalts"),
                                                      len(exp_content),
                                                      descr="{} Element".format(len(exp_content))))
            if len(response[4:]) == len(exp_content):
                testresult.extend(basic_tests.compare(meta(response[4:],
                                                           alias="Inhalt"),
                                                      "==",
                                                      meta(exp_content,
                                                           alias="Erwarteter Inhalt"),
                                                      descr="Inhalt der Response"))
            elif  len(response[4:]) == 0:
                testresult.extend(basic_tests.compare([0],
                                                      "==",
                                                      meta(exp_content,
                                                           alias="Erwarteter Inhalt"),
                                                      descr="Inhalt der Response"))

            else:
                testresult.append(['Inhalt der Response kann nicht verglichen werden.', 'FAILED'])
        else:
            testresult.extend(basic_tests.checkStatus(meta(len(response[4:]),
                                                           alias="Länge des Inhalts"),
                                                      0,
                                                      descr="Kein Inhalt - Liste leer"))
        return testresult
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


class ResponseDictionaries(object):

    def AUTOSAR_standard_application_software_identification(self):
        waehlhebel_ssw_moduls_version = {
            # ssw modul id : ssw version, vendor id
            0x0B00: [0x130000, 0x001E],  # NM-High (CAN)
            0x1A00: [0x050101, 0x001E],  # XCP Service Implementation
            0x1F00: [0x060101, 0x001E],  # Kypto Library
            0xCF00: [0x010301, 0x001E],  # E2E Protection Wrapper
            0xD400: [0x030000, 0x001E],  # XCP Transport Layer on CAN
            0xD700: [0x040101, 0x001E],  # CRY-SW (Crypto-Algorithmen in Software)
            0xDD00: [0x040001, 0x001E],  # Knockout Module
            0x000A: [0x100002, 0x001E],  # ECU State Manager
            0x000C: [0x110000, 0x001E],  # Comunication Manager
            0x000F: [0x210001, 0x001E],  # Development Error Tracer
            0x001F: [0x110000, 0x001E],  # CAN NM
            0x0023: [0x050100, 0x001E],  # CAN TP
            0x002A: [0x160002, 0x001E],  # BswModeManager
            0x0032: [0x180001, 0x001E],  # AUTOSAR Com
            0x0033: [0x160004, 0x001E],  # PDU Router
            0x0034: [0x100502, 0x001E],  # IPDU Multiplexer
            0x0035: [0x120501, 0x001E],  # DCM
            0x0036: [0x180101, 0x001E],  # DEM
            0x003C: [0x110100, 0x001E],  # CAN Interface
            0x0050: [0x010101, 0x001E],  # CAN Driver
            0x006E: [0x040301, 0x001E],  # CSM
            0x008C: [0x070003, 0x001E],  # CAN State Manager
            0x00CF: [0x020200, 0x001E],  # E2E Library
            0x0000: [0x030402, 0x004B],  # IVD Module
        }

        # aus Q-LAH 80125 - Anhang A Querschnittslastenheft LAH.000.900.N
        all_ssw_modul_id = {
            0x0000: "IVD Module",
            0x0100: "BAP",
            0x0200: "UDS",
            0x0300: "DEH",
            0x0700: "ISO-TP",
            0x0B00: "NM-High (CAN)",
            0x1200: "KS (Komponentenschutz)",
            0x1500: "SDS für UDS",
            0x1600: "BLF CAN",
            0x1700: "BLF FlexRay",
            0x1A00: "XCP Service Implementation",
            0x1F00: "Kypto Library",
            0x2000: "Dekompressionsmodul",
            0x2200: "WaP - Software als Produkt",
            0xCC00: "E2E Library Profile 2",
            0xCD00: "E2E Library Profile XOR",
            0xCE00: "E2E Library Profile XOR CRC8",
            0xCF00: "E2E Protection Wrapper",
            0xD300: "XCP Transport Layer on FlexRay",
            0xD400: "XCP Transport Layer on CAN",
            0xD500: "FoD-Master (Function on Demand)",
            0xD600: "FoD-Slave (Function on Demand)",
            0xD700: "CRY-SW (Crypto-Algorithmen in Software)",
            0xD800: "CRY-HW (Crypto-Algorithmen in Hardware, z.B. SHE oder HSM mit SHE)",
            0xD900: "SFD (Schutz der Fahrzeugdiagnose)",
            0xDA00: "VKMS (Vehicle Key Management System)",
            0xDB00: "SOKFM (Sichere OnBoard Kommunikation Freshness Manager)",
            0xDC00: "VNSM (Vehicle Network State Manager)",
            0xDD00: "Knockout Module",
            0xDE00: "Immobilizer Module",
            0xDF00: "Ethernet Testability Services",
            0x000A: "ECU State Manager",
            0x000C: "Comunication Manager",
            0x000F: "Development Error Tracer",
            0x001D: "Generic NM",
            0x001F: "CAN NM",
            0x0020: "FlexRay NM",
            0x0023: "CAN TP",
            0x0024: "FlexRay TP",
            0x002A: "BswModeManager",
            0x0032: "AUTOSAR Com",
            0x0033: "PDU Router",
            0x0034: "IPDU Multiplexer",
            0x0035: "DCM",
            0x0036: "DEM",
            0x003C: "CAN Interface",
            0x003D: "FR Interface",
            0x003E: "LIN Interface",
            0x0050: "CAN Driver",
            0x0051: "FlexRay Driver",
            0x0052: "LIN Driver",
            0x006E: "CSM",
            0x008C: "CAN State Manager",
            0x008D: "LIN State Manager",
            0x008E: "FlexRay State Manager",
            0x00CF: "E2E Library",
        }

        # https://www.autosar.org/about/vendorid/
        vendor_id = {
            0x0000: "not defined",
            0x001E: "Vector",
            0x004B: "ITK",
        }

        return waehlhebel_ssw_moduls_version, all_ssw_modul_id, vendor_id

    def Programming_preconditions(self):
        exp_preconditions = [0x0A, 0x0A, 0x9A, 0x0C, 0x0B, 0x83, 0x81, 0x05, 0x95, 0xA5, 0xA7]

        all_preconditions = {
            0x05: "Fahrzeuggeschwindigkeit ist nicht Null",
            #0x09: "Zuendung (Klemme 15) ist nicht eingeschaltet",
            0x0A: "Versorgungsspannung zu niedrig",
            0x0B: "Temperatur zu hoch",
            0x0C: "Temperatur zu niedrig",
            0x81: "Sperrzeit für Programmierung ist aktiv",
            0x83: "Maximale Anzahl der Programmierungen erreicht",
            #0x8B: "Steuergeraet defekt im Ereignisspeicher eingetragen",
            0x95: "Elektrische Fahrbereitschaft ist nicht aus",
            0xA5: "Feststellbremse nicht geschlossen",
            #0xA6: "KL30 zu niedrig",
            0xA7: "Sicherer Zustand für Updateprogrammierung nicht hergestellt",
            0x9A: "Versorgungsspannung zu hoch",
        }

        return exp_preconditions, all_preconditions
