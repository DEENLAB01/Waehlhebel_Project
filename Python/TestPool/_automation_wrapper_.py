# ******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : _automation_wrapper_.py
# Task    : Basic functionality and definitions for test automation
# Author  : Mohammed Abdul Karim
# Date    : 14.12.2020
# Copyright 2011 - 2020 Eissmann Automotive Deutschland GmbH
#
# ******************************************************************************
# ********************************* Version ************************************
# ******************************************************************************
# Rev. | Date       | Name      | Description
# ------------------------------------------------------------------------------
# 1.0  | 14.12.2020 | Abdul Karim   | initial, adapted from template.
# 1.1  | 17.05.2021 | NeumannA  | fix some bugs in shutdown ECU
# 1.2  | 18.05.2021 | StengerS  | added CANapeDiagnosis in getCanapeDiagnostic
# 1.3  | 20.05.2021 | NeumannA  | add offline stubs and header for testcase
# 1.4  | 21.05.2021 | NeumannA  | add GammaDaq Instance
# 1.5  | 25.08.2021 | Mushtaq   | add Can bus variables Instance
# ******************************************************************************
# basic libraries
import os
import sys
import time
import inspect

# initialize path to test support libraries
_test_support_path = r'D:\Programme\iTestStudio\libraries\test_support27.pyz'  # iTestStudio
_test_support_path = os.path.join(  # iTestStudio
    os.getenv("ITESTSTUDIO_PATH", ""), "libraries",
    "test_support%d%d.pyz" % sys.version_info[0:2]  # auto-select matching support-libs
)
# derive project base path from this script's folder
_test_pool_path = os.path.realpath(inspect.currentframe().f_code.co_filename)
_test_pool_path = os.path.dirname(_test_pool_path)  # module located in testpool folder
_base_project_path = os.path.dirname(_test_pool_path)  # parent is python project folder
_base_project_path = os.path.dirname(_base_project_path)  # parent is main/base project folder

# #######################################
# Import Test Environment
# #######################################
_test_support_path = os.path.normpath(_test_support_path)
if _test_support_path not in sys.path:
    # insert test support in search order right after the "current" folder
    sys.path.insert(1, _test_support_path)

from test_environment import TestEnvironmentBase  # @UnresolvedImport, part of test_support
from test_environment import sleepWithFeedback, appendSysPath, getConfig  # @UnresolvedImport

# if you want to get the _test_libs_folder_name from configuration:
# get configured folder paths
config = getConfig(_base_project_path)
if _test_pool_path != config.getAbsPath("FOLDERS", "test_pool"):
    print "> please check test pool path configured in hil_project.ini"
_test_libs_path = config.getAbsPath("FOLDERS", "test_libs")
# alternatively, you could of course just keep the libs path hardcoded (K.I.S.S.)
# #######################################
# Project Libraries
# #######################################
appendSysPath(_test_libs_path)

# #######################################
# Project-specific Modules
# #######################################
import hil_variables
import cal_variables
import can_bus_variables
import data_common
from functions_diag import CANapeDiagnosis
from functions_daq import FunctionsDaq

if os.getenv('COMPUTERNAME') in data_common.CONTROL_COMPUTER_NAMES:
    # "online" libs ###############################################################
    from ttk_tools.vector import canapeapi
    from ttk_tools.rst import gamma_api

    hil_name = os.getenv('COMPUTERNAME')
else:
    # offline stubs ###############################################################
    import ttk_tools.vector.canapeapi_offline_stub as canapeapi
    import ttk_tools.rst.gamma_api_offline_stub    as gamma_api

    hil_name = "%s (offline stubs)" % os.getenv('COMPUTERNAME')


