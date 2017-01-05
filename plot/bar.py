#!/usr/bin/env python

"""Convenience module to plot various bar functions"""
import conv
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
#from pylab import *

#not tested taken directly from scatterplot script
def plot_series(ax, lines, title, x_axis, y_axis, colors=None, stacked=True, tick_label=None):

    #not in use currently
    patterns = ('>', 'o', 'D', '*', '^','s')
    colors = ('cyan', 'black', 'crimson', 'darkorchid', 'green', 'gold', 'yellow', 'greenyellow',
                'aquamarine', 'teal', 'cyan', 'darkblue', 'slateblue', 'darkorchid',
                'deeppink', 'crimson')    
    bottom = np.zeros(len(lines[0][0]))
    for (heights,label), color in zip(lines, colors):
        draw_actual_plot(ax, heights, color, title, x_axis, y_axis, label=label, tick_label=tick_label, bottom=bottom)
	bottom = bottom + heights

    conv.add_legend(ax)

def draw_actual_plot(ax, heights, color, title, x_axis, y_axis, tick_label=None, bottom=0, label=""):
    left = np.arange(len(heights))
    ax.bar(left, heights, bottom=bottom, color=color, width=0.8, label=label)

    ax.set_title(title)

    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_xticks(left + 0.4)
    ax.set_xticklabels(tick_label)
 
    #for tk in ax.get_yticklabels():
    #    tk.set_visible(True)
    #for tk in ax.get_xticklabels():
    #    tk.set_visible(True)
