#!/usr/bin/env python

"""Convenience module to prep various plot functions"""

import os
import matplotlib.pyplot as plt

def create_ax(x_dim, y_dim, shx=False, shy=False):

    """Creates a fig and axarr and returns them"""

    fig,axarr = plt.subplots( y_dim, x_dim, sharex=shx, sharey=shy, squeeze=False )

    return fig,axarr

def save_fig(fig, infilename, suffix, width, height, tight=True):

    """Performs several functions related to saving figures, i.e. fontsize, tickparams, filename, and size"""

    plt.rcParams.update({'font.size': 8})

    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='on',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='on')

    #plt.tick_params(
    #   axis='y',          # changes apply to the x-axis
    #   which='both',      # both major and minor ticks are affected
    #   left='on',      # ticks along the bottom edge are off
    #   right='off',         # ticks along the top edge are off
    #   labelleft='on')

    root, ext = os.path.splitext(infilename)
    if len(suffix) > 0:
        out_fig = '%s_%s.png' % (root, suffix)    
    else:
        out_fig = '%s.png' % (root)

    fig.set_tight_layout(tight)

    fig.set_size_inches(width, height, dpi=120) 
    fig.savefig(out_fig)

def add_text(ax, prefix, dec_text):
    ax.text(0.8,0.9,'%s:%0.2f\n'% (prefix, dec_text),transform=ax.transAxes,fontsize=8)

def add_text_dict(ax, dict_text):
    start_y = 0.9
    for k, v in dict_text.items():
        ax.text(0.8,start_y,'%s:%0.2f\n'% (k, v),ha="right",transform=ax.transAxes,fontsize=8)
        start_y -= 0.05

#TODO add custom location settings that place legend outside axes
def add_legend(ax, location="upper center"):
    ax.legend(loc=location, bbox_to_anchor=(0.5, 1.05),
              ncol=3, fancybox=True, shadow=True)

def add_ver_line(ax, ymin=0, ymax=1, x=0, color='k'):

    ax.axvline(x=x, ymin=ymin, ymax=ymax, color=color)

def add_hor_line(ax, xmin=0, xmax=1, y=0, color='k'):

    ax.axhline(y=y, xmin=xmin, xmax=xmax, color=color)