# #############################################################################
# Test Environment
# #############################################################################
class TestEnv(TestEnvironmentBase):
    """ Test environment automation access helper/wrapper. """

    # #########################################################################
    def __init__(self, test_script_name=None):
        """ TestEnv base initialization.

            Parameters:
                test_script_name - name of the current test script in test pool.
                                   Optional; if not supplied, TestEnvironment
                                   will determine the script name by inspecting
                                   the frame stack.
        """
        # Ensure that all required lib paths are present in sys.path
        # Note: The above init on module level will only get executed on first
        #       import. We had occasional issues during (pre-iTS automation)
        #       test series runs, with sys.path reverting to its default
        #       entries between test scripts while this module remained
        #       properly loaded.
        #       This specific issue should not longer occur in the current
        #       implementation, but better safe than sorry.
        appendSysPath(_test_support_path)
        appendSysPath(_test_libs_path)

        # init base class
        TestEnvironmentBase.__init__(self, _base_project_path, test_script_name)

        # prepare member variables that will be used later
        self.gamma = None  # hil real-time application
        self.gamma_daq = None
        self.daq = None  # data acquisition
        self.asap3 = None  # canape's base asap3 handle
        self.canape_cal = None  # canape_cal: ccp/xcp device
        self.canape_can = None  # canape_can: can device
        self.canape_arxml = None  # canape_arxml CAN FD
        self.canape_Diagnostic = None
        self.hil = None  # hil variables container
        self.cal = None  # cal variables container
        self.can_bus = None  # Can bus variables container

        # instances_to_cleanup:
        # Add classes for which the wrapper should attempt to cleanup any
        # leftover instances during breakdown:
        self.instances_to_cleanup = [
            canapeapi.CANapeDevice,
            canapeapi.CANapeASAP3,
            canapeapi.DataAcquisition,
            hil_variables.HilVars,  # note that this will also clean up
            cal_variables.CalVars,  # instances of derived child classes
            can_bus_variables.CanBusSignals,
        ]

    # #########################################################################
    def setup(self):
        """ Test Setup: initialize test environment. """
        TestEnvironmentBase.setup(self)

        # datamodel_path = os.path.join(_base_project_path, "Datamodel")
        datamodel_path = os.path.join(_base_project_path, "Datamodel")
        config_file = os.path.join(datamodel_path, "winconfig.xml")

        self.gamma = gamma_api.Gamma(
            system_file=None,
            config_file=config_file,
            system_name_local="Steuer_PC",  # required if system_file not used
            system_name_remote="Waehlhebel",
            keep_gamma_alive=True,
            timeout_ms=5000,
        )

        # initialize hil variables with the real-time system
        self.hil = hil_variables.HilVars(self.gamma.getReference())
        # print (self.hil)
        self.can_bus = can_bus_variables.CanBusSignals(self.gamma.getReference())

        # cal variables will be later initialized on-demand:
        self.cal = None

        self.getResults().append([
            "\nHIL Information:\n"
            "Project: %(project)s \nHil Name: %(name)s" % {
                "project": data_common.project_name,
                "name": hil_name},
            "INFO"])

    # #########################################################################
    def breakdown(self, ecu_shutdown=True):
        """ Test breakdown: cleanup & housekeeping. """

        # restore previous values
        if self.hil:
            self.hil.resetAll()

        if self.gamma_daq:
            if self.gamma_daq._getCurrentStatus() == self.gamma_daq._status_lookup['M_RUNNING']:
                self.gamma_daq.stop()
                time.sleep(1)
            self.gamma_daq = None

        if ecu_shutdown:
            if self.hil.cl15_on__.getState() == "On":
                self.hil.cl15_on__.setState('Off')
            if self.hil.cl30_on__.getState() == "On":
                self.hil.cl30_on__.setState('Off')

        # the base's breakdown() will handle, among other things, storing of
        # the current test results
        TestEnvironmentBase.breakdown(self)

        # cleanup internal references
        # (typically those were defined during setup)
        self.daq = None
        self.canape_cal = None
        self.canape_can = None
        self.asap3 = None
        self.gamma = None
     ######### for N-Haltphase test
    '''
        if self.canape_Diagnostic:
            print("Disable Tester Present")
            self.canape_Diagnostic.disableTesterPresent()
            self.canape_Diagnostic = None

        # the base's breakdown() will handle, among other things, storing of
        # the current test results
        # more cleanup
        
        self.gamma = None
    '''
    # #########################################################################
    # On-demand tool init
    # #########################################################################
    def getAsap3(self):
        """ Get the main CANape application instance handle. """
        if not self.asap3:
            self.asap3 = canapeapi.CANapeASAP3(
                working_dir=os.path.join(_base_project_path, "CANape"),         # use for the ISO related test case only
                #working_dir=os.path.join(_base_project_path, "CANapeOTA"),    # use for the OTA related test case only
                clear_device_list=False,  # clear devices defined in canape.ini
                debug_mode=True,  # show debug window
                keep_canape_alive=False,  # True: keep window open after connection closes
                init_timeout=50000,  # ms, timeout for connection init and responses
            )
        return self.asap3

    # #########################################################################

    def getCanapeCal(self):
        """ Get a CANape XCP/CCP device instance. """
        if not self.canape_cal:
            self.canape_cal = canapeapi.CANapeDevice(
                self.getAsap3(),
                db_filename="GSL_ECU_Master.a2l",
                comm_channel=canapeapi.DEV.CANFD1,
                driver_type=canapeapi.DRIVER.XCP,
                module_name="waehlhebel")
        return self.canape_cal

    # #########################################################################

    def getCanapeCan(self):
        """ Get a CANape CAN device instance. """
        if not self.canape_can:
            self.canape_can = canapeapi.CANapeDevice(
                self.getAsap3(), db_filename="Waehlhebel.arxml",
                comm_channel=canapeapi.DEV.CANFD1,
                driver_type=canapeapi.DRIVER.CAN,
                module_name="wh")
        return self.canape_can

    # #########################################################################
    def getCanapeDiagnostic(self):
        """ Get a CANape Diagnostic/CDD device instance. """
        if not self.canape_Diagnostic:
            self.canape_Diagnostic = CANapeDiagnosis(
                self.getAsap3(),
                db_filename="Gear_Shift_Control_Module.cdd",
                comm_channel=canapeapi.DEV.CANFD1,
                driver_type=canapeapi.DRIVER.CANDELA,
                module_name="Gear_Shift_Control_Module",
            )
        return self.canape_Diagnostic

    # #########################################################################
    def getCanapeDAQ(self):
        """ Get a data acquisition instance configured for measurements with
            our defined CANape devices.
        """
        if not self.daq:
            self.daq = canapeapi.DataAcquisition(
                self.getAsap3(),
                self.getCanapeCal(),  # device 0: xcp
                self.getCanapeCan(),  # device 1: can (for sync)
                self.getCanapeDiagnostic(),
                #              self.canape_arxml()
            )
        return self.daq

    def getGammaDAQ(self):
        """ Get a data acquisition instance configured for measurements with
                    our defined CANape devices.
        """
        if not self.gamma_daq:
            self.gamma_daq = FunctionsDaq(
                self.gamma.getReference(),
                system_name="Waehlhebel"
            )

        return self.gamma_daq

    # #########################################################################
    # Calibration and HIL parameters/variables Containers
    # #########################################################################
    def getCal(self):
        """ Get an instance of an object containing all defined calibration
            variables.
            Note:
                This will cause CANape to be started if it is not already 
                running.
        """
        if not self.cal:
            self.cal = cal_variables.CalVars(self.getCanapeCal())
        return self.cal
        # #########################################################################
        # Calibration and HIL parameters/variables Containers
        # #########################################################################

    def getBus(self):
        """ Get an instance of an object containing all defined calibration
            variables.
            Note:
                This will cause CANape to be started if it is not already
                running.
        """
        if not self.cal:
            self.cal = cal_variables.CalVars(self.getCanapeCan())
        return self.cal

    # #########################################################################
    def getHil(self):
        # type: () -> object
        """ Get an instance of an object containing all defined hil/model
            variables.
        """
        # since the ubiquitous self.hil has been initialized during setup,
        # we can just return it here
        ## To Do
        # if not self.hil:
        #    self.hil = hil_variables.HilVars(self.gamma_service.getReference())
        return self.hil


