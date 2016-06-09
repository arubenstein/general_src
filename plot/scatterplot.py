#!/usr/bin/env python

"""Convenience module to plot various scatterplot functions"""
import conv
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
#from pylab import *

def draw_actual_plot(ax, x, y, r, title, x_axis, y_axis, cm="Blues_r", size=10, edgecolors="None"):

    if len(r)>1:
        #plot scatter plot
        s = ax.scatter(x, y, c=r, alpha=0.5,s=size, cmap=cm, edgecolors=edgecolors, lw = 2)
    else:
	    s = ax.scatter(x, y, c=r, alpha=0.5,s=size, edgecolors=edgecolors, lw = 2)
    ax.set_title(title)

    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)

    for tk in ax.get_yticklabels():
        tk.set_visible(True)
    for tk in ax.get_xticklabels():
        tk.set_visible(True)

    return s

def find_fit_regression(x, y):
    slope, intercept, r_value, p_value, std_err = stats.linregress(x_both, y_both)                                            
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

def plot_regression(ax, x, y, fit=False, neg=False):

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

    # Fit
    ax.plot(x,y_model,'-', color='0.1', linewidth='2', alpha=0.5, label='x=y')

    x2 = np.linspace(np.min(x), np.max(x), 100)
    if neg:
        y2 = np.linspace(np.max(y_model), np.min(y_model), 100)
    else:
        y2 = np.linspace(np.min(y_model), np.max(y_model), 100)

    # Confidence Interval
    CI = t*s_err*np.sqrt(1/n +(x2-np.mean(x))**2/np.sum((x-np.mean(x))**2))
    ax.fill_between(x2, y2+CI, y2-CI, color='#b9cfe7', edgecolor='')

    '''Minor hack for labeling CI fill_between()'''
    ax.plot(x2, y2+CI, '-', color='#b9cfe7', label='95% Confidence Limits')

    # Prediction Interval
    PI = t*s_err*np.sqrt(1+1/n+(x2-np.mean(x))**2/np.sum((x-np.mean(x))**2))
    ax.fill_between(x2, y2+PI, y2-PI, color='None', linestyle='--')
    ax.plot(x2, y2-PI, '--', color='0.5', label='95% Prediction Limits')
    ax.plot(x2, y2+PI, '--', color='0.5')

    # Annotate plot with R^2
    conv.add_text(ax, "C", r_2)

def add_x_y_line(ax, min_val, max_val):
    lims = [min_val, max_val]
#        np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
#        np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
#    ]

    # now plot both limits against eachother
    ax.plot(lims, lims, 'k-', alpha=0.75, zorder=0)
