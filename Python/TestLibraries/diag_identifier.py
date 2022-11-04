#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : diag_identifier.py
# Task    : includes all relevant diagnostic identifier
# Author  : Sabine Stenger
# Date    : 18.05.2021
#
# Copyright 2012 - 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name         | Description
#------------------------------------------------------------------------------
# 1.0  | 18.05.2021 | StengerS     | initial
# 1.1  | 31.05.2021 | StengerS     | added new information
# 1.2  | 17.06.2021 | NeumannA     | add identifier for 0xF1AF
# 1.3  | 18.06.2021 | NeumannA     | add identifier for 0x0250, 0x0410, 0x0448, 0x02CF
# 1.4  | 21.06.2021 | StengerS     | add identifier for 0xF1B8, 0x0189, 0xF15B
# 1.5  | 21.06.2021 | NeumannA     | add identifier for 0xF1AB, 0xF1DF, 0xF17C
# 1.6  | 21.06.2021 | StengerS     | add identifier for 0xF16B, 0x040F
# 1.7  | 22.06.2021 | NeumannA     | add identifier for 0x0102, 0xF15A
# 1.8  | 23.06.2021 | StengerS     | add identifier for 0x02B3
# 1.9  | 25.06.2021 | NeumannA     | add identifier for 0xF1D5
# 1.10 | 28.06.2021 | NeumannA     | add identifier for 0xF18A
# 1.11 | 07.07.2021 | NeumannA     | add identifier for 0x0253 und 0x06A8
# 1.12 | 09.07.2021 | NeumannA     | add identifier for 0xFF01 und 0x045A
# 1.13 | 22.07.2021 | Mohammed     | add identifier for 0x065E
# 1.14 | 22.07.2021 | Mohammed     | add identifier for 0xF194 und 0xF195
# 1.15 | 22.07.2021 | Mohammed     | add Data length for 0x40F, 0xF1B8, 0xF189, 0xF18A und expected_response for 0xF1B6
# 1.16 | 22.07.2021 | Mohammed     | add Data length for 0250
# 1.17 | 22.07.2021 | Mohammed     | add identifier for F1A0, 0261
# 1.18 | 22.07.2021 | Mohammed     | add identifier for 0407 Expected response
# 1.19 | 16.11.2021 | Mohammed     | add identifier for F191, F187 Expected response
# 1.20 | 16.11.2021 | Mohammed     | Change identifier for F191 Expected response
# 1.21 | 19.11.2021 | Mohammed     | Add identifier for 0xFF00
# 1.22 | 23.11.2021 | Mohammed     | Add identifier for 0x0544
# 1.23 | 24.11.2021 | Julia        | rework expected_response for 0xF191, 0xF192, 0xF187, 0xF1A3, 0xF189, 0x02CA, 0x02CB, 0x09F3, 0x02CF, 0x0189, 0x040F, 0xF1AB, delete expected_response for 0x0407, rework comment for 0xF18C, 0x0407, 0xF193, 0xF194, 0xF195, 0xF1B4, 0xF1AA, 0xF1A2, 0xF1AF, 0x0448, 0x0250, 0xF15B
# 1.24 | 25.11.2021 | Julia        | rework comment for 0xF17C, 0xF18A, 0xF15B, 0xF17C, 02B3, deleted 0xF15A, 0x06A8, 0x045A, 0x065E, 0xF190, 0xF1A0
# 1.25 | 23.11.2021 | Mohammed     | Copy after Review
# 1.26 | 02.12.2021 | H. Förtsch   | added dict DIAG_SESSION_DICT for diagnose session data
# 1.27 | 18.01.2022 | Mohammed     | Diag Id aktualisiert
# 1.29 | 02.05.2022 | Mohammed     | Added Tester Present ID
#******************************************************************************
# zu jedem Update zu kontrollieren: 0xF1A3, 0xF189, 0xF1B8, (0xF1AB?)
# für folgende IDs werden Dummys vergeben: 0xF17C, 0xF18A, 0xF18C, 0xF192, 0xF193, 0xF194, 0xF195, 0xF1AF
#******************************************************************************

from functions_diag import ResponseDictionaries


