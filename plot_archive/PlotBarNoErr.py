import os
import sys
import scipy.stats
import math
import matplotlib as mpl
mpl.use( "agg" )
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from pylab import *
import numpy as np

def plot_bar (ind, width, y, ax, col,patt):

    color = ax._get_lines.color_cycle.next()
    prop = fm.FontProperties(fname="/Users/arubenstein/.matplotlib/mpl-data/fonts/ttf/Helvetica.ttf")    
    rects1 = ax.bar(ind, y, width, color=col,hatch=patt)
#    rects1 = ax.bar(ind, y, width, color=col,error_kw=dict(ecolor='black', lw=2, capsize=5, capthick=2))

    plt.rcParams.update({'font.size': 10})
    #plt.legend(loc='upper right')
    #plt.tick_params(
    #    axis='x',          # changes apply to the x-axis
    #    which='both',      # both major and minor ticks are affected
    #    bottom='on',      # ticks along the bottom edge are off
    #    top='off',         # ticks along the top edge are off
    #    labelbottom='on')

    #plt.tick_params(
    #    axis='y',          # changes apply to the x-axis
    #    which='both',      # both major and minor ticks are affected
    #    left='on',      # ticks along the bottom edge are off
    #    right='off',         # ticks along the top edge are off
    #    labelleft='on')

    return rects1[0]

def main(args):
    #read in and rename arguments
    inp_vals=args[1]
    log_option=args[2]
    title=args[3]
    x_axis=args[4]
    y_axis=args[5]
    series_l=int(args[6])
    no_lim=args[7]

    #make a name for the score file
    file=inp_vals.rsplit('.',1)[0]
    out_fig = '%s_test.png' % (file)
    
    #read in list of vals
    with open(inp_vals) as vals:
        lines = vals.readlines()

    label = []
    x = []
    y = []

    for ind in range(0, len(lines),series_l+1):
        print lines[ind]
        label.append(lines[ind].strip())
        temp_x = []
        temp_y = []
        for i in range(ind+1,ind+series_l+1):
            tokens = lines[i].split()
            temp_x.append( tokens[0] )
            temp_y.append( float( tokens[1] ) )
        x.append(temp_x)
        y.append(temp_y)
    mpl.rcParams['font.family'] = 'Helvetica'

    fig = plt.figure()
    ax = fig.add_subplot(111)

    if log_option == "1":
        ax.set_xscale("log")
        ax.set_yscale("log")

    x_ind = np.arange(len(x[0]))
    width = 0.28
    rects=[]
    
    color=['r','b','g','y','k']
    patterns = ('-', 'x', 'o', 'O', '.')
    for ind,l in enumerate(label,0):
        rects.append(plot_bar( x_ind, width, y[ind], ax,color[ind],patterns[ind]))
        x_ind = x_ind + width

    prop = fm.FontProperties(fname="/Users/arubenstein/.matplotlib/mpl-data/fonts/ttf/Helvetica.ttf")
 
    lgd = ax.legend( rects, label,loc='upper center',ncol=3, fancybox=True, shadow=True,bbox_to_anchor=(0., 1.02, 1., .102),prop={'size':10})
    ax.set_xticks(np.arange(len(x[0]))+0.35)
    ax.set_xticklabels( x[0] )
    plt.xlabel(x_axis,fontproperties=prop)
    plt.ylabel(y_axis)
#    fig.suptitle(title)
    if ( no_lim == "false" ):    
        plt.ylim([0.0,1.0]) 
    else:
        ax.axhline(0, linestyle='-', color='k')   
    width=4
    height=2.66
    fig.set_size_inches(width, height)
    fig.savefig(out_fig, bbox_extra_artists=(lgd,), bbox_inches='tight')
if __name__ == "__main__":
    #infile = '/Users/arubenstein/Downloads/sorted_complete.txt'
    #outfile = '/Users/arubenstein/Dropbox/Research/Khare Lab/Mean Field/Design/HCV.transfac'

    main(sys.argv)
