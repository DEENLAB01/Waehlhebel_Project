# -*- coding: latin-1 -*-
# File    : hil_variables.py
# Task    : Container for hil variables (here: Gamma V model variables)
#
# Author  : Mohammed Abdul Karim
# Date    : 14.12.2020
# Copyright 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ******************************** Version *************************************
# ******************************************************************************
# Rev. | Date       | Author    | Description
# ------------------------------------------------------------------------------
# 1.0  | 07.11.2020 | Mohammed | initial: GammaV Varcontainer HiL-Vars
# 1.1  | 17.05.2021 | NeumannA  | cc_mon__A ergänzt zum Messen der Busruhe
# 1.2  | 20.05.2021 | NeumannA  | add default values for global enable variables
# 1.3  | 21.05.2021 | NeumannA  | add lookup for periods of messages (an/aus)
# 1.4  | 21.05.2021 | NeumannA  | add lookup vor NM Waehlhebel, removed unused variables
# 1.5  | 09.09.2021 | Mohammed  | add OBDC_Waehlhebel and DIA_SAAM, Waehlhebel_Lokalaktiv und Subsystemaktiv, ORU_01, ORU_Control_A_01, ORU_Control_D_01
# 1.5  | 23.09.2021 | Devangbhai | Added the period value of the newly added signals
# 1.6  | 30.10.2021 | Mohammed | Added new Signal from Update K-matrix : V12.05.0F
# ******************************************************************************
# TTk 2.0
from ttk_base.rst_gammav.variables import VarContainer as GammaVarContainer  # @UnresolvedImport
from ttk_base.rst_gammav.variables import VarDeferred as GammaVarDeferred  # @UnresolvedImport


