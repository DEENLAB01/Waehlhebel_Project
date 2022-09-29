# ******************************************************************************
# -*- coding: latin1 -*-
# File    : KL15_AUS_Wechsel_In_NonDefaultSession.py
# Title   : KL15_AUS_Wechsel_In_NonDefaultSession
# Task    : KL15 AUS Wechsel In Non Default Session
#
# Author  : Mohammed Abdul Karim
# Date    : 17.01.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name         | Description
# ------------------------------------------------------------------------------
# 1.0  | 17.01.2022 | Mohammed  | initial
# 1.1  | 04.02.2022 | Mohammed | Added Fehler ID
# 1.2  | 17.03.2022 | Devangbhai  | Rework according to Test specification changed
# 1.3  | 30.03.2022 | Devangbhai  | Added NM cycle time evaluation methode, changed the test step 11.1 and 12


# ******************************************************************************
#
# Imports #####################################################################
from _automation_wrapper_ import TestEnv
from ttk_checks import basic_tests
import time
from ttk_daq import eval_signal
from functions_nm import _checkStatus
from time import time as t


def check_cycletime(sec, application_msg=True, nm_msg=False):
    Waehlhebel_04__timestamp_list = []
    DS_Waehlhebel__timestamp_list = []
    KN_Waehlhebel__timestamp_list = []
    NM_Waehlhebel__timestamp_list = []

    timeout = sec + t()
    while timeout > t():
        timestamp_Waehlhebel_04 = hil.Waehlhebel_04__timestamp.get()
        timestamp_DS_Waehlhebel = hil.DS_Waehlhebel__timestamp.get()
        timestamp_KN_Waehlhebel = hil.KN_Waehlhebel__timestamp.get()
        timestamp_NM_Waehlhebel = hil.NM_Waehlhebel__timestamp.get()

        if len(Waehlhebel_04__timestamp_list) == 0 or Waehlhebel_04__timestamp_list[-1] != timestamp_Waehlhebel_04:
            Waehlhebel_04__timestamp_list.append(timestamp_Waehlhebel_04)
        elif len(DS_Waehlhebel__timestamp_list) == 0 or DS_Waehlhebel__timestamp_list[-1] != timestamp_DS_Waehlhebel:
            DS_Waehlhebel__timestamp_list.append(timestamp_DS_Waehlhebel)
        elif len(KN_Waehlhebel__timestamp_list) == 0 or KN_Waehlhebel__timestamp_list[-1] != timestamp_KN_Waehlhebel:
            KN_Waehlhebel__timestamp_list.append(timestamp_KN_Waehlhebel)
        elif len(NM_Waehlhebel__timestamp_list) == 0 or NM_Waehlhebel__timestamp_list[-1] != timestamp_NM_Waehlhebel:
            NM_Waehlhebel__timestamp_list.append(timestamp_NM_Waehlhebel)

    new_sec = sec * 1000
    Waehlhebel_04__timestamp = 10
    DS_Waehlhebel__timestamp = 1000
    KN_Waehlhebel__timestamp = 500
    NM_Waehlhebel_timestamp = 200

    testresult.append(basic_tests.checkRange((len(Waehlhebel_04__timestamp_list)) if application_msg else (len(Waehlhebel_04__timestamp_list) - 1), ((new_sec / Waehlhebel_04__timestamp) - 5) if application_msg else 0, ((new_sec / Waehlhebel_04__timestamp) + 5) if application_msg else 0, "Prüfen, ob die Applikation Botschaft Waehlhebel_04 mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (Waehlhebel_04__timestamp, sec) if application_msg else "Prüfen, ob die Waehlhebel_04 Botschaft nicht gesendet wird."))
    testresult.append(basic_tests.checkRange((len(DS_Waehlhebel__timestamp_list)) if application_msg else (len(DS_Waehlhebel__timestamp_list) - 1), ((new_sec / DS_Waehlhebel__timestamp) - 2) if application_msg else 0, ((new_sec / DS_Waehlhebel__timestamp) + 2) if application_msg else 0, "Prüfen, ob die Applikation Botschaft DS_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % ( DS_Waehlhebel__timestamp, sec)if application_msg else "Prüfen, ob die DS_Waehlhebel Botschaft nicht gesendet wird."))
    testresult.append(basic_tests.checkRange((len(KN_Waehlhebel__timestamp_list)) if application_msg else (len(KN_Waehlhebel__timestamp_list) - 1), ((new_sec / KN_Waehlhebel__timestamp) - 2) if application_msg else 0,((new_sec / KN_Waehlhebel__timestamp) + 2) if application_msg else 0, "Prüfen, ob die Applikation Botschaft KN_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % ( KN_Waehlhebel__timestamp, sec)if application_msg else "Prüfen, ob die KN_Waehlhebel Botschaft nicht gesendet wird."))
    testresult.append(basic_tests.checkRange((len(NM_Waehlhebel__timestamp_list)) if nm_msg else (len(NM_Waehlhebel__timestamp_list) - 1), ((new_sec / NM_Waehlhebel_timestamp) - 2) if nm_msg else 0, ((new_sec / NM_Waehlhebel_timestamp) + 2) if nm_msg else 0, "Prüfen, ob die Applikation Botschaft NM_Waehlhebel mit dem Zeitzyklus von  %s ms in %s Sekunden gesendet wird." % (NM_Waehlhebel_timestamp, sec) if nm_msg else "Prüfen, ob die Applikation Botschaft NM_Waehlhebel nicht  gesendet wird." ))

# Instantiate test environment
testenv = TestEnv()
hil = testenv.getHil()

try:
    # #########################################################################
    # Testenv #################################################################
    testenv.setup()
    testresult = testenv.getResults()

    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_314")

    # Initialize functions ####################################################
    hil = testenv.getHil()
    daq = testenv.getGammaDAQ()

    # Initialize variables ####################################################
    nm_Waehlhebel_Diag = hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value

    meas_vars = [nm_Waehlhebel_Diag]

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Schalte KL30 und KL15 ein", ""])
    testenv.startupECU()
    canape_diag = testenv.getCanapeDiagnostic()
    testresult.append(["[.] Deaktiviere Tester Present", ""])
    canape_diag.disableTesterPresent()

    # TEST PROCESS ############################################################
    testresult.append(["[-] Starte Testprozess: %s" % testenv.script_name.split('.py')[0], ""])
    daq.startMeasurement(meas_vars)
    time.sleep(1)

    # test step 1
    testresult.append(["\x0a1. KL15 ausschalten", ""])
    #hil.cl15_on__.set(0)
    hil.ClampControl_01__KST_KL_15__value.set(0)
    # 2. Auslesen der Active Diagnostic Session: 0x22F186
    testresult.append(["\x0a2. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 3
    testresult.append(["\x0a3 Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )
    # test step 4
    testresult.append(["\x0a4. Wechsel in DefaultSession: 0x1001", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('default'))

    # test step 5
    testresult.append(["\x0a5. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('default'))

    # test step 6
    testresult.append(["\x0a6. Warte 2 Sekunde", ""])
    time.sleep(2.0)

    # test step 7
    testresult.append(["\x0a7. Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )

    # test step 8
    testresult.append(["\x0a8. Wechsel in Extended Session: 0x1003 (NonDefaultSession)", ""])
    testresult.extend(canape_diag.changeAndCheckDiagSession('extended'))

    # test step 9
    testresult.append(["\x0a9. Auslesen der Active Diagnostic Session: 0x22F186", ""])
    testresult.extend(canape_diag.checkDiagSession('extended'))

    # test step 10
    testresult.append(["\x0a10. Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag", ""])
    testresult.append(
        basic_tests.checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
            nominal_status=1,
            descr="Prüfe, dass Wert 1 ist",
        )
    )

    # test step 11
    testresult.append(["\x0a11. Warte 15 Sekunde", ""])
    time.sleep(15.0)

    testresult.append(["\x0a11.1  Prüfe 5s lang, dass NM Botschaft nicht gesendet wird. Es werden nur applikation Botschaft gesendet.", ""])
    check_cycletime(5, application_msg=True, nm_msg=False)

    # 12
    testresult.append(["\x0a12. Prüfen ob der zuletzt gesendete Wert des Signals NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag = 1 ist. ", ""])
    testresult.append(
        _checkStatus(
            current_status=hil.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value,
            nominal_status=1,
            descr="Prüfe NM_Waehlhebel:NM_Waehlhebel_NM_aktiv_Diag__value = 1 (zuletzt gesendete Wert) ist", ticket_id='FehlerId:EGA-PRM-141',
        )
    )

    testresult.append(["\x0a Stoppe  DAQ Measurement", ""])
    daq_data = daq.stopMeasurement()
    time.sleep(1)
    testresult.append(["\nStart Analyse of DAQ Measurement", ""])
    plot_data = {}
    for mes in [nm_Waehlhebel_Diag]:
        plot_data[str(mes)] = daq_data[str(mes)]
    testresult.append(
        daq.plotMultiShot(plot_data, str(testenv.script_name.split('.py')[0])))

    # TEST POST CONDITIONS ####################################################
    testresult.append(["[#0] Test Nachbedingungen", ""])
    testresult.append(["[+] ECU ausschalten", ""])
    testenv.shutdownECU()


finally:
    # #########################################################################
    testenv.breakdown()
    del (testenv)
    # #########################################################################

print "Done."
