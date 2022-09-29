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
# 1.0  | 23.09.2021 | Mohammed   | Initial
# 1.1  | 11.11.2021 | Mohammed   | Rework
# 1.2  | 10.12.2021 | Mohammed   | Added Fehler Id
# 1.2  | 15.12.2021 | Devangbhai | Corrected current value and added busruhe
# 1.3  | 15.12.2021 | Mohammed   | Corrected NM_aktiv_Tmin and NM_Aktiv_N_Haltephase_abgelaufen value
# 1.4  | 07.02.2022 | Mohammed   | Added Strommonitoring
# 1.5  | 13.04.2022 | Devangbhai   | Corrected the evaluation method.Added checking of fast NM cycle method
# 1.6  | 22.04.2022 | Devangbhai   | Added Ticket ID
# 1.7  | 09.06.2022 | Devanhbhai | Added FCAB value check method in the test step 6



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
    testresult.setTestcaseId("TestSpec_xxx")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    testresult.append(["[.]Initialisierungsphase abgeschlossen und Waehlhebelposition D aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('D')
    testresult.append(["\xa0" + descr, verdict])

    # TEST PROCESS ############################################################
    testresult.append([" Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])


    a,b,c = func_nm.checkFcabBitwise(fcab_value=hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), bit_exp_one=[], bit_exp_zero=[1])

    checktime = 2

    t_out = checktime + t()

    nm_timestamp = hil.NM_Waehlhebel__timestamp
    start_timestamp_1 = nm_timestamp.get()

    number= 0
    description, ticket_id, verdict = func_nm.checkFcabBitwise( fcab_value=hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), bit_exp_one=[], bit_exp_zero=[1])
    dev = None
    while t_out > t():
        curr_timestamp_1 = nm_timestamp.get()
        description, ticket_id, verdict = func_nm.checkFcabBitwise(fcab_value=hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value.get(), bit_exp_one=[], bit_exp_zero=[1])
        if verdict == "PASSED":
            print "CAR Wakeup bit is set to 0 in %s s PASSED" %(curr_timestamp_1 - start_timestamp_1)
            break
        elif verdict == "FAILED":
            print "CAR Wakeup bit is set to #### in %s s" % (curr_timestamp_1 - start_timestamp_1)
            dev= False
        elif t_out > t() == False:
            curr_timestamp_1 = nm_timestamp.get()
            print "CAR Wakeup bit is set to *************** in %s s" % (curr_timestamp_1 - start_timestamp_1)
            break
    if dev is False:
        print "CAR Wakeup bit is set to *************** in %s sec" %checktime

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    # cleanup #################################################################
    hil = None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
