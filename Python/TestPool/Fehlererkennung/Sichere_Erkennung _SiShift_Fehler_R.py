#******************************************************************************
# -*- coding: latin1 -*-
# File    : Sichere_Erkennung _SiShift_Fehler_R.py
# Title   : Sichere Erkennung Sishift Fehler R
# Task    : Sichere Erkennung der Sishift Fehler R
#
# Author  : Mohammed Abdul Karim
# Date    : 29.07.2021
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 23.07.2021 | Mohammed | initial
# 1.1  | 21.09.2021 | Mohammed | Rework
# 1.2  | 10.03.2022 | Devangbhai patel | Changed the waiting time


#******************************************************************************
# Imports #####################################################################
import time
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import functions_gearselection
import functions_common
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
    testresult.setTestcaseId("TestSpec_45")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()
    func_gs = functions_gearselection.FunctionsGearSelection(testenv, hil)
    func_com = functions_common.FunctionsCommon(testenv)

    # Initialize variables ####################################################
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    sishift_stlfgtDrvPos = hil.SiShift_01__SIShift_StLghtDrvPosn__value

    wh_fahrstufe_fehlerwert = 15
    meas_vars = [sishift_stlfgtDrvPos, wh_fahrstufe]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    testenv.startupECU()

    testresult.append(["[.] Waehlhebelposition P aktiviert", ""])
    descr, verdict = func_gs.changeDrivePosition('P')
    testresult.append(["\xa0" + descr, verdict])

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    testresult.append(["\xa0Start DAQ Measurement für WH_Fahrstufe der Fehlerreaktionen", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["[.] Wählhebel in Position A2 bringen ", ""])
    timeout = 60
    t_out = timeout + t()
    while hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 4 or t_out > t():
        if hil.Waehlhebel_04__WH_SensorPos_roh__value.get() == 7:
            testresult.append(["[.] Warte %s ms" %(global_wait_time*1000), ""])
            time.sleep(global_wait_time)
            testresult.append(["[.] Prüfe, dass WH_Fahrstufe ist", ""])
            testresult.append(basic_tests.checkStatus(current_status=wh_fahrstufe, nominal_status=7,
                                                      descr="Prüfe, dass WH_Fahrstufe = 7 ist"))
            break
        elif not (t_out > t()):
            testresult.append(["Wählhebel würde nicht in %s sec auf Position A2 eingestellt" % timeout, "FAILED"])
            break

### 2. Getriebe Fehler senden
    time.sleep(0.050)
    testresult.append(["[.] Prüfe, dass Getriebe Fehler senden ", ""])
    testresult.append(["\xa0Setze SiShift SIShift_StLghtDrvPosn auf 15 (Fehler)", ""])
    descr, verdict = func_gs.changeDrivePosition('Fehler')
    testresult.append(["\xa0" + descr, verdict])

    testresult.append(["[.] Warte 2 Sekunde, bevor DAQ Messung beendet wird", ""])
    time.sleep(2)
    testresult.append(["Stopp DAQ Measurement", "INFO"])
    daq_data = daq.stopMeasurement()
    time.sleep(0.5)
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])

    testresult.append(["[+] Prüfe WH_Fahrstufe = 15 (Fehler) ist", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=wh_fahrstufe,
            nominal_status= 15,
            descr="Prüfe, dass WH_Fahrstufe = Fehler ist"
        )
    )

    # erzeuge Plot für Testreport (ohne KL15)
    plot_data = {}
    for mes in [sishift_stlfgtDrvPos, wh_fahrstufe]:
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
    testenv.breakdown()
    # #########################################################################
