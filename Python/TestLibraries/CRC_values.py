#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : CRC_values.py
# Task    : includes crc values with the BZ number
# Author  : Devangbhai Patel
# Date    : 06.10.2022
#
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name         | Description
#------------------------------------------------------------------------------
# 1.0  | 06.10.2022 | Devangbhai     | initial


"""
The Following Dict works only with the following condition
1.OTAMC_D_01 VehicleProtectedEnvironment = 0
2.ORU_Control_A_01 OnlineRemoteUpdateControlA = 4
3. ORU_Control_D_01 OnlineRemoteUpdateControlD= 4
NOTE: --> with other values of the signal, CRC calculation will not work

4.  SiShift_01:SIShift_StLghtDrvPosn = 8 (P) and SiShift_01:SIShift_FlgStrtNeutHldPha__value = 0
NOTE: --> With other gear values, activated N-HaltPhase signal and other values of the signal CRC calculation won't work
"""
crc_dict = {'ORU_Control_A_01': {'0': 119,
                                 '1': 168,
                                 '2': 96,
                                 '3': 217,
                                 '4': 33,
                                 '5': 151,
                                 '6': 243,
                                 '7': 52,
                                 '8': 19,
                                 '9': 36,
                                 '10': 82,
                                 '11': 206,
                                 '12': 74,
                                 '13': 238,
                                 '14': 191,
                                 '15': 107},
            'ORU_Control_D_01': {'0': 228,
                                 '1': 27,
                                 '2': 216,
                                 '3': 57,
                                 '4': 67,
                                 '5': 109,
                                 '6': 211,
                                 '7': 60,
                                 '8': 134,
                                 '9': 85,
                                 '10': 141,
                                 '11': 46,
                                 '12': 218,
                                 '13': 156,
                                 '14': 131,
                                 '15': 221},
            'OTAMC_D_01': {'0': 192,
                           '1': 94,
                           '2': 28,
                           '3': 246,
                           '4': 37,
                           '5': 131,
                           '6': 225,
                           '7': 79,
                           '8': 36,
                           '9': 250,
                           '10': 76,
                           '11': 64,
                           '12': 234,
                           '13': 40,
                           '14': 21,
                           '15': 63},
            'SiShift_01': {'0': 137,
                           '1': 206,
                           '2': 159,
                           '3': 21,
                           '4': 170,
                           '5': 49,
                           '6': 123,
                           '7': 113,
                           '8': 163,
                           '9': 166,
                           '10': 234,
                           '11': 10,
                           '12': 211,
                           '13': 59,
                           '14': 183,
                           '15': 196}
            }
