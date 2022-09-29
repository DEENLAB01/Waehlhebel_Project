#******************************************************************************
# -*- coding: latin-1 -*-
#
# File    : plot_utils.py
# Task    : Utility functions for plotting data
#
# Author  : J.Tremmel
# Date    : 24.05.2016
# Copyright 2016-2018 iSyst Intelligente Systeme GmbH
#
#******************************************************************************
#********************************* Version ************************************
#******************************************************************************
# Rev. | Date       | Name      | Description
#------------------------------------------------------------------------------
# 1.0  | 24.05.2016 | J.Tremmel | initial
# 1.1  | 31.05.2016 | J.Tremmel | added parameters fig_size and fig_dpi to plotSignals
# 1.2  | 08.11.2018 | J.Tremmel | switched from ancient pylab to pyplot  
#******************************************************************************

# The pylab API is now "disapproved", but was typically used w/ matplotlib 0.90.1
# import pylab 
# For basic usage (just .figure()/.show()/.close()), 
# both pylab and matplotlib.pyplot behave the same

# with more recent matplotlib releases we can use pyplot directly
from matplotlib import pyplot 


# #############################################################################
def plotSignals(daq_data, variables, out_file_path=None, 
                xlabel="time", ylabel="values", title="data", 
                fig_size=(14, 4), fig_dpi=72):
    """ Simple plotting of signals using matplotlib (just as sample).
        See http://matplotlib.org/ for available options and usage.
        
        Parameters:
            daq_data      - data acquisition data structure containing data for variables
            variables     - list of variables to add to plot
            out_file_path - output file path, 
                            None: just show a (modal) dialog with plotted data 
                                  (mainly for debug purposes) 
            xlabel        - label for x-axis
            ylabel        - label for y-axis
            title         - title for plot/figure
            fig_size      - tuple with (<width>, <height>) values for plot/figure
            fig_dpi       - resolution (dpi) for stored pixel/raster images
            
    """
    if not daq_data:
        daq_data = {}
    
    fig = pyplot.figure(figsize=fig_size)
    
    
    # pylab | matplotlib 0.90.1
    subplot = fig.add_subplot(111)
    
    subplot.set_title(title)
    subplot.set_xlabel(xlabel)
    subplot.set_ylabel(ylabel)
    subplot.grid(True)
    
    if not variables:
        # daq data may contain the same data referenced by multiple keys
        # (once as plain <name> and once with <device_name>.<name>)
        # => only plot unique variables/data
        variables = {}
        # order by length of variable name, so shorter names will be found first,
        # and longer names for the same data (i.e. with prefix) will be skipped.
        for name, entry in sorted(daq_data.iteritems(), key=lambda item: len(item[0])):
            for existing_entry in variables.itervalues():
                if entry is existing_entry:
                    print "# [skipped]  %s"%(name)
                    break
            else:
                # data not yet added: add now
                print "# [variable] %s"%(name)
                variables[name] = entry
                
        variables = variables.keys()
        
    for var in variables:
        # use alias attribute instead of full representation/path, if available
        alias = getattr(var, "alias", "%s"%(var)) 
        if var not in daq_data:
            print "> %s not found in data, skipped"%(alias)
            continue
        sig_data = daq_data[var]
        subplot.plot(sig_data["time"], sig_data["data"], label=alias)
        
    subplot.legend()
    
    if out_file_path:
        fig.savefig(out_file_path, bbox_inches="tight", dpi=fig_dpi)
    else:
        # pylab.show() opens a modal control, so it does not work that well 
        # during automatic tests (but it may be nice during debugging)
        pyplot.show()
    
    # release figure memory (might not work as well in older pylab releases)
    fig.clear()
    pyplot.close() 


# #############################################################################
def demoPlot(daq_data, output_path="output.png"):
    """ Simple plotting of signals using matplotlib.
        Parameters:
            daq_data    - daq data structure containing data to display
            output_path - plotted data will be stored to this path 
    """
    fig = pyplot.figure(figsize=(12, 4)) 
    subplot = fig.add_subplot(
        111, title="title", xlabel="time [s]", ylabel="values"
    )
    for sig_label, sig_data in sorted(daq_data.iteritems()):
        subplot.plot(
            sig_data["time"], sig_data["data"], 
            label=sig_label, color=(0, 0.6, 0), marker="x", linestyle="-"
        )
        
    subplot.grid(True)
    subplot.legend()
    
    # store plot to file
    fig.savefig(output_path, bbox_inches="tight", dpi=96)
    
    # release figure memory (might not work as well in older pylab releases)
    fig.clear()
    pyplot.close() 
    

# #############################################################################
#
# #############################################################################
if __name__ == "__main__":
    import os
    import tempfile
    import random
    
    random.seed(0) # static seed to get the same dummy data every time
    num_values = 120
    
    def rnd(x):
        return random.random() * 12 / max(1, abs(x - num_values / 2))
    
    daq_data = {
        "signal": {
            "time": [t * 0.001 for t in xrange(num_values)], 
            "data": [rnd(x)    for x in xrange(num_values)]
        }
    }
    
    path = os.path.join(tempfile.gettempdir(), "output.png")
    demoPlot(daq_data, path)
    os.startfile(path)
    
    print "Done."
    