#******************************************************************************
# -*- coding: latin-1 -*-
# File    : functions_daq.py
# Task    : functions to work with daq measuremmt
#
# Author  : An3Neumann
# Date    : 21.05.2021
# Copyright 2021 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 21.05.2021 | An3Neumann | initial
#******************************************************************************
import data_common
import os
if os.getenv('COMPUTERNAME') in data_common.CONTROL_COMPUTER_NAMES:
    from ttk_tools.rst import gamma_api
    from ttk_tools.rst.gamma_api import DataAcquisition
else:
    import ttk_tools.rst.gamma_api_offline_stub as gamma_api
    from ttk_tools.rst.gamma_api_offline_stub import DataAcquisition #@UnresolvedImport
import time
import data_common as dc
import pylab
import copy

class FunctionsDaq(DataAcquisition):
    
    def __init__(self, gamma, system_name="iSyst", ftp_host=None):
        """
         init constructor
        """
        super(FunctionsDaq, self).__init__(gamma, system_name, ftp_host)

    def plotSingleShot(self, daq_data, filename, label_signal, path = None, yscaling=False, gamma = True):
        """ Create a Picture with more curves without any Qualification --> MAXIMAL 8 CURVES !!
            Parameters:
                daq_data   - data dict to be checked with "time" and "data" keys
                filename  - save filename
                label_signal - label in plot for the signal
                path      - if path is None, the path from data_common will be used
                yscaling - ymin and ymax eg. [0, 5]
                gamma    - if data are from gamma measurement
            Returns a testresult entry [<result>, <img>, <verdict>]
        """
        # Headline ----------------------------------------------------------------
        description = 'Filename: %s' % (filename)

        # Re-Define filename ------------------------------------------------------
        filename = filename + '.png'

        # Define out_file_path ----------------------------------------------------
        if path is None:
            path = dc.daq_meas_path
        out_file_path = os.path.join(path, filename)

        # clear figure for new creation -------------------------------------------
        fig = pylab.figure(figsize=(56, 10))
        fig.clear()

        # define figure parameters ------------------------------------------------
        font_size = '28'
        fig_dpi_low = 80

        # create figure -----------------------------------------------------------
        subplot = fig.add_subplot(111)
        subplot.set_title(filename, fontdict={'size': font_size}, loc='left')
        subplot.set_xlabel('time [s]', fontsize=font_size)
        subplot.set_ylabel('values', fontsize=font_size)
        xticklabels = pylab.getp(pylab.gca(), 'xticklabels')
        pylab.setp(xticklabels, fontsize=font_size)
        yticklabels = pylab.getp(pylab.gca(), 'yticklabels')
        pylab.setp(yticklabels, fontsize=font_size)
        subplot.grid(True)

        def addPlot(data, **kwargs):
            subplot.plot(data["time"], data["data"], **kwargs)
            if yscaling is not False and len(yscaling) == 2:
                subplot.set_ylim(yscaling[0], yscaling[1])

        plot_data = copy.deepcopy(daq_data)
        if gamma is True:
            start_time = plot_data['time'][0]
            def sub(x):
                return x-start_time
            new_times = map(sub, plot_data['time'])
            plot_data['time'] = new_times

        label = label_signal
        addPlot(plot_data, marker=".", label=label_signal, linewidth=2.0)
        leg = subplot.legend(loc='best', fontsize=font_size, bbox_to_anchor=(1, 1), fancybox=True, ncol=1)
        leg.set_title('SIGNAL:', prop={'size': '28'})

        # save figure to file path and add picture to result ----------------------
        fig.savefig(out_file_path, bbox_inches="tight", dpi=fig_dpi_low)
        picture = "[[IMG]] " + out_file_path

        # return resultlist -------------------------------------------------------
        return [description, picture, 'INFO']

    def plotMultiShot(self, daq_data, filename, path=None, yscaling=False, gamma = True, v_lines = None):

        """ Create a Picture with more curves without any Qualification --> MAXIMAL 8 CURVES !!
            Parameters:
                data_list  - data dict to be checked with "time" and "data" keys
                label_list - list ob labelnames
                filename   - string of filename without acronym like '.png'
                path       - if path is None, the path from data_common will be used
                yscaling   - ymin and ymax eg. [0, 5]
                gamma      - if data are from gamma measurement
                v_lines    - add vertikal lines on defined x-position (dict: {'x': , 'label': })

                yscaling - ymin and ymax eg. [0, 5]
            Returns a testresult entry [<result>, <img>, <verdict>]
        """
        # Headline ----------------------------------------------------------------
        description = 'Filename: %s' % (filename)

        # Re-Define filename ------------------------------------------------------
        filename = filename + '.png'

        # Define out_file_path ----------------------------------------------------
        if path is None:
            path = dc.daq_meas_path
        out_file_path = os.path.join(path, filename)

        # clear figure for new creation -------------------------------------------
        fig = pylab.figure(figsize=(56, 10))
        fig.clear()

        # define figure parameters ------------------------------------------------
        font_size = '24'
        fig_dpi_low = 80

        # create figure -----------------------------------------------------------
        subplot = fig.add_subplot(111)
        subplot.set_title(filename, fontdict={'size': font_size}, loc='left')
        subplot.set_xlabel('time [s]', fontsize=font_size)
        subplot.set_ylabel('values', fontsize=font_size)
        xticklabels = pylab.getp(pylab.gca(), 'xticklabels')
        pylab.setp(xticklabels, fontsize=font_size)
        yticklabels = pylab.getp(pylab.gca(), 'yticklabels')
        pylab.setp(yticklabels, fontsize=font_size)
        subplot.grid(True)

        plot_data = copy.deepcopy(daq_data)
        if gamma is True:
            for data in plot_data:
                start_time = plot_data[data]['time'][0]
                def sub(x):
                    return x - start_time
                new_times = map(sub, plot_data[data]['time'])
                plot_data[data]['time'] = new_times

        def addPlot(data, **kwargs):
            subplot.plot(data["time"], data["data"], **kwargs)
            if yscaling is not False and len(yscaling) == 2:
                subplot.set_ylim(yscaling[0], yscaling[1])

        for data in plot_data:
            label_signal = data
            label = label_signal.split('/')[-1]
            addPlot(plot_data[data], marker=".", label=label, linewidth=2.0)

        if v_lines:
            colorlist = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
            i=0
            if isinstance(v_lines, dict):
                for vl in v_lines:
                    subplot.axvline(x=v_lines[vl]['x'], linestyle='--', label=v_lines[vl]['label'], color=colorlist[i])
                    i+=1

        leg = subplot.legend(loc='best', fontsize=font_size, bbox_to_anchor=(1, 1), fancybox=True, ncol=1)
        leg.set_title('SIGNALS:', prop={'size': '28'})

        # save figure to file path and add picture to result ----------------------
        fig.savefig(out_file_path, bbox_inches="tight", dpi=fig_dpi_low)
        picture = "[[IMG]] " + out_file_path

        # return resultlist -------------------------------------------------------
        return [description, picture, 'INFO']

    def startMeasurement(self, meas_vars):
        """
        Parameter:
            meas_vars   - list of measured variables
        Info:
            start GammaVLogger Measurement
        Returns:
            -
        """
        if not isinstance(meas_vars, list):
            raise ValueError("Messvariablen müssen in einer Liste sein")

        try:
            self.setup(meas_vars)
        except gamma_api.GammaDaqError:
            print("Gamma Logger is still running. Stop measurement.")
            self.stop()
            print("Setup Gamma Logger")
            self.setup(meas_vars)

        time.sleep(0.01)
        print("Start Gamma Logger")
        self.start()

    def stopMeasurement(self):
        """
        Parameter:
            -
        Info:
           stop GammaVLogger Measurement
        Return:
            daq_data
        """
        try:
            self.stop()
            time.sleep(0.5)
            daq_data = self.getData()

            # for signal in daq_data:
            #     start_time = daq_data[signal]['time'][0]
            #     def sub(x):
            #         return x-start_time
            #     new_times = map(sub, daq_data[signal]['time'])
            #     daq_data[signal]['time'] = new_times

            return daq_data
        except:
            print("Maybe measurement start was not successfully!")
            return None

    def checkDataIsEqual(self, daq_data, exp_value=None):
        """
        Parameters:
           daq_data:        daq data which have to analysed --> daq_data = daq_data[signal_name]['data']
           exp_value:       all data entries have to been in this value, if None the first value will taken

        Return:
            descr, verdict
        """

        if isinstance(daq_data, list):
            if exp_value is None:
                exp_value = daq_data[0]
            if isinstance(exp_value, float) or isinstance(exp_value, int) or isinstance(exp_value, long):
                counter_wrong = 0
                for data in daq_data:
                    if data != exp_value:
                        counter_wrong += 1

                if counter_wrong > 0:
                    descr = "Measurement Data not as expected (State: %s) - %s wrong Datapoints from %s" % (
                    exp_value, counter_wrong, len(daq_data))
                    verdict = 'FAILED'
                else:
                    descr = "All Measurmentpoints (%s) are as expected (State: %s)" % (len(daq_data), exp_value)
                    verdict = 'PASSED'
            else:
                raise ValueError('Wrong input! Expected Value has to be float, int or long!')
        else:
            raise ValueError('Wrong Input! Daq Data has to be a list')

        return descr, verdict