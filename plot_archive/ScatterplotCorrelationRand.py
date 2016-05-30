
'''Was used in the past to generate bubble plots. archived for historical purposes'''

import os
import sys
import scipy.stats
import math
import matplotlib.pyplot as plt
from pylab import *
import random

def main(args):
    #read in and rename arguments
    list_files=args[1]
    metric_1=args[2]
    metric_2=args[3]
    output_path=args[4]
    log_option=args[5]
    
    if log_option == "1":
        suff = "_p"
    else:
        suff = ""
  
    #make a name for the score file
    out_fig = '%s_%s%s_corr.png' % (metric_1,metric_2,suff)
    out_r = '%s_%s%s_r2.txt' % (metric_1,metric_2,suff)
    
    with open(list_files) as f:
        inp_vals_files = f.readlines()
    
    x = []
    y = []
    z = []
    for f in inp_vals_files:
        f = f.strip()
	fname_1 = f+metric_1+".txt"
        fname_2 = f+metric_2+".txt"
        with open(fname_1) as vals:
            x_vals = vals.readlines()
        with open(fname_2) as vals:
            y_vals = vals.readlines()
        #list_indices = random.sample(xrange(len(x_vals)),10)
        
        #if metric_1 == 'auc' or metric_1 == 'cosine':
        #    x.extend([ 1.0 - float(x_vals[i].strip()) for i in list_indices])
        #else:
	#    x.extend([ float( x_vals[i].strip()) for i in list_indices])

        #if metric_2 == 'auc' or metric_2 == 'cosine':        
        #    y.extend([ 1 - float(y_vals[i].strip()) for i in list_indices])
        #else:
        #    y.extend([ float(y_vals[i].strip()) for i in list_indices])    
        #z.extend([ 0.0 for i in list_indices]) 
        if metric_1 == 'auc' or metric_1 == 'cosine':
            x_vals_f = [ 1.0 - float( xv.strip()) for xv in x_vals ]    
        else:
            x_vals_f = [ float( xv.strip()) for xv in x_vals ]
        if metric_2 == 'auc' or metric_2 == 'cosine':
            y_vals_f = [ 1.0 - float( yv.strip()) for yv in y_vals ]
        else:
            y_vals_f = [ float( yv.strip()) for yv in y_vals ]

        points = zip(x_vals_f,y_vals_f)
        points_sorted = sorted(points)
        
        for i in range(0,len(points), len(points)/20):
            if log_option == 0:
                x.append( points_sorted[i][0])
                y.append( points_sorted[i][1])
            else:
                x.append( float(sum([ points_sorted[i][0] < xvf for xvf in x_vals_f]))/len(points) )
                y.append( float(sum([ points_sorted[i][1] < yvf for yvf in y_vals_f]))/len(points) )
            z.append( 0.0 )       
    
    x_uniq = []
    y_uniq = []
    z_uniq = []
    weight = []

    points = zip(x,y)
    points_uniq = []
    
    for idx,p in enumerate( points,0):
        if p not in points_uniq:
            points_uniq.append(p)
            x_uniq.append(p[0])
            y_uniq.append(p[1])
            z_uniq.append(z[idx])
            weight.append(1)
        else:
	    uniq_idx = points_uniq.index(p)
            weight[uniq_idx] = weight[uniq_idx]+1
            if z_uniq[uniq_idx] > z[idx]:
                 z_uniq[uniq_idx] = z[idx]
    size = [ (w)*12 for w in weight ]       
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    r_2 = r_value**2
    
    fig = plt.figure()
    ax = fig.add_subplot(111)

    if log_option == "1":
        ax.set_xscale("log")
        ax.set_yscale("log")
    
    ax.scatter(x_uniq, y_uniq, c=z_uniq, cmap='Blues_r', s=size,alpha=0.5 )


    #if log_option == "1":
	#ax.relim()
        #ax.autoscale()

    #plt.legend(loc='lower right')
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off')

    plt.tick_params(
        axis='y',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        left='off',      # ticks along the bottom edge are off
        right='off',         # ticks along the top edge are off
        labelleft='off')
    width=1.5
    height=1.5
    fig.set_size_inches(width, height) 
    fig.savefig(out_fig,bbox_inches="tight", pad_inches=0.0)
    with open(out_r,"w") as r:
        r.write('%0.4f'% (r_2))
if __name__ == "__main__":
    #infile = '/Users/arubenstein/Downloads/sorted_complete.txt'
    #outfile = '/Users/arubenstein/Dropbox/Research/Khare Lab/Mean Field/Design/HCV.transfac'

    main(sys.argv)