# #########################################################################
    def getCanBus(self):
        # type: () -> object
        """ Get an instance of an object containing all defined hil/model
            variables.
        """
        # since the ubiquitous self.hil has been initialized during setup,
        # we can just return it here
        ## To Do
        # if not self.hil:
        #    self.hil = hil_variables.HilVars(self.gamma_service.getReference())
        return self.can_bus

    # #########################################################################

    def startupECU(self):
        """ Startup the ECU using a defined startup cycle. """
        # A simple sample implementation:
        print
        "# ECU startup...",
        self.hil.vbat_cl30__V.set(13.0)  # 14V to 13V changed
        self.hil.current_cl30__A.set(4.0)
        self.hil.supply_sense__.set(0)
        time.sleep(0.200)

        print
        '.',
        self.hil.cl30_on__.set(1)
        time.sleep(0.200)

        print
        '.',
        self.hil.cl15_on__.set(1)

        # Example for some additional delay time to wait until a initial check,
        # calibration or whatever is over and ECU is in a stable state.
        # TODO: Ideally there would be some flag to signal a "init complete"
        sleepWithFeedback(1500, comment="...wait for init...")

        # if CANape (ccp/xcp) was already running (might be the case if ECU has
        # been shut down during the test), try to re-establish the connection
        if self.canape_cal:
            self.canape_cal.goOnline()

        # #########################################################################

    def shutdownECU(self):
        """ Shutdown the ECU using a defined shutdown cycle. """

        # set any currently running ccp/xcp connection to offline to avoid
        # connection loss / timeout trouble
        if self.canape_cal:
            self.canape_cal.goOffline()

        # A simple sample implementation:
        if self.hil.vbat_cl30__V.get() < 0.5:
            # looks like we have already shut down:
            # just make sure all settings are in their proper shutdown states
            self.hil.cl30_on__.set(0)
            self.hil.vbat_cl30__V.set(0.0)
            return
        self.hil.cl15_on__.set(0)
        time.sleep(0.200)  # added to adjust #TODO
        print
        "# ECU shutdown...",

        # wait for ECU should fall asleep i.e. current to drop below
        # "active" levels
        timeout = time.time() + 2.0  # [s]
        level = 0.250  # [A] (assuming the ECU draws about 350mA in "idle)
        step_time_s = 0.200  # [s]
        steps = 0
        while (True):
            current = self.hil.cc_mon__A.get()
            if steps <= 0:
                print
                "%dmA" % (current * 1000),
            else:
                print
                ".",
            steps += 1

            if current < level:
                print
                "%dmA" % (current * 1000), "...ok"
                time.sleep(0.100)
                self.hil.cl30_on__.set(0)
                break

            if time.time() > timeout:
                print
                "...timeout!"
                break

            time.sleep(step_time_s)

        time.sleep(step_time_s)  # just for good measure
        self.hil.vbat_cl30__V.set(0.0)  # Vbat off


# #############################################################################
#
# #############################################################################

if __name__ == "__main__":
    print "Test Support Path:   ", _test_support_path
    print "Project Path:        ", _base_project_path
    print "Test Pool Path:      ", _test_pool_path
    print "Test Libraries Path: ", _test_libs_path
    print
    print config
