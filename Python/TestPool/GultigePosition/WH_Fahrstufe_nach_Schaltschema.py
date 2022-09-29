#******************************************************************************
# -*- coding: latin1 -*-
# File    : WH_Fahrstufe_nach_Schaltschema.py
# Title   : WH_Fahrstufe nach Schaltschema
# Task    : WH_Fahrstufe wird dem Schaltschema gesendet der Wählhebelposition
#
# Author  : Mohammed Abdul Karim
# Date    : 02.08.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 02.08.2021 | Mohammed | initial
# 1.1  | 09.09.2021 | Mohammed | Adapted the new TestSpec.
# 1.2  | 11.10.2021 | Devangbhai | Rework
# 1.3  | 10.03.2022 | Devangbhai patel | Changed the waiting time
# 1.4  | 22.03.2022 | Devangbhai patel | Added the evaluation methon using the DAQ


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
from ttk_daq import eval_signal



Fahrstufe_lower_limit = 0.048
Fahrstufe_upper_limit = 0.052
sensor_pos_wh_fahrstufe_lower = 0.039
sensor_pos_wh_fahrstufe_upper = 0.041

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_14")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_com = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_nm = functions_nm.FunctionsNM(testenv)

    # Initialize variables ####################################################
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    wh_sensorRoh = hil.Waehlhebel_04__WH_SensorPos_roh__value
    sishift_StlghDrvPosn = hil.SiShift_01__SIShift_StLghtDrvPosn__value

    meas_vars = [sishift_StlghDrvPosn, wh_fahrstufe,wh_sensorRoh]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()
    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["\xa0Start DAQ Measurement für WH_Fahrstufe und WH_SensorPos_roh ", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)
