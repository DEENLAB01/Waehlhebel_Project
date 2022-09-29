# ******************************************************************************
# -*- coding: latin1 -*-
# File    : E2E.py
# Title   :E2E SiShift CRC
# Task    : Test for E2E SiShift CRC
#
# Author  : Devangbhai Patel
# Date    : 18.07.2022
# Copyright 2021 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name       | Description
# ------------------------------------------------------------------------------
# 1.0  | 20.07.2022 | Devangbhai   | initial

from _automation_wrapper_ import TestEnv
from functions_diag import HexList
from diag_identifier import identifier_dict
import functions_common
from ttk_checks import basic_tests
import functions_gearselection
import time
from time import time as t
import functions_nm
from ttk_base.values_base import meta


import os

# Instantiate test environment
testenv = TestEnv()

def checkProgrammingPrecondition(exp_content):
    """ Checks the programming precondition
    Parameters:
        exp_content - expected content as list of bytes
    Returns:
        None
    """
    # test step
    testresult.append(["[.] Programmiervorbedingungen prüfen: 0x3101 + {}"
                       .format(HexList(test_data['identifier'])),
                       ""])
    request = [0x31, 0x01] + test_data['identifier']
    result_1, len_res, response = func_nm.send_ISOx_req(requestlist="31010203", job_len= "04", msg_length=8)

    print response, "the response"
    testresult.append(response)

    testresult.append(["\xa0Auf positive Response überprüfen", ""])
    testresult.append(func_nm.checkPositiveResponse(result_1, request, 4))

    # test step
    testresult.append(["[.] Prüfe Inhalt der Response", ""])
    if exp_content:
        testresult.append(basic_tests.checkStatus(meta(len(result_1[4:]),
                                                       alias="Länge des Inhalts"),
                                                  len(exp_content),
                                                  descr="{} Element".format(len(exp_content))))
        if len(result_1[4:]) == len(exp_content):
            testresult.append(basic_tests.compare(meta(result_1[4:],
                                                       alias="Inhalt"),
                                                  "==",
                                                  meta(exp_content,
                                                       alias="Erwarteter Inhalt"),
                                                  descr="Inhalt der Response"))
        else:
            testresult.append(['Inhalt der Response kann nicht verglichen werden.', 'FAILED'])
    else:
        testresult.append(basic_tests.checkStatus(meta(len(result_1[4:]),
                                                       alias="Länge des Inhalts"),
                                                  0,
                                                  descr="Kein Inhalt - Liste leer"))



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
    test_data = identifier_dict['Check Programming Preconditions']
    exp_wrong_prec = [0xA7]



    # set Testcase ID #########################################################
    testresult.setTestcaseId("TestSpec_XXX")

    # TEST PRE CONDITIONS #####################################################
    testresult.append(["[#0] Test Vorbedingungen", ""])
    testresult.append(["[+] Starte ECU (KL30 an, KL15 an)", ""])
    WH_Sends_data = False
    nm_timestamp = hil.NM_Waehlhebel__timestamp.get()
    # start_timestamp = nm_timestamp.get()
    hil.OTAMC_D_01__VehicleProtectedEnvironment_D__value.set(1)
    hil.ORU_01__ORU_Status__value.set(0)
    hil.ORU_Control_A_01__OnlineRemoteUpdateControlA__value.set(0)
    hil.ORU_Control_D_01__OnlineRemoteUpdateControlD__value.set(0)



    hil.cl30_on__.set(1)
    hil.cl15_on__.set(1)
    hil.ClampControl_01__KST_KL_15__value.set(1)

    t_out = 25 + t()
    while t_out > t():
        curr_timestamp = hil.NM_Waehlhebel__timestamp.get()
        if nm_timestamp != curr_timestamp:
            WH_Sends_data = True
            break
    time.sleep(0.3)
    # func_nm.crc_trigger(mesage, 2, cycletime=20)

    # result_1, len_res, hex_l = func_nm.send_ISOx_req(requestlist="31010203", job_len="04", msg_length=8)

    # print hex_l , "HEX LIST"
    # time.sleep(1)
    # checkProgrammingPrecondition(exp_content=[0x00, 0x00, 0x00])

    # result =func_nm.readDiagSession()
    # testresult.append(result)
    testresult.append(func_nm.checkEventMemoryEmpty())





finally:
    # #########################################################################
    testenv.breakdown(ecu_shutdown=True)