# #############################################################################
class HilVars(GammaVarContainer):
    def __init__(self, gamma_api):
        GammaVarContainer.__init__(self, gamma_api)
        # ##################  CAN globals ######################
        self.can0_HIL__HIL_GLOBAL__cycle_factor = GammaVarDeferred(gamma_api,
                                                                   "Waehlhebel:CAN.can0_HIL.HIL_GLOBAL.cycle_factor")
        self.can0_HIL__HIL_RX__enable = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_RX.GLOBAL.enable", default = 1)
        self.can0_HIL__HIL_TX__enable = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.GLOBAL.enable", default = 1)

        # ######################  RX message control ######################
        # ******************** DEV_Waehlhebel_Req_00 (NonMux) ********************
        # Gamma PVs for complete RX-message:
        self.DEV_Waehlhebel_Req_00__length = GammaVarDeferred(gamma_api,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_RX.DEV_Waehlhebel_Req_00.length")
        self.DEV_Waehlhebel_Req_00__timestamp = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_RX.DEV_Waehlhebel_Req_00.timestamp")
        # Gamma ignal PVs (NonMux) for message:
        self.DEV_Waehlhebel_Req_00__DEV_Waehlhebel_Req_00_Data__value = GammaVarDeferred(gamma_api,
                                                                                         "Waehlhebel:CAN.can0_HIL.HIL_RX.DEV_Waehlhebel_Req_00.signals.DEV_Waehlhebel_Req_00_Data.value",
                                                                                         unit="")  # default="0"

        # ******************** DEV_Waehlhebel_Resp_FF (NonMux) ********************
        # Gamma PVs for complete RX-message:
        self.DEV_Waehlhebel_Resp_FF__length = GammaVarDeferred(gamma_api,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_RX.DEV_Waehlhebel_Resp_FF.length")
        self.DEV_Waehlhebel_Resp_FF__timestamp = GammaVarDeferred(gamma_api,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_RX.DEV_Waehlhebel_Resp_FF.timestamp")
        # Gamma ignal PVs (NonMux) for message:
        # Gamma ignal PVs (NonMux) for message:
        self.DEV_Waehlhebel_Resp_FF__DEV_Waehlhebel_Resp_FF_Data__value = GammaVarDeferred(gamma_api,
                                                                                           "Waehlhebel:CAN.can0_HIL.HIL_RX.DEV_Waehlhebel_Resp_FF.signals.DEV_Waehlhebel_Resp_FF_Data.value",
                                                                                           unit="")  # default="0"

        # ******************** OBDC_Funktionaler_Req_All_FD (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.OBDC_Funktionaler_Req_All_FD__length = GammaVarDeferred(gamma_api,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.OBDC_Funktionaler_Req_All_FD.length")
        self.OBDC_Funktionaler_Req_All_FD__timestamp = GammaVarDeferred(gamma_api,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.OBDC_Funktionaler_Req_All_FD.timestamp")
        self.OBDC_Funktionaler_Req_All_FD__period = GammaVarDeferred(gamma_api,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.OBDC_Funktionaler_Req_All_FD.period",  lookup={0: "aus", 100: "an"})

        # Gamma signal PVs (NonMux) for message:
        self.OBDC_Funktionaler_Req_All_FD__OBDC_Funktion_Req_All_FD_Data__value = GammaVarDeferred(gamma_api,
                                                                                                   "Waehlhebel:CAN.can0_HIL.HIL_TX.OBDC_Funktionaler_Req_All_FD.signals.OBDC_Funktion_Req_All_FD_Data.value",
                                                                                                   unit="")  # default="0"
        # ******************** OBDC_Waehlhebel_Resp_FD (NonMux) ********************
        # Gamma PVs for complete RX-message:
        self.OBDC_Waehlhebel_Resp_FD__length = GammaVarDeferred(gamma_api,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_RX.OBDC_Waehlhebel_Resp_FD.length")
        self.OBDC_Waehlhebel_Resp_FD__timestamp = GammaVarDeferred(gamma_api,
                                                                   "Waehlhebel:CAN.can0_HIL.HIL_RX.OBDC_Waehlhebel_Resp_FD.timestamp")
        # Gamma signal PVs (NonMux) for message:
        self.OBDC_Waehlhebel_Resp_FD__OBDC_Waehlhebel_Resp_FD_Data__value = GammaVarDeferred(gamma_api,
                                                                                             "Waehlhebel:CAN.can0_HIL.HIL_RX.OBDC_Waehlhebel_Resp_FD.signals.OBDC_Waehlhebel_Resp_FD_Data.value",
                                                                                             unit="")  # default="0"
        # ******************** OBDC_Waehlhebel_Req_FD (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.OBDC_Waehlhebel_Req_FD__length = GammaVarDeferred(gamma_api,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.OBDC_Waehlhebel_Req_FD.length")
        self.OBDC_Waehlhebel_Req_FD__timestamp = GammaVarDeferred(gamma_api,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.OBDC_Waehlhebel_Req_FD.timestamp")
        self.OBDC_Waehlhebel_Req_FD__period = GammaVarDeferred(gamma_api,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.OBDC_Waehlhebel_Req_FD.period", lookup={0: "aus", 1000000000: "an"})

        # Gamma signal PVs (NonMux) for message:
        self.OBDC_Waehlhebel_Req_FD__OBDC_Waehlhebel_Req_FD_Data__value = GammaVarDeferred(gamma_api,
                                                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.OBDC_Waehlhebel_Req_FD.signals.OBDC_Waehlhebel_Req_FD_Data.value",
                                                                                           unit="")  # default="0"

        # ******************** DIA_SAAM_Resp (NonMux) ********************
        # Gamma PVs for complete RX-message:
        self.DIA_SAAM_Resp__length = GammaVarDeferred(gamma_api,
                                                      "Waehlhebel:CAN.can0_HIL.HIL_RX.DIA_SAAM_Resp.length")
        self.DIA_SAAM_Resp__timestamp = GammaVarDeferred(gamma_api,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_RX.DIA_SAAM_Resp.timestamp")
        # Gamma signal PVs (NonMux) for message:
        self.DIA_SAAM_Resp__DIA_SAAM_Resp__value = GammaVarDeferred(gamma_api,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_RX.DIA_SAAM_Resp.signals.DIA_SAAM_Resp.value",
                                                                    unit="")  # default="0"

        # ******************** DIA_SAAM_Req (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.DIA_SAAM_Req__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.DIA_SAAM_Req.length")
        self.DIA_SAAM_Req__timestamp = GammaVarDeferred(gamma_api,
                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.DIA_SAAM_Req.timestamp")
        self.DIA_SAAM_Req__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.DIA_SAAM_Req.period",  lookup={0: "aus", 1000000000: "an"})

        # Gamma signal PVs (NonMux) for message:
        self.DIA_SAAM_Req__DIA_SAAM_Req_Data__value = GammaVarDeferred(gamma_api,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.DIA_SAAM_Req.signals.DIA_SAAM_Req_Data.value",
                                                                       unit="")  # default="0"

        # ******************** ISOx_Waehlhebel_Req_FD (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.ISOx_Waehlhebel_Req_FD__length = GammaVarDeferred(gamma_api,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Waehlhebel_Req_FD.length")
        self.ISOx_Waehlhebel_Req_FD__timestamp = GammaVarDeferred(gamma_api,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Waehlhebel_Req_FD.timestamp")
        self.ISOx_Waehlhebel_Req_FD__period = GammaVarDeferred(gamma_api,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Waehlhebel_Req_FD.period", lookup={0: "aus", 2000: "an"})

        # Gamma signal PVs (NonMux) for message:
        self.ISOx_Waehlhebel_Req_FD__ISOx_Waehlhebel_Req_FD_Data__value = GammaVarDeferred(gamma_api,
                                                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Waehlhebel_Req_FD.signals.ISOx_Waehlhebel_Req_FD_Data.value",
                                                                                           unit="")  # default="0"
        # ******************** ISOx_Waehlhebel_Resp_FD (NonMux) ********************
        # Gamma PVs for complete RX-message:
        self.ISOx_Waehlhebel_Resp_FD__length = GammaVarDeferred(gamma_api,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_RX.ISOx_Waehlhebel_Resp_FD.length")
        self.ISOx_Waehlhebel_Resp_FD__timestamp = GammaVarDeferred(gamma_api,
                                                                   "Waehlhebel:CAN.can0_HIL.HIL_RX.ISOx_Waehlhebel_Resp_FD.timestamp")
        # Gamma signal PVs (NonMux) for message:
        self.ISOx_Waehlhebel_Resp_FD__ISOx_Waehlhebel_Resp_FD_Data__value = GammaVarDeferred(gamma_api,
                                                                                             "Waehlhebel:CAN.can0_HIL.HIL_RX.ISOx_Waehlhebel_Resp_FD.signals.ISOx_Waehlhebel_Resp_FD_Data.value",
                                                                                             unit="")  # default="0"
        # ******************** ISOx_Funkt_Req_All_FD (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.ISOx_Funkt_Req_All_FD__length = GammaVarDeferred(gamma_api,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.length")
        self.ISOx_Funkt_Req_All_FD__timestamp = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.timestamp")
        self.ISOx_Funkt_Req_All_FD__period = GammaVarDeferred(gamma_api,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.period", lookup={0: "aus", 1000000000: "an"})

        # Gamma signal PVs (NonMux) for message:
        self.ISOx_Funkt_Req_All_FD__ISOx_Funkt_Req_All_FD_Data__algo = GammaVarDeferred(gamma_api,
                                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.signals.ISOx_Funkt_Req_All_FD_Data.algo",
                                                                                        unit="")  # default="0"
        self.ISOx_Funkt_Req_All_FD__ISOx_Funkt_Req_All_FD_Data__dyn_value_phy = GammaVarDeferred(gamma_api,
                                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.signals.ISOx_Funkt_Req_All_FD_Data.dyn_value_phy",
                                                                                                 unit="")  # default="0"
        self.ISOx_Funkt_Req_All_FD__ISOx_Funkt_Req_All_FD_Data__dyn_algo = GammaVarDeferred(gamma_api,
                                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.signals.ISOx_Funkt_Req_All_FD_Data.dyn_algo",
                                                                                            unit="")  # default="0"
        self.ISOx_Funkt_Req_All_FD__ISOx_Funkt_Req_All_FD_Data__dyn_count = GammaVarDeferred(gamma_api,
                                                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.signals.ISOx_Funkt_Req_All_FD_Data.dyn_count",
                                                                                             unit="")  # default="0"
        self.ISOx_Funkt_Req_All_FD__ISOx_Funkt_Req_All_FD_Data__dyn_pattern = GammaVarDeferred(gamma_api,
                                                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.signals.ISOx_Funkt_Req_All_FD_Data.dyn_pattern",
                                                                                               unit="")  # default="0"
        self.ISOx_Funkt_Req_All_FD__ISOx_Funkt_Req_All_FD_Data__mode = GammaVarDeferred(gamma_api,
                                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.signals.ISOx_Funkt_Req_All_FD_Data.mode",
                                                                                        unit="")  # default="0"
        self.ISOx_Funkt_Req_All_FD__ISOx_Funkt_Req_All_FD_Data__offset = GammaVarDeferred(gamma_api,
                                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.signals.ISOx_Funkt_Req_All_FD_Data.offset",
                                                                                          unit="")  # default="0"
        self.ISOx_Funkt_Req_All_FD__ISOx_Funkt_Req_All_FD_Data__static_value_phy = GammaVarDeferred(gamma_api,
                                                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.signals.ISOx_Funkt_Req_All_FD_Data.static_value_phy",
                                                                                                    unit="")  # default="0"
        self.ISOx_Funkt_Req_All_FD__ISOx_Funkt_Req_All_FD_Data__static_value_raw = GammaVarDeferred(gamma_api,
                                                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.signals.ISOx_Funkt_Req_All_FD_Data.static_value_raw",
                                                                                                    unit="")  # default="0"
        self.ISOx_Funkt_Req_All_FD__ISOx_Funkt_Req_All_FD_Data__value = GammaVarDeferred(gamma_api,
                                                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.ISOx_Funkt_Req_All_FD.signals.ISOx_Funkt_Req_All_FD_Data.value",
                                                                                         unit="")  # default="0"
        # ******************** ORU_Control_A_01 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.ORU_Control_A_01__length = GammaVarDeferred(gamma_api,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.length")
        self.ORU_Control_A_01__timestamp = GammaVarDeferred(gamma_api,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.timestamp")
        self.ORU_Control_A_01__period = GammaVarDeferred(gamma_api,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.period", lookup={0: "aus", 500: "an"}) # added the period

        # Gamma signal PVs (NonMux) for message:
        self.ORU_Control_A_01__OruIntegrityCheckActiveA__value = GammaVarDeferred(gamma_api,
                                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OruIntegrityCheckActiveA.value",
                                                                                  unit="")  # default="0"
        self.ORU_Control_A_01__ORU_Control_A_01_BZ__value = GammaVarDeferred(gamma_api,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.ORU_Control_A_01_BZ.value",
                                                                             unit="")  # default="0.0"
        self.ORU_Control_A_01__OruVehicleLockRequestA__value = GammaVarDeferred(gamma_api,
                                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OruVehicleLockRequestA.value",
                                                                                unit="")  # default="0"
        self.ORU_Control_A_01__OTA_FlgPTAcvPhdA__value = GammaVarDeferred(gamma_api,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OTA_FlgPTAcvPhdA.value",
                                                                          unit="")  # default="0"
        self.ORU_Control_A_01__ISignalVoid_ORU_Control_A_01_1__value = GammaVarDeferred(gamma_api,
                                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.ISignalVoid_ORU_Control_A_01_1.value",
                                                                                        unit="")  # default="0"
        self.ORU_Control_A_01__ISignalVoid_ORU_Control_A_01_0__value = GammaVarDeferred(gamma_api,
                                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.ISignalVoid_ORU_Control_A_01_0.value",
                                                                                        unit="")  # default="0"
        self.ORU_Control_A_01__OruControlStateA__value = GammaVarDeferred(gamma_api,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OruControlStateA.value",
                                                                          unit="")  # default="0"
        self.ORU_Control_A_01__OnlineRemoteUpdateControlOldA__value = GammaVarDeferred(gamma_api,
                                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OnlineRemoteUpdateControlOldA.value",
                                                                                       unit="")  # default="0"
        self.ORU_Control_A_01__OruControlReleaseA__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OruControlReleaseA.value",
                                                                            unit="Unit_None")  # default="0"
        self.ORU_Control_A_01__OnlineRemoteUpdateControlA__value = GammaVarDeferred(gamma_api,
                                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OnlineRemoteUpdateControlA.value",
                                                                                    unit="")  # default="0"
        self.ORU_Control_A_01__OruHostUpdateA__value = GammaVarDeferred(gamma_api,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OruHostUpdateA.value",
                                                                        unit="")  # default="0"
        self.ORU_Control_A_01__OruReleasePartitionSwitchA__value = GammaVarDeferred(gamma_api,
                                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.OruReleasePartitionSwitchA.value",
                                                                                    unit="")  # default="0"
        self.ORU_Control_A_01__ORU_Control_A_01_CRC__value = GammaVarDeferred(gamma_api,
                                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_A_01.signals.ORU_Control_A_01_CRC.value",
                                                                              unit="")  # default="0.0"

        # ******************** ORU_Control_D_01 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.ORU_Control_D_01__length = GammaVarDeferred(gamma_api,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.length")
        self.ORU_Control_D_01__timestamp = GammaVarDeferred(gamma_api,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.timestamp")
        self.ORU_Control_D_01__period = GammaVarDeferred(gamma_api,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.period", lookup={0: "aus", 320: "an"}) # added the period

        # Gamma signal PVs (NonMux) for message:
        self.ORU_Control_D_01__ORU_Control_D_01_BZ__value = GammaVarDeferred(gamma_api,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.ORU_Control_D_01_BZ.value",
                                                                             unit="")  # default="0"
        self.ORU_Control_D_01__OruVehicleLockRequestD__value = GammaVarDeferred(gamma_api,
                                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OruVehicleLockRequestD.value",
                                                                                unit="")  # default="0"
        self.ORU_Control_D_01__OruIntegrityCheckActiveD__value = GammaVarDeferred(gamma_api,
                                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OruIntegrityCheckActiveD.value",
                                                                                  unit="")  # default="0"
        self.ORU_Control_D_01__OruControlStateD__value = GammaVarDeferred(gamma_api,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OruControlStateD.value",
                                                                          unit="")  # default="0"
        self.ORU_Control_D_01__ISignalVoid_ORU_Control_D_01_1__value = GammaVarDeferred(gamma_api,
                                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.ISignalVoid_ORU_Control_D_01_1.value",
                                                                                        unit="")  # default="0"
        self.ORU_Control_D_01__OruControlReleaseD__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OruControlReleaseD.value",
                                                                            unit="Unit_None")  # default="0"
        self.ORU_Control_D_01__OnlineRemoteUpdateControlD__value = GammaVarDeferred(gamma_api,
                                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OnlineRemoteUpdateControlD.value",
                                                                                    unit="")  # default="0"
        self.ORU_Control_D_01__ISignalVoid_ORU_Control_D_01_0__value = GammaVarDeferred(gamma_api,
                                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.ISignalVoid_ORU_Control_D_01_0.value",
                                                                                        unit="")  # default="0"
        self.ORU_Control_D_01__OnlineRemoteUpdateControlOldD__value = GammaVarDeferred(gamma_api,
                                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OnlineRemoteUpdateControlOldD.value",
                                                                                       unit="")  # default="0"
        self.ORU_Control_D_01__OruHostUpdateD__value = GammaVarDeferred(gamma_api,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OruHostUpdateD.value",
                                                                        unit="")  # default="0"
        self.ORU_Control_D_01__OruReleasePartitionSwitchD__value = GammaVarDeferred(gamma_api,
                                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.OruReleasePartitionSwitchD.value",
                                                                                    unit="")  # default="0"
        self.ORU_Control_D_01__ORU_Control_D_01_CRC__value = GammaVarDeferred(gamma_api,
                                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_Control_D_01.signals.ORU_Control_D_01_CRC.value",
                                                                              unit="")  # default="0"
        # ******************** OTAMC_D_01 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.OTAMC_D_01__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.length")
        self.OTAMC_D_01__timestamp = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.timestamp")
        self.OTAMC_D_01__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.period", lookup={0: "aus", 320: "an"})

        # Gamma signal PVs (NonMux) for message:
        self.OTAMC_D_01__VehicleProtectedEnvironment_D__value = GammaVarDeferred(gamma_api,
                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.signals.VehicleProtectedEnvironment_D.value",
                                                                                 unit="")  # default="0"
        self.OTAMC_D_01__OTAMC_D_01_CRC__value = GammaVarDeferred(gamma_api,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.signals.OTAMC_D_01_CRC.value",
                                                                  unit="")  # default="0"
        self.OTAMC_D_01__ISignalVoid_OTAMC_D_01_0__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.signals.ISignalVoid_OTAMC_D_01_0.value",
                                                                            unit="")  # default="0"
        self.OTAMC_D_01__ISignalVoid_OTAMC_D_01_1__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.signals.ISignalVoid_OTAMC_D_01_1.value",
                                                                            unit="")  # default="0"
        self.OTAMC_D_01__ISignalVoid_OTAMC_D_01_2__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.signals.ISignalVoid_OTAMC_D_01_2.value",
                                                                            unit="")  # default="0"
        self.OTAMC_D_01__OTAMC_D_01_BZ__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_D_01.signals.OTAMC_D_01_BZ.value",
                                                                 unit="")  # default="0"


        # ******************** ORU_01 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.ORU_01__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_01.length")
        self.ORU_01__timestamp = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_01.timestamp")
        self.ORU_01__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_01.period", lookup={0: "aus", 500000: "an"}) # added the period

        # Gamma signal PVs (NonMux) for message:
        self.ORU_01__ORU_Status__value = GammaVarDeferred(gamma_api,
                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ORU_01.signals.ORU_Status.value",
                                                          unit="")  # default="0"

        # ******************** DS_Waehlhebel (NonMux) ********************
        # Gamma PVs for complete RX-message:
        self.DS_Waehlhebel__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.length")
        self.DS_Waehlhebel__timestamp = GammaVarDeferred(gamma_api,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.timestamp")
        # Gamma ignal PVs (NonMux) for message:
        self.DS_Waehlhebel__DS_Waehlhebel_StMemChanged__value = GammaVarDeferred(gamma_api,
                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_StMemChanged.value",
                                                                                 unit="")  # default="0"
        self.DS_Waehlhebel__DS_Waehlhebel_Lokalaktiv__value = GammaVarDeferred(gamma_api,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_Lokalaktiv.value",
                                                                               unit="")  # default="0"
        self.DS_Waehlhebel__DS_Waehlhebel_Subsystemaktiv__value = GammaVarDeferred(gamma_api,
                                                                                   "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_Subsystemaktiv.value",
                                                                                   unit="")  # default="0"
        self.DS_Waehlhebel__DS_Waehlhebel_DiagAdr__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_DiagAdr.value",
                                                                            unit="")  # default="0"0"
        self.DS_Waehlhebel__DS_Waehlhebel_IdentValid__value = GammaVarDeferred(gamma_api,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_IdentValid.value",
                                                                               unit="")  # default="0"0"
        self.DS_Waehlhebel__DS_Waehlhebel_MemSelChanged__value = GammaVarDeferred(gamma_api,
                                                                                  "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_MemSelChanged.value",
                                                                                  unit="")  # default="0"
        self.DS_Waehlhebel__DS_Waehlhebel_MemSel10Changed__value = GammaVarDeferred(gamma_api,
                                                                                    "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_MemSel10Changed.value",
                                                                                    unit="")  # default="0"
        self.DS_Waehlhebel__DS_Waehlhebel_ConfDTCChanged__value = GammaVarDeferred(gamma_api,
                                                                                   "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_ConfDTCChanged.value",
                                                                                   unit="")  # default="0"
        self.DS_Waehlhebel__DS_Waehlhebel_TestFailedChanged__value = GammaVarDeferred(gamma_api,
                                                                                      "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_TestFailedChanged.value",
                                                                                      unit="")  # default="0"
        self.DS_Waehlhebel__DS_Waehlhebel_WIRChanged__value = GammaVarDeferred(gamma_api,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_RX.DS_Waehlhebel.signals.DS_Waehlhebel_WIRChanged.value",
                                                                               unit="")  # default="0"

        # ******************** KN_Waehlhebel (NonMux) ********************
        # Gamma PVs for complete RX-message:
        self.KN_Waehlhebel__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.length")
        self.KN_Waehlhebel__timestamp = GammaVarDeferred(gamma_api,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.timestamp")
        # Gamma ignal PVs (NonMux) for message:
        self.KN_Waehlhebel__KN_Waehlhebel_DiagPfad__value = GammaVarDeferred(gamma_api,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.KN_Waehlhebel_DiagPfad.value",
                                                                             unit="")  # default="0"
        self.KN_Waehlhebel__Waehlhebel_Abschaltstufe__value = GammaVarDeferred(gamma_api,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.Waehlhebel_Abschaltstufe.value",
                                                                               unit="")  # default="0"
        self.KN_Waehlhebel__KN_Waehlhebel_BusKnockOut__value = GammaVarDeferred(gamma_api,
                                                                                "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.KN_Waehlhebel_BusKnockOut.value",
                                                                                unit="")  # default="0"
        self.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOutTimer__value = GammaVarDeferred(gamma_api,
                                                                                     "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.KN_Waehlhebel_ECUKnockOutTimer.value",
                                                                                     unit="")  # default="0"
        self.KN_Waehlhebel__Waehlhebel_KD_Fehler__value = GammaVarDeferred(gamma_api,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.Waehlhebel_KD_Fehler.value",
                                                                           unit="")  # default="0"
        self.KN_Waehlhebel__KN_Waehlhebel_ECUKnockOut__value = GammaVarDeferred(gamma_api,
                                                                                "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.KN_Waehlhebel_ECUKnockOut.value",
                                                                                unit="")  # default="0"
        self.KN_Waehlhebel__NM_Waehlhebel_FCIB__value = GammaVarDeferred(gamma_api,
                                                                         "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.NM_Waehlhebel_FCIB.value",
                                                                         unit="")  # default="10.0"
        self.KN_Waehlhebel__Waehlhebel_SNI_10__value = GammaVarDeferred(gamma_api,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.Waehlhebel_SNI_10.value",
                                                                        unit="")  # default="0.0"
        self.KN_Waehlhebel__NM_Waehlhebel_Subsystemaktiv__value = GammaVarDeferred(gamma_api,
                                                                                   "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.NM_Waehlhebel_Subsystemaktiv.value",
                                                                                   unit="")  # default="0"
        self.KN_Waehlhebel__Waehlhebel_Transport_Mode__value = GammaVarDeferred(gamma_api,
                                                                                "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.Waehlhebel_Transport_Mode.value",
                                                                                unit="")  # default="0"
        self.KN_Waehlhebel__NM_Waehlhebel_Lokalaktiv__value = GammaVarDeferred(gamma_api,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.NM_Waehlhebel_Lokalaktiv.value",
                                                                               unit="")  # default="0"
        self.KN_Waehlhebel__Waehlhebel_KompSchutz__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.Waehlhebel_KompSchutz.value",
                                                                            unit="")  # default="0""
        self.KN_Waehlhebel__Waehlhebel_Nachlauftyp__value = GammaVarDeferred(gamma_api,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.Waehlhebel_Nachlauftyp.value",
                                                                             unit="")  # default="2.0"
        self.KN_Waehlhebel__KN_Waehlhebel_BusKnockOutTimer__value = GammaVarDeferred(gamma_api,
                                                                                     "Waehlhebel:CAN.can0_HIL.HIL_RX.KN_Waehlhebel.signals.KN_Waehlhebel_BusKnockOutTimer.value",
                                                                                     unit="")  # default="0"

        # ******************** Waehlhebel_04 (NonMux) ********************
        # Gamma PVs for complete RX-message:
        self.Waehlhebel_04__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.length")
        self.Waehlhebel_04__timestamp = GammaVarDeferred(gamma_api,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.timestamp")
        # Gamma ignal PVs (NonMux) for message:
        self.Waehlhebel_04__Waehlhebel_04_CRC__value = GammaVarDeferred(gamma_api,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.Waehlhebel_04_CRC.value",
                                                                        unit="")  # default="0"
        self.Waehlhebel_04__WH_Zustand_N_Haltephase_2__value = GammaVarDeferred(gamma_api,
                                                                                "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.WH_Zustand_N_Haltephase_2.value",
                                                                                unit="")  # default="0""
        self.Waehlhebel_04__Waehlhebel_04_BZ__value = GammaVarDeferred(gamma_api,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.Waehlhebel_04_BZ.value",
                                                                       unit="")  # default="0"
        lookup_SensRoh = {4: "Pos_4", 5: "Pos_5", 6: "Pos_6", 7: "Pos_7", 8: "Pos_8", 9: "Pos_9", 10: "Pos_10" }
        self.Waehlhebel_04__WH_SensorPos_roh__value = GammaVarDeferred(gamma_api,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.WH_SensorPos_roh.value",
                                                                       unit="init", alias="SensorPosRoh", descr="WH Sensor Position roh Value",
                                                                       lookup=lookup_SensRoh,default=0, resettable=False)  # default="0"
        self.Waehlhebel_04__WH_Entsperrtaste_02__value = GammaVarDeferred(gamma_api,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.WH_Entsperrtaste_02.value",
                                                                          unit="")  # default="0"
        look_wh = {0: 'Init', 4: "nicht_betaetigt", 5: "D", 6: "N", 7: "R", 8: "P", 15: 'Fehler'}
        self.Waehlhebel_04__WH_Fahrstufe__value = GammaVarDeferred(gamma_api,
                                                                   "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.WH_Fahrstufe.value",
                                                                   unit="int", alias="FahrstufeControl", descr="Wunschfahrstufe", lookup=look_wh,
                                                                   default=0, resettable=False)  # default="0"
        self.Waehlhebel_04__WH_Zustand_N_Haltephase__value = GammaVarDeferred(gamma_api,
                                                                              "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.WH_Zustand_N_Haltephase.value",
                                                                              unit="")  # default="0"
        self.Waehlhebel_04__WH_P_Taste__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_RX.Waehlhebel_04.signals.WH_P_Taste.value",
                                                                 unit="")  # default="0"

        # ******************** NM_Waehlhebel (NonMux) ********************
        # Gamma PVs for complete RX-message:
        self.NM_Waehlhebel__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.length")
        self.NM_Waehlhebel__timestamp = GammaVarDeferred(gamma_api,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.timestamp")
        # Gamma ignal PVs (NonMux) for message:
        self.NM_Waehlhebel__NM_Waehlhebel_FCAB__value = GammaVarDeferred(gamma_api,
                                                                         "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_FCAB.value",
                                                                         unit="", lookup={0: 'Init', 1: '01_CarWakeUp',2: '02_Basefunction_Powertrain',
                                                                                          4: '03_Basefunction_Chassis', 5: '04_Basefunction_DrivingAssistance',
                                                                                          16: '05_Basefunction_Infotainment', 32: '06_Basefunction_ComfortLight',
                                                                                          64: '07_Basefunction_CrossSection', 128: '08_Basefunction_Connectivity',
                                                                                          256: '09_<reserved>', 512: '10_Powertrain', 1024: '11_Chassis',
                                                                                          2048: '12_GearSelector', 4096: '13_Airbag', 8192: '14_InfotainmentExtensions',
                                                                                          16384: '15_InstrumentclusterDisplay', 32768: '16_InfotainmentDisplay',
                                                                                          65536: '17_Audio', 131072: '18_VirtualSideMirrors', 262144: '19_Doors_Hatches',
                                                                                          524288: '20_OptionalComfort', 1048576: '21_AirSuspension',
                                                                                          2097152: '22_ExteriorLights', 4194304: '23_Climate', 8388608: '24_ThermoManagement',
                                                                                          16777216: '25_AccessSystemSensors', 33554432: '26_HighVoltage_Charging',
                                                                                          67108864: '27_Timemaster_Timer', 134217728: '28_OnboardTester_DataCollector',
                                                                                          268435456: '29_SteeringColumnLock', 536870912: '30_EnergyManagement',
                                                                                          1073741824: '31_MultifunctionalSteeringWheel', 2147483648: '56_Charging_Status',
                                                                                          })  # default="0"
        self.NM_Waehlhebel__NM_Waehlhebel_UDS_CC__value = GammaVarDeferred(gamma_api,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_UDS_CC.value",
                                                                           unit="", lookup={0: 'Inaktiv', 1: 'CC_aktiv'})  # default="0"
        self.NM_Waehlhebel__NM_Aktiv_N_Haltephase_abgelaufen__value = GammaVarDeferred(gamma_api,
                                                                                       "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Aktiv_N_Haltephase_abgelaufen.value",
                                                                                       unit="", lookup={0: 'Inaktiv', 1: 'Aktiv'})  # default="0"
        self.NM_Waehlhebel__NM_Waehlhebel_NM_State__value = GammaVarDeferred(gamma_api,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_NM_State.value",
                                                                             unit="",
                                                                             lookup={0: "Init", 1: "NM_RM_aus_BSM", 2: "NM_RM_aus_PBSM", 4: "NM_NO_aus_RM",
                                                                                     8: "NM_NO_aus_RS", 16: "reserved", 32: "reserved" })  # KMatrix 20210226
        self.NM_Waehlhebel__NM_Waehlhebel_SNI_10__value = GammaVarDeferred(gamma_api,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_SNI_10.value",
                                                                           unit="", lookup={83: 'Waehlhebel_SNI'})  # default="83.0"
        self.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Tmin__value = GammaVarDeferred(gamma_api,
                                                                                  "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_NM_aktiv_Tmin.value",
                                                                                  unit="", lookup={0: 'Inaktiv', 1: 'Mindestaktivzeit'})  # default="0"
        self.NM_Waehlhebel__NM_Waehlhebel_Wakeup_V12__value = GammaVarDeferred(gamma_api,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_Wakeup_V12.value",
                                                                               unit="", lookup={0: 'Peripherie_Wakeup_Ursache_nicht_bekannt', 1: 'Bus_Wakeup', 2: 'KL15_HW',
                                                                                                128: 'N_Haltephase_abgelaufen'})  # default="0"
        self.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_KL15__value = GammaVarDeferred(gamma_api,
                                                                                  "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_NM_aktiv_KL15.value",
                                                                                  unit="", lookup={0: 'NM_ohne_Clusteranforderunge', 1: 'KL15_EIN'})  # default="0"
        self.NM_Waehlhebel__NM_Waehlhebel_CBV_CRI__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_CBV_CRI.value",
                                                                            unit="", lookup={0: 'Inaktiv',
                                                                                             1: 'NM_mit_Clusteranforderungen'})  # default="1.0"
        self.NM_Waehlhebel__NM_Waehlhebel_CBV_AWB__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_CBV_AWB.value",
                                                                            unit="", lookup={0: "Passiver_WakeUp",
                                                                                             1: "Aktiver_WakeUp"})  # default="0"
        self.NM_Waehlhebel__NM_Waehlhebel_NM_aktiv_Diag__value = GammaVarDeferred(gamma_api,
                                                                                  "Waehlhebel:CAN.can0_HIL.HIL_RX.NM_Waehlhebel.signals.NM_Waehlhebel_NM_aktiv_Diag.value",
                                                                                  unit="", lookup={0: 'Inaktiv',
                                                                                                   1: 'Aktiv'})  # default="0"

        # ######################  TX message control ######################
        # ******************** OBD_03 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.OBD_03__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.length")
        self.OBD_03__timestamp = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.timestamp")
        self.OBD_03__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.period", lookup={0: "aus", 320: "an"}) # KMatrix20210226
        self.OBD_03__trigger = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.trigger")
        # Gamma ignal PVs (NonMux) for message:
        self.OBD_03__OBD_Eng_Cool_Temp__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Eng_Cool_Temp.value",
                                                                 unit="Unit_DegreCelsi")  # default="215.0"
        self.OBD_03__OBD_Driving_Cycle__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Driving_Cycle.value",
                                                                 unit="")  # default="0"
        self.OBD_03__OBD_Normed_Trip__value = GammaVarDeferred(gamma_api,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Normed_Trip.value",
                                                               unit="")  # default="0"
        self.OBD_03__OBD_Warm_Up_Cycle__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Warm_Up_Cycle.value",
                                                                 unit="")  # default="0"
        self.OBD_03__OBD_Aussen_Temp_gef__value = GammaVarDeferred(gamma_api,
                                                                   "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Aussen_Temp_gef.value",
                                                                   unit="Unit_DegreCelsi")  # default="55.0"
        self.OBD_03__OBD_Abs_Load_Val__value = GammaVarDeferred(gamma_api,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Abs_Load_Val.value",
                                                                unit="Unit_PerCent")  # default="6553.5"
        self.OBD_03__OBD_Abs_Throttle_Pos__value = GammaVarDeferred(gamma_api,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Abs_Throttle_Pos.value",
                                                                    unit="Unit_PerCent")  # default="99.45"
        self.OBD_03__OBD_Minimum_Trip__value = GammaVarDeferred(gamma_api,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Minimum_Trip.value",
                                                                unit="")  # default="0"
        self.OBD_03__OBD_Abs_Pedal_Pos__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_03.signals.OBD_Abs_Pedal_Pos.value",
                                                                 unit="Unit_PerCent")  # default="99.45"

        # ******************** NM_Airbag (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.NM_Airbag__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.length")
        self.NM_Airbag__timestamp = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.timestamp")
        self.NM_Airbag__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.period", lookup={0: "aus", 200: "an"}) # KMatrix20210226
        self.NM_Airbag__trigger = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.trigger")
        # Gamma ignal PVs (NonMux) for message:
        self.NM_Airbag__NM_Airbag_01_NM_State__value = GammaVarDeferred(gamma_api,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_NM_State.value",
                                                                        unit="")  # default="0"
        self.NM_Airbag__NM_Airbag_01_SNI_10__value = GammaVarDeferred(gamma_api,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_SNI_10.value",
                                                                      unit="")  # default="21.0"
        self.NM_Airbag__NM_Airbag_01_NM_aktiv_Tmin__value = GammaVarDeferred(gamma_api,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_NM_aktiv_Tmin.value",
                                                                             unit="")  # default="0"
        self.NM_Airbag__NM_Airbag_01_FCAB__value = GammaVarDeferred(gamma_api,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_FCAB.value",
                                                                    unit="")  # default="0"
        self.NM_Airbag__NM_aktiv_Gurtparken__value = GammaVarDeferred(gamma_api,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_aktiv_Gurtparken.value",
                                                                      unit="")  # default="0""
        self.NM_Airbag__NM_aktiv_Kl15_unplausibel__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_aktiv_Kl15_unplausibel.value",
                                                                            unit="")  # default="0"
        self.NM_Airbag__NM_Airbag_01_UDS_CC__value = GammaVarDeferred(gamma_api,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_UDS_CC.value",
                                                                      unit="")  # default="0"
        self.NM_Airbag__NM_Airbag_01_CBV_CRI__value = GammaVarDeferred(gamma_api,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_CBV_CRI.value",
                                                                       unit="")  # default="1.0"
        self.NM_Airbag__NM_aktiv_AntriebsCAN_aktiv__value = GammaVarDeferred(gamma_api,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_aktiv_AntriebsCAN_aktiv.value",
                                                                             unit="")  # default="0"
        self.NM_Airbag__NM_Airbag_01_NM_aktiv_Diag__value = GammaVarDeferred(gamma_api,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_NM_aktiv_Diag.value",
                                                                             unit="")  # default="0"
        self.NM_Airbag__NM_Airbag_01_CBV_AWB__value = GammaVarDeferred(gamma_api,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_CBV_AWB.value",
                                                                       unit="")  # default="0
        self.NM_Airbag__NM_aktiv_Ausloesefaehig__value = GammaVarDeferred(gamma_api,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_aktiv_Ausloesefaehig.value",
                                                                          unit="")  # default="0"
        self.NM_Airbag__NM_aktiv_Gurtschloss__value = GammaVarDeferred(gamma_api,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_aktiv_Gurtschloss.value",
                                                                       unit="")  # default="0"
        self.NM_Airbag__NM_Airbag_01_NM_aktiv_KL15__value = GammaVarDeferred(gamma_api,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_NM_aktiv_KL15.value",
                                                                             unit="")  # default="0"
        self.NM_Airbag__NM_aktiv_Sitzbelegung__value = GammaVarDeferred(gamma_api,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_aktiv_Sitzbelegung.value",
                                                                        unit="")  # default="0"
        self.NM_Airbag__NM_Airbag_01_Wakeup_V12__value = GammaVarDeferred(gamma_api,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_Airbag.signals.NM_Airbag_01_Wakeup_V12.value",
                                                                          unit="")  # default="0"

        # ******************** OBD_04 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.OBD_04__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.length")
        self.OBD_04__timestamp = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.timestamp")
        self.OBD_04__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.period", lookup={0: "aus", 320: "an"}) # KMatrix20210226
        self.OBD_04__trigger = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.trigger")
        # Gamma ignal PVs (NonMux) for message:
        self.OBD_04__OBD_Kaltstart_Denominator__value = GammaVarDeferred(gamma_api,
                                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_Kaltstart_Denominator.value",
                                                                         unit="")  # default="0"
        self.OBD_04__OBD_Sperrung_Kaltstart_Denom__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_Sperrung_Kaltstart_Denom.value",
                                                                            unit="")  # default="0"0"
        self.OBD_04__OBD_Sperrung_IUMPR__value = GammaVarDeferred(gamma_api,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_Sperrung_IUMPR.value",
                                                                  unit="")  # default="0"
        self.OBD_04__OBD_Calc_Load_Val__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_Calc_Load_Val.value",
                                                                 unit = "")
        self.OBD_04__OBD_ClearMem_Inhibit__value = GammaVarDeferred(gamma_api,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.OBD_ClearMem_Inhibit.value",
                                                                    unit="")  # default="0"
        self.OBD_04__MM_PropulsionSystemActive__value = GammaVarDeferred(gamma_api,
                                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.OBD_04.signals.MM_PropulsionSystemActive.value",
                                                                         unit="")  # default="0"

        # ******************** Dimmung_01 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.Dimmung_01__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.length")
        self.Dimmung_01__timestamp = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.timestamp")
        self.Dimmung_01__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.period", lookup={0: "aus", 200: "an"}) # KMatrix20210226
        self.Dimmung_01__trigger = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.trigger")
        # Gamma ignal PVs (NonMux) for message:
        self.Dimmung_01__DI_KL_58xd__value = GammaVarDeferred(gamma_api,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.signals.DI_KL_58xd.value",
                                                              unit="")  # default="200.0"
        self.Dimmung_01__DI_Fotosensor__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.signals.DI_Fotosensor.value",
                                                                 unit="")  # default="0"
        self.Dimmung_01__DI_Display_Nachtdesign__value = GammaVarDeferred(gamma_api,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.signals.DI_Display_Nachtdesign.value",
                                                                          unit="")  # default="0"
        self.Dimmung_01__DI_KL_58xt__value = GammaVarDeferred(gamma_api,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.signals.DI_KL_58xt.value",
                                                              unit="Unit_PerCent")  # default="100.0"
        self.Dimmung_01__BCM1_Stellgroesse_Kl_58s__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.signals.BCM1_Stellgroesse_Kl_58s.value",
                                                                            unit="")  # default="100.0"
        self.Dimmung_01__DI_KL_58xs__value = GammaVarDeferred(gamma_api,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.Dimmung_01.signals.DI_KL_58xs.value",
                                                              unit="Unit_PerCent")  # default="100.0"

        # ******************** SiShift_01 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.SiShift_01__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.SiShift_01.length")
        self.SiShift_01__timestamp = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.SiShift_01.timestamp")
        self.SiShift_01__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.SiShift_01.period", lookup={0: "aus", 20: "an"}) # KMatrix20210226
        self.SiShift_01__trigger = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.SiShift_01.trigger")
        # Gamma ignal PVs (NonMux) for message:
        self.SiShift_01__SIShift_StLghtDrvPosn__value = GammaVarDeferred(gamma_api,
                                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.SiShift_01.signals.SIShift_StLghtDrvPosn.value",
                                                                         unit="")  # default="0"
        self.SiShift_01__SIShift_FlgStrtNeutHldPha__value = GammaVarDeferred(gamma_api,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.SiShift_01.signals.SIShift_FlgStrtNeutHldPha.value",
                                                                             unit="")  # default="0"
        self.SiShift_01__SiShift_01_20ms_BZ__value = GammaVarDeferred(gamma_api,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.SiShift_01.signals.SiShift_01_20ms_BZ.value",
                                                                      unit="")  # default="0"
        self.SiShift_01__SiShift_01_20ms_CRC__value = GammaVarDeferred(gamma_api,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.SiShift_01.signals.SiShift_01_20ms_CRC.value",
                                                                       unit="")  # default="0"

        # ******************** Systeminfo_01 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.Systeminfo_01__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.length")
        self.Systeminfo_01__timestamp = GammaVarDeferred(gamma_api,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.timestamp")
        self.Systeminfo_01__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.period", lookup={0: "aus", 1000: "an"}) # KMatrix20210226
        self.Systeminfo_01__trigger = GammaVarDeferred(gamma_api,
                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.trigger")
        # Gamma ignal PVs (NonMux) for message:
        self.Systeminfo_01__SI_QRS_Mode__value = GammaVarDeferred(gamma_api,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_QRS_Mode.value",
                                                                  unit="")  # default="0"
        self.Systeminfo_01__SI_NWDF_30__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_NWDF_30.value",
                                                                 unit="")  # default="0"
        self.Systeminfo_01__SI_P_Mode__value = GammaVarDeferred(gamma_api,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_P_Mode.value",
                                                                unit="")  # default="0"
        self.Systeminfo_01__SI_NWDF_gueltig__value = GammaVarDeferred(gamma_api,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_NWDF_gueltig.value",
                                                                      unit="")  # default="1.0"
        self.Systeminfo_01__SI_T_Schutz__value = GammaVarDeferred(gamma_api,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_T_Schutz.value",
                                                                  unit="")  # default="0"
        self.Systeminfo_01__SI_P_Mode_gueltig__value = GammaVarDeferred(gamma_api,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_P_Mode_gueltig.value",
                                                                        unit="")  # default="0"
        self.Systeminfo_01__SI_NWDF__value = GammaVarDeferred(gamma_api,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_NWDF.value",
                                                              unit="")  # default="0"
        self.Systeminfo_01__SI_T_Mode__value = GammaVarDeferred(gamma_api,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.Systeminfo_01.signals.SI_T_Mode.value",
                                                                unit="")  # default="0"

        # ******************** NM_HCP1 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.NM_HCP1__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.length")
        self.NM_HCP1__timestamp = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.timestamp")
        self.NM_HCP1__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.period", lookup={0: "aus", 200: "an"}) # KMatrix20210226
        self.NM_HCP1__trigger = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.trigger")
        # Gamma ignal PVs (NonMux) for message:
        self.NM_HCP1__NM_HCP1_UDS_CC__value = GammaVarDeferred(gamma_api,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_UDS_CC.value",
                                                               unit="")  # default="0"
        self.NM_HCP1__NM_HCP1_FCAB__value = GammaVarDeferred(gamma_api,
                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_FCAB.value",
                                                             unit="")  # default="0"
        self.NM_HCP1__NM_aktiv_Niveauregelung__value = GammaVarDeferred(gamma_api,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_aktiv_Niveauregelung.value",
                                                                        unit="")  # default="0"
        self.NM_HCP1__NM_HCP1_SNI_10__value = GammaVarDeferred(gamma_api,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_SNI_10.value",
                                                               unit="")  # default="271.0"
        self.NM_HCP1__NM_aktiv_Parkanforderung__value = GammaVarDeferred(gamma_api,
                                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_aktiv_Parkanforderung.value",
                                                                         unit="")  # default="0"
        self.NM_HCP1__NM_aktiv_Stillstandsmanagement__value = GammaVarDeferred(gamma_api,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_aktiv_Stillstandsmanagement.value",
                                                                               unit="")  # default="0"
        self.NM_HCP1__NM_HCP1_CBV_CRI__value = GammaVarDeferred(gamma_api,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_CBV_CRI.value",
                                                                unit="")  # default="1.0"
        self.NM_HCP1__NM_HCP1_NM_aktiv_KL15__value = GammaVarDeferred(gamma_api,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_NM_aktiv_KL15.value",
                                                                      unit="")  # default="0"
        self.NM_HCP1__NM_HCP1_NM_aktiv_Tmin__value = GammaVarDeferred(gamma_api,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_NM_aktiv_Tmin.value",
                                                                      unit="")  # default="0"
        self.NM_HCP1__NM_aktiv_Halteanforderung__value = GammaVarDeferred(gamma_api,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_aktiv_Halteanforderung.value",
                                                                          unit="")  # default="0""
        self.NM_HCP1__NM_HCP1_CBV_AWB__value = GammaVarDeferred(gamma_api,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_CBV_AWB.value",
                                                                unit="")  # default="0"
        self.NM_HCP1__NM_HCP1_NM_aktiv_Diag__value = GammaVarDeferred(gamma_api,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_NM_aktiv_Diag.value",
                                                                      unit="")  # default="0"
        self.NM_HCP1__NM_HCP1_NM_State__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_NM_State.value",
                                                                 unit="")  # default="0"
        self.NM_HCP1__NM_HCP_1_Wakeup_V12__value = GammaVarDeferred(gamma_api,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP_1_Wakeup_V12.value",
                                                                    unit="")  # default="0"
        self.NM_HCP1__NM_HCP1_NM_aktiv_CABaktiv__value = GammaVarDeferred(gamma_api,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.NM_HCP1.signals.NM_HCP1_NM_aktiv_CABaktiv.value",
                                                                          unit="")  # default="0"

        # ******************** OTAMC_01 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.OTAMC_01__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_01.length")
        self.OTAMC_01__timestamp = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_01.timestamp")
        self.OTAMC_01__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_01.period", lookup={0: "aus", 960: "an"}) # KMatrix20210226 # added correct period
        self.OTAMC_01__trigger = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_01.trigger")
        # Gamma ignal PVs (NonMux) for message:
        self.OTAMC_01__VPE_State__value = GammaVarDeferred(gamma_api,
                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_01.signals.VPE_State.value",
                                                           unit="")  # default="0"
        self.OTAMC_01__OTAMC_01_BZ__value = GammaVarDeferred(gamma_api,
                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_01.signals.OTAMC_01_BZ.value",
                                                             unit="")  # default="0"
        self.OTAMC_01__OTA_State__value = GammaVarDeferred(gamma_api,
                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_01.signals.OTA_State.value",
                                                           unit="")  # default="0"
        self.OTAMC_01__OTAMC_01_CRC__value = GammaVarDeferred(gamma_api,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.OTAMC_01.signals.OTAMC_01_CRC.value",
                                                              unit="")  # default="0"

        # ******************** VDSO_05 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.VDSO_05__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.length")
        self.VDSO_05__timestamp = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.timestamp")
        self.VDSO_05__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.period", lookup={0: "aus", 20: "an"}) # KMatrix20210226 # changed from 5 to 20ms as defined in the gamma
        self.VDSO_05__trigger = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.trigger")
        # Gamma ignal PVs (NonMux) for message:
        self.VDSO_05__VDSO_Vx3d__value = GammaVarDeferred(gamma_api,
                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.signals.VDSO_Vx3d.value",
                                                          unit="Unit_MeterPerSecon")  # default="0.0"
        self.VDSO_05__VDSO_05_CRC__value = GammaVarDeferred(gamma_api,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.signals.VDSO_05_CRC.value",
                                                            unit="")  # default="0"
        self.VDSO_05__VDSO_Vx3dKmph__value = GammaVarDeferred(gamma_api,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.signals.VDSO_Vx3dKmph.value",
                                                              unit="Unit_KiloMeterPerHour")  # default="65533.8571429""
        self.VDSO_05__VDSO_05_BZ__value = GammaVarDeferred(gamma_api,
                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.signals.VDSO_05_BZ.value",
                                                           unit="")  # default="0"
        self.VDSO_05__VDSO_BasTi200_NumClc__value = GammaVarDeferred(gamma_api,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.signals.VDSO_BasTi200_NumClc.value",
                                                                     unit="")  # default="0"
        self.VDSO_05__VDSO_Vx3dDisp__value = GammaVarDeferred(gamma_api,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.VDSO_05.signals.VDSO_Vx3dDisp.value",
                                                              unit="")  # default="0"

        # ******************** DPM_01 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.DPM_01__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.length")
        self.DPM_01__timestamp = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.timestamp")
        self.DPM_01__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.period", lookup={0: "aus", 1000000000000000000000000000000000: "an"}) # KMatrix20210226
        self.DPM_01__trigger = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.trigger")
        # Gamma ignal PVs (NonMux) for message:
        self.DPM_01__DPM_StTarDrvPosn__value = GammaVarDeferred(gamma_api,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_StTarDrvPosn.value",
                                                                unit="")  # default="0"
        self.DPM_01__DPM_StSrcTarDrvPosn__value = GammaVarDeferred(gamma_api,
                                                                   "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_StSrcTarDrvPosn.value",
                                                                   unit="")  # default="0"
        self.DPM_01__DPM_FlgStrtNeutHldPha__value = GammaVarDeferred(gamma_api,
                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_FlgStrtNeutHldPha.value",
                                                                     unit="")  # default="0"
        self.DPM_01__DPM_01_BZ__value = GammaVarDeferred(gamma_api,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_01_BZ.value",
                                                         unit="")  # default="0"
        self.DPM_01__DPM_StReqVld_VMMscnd__value = GammaVarDeferred(gamma_api,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_StReqVld_VMMscnd.value",
                                                                    unit="")  # default="0"
        self.DPM_01__DPM_01_CRC__value = GammaVarDeferred(gamma_api,
                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_01_CRC.value",
                                                          unit="")  # default="0"
        self.DPM_01__DPM_StLghtDrvPosn__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.DPM_01.signals.DPM_StLghtDrvPosn.value",
                                                                 unit="")  # default="0"

        # ******************** Diagnose_01 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.Diagnose_01__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.length")
        self.Diagnose_01__timestamp = GammaVarDeferred(gamma_api,
                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.timestamp")
        self.Diagnose_01__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.period", lookup={0: "aus", 1000: "an"}) # KMatrix20210226
        self.Diagnose_01__trigger = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.trigger")
        # Gamma ignal PVs (NonMux) for message:
        self.Diagnose_01__UH_Monat__value = GammaVarDeferred(gamma_api,
                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.UH_Monat.value",
                                                             unit="Unit_Month")  # default="0"
        self.Diagnose_01__UH_Minute__value = GammaVarDeferred(gamma_api,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.UH_Minute.value",
                                                              unit="Unit_Minut")  # default="0"
        self.Diagnose_01__UH_Tag__value = GammaVarDeferred(gamma_api,
                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.UH_Tag.value",
                                                           unit="Unit_Day")  # default="0"
        self.Diagnose_01__Vehicle_Driving_Cycle__value = GammaVarDeferred(gamma_api,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.Vehicle_Driving_Cycle.value",
                                                                          unit="")  # default="0"
        self.Diagnose_01__DW_Kilometerstand__value = GammaVarDeferred(gamma_api,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.DW_Kilometerstand.value",
                                                                      unit="Unit_KiloMeter")  # default="1048574.0"
        self.Diagnose_01__UH_Stunde__value = GammaVarDeferred(gamma_api,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.UH_Stunde.value",
                                                              unit="Unit_Hours")  # default="0"
        self.Diagnose_01__DGN_Verlernzaehler__value = GammaVarDeferred(gamma_api,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.DGN_Verlernzaehler.value",
                                                                       unit="")  # default="0"
        self.Diagnose_01__UH_Jahr__value = GammaVarDeferred(gamma_api,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.UH_Jahr.value",
                                                            unit="Unit_Year")  # default="2000"
        self.Diagnose_01__UH_Sekunde__value = GammaVarDeferred(gamma_api,
                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.Diagnose_01.signals.UH_Sekunde.value",
                                                               unit="Unit_Secon")  # default="0"

        # ******************** ClampControl_01 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.ClampControl_01__length = GammaVarDeferred(gamma_api,
                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.length")
        self.ClampControl_01__timestamp = GammaVarDeferred(gamma_api,
                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.timestamp")
        self.ClampControl_01__period = GammaVarDeferred(gamma_api,
                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.period", lookup={0: "aus", 100: "an"}) # KMatrix20210226
        self.ClampControl_01__trigger = GammaVarDeferred(gamma_api,
                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.trigger")
        # Gamma ignal PVs (NonMux) for message:

        self.ClampControl_01__KST_Fahrerhinweis_4__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Fahrerhinweis_4.value",
                                                                            unit="")  # default="0"
        self.ClampControl_01__KST_Fahrerhinweis_5__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Fahrerhinweis_5.value",
                                                                            unit="")  # default="0""
        self.ClampControl_01__KST_Fahrerhinweis_6__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Fahrerhinweis_6.value",
                                                                            unit="")  # default="0"
        self.ClampControl_01__KST_Sonderzustand_Anforderung__value = GammaVarDeferred(gamma_api,
                                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Sonderzustand_Anforderung.value",
                                                                                      unit="")  # default="0"
        self.ClampControl_01__KST_Fahrerhinweis_1__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Fahrerhinweis_1.value",
                                                                            unit="")  # default="0"
        self.ClampControl_01__KST_Fahrerhinweis_2__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Fahrerhinweis_2.value",
                                                                            unit="")  # default="0"
        self.ClampControl_01__KST_Current_State__value = GammaVarDeferred(gamma_api,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Current_State.value",
                                                                          unit="")  # default="0"
        self.ClampControl_01__KST_ComfortReadyStatus__value = GammaVarDeferred(gamma_api,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_ComfortReadyStatus.value",
                                                                               unit="")  # default="0"
        self.ClampControl_01__KST_StPtDeacReq__value = GammaVarDeferred(gamma_api,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_StPtDeacReq.value",
                                                                        unit="")  # default="0"
        self.ClampControl_01__KST_Fahrerhinweis_3__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Fahrerhinweis_3.value",
                                                                            unit="")  # default="0"
        self.ClampControl_01__KST_BulbCheckReq__value = GammaVarDeferred(gamma_api,
                                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_BulbCheckReq.value",
                                                                         unit="")  # default="0"
        self.ClampControl_01__KST_Target_Function__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Target_Function.value",
                                                                            unit="")  # default="0"
        self.ClampControl_01__KST_Txt_Panikabschaltung__value = GammaVarDeferred(gamma_api,
                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Txt_Panikabschaltung.value",
                                                                                 unit="")  # default="0"
        self.ClampControl_01__KST_Target_Mode__value = GammaVarDeferred(gamma_api,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Target_Mode.value",
                                                                        unit="")  # default="0"
        self.ClampControl_01__KST_Kl_50_Startanforderung__value = GammaVarDeferred(gamma_api,
                                                                                   "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Kl_50_Startanforderung.value",
                                                                                   unit="")  # default="0"
        self.ClampControl_01__KST_Kl_X__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Kl_X.value",
                                                                 unit="")  # default="0"
        self.ClampControl_01__KST_StPtAcvReq__value = GammaVarDeferred(gamma_api,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_StPtAcvReq.value",
                                                                       unit="")  # default="0"
        self.ClampControl_01__KST_Kl_S__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Kl_S.value",
                                                                 unit="")  # default="0"
        self.ClampControl_01__KST_WFS_Fahrfreigabe_Anforderung__value = GammaVarDeferred(gamma_api,
                                                                                         "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_WFS_Fahrfreigabe_Anforderung.value",
                                                                                         unit="")  # default="0"
        self.ClampControl_01__KST_Ausstiegswunsch_Status__value = GammaVarDeferred(gamma_api,
                                                                                   "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Ausstiegswunsch_Status.value",
                                                                                   unit="")  # default="0"
        self.ClampControl_01__ClampControl_01_BZ__value = GammaVarDeferred(gamma_api,
                                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.ClampControl_01_BZ.value",
                                                                           unit="")  # default="0"
        self.ClampControl_01__KST_Remotestart_KL15_Anf__value = GammaVarDeferred(gamma_api,
                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Remotestart_KL15_Anf.value",
                                                                                 unit="")  # default="0"
        self.ClampControl_01__KST_Ausparken_Betrieb__value = GammaVarDeferred(gamma_api,
                                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Ausparken_Betrieb.value",
                                                                              unit="")  # default="0"

        self.ClampControl_01__KST_Deaktivierungs_Trigger__value = GammaVarDeferred(gamma_api,
                                                                                   "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Deaktivierungs_Trigger.value",
                                                                                   unit="")  # default="0"
        self.ClampControl_01__KST_ZAT_betaetigt__value = GammaVarDeferred(gamma_api,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_ZAT_betaetigt.value",
                                                                          unit="")  # default="0"
        self.ClampControl_01__KST_Anf_Klemmenfreigabe_ELV__value = GammaVarDeferred(gamma_api,
                                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Anf_Klemmenfreigabe_ELV.value",
                                                                                    unit="")  # default="0"
        self.ClampControl_01__KST_aut_Abschaltung_Zuendung__value = GammaVarDeferred(gamma_api,
                                                                                     "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_aut_Abschaltung_Zuendung.value",
                                                                                     unit="")  # default="0"
        self.ClampControl_01__ClampControl_01_CRC__value = GammaVarDeferred(gamma_api,
                                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.ClampControl_01_CRC.value",
                                                                            unit="")  # default="0"
        self.ClampControl_01__KST_KL_15__value = GammaVarDeferred(gamma_api,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_KL_15.value",
                                                                  unit="")  # default="0"
        self.ClampControl_01__KST_Sonderzustand_Status__value = GammaVarDeferred(gamma_api,
                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.ClampControl_01.signals.KST_Sonderzustand_Status.value",
                                                                                 unit="")  # default="0"

        # ******************** NVEM_12 (NonMux) ********************
        # Gamma PVs for complete TX-message:
        self.NVEM_12__length = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.length")
        self.NVEM_12__timestamp = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.timestamp")
        self.NVEM_12__period = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.period", lookup={0: "aus", 100: "an"}) # KMatrix20210226
        self.NVEM_12__trigger = GammaVarDeferred(gamma_api, "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.trigger")
        # Gamma ignal PVs (NonMux) for message:
        self.NVEM_12__BEM_STH_Einschaltverbot__value = GammaVarDeferred(gamma_api,
                                                                        "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.BEM_STH_Einschaltverbot.value",
                                                                        unit="")  # default="0"
        self.NVEM_12__NVEM_Abschaltstufe__value = GammaVarDeferred(gamma_api,
                                                                   "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_Abschaltstufe.value",
                                                                   unit="")  # default="0"0"
        self.NVEM_12__BEM_Batt_Ab__value = GammaVarDeferred(gamma_api,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.BEM_Batt_Ab.value",
                                                            unit="")  # default="0"
        self.NVEM_12__NVEM_DC_iSoll_NV__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_DC_iSoll_NV.value",
                                                                 unit="Unit_Amper")  # default="254.0"
        self.NVEM_12__NVEM_NV_BAT_ZellStatus_Index_Anf__value = GammaVarDeferred(gamma_api,
                                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_NV_BAT_ZellStatus_Index_Anf.value",
                                                                                 unit="")  # default="0"
        self.NVEM_12__NVEM_DC_uSoll_NV__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_DC_uSoll_NV.value",
                                                                 unit="Unit_Volt")  # default="16.0"
        self.NVEM_12__NVEM_Last_Anf__value = GammaVarDeferred(gamma_api,
                                                              "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_Last_Anf.value",
                                                              unit="")  # default="0"
        self.NVEM_12__BEM_STH_Zielzeit__value = GammaVarDeferred(gamma_api,
                                                                 "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.BEM_STH_Zielzeit.value",
                                                                 unit="Unit_Minut")  # default="14.0"
        self.NVEM_12__NVEM_Bordnetzdiagnose__value = GammaVarDeferred(gamma_api,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_Bordnetzdiagnose.value",
                                                                      unit="")  # default="0"
        self.NVEM_12__NVEM_Bordnetz_Information__value = GammaVarDeferred(gamma_api,
                                                                          "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_Bordnetz_Information.value",
                                                                          unit="")  # default="14.0"
        self.NVEM_12__BEM_HL_Regelung_Status__value = GammaVarDeferred(gamma_api,
                                                                       "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.BEM_HL_Regelung_Status.value",
                                                                       unit="")  # default="0""
        self.NVEM_12__NVEM_NV_BAT_ZellStatus_Typ_Anf__value = GammaVarDeferred(gamma_api,
                                                                               "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_NV_BAT_ZellStatus_Typ_Anf.value",
                                                                               unit="")  # default="0"
        self.NVEM_12__NVEM_MV_DC_iSoll_NV__value = GammaVarDeferred(gamma_api,
                                                                    "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_MV_DC_iSoll_NV.value",
                                                                    unit="Unit_Amper")  # default="254.0"
        self.NVEM_12__NVEM_MV_DC_uSollLV__value = GammaVarDeferred(gamma_api,
                                                                   "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_MV_DC_uSollLV.value",
                                                                   unit="Unit_Volt")  # default="12.0"
        self.NVEM_12__NVEM_DC_uMin_NV__value = GammaVarDeferred(gamma_api,
                                                                "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_DC_uMin_NV.value",
                                                                unit="Unit_Volt")  # default="10.0"
        self.NVEM_12__NVEM_MV_DC_uMinLV__value = GammaVarDeferred(gamma_api,
                                                                  "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_MV_DC_uMinLV.value",
                                                                  unit="Unit_Volt")  # default="3.5"
        self.NVEM_12__BEM_Red_Innengeblaese__value = GammaVarDeferred(gamma_api,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.BEM_Red_Innengeblaese.value",
                                                                      unit="")  # default="0"
        self.NVEM_12__NVEM_12_CRC__value = GammaVarDeferred(gamma_api,
                                                            "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_12_CRC.value",
                                                            unit="")  # default="0"
        self.NVEM_12__BEM_Generatordiagnose__value = GammaVarDeferred(gamma_api,
                                                                      "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.BEM_Generatordiagnose.value",
                                                                      unit="")  # default="0"
        self.NVEM_12__NVEM_Verbraucher_Information__value = GammaVarDeferred(gamma_api,
                                                                             "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_Verbraucher_Information.value",
                                                                             unit="")  # default="6.0"
        self.NVEM_12__NVEM_12_BZ__value = GammaVarDeferred(gamma_api,
                                                           "Waehlhebel:CAN.can0_HIL.HIL_TX.NVEM_12.signals.NVEM_12_BZ.value",
                                                           unit="")  # default="0"

        # Variables on HIL #############################################################################################
        # lookup tables -------------------------------------------------------
        lookup_bool = {0: "Off", 1: "On"}

        # Power supply
        self.vbat_cl30__V = GammaVarDeferred(gamma_api,
                                             'Waehlhebel:UserInterface.IOWrite.PowerSupplyWrite.vbat_cl30__V',
                                             unit="V",
                                             alias="BatteryCurrent",
                                             descr="Manipulate the power supply to simulate expected battery voltage.",
                                             default=13.0,
                                             fmt="%.2f")
        self.current_cl30__A = GammaVarDeferred(gamma_api,
                                                'Waehlhebel:UserInterface.IOWrite.PowerSupplyWrite.current_cl30__A',
                                                unit="A",
                                                alias="BatteryCurrent",
                                                descr="Manipulate the limitation of power supply current to control current flow.",
                                                default=10.0,
                                                fmt="%.2f")
        # clamp control
        self.cl30_on__ = GammaVarDeferred(gamma_api, 'Waehlhebel:UserInterface.IOWrite.PowerSupplyWrite.cl30_on__',
                                          unit="bool",
                                          alias="Clamp30Controm",
                                          descr="De/Activate clamp 30 relay to supply and wake up ecu.",
                                          lookup=lookup_bool,
                                          default=False,
                                          resettable=False
                                          )
        self.cl15_on__ = GammaVarDeferred(gamma_api, 'Waehlhebel:UserInterface.IOWrite.PowerSupplyWrite.cl15_on__',
                                          unit="bool",
                                          alias="Clamp15Control",
                                          descr="De/Activate clamp 15 relay to supply and wake up ecu.",
                                          lookup=lookup_bool,
                                          default=False,
                                          resettable=False)
        self.supply_sense__ = GammaVarDeferred(gamma_api,
                                               'Waehlhebel:UserInterface.IOWrite.PowerSupplyWrite.supply_sense__',
                                               unit="bool",
                                               alias="SenseWireControl",
                                               descr="De/Activate Sense Wire on and off ",
                                               lookup=lookup_bool,
                                               default=False,
                                               resettable=False)
        # power supply monitoring
        self.cc_mon__A = GammaVarDeferred(gamma_api,
                                               'Waehlhebel:UserInterface.IORead.PowerSupplyRead.cc_mon__A',
                                               unit="A",
                                               alias="CC Monitor A",
                                               descr="current monitored ampere",
                                               default=False,
                                               resettable=False)

        # Failure Injection on HIL #####################################################################################
        self.error_type = GammaVarDeferred(gamma_api,
                                           'Waehlhebel:UserInterface.IOWrite.FIUWrite.error_type',
                                           alias="Error type",
                                           descr="0::No Error, 1::Open_Circuit,2::one_Short_circuit_Error,3::two_Short_circuit_Error",
                                           lookup={0: 'No Error', 1: 'Open_Circuit', 2: 'one_Short_circuit_Error',
                                                   3: 'two_Short_circuit_Error'},
                                           default=0,
                                           resettable=True)

        self.load_number_select = GammaVarDeferred(gamma_api,
                                                   'Waehlhebel:UserInterface.IOWrite.FIUWrite.load_single_error',
                                                   descr="Last number selection",
                                                   default=0,
                                                   resettable=True)

        self.second_load_number_select = GammaVarDeferred(gamma_api,
                                                          'Waehlhebel:UserInterface.IOWrite.FIUWrite.second_load_single_error',
                                                          descr="Second Last number selection",
                                                          default=0,
                                                          resettable=True)

        self.bus_physical_error = GammaVarDeferred(gamma_api,
                                                   'Waehlhebel:UserInterface.IOWrite.FIUWrite.BusPhysicalError',
                                                   descr="Bus Physical Error",
                                                   lookup={0: "No Error", 1: "CAN_1_H Break", 2: "CAN_1_L Break",
                                                           3: "CAN_1_H EI1", 4: "CAN_1_L EI1",
                                                           5: "short_CAN_1_L_CAN_1_H"},
                                                   default=0,
                                                   resettable=True)
# #############################################################################
#
# #############################################################################


if __name__ == '__main__':
    pass
