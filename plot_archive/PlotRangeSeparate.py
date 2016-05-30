import os
import sys
import scipy.stats
import math
import matplotlib.pyplot as plt
from pylab import *
import numpy as np

def plot_line ( x, y, label, ax, min_range, max_range, se):
    color = ax._get_lines.color_cycle.next()
    ax.plot(x, y, '-o',label=label, color=color)
    #ax.fill_between(x, max_range, min_range, alpha=0.2, color=color)    
    x_tick_marks=[0]
    x_tick_marks.extend(x)
    x_tick_marks.append(x[len(x)-1]+1)
    ax.set_xticks(x_tick_marks)

    plt.rcParams.update({'font.size': 12})
    plt.legend(loc='lower right')
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='on',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='on')

    plt.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left='on',      # ticks along the bottom edge are off
        right='off',         # ticks along the top edge are off
        labelleft='on')

def plot_range ( x, y, label, ax, min_range, max_range, se):
    color = ax._get_lines.color_cycle.next()
    ax.plot(x, y, '-o',label=label, color=color)
    ax.fill_between(x, max_range, min_range, alpha=0.2, color=color)
    x_tick_marks=[0]
    x_tick_marks.extend(x)
    x_tick_marks.append(x[len(x)-1]+1)
    ax.set_xticks(x_tick_marks)

    plt.rcParams.update({'font.size': 12})
    plt.legend(loc='lower right')
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='on',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='on')

    plt.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left='on',      # ticks along the bottom edge are off
        right='off',         # ticks along the top edge are off
        labelleft='on')


def main(args):
    #read in and rename arguments
    inp_vals=args[1]
    log_option=args[2]
    title=args[3]
    x_axis=args[4]
    y_axis=args[5]
    series_l=int(args[6])

    #make a name for the score file
    file=inp_vals.rsplit('.',1)[0]
    out_fig = '%s_range_sep.png' % (file)
    
    #read in list of vals
    with open(inp_vals) as vals:
        lines = vals.readlines()

    label = []
    x = []
    y = []
    min = []
    max = []
    se = []

    for ind in range(0, len(lines),series_l+1):
        print lines[ind]
        label.append(lines[ind].strip())
        temp_x = []
        temp_y = []
	temp_min = []
        temp_max = []
        temp_se = []
        for i in range(ind+1,ind+series_l+1):
            tokens = lines[i].split()
            temp_x.append( float( tokens[0] ) )
            temp_y.append( float( tokens[1] ) )
	    temp_min.append( float( tokens[2] ))
            temp_max.append( float( tokens[3] ))
            temp_se.append( float( tokens[4] ))
        x.append(temp_x)
        y.append(temp_y)
	min.append(temp_min)
        max.append(temp_max)
        se.append(temp_se)

    fig = plt.figure()
    ax = fig.add_subplot(411)

    if log_option == "1":
        ax.set_xscale("log")
        ax.set_yscale("log")

    
    for ind,l in enumerate(label,0):
        plot_line( x[ind],y[ind], l, ax,min[ind],max[ind],se[ind])
    
    for ind,l in enumerate(label,0):
        plt.ylim([0.0,1.0])
        ax = fig.add_subplot(4,1,ind+2)
        plot_range( x[ind],y[ind], l, ax,min[ind],max[ind],se[ind])

    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
#    fig.suptitle(title)
    plt.ylim([0.0,1.0])    
    width=6
    height=24
    fig.set_size_inches(width, height) 
    fig.savefig(out_fig)
if __name__ == "__main__":
    #infile = '/Users/arubenstein/Downloads/sorted_complete.txt'
    #outfile = '/Users/arubenstein/Dropbox/Research/Khare Lab/Mean Field/Design/HCV.transfac'

    main(sys.argv)
