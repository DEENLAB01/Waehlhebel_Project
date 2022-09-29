# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : can_bus_variables.py
# Task    : Container for can bus variables (here: Gamma model variables)
#           to change manipulate and control CAN bus simulation.
#
# Author  : M.A.Muahtaq
# Date    : 20.08.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name        | Description
# ------------------------------------------------------------------------------
# 1.0  | 20.08.2021 | M.A.Mushtaq | initial
# 1.1  | 07.09.2021 | M. Mushtaq  | updated with new K-Matrix
# ------------------------------------------------------------------------------

# ******************************************************************************

# =============================================================================
# IMPORTANT:
# self.tx_sig... = signal from Gamma to ECU,  class: RxCanBusSignal
# self.rx_sig... = signal from ECU to Gamma,  class TxCanSignal
#
# NOTE: name tx_sig/rx_sig is according to .arxml file and bussystems path

# =============================================================================

### base import ###############################################################
# > base class
# > add all messages and signals and generate instance of it
from ttk_bus.bus_signals_cangamma import CanBusSignalContainer

### message and signal class import ###########################################
# TODO: in project generate a derived class in case of customer solution
# > also it can be usefull for the project to generate solutions here
# > most of the time some parameters can get a base definition
from ttk_bus.bus_signals_cangamma import RxCanBusMessage as DefaultRxCanBusMessage
from ttk_bus.bus_signals_cangamma import TxCanBusMessage
from ttk_bus.bus_signals_cangamma import RxCanBusSignal, TxCanBusSignal


class RxCanBusMessage(DefaultRxCanBusMessage):
    def __init__(self, context, bus_systems_path, cycle_time=None, debounce_time=None,
                 alias="", descr=""):
        """ Rx CAN Message/PDU data (HIL-Tx => ECU-Rx).
            Parameters:
                context           - parent context (an RTE application instance to
                                                    resolve signal/variable paths)
                enable_path       - manual path to a tx enable switch. Keep at None
                                    to use default enable switch below BusSystems
                                    (see parameter bus_systems_path).
                                    The enable variable will later be set to 1
                                    to enable or to 0 to disable message
                                    transmisssion.
                bus_systems_path  - base path to PDU/message below BusSystems,
                                    use
                                    "BusSystems/CAN/<CAN_NAME>/<MSG_NAME>/TX/<MSG_NAME>
                                    "
                                    or
                                    "BusSystems/CAN/<CAN_NAME>/<MSG_NAME>/TX/<MSG_NAME>
                                     _Enable"
                                    Helper entries will be derived from this path,
                                    e.g. kickout or status variables (though this is more
                                    relevant to messages sent to DUT, see RxCanBusMessage)
                cycle_time        - cycle time in [ms]. Event-triggered messages
                                    have a cycle time of 0 (similar to DBC value)
                debounce_time     - minimum debounce delay between events in [ms]
                alias             - Message alias/name
                descr             - (opt) Message description (may be used in report
                                          entries)
                change_delay      - (opt) delay to wait after a value change [ms],
                                          defaults to 2x max(cycle_time, debounce_time)
                timeout           - (opt) detection time for timeout errors [ms],
                                          defaults to 2x max(cycle_time, debounce_time)
                recovery_time     - (opt) time for recovery/"wiedergut" checks [ms],
                                          defaults to 2x max(cycle_time, debounce_time)
            """
        DefaultRxCanBusMessage.__init__(
            self,
            context=context, base_identifier=bus_systems_path,
            cycle_time=cycle_time, debounce_time=debounce_time, alias=alias, descr=descr,
            # change_delay, timeout, recovery_time
        )


