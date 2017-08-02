#!/usr/bin/env python

"""Convenience module to plot various bar functions"""
import conv
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
#from pylab import *

#not tested taken directly from scatterplot script
def plot_series(ax, lines, title, x_axis, y_axis, colors=None, stacked=True, tick_label=None, unique_label=True, pattern=False):

    #not in use currently
    if pattern and not unique_label:
        patterns = ('-', 'x', 'o', '*', '^','s')
    if not colors:
        colors = ('cyan', 'black', 'crimson', 'darkorchid', 'green', 'gold', 'yellow', 'greenyellow',
                'aquamarine', 'teal', 'cyan', 'darkblue', 'slateblue', 'darkorchid',
                'deeppink', 'crimson')    
    
    bottom = np.zeros(len(lines[0][0]))
    if stacked:
        for ind, (heights,label), color in enumerate(zip(lines, colors)):
            draw_actual_plot(ax, heights, color, title, x_axis, y_axis, label=label, bottom=bottom, unique_label=unique_label, pattern=patterns[ind])
	    bottom = bottom + heights
    else:
	width = 0.8/len(lines)
        left = np.arange(len(lines[0][0]))
        for ind, ((heights,label), color) in enumerate(zip(lines, colors)):
	    draw_actual_plot(ax, heights, color, title, x_axis, y_axis, label=label, bottom=bottom, width=width, unique_label=unique_label, pattern=patterns[ind], left=left)
	    left = left+width 

    left = np.arange(len(lines[0][0]))
    ax.set_xticks(left + 0.5)
    ax.set_xticklabels(tick_label)

def draw_actual_plot(ax, heights, color, title, x_axis, y_axis, tick_label=None, bottom=0, label="", yerr=None, pattern=False, vertical_labels=False, unique_label=True, left=np.array([]), width=0.8, legend=False):
    if left.size == 0:
        left = np.arange(len(heights))

    #don't set label here because may have only a few unique labels
    bars = ax.bar(left, heights, bottom=bottom, color=color, width=width, yerr=yerr, ecolor='k', alpha=0.8, label=label, hatch=pattern)

    if unique_label and pattern:
        avail_patterns = ('/', 'o', '+', 'x','0','//')
        avail_colors = set(color)
        patt_col = dict(zip(avail_colors, avail_patterns))
        patt_col['black'] = ''
	patt_col['tomato'] = ''
        patt_col['lightskyblue'] = ''
        
        patterns = [ patt_col[c] for c in color ]

        for bar, pattern in zip(bars, patterns):
            bar.set_hatch(pattern)

    patches = []

    ax.set_title(title)

    ax.set_xlabel(x_axis, fontweight='bold')
    ax.set_ylabel(y_axis, fontweight='bold')

    #only set tick_labels if calling path is not thru plot_series
    if tick_label:
        ax.set_xticks(left + 0.4)
        ax.set_xticklabels(tick_label)
    if vertical_labels:
        plt.xticks(rotation='vertical') 
    #for tk in ax.get_yticklabels():
    #    tk.set_visible(True)
    #for tk in ax.get_xticklabels():
    #    tk.set_visible(True)


    if unique_label and legend:
	new_label = []
        if isinstance(color, basestring):
	    color = [color]
        for ind in range(len(color)):
            if ind > 0 and color[ind-1] == color[ind]:
                continue
            if not label[ind]:
                continue
	    new_label.append(label[ind])
            patches.append(bars[ind])
        return patches, new_label
