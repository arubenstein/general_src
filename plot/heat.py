#!/usr/bin/env python

"""Convenience module to plot heatmap colorbar functions"""
import conv
import scipy.stats as stats
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
#from pylab import *

def plot_colorbar(ax, vmin=0.0, vmax=1.0, cmap="Blues"):

    gradient = np.linspace(vmax, vmin, 256)
    gradient = np.array(zip(gradient,gradient))
    ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(cmap))
    
    plt.tick_params(
    axis='y',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off', # labels along the bottom edge are off
    labeltop='off',
    left='off',      # ticks along the bottom edge are off
    right='off',         # ticks along the top edge are off
    labelright='off',
    labelleft='off') # labels along the bottom edge are off

    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
    '''
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower ofset). Should be between
          0.0 and `midpoint`.
      midpoint : The new center of the colormap. Defaults to 
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax/(vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highets point in the colormap's range.
          Defaults to 1.0 (no upper ofset). Should be between
          `midpoint` and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap

def offsetColorMap(cmap, start=0, stop=1.0, name='offsetcmap'):
    '''
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower ofset). Should be between
          0.0 and `midpoint`.
      stop : Offset from highets point in the colormap's range.
          Defaults to 1.0 (no upper ofset). Should be between
          `midpoint` and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    shift_index = np.linspace(0.0, 1.0, 257)


    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap

def plot_heatmap(ax, data, colormap, xticks, yticks, xticklabels, yticklabels, xlabel, ylabel, title, colorbar_fig=None, set_under_color=None, sep_colorbar=False):
    CS = ax.pcolor(data, cmap=colormap, vmin=0.0, vmax=1.0)

    ax.set_xticklabels('')
    ax.set_yticklabels('')

    ax.set_xticks(xticks, minor=True)
    ax.set_yticks(yticks, minor=True)
    ax.set_xticklabels(xticklabels, minor=True, rotation=90)
    ax.set_yticklabels(yticklabels, minor=True)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    ax.tick_params(
    axis='both',          # changes apply to the x-axis
    which='major',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    left='off',
    right='off')

    if set_under_color:
        colormap.set_under(color=set_under_color)

    if colorbar_fig and not sep_colorbar:
    
    #axarr[0,0].set_ylim(0, len(sequences))
        colorbar_fig.subplots_adjust(right=0.8)
        cbar_ax = colorbar_fig.add_axes([0.85, 0.15, 0.05, 0.7])

        plt.colorbar(CS, cax=cbar_ax)

    if colorbar_fig and sep_colorbar:
        plt.colorbar(CS, cax=colorbar_fig)
