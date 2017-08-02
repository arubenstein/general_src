#!/usr/bin/env python

"""Convenience module to plot various histogram functions"""
import conv
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np

def draw_actual_plot(ax, values, title, x_axis, log=False, normed=True, label=None, nbins=10, stacked=False, edgecolor=None, colors="", no_y_axis=False):
    if len(colors) == 0:
        colors = ('lightskyblue', 'black', 'tomato', 'darkorchid', 'green', 'gold', 'yellow', 'greenyellow',
                'aquamarine', 'teal', 'cyan', 'darkblue', 'slateblue', 'darkorchid',
                'deeppink', 'crimson')
    if len(values) > 1:
	col = colors[0:len(label)] if label else colors[0]
	print col
        counts, bins, patches = ax.hist(values, nbins, normed=normed,color=col, log=log,alpha=0.75, label=label, stacked=stacked, linewidth=0)
    else:
        ax.text(0.5,0.5,"Only one data point in dataset",
            horizontalalignment='center',
            verticalalignment='center',
            fontsize=10, color='green',
            transform=ax.transAxes)

    if not no_y_axis:
        y_axis = "Counts" if not normed else "Normalized Frequency"
        y_axis_suff = " (log)" if log else ""
        y_axis = y_axis + y_axis_suff
        y_axis = "Normalized\nFrequency (log)" if y_axis == "Normalized Frequency (log)" else y_axis
        ax.set_ylabel(y_axis, fontweight='bold')
    
    ax.set_xlabel(x_axis, fontweight='bold')
    ax.set_title(title)

    # Set the ticks to be at the edges of the bins.
    #ax.set_xticks(bins)
    # Set the xaxis's tick labels to be formatted with 1 decimal place...
    #ax.xaxis.set_major_formatter(FormatStrFormatter('%0.1f'))
    #[label.set_visible(True) for label in ax.get_xticklabels()]
    # Change the colors of bars at the edges...
    #twentyfifth, seventyfifth = np.percentile(values, [25, 75])
    #for patch, rightside, leftside in zip(patches, bins[1:], bins[:-1]):
    #    if rightside < twentyfifth:
    #        patch.set_facecolor('green')
    #    elif leftside > seventyfifth:
    #        patch.set_facecolor('red')

    # Label the raw counts and the percentages below the x-axis...
    #bin_centers = 0.5 * np.diff(bins) + bins[:-1]
    #for count, x in zip(counts, bin_centers):
        # Label the raw counts
        #ax.annotate(str(count), xy=(x, 0), xycoords=('data', 'axes fraction'),
        #    xytext=(0, -18), textcoords='offset points', va='top', ha='center')

        # Label the percentages
    #    percent = '%0.0f%%' % (100 * float(count) / counts.sum())
    #    ax.annotate(percent, xy=(x, 0), xycoords=('data', 'axes fraction'),
    #        xytext=(0, -18), textcoords='offset points', va='top', ha='center')


    # Give ourselves some more room at the bottom of the plot
    plt.subplots_adjust(bottom=0.15)
