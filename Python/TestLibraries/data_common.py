#******************************************************************************
# -*- coding: latin-1 -*-
# File    : data_common.py
# Task    : allgemeine project daten
#
# Author  : An3Neumann
# Date    : 20.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name       | Description
#------------------------------------------------------------------------------
# 1.0  | 20.05.2021 | An3Neumann | initial
# 1.1  | 20.05.2021 | StengerS   | added s3_timeout
# 1.2  | 21.05.2021 | NeumannA   | add daq measurement path
#******************************************************************************
import os
import inspect
# computer names ##############################################################
# for computer in this list the online stubs will be used, 
# otherwise the offline stubs
CONTROL_COMPUTER_NAMES = ['DEBU-CD012']

# project infos ###############################################################
project_name = "Waehlhebel"

# DIAGNOSE ####################################################################
# parameter which should be updated for every new software
programming_date = [2022, 0x09, 05]  # date of last flashing [YY, MM, DD] - 0x22 0xF15B Test

# sw_version will be read out from iTestStudio 
# hw_version will be read out from iTestStudio 

# parameter which should not changed for every new sw
s3_timeout = 5 # time in seconds (fallback from non-default in default session)
DTCwhitelist = []
DTCactive = 0x27 # cdd: '0bxxxx1xx1' ## 0x9
DTCpassive = 0x2F # cdd: '0bxxxx1xx0' ## 0x8

# further common settings ####################################################
voltage_range = {
    'Normal': {'voltage': 13, 'DTCs': [], 'tol_perc': 2, 'hil_tol_ma': 0.03},
    'Overvoltage': {'voltage': 16.30, 'DTCs': [0x800101], 'tol_perc': 2, 'hil_tol_ma': 0.03},
    'Undervoltage': {'voltage': 5.7, 'DTCs': [0x800102], 'tol_perc': 2, 'hil_tol_ma': 0.03},
    'Overvoltage Functions': {'voltage': 18, 'DTCs': [0x800101], 'tol_perc': 2, 'hil_tol_ma': 0.03},  # Funktionseinschränkungen
    'Undervoltage Functions': {'voltage': 6, 'DTCs': [], 'tol_perc': 2, 'hil_tol_ma': 0.03},  # Funktionseinschränkungen
     }


# pathes ######################################################################
# Project Base Folder =========================================================
project_base_folder = os.path.realpath(inspect.currentframe().f_code.co_filename)   # path to this script/module
project_base_folder = os.path.dirname(project_base_folder)                          # this module's folder: <project>/Python/ProjectHandling/
project_base_folder = os.path.dirname(project_base_folder)                          # .. parent folder:     <project>/Python/
project_base_folder = os.path.dirname(project_base_folder)                          # .. parent folder:     <project>/
project_base_folder = os.path.join(project_base_folder, '')                         # ensure that we have a trailing (back)slash

# daq_measurement_data save pathes =============================================
daq_meas_path = os.path.join(project_base_folder, 'TestReports', 'Measurements')

# DATABASE PATH - SQL LITE
db_path_key = os.path.join(project_base_folder, 'Python', 'TestLibraries', 'db_lib', 'waehlhebel_database.db')

