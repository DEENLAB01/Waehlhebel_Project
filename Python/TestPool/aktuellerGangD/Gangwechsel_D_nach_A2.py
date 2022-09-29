#******************************************************************************
# -*- coding: latin1 -*-
# File    : Gangwechsel_D_nach_A2.py
# Title   : Gangwechsel D nach A2
# Task    : Gangwechsel aus D nach A2
#
# Author  : Mohammed Abdul Karim
# Date    : 03.08.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 03.08.2021 | Mohammed | initial
# 1.1  | 17.09.2021 | Devangbhai Patel  | Rework
# 1.3  | 10.03.2022 | Devangbhai patel |Changed the waiting time
#******************************************************************************
# Imports #####################################################################
import time
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
import functions_common
import functions_nm
from time import time as t
from global_wait_time import global_wait_time

# Instantiate test environment
testenv = TestEnv()



try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_63")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_com = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    wh_sensorRoh = hil.Waehlhebel_04__WH_SensorPos_roh__value
    SiShift = hil.SiShift_01__SIShift_StLghtDrvPosn__value

    meas_vars = [wh_fahrstufe, wh_sensorRoh, SiShift]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    testresult.append(["[.] Waehlhebelposition D aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('D')
    testresult.append(["\xa0" + descr, verdict])

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["\xa0Start DAQ Measurement für WH_Fahrstufe und WH_SensorPos_roh ", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)
### 1
    testresult.append(["[.] Wählhebel in Position A2 bringen ", ""])
    timeout = 60
    t_out = timeout + t()
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4 or t_out > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 7:
            testresult.append(["[.] Warte %s ms" %(global_wait_time*1000), ""])
            testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
            testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=7, descr="Prüfe, dass wh_sensorRoh = 7 ist"))
            time.sleep(global_wait_time)
            testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=7, descr="Prüfe, dass WH_Fahrstufe = 7 ist"))
            break
        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position A2 eingestellt" % timeout, "FAILED"])
            break

    t_out2 = timeout + t()
    testresult.append(["[.] Wählhebel in Position X bringen", ""])
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 7 or t_out2 > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4:
            testresult.append(["[.] Warte %s ms" %(global_wait_time*1000), ""])
            testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
            testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=4, descr="Prüfe, dass wh_sensorRoh = 4 ist"))
            time.sleep(global_wait_time)
            testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=4, descr="Prüfe, dass WH_Fahrstufe = 4 ist"))
            break
        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position X eingestellt" % timeout, "FAILED"])
            break

    testresult.append(["[.] Warte 2 Sekunde, bevor DAQ Messung beendet wird", ""])
    time.sleep(2)
    testresult.append(["Stopp DAQ Measurement", "INFO"])
    daq_data = daq.stopMeasurement()
    time.sleep(0.5)
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])

    # erzeuge Plot für Testreport
    plot_data = {}
    for mes in [wh_fahrstufe, wh_sensorRoh, SiShift]:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(
        daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()

    ## Cleanup
    hil=None

finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=False)
    # #########################################################################