# read out the ssw moduls from functions diag
rd = ResponseDictionaries()
ssw, _, _ = rd.AUTOSAR_standard_application_software_identification()
precond, _ = rd.Programming_preconditions()




identifier_dict = {
        'Active Diagnostic Session': {
                    'identifier': [0xF1, 0x86],
                    'name': 'Active Diagnostic Session',
                    'expected_response': [],  # Default Session OR Extended Session OR Programming Session OR Factory Mode
                    'exp_data_length':  1,  # Bytes
                    },

        'VW ECU Hardware Number': {
                    'identifier': [0xF1, 0x91],
                    'name': 'VW ECU Hardware Number',
                    'expected_response': [0x39, 0x35, 0x43, 0x37, 0x31, 0x33, 0x30, 0x34, 0x31, 0x20, 0x20],  # ECU Hardware Number ist Referenzhardware, in unserem Fall das Gleiche wie bei Teilenummer
                    'exp_data_length':  11,  # Bytes
                    },

        'System Supplier ECU Hardware Number': {
                    'identifier': [0xF1, 0x92],
                    'name': 'System Supplier ECU Hardware Number',
                    'expected_response': [0x22, 0x09, 0x05, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF],  # Dummywert 000000000, EGA-TNR wird bei EOL reingeschrieben 100051508,  #
                    'exp_data_length': 9,  # Bytes
                    },

        'System Supplier ECU Hardware Version Number': {
                    'identifier': [0xF1, 0x93],
                    'name': 'System Supplier ECU Hardware Version Number',
                    'expected_response': [0x48, 0x30, 0x33],  # Dummywert 000, aktuell auch 0
                    'exp_data_length': 3,  # Bytes Replace 0 to 3
                    },

        'VW ECU Hardware Version Number': {
                    'identifier': [0xF1, 0xA3],
                    'name': 'VW ECU Hardware Version Number',
                    'expected_response': [0x48, 0x30, 0x33], # aktuelle HW-Version H03,
                    'exp_data_length': 3,  # Bytes
                    },
        'VW Spare Part Number': {
                    'identifier': [0xF1, 0x87],
                    'name': 'VW Spare Part Number',
                    'expected_response': [0x39, 0x35, 0x43, 0x37, 0x31, 0x33, 0x30, 0x34, 0x31, 0x20, 0x20],  # "95C.713.042  " (Rechtslenker, Trennzeichen bleiben unberücksichtigt, Auffüllen mit Leerzeichen)
                    'exp_data_length': 11,  # Bytes
                    },
        'VW Logical Software Block Counter Of Programming Attempts': {
                    'identifier': [0x04, 0x07],
                    'name': 'VW Logical Software Block Counter Of Programming Attempts',
                    'expected_response': [0x00, 0x01, 0x00, 0x17], # wird nach jedem Update hochgezählt, kein Defaultwert/Dummywert verfügbar (EOL auf 0 gesetzt)
                    'exp_data_length': 4,  # Bytes (2 * number of SW blocks) ## Replace 512 to 2
                    },
        'ECU Serial Number': {
                    'identifier': [0xF1, 0x8C],
                    'name': 'ECU Serial Number',
                    'expected_response': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],  #
                    'exp_data_length': 20,  # Bytes
                    },
        'VW Application Software Version Number': {
                    'identifier': [0xF1, 0x89],
                    'name': 'VW Application Software Version Number',
                    'expected_response': [0x30, 0x31, 0x31, 0x32],
                    'exp_data_length': 4,  # Bytes
                    },
        'System Supplier ECU Software Number': {
                    'identifier': [0xF1, 0x94],
                    'name': 'System Supplier ECU Software Number',
                    'expected_response': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], #[0x62, 0xF1, 0x94, 0x31, 0x32, 0x33, 0x34, 0x35, 0x41, 0x42, 0x43, 0x44],   Added Response
                    'exp_data_length': 9,  # Added 9 Bytes
                    },
        'System Supplier ECU Software Version Number': {
                    'identifier': [0xF1, 0x95],
                    'name': 'System Supplier ECU Software Version Number',
                    'expected_response':[0x30, 0x36, 0x30], # wird vom Lieferant vergeben, Dummywert, wird bei EOL reingeschrieben, TNR-Index für den SW-Container (000)
                    'exp_data_length': 3,  # Added 3 Bytes
                    },
        'VW System Name Or Engine Type': {
                    'identifier': [0xF1, 0x97],
                    'name': 'VW System Name Or Engine Type',
                    'expected_response': [0x57, 0x61, 0x65, 0x68, 0x6C, 0x68, 0x65, 0x62, 0x65, 0x6C, 0x20, 0x20, 0x20],  # Systemname ist 'Waehlhebel', nicht verwendete Bytes müssen mit Leerzeichen aufgefüllt werden
                    'exp_data_length': 13,  # Bytes
                    },
        'Technical_specifications_version': {
                    'identifier': [0xF1, 0xB4],
                    'name': 'Technical_specifications_version',
                    'expected_response': [0x05, 0x08, 0x02, 0x08, 0x05, 0x08, 0x02, 0x08, 0x05, 0x08, 0x04, 0x04, 0x00,
                                          0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x02, 0x01, 0x00, 0x00, 0x00, 0x00], # 80114 5.8, 80124 2.8, 80125 5.8, 80126 2.8, 80127 5.8, 80128-3 4.4, DSDL na, DUL na, SFD na, SWaP na, ORU 2.1, PMode na, VKMS na. Nicht implementierte Lastenhefte sind mit der Hauptversion = 0 und Nebenversion = 0 auszugeben.
                    'exp_data_length': 26,  # Bytes
                    },
        'VW Workshop System Name': {
                    'identifier': [0xF1, 0xAA],
                    'name': 'VW Workshop System Name',
                    'expected_response': [0x4A, 0x30, 0x30, 0x30, 0x30],  # J0000, wird vom Kundendienst vergeben, TODO (PAG)
                    'exp_data_length': 5,  # Bytes
                    },
        'Hall-Sensor ADC1': {
                    'identifier': [0xF1, 0xF0],
                    'name': 'Hall-Sensor ADC1',
                    'exp_data_length': 2,  # Bytes
                    },
        'Hall-Sensor ADC2': {
                    'identifier': [0xF1, 0xF1],
                    'name': 'Hall-Sensor ADC2',
                    'exp_data_length': 2,  # Bytes
                    },
        'ASAM ODX File Identifier': {
                    'identifier': [0xF1, 0x9E],
                    'name': 'ASAM ODX File Identifier',
                    'expected_response': [0x45, 0x56, 0x5F, 0x47, 0x53, 0x4D, 0x45, 0x47, 0x41, 0x50, 0x4F, 0x34, 0x32, 0x36, 0x00],  # EV_GSMEGAPO426 (ASCII, terminiert mit 0x00)
                    'exp_data_length': 15,  # Bytes
                    },
        'ASAM ODX File Version': {
                    'identifier': [0xF1, 0xA2],
                    'name': 'ASAM ODX File Version',
                    'expected_response': [0x30, 0x30, 0x31, 0x30, 0x31, 0x34],  # Hauptversion ist 001 (3 Byte ASCII), Nebenversion ist aktuell 009 (3 Byte ASCII)
                    'exp_data_length': 6,  # Bytes
                    },
        'Status_ECU_Standalone-Mode': {
                    'identifier': [0xC1, 0x01],
                    'name': 'Status_ECU_Standalone-Mode',
                    'expected_response': {
                        'active': [0x01],
                        'inactive': [0x00],
                    },
                    'exp_data_length': 1,  # Bytes
                    },
        'ECU_standalone_mode_1': {
                    'identifier': [0xC1, 0x10],
                    'name': 'ECU_standalone_mode_1',
                    'expected_response': {
                        'active': [0xBD, 0xDB, 0x6B, 0x3A],
                        'inactive': [0x00, 0x00, 0x00, 0x00],
                    },
                    'exp_data_length': 4,  # Bytes
                    },
        'ECU_standalone_mode_2': {
                    'identifier': [0xC1, 0x11],
                    'name': 'ECU_standalone_mode_2',
                    'expected_response': {
                        'active': [0x42, 0x24, 0x94, 0xC5],
                        'inactive': [0x00, 0x00, 0x00, 0x00],
                    },
                    'exp_data_length': 4,  # Bytes
                    },
        'Knockout_counter': {
                    'identifier': [0x02, 0xCA],
                    'name': 'Knockout_counter',
                    'expected_response': [0x00, 0x00], # ToDo Routine zum Reset nach einem Test_Completed, Überprüfen ToDo
                    'exp_data_length': 2,  # Bytes
                    },
        'Knockout_timer': {
                    'identifier': [0x02, 0xCB],
                    'name': 'Knockout_timer',
                    'expected_response': [0x0F, 0x4F], # Default 15 min für ECU und Bus Knockout und NVEM_Kopplung aktiv, ÜberprüfenToDo
                    'exp_data_length': 2,  # Bytes
                    },
        'Knockout_test_mode': {
                    'identifier': [0x09, 0xF3],
                    'name': 'Knockout_test_mode',
                    'expected_response': [0x00], # Default 0
                    'exp_data_length': 1,  # Bytes
                    },

        'AUTOSAR_standard_application_software_identification': {
                    'identifier': [0xF1, 0xAF],
                    'name': 'AUTOSAR_standard_application_software_identification',
                    'expected_response': [0xAA, 0xBB, 0xCC], # Dummywert Matrickz, Überprüfung gemäß 80125 Anhang TODO
                    'exp_data_length': 168 #7*len(ssw),  # Bytes - SSW Modul = 7Byte --> n SSW Module
                    },
        'Integrity_validation_data_configuration_list':  {
                    'identifier': [0x02, 0x50],
                    'name': 'Integrity_validation_data_configuration_list',
                    'expected_response': [0x00, 0x00],
                    'exp_data_length': 2,  # Bytes - 2 Bytes immer + 2*n Bytes/Dataidentifier ## Added 2 byte to 4 Byte info : vom Matricz
                    },
        'Bootloader TP Blocksize': {
                    'identifier': [0x04, 0x10],
                    'name': 'Bootloader TP Blocksize',
                    'expected_response': [0x0F], # Default Wert
                    'exp_data_length': 1,  # Bytes - 0x00 - 0xFF
                    },
        'Programming_preconditions': {
                    'identifier': [0x04, 0x48],
                    'name': 'Programming_preconditions',
                    'expected_response': precond, # VORSICHT: this is a list, Abfrage implementierter Vorbedingungen ToDo
                    'exp_data_length': 12 # len(precond), #3 + len(precond),  # Bytes - 0x00 - 0xFF ### added 1 to 3 +
                    },
        'OBD_class_description': {
                    'identifier': [0x02, 0xCF],
                    'name': 'OBD_class_description',
                    'expected_response': [0x01, 0x01], # Byte 0 noch unklar, Byte 1, Bit 7 auch noch unklar
                    'exp_data_length': 2,  # Bytes - Version + OBD class
        },
        'VW_system_firmware_versions': {
                    'identifier': [0xF1, 0xB8],
                    'name': 'VW_system_firmware_versions',
                    'expected_response': [0x01, 0x30, 0x31, 0x39, 0x30], # n=1, aktuelle Bootloaderversion 0190
                    'exp_data_length': 5,  # Bytes - 1 + (n * 4) Bytes
        },
        'VW_logical_block_downgrade_protection_versions': {
                    'identifier': [0x01, 0x89],
                    'name': 'VW_logical_block_downgrade_protection_versions',
                    'expected_response': [0x00, 0x30, 0x30, 0x30, 0x31, 0x30, 0x30, 0x30, 0x31], # Lt. 80125 Init-Werte Überprüfen ToDo
                    'exp_data_length': 9,  # Bytes - 1 + n * (4 + 4) Bytes
        },
        'Fingerprint And Programming Date Of Logical Software Blocks': {
                    'identifier': [0xF1, 0x5B],
                    'name': 'Fingerprint And Programming Date Of Logical Software Blocks',
                    'expected_response': None, # Byte 0-2 wird mit data common definiert, rest im Test TestSpec_147
                    'exp_data_length': 10,  # 10 Bytes * n
        },
        'VW Logical Software Block Lock Value': {
                    'identifier': [0x04, 0x0F],
                    'name': 'VW Logical Software Block Lock Value',
                    'expected_response': [0x00, 0x01, 0x00, 0x00], # Bootloader und Applikation in der Response (logische Blöcke) enthalten
                    'exp_data_length': 4,  # n * 2 Bytes
        },
        'VW Logical Software Block Version': {
                    'identifier': [0xF1, 0xAB],
                    'name': 'VW Logical Software Block Version',
                    'expected_response': [0x30, 0x31, 0x39, 0x30, 0x30, 0x31, 0x31, 0x32],  # logische Blöcke Bootloader und Applikation, aktuell 2001, 1005 Überprüfen ToDo
                    'exp_data_length': 8,  # n * 4 Bytes, n=2
        },
        'ECU Programming Information': {
                    'identifier': [0xF1, 0xDF],
                    'name': 'ECU Programming Information',
                    'expected_response': [0x40], # 0100: Programmierbar / 0000 konsistent -> 0100 0000 -> 0x40
                    'exp_data_length': 1,  # Bytes
        },
        'System_identification': {
                    'identifier': [0xF1, 0xB6],
                    'name': 'System_identification',
                    'expected_response': [0x00, 0x53, 0x00, 0x81], # Add
                    'exp_data_length': 4,  # Bytes
        },
        'VW FAZIT Identification String': {
                    'identifier': [0xF1, 0x7C],
                    'name': 'VW FAZIT Identification String',
                    'expected_response': [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0xAA, 0x00, 0x00, 0x00, 0x00],  # Seriennummer ECU nach VW-Regeln, Dummywert
                    'exp_data_length': 23,  # Bytes
        },
        'Basic Settings Status': {
                    'identifier': [0x01, 0x02],
                    'name': 'Basic Settings Status',
                    'expected_response': [0x00], # Default Wert = 0x00 (kein RoutineControl aktiv)
                    'exp_data_length': 1,  # Bytes
        },
        'Fingerprint': {
                    'identifier': [0xF1, 0x5A],
                    'name': 'Fingerprint',
                    'expected_response': [], # Es wird nur eine positive response erwartet
                    'exp_data_length': 0,  # Bytes
        },


        'FDS_project_data': {
                    'identifier': [0xF1, 0xD5],
                    'name': 'FDS_project_data',
                    'expected_response': [0x11, 0x00, 0x00, 0x08, 0x0E, 0x20, 0x8A, 0xDA, 0x04, 0xB0, 0x69, 0x91, 0xEF, 0x3E, 0x69, 0xA6, 0x3F, 0x7F, 0xE1, 0xE5, 0x86, 0x6F, 0xFC, 0x17, 0x5E, 0x3A, 0x36, 0x48, 0x43, 0x48, 0x16, 0xED, 0xEC, 0x17, 0x50, 0x64, 0x2B, 0xC1, 0x00], # Sollte mit Matrickz geklärt werden Todo
                    'exp_data_length': 39,  # Bytes
        },
       'System Supplier Identifier': {
                    'identifier': [0xF1, 0x8A],
                    'name': 'System Supplier Identifier',
                    'expected_response': [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], # Dummywert, wird vom Lieferant vergeben
                    'exp_data_length': 9,  # Bytes, wurde mit dem Lieferant abgestimmt
       },
       'Calculate_integrity_validation_data': { # Routine!!!!
                    'identifier': {
                        'programming': [0x02, 0x53, 0x01, 0x01], # für uns nur programming relevant
                        # 'configuration': [0x02, 0x53, 0x00, 0x01], # wir konfigurieren nicht, muss mit NRC abgelehnt werden
                    },
                    'name': 'Calculate_integrity_validation_data',
                    # 'expected_response': [0x00, 0x01] + [0x01]*32, # Byte 0: Result, Byte 1: Type, Byte 2-31: Hashvalue
                    'expected_response': [0x00, 0x01, 0xef, 0x6c, 0x44, 0x4d, 0xb3, 0xa6, 0xb5, 0x28, 0x67, 0x40, 0x26, 0xd4, 0xe5, 0xad, 0xa2, 0x01, 0x4a, 0xa3, 0x25, 0x9d, 0x53, 0x32, 0xdb, 0xa2, 0xe4, 0xfb, 0x9e, 0x73, 0xde, 0xbc, 0x40, 0x64],
                    'exp_data_length': 34,  # Bytes mit Hashwert!
       },
    'Reset_healing_inhibition': { # Routine!!!!
                    'identifier': [0x06, 0xA8, 0x00],
                    'name': 'Reset_healing_inhibition',
                    'expected_response': [0x01], #
                    'exp_data_length': 1,  # Bytes
       },
    'Check Programming Preconditions': { # Routine!!!!
                    'identifier': [0x02, 0x03],
                    'name': 'Check Programming Preconditions',
                    'expected_response': [0x00, 0x00], # Wenn Liste Leer
                    'exp_data_length': 2,  # Bytes Wenn Liste Leer
       },
    'Check Programming Dependencies': { # Routine!!!!
                    'identifier': [0xFF, 0x01],
                    'name': 'Check Programming Dependencies',
                    'expected_response': [0x00], # correct result
                    'exp_data_length': 1,  # Bytes Wenn Liste Leer
       },
    'Clear_user_defined_DTC_information': { # Routine!!!!
                    'identifier': [0x04, 0x5A],
                    'name': 'Clear_user_defined_DTC_information',
                    'expected_response': [0x00, 0x00, 0x00], # correct result
                    'exp_data_length': 3,  # Bytes Wenn Liste Leer
       },
    'Check Memory': { # Routine!!!!
                    'identifier': [0x02, 0x02],
                    'name': 'Check Memory',
                    'expected_response': [0x00], # correct result
                    'exp_data_length': 1,  # Bytes Wenn Liste Leer
       },
    'Clear downgrade protection data': { # Routine!!!
                    'identifier': [0x06, 0x5E],
                    'name': 'Clear_downgrade_protection_data',
                    'expected_response': [0x00],  # correct result
                    'exp_data_length': 1,  # Bytes Wenn Liste Leer
        },
    'Diagnose Vehicle Identification Number': {  # !!!
                    'identifier': [0xF1, 0x90],
                    'name': 'Diagnose Vehicle Identification Number',
                    'expected_response': [0x00],  # correct result #
                    'exp_data_length': 17, # Bytes Wenn Liste Leer
        },
    'VW Data Set Number Or ECU Data Container Number': {  # !!!
                    'identifier': [0xF1, 0xA0],
                    'name': 'VW Data Set Number Or ECU Data Container Number',
                    'expected_response': [0x30, 0x30, 0x31, 0x30, 0x31, 0x33, 0x45, 0x47, 0x41, 0x50, 0x4F],  # correct result #Todo
                    'exp_data_length': 11,  # Bytes Wenn Liste Leer
    },
    'OBD Driving Cycle set once': {  # !!!
                    'identifier': [0x02, 0x61],
                    'name': 'OBD Driving Cycle set once',
                    'expected_response': [0x01],  # correct result #
                    'exp_data_length': 1,  # Bytes Wenn Liste Leer
    },
    'Check Erase Memory': {  # Routine!!!!
                    'identifier': [0xFF, 0x00],
                    'name': 'Check Memory',
                    'expected_response': [0x00],  # correct result
                    'exp_data_length': 1,  # Bytes Wenn Liste Leer
    },
    'Routine Verify Partial Software Checksum': {  # Routine!!!!
                'identifier': [0x05, 0x44],
                'name': 'Check Memory',
                'expected_response': [0x00],  # correct result
                'exp_data_length': 1,  # Bytes Wenn Liste Leer
    },
   'Tester Present': {
        'identifier': [0x00],
        'name': 'Check Memory',
        'expected_response': [0x7E, 0x00],
        'exp_data_length': 2,  # Bytes
    }
}

DIAG_SESSION_DICT = {
    'default': {
        'identifier': [0x10, 0x01],
        'name': 'default',
        'expected_response': [0x50, 0x01, 0x00, 0x32, 0x01, 0xF4],
        'exp_data_length': 3
    },
    'programming': {
        'identifier': [0x10, 0x02],
        'name': 'programming',
        'expected_response': [0x50, 0x02, 0x00, 0x32, 0x01, 0xF4],
        'exp_data_length': 3,  # Bytes
    },
    'extended': {
        'identifier': [0x10, 0x03],
        'name': 'extended',
        'expected_response': [0x50, 0x03, 0x00, 0x32, 0x01, 0xF4],
        'exp_data_length': 3
    },
}
