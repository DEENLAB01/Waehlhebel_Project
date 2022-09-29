#******************************************************************************
# -*- coding: latin1 -*-
# File    : InterneMessung_KL30Spannung_36.py
# Task    : A minimal "InterneMessung_KL30Spannung!" test script
#
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name     | Description
#------------------------------------------------------------------------------
# 1.0  | 12.02.2021 | Abdul Karim  | initial
#******************************************************************************
import time
import canapeapi
from ttk_tools.vector.canapeapi import CANapeDevice
from ttk_bus import bus_signals_base
from _automation_wrapper_ import TestEnv
testenv = TestEnv()
from ttk_checks import basic_tests
##
from ttk_bus.bus_signals_base import RxBusSignal, TxBusSignal, BusSignalContainer

class BusSignals(BusSignalContainer):
    def __init__(self, tool_ref=None):
        BusSignalContainer.__init__(self, tool_ref)
        self.tx_sig = TxBusSignal(self, self,
                                       "$EcuUserData_XIX_HCP1_CANFD02$RawADCSensor2Val_XIX_EcuUserData_XIX_HCP1_CANFD02",
                                        descr="RawADCKL30Val", unit="V" )
        self.tx_sig = RxBusSignal(self,
                                       "$EcuUserData_XIX_HCP1_CANFD02$RawADCSensor1Val_XIX_EcuUserData_XIX_HCP1_CANFD02",
                                       unit="", descr="RawADCSensor2Val")
        self.RawADCSensor1Val = TxBusSignal(self,
                                       "$EcuUserData_XIX_HCP1_CANFD02$RawADCSensor2Val_XIX_EcuUserData_XIX_HCP1_CANFD02",
                                       unit=" ",  descr="RawADCKL30Val")
        self.RawADCSensor2Val = TxBusSignal(self,
                                       "$EcuUserData_XIX_HCP1_CANFD02$RawADCSensor1Val_XIX_EcuUserData_XIX_HCP1_CANFD02",
                                       unit="", descr="RawADCSensor2Val")
        self.ResetCounterFlag = TxBusSignal(self,
                                       "$EcuUserData_XIX_HCP1_CANFD02$ResetCounterFlag_XIX_EcuUserData_XIX_HCP1_CANFD02",
                                       unit=" ", descr="ResetCounterFlag")
        self.SwVersion = TxBusSignal(self, "$SwVersion_XIX_HCP1_CANFD02$SwVersion_XIX_HCP1_CANFD02", unit=" ",
                                descr="SwVersion")
        self.SiShift_StLghtDrvPosn = RxBusSignal(self,
                                            "$SiShift_01_E2E_XIX_HCP1_CANFD02$SIShift_StLghtDrvPosn_XIX_SiShift_01_XIX_HCP1_CANFD02",
                                            unit=" ", descr="SwVersion")
        self.SiShift_FlgStrtNeutHldPha = RxBusSignal(self,
                                                "$SiShift_01_E2E_XIX_HCP1_CANFD02$SIShift_FlgStrtNeutHldPha_XIX_SiShift_01_XIX_HCP1_CANFD02",
                                                unit=" ",
                                                descr="SwVersion")
try:
##
    testenv.setup()
    #testresult = testenv.getResults()
    testresult = []
    hil = testenv.getHil()

    testenv.startupECU()
    daq = testenv.getCanapeDAQ()
    cal = testenv.getCal()
#    bus = BusSignalContainer()
    time.sleep(.200)
    canape = testenv.getCanapeCan()
#    testresult.append((TxBusSignal._bus_signals_base.TxBusSignal.get()))
    testresult.append(TxBusSignal.BusSignal(
        cal.RawADCSensor1Val,
        set_value=100,
        set_value_descr="Some test value",
        check_var_list=[
            {"var": cal.RawADCSensor1Val, "value": 1300, "abs_pos": 1, "abs_neg": -.1},

        ],
        descr="This is the supplied testRxSignal description text"
    ))
    ## Cleanup
    #hil=None
    cal=None

finally:
    # #########################################################################
    testenv.breakdown()
    # #########################################################################

