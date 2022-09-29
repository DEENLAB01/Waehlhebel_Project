#******************************************************************************
# -*- coding: latin1 -*-
# File    : Fehlererkennung_Timeout_Kl15_Keine_Botschaft.py
# Title   : Fehlererkennung Timeout KL15 keine Botschaft
# Task    : Fehlererkennungund Behandlung bei KL15 Timeout
#
# Author  : A. Neumann
# Date    : 08.07.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 08.07.2021 | NeumannA | initial
# 1.1  | 27.07.2021 | Mohammed | Added TestSpec_ID
# 1.2  | 19.07.2021 | Mohammed | ClampControl_01 value corrected 0 to 1
# 1.3  | 16.08.2021 | Mohammed | Added warte Zeit
# 1.4  | 22.08.2022 | Mohammed | Rework
#******************************************************************************
# Imports #####################################################################
import time
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
from simplified_bus_tests import getMaxValidPeriod
from ttk_daq import eval_signal

# Instantiate test environment
testenv = TestEnv()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_200")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    kl15_period = hil.ClampControl_01__period
    cycle_time = kl15_period.value_lookup["an"]
    timeout_quali_max = 10
    kl15_status_var = hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value
    wh_fahrstufe = hil.Waehlhebel_04__WH_Fahrstufe__value
    wh_fahrstufe_fehlerwert = 15
    allowed_fahrstufe = [4, 5, 6, 7]  # Nicht betigt, D, N, R
    KST_KL_15 = hil.ClampControl_01__KST_KL_15__value

    meas_vars = [kl15_status_var, wh_fahrstufe, KST_KL_15]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte ECU an - ClampConrol_01 Period = 0", ""])
    hil.cl30_on__.set(1)
    hil.cl15_on__.set(1)
    kl15_period.setState('aus')
    canape_diag = testenv.getCanapeDiagnostic()

    # TEST PROCESS ############################################################
    testresult.append(["\n Starte Testprozess: {}".format(testenv.script_name.split('.py')[0]), ""])
    # silently go one chapter level up
    testresult.append(["[-0]", ""])

    testresult.append(["[.] Start DAQ Measurement für Timing-Verhalten der Fehlerreaktionen", ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    testresult.append(["[.] Lese ClampControl_01:KST_KL_15 ", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.ClampControl_01__KST_KL_15__value,
            nominal_status=1, ## to change value 0 to 1
            descr="Prüfe, dass KL15 Status == 1 (an) ist"
        )
    )

    testresult.append(["[.] Lese NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=kl15_status_var,
            nominal_status=0,
            descr="Prüfe, dass KL15 Status == 0 (aus) ist"
        )
    )

    testresult.append(["[.] Warte %ss (max. Timeoutqualifizierungszeit)"%timeout_quali_max, ""])
    time.sleep(timeout_quali_max)

    testresult.append(["[.] Prüfe Wert Waehlhebel_04:WH_Fahrstufe nachdem ClampControl_01 = 0", ""])
    hil.cl15_on__.set(0)
    testresult.append(["[.] Prüfe Waehlhebel_04:WH_Fahrstufe != 15", ""])
    current_fahrstufe = wh_fahrstufe.get()
    testresult.append(
        basic_tests.contains(
            defined_values = allowed_fahrstufe,
            current_value= current_fahrstufe,
            descr="Prüfe, dass aktueller Status der Fahrstufe korrekt ist"
        )
    )
    # Prüfe alle Werte der MEssung
    # wh_fahrstufe_data = daq_data[str(wh_fahrstufe)]['data'][:]
    # verdict = 'PASSED'
    # for value in wh_fahrstufe_data:
    #     failure_count = 0
    #     if value == wh_fahrstufe_fehlerwert:
    #         failure_count += 1
    #         verdict = 'FAILED'
    # if verdict == 'FAILED':
    #     descr = "Fehlerwert wurde gesetzt (%s Messwerte)"%failure_count
    # else:
    #     descr = "Fehlerwert wurde nicht gesetzt"
    # testresult.append([descr, verdict])

    # Prüfe alle Werte der MEssung
    # kl15_status_data = daq_data[str(kl15_status_var)]['data'][:]
    # verdict = 'PASSED'
    # for value in kl15_status_data:
    #     failure_count = 0
    #     if value != 0:
    #         failure_count += 1
    #         verdict = 'FAILED'
    # if verdict == 'FAILED':
    #     descr = "[7] KL15 Status wurde geändert, nachdem ClampControl_01 Periode auf 0 gesetzt wurde (%s Messwerte)" % failure_count
    # else:
    #     descr = "[7] KL15 Status wurde nicht geändert, nachdem ClampControl_01 Periode auf 0 gesetzt wurde"
    # testresult.append([descr, verdict])

    testresult.append(["[.] Lese Fehlerspeicher aus ", ""])
    testresult.append(["\x0aPrüfe Fehlerspeicher leer ist", ""])
    testresult.append(canape_diag.checkEventMemoryEmpty())

    testresult.append(["[.] Lese NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=kl15_status_var,
            nominal_status=0,
            descr="Prüfe, dass KL15 Status == 0 (aus) ist"
        )
    )

    testresult.append(["[.] Schalte Senden von ClampControl_01 wieder an", ""])
    testresult.append(["Schalte Periode von ClampControl_01 auf %sms" %cycle_time, "INFO"])
    kl15_period.setState('an')
    hil.cl15_on__.set(1)

    testresult.append(["[+] warte 300ms", ""])
    time.sleep(.300)
    testresult.append(["[-0]", ""])

    testresult.append(["[.] Lese NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_KL15", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=kl15_status_var,
            nominal_status=1,
            descr="Prüfe, dass KL15 Status == 1 (an) ist"
        )
    )

    testresult.append(["[.] Warte 2 Sekunde, bevor DAQ Messung beendet wird", ""])
    time.sleep(2)
    testresult.append(["Stopp DAQ Measurement", "INFO"])
    daq_data = daq.stopMeasurement()
    time.sleep(0.5)

    testresult.append(["[+] DAQ Messung: KST_KL_15, WH_Fahrstufe und NM_Waehlhebel_NM_aktiv_KL15 Signals", ""])
    testresult.append(["[-0]", ""])

    # erzeuge Plot für Testreport (ohne KL15)
    plot_data = {}
    for mes in [kl15_status_var, wh_fahrstufe, KST_KL_15]:
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
