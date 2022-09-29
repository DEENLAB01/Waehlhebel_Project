# ******************************************************************************
# -*- coding: latin1 -*-
# File    : PowerOn_73.py
# Title   : NM Power On
# Task    : A minimal "PowerOn!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name     | Description
# ------------------------------------------------------------------------------
# 1.0  | 04.01.2021 | Mohammed     | initial
# 1.1  | 13.04.2021 | Mohammed     | added Busruhe Signals
# 1.2  | 19.05.2021 | NeumannA     | update for testspec
# 1.3  | 30.06.2021 | NeumannA     | evaluation of FCAB Value updated
# 1.4  | 06.07.2021 | Mohammed     | corrected NM_Waehlhebel_Wakeup_V12 signal value
# 1.5  | 04.08.2021 | Mohammed     | Replace aktiv_Tmin 1 to 0 und CBV_CRI 0 to 1
# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_nm

import time
import functions_gearselection

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()
    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    test_variables = {
        "CBV_AWB": hil.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value,
        "CBV_CRI": hil.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value,
        "FCAB": hil.NM_Waehlhebel__NM_Waehlhebel_FCAB__value,
        "SNI_10": hil.NM_Waehlhebel__NM_Waehlhebel_SNI_10__value,
        "NM_State": hil.NM_Waehlhebel__NM_Waehlhebel_NM_State__value,
        "UDS_CC": hil.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value,
        "Wakeup_V12": hil.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value,
        "aktiv_KL15": hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value,
        "aktiv_Diag": hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
        "aktiv_Tmin": hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value,
        "Haltephase_abgelaufen": hil.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value
    }

    test_loops = {
        1: {
            'wait': 0.4,
            "CBV_AWB": [0, 'Passiver Wakeup'], "CBV_CRI": [1, 'NM_mit_Clusteranforderungen'],
            "FCAB": [[1], 'CarWakeUp'], "SNI_10": [83, 'Waehlhebel_SNI'],
            "NM_State": [1, 'NM_RM_aus_BSM'], "UDS_CC": [0, 'Inaktiv'],
            "Wakeup_V12": [1, 'Bus_Wakeup'], "aktiv_KL15": [1, 'KL15_EIN'],
            "aktiv_Diag": [0, 'Inaktiv'], "aktiv_Tmin": [1, 'Mindestaktivzeit'],
            "Haltephase_abgelaufen": [0, 'Inaktiv']
        },
        2: {
            'wait': 3.0,
            "CBV_AWB": [0, 'Passiver Wakeup'], "CBV_CRI": [1, 'NM_mit_Clusteranforderungen'],
            "FCAB": [[1], 'CarWakeUp'], "SNI_10": [83, 'Waehlhebel_SNI'],
            "NM_State": [1, 'NM_RM_aus_BSM'], "UDS_CC": [0, 'Inaktiv'],
            "Wakeup_V12": [1, 'Bus_Wakeup'], "aktiv_KL15": [1, 'KL15_EIN'],
            "aktiv_Diag": [0, 'Inaktiv'], "aktiv_Tmin": [1, 'Mindestaktivzeit'],
            "Haltephase_abgelaufen": [0, 'Inaktiv']
        },
        3: {
            'wait': 1.0,
            "CBV_AWB": [0, 'Passiver Wakeup'], "CBV_CRI": [1, 'NM_mit_Clusteranforderungen'], ### Replace CBV_CRI 0 to 1
            "FCAB": [[1], 'CarWakeUp'], "SNI_10": [83, 'Waehlhebel_SNI'],
            "NM_State": [4, 'NM_NO_aus_RM'], "UDS_CC": [0, 'Inaktiv'],
            "Wakeup_V12": [1, 'Bus_Wakeup'], "aktiv_KL15": [1, 'KL15_EIN'],
            "aktiv_Diag": [0, 'Inaktiv'], "aktiv_Tmin": [0, 'Mindestaktivzeit'], ### Replace aktiv_Tmin 1 to 0
            "Haltephase_abgelaufen": [0, 'Inaktiv']
        }
    }

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_73")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte KL30 an (KL15 aus)", ""])
    hil.cl30_on__.set(1)
    hil.cl15_on__.set(0)
    testresult.append(["Schalte Senden von empfangenen Signalen aus (HiL -> ECU)", "INFO"])
    hil.can0_HIL__HIL_TX__enable.set(0)
    time.sleep(30)
    testresult.append(["[.] Prüfe Busruhe", ""])
    descr, verdict = func_gs.checkBusruhe(daq)
    testresult.append([descr, verdict])
    '''
    temp_value = func_nm.low_current()
    testresult.append(["\x0a6. Botschaftsein- und ausgänge prüfen", ""])
    time.sleep(30)
    testresult.append(basic_tests.checkRange(value=temp_value / 1000,
                                             min_value=0.0,  # 0mA
                                             max_value=0.002,  # 2mA
                                             descr="Prüfe, dass Strom zwischen 0mA und 2mA liegt"))
'''
    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])

    testresult.append(["[.] Schalte KL 15 an (=1) und prüfe NM_Waehlhebel Botschaft", ""])
    testresult.append(["Schalte KL15 = 1", "INFO"])
    hil.cl15_on__.set(1)
    testresult.append(["Schalte Senden von empfangenen Signalen an (HiL -> ECU)", "INFO"])
    hil.can0_HIL__HIL_TX__enable.set(1)

    for loop in test_loops:
        test = test_loops[loop]
        testresult.append(["[.] Warte %ss" % test['wait'], ""])
        time.sleep(test['wait'])  # Zykluszeit NM_Waehlhebel
        testresult.append(["[.] Prüfe Botschaft NM_Waehlhebel", ""])
        testresult.append(["[+0]", ""])
        for variable in test_variables:
            testresult.append(["[.] Prüfe Signal %s" % variable, ""])
            if variable == "FCAB":
                descr,test_id,  verdict = func_nm.checkFcabBitwise(
                    fcab_value = test_variables[variable].get(),
                    bit_exp_one = test[variable][0],
                    bit_exp_zero = [],
                    descr = "Prüfe, dass Bit %s (%s) auf 1 ist"%(', '.join(map(str, test[variable][0])), test[variable][1]))
            else:
                descr,verdict = basic_tests.checkStatus(
                    current_status=test_variables[variable],
                    nominal_status=test[variable][0],
                    descr="Prüfe, dass Wert %s (%s) ist" % (test[variable][0], test[variable][1])
                )
            testresult.append([descr, verdict])
        testresult.append(["[-0]", ""])

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[.] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    # cleanup
    hil = None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################