### 1 ,2

    testresult.append(["\xa0 1. Von X nach Position A1 bringen ", ""])
    timeout = 60
    t_out = timeout + t()
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4 or t_out > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 9:
            testresult.append(["Warte %s ms" %(global_wait_time*1000), ""])
            # testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=9, descr="Prüfe, dass wh_sensorRoh = 9 ist"))
            time.sleep(global_wait_time)
            # testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=6, descr="Prüfe, dass WH_Fahrstufe = 6 ist"))
            break
        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position A1 eingestellt" % timeout, "FAILED"])
            break

    # implementation for checking the WH Fahrstufe value by bringing WH rom A1 to position X
    t_out2 = timeout + t()
    testresult.append(["\xa0 2. Von A1 nach Position X bringen", ""])
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 9 or t_out2 > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4:
            testresult.append(["Warte %s ms" %(global_wait_time*1000), ""])
            # testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=4, descr="Prüfe, dass wh_sensorRoh = 4 ist"))
            time.sleep(global_wait_time)
            # testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=4, descr="Prüfe, dass WH_Fahrstufe = 4 ist"))
            break
        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position X eingestellt" % timeout, "FAILED"])
            break

    testresult.append(["\xa0 2.1 SIShift_StLghtDrvPosn = N setzen", ""])
    descr, verdict = func_gs.changeDrivePosition('N')
    testresult.append(["\xa0" + descr, verdict])

  ### 3 ,4
    testresult.append(["\xa0 3. Von X nach Position B1 bringen ", ""])
    timeout = 60
    t_out = timeout + t()

    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4 or t_out > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 6:
            testresult.append(["Warte %s ms" %(global_wait_time*1000), ""])
            # testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=6, descr="Prüfe, dass wh_sensorRoh = 6 ist"))
            time.sleep(global_wait_time)
            # testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=5,  descr="Prüfe, dass WH_Fahrstufe = 5 ist"))
            break
        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position B1 eingestellt" % timeout, "FAILED"])
            break

    t_out2 = timeout + t()
    testresult.append(["\xa0 4. Von B1 nach Position X bringen", ""])
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 6 or t_out2 > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4:
            testresult.append([" Warte %s ms" %(global_wait_time*1000), ""])
            # testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=4, descr="Prüfe, dass wh_sensorRoh = 4 ist"))
            time.sleep(global_wait_time)
            # testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=4, descr="Prüfe, dass WH_Fahrstufe = 4 ist"))
            break
        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position X eingestellt" % timeout, "FAILED"])
            break

    testresult.append(["\xa0 4.1. SIShift_StLghtDrvPosn = 5 setzen", ""])
    descr, verdict = func_gs.changeDrivePosition('D')
    testresult.append(["\xa0" + descr, verdict])

    ### 5 ,6
    testresult.append(["\xa0 5. von X nach A1  bringen ", ""])
    timeout = 60
    t_out = timeout + t()
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4 or t_out > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 9:
            testresult.append(["Warte %s ms" %(global_wait_time*1000), ""])
            # testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=9, descr="Prüfe, dass wh_sensorRoh = 9 ist"))
            time.sleep(global_wait_time)
            # testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=6, descr="Prüfe, dass WH_Fahrstufe = 6 ist"))
            testresult.append(["\xa0 Von A1 nach A2 bringen ", ""])

            while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 9 or t_out > t():
                if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 7:
                    testresult.append(["Warte %s ms" %(global_wait_time*1000), ""])
                    # testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
                    # testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=7, descr="Prüfe, dass wh_sensorRoh = 7 ist"))
                    time.sleep(global_wait_time)
                    # testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
                    # testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=7, descr="Prüfe, dass WH_Fahrstufe = 7 ist"))
                    break

                elif not (t_out > t()):
                    testresult.append(
                        ["Wählhebel würde nicht in %s sec auf Position A2 eingestellt" % timeout, "FAILED"])
                    break
            break

        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position A1 eingestellt" % timeout, "FAILED"])
            break

    testresult.append(["\xa0 5.1.  SIShift_StLghtDrvPosn = 7 setzen", ""])
    descr, verdict = func_gs.changeDrivePosition('R')
    testresult.append(["\xa0" + descr, verdict])

    t_out2 = timeout + t()
    testresult.append(["\xa0 6. Von A2 über A1 nach X Position verfahren", ""])
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 7 or t_out2 > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4:
            testresult.append(["Warte %s ms" %(global_wait_time*1000), ""])
            # testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=4, descr="Prüfe, dass wh_sensorRoh = 4 ist"))
            time.sleep(global_wait_time)
            # testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=4, descr="Prüfe, dass WH_Fahrstufe = 4 ist"))
            break
        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position X eingestellt" % timeout, "FAILED"])
            break


    ### 7 ,8
    testresult.append(["\xa0 7. Wählhebel X nach B1 bringen ", ""])
    timeout = 60
    t_out = timeout + t()
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4 or t_out > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 6:
            testresult.append([" Warte %s ms" %(global_wait_time*1000), ""])
            # testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=6, descr="Prüfe, dass wh_sensorRoh = 6 ist"))
            time.sleep(global_wait_time)
            # testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=6, descr="Prüfe, dass WH_Fahrstufe = 6 ist"))

            testresult.append(["\xa0 Wählhebel B1 nach B2 bringen ", ""])
            while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 6 or t_out > t():
                if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 5:
                    testresult.append([" Warte %s ms" %(global_wait_time*1000), ""])
                    # testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
                    # testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=5, descr="Prüfe, dass wh_sensorRoh = 5 ist"))
                    time.sleep(global_wait_time)
                    # testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
                    # testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=5, descr="Prüfe, dass WH_Fahrstufe = 5 ist"))
                    break
                elif not (t_out > t()):
                    testresult.append(
                        ["Wählhebel würde nicht in %s sec auf Position B2 eingestellt" % timeout, "FAILED"])
                    break
            break
        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position B1 eingestellt" % timeout, "FAILED"])
            break

    testresult.append([" \xa0 7.1 SIShift_StLghtDrvPosn = 5 setzen", ""])
    descr, verdict = func_gs.changeDrivePosition('D')
    testresult.append(["\xa0" + descr, verdict])

    t_out2 = timeout + t()
    testresult.append(["\xa0 8 Wählhebel von B2 über B1 nach X bringen", ""])
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 5 or t_out2 > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4:
            testresult.append([" Warte %s ms" %(global_wait_time*1000), ""])
            # testresult.append(["[.] Prüfe, dass WH_SensorPos_roh ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_sensorRoh, nominal_status=4, descr="Prüfe, dass wh_sensorRoh = 4 ist"))
            time.sleep(global_wait_time)
            # testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            # testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=4, descr="Prüfe, dass WH_Fahrstufe = 4 ist"))
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
    for mes in [sishift_StlghDrvPosn, wh_fahrstufe, wh_sensorRoh]:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(
        daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))

    WH_SensorPos_roh = daq_data[str(hil.Waehlhebel_04__WH_SensorPos_roh__value)]
    WH_SensorPos_roh = eval_signal.EvalSignal(WH_SensorPos_roh)
    WH_SensorPos_roh.clearAll()
    time_zero = WH_SensorPos_roh.getTime()
    SensorPos_x = WH_SensorPos_roh.find(operator="==", value=4)
    SensorPos_a1 = WH_SensorPos_roh.findNext(operator="==", value=9)
    SensorPos_a1_x = WH_SensorPos_roh.findNext(operator="==", value=4)
    SensorPos_b1 = WH_SensorPos_roh.findNext(operator="==", value=6)
    SensorPos_b1_x = WH_SensorPos_roh.findNext(operator="==", value=4)
    SensorPos_x_a1 = WH_SensorPos_roh.findNext(operator="==", value=9)
    SensorPos_a1_a2 = WH_SensorPos_roh.findNext(operator="==", value=7)
    SensorPos_a2_x = WH_SensorPos_roh.findNext(operator="==", value=4)
    SensorPos_x_b1 = WH_SensorPos_roh.findNext(operator="==", value=6)
    SensorPos_b1_b2 = WH_SensorPos_roh.findNext(operator="==", value=5)
    SensorPos_b2_x = WH_SensorPos_roh.findNext(operator="==", value=4)
    WH_SensorPos_roh.setEvalRange(SensorPos_x, SensorPos_b2_x)
    SensorPos_error = WH_SensorPos_roh.find(operator="==", value=15)

    testresult.append(["Ermittelter Zeitpunkt 'x': %s" % (SensorPos_x - time_zero), "INFO"])
    testresult.append(["Ermittelter Zeitpunkt 'A1': %s" % (SensorPos_a1 - time_zero), "INFO"])
    testresult.append(["Ermittelter Zeitpunkt 'x': %s" % (SensorPos_a1_x - time_zero), "INFO"])
    testresult.append(["Ermittelter Zeitpunkt 'B1': %s" % (SensorPos_b1 - time_zero), "INFO"])
    testresult.append(["Ermittelter Zeitpunkt 'x': %s" % (SensorPos_b1_x - time_zero), "INFO"])
    testresult.append(["Ermittelter Zeitpunkt 'A1': %s" % (SensorPos_x_a1 - time_zero), "INFO"])
    testresult.append(["Ermittelter Zeitpunkt 'A2': %s" % (SensorPos_a1_a2 - time_zero), "INFO"])
    testresult.append(["Ermittelter Zeitpunkt 'x': %s" % (SensorPos_a2_x - time_zero), "INFO"])
    testresult.append(["Ermittelter Zeitpunkt 'B1': %s" % (SensorPos_x_b1 - time_zero), "INFO"])
    testresult.append(["Ermittelter Zeitpunkt 'B2': %s" % (SensorPos_b1_b2 - time_zero), "INFO"])
    testresult.append(["Ermittelter Zeitpunkt 'x': %s" % (SensorPos_b2_x - time_zero), "INFO"])

    WH_Fahrstufe = daq_data[str(hil.Waehlhebel_04__WH_Fahrstufe__value)]
    WH_Fahrstufe = eval_signal.EvalSignal(WH_Fahrstufe)
    WH_Fahrstufe.clearAll()
    time_zero2 = WH_Fahrstufe.getTime()
    WH_Fahrstufe_x = WH_Fahrstufe.find(operator="==", value=4)
    WH_Fahrstufe_a1 = WH_Fahrstufe.findNext(operator="==", value=6)
    WH_Fahrstufe_a1_x = WH_Fahrstufe.findNext(operator="==", value=4)
    WH_Fahrstufe_b1 = WH_Fahrstufe.findNext(operator="==", value=5)
    WH_Fahrstufe_b1_x = WH_Fahrstufe.findNext(operator="==", value=4)
    WH_Fahrstufe_x_a1 = WH_Fahrstufe.findNext(operator="==", value=6)
    WH_Fahrstufe_x_a1_x = WH_Fahrstufe.findNext(operator="==", value=4)
    WH_Fahrstufe_a1_a2 = WH_Fahrstufe.findNext(operator="==", value=7)
    WH_Fahrstufe_a2_x = WH_Fahrstufe.findNext(operator="==", value=4)
    WH_Fahrstufe_x_b1 = WH_Fahrstufe.findNext(operator="==", value=6)
    WH_Fahrstufe_x_b1_x = WH_Fahrstufe.findNext(operator="==", value=4)
    WH_Fahrstufe_b1_b2 = WH_Fahrstufe.findNext(operator="==", value=5)
    WH_Fahrstufe_b2_x = WH_Fahrstufe.findNext(operator="==", value=4)
    WH_Fahrstufe.setEvalRange(WH_Fahrstufe_x, WH_Fahrstufe_b2_x)
    WH_Fahrstufe_error = WH_Fahrstufe.find(operator="==", value=15)

    # position x->A1
    testresult.append(["\x0a 1. Wählhebel von  X nach  A1 bringen ", ""])
    if WH_Fahrstufe_a1 and SensorPos_a1 is not None:
        testresult.append(["Wählhebel hat um %s wh_sensorRoh = 9 gesendet " % (SensorPos_a1 - time_zero), "PASSED"])
        testresult.append(basic_tests.checkRange((WH_Fahrstufe_a1 - time_zero2) - (SensorPos_a1 - time_zero),
                                                 sensor_pos_wh_fahrstufe_lower, sensor_pos_wh_fahrstufe_upper,
                                                 descr="Prüfe das WH fahrstufe nach 40ms nach erkennung der  SensorPos_roh = 9 gesendet wird"))
    if WH_Fahrstufe_a1 and WH_Fahrstufe_a1_x is not None:
        testresult.append(basic_tests.checkRange((WH_Fahrstufe_a1_x - time_zero2) - (WH_Fahrstufe_a1 - time_zero2),
                                                 Fahrstufe_lower_limit, Fahrstufe_upper_limit,
                                                 descr="Prüfe das WH fahrstufe is 6 für 50ms gesendet "))

    # position A1-> x
    testresult.append(["\x0a2. Wählhebel von A1 nach X bringen", ""])
    if SensorPos_a1_x and WH_Fahrstufe_a1_x is not None:
        testresult.append(["Wählhebel hat um %s wh_sensorRoh = 4 gesendet " % (SensorPos_a1_x - time_zero), "PASSED"])
        testresult.append(
            ["Wählhebel hat um %s WH_Fahrstufe = 4 gesendet " % (WH_Fahrstufe_a1_x - time_zero2), "PASSED"])

    # position x->B1
    testresult.append(["\x0a 3. Wählhebel von X nach  B1 bringen ", ""])
    if WH_Fahrstufe_b1 and SensorPos_b1 is not None:
        testresult.append(["Wählhebel hat um %s wh_sensorRoh = 6 gesendet " % (SensorPos_b1 - time_zero), "PASSED"])
        testresult.append(basic_tests.checkRange((WH_Fahrstufe_b1 - time_zero2) - (SensorPos_b1 - time_zero),
                                                 sensor_pos_wh_fahrstufe_lower, sensor_pos_wh_fahrstufe_upper,
                                                 descr="Prüfe das WH fahrstufe nach 40ms nach erkennung der  SensorPos_roh = 6 gesendet wird"))
    if WH_Fahrstufe_b1 and WH_Fahrstufe_b1_x is not None:
        testresult.append(basic_tests.checkRange((WH_Fahrstufe_b1_x - time_zero2) - (WH_Fahrstufe_b1 - time_zero2),
                                                 Fahrstufe_lower_limit, Fahrstufe_upper_limit,
                                                 descr="Prüfe das WH fahrstufe is 5 für 50ms gesendet "))

    # position B1-> X
    testresult.append(["\x0a4. Wählhebel von B1 nach X bringen", ""])
    if SensorPos_b1_x and WH_Fahrstufe_b1_x is not None:
        testresult.append(["Wählhebel hat um %s wh_sensorRoh = 4 gesendet " % (SensorPos_b1_x - time_zero), "PASSED"])
        testresult.append(
            ["Wählhebel hat um %s WH_Fahrstufe = 4 gesendet " % (WH_Fahrstufe_b1_x - time_zero2), "PASSED"])

    # position x->A1
    testresult.append(["\x0a5.1. Wählhebel von  X nach  A1 bringen", ""])
    if WH_Fahrstufe_x_a1 and SensorPos_x_a1 is not None:
        testresult.append(["Wählhebel hat um %s wh_sensorRoh = 9 gesendet " % (SensorPos_x_a1 - time_zero), "PASSED"])
        testresult.append(basic_tests.checkRange((WH_Fahrstufe_x_a1 - time_zero2) - (SensorPos_x_a1 - time_zero),
                                                 sensor_pos_wh_fahrstufe_lower, sensor_pos_wh_fahrstufe_upper,
                                                 descr="Prüfe das WH fahrstufe nach 40ms nach erkennung der  SensorPos_roh = 9 gesendet wird"))

    if WH_Fahrstufe_x_a1 and WH_Fahrstufe_x_a1_x is not None:
        testresult.append(basic_tests.checkRange((WH_Fahrstufe_x_a1_x - time_zero2) - (WH_Fahrstufe_x_a1 - time_zero2),
                                                 Fahrstufe_lower_limit, Fahrstufe_upper_limit,
                                                 descr="Prüfe das WH fahrstufe is 6 für 50ms gesendet "))

    # position A1->A2
    testresult.append(["\x0a5.2.  Wählhebel von A1 nach A2 bringen", ""])
    if WH_Fahrstufe_a1_a2 and SensorPos_a1_a2 is not None:
        testresult.append(["Wählhebel hat um %s wh_sensorRoh = 7 gesendet " % (SensorPos_a1_a2 - time_zero), "PASSED"])
        testresult.append(basic_tests.checkRange((WH_Fahrstufe_a1_a2 - time_zero2) - (SensorPos_a1_a2 - time_zero),
                                                 sensor_pos_wh_fahrstufe_lower, sensor_pos_wh_fahrstufe_upper,
                                                 descr="Prüfe das WH fahrstufe nach 40ms nach erkennung der  SensorPos_roh = 7 gesendet wird"))

    if WH_Fahrstufe_a1_a2 and WH_Fahrstufe_a2_x is not None:
        testresult.append(basic_tests.checkRange((WH_Fahrstufe_a2_x - time_zero2) - (WH_Fahrstufe_a1_a2 - time_zero2),
                                                 Fahrstufe_lower_limit, Fahrstufe_upper_limit,
                                                 descr="Prüfe das WH fahrstufe is 7 für 50ms gesendet"))

    # position A2-> x
    testresult.append(["\x0a6. Wählhebel von A2 nach X bringen", ""])
    if SensorPos_a2_x and WH_Fahrstufe_a2_x is not None:
        testresult.append(["Wählhebel hat um %s wh_sensorRoh = 4 gesendet " % (SensorPos_a2_x - time_zero), "PASSED"])
        testresult.append(
            ["Wählhebel hat um %s WH_Fahrstufe = 4 gesendet " % (WH_Fahrstufe_a2_x - time_zero2), "PASSED"])

    # position x->B1
    testresult.append(["\x0a7.1. Wählhebel von X nach  B1 bringen", ""])
    if WH_Fahrstufe_x_b1 and SensorPos_x_b1 is not None:
        testresult.append(["Wählhebel hat um %s wh_sensorRoh = 6 gesendet " % (SensorPos_x_b1 - time_zero), "PASSED"])
        testresult.append(basic_tests.checkRange((WH_Fahrstufe_x_b1 - time_zero2) - (SensorPos_x_b1 - time_zero),
                                                 sensor_pos_wh_fahrstufe_lower, sensor_pos_wh_fahrstufe_upper,
                                                 descr="Prüfe das WH fahrstufe nach 40ms nach erkennung der  SensorPos_roh = 6 gesendet wird"))

    if WH_Fahrstufe_x_b1 and WH_Fahrstufe_x_b1_x is not None:
        testresult.append(basic_tests.checkRange((WH_Fahrstufe_x_b1_x - time_zero2) - (WH_Fahrstufe_x_b1 - time_zero2),
                                                 Fahrstufe_lower_limit, Fahrstufe_upper_limit,
                                                 descr="Prüfe das WH fahrstufe is 6 für 50ms gesendet"))

    # position B1->B2
    testresult.append(["\x0a7.2. Wählhebel von B1 nach  B2 bringen", ""])
    if WH_Fahrstufe_b1_b2 and SensorPos_b1_b2 is not None:
        testresult.append(["Wählhebel hat um %s wh_sensorRoh = 5 gesendet " % (SensorPos_b1_b2 - time_zero), "PASSED"])
        testresult.append(basic_tests.checkRange((WH_Fahrstufe_b1_b2 - time_zero2) - (SensorPos_b1_b2 - time_zero),
                                                 sensor_pos_wh_fahrstufe_lower, sensor_pos_wh_fahrstufe_upper,
                                                 descr="Prüfe das WH fahrstufe nach 40ms nach erkennung der  SensorPos_roh = 5 gesendet wird"))

    if WH_Fahrstufe_b1_b2 and WH_Fahrstufe_b2_x is not None:
        testresult.append(basic_tests.checkRange((WH_Fahrstufe_b2_x - time_zero2) - (WH_Fahrstufe_b1_b2 - time_zero2),
                                                 Fahrstufe_lower_limit, Fahrstufe_upper_limit,
                                                 descr="Prüfe das WH fahrstufe ist 5 für 50ms gesendet "))

    testresult.append(["\x0a8. Wählhebel von B2 nach X bringen", ""])
    if SensorPos_b2_x and WH_Fahrstufe_b2_x is not None:
        testresult.append(["Wählhebel hat um %s wh_sensorRoh = 4 gesendet " % (SensorPos_b2_x - time_zero), "PASSED"])
        testresult.append(
            ["Wählhebel hat um %s WH_Fahrstufe = 4 gesendet " % (WH_Fahrstufe_b2_x - time_zero2), "PASSED"])

    # Check WH_Fahrstufe Error value
    testresult.append(["\x0a9 Prüf Zu keiner Zeit wird Fehler für WH_Fahrstufe gesendet", ""])
    if WH_Fahrstufe_error is not None:
        testresult.append(
            ["WH_Fahrstufe ist hat  Error (15) wert gesendet um %s " % (WH_Fahrstufe_error - time_zero2), "FAILED"])
    else:
        testresult.append(["WH_Fahrstufe ist hat kein Error (15) wert gesendet", "PASSED"])

    # Check SensorPos_Roh Error value
    testresult.append(["\x0a10 Prüf Zu keiner Zeit wird Fehler für SensorPos_Roh gesendet", ""])
    if SensorPos_error is not None:
        testresult.append(
            ["SensorPos_Roh ist hat  Error (15) wert gesendet um %s " % (SensorPos_error - time_zero), "FAILED"])
    else:
        testresult.append(["SensorPos_Roh ist hat kein Error (15) wert gesendet", "PASSED"])

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