class CanBusSignals(CanBusSignalContainer):
    """ A BusSignalContainer for CAN Bus Signals """

    def __init__(self, app):
        CanBusSignalContainer.__init__(self, app)

        # DS_Waehlhebel # ==================================================
        self.rx_mesg_DS_Waehlhebel = RxCanBusMessage(app, None, 1000, alias="DS_Waehlhebel", descr="")
        self.DS_Waehlhebel__DS_Waehlhebel_Lokalaktiv__value = RxCanBusSignal(app,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_Lokalaktiv.value",
                                                                             self.rx_mesg_DS_Waehlhebel,
                                                                             alias="DS_Waehlhebel_Lokalaktiv", descr="")
        self.DS_Waehlhebel__DS_Waehlhebel_StMemChanged__value = RxCanBusSignal(app,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_StMemChanged.value",
                                                                               self.rx_mesg_DS_Waehlhebel,
                                                                               alias="DS_Waehlhebel_StMemChanged",
                                                                               descr="")
        self.DS_Waehlhebel__DS_Waehlhebel_DiagAdr__value = RxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_DiagAdr.value",
                                                                          self.rx_mesg_DS_Waehlhebel,
                                                                          alias="DS_Waehlhebel_DiagAdr", descr="")
        self.DS_Waehlhebel__DS_Waehlhebel_IdentValid__value = RxCanBusSignal(app,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_IdentValid.value",
                                                                             self.rx_mesg_DS_Waehlhebel,
                                                                             alias="DS_Waehlhebel_IdentValid", descr="")
        self.DS_Waehlhebel__DS_Waehlhebel_MemSelChanged__value = RxCanBusSignal(app,
                                                                                "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_MemSelChanged.value",
                                                                                self.rx_mesg_DS_Waehlhebel,
                                                                                alias="DS_Waehlhebel_MemSelChanged",
                                                                                descr="")
        self.DS_Waehlhebel__DS_Waehlhebel_MemSel10Changed__value = RxCanBusSignal(app,
                                                                                  "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_MemSel10Changed.value",
                                                                                  self.rx_mesg_DS_Waehlhebel,
                                                                                  alias="DS_Waehlhebel_MemSel10Changed",
                                                                                  descr="")
        self.DS_Waehlhebel__DS_Waehlhebel_ConfDTCChanged__value = RxCanBusSignal(app,
                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_ConfDTCChanged.value",
                                                                                 self.rx_mesg_DS_Waehlhebel,
                                                                                 alias="DS_Waehlhebel_ConfDTCChanged",
                                                                                 descr="")
        self.DS_Waehlhebel__DS_Waehlhebel_TestFailedChanged__value = RxCanBusSignal(app,
                                                                                    "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_TestFailedChanged.value",
                                                                                    self.rx_mesg_DS_Waehlhebel,
                                                                                    alias="DS_Waehlhebel_TestFailedChanged",
                                                                                    descr="")
        self.DS_Waehlhebel__DS_Waehlhebel_WIRChanged__value = RxCanBusSignal(app,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_WIRChanged.value",
                                                                             self.rx_mesg_DS_Waehlhebel,
                                                                             alias="DS_Waehlhebel_WIRChanged", descr="")
        self.DS_Waehlhebel__DS_Waehlhebel_Subsystemaktiv__value = RxCanBusSignal(app,
                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_Subsystemaktiv.value",
                                                                                 self.rx_mesg_DS_Waehlhebel,
                                                                                 alias="DS_Waehlhebel_Subsystemaktiv",
                                                                                 descr="")

        # KN_Waehlhebel # ==================================================
        self.rx_mesg_KN_Waehlhebel = RxCanBusMessage(app, None, 500, alias="KN_Waehlhebel", descr="")
        self.KN_Waehlhebel__KN_Waehlhebel_DiagPfad__value = RxCanBusSignal(app,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.KN_Waehlhebel_DiagPfad.value",
                                                                           self.rx_mesg_KN_Waehlhebel,
                                                                           alias="KN_Waehlhebel_DiagPfad", descr="")
        self.KN_Waehlhebel__Waehlhebel_Nachlauftyp__value = RxCanBusSignal(app,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.Waehlhebel_Nachlauftyp.value",
                                                                           self.rx_mesg_KN_Waehlhebel,
                                                                           alias="Waehlhebel_Nachlauftyp", descr="")
        self.KN_Waehlhebel__Waehlhebel_SNI_10__value = RxCanBusSignal(app,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.Waehlhebel_SNI_10.value",
                                                                      self.rx_mesg_KN_Waehlhebel,
                                                                      alias="Waehlhebel_SNI_10", descr="")
        self.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value = RxCanBusSignal(app,
                                                                                   "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.KN_Waehlhebel_ECUKnockOutTimer.value",
                                                                                   self.rx_mesg_KN_Waehlhebel,
                                                                                   alias="KN_Waehlhebel_ECUKnockOutTimer",
                                                                                   descr="")
        self.KN_Waehlhebel__Waehlhebel_KD_Fehler__value = RxCanBusSignal(app,
                                                                         "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.Waehlhebel_KD_Fehler.value",
                                                                         self.rx_mesg_KN_Waehlhebel,
                                                                         alias="Waehlhebel_KD_Fehler", descr="")
        self.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value = RxCanBusSignal(app,
                                                                              "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.KN_Waehlhebel_ECUKnockOut.value",
                                                                              self.rx_mesg_KN_Waehlhebel,
                                                                              alias="KN_Waehlhebel_ECUKnockOut",
                                                                              descr="")
        self.KN_Waehlhebel__NM_Waehlhebel_Lokalaktiv__value = RxCanBusSignal(app,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.NM_Waehlhebel_Lokalaktiv.value",
                                                                             self.rx_mesg_KN_Waehlhebel,
                                                                             alias="NM_Waehlhebel_Lokalaktiv", descr="")
        self.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value = RxCanBusSignal(app,
                                                                              "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.KN_Waehlhebel_BusKnockOut.value",
                                                                              self.rx_mesg_KN_Waehlhebel,
                                                                              alias="KN_Waehlhebel_BusKnockOut",
                                                                              descr="")
        self.KN_Waehlhebel__NM_Waehlhebel_Subsystemaktiv__value = RxCanBusSignal(app,
                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.NM_Waehlhebel_Subsystemaktiv.value",
                                                                                 self.rx_mesg_KN_Waehlhebel,
                                                                                 alias="NM_Waehlhebel_Subsystemaktiv",
                                                                                 descr="")
        self.KN_Waehlhebel__Waehlhebel_Transport_Mode__value = RxCanBusSignal(app,
                                                                              "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.Waehlhebel_Transport_Mode.value",
                                                                              self.rx_mesg_KN_Waehlhebel,
                                                                              alias="Waehlhebel_Transport_Mode",
                                                                              descr="")
        self.KN_Waehlhebel__NM_Waehlhebel_FCIB__value = RxCanBusSignal(app,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.NM_Waehlhebel_FCIB.value",
                                                                       self.rx_mesg_KN_Waehlhebel,
                                                                       alias="NM_Waehlhebel_FCIB", descr="")
        self.KN_Waehlhebel__Waehlhebel_KompSchutz__value = RxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.Waehlhebel_KompSchutz.value",
                                                                          self.rx_mesg_KN_Waehlhebel,
                                                                          alias="Waehlhebel_KompSchutz", descr="")
        self.KN_Waehlhebel__Waehlhebel_Abschaltstufe__value = RxCanBusSignal(app,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.Waehlhebel_Abschaltstufe.value",
                                                                             self.rx_mesg_KN_Waehlhebel,
                                                                             alias="Waehlhebel_Abschaltstufe", descr="")
        self.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value = RxCanBusSignal(app,
                                                                                   "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.KN_Waehlhebel_BusKnockOutTimer.value",
                                                                                   self.rx_mesg_KN_Waehlhebel,
                                                                                   alias="KN_Waehlhebel_BusKnockOutTimer",
                                                                                   descr="")

        # NM_Waehlhebel # ==================================================
        self.rx_mesg_NM_Waehlhebel = RxCanBusMessage(app, None, 0, alias="NM_Waehlhebel", descr="")
        self.NM_Waehlhebel__NM_Waehlhebel_FCAB__value = RxCanBusSignal(app,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_FCAB.value",
                                                                       self.rx_mesg_NM_Waehlhebel,
                                                                       alias="NM_Waehlhebel_FCAB", descr="")
        self.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value = RxCanBusSignal(app,
                                                                         "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_UDS_CC.value",
                                                                         self.rx_mesg_NM_Waehlhebel,
                                                                         alias="NM_Waehlhebel_UDS_CC", descr="")
        self.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value = RxCanBusSignal(app,
                                                                                     "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Aktiv_N_Haltephase_abgelaufen.value",
                                                                                     self.rx_mesg_NM_Waehlhebel,
                                                                                     alias="NM_Aktiv_N_Haltephase_abgelaufen",
                                                                                     descr="")
        self.NM_Waehlhebel__NM_Waehlhebel_NM_State__value = RxCanBusSignal(app,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_NM_State.value",
                                                                           self.rx_mesg_NM_Waehlhebel,
                                                                           alias="NM_Waehlhebel_NM_State", descr="")
        self.NM_Waehlhebel__NM_Waehlhebel_SNI_10__value = RxCanBusSignal(app,
                                                                         "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_SNI_10.value",
                                                                         self.rx_mesg_NM_Waehlhebel,
                                                                         alias="NM_Waehlhebel_SNI_10", descr="")
        self.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value = RxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_CBV_AWB.value",
                                                                          self.rx_mesg_NM_Waehlhebel,
                                                                          alias="NM_Waehlhebel_CBV_AWB", descr="")
        self.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value = RxCanBusSignal(app,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_Wakeup_V12.value",
                                                                             self.rx_mesg_NM_Waehlhebel,
                                                                             alias="NM_Waehlhebel_Wakeup_V12", descr="")
        self.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value = RxCanBusSignal(app,
                                                                                "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_NM_aktiv_KL15.value",
                                                                                self.rx_mesg_NM_Waehlhebel,
                                                                                alias="NM_Waehlhebel_NM_aktiv_KL15",
                                                                                descr="")
        self.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value = RxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_CBV_CRI.value",
                                                                          self.rx_mesg_NM_Waehlhebel,
                                                                          alias="NM_Waehlhebel_CBV_CRI", descr="")
        self.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value = RxCanBusSignal(app,
                                                                                "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_NM_aktiv_Tmin.value",
                                                                                self.rx_mesg_NM_Waehlhebel,
                                                                                alias="NM_Waehlhebel_NM_aktiv_Tmin",
                                                                                descr="")
        self.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value = RxCanBusSignal(app,
                                                                                "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_NM_aktiv_Diag.value",
                                                                                self.rx_mesg_NM_Waehlhebel,
                                                                                alias="NM_Waehlhebel_NM_aktiv_Diag",
                                                                                descr="")

        # DIA_SAAM_Resp # ==================================================
        self.rx_mesg_DIA_SAAM_Resp = RxCanBusMessage(app, None, 0, alias="DIA_SAAM_Resp", descr="")
        self.DIA_SAAM_Resp__DIA_SAAM_Resp__value = RxCanBusSignal(app,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_RX.DIA_SAAM_Resp.signals.DIA_SAAM_Resp.value",
                                                                  self.rx_mesg_DIA_SAAM_Resp, alias="DIA_SAAM_Resp",
                                                                  descr="")

        # DEV_Waehlhebel_Req_00 # ==================================================
        self.rx_mesg_DEV_Waehlhebel_Req_00 = RxCanBusMessage(app, None, 0, alias="DEV_Waehlhebel_Req_00", descr="")
        self.DEV_Waehlhebel_Req_00__DEV_Waehlhebel_Req_00_Data__value = RxCanBusSignal(app,
                                                                                       "Waehlhebel:CAN.can0_HIL.HIL_RX.DEV_Waehlhebel_Req_00.signals.DEV_Waehlhebel_Req_00_Data.value",
                                                                                       self.rx_mesg_DEV_Waehlhebel_Req_00,
                                                                                       alias="DEV_Waehlhebel_Req_00_Data",
                                                                                       descr="")

        # DEV_Waehlhebel_Resp_FF # ==================================================
        self.rx_mesg_DEV_Waehlhebel_Resp_FF = RxCanBusMessage(app, None, 0, alias="DEV_Waehlhebel_Resp_FF", descr="")
        self.DEV_Waehlhebel_Resp_FF__DEV_Waehlhebel_Resp_FF_Data__value = RxCanBusSignal(app,
                                                                                         "Waehlhebel:CAN.can0_HIL.HIL_RX.DEV_Waehlhebel_Resp_FF.signals.DEV_Waehlhebel_Resp_FF_Data.value",
                                                                                         self.rx_mesg_DEV_Waehlhebel_Resp_FF,
                                                                                         alias="DEV_Waehlhebel_Resp_FF_Data",
                                                                                         descr="")

        # OBDC_Waehlhebel_Resp_FD # ==================================================
        self.rx_mesg_OBDC_Waehlhebel_Resp_FD = RxCanBusMessage(app, None, 0, alias="OBDC_Waehlhebel_Resp_FD", descr="")
        self.OBDC_Waehlhebel_Resp_FD__OBDC_Waehlhebel_Resp_FD_Data__value = RxCanBusSignal(app,
                                                                                           "Waehlhebel:CAN.can0_HIL.HIL_RX.OBDC_Waehlhebel_Resp_FD.signals.OBDC_Waehlhebel_Resp_FD_Data.value",
                                                                                           self.rx_mesg_OBDC_Waehlhebel_Resp_FD,
                                                                                           alias="OBDC_Waehlhebel_Resp_FD_Data",
                                                                                           descr="")

        # Waehlhebel_04 # ==================================================
        self.rx_mesg_Waehlhebel_04 = RxCanBusMessage(app, None, 10, alias="Waehlhebel_04", descr="")
        self.Waehlhebel_04__Waehlhebel_04_CRC__value = RxCanBusSignal(app,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.Waehlhebel_04_CRC.value",
                                                                      self.rx_mesg_Waehlhebel_04,
                                                                      alias="Waehlhebel_04_CRC", descr="")
        self.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value = RxCanBusSignal(app,
                                                                              "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.WH_Zustand_N_Haltephase_2.value",
                                                                              self.rx_mesg_Waehlhebel_04,
                                                                              alias="WH_Zustand_N_Haltephase_2",
                                                                              descr="")
        self.Waehlhebel_04__Waehlhebel_04_BZ__value = RxCanBusSignal(app,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.Waehlhebel_04_BZ.value",
                                                                     self.rx_mesg_Waehlhebel_04,
                                                                     alias="Waehlhebel_04_BZ", descr="")
        self.Waehlhebel_04__WH_SensorPos_roh__value = RxCanBusSignal(app,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.WH_SensorPos_roh.value",
                                                                     self.rx_mesg_Waehlhebel_04,
                                                                     alias="WH_SensorPos_roh", descr="")
        self.Waehlhebel_04__WH_P_Taste__value = RxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.WH_P_Taste.value",
                                                               self.rx_mesg_Waehlhebel_04, alias="WH_P_Taste", descr="")
        self.Waehlhebel_04__WH_Fahrstufe__value = RxCanBusSignal(app,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.WH_Fahrstufe.value",
                                                                 self.rx_mesg_Waehlhebel_04, alias="WH_Fahrstufe",
                                                                 descr="")
        self.Waehlhebel_04__WH_Zustand_N_Haltephase__value = RxCanBusSignal(app,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.WH_Zustand_N_Haltephase.value",
                                                                            self.rx_mesg_Waehlhebel_04,
                                                                            alias="WH_Zustand_N_Haltephase", descr="")
        self.Waehlhebel_04__WH_Entsperrtaste_02__value = RxCanBusSignal(app,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.WH_Entsperrtaste_02.value",
                                                                        self.rx_mesg_Waehlhebel_04,
                                                                        alias="WH_Entsperrtaste_02", descr="")

        # SiShift_01 # ==================================================
        self.tx_mesg_SiShift_01 = TxCanBusMessage(app, None, 20, alias="SiShift_01", descr="")
        self.SiShift_01__SIShift_StLghtDrvPosn__value = TxCanBusSignal(app,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.SiShift_01.signals.SIShift_StLghtDrvPosn.value",
                                                                       self.tx_mesg_SiShift_01,
                                                                       alias="SIShift_StLghtDrvPosn", descr="")
        self.SiShift_01__SiShift_01_20ms_CRC__value = TxCanBusSignal(app,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.SiShift_01.signals.SiShift_01_20ms_CRC.value",
                                                                     self.tx_mesg_SiShift_01,
                                                                     alias="SiShift_01_20ms_CRC", descr="")
        self.SiShift_01__SiShift_01_20ms_BZ__value = TxCanBusSignal(app,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.SiShift_01.signals.SiShift_01_20ms_BZ.value",
                                                                    self.tx_mesg_SiShift_01, alias="SiShift_01_20ms_BZ",
                                                                    descr="")
        self.SiShift_01__SIShift_FlgStrtNeutHldPha__value = TxCanBusSignal(app,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.SiShift_01.signals.SIShift_FlgStrtNeutHldPha.value",
                                                                           self.tx_mesg_SiShift_01,
                                                                           alias="SIShift_FlgStrtNeutHldPha", descr="")

        # NVEM_12 # ==================================================
        self.tx_mesg_NVEM_12 = TxCanBusMessage(app, None, 100, alias="NVEM_12", descr="")
        self.NVEM_12__BEM_Batt_Ab__value = TxCanBusSignal(app,
                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.BEM_Batt_Ab.value",
                                                          self.tx_mesg_NVEM_12, alias="BEM_Batt_Ab", descr="")
        self.NVEM_12__NVEM_DC_iSoll_NV__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_DC_iSoll_NV.value",
                                                               self.tx_mesg_NVEM_12, alias="NVEM_DC_iSoll_NV", descr="")
        self.NVEM_12__NVEM_Last_Anf__value = TxCanBusSignal(app,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_Last_Anf.value",
                                                            self.tx_mesg_NVEM_12, alias="NVEM_Last_Anf", descr="")
        self.NVEM_12__NVEM_12_BZ__value = TxCanBusSignal(app,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_12_BZ.value",
                                                         self.tx_mesg_NVEM_12, alias="NVEM_12_BZ", descr="")
        self.NVEM_12__NVEM_DC_uMin_NV__value = TxCanBusSignal(app,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_DC_uMin_NV.value",
                                                              self.tx_mesg_NVEM_12, alias="NVEM_DC_uMin_NV", descr="")
        self.NVEM_12__NVEM_DC_uSoll_NV__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_DC_uSoll_NV.value",
                                                               self.tx_mesg_NVEM_12, alias="NVEM_DC_uSoll_NV", descr="")
        self.NVEM_12__NVEM_NV_BAT_ZellStatus_Index_Anf__value = TxCanBusSignal(app,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_NV_BAT_ZellStatus_Index_Anf.value",
                                                                               self.tx_mesg_NVEM_12,
                                                                               alias="NVEM_NV_BAT_ZellStatus_Index_Anf",
                                                                               descr="")
        self.NVEM_12__NVEM_Verbraucher_Information__value = TxCanBusSignal(app,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_Verbraucher_Information.value",
                                                                           self.tx_mesg_NVEM_12,
                                                                           alias="NVEM_Verbraucher_Information",
                                                                           descr="")
        self.NVEM_12__NVEM_12_CRC__value = TxCanBusSignal(app,
                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_12_CRC.value",
                                                          self.tx_mesg_NVEM_12, alias="NVEM_12_CRC", descr="")
        self.NVEM_12__BEM_STH_Einschaltverbot__value = TxCanBusSignal(app,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.BEM_STH_Einschaltverbot.value",
                                                                      self.tx_mesg_NVEM_12,
                                                                      alias="BEM_STH_Einschaltverbot", descr="")
        self.NVEM_12__BEM_Red_Innengeblaese__value = TxCanBusSignal(app,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.BEM_Red_Innengeblaese.value",
                                                                    self.tx_mesg_NVEM_12, alias="BEM_Red_Innengeblaese",
                                                                    descr="")
        self.NVEM_12__BEM_STH_Zielzeit__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.BEM_STH_Zielzeit.value",
                                                               self.tx_mesg_NVEM_12, alias="BEM_STH_Zielzeit", descr="")
        self.NVEM_12__NVEM_Bordnetzdiagnose__value = TxCanBusSignal(app,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_Bordnetzdiagnose.value",
                                                                    self.tx_mesg_NVEM_12, alias="NVEM_Bordnetzdiagnose",
                                                                    descr="")
        self.NVEM_12__BEM_HL_Regelung_Status__value = TxCanBusSignal(app,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.BEM_HL_Regelung_Status.value",
                                                                     self.tx_mesg_NVEM_12,
                                                                     alias="BEM_HL_Regelung_Status", descr="")
        self.NVEM_12__NVEM_NV_BAT_ZellStatus_Typ_Anf__value = TxCanBusSignal(app,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_NV_BAT_ZellStatus_Typ_Anf.value",
                                                                             self.tx_mesg_NVEM_12,
                                                                             alias="NVEM_NV_BAT_ZellStatus_Typ_Anf",
                                                                             descr="")
        self.NVEM_12__NVEM_MV_DC_uSollLV__value = TxCanBusSignal(app,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_MV_DC_uSollLV.value",
                                                                 self.tx_mesg_NVEM_12, alias="NVEM_MV_DC_uSollLV",
                                                                 descr="")
        self.NVEM_12__NVEM_MV_DC_uMinLV__value = TxCanBusSignal(app,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_MV_DC_uMinLV.value",
                                                                self.tx_mesg_NVEM_12, alias="NVEM_MV_DC_uMinLV",
                                                                descr="")
        self.NVEM_12__BEM_Generatordiagnose__value = TxCanBusSignal(app,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.BEM_Generatordiagnose.value",
                                                                    self.tx_mesg_NVEM_12, alias="BEM_Generatordiagnose",
                                                                    descr="")
        self.NVEM_12__NVEM_Abschaltstufe__value = TxCanBusSignal(app,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_Abschaltstufe.value",
                                                                 self.tx_mesg_NVEM_12, alias="NVEM_Abschaltstufe",
                                                                 descr="")
        self.NVEM_12__NVEM_Freigabe_OTA__value = TxCanBusSignal(app,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_Freigabe_OTA.value",
                                                                self.tx_mesg_NVEM_12, alias="NVEM_Freigabe_OTA",
                                                                descr="")
        self.NVEM_12__NVEM_Bordnetz_Information__value = TxCanBusSignal(app,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_Bordnetz_Information.value",
                                                                        self.tx_mesg_NVEM_12,
                                                                        alias="NVEM_Bordnetz_Information", descr="")
        self.NVEM_12__NVEM_MV_DC_iSoll_NV__value = TxCanBusSignal(app,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_MV_DC_iSoll_NV.value",
                                                                  self.tx_mesg_NVEM_12, alias="NVEM_MV_DC_iSoll_NV",
                                                                  descr="")

        # DPM_01 # ==================================================
        self.tx_mesg_DPM_01 = TxCanBusMessage(app, None, 20, alias="DPM_01", descr="")
        self.DPM_01__DPM_StTarDrvPosn__value = TxCanBusSignal(app,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_StTarDrvPosn.value",
                                                              self.tx_mesg_DPM_01, alias="DPM_StTarDrvPosn", descr="")
        self.DPM_01__DPM_StSrcTarDrvPosn__value = TxCanBusSignal(app,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_StSrcTarDrvPosn.value",
                                                                 self.tx_mesg_DPM_01, alias="DPM_StSrcTarDrvPosn",
                                                                 descr="")
        self.DPM_01__DPM_FlgStrtNeutHldPha__value = TxCanBusSignal(app,
                                                                   "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_FlgStrtNeutHldPha.value",
                                                                   self.tx_mesg_DPM_01, alias="DPM_FlgStrtNeutHldPha",
                                                                   descr="")
        self.DPM_01__DPM_01_BZ__value = TxCanBusSignal(app,
                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_01_BZ.value",
                                                       self.tx_mesg_DPM_01, alias="DPM_01_BZ", descr="")
        self.DPM_01__DPM_StReqVld_VMMscnd__value = TxCanBusSignal(app,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_StReqVld_VMMscnd.value",
                                                                  self.tx_mesg_DPM_01, alias="DPM_StReqVld_VMMscnd",
                                                                  descr="")
        self.DPM_01__DPM_01_CRC__value = TxCanBusSignal(app,
                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_01_CRC.value",
                                                        self.tx_mesg_DPM_01, alias="DPM_01_CRC", descr="")
        self.DPM_01__DPM_StLghtDrvPosn__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_StLghtDrvPosn.value",
                                                               self.tx_mesg_DPM_01, alias="DPM_StLghtDrvPosn", descr="")

        # Systeminfo_01 # ==================================================
        self.tx_mesg_Systeminfo_01 = TxCanBusMessage(app, None, 1000, alias="Systeminfo_01", descr="")
        self.Systeminfo_01__SI_T_Schutz__value = TxCanBusSignal(app,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_T_Schutz.value",
                                                                self.tx_mesg_Systeminfo_01, alias="SI_T_Schutz",
                                                                descr="")
        self.Systeminfo_01__SI_Diagnose_Aktiv__value = TxCanBusSignal(app,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_Diagnose_Aktiv.value",
                                                                      self.tx_mesg_Systeminfo_01,
                                                                      alias="SI_Diagnose_Aktiv", descr="")
        self.Systeminfo_01__SI_NWDF_30__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_NWDF_30.value",
                                                               self.tx_mesg_Systeminfo_01, alias="SI_NWDF_30", descr="")
        self.Systeminfo_01__SI_P_Mode__value = TxCanBusSignal(app,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_P_Mode.value",
                                                              self.tx_mesg_Systeminfo_01, alias="SI_P_Mode", descr="")
        self.Systeminfo_01__SI_NWDF_gueltig__value = TxCanBusSignal(app,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_NWDF_gueltig.value",
                                                                    self.tx_mesg_Systeminfo_01, alias="SI_NWDF_gueltig",
                                                                    descr="")
        self.Systeminfo_01__SI_QRS_Mode__value = TxCanBusSignal(app,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_QRS_Mode.value",
                                                                self.tx_mesg_Systeminfo_01, alias="SI_QRS_Mode",
                                                                descr="")
        self.Systeminfo_01__SI_P_Mode_gueltig__value = TxCanBusSignal(app,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_P_Mode_gueltig.value",
                                                                      self.tx_mesg_Systeminfo_01,
                                                                      alias="SI_P_Mode_gueltig", descr="")
        self.Systeminfo_01__SI_NWDF__value = TxCanBusSignal(app,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_NWDF.value",
                                                            self.tx_mesg_Systeminfo_01, alias="SI_NWDF", descr="")
        self.Systeminfo_01__SI_T_Mode__value = TxCanBusSignal(app,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_T_Mode.value",
                                                              self.tx_mesg_Systeminfo_01, alias="SI_T_Mode", descr="")

        # VDSO_05 # ==================================================
        self.tx_mesg_VDSO_05 = TxCanBusMessage(app, None, 20, alias="VDSO_05", descr="")
        self.VDSO_05__VDSO_Vx3dDisp__value = TxCanBusSignal(app,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.signals.VDSO_Vx3dDisp.value",
                                                            self.tx_mesg_VDSO_05, alias="VDSO_Vx3dDisp", descr="")
        self.VDSO_05__VDSO_05_CRC__value = TxCanBusSignal(app,
                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.signals.VDSO_05_CRC.value",
                                                          self.tx_mesg_VDSO_05, alias="VDSO_05_CRC", descr="")
        self.VDSO_05__VDSO_Vx3dKmph__value = TxCanBusSignal(app,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.signals.VDSO_Vx3dKmph.value",
                                                            self.tx_mesg_VDSO_05, alias="VDSO_Vx3dKmph", descr="")
        self.VDSO_05__VDSO_05_BZ__value = TxCanBusSignal(app,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.signals.VDSO_05_BZ.value",
                                                         self.tx_mesg_VDSO_05, alias="VDSO_05_BZ", descr="")
        self.VDSO_05__VDSO_Vx3d__value = TxCanBusSignal(app,
                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.signals.VDSO_Vx3d.value",
                                                        self.tx_mesg_VDSO_05, alias="VDSO_Vx3d", descr="")
        self.VDSO_05__VDSO_BasTi200_NumClc__value = TxCanBusSignal(app,
                                                                   "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.signals.VDSO_BasTi200_NumClc.value",
                                                                   self.tx_mesg_VDSO_05, alias="VDSO_BasTi200_NumClc",
                                                                   descr="")

        # Dimmung_01 # ==================================================
        self.tx_mesg_Dimmung_01 = TxCanBusMessage(app, None, 200, alias="Dimmung_01", descr="")
        self.Dimmung_01__DI_KL_58xd__value = TxCanBusSignal(app,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.signals.DI_KL_58xd.value",
                                                            self.tx_mesg_Dimmung_01, alias="DI_KL_58xd", descr="")
        self.Dimmung_01__DI_Fotosensor__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.signals.DI_Fotosensor.value",
                                                               self.tx_mesg_Dimmung_01, alias="DI_Fotosensor", descr="")
        self.Dimmung_01__DI_Display_Nachtdesign__value = TxCanBusSignal(app,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.signals.DI_Display_Nachtdesign.value",
                                                                        self.tx_mesg_Dimmung_01,
                                                                        alias="DI_Display_Nachtdesign", descr="")
        self.Dimmung_01__DI_KL_58xt__value = TxCanBusSignal(app,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.signals.DI_KL_58xt.value",
                                                            self.tx_mesg_Dimmung_01, alias="DI_KL_58xt", descr="")
        self.Dimmung_01__BCM1_Stellgroesse_Kl_58s__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.signals.BCM1_Stellgroesse_Kl_58s.value",
                                                                          self.tx_mesg_Dimmung_01,
                                                                          alias="BCM1_Stellgroesse_Kl_58s", descr="")
        self.Dimmung_01__DI_KL_58xs__value = TxCanBusSignal(app,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.signals.DI_KL_58xs.value",
                                                            self.tx_mesg_Dimmung_01, alias="DI_KL_58xs", descr="")

        # Diagnose_01 # ==================================================
        self.tx_mesg_Diagnose_01 = TxCanBusMessage(app, None, 1000, alias="Diagnose_01", descr="")
        self.Diagnose_01__UH_Monat__value = TxCanBusSignal(app,
                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.UH_Monat.value",
                                                           self.tx_mesg_Diagnose_01, alias="UH_Monat", descr="")
        self.Diagnose_01__DGN_Verlernzaehler__value = TxCanBusSignal(app,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.DGN_Verlernzaehler.value",
                                                                     self.tx_mesg_Diagnose_01,
                                                                     alias="DGN_Verlernzaehler", descr="")
        self.Diagnose_01__UH_Tag__value = TxCanBusSignal(app,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.UH_Tag.value",
                                                         self.tx_mesg_Diagnose_01, alias="UH_Tag", descr="")
        self.Diagnose_01__Vehicle_Driving_Cycle__value = TxCanBusSignal(app,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.Vehicle_Driving_Cycle.value",
                                                                        self.tx_mesg_Diagnose_01,
                                                                        alias="Vehicle_Driving_Cycle", descr="")
        self.Diagnose_01__DW_Kilometerstand__value = TxCanBusSignal(app,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.DW_Kilometerstand.value",
                                                                    self.tx_mesg_Diagnose_01, alias="DW_Kilometerstand",
                                                                    descr="")
        self.Diagnose_01__UH_Stunde__value = TxCanBusSignal(app,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.UH_Stunde.value",
                                                            self.tx_mesg_Diagnose_01, alias="UH_Stunde", descr="")
        self.Diagnose_01__UH_Minute__value = TxCanBusSignal(app,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.UH_Minute.value",
                                                            self.tx_mesg_Diagnose_01, alias="UH_Minute", descr="")
        self.Diagnose_01__UH_Jahr__value = TxCanBusSignal(app,
                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.UH_Jahr.value",
                                                          self.tx_mesg_Diagnose_01, alias="UH_Jahr", descr="")
        self.Diagnose_01__UH_Sekunde__value = TxCanBusSignal(app,
                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.UH_Sekunde.value",
                                                             self.tx_mesg_Diagnose_01, alias="UH_Sekunde", descr="")

        # ClampControl_01 # ==================================================
        self.tx_mesg_ClampControl_01 = TxCanBusMessage(app, None, 100, alias="ClampControl_01", descr="")
        self.ClampControl_01__KST_Fahrerhinweis_4__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Fahrerhinweis_4.value",
                                                                          self.tx_mesg_ClampControl_01,
                                                                          alias="KST_Fahrerhinweis_4", descr="")
        self.ClampControl_01__KST_Fahrerhinweis_5__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Fahrerhinweis_5.value",
                                                                          self.tx_mesg_ClampControl_01,
                                                                          alias="KST_Fahrerhinweis_5", descr="")
        self.ClampControl_01__KST_Fahrerhinweis_6__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Fahrerhinweis_6.value",
                                                                          self.tx_mesg_ClampControl_01,
                                                                          alias="KST_Fahrerhinweis_6", descr="")
        self.ClampControl_01__KST_Sonderzustand_Anforderung__value = TxCanBusSignal(app,
                                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Sonderzustand_Anforderung.value",
                                                                                    self.tx_mesg_ClampControl_01,
                                                                                    alias="KST_Sonderzustand_Anforderung",
                                                                                    descr="")
        self.ClampControl_01__KST_Fahrerhinweis_1__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Fahrerhinweis_1.value",
                                                                          self.tx_mesg_ClampControl_01,
                                                                          alias="KST_Fahrerhinweis_1", descr="")
        self.ClampControl_01__KST_Fahrerhinweis_2__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Fahrerhinweis_2.value",
                                                                          self.tx_mesg_ClampControl_01,
                                                                          alias="KST_Fahrerhinweis_2", descr="")
        self.ClampControl_01__KST_Current_State__value = TxCanBusSignal(app,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Current_State.value",
                                                                        self.tx_mesg_ClampControl_01,
                                                                        alias="KST_Current_State", descr="")
        self.ClampControl_01__KST_ComfortReadyStatus__value = TxCanBusSignal(app,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_ComfortReadyStatus.value",
                                                                             self.tx_mesg_ClampControl_01,
                                                                             alias="KST_ComfortReadyStatus", descr="")
        self.ClampControl_01__KST_StPtDeacReq__value = TxCanBusSignal(app,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_StPtDeacReq.value",
                                                                      self.tx_mesg_ClampControl_01,
                                                                      alias="KST_StPtDeacReq", descr="")
        self.ClampControl_01__KST_Fahrerhinweis_3__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Fahrerhinweis_3.value",
                                                                          self.tx_mesg_ClampControl_01,
                                                                          alias="KST_Fahrerhinweis_3", descr="")
        self.ClampControl_01__KST_BulbCheckReq__value = TxCanBusSignal(app,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_BulbCheckReq.value",
                                                                       self.tx_mesg_ClampControl_01,
                                                                       alias="KST_BulbCheckReq", descr="")
        self.ClampControl_01__KST_Target_Function__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Target_Function.value",
                                                                          self.tx_mesg_ClampControl_01,
                                                                          alias="KST_Target_Function", descr="")
        self.ClampControl_01__KST_Txt_Panikabschaltung__value = TxCanBusSignal(app,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Txt_Panikabschaltung.value",
                                                                               self.tx_mesg_ClampControl_01,
                                                                               alias="KST_Txt_Panikabschaltung",
                                                                               descr="")
        self.ClampControl_01__KST_Target_Mode__value = TxCanBusSignal(app,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Target_Mode.value",
                                                                      self.tx_mesg_ClampControl_01,
                                                                      alias="KST_Target_Mode", descr="")
        self.ClampControl_01__KST_Kl_50_Startanforderung__value = TxCanBusSignal(app,
                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Kl_50_Startanforderung.value",
                                                                                 self.tx_mesg_ClampControl_01,
                                                                                 alias="KST_Kl_50_Startanforderung",
                                                                                 descr="")
        self.ClampControl_01__KST_Kl_X__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Kl_X.value",
                                                               self.tx_mesg_ClampControl_01, alias="KST_Kl_X", descr="")
        self.ClampControl_01__KST_StPtAcvReq__value = TxCanBusSignal(app,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_StPtAcvReq.value",
                                                                     self.tx_mesg_ClampControl_01,
                                                                     alias="KST_StPtAcvReq", descr="")
        self.ClampControl_01__KST_Kl_S__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Kl_S.value",
                                                               self.tx_mesg_ClampControl_01, alias="KST_Kl_S", descr="")
        self.ClampControl_01__KST_WFS_Fahrfreigabe_Anforderung__value = TxCanBusSignal(app,
                                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_WFS_Fahrfreigabe_Anforderung.value",
                                                                                       self.tx_mesg_ClampControl_01,
                                                                                       alias="KST_WFS_Fahrfreigabe_Anforderung",
                                                                                       descr="")
        self.ClampControl_01__KST_Ausstiegswunsch_Status__value = TxCanBusSignal(app,
                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Ausstiegswunsch_Status.value",
                                                                                 self.tx_mesg_ClampControl_01,
                                                                                 alias="KST_Ausstiegswunsch_Status",
                                                                                 descr="")
        self.ClampControl_01__ClampControl_01_BZ__value = TxCanBusSignal(app,
                                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.ClampControl_01_BZ.value",
                                                                         self.tx_mesg_ClampControl_01,
                                                                         alias="ClampControl_01_BZ", descr="")
        self.ClampControl_01__KST_Remotestart_KL15_Anf__value = TxCanBusSignal(app,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Remotestart_KL15_Anf.value",
                                                                               self.tx_mesg_ClampControl_01,
                                                                               alias="KST_Remotestart_KL15_Anf",
                                                                               descr="")
        self.ClampControl_01__KST_Ausparken_Betrieb__value = TxCanBusSignal(app,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Ausparken_Betrieb.value",
                                                                            self.tx_mesg_ClampControl_01,
                                                                            alias="KST_Ausparken_Betrieb", descr="")
        self.ClampControl_01__KST_Deaktivierungs_Trigger__value = TxCanBusSignal(app,
                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Deaktivierungs_Trigger.value",
                                                                                 self.tx_mesg_ClampControl_01,
                                                                                 alias="KST_Deaktivierungs_Trigger",
                                                                                 descr="")
        self.ClampControl_01__KST_ZAT_betaetigt__value = TxCanBusSignal(app,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_ZAT_betaetigt.value",
                                                                        self.tx_mesg_ClampControl_01,
                                                                        alias="KST_ZAT_betaetigt", descr="")
        self.ClampControl_01__KST_Anf_Klemmenfreigabe_ELV__value = TxCanBusSignal(app,
                                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Anf_Klemmenfreigabe_ELV.value",
                                                                                  self.tx_mesg_ClampControl_01,
                                                                                  alias="KST_Anf_Klemmenfreigabe_ELV",
                                                                                  descr="")
        self.ClampControl_01__KST_aut_Abschaltung_Zuendung__value = TxCanBusSignal(app,
                                                                                   "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_aut_Abschaltung_Zuendung.value",
                                                                                   self.tx_mesg_ClampControl_01,
                                                                                   alias="KST_aut_Abschaltung_Zuendung",
                                                                                   descr="")
        self.ClampControl_01__ClampControl_01_CRC__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.ClampControl_01_CRC.value",
                                                                          self.tx_mesg_ClampControl_01,
                                                                          alias="ClampControl_01_CRC", descr="")
        self.ClampControl_01__KST_KL_15__value = TxCanBusSignal(app,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_KL_15.value",
                                                                self.tx_mesg_ClampControl_01, alias="KST_KL_15",
                                                                descr="")
        self.ClampControl_01__KST_Sonderzustand_Status__value = TxCanBusSignal(app,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Sonderzustand_Status.value",
                                                                               self.tx_mesg_ClampControl_01,
                                                                               alias="KST_Sonderzustand_Status",
                                                                               descr="")

        # OBD_03 # ==================================================
        self.tx_mesg_OBD_03 = TxCanBusMessage(app, None, 320, alias="OBD_03", descr="")
        self.OBD_03__OBD_Eng_Cool_Temp__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Eng_Cool_Temp.value",
                                                               self.tx_mesg_OBD_03, alias="OBD_Eng_Cool_Temp", descr="")
        self.OBD_03__OBD_Driving_Cycle__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Driving_Cycle.value",
                                                               self.tx_mesg_OBD_03, alias="OBD_Driving_Cycle", descr="")
        self.OBD_03__OBD_Normed_Trip__value = TxCanBusSignal(app,
                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Normed_Trip.value",
                                                             self.tx_mesg_OBD_03, alias="OBD_Normed_Trip", descr="")
        self.OBD_03__OBD_Warm_Up_Cycle__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Warm_Up_Cycle.value",
                                                               self.tx_mesg_OBD_03, alias="OBD_Warm_Up_Cycle", descr="")
        self.OBD_03__OBD_Minimum_Trip__value = TxCanBusSignal(app,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Minimum_Trip.value",
                                                              self.tx_mesg_OBD_03, alias="OBD_Minimum_Trip", descr="")
        self.OBD_03__OBD_Abs_Pedal_Pos__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Abs_Pedal_Pos.value",
                                                               self.tx_mesg_OBD_03, alias="OBD_Abs_Pedal_Pos", descr="")
        self.OBD_03__OBD_Abs_Throttle_Pos__value = TxCanBusSignal(app,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Abs_Throttle_Pos.value",
                                                                  self.tx_mesg_OBD_03, alias="OBD_Abs_Throttle_Pos",
                                                                  descr="")
        self.OBD_03__OBD_Aussen_Temp_gef__value = TxCanBusSignal(app,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Aussen_Temp_gef.value",
                                                                 self.tx_mesg_OBD_03, alias="OBD_Aussen_Temp_gef",
                                                                 descr="")
        self.OBD_03__OBD_Abs_Load_Val__value = TxCanBusSignal(app,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Abs_Load_Val.value",
                                                              self.tx_mesg_OBD_03, alias="OBD_Abs_Load_Val", descr="")

        # OBD_04 # ==================================================
        self.tx_mesg_OBD_04 = TxCanBusMessage(app, None, 320, alias="OBD_04", descr="")
        self.OBD_04__OBD_Kaltstart_Denominator__value = TxCanBusSignal(app,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_Kaltstart_Denominator.value",
                                                                       self.tx_mesg_OBD_04,
                                                                       alias="OBD_Kaltstart_Denominator", descr="")
        self.OBD_04__OBD_Typ__value = TxCanBusSignal(app, "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_Typ.value",
                                                     self.tx_mesg_OBD_04, alias="OBD_Typ", descr="")
        self.OBD_04__OBD_Sperrung_Kaltstart_Denom__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_Sperrung_Kaltstart_Denom.value",
                                                                          self.tx_mesg_OBD_04,
                                                                          alias="OBD_Sperrung_Kaltstart_Denom",
                                                                          descr="")
        self.OBD_04__OBD_Sperrung_IUMPR__value = TxCanBusSignal(app,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_Sperrung_IUMPR.value",
                                                                self.tx_mesg_OBD_04, alias="OBD_Sperrung_IUMPR",
                                                                descr="")
        self.OBD_04__OBD_Calc_Load_Val__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_Calc_Load_Val.value",
                                                               self.tx_mesg_OBD_04, alias="OBD_Calc_Load_Val", descr="")
        self.OBD_04__OBD_NumDcyMilOnReq__value = TxCanBusSignal(app,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_NumDcyMilOnReq.value",
                                                                self.tx_mesg_OBD_04, alias="OBD_NumDcyMilOnReq",
                                                                descr="")
        self.OBD_04__OBD_ClearMem_Inhibit__value = TxCanBusSignal(app,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_ClearMem_Inhibit.value",
                                                                  self.tx_mesg_OBD_04, alias="OBD_ClearMem_Inhibit",
                                                                  descr="")
        self.OBD_04__OBD_MIL__value = TxCanBusSignal(app, "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_MIL.value",
                                                     self.tx_mesg_OBD_04, alias="OBD_MIL", descr="")
        self.OBD_04__MM_PropulsionSystemActive__value = TxCanBusSignal(app,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.MM_PropulsionSystemActive.value",
                                                                       self.tx_mesg_OBD_04,
                                                                       alias="MM_PropulsionSystemActive", descr="")
        self.OBD_04__OBD_QBit_Aussen_Temp__value = TxCanBusSignal(app,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_QBit_Aussen_Temp.value",
                                                                  self.tx_mesg_OBD_04, alias="OBD_QBit_Aussen_Temp",
                                                                  descr="")

        # ORU_Control_D_01 # ==================================================
        self.tx_mesg_ORU_Control_D_01 = TxCanBusMessage(app, None, 320, alias="ORU_Control_D_01", descr="")
        self.ORU_Control_D_01__ORU_Control_D_01_BZ__value = TxCanBusSignal(app,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.ORU_Control_D_01_BZ.value",
                                                                           self.tx_mesg_ORU_Control_D_01,
                                                                           alias="ORU_Control_D_01_BZ", descr="")
        self.ORU_Control_D_01__OruVehicleLockRequestD__value = TxCanBusSignal(app,
                                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OruVehicleLockRequestD.value",
                                                                              self.tx_mesg_ORU_Control_D_01,
                                                                              alias="OruVehicleLockRequestD", descr="")
        self.ORU_Control_D_01__OruIntegrityCheckActiveD__value = TxCanBusSignal(app,
                                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OruIntegrityCheckActiveD.value",
                                                                                self.tx_mesg_ORU_Control_D_01,
                                                                                alias="OruIntegrityCheckActiveD",
                                                                                descr="")
        self.ORU_Control_D_01__OruControlStateD__value = TxCanBusSignal(app,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OruControlStateD.value",
                                                                        self.tx_mesg_ORU_Control_D_01,
                                                                        alias="OruControlStateD", descr="")
        self.ORU_Control_D_01__OnlineRemoteUpdateControlOldD__value = TxCanBusSignal(app,
                                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OnlineRemoteUpdateControlOldD.value",
                                                                                     self.tx_mesg_ORU_Control_D_01,
                                                                                     alias="OnlineRemoteUpdateControlOldD",
                                                                                     descr="")
        self.ORU_Control_D_01__OruControlReleaseD__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OruControlReleaseD.value",
                                                                          self.tx_mesg_ORU_Control_D_01,
                                                                          alias="OruControlReleaseD", descr="")
        self.ORU_Control_D_01__OnlineRemoteUpdateControlD__value = TxCanBusSignal(app,
                                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OnlineRemoteUpdateControlD.value",
                                                                                  self.tx_mesg_ORU_Control_D_01,
                                                                                  alias="OnlineRemoteUpdateControlD",
                                                                                  descr="")
        self.ORU_Control_D_01__ISignalVoid_ORU_Control_D_01_0__value = TxCanBusSignal(app,
                                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.ISignalVoid_ORU_Control_D_01_0.value",
                                                                                      self.tx_mesg_ORU_Control_D_01,
                                                                                      alias="ISignalVoid_ORU_Control_D_01_0",
                                                                                      descr="")
        self.ORU_Control_D_01__ISignalVoid_ORU_Control_D_01_1__value = TxCanBusSignal(app,
                                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.ISignalVoid_ORU_Control_D_01_1.value",
                                                                                      self.tx_mesg_ORU_Control_D_01,
                                                                                      alias="ISignalVoid_ORU_Control_D_01_1",
                                                                                      descr="")
        self.ORU_Control_D_01__OruHostUpdateD__value = TxCanBusSignal(app,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OruHostUpdateD.value",
                                                                      self.tx_mesg_ORU_Control_D_01,
                                                                      alias="OruHostUpdateD", descr="")
        self.ORU_Control_D_01__OruReleasePartitionSwitchD__value = TxCanBusSignal(app,
                                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OruReleasePartitionSwitchD.value",
                                                                                  self.tx_mesg_ORU_Control_D_01,
                                                                                  alias="OruReleasePartitionSwitchD",
                                                                                  descr="")
        self.ORU_Control_D_01__ORU_Control_D_01_CRC__value = TxCanBusSignal(app,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.ORU_Control_D_01_CRC.value",
                                                                            self.tx_mesg_ORU_Control_D_01,
                                                                            alias="ORU_Control_D_01_CRC", descr="")

        # OTAMC_D_01 # ==================================================
        self.tx_mesg_OTAMC_D_01 = TxCanBusMessage(app, None, 320, alias="OTAMC_D_01", descr="")
        self.OTAMC_D_01__VehicleProtectedEnvironment_D__value = TxCanBusSignal(app,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.signals.VehicleProtectedEnvironment_D.value",
                                                                               self.tx_mesg_OTAMC_D_01,
                                                                               alias="VehicleProtectedEnvironment_D",
                                                                               descr="")
        self.OTAMC_D_01__OTAMC_D_01_CRC__value = TxCanBusSignal(app,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.signals.OTAMC_D_01_CRC.value",
                                                                self.tx_mesg_OTAMC_D_01, alias="OTAMC_D_01_CRC",
                                                                descr="")
        self.OTAMC_D_01__ISignalVoid_OTAMC_D_01_0__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.signals.ISignalVoid_OTAMC_D_01_0.value",
                                                                          self.tx_mesg_OTAMC_D_01,
                                                                          alias="ISignalVoid_OTAMC_D_01_0", descr="")
        self.OTAMC_D_01__ISignalVoid_OTAMC_D_01_1__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.signals.ISignalVoid_OTAMC_D_01_1.value",
                                                                          self.tx_mesg_OTAMC_D_01,
                                                                          alias="ISignalVoid_OTAMC_D_01_1", descr="")
        self.OTAMC_D_01__ISignalVoid_OTAMC_D_01_2__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.signals.ISignalVoid_OTAMC_D_01_2.value",
                                                                          self.tx_mesg_OTAMC_D_01,
                                                                          alias="ISignalVoid_OTAMC_D_01_2", descr="")
        self.OTAMC_D_01__OTAMC_D_01_BZ__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.signals.OTAMC_D_01_BZ.value",
                                                               self.tx_mesg_OTAMC_D_01, alias="OTAMC_D_01_BZ", descr="")

        # OTAMC_01 # ==================================================
        self.tx_mesg_OTAMC_01 = TxCanBusMessage(app, None, 960, alias="OTAMC_01", descr="")
        self.OTAMC_01__OTAMC_01_BZ__value = TxCanBusSignal(app,
                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_01.signals.OTAMC_01_BZ.value",
                                                           self.tx_mesg_OTAMC_01, alias="OTAMC_01_BZ", descr="")
        self.OTAMC_01__OTAMC_01_CRC__value = TxCanBusSignal(app,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_01.signals.OTAMC_01_CRC.value",
                                                            self.tx_mesg_OTAMC_01, alias="OTAMC_01_CRC", descr="")
        self.OTAMC_01__VPE_State__value = TxCanBusSignal(app,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_01.signals.VPE_State.value",
                                                         self.tx_mesg_OTAMC_01, alias="VPE_State", descr="")
        self.OTAMC_01__OruControlReleaseA__value = TxCanBusSignal(app,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_01.signals.OruControlReleaseA.value",
                                                                  self.tx_mesg_OTAMC_01, alias="OruControlReleaseA",
                                                                  descr="")
        self.OTAMC_01__OTA_State__value = TxCanBusSignal(app,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_01.signals.OTA_State.value",
                                                         self.tx_mesg_OTAMC_01, alias="OTA_State", descr="")

        # DIA_SAAM_Req # ==================================================
        self.tx_mesg_DIA_SAAM_Req = TxCanBusMessage(app, None, 0, alias="DIA_SAAM_Req", descr="")
        self.DIA_SAAM_Req__DIA_SAAM_Req_Data__value = TxCanBusSignal(app,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.DIA_SAAM_Req.signals.DIA_SAAM_Req_Data.value",
                                                                     self.tx_mesg_DIA_SAAM_Req,
                                                                     alias="DIA_SAAM_Req_Data", descr="")

        # ORU_Control_A_01 # ==================================================
        self.tx_mesg_ORU_Control_A_01 = TxCanBusMessage(app, None, 500, alias="ORU_Control_A_01", descr="")
        self.ORU_Control_A_01__OruIntegrityCheckActiveA__value = TxCanBusSignal(app,
                                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OruIntegrityCheckActiveA.value",
                                                                                self.tx_mesg_ORU_Control_A_01,
                                                                                alias="OruIntegrityCheckActiveA",
                                                                                descr="")
        self.ORU_Control_A_01__ORU_Control_A_01_BZ__value = TxCanBusSignal(app,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.ORU_Control_A_01_BZ.value",
                                                                           self.tx_mesg_ORU_Control_A_01,
                                                                           alias="ORU_Control_A_01_BZ", descr="")

        self.ORU_Control_A_01__OruVehicleLockRequestA__value = TxCanBusSignal(app,
                                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OruVehicleLockRequestA.value",
                                                                              self.tx_mesg_ORU_Control_A_01,
                                                                              alias="OruVehicleLockRequestA", descr="")
        self.ORU_Control_A_01__OTA_FlgPTAcvPhdA__value = TxCanBusSignal(app,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OTA_FlgPTAcvPhdA.value",
                                                                        self.tx_mesg_ORU_Control_A_01,
                                                                        alias="OTA_FlgPTAcvPhdA", descr="")
        self.ORU_Control_A_01__ISignalVoid_ORU_Control_A_01_1__value = TxCanBusSignal(app,
                                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.ISignalVoid_ORU_Control_A_01_1.value",
                                                                                      self.tx_mesg_ORU_Control_A_01,
                                                                                      alias="ISignalVoid_ORU_Control_A_01_1",
                                                                                      descr="")
        self.ORU_Control_A_01__ISignalVoid_ORU_Control_A_01_0__value = TxCanBusSignal(app,
                                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.ISignalVoid_ORU_Control_A_01_0.value",
                                                                                      self.tx_mesg_ORU_Control_A_01,
                                                                                      alias="ISignalVoid_ORU_Control_A_01_0",
                                                                                      descr="")
        self.ORU_Control_A_01__OruControlStateA__value = TxCanBusSignal(app,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OruControlStateA.value",
                                                                        self.tx_mesg_ORU_Control_A_01,
                                                                        alias="OruControlStateA", descr="")
        self.ORU_Control_A_01__OnlineRemoteUpdateControlOldA__value = TxCanBusSignal(app,
                                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OnlineRemoteUpdateControlOldA.value",
                                                                                     self.tx_mesg_ORU_Control_A_01,
                                                                                     alias="OnlineRemoteUpdateControlOldA",
                                                                                     descr="")
        self.ORU_Control_A_01__OruControlReleaseA__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OruControlReleaseA.value",
                                                                          self.tx_mesg_ORU_Control_A_01,
                                                                          alias="OruControlReleaseA", descr="")
        self.ORU_Control_A_01__OnlineRemoteUpdateControlA__value = TxCanBusSignal(app,
                                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OnlineRemoteUpdateControlA.value",
                                                                                  self.tx_mesg_ORU_Control_A_01,
                                                                                  alias="OnlineRemoteUpdateControlA",
                                                                                  descr="")
        self.ORU_Control_A_01__OruHostUpdateA__value = TxCanBusSignal(app,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OruHostUpdateA.value",
                                                                      self.tx_mesg_ORU_Control_A_01,
                                                                      alias="OruHostUpdateA", descr="")
        self.ORU_Control_A_01__OruReleasePartitionSwitchA__value = TxCanBusSignal(app,
                                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OruReleasePartitionSwitchA.value",
                                                                                  self.tx_mesg_ORU_Control_A_01,
                                                                                  alias="OruReleasePartitionSwitchA",
                                                                                  descr="")
        self.ORU_Control_A_01__ORU_Control_A_01_CRC__value = TxCanBusSignal(app,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.ORU_Control_A_01_CRC.value",
                                                                            self.tx_mesg_ORU_Control_A_01,
                                                                            alias="ORU_Control_A_01_CRC", descr="")

        # ORU_01 # ==================================================
        self.tx_mesg_ORU_01 = TxCanBusMessage(app, None, 500, alias="ORU_01", descr="")
        self.ORU_01__ORU_Status__value = TxCanBusSignal(app,
                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_01.signals.ORU_Status.value",
                                                        self.tx_mesg_ORU_01, alias="ORU_Status", descr="")

        # NM_Airbag # ==================================================
        self.tx_mesg_NM_Airbag = TxCanBusMessage(app, None, 0, alias="NM_Airbag", descr="")
        self.NM_Airbag__NM_Airbag_01_NM_State__value = TxCanBusSignal(app,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_NM_State.value",
                                                                      self.tx_mesg_NM_Airbag,
                                                                      alias="NM_Airbag_01_NM_State", descr="")
        self.NM_Airbag__NM_Airbag_01_SNI_10__value = TxCanBusSignal(app,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_SNI_10.value",
                                                                    self.tx_mesg_NM_Airbag, alias="NM_Airbag_01_SNI_10",
                                                                    descr="")
        self.NM_Airbag__NM_Airbag_01_NM_aktiv_Tmin__value = TxCanBusSignal(app,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_NM_aktiv_Tmin.value",
                                                                           self.tx_mesg_NM_Airbag,
                                                                           alias="NM_Airbag_01_NM_aktiv_Tmin", descr="")
        self.NM_Airbag__NM_Airbag_01_FCAB__value = TxCanBusSignal(app,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_FCAB.value",
                                                                  self.tx_mesg_NM_Airbag, alias="NM_Airbag_01_FCAB",
                                                                  descr="")
        self.NM_Airbag__NM_Airbag_01_NM_aktiv_Diag__value = TxCanBusSignal(app,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_NM_aktiv_Diag.value",
                                                                           self.tx_mesg_NM_Airbag,
                                                                           alias="NM_Airbag_01_NM_aktiv_Diag", descr="")
        self.NM_Airbag__NM_aktiv_Kl15_unplausibel__value = TxCanBusSignal(app,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_aktiv_Kl15_unplausibel.value",
                                                                          self.tx_mesg_NM_Airbag,
                                                                          alias="NM_aktiv_Kl15_unplausibel", descr="")
        self.NM_Airbag__NM_Airbag_01_UDS_CC__value = TxCanBusSignal(app,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_UDS_CC.value",
                                                                    self.tx_mesg_NM_Airbag, alias="NM_Airbag_01_UDS_CC",
                                                                    descr="")
        self.NM_Airbag__NM_Airbag_01_CBV_CRI__value = TxCanBusSignal(app,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_CBV_CRI.value",
                                                                     self.tx_mesg_NM_Airbag,
                                                                     alias="NM_Airbag_01_CBV_CRI", descr="")
        self.NM_Airbag__NM_aktiv_AntriebsCAN_aktiv__value = TxCanBusSignal(app,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_aktiv_AntriebsCAN_aktiv.value",
                                                                           self.tx_mesg_NM_Airbag,
                                                                           alias="NM_aktiv_AntriebsCAN_aktiv", descr="")
        self.NM_Airbag__NM_aktiv_Gurtparken__value = TxCanBusSignal(app,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_aktiv_Gurtparken.value",
                                                                    self.tx_mesg_NM_Airbag, alias="NM_aktiv_Gurtparken",
                                                                    descr="")
        self.NM_Airbag__NM_Airbag_01_CBV_AWB__value = TxCanBusSignal(app,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_CBV_AWB.value",
                                                                     self.tx_mesg_NM_Airbag,
                                                                     alias="NM_Airbag_01_CBV_AWB", descr="")
        self.NM_Airbag__NM_aktiv_Ausloesefaehig__value = TxCanBusSignal(app,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_aktiv_Ausloesefaehig.value",
                                                                        self.tx_mesg_NM_Airbag,
                                                                        alias="NM_aktiv_Ausloesefaehig", descr="")
        self.NM_Airbag__NM_aktiv_Gurtschloss__value = TxCanBusSignal(app,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_aktiv_Gurtschloss.value",
                                                                     self.tx_mesg_NM_Airbag,
                                                                     alias="NM_aktiv_Gurtschloss", descr="")
        self.NM_Airbag__NM_Airbag_01_NM_aktiv_KL15__value = TxCanBusSignal(app,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_NM_aktiv_KL15.value",
                                                                           self.tx_mesg_NM_Airbag,
                                                                           alias="NM_Airbag_01_NM_aktiv_KL15", descr="")
        self.NM_Airbag__NM_aktiv_Sitzbelegung__value = TxCanBusSignal(app,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_aktiv_Sitzbelegung.value",
                                                                      self.tx_mesg_NM_Airbag,
                                                                      alias="NM_aktiv_Sitzbelegung", descr="")
        self.NM_Airbag__NM_Airbag_01_Wakeup_V12__value = TxCanBusSignal(app,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_Wakeup_V12.value",
                                                                        self.tx_mesg_NM_Airbag,
                                                                        alias="NM_Airbag_01_Wakeup_V12", descr="")

        # NM_HCP1 # ==================================================
        self.tx_mesg_NM_HCP1 = TxCanBusMessage(app, None, 0, alias="NM_HCP1", descr="")
        self.NM_HCP1__NM_HCP1_UDS_CC__value = TxCanBusSignal(app,
                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_UDS_CC.value",
                                                             self.tx_mesg_NM_HCP1, alias="NM_HCP1_UDS_CC", descr="")
        self.NM_HCP1__NM_aktiv_Fahrstufenanzeige__value = TxCanBusSignal(app,
                                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_aktiv_Fahrstufenanzeige.value",
                                                                         self.tx_mesg_NM_HCP1,
                                                                         alias="NM_aktiv_Fahrstufenanzeige", descr="")
        self.NM_HCP1__NM_aktiv_Niveauregelung__value = TxCanBusSignal(app,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_aktiv_Niveauregelung.value",
                                                                      self.tx_mesg_NM_HCP1,
                                                                      alias="NM_aktiv_Niveauregelung", descr="")
        self.NM_HCP1__NM_HCP1_SNI_10__value = TxCanBusSignal(app,
                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_SNI_10.value",
                                                             self.tx_mesg_NM_HCP1, alias="NM_HCP1_SNI_10", descr="")
        self.NM_HCP1__NM_aktiv_Parkanforderung__value = TxCanBusSignal(app,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_aktiv_Parkanforderung.value",
                                                                       self.tx_mesg_NM_HCP1,
                                                                       alias="NM_aktiv_Parkanforderung", descr="")
        self.NM_HCP1__NM_aktiv_Stillstandsmanagement__value = TxCanBusSignal(app,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_aktiv_Stillstandsmanagement.value",
                                                                             self.tx_mesg_NM_HCP1,
                                                                             alias="NM_aktiv_Stillstandsmanagement",
                                                                             descr="")
        self.NM_HCP1__NM_HCP1_CBV_CRI__value = TxCanBusSignal(app,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_CBV_CRI.value",
                                                              self.tx_mesg_NM_HCP1, alias="NM_HCP1_CBV_CRI", descr="")
        self.NM_HCP1__NM_HCP1_NM_aktiv_KL15__value = TxCanBusSignal(app,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_NM_aktiv_KL15.value",
                                                                    self.tx_mesg_NM_HCP1, alias="NM_HCP1_NM_aktiv_KL15",
                                                                    descr="")
        self.NM_HCP1__NM_HCP1_NM_aktiv_Tmin__value = TxCanBusSignal(app,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_NM_aktiv_Tmin.value",
                                                                    self.tx_mesg_NM_HCP1, alias="NM_HCP1_NM_aktiv_Tmin",
                                                                    descr="")
        self.NM_HCP1__NM_aktiv_Halteanforderung__value = TxCanBusSignal(app,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_aktiv_Halteanforderung.value",
                                                                        self.tx_mesg_NM_HCP1,
                                                                        alias="NM_aktiv_Halteanforderung", descr="")
        self.NM_HCP1__NM_HCP1_CBV_AWB__value = TxCanBusSignal(app,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_CBV_AWB.value",
                                                              self.tx_mesg_NM_HCP1, alias="NM_HCP1_CBV_AWB", descr="")
        self.NM_HCP1__NM_HCP1_NM_aktiv_Diag__value = TxCanBusSignal(app,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_NM_aktiv_Diag.value",
                                                                    self.tx_mesg_NM_HCP1, alias="NM_HCP1_NM_aktiv_Diag",
                                                                    descr="")
        self.NM_HCP1__NM_HCP1_NM_State__value = TxCanBusSignal(app,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_NM_State.value",
                                                               self.tx_mesg_NM_HCP1, alias="NM_HCP1_NM_State", descr="")
        self.NM_HCP1__NM_HCP_1_Wakeup_V12__value = TxCanBusSignal(app,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP_1_Wakeup_V12.value",
                                                                  self.tx_mesg_NM_HCP1, alias="NM_HCP_1_Wakeup_V12",
                                                                  descr="")
        self.NM_HCP1__NM_HCP1_NM_aktiv_CABaktiv__value = TxCanBusSignal(app,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_NM_aktiv_CABaktiv.value",
                                                                        self.tx_mesg_NM_HCP1,
                                                                        alias="NM_HCP1_NM_aktiv_CABaktiv", descr="")
        self.NM_HCP1__NM_HCP1_FCAB__value = TxCanBusSignal(app,
                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_FCAB.value",
                                                           self.tx_mesg_NM_HCP1, alias="NM_HCP1_FCAB", descr="")

        # ISOx_Waehlhebel_Resp_FD # ==================================================
        self.rx_mesg_ISOx_Waehlhebel_Resp_FD = RxCanBusMessage(app, None, 0, alias="ISOx_Waehlhebel_Resp_FD", descr="")
        self.ISOx_Waehlhebel_Resp_FD__ISOx_Waehlhebel_Resp_FD_Data__value = RxCanBusSignal(app,
                                                                                           "Waehlhebel:CAN.can0_HIL.HIL_RX.ISOx_Waehlhebel_Resp_FD.signals.ISOx_Waehlhebel_Resp_FD_Data.value",
                                                                                           self.rx_mesg_ISOx_Waehlhebel_Resp_FD,
                                                                                           alias="ISOx_Waehlhebel_Resp_FD_Data",
                                                                                           descr="")

        # OBDC_Waehlhebel_Req_FD # ==================================================
        self.tx_mesg_OBDC_Waehlhebel_Req_FD = TxCanBusMessage(app, None, 0, alias="OBDC_Waehlhebel_Req_FD", descr="")
        self.OBDC_Waehlhebel_Req_FD__OBDC_Waehlhebel_Req_FD_Data__value = TxCanBusSignal(app,
                                                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.OBDC_Waehlhebel_Req_FD.signals.OBDC_Waehlhebel_Req_FD_Data.value",
                                                                                         self.tx_mesg_OBDC_Waehlhebel_Req_FD,
                                                                                         alias="OBDC_Waehlhebel_Req_FD_Data",
                                                                                         descr="")

        # ISOx_Waehlhebel_Req_FD # ==================================================
        self.tx_mesg_ISOx_Waehlhebel_Req_FD = TxCanBusMessage(app, None, 0, alias="ISOx_Waehlhebel_Req_FD", descr="")
        self.ISOx_Waehlhebel_Req_FD__ISOx_Waehlhebel_Req_FD_Data__value = TxCanBusSignal(app,
                                                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Waehlhebel_Req_FD.signals.ISOx_Waehlhebel_Req_FD_Data.value",
                                                                                         self.tx_mesg_ISOx_Waehlhebel_Req_FD,
                                                                                         alias="ISOx_Waehlhebel_Req_FD_Data",
                                                                                         descr="")

        # ISOx_Funkt_Req_All_FD # ==================================================
        self.tx_mesg_ISOx_Funkt_Req_All_FD = TxCanBusMessage(app, None, 0, alias="ISOx_Funkt_Req_All_FD", descr="")
        self.ISOx_Funkt_Req_All_FD__ISOx_Funkt_Req_All_FD_Data__value = TxCanBusSignal(app,
                                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.signals.ISOx_Funkt_Req_All_FD_Data.value",
                                                                                       self.tx_mesg_ISOx_Funkt_Req_All_FD,
                                                                                       alias="ISOx_Funkt_Req_All_FD_Data",
                                                                                       descr="")

        # OBDC_Funktionaler_Req_All_FD # ==================================================
        self.tx_mesg_OBDC_Funktionaler_Req_All_FD = TxCanBusMessage(app, None, 0, alias="OBDC_Funktionaler_Req_All_FD",
                                                                    descr="")
        self.OBDC_Funktionaler_Req_All_FD__OBDC_Funktion_Req_All_FD_Data__value = TxCanBusSignal(app,
                                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.OBDC_Funktionaler_Req_All_FD.signals.OBDC_Funktion_Req_All_FD_Data.value",
                                                                                                 self.tx_mesg_OBDC_Funktionaler_Req_All_FD,
                                                                                                 alias="OBDC_Funktion_Req_All_FD_Data",
                                                                                                 descr="")


#
# #############################################################################
# Main
# #############################################################################
if __name__ == "__main__":
    ### TODO: replace with code working with XIL-API
    ### from ttk_tools.dspace import rtplib_offline_stub
    ### tracefile, board, system = "foo.sdf", "bar1005", "Offline"
    ### rt_app = rtplib_offline_stub.Appl(tracefile, board, system)

    ### bus = CanBusSignals(rt_app)
    print "Load %s" % (__file__)
    print "Done."

















