#!/usr/bin/env python

"""Convenience module to plot various scatterplot functions"""
import conv
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text
#from pylab import *

def plot_series(ax, lines, title, x_axis, y_axis, colors=None,size=10, connect_dots=False, alpha=0.3, edgecolors=None, linewidth=1):

    #not in use currently
    patterns = ('>', 'o', 'D', '*', '^','s')
    if colors is None:
        colors = ('cyan', 'orange', 'greenyellow', 'steelblue', 'crimson', 'gold', 'yellow', 'greenyellow',
                'aquamarine', 'teal', 'cyan', 'steelblue', 'darkblue', 'slateblue', 'darkorchid',
                'deeppink', 'crimson')    
    for (x,y,label), color in zip(lines, colors):
        draw_actual_plot(ax, x, y, color, title, x_axis, y_axis, label=label, size=size, connect_dots=connect_dots, alpha=alpha, edgecolors=edgecolors, linewidth=linewidth)

    #conv.add_legend(ax)

def draw_actual_plot(ax, x, y, r, title, x_axis, y_axis, cm="Blues_r", size=10, edgecolors="None", label=None, secondary_y=False, connect_dots=False, alpha=0.3, linewidth=1):

    if secondary_y:

        ax = ax.twinx()
    else:
        ax = ax

    if len(r)>1:
        #plot scatter plot
        s = ax.scatter(x, y, c=r, alpha=alpha,s=size, cmap=cm, edgecolors=edgecolors, lw = linewidth, label=label)
    else:
        s = ax.scatter(x, y, c=r, alpha=1.0,s=size, edgecolors=edgecolors, lw = linewidth, label=label)

    if connect_dots and isinstance(r, basestring):
        ax.plot(x, y, c=r)
    elif connect_dots:
        ax.plot(x, y, c='k')
    ax.set_title(title, fontweight='bold')

    ax.set_xlabel(x_axis, fontweight='bold')

    if secondary_y: #not completely true, should have another setting to show that will beplotting secondary plot
        ylabel_col = r
    else:
        ylabel_col = 'k'

    ax.set_ylabel(y_axis, color=ylabel_col, fontweight='bold')

    for tk in ax.get_yticklabels():
        tk.set_visible(True)
    for tk in ax.get_xticklabels():
        tk.set_visible(True)

    return s, ax

def find_fit_regression(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)                                            
    r_2 = r_value**2

    p = np.array([slope,intercept])
    y_model = np.polyval(p, x)

    return y_model, r_2

def find_xy_regression(x, y, neg=False):
    
    if neg:
	p = np.array([-1,0])
    else:
	p = np.array([1,0])
    
    y_model = np.polyval(p, x)                    # model using the fit parameters; NOTE: parameters here are coefficients

    ybar = np.sum(y)/len(y)

    ssres = np.sum((y - y_model) **2)
    sstot = np.sum((y - ybar) **2)

    if sstot == 0:
        print "Warning: Appears to be no error"

        return y_model, -100    

    r_2 = 1 - ssres / sstot

    return y_model, r_2

def plot_regression(ax, x, y, fit=False, neg=False, label_corr=False, labels=None, plot_PI=True):

    if fit == True:
        y_model, r_2 = find_fit_regression(x, y)
    else:
	y_model, r_2 = find_xy_regression(x, y, neg)

    if r_2 == -100:
        return

    # Statistics
    n = len(x)                              # number of observations
    m = 2 				    # should be p.size() but simpler to do 2. number of parameters
    DF = n - m                                    # degrees of freedom
    t = stats.t.ppf(0.95, n - m)                  # used for CI and PI bands

    # Estimates of Error in Data/Model
    resid = y - y_model
    #chi2 = np.sum((resid/y_model)**2)             # chi-squared; estimates error in data
    #chi2_red = chi2/(DF)                          # reduced chi-squared; measures goodness of fit
    s_err = np.sqrt(np.sum(resid**2)/(DF))        # standard deviation of the error

    label_fit = "x=y" if fit==False else "best fit"

    if plot_PI:
        # Fit
        ax.plot(x,y_model,'-', color='0.1', linewidth='2', alpha=0.5, label=label_fit)

    x2 = np.linspace(np.min(x), np.max(x), 100)
    if neg:
        y2 = np.linspace(np.max(y_model), np.min(y_model), 100)
    else:
        y2 = np.linspace(np.min(y_model), np.max(y_model), 100)

    # Confidence Interval
#    CI = t*s_err*np.sqrt(1/n +(x2-np.mean(x))**2/np.sum((x-np.mean(x))**2))
#    ax.fill_between(x2, y2+CI, y2-CI, color='#b9cfe7', edgecolor='')

    '''Minor hack for labeling CI fill_between()'''
#    ax.plot(x2, y2+CI, '-', color='#b9cfe7', label='95% Confidence Limits')

    # Prediction Interval
    PI = t*s_err*np.sqrt(1+1/n+(x2-np.mean(x))**2/np.sum((x-np.mean(x))**2))
    if plot_PI:
        ax.fill_between(x2, y2+PI, y2-PI, color='None', linestyle='--')
        ax.plot(x2, y2-PI, '--', color='0.5', label='95% Prediction Limits')
        ax.plot(x2, y2+PI, '--', color='0.5')

    if label_corr:
        # Annotate plot with R^2 
        conv.add_text(ax, "C", r_2)
    np.set_printoptions(suppress=True)
    if labels:
        label_outliers(ax, x, y, x2, y2-PI, y2+PI, labels)

def add_x_y_line(ax, min_val=None, max_val=None, neg=False):
    if min_val is not None and max_val is not None:
        lims = [min_val, max_val]
    else:
        lims = [
            np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
            np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
            ]
    if neg:
        lims1 = [lims[0], lims[1]]
        lims2 = [lims[1], lims[0]]
    else:
        lims1 = lims
        lims2 = lims
    # now plot both limits against eachother
    ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)

def label_outliers(ax, x, y, x_lim, y_bottom_lim, y_top_lim, labels):

    texts = []    

    for x_val, y_val, label in zip(x, y, labels):
        for i,value in enumerate(x_lim):
	    if x_val <= value:
                ind = i - 1 if i > 0 else 0
		if y_val < y_bottom_lim[ind] or y_val > y_top_lim[ind]:
		    #conv.annotate_point(ax, x_val, y_val, label)
		    texts.append(conv.add_text_adjust(ax, x_val, y_val, label, size=7))
		break

    #adjust_text(texts)
