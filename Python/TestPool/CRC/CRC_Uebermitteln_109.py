#******************************************************************************
# -*- coding: latin1 -*-
# File    : CRC_Uebermitteln_109.py
# Title   : Botschaften Übermitteln CRC
# Task    : Test for correct calculation of CRC
#
# Author  : An3Neumann
# Date    : 09.07.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 09.07.2021 | An3Neumann | initial
# 1.1  | 09.07.2021 | Mohammed | Botschaft korrigiert: bz_signal nach crc_signal
# 1.2  | 09.07.2021 | Mohammed | Rework

#******************************************************************************
import time
from _automation_wrapper_ import TestEnv
import functions_common
import functions_gearselection
from ttk_daq import eval_signal

testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_com = functions_common.FunctionsCommon(testenv)
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)

    # Initialize variables ####################################################
    #bz_signal = hil.Waehlhebel_04__Waehlhebel_04_BZ__value ### Falsche Signal
    crc_signal = hil.Waehlhebel_04__Waehlhebel_04_CRC__value
    waehlhebel_04_timestamp = hil.Waehlhebel_04__timestamp
    meas_vars = [crc_signal, waehlhebel_04_timestamp]
    cycle_time = func_gs.messages_tx_cycletimes['self.hil.Waehlhebel_04']
    cycle_time_tol_perc = 0.15 # 15%
    min_cycle_time = round(cycle_time*(1-cycle_time_tol_perc), 2)
    max_cycle_time = round(cycle_time*(1+cycle_time_tol_perc), 2)
    measure_time_s = 10

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_109")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] ECU einschalten", ""])
    testenv.startupECU()
    testresult.append(["[.] Setze SiShift_01:SIShift_StLghtDrvPosn auf P", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append([descr, verdict])

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split(".py")[0], ""])

    testresult.append(["[+] Start DAQ Measurement für CRC Analyse", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["[.] Warte %s Sekunden"%measure_time_s, ""])
    func_com.waitSecondsWithResponse(wait_second=measure_time_s)

    testresult.append(["[.] Stopp DAQ Measurement", ""])
    daq_data = daq.stopMeasurement()
    time.sleep(0.5)

    testresult.append(["\nStart Analyse of DAQ Measurement", ""])

    crc_data = daq_data[str(crc_signal)]
    analyse_crc_data = eval_signal.EvalSignal(crc_data)
    analyse_crc_data.clearAll()

    waehlhebel_04 = daq_data[str(waehlhebel_04_timestamp)]
    analyse_waehlhebel_04 = eval_signal.EvalSignal(waehlhebel_04)
    analyse_waehlhebel_04.clearAll()

    analyse_crc_data.findChanged()
    curr_value = analyse_crc_data.getData()
    curr_timestamp = analyse_waehlhebel_04.seek(analyse_crc_data.getTime())

    verdict_cycletime = 'PASSED'
    verdict_crc = 'PASSED'
    counter = 0
    failed_ct_counter = []
    while True:
        result = analyse_crc_data.findChanged()
        if result:
            next_value = analyse_crc_data.getData()
            next_timestamp = analyse_waehlhebel_04.seek(analyse_crc_data.getTime())

            curr_cycle_time = round(next_timestamp - curr_timestamp, 2)/1000.0
            if not (min_cycle_time <= curr_cycle_time <= max_cycle_time):
                verdict_cycletime = 'FAILED'
                failed_ct_counter.append(curr_cycle_time)
            curr_timestamp = next_timestamp

            if curr_value == 255:
                if next_value != 0:
                    verdict_bz = 'FAILED'
            else:
                if next_value != curr_value + 1:
                    verdict_bz = 'FAILED'
            curr_value = next_value

            counter += 1
        else:
            break
    '''
            if next_value == curr_value: # Todo ggf. Wertebereich?
                verdict_crc = 'FAILED'
            curr_value = next_value

            counter += 1
        else:
            break
        '''

    testresult.append(["Es wurden %s Änderungen des Zählers geprüft"%counter, "INFO"])

    testresult.append(["[.] Prüfe, dass die Inkrementierung des CRCs korrekt ist", ""])
    if verdict_crc == 'PASSED':
        testresult.append(["Der CRC wurde korrekt inkrementiert", verdict_crc])
    else:
        testresult.append(["Der CRC wurde nicht korrekt inkrementiert", verdict_crc])

    testresult.append(["[.] Prüfe die Zykluszeit (%ss - %ss) der Inkrementierung des CRCs"%(min_cycle_time, max_cycle_time), ""])
    if verdict_cycletime == 'PASSED':
        testresult.append(["Die Zykluszeit des Inkrementierens ist korrekt", verdict_cycletime])
    else:
        testresult.append(["Die Zykluszeit des Inkrementierens ist nicht korrekt\n%s Falsche Zykluszeiten:\n"
                              "%s"%(len(failed_ct_counter), ', '.join(map(str, failed_ct_counter))), verdict_cycletime])

    testresult.append(
        daq.plotSingleShot(crc_data, testenv.script_name.split(".py")[0], "Waehlhebel_04:Waehlhebel_04_CRC ",)
    )

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[-] Test Nachbedingungen", ""])
    testresult.append(["Shutdown ECU", ""])
    testenv.shutdownECU()

    ## Cleanup
    hil=None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################
