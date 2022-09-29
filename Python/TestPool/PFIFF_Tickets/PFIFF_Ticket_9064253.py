# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : PFIFF_Ticket_9064253.py
# Title   : CAN Tx Signals DS Waehlhebel cycletime
# Task    : Test of Cycle time ECU-Tx => HIL-Rx Signals of CAN Message DS_Waehlhebel
#
# Author  : Mohammed Abdul Karim
# Date    : 10.08.2022
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 10.08.2022 | Mohammed   | initial
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
import simplified_bus_tests

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    canbus = testenv.getCanBus()
    # cal = testenv.getCal()

    # Initialize variables ####################################################
    cycle_time_ms = 1000
    inhibitzeit_ms = 80
    tolerance_percent = 0.10

    # set Testcase ID #########################################################
    #testenv.setTCID(mdd=None, mdp=None, cabin=None, private=None)
    testresult.setTestcaseId("PFIFF_9064253")

    # TEST PRE CONDITIONS #####################################################
    testresult.append([" \x0aKl30 und Kl15 ein ", ""])
    testenv.startupECU()
    testresult.append([" \x0aLese Fehlerspeicher (muss leer sein)", ""])
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(canape_diag.resetEventMemory(wait=True))
    testresult.append(canape_diag.checkEventMemoryEmpty(ticket_id='FehlerId:EGA-PRM-235'))

    # TEST PROCESS ############################################################
    testresult.append(['Check the cycle time of the message DS_Waehlhebel.', 'INFO'])
    testresult.append(
        simplified_bus_tests.checkTiming(
            time_stamp_variable=hil.DS_Waehlhebel__timestamp,
            cycle_time_value_ms=cycle_time_ms,
            message_name="DS_Waehlhebel",
            tol_perc=tolerance_percent,
            operator="==")
    )
    # testresult.append(['get the value of DS_Waehlhebel__DS_Waehlhebel_ConfDTCChanged__value.', 'INFO'])
    # canbus.DS_Waehlhebel__DS_Waehlhebel_ConfDTCChanged__value.get()
    # #Anna Neumann: Inhibit zeit test aktuell noch nicht möglich
    # testresult.append(['Check the inhibit cycle time of the message DS_Waehlhebel.','INFO'])
    # testresult.append(
    #     simplified_bus_tests.checkInhibitTiming(
    #         time_stamp_variable=hil.DS_Waehlhebel__timestamp,
    #         set_variable = hil.DS_Waehlhebel__DS_Waehlhebel_ConfDTCChanged__value,
    #         set_values = [0x0, 0x1],
    #         cycle_time_value_ms = 1000,
    #         message_name="DS_Waehlhebel",
    #         inhibit_time_ms = 80,
    #         tol_perc=tolerance_percent,
    #         )
    #     )

    # TEST POST CONDITIONS ####################################################
    testenv.shutdownECU()

    # cleanup
    hil = None
    canbus = None
finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
