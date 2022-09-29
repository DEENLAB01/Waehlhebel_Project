#******************************************************************************
# -*- coding: latin1 -*-
# File    : Init_Inbetriebnahme.py
# Title   : Initialisierungs Phase
# Task    : Initialisierungs Phase
#
# Author  : Mohammed Abdul Karim
# Date    : 30.07.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 30.07.2021 | Mohammed | initial
# 1.1  | 07.10.2021 | Devangbhai Patel | Rework
# 1.2  | 10.03.2022 | Devangbhai patel | Changed the waiting time

#******************************************************************************
# Imports #####################################################################
import time
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
from time import time as t
from global_wait_time import global_wait_time
from ttk_daq import eval_signal



# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_6")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)


    # Initialize variables ####################################################
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    wh_fahrstufe.alias = "Waehlhebel_04:WH_Fahrstufe"
    kl15_status_var = hil.ClampControl_01__KST_KL_15__value
    kl15_status_var.alias = "ClampControl_01:KST_KL_15"
    wh_sensorRoh = hil.Waehlhebel_04__WH_SensorPos_roh__value
    wh_sensorRoh.alias = "Waehlhebel_04:WH_SensorPos_roh"
    SiShift = hil.SiShift_01__SIShift_StLghtDrvPosn__value

    meas_vars = [kl15_status_var, wh_fahrstufe,wh_sensorRoh, SiShift]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an)", ""])
    hil.cl30_on__.set(1)

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["\xa0Start DAQ Measurement für WH_Fahrstufe und WH_SensorPos_roh ", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["[+] Starte ECU (KL15 an)", ""])
    hil.cl15_on__.set(1)
    testresult.append(["[.] CAN-Trace auswerten nach 200 ms", ""])
    time.sleep(0.200)

    testresult.append(["[] Prüfe, dass WH_Fahrstufe ist", ""])
    testresult.append( basic_tests.checkStatus(current_status=hil.Waehlhebel_04__WH_Fahrstufe__value, nominal_status=4, descr="Prüfe, dass WH_Fahrstufe = 4 ist"))

    testresult.append(["[] Prüfe, dass WH_SensorPos_roh ist", ""])
    testresult.append(basic_tests.checkStatus(current_status=hil.Waehlhebel_04__WH_SensorPos_roh__value, nominal_status=4, descr="Prüfe, dass wh_sensorRoh = 4 ist"))

    testresult.append(["[.] Waehlhebelposition P (8) setzen, nach 1000ms CAN Trace Auswerten", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])
    time.sleep(1)

    testresult.append(["[] Prüfe, dass WH_Fahrstufe ist", ""])
    testresult.append(basic_tests.checkStatus(current_status=hil.Waehlhebel_04__WH_Fahrstufe__value, nominal_status=4,descr="Prüfe, dass WH_Fahrstufe = 4 ist"))

    testresult.append(["[] Prüfe, dass WH_SensorPos_roh ist", ""])
    testresult.append(basic_tests.checkStatus(current_status=hil.Waehlhebel_04__WH_SensorPos_roh__value, nominal_status=4, descr="Prüfe, dass wh_sensorRoh = 4 ist"))


    testresult.append(["[.] Wählhebel in Position A1 bringen ", ""])
    timeout = 60
    t_out = timeout + t()
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4 or t_out > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 9:
            testresult.append(["[.] Warte %s ms" %(global_wait_time*1000), ""])
            testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
            testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=9,
                                                      descr="Prüfe, dass wh_sensorRoh = 9 ist"))
            time.sleep(global_wait_time)
            testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=6,
                                                      descr="Prüfe, dass WH_Fahrstufe = 6 ist"))
            break
        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position A1 eingestellt" % timeout, "FAILED"])
            break

    t_out2 = timeout + t()
    testresult.append(["[.] Wählhebel loslassen", ""])
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 9 or t_out2 > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4:
            testresult.append(["[.] Warte %s ms" %(global_wait_time*1000), ""])
            testresult.append(["[] Prüfe, dass WH_SensorPos_roh ist", ""])
            testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=4, descr="Prüfe, dass wh_sensorRoh = 4 ist"))
            time.sleep(global_wait_time)
            testresult.append(["[] Prüfe, dass WH_Fahrstufe ist", ""])
            testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=4, descr="Prüfe, dass WH_Fahrstufe = 4 ist"))
            break
        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position X eingestellt" % timeout, "FAILED"])
            break
    testresult.append(["[.] Waehlhebelposition N (6) aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Wählhebel in Position B1 bringen ", ""])
    t_out = timeout + t()
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4 or t_out > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 6:
            testresult.append(["[.] Warte %s ms" %(global_wait_time*1000), ""])
            testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
            testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=6, descr="Prüfe, dass wh_sensorRoh = 6 ist"))
            time.sleep(global_wait_time)
            testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=5, descr="Prüfe, dass WH_Fahrstufe = 5 ist"))
            break
        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position B1 eingestellt" % timeout, "FAILED"])
            break

    t_out2 = timeout + t()
    testresult.append(["[.] Wählhebel loslassen", ""])
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 6 or t_out2 > t():
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

    testresult.append(["[.] Waehlhebelposition D (5) aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('D')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Wählhebel in Position A2 bringen ", ""])
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
    testresult.append(["[.] Wählhebel loslassen", ""])
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

    testresult.append(["[.] Waehlhebelposition R (7) aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('R')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Wählhebel in Position B2 bringen ", ""])

    t_out = timeout + t()
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4 or t_out > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 5:
            testresult.append(["[.] Warte %s ms" %(global_wait_time*1000), ""])
            testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
            testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=5, descr="Prüfe, dass wh_sensorRoh = 5 ist"))
            time.sleep(global_wait_time)
            testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=5, descr="Prüfe, dass WH_Fahrstufe = 5 ist"))
            break
        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position B2 eingestellt" % timeout, "FAILED"])
            break

    t_out2 = timeout + t()
    testresult.append(["[.] Wählhebel loslassen", ""])
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 5 or t_out2 > t():
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
    for mes in [kl15_status_var, wh_fahrstufe, wh_sensorRoh, SiShift]:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(
        daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))

    # WH_SensorPos_roh = daq_data[str(hil.Waehlhebel_04__WH_SensorPos_roh__value)]
    # WH_SensorPos_roh = eval_signal.EvalSignal(WH_SensorPos_roh)
    # WH_SensorPos_roh.clearAll()
    # time_zero = WH_SensorPos_roh.getTime()
    # SensorPos_original = WH_SensorPos_roh.find(operator="==", value=4)
    # SensorPos_original = WH_SensorPos_roh.find(operator="==", value=4)

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
