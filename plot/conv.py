#!/usr/bin/env python

"""Convenience module to prep various plot functions"""

import os
import matplotlib.pyplot as plt

def create_ax(x_dim, y_dim, shx=False, shy=False):

    """Creates a fig and axarr and returns them"""

    fig,axarr = plt.subplots( y_dim, x_dim, sharex=shx, sharey=shy, squeeze=False )

    return fig,axarr

def save_fig(fig, infilename, suffix, width, height, tight=True, size=8, extra_artists=None, dpi=400, format="png"):

    """Performs several functions related to saving figures, i.e. fontsize, tickparams, filename, and size"""

    plt.rcParams.update({'font.size': size})
    # Say, "the default sans-serif font is COMIC SANS"
    plt.rcParams['font.sans-serif'] = "Arial"
    # Then, "ALWAYS use sans-serif fonts"
    plt.rcParams['font.family'] = "sans-serif"
    plt.rcParams['mathtext.default'] = "regular"

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

    if format == 'png':
        root, ext = os.path.splitext(infilename)
        if len(suffix) > 0:
            out_fig = '%s_%s.%s' % (root, suffix, format)    
        else:
            out_fig = '%s.%s' % (root, format)
    else:
	out_fig = infilename

    fig.set_tight_layout(tight)

    fig.set_size_inches(width, height) 

    if extra_artists:
        fig.savefig(out_fig, bbox_extra_artists=(extra_artists,), bbox_inches='tight', dpi=dpi, format=format)
    else:
	fig.savefig(out_fig, dpi=dpi, format=format)

def add_text(ax, prefix, dec_text):
    ax.text(0.75,0.8,'%s: %0.2f\n'% (prefix, dec_text),transform=ax.transAxes,fontsize=8)

def add_text_dict(ax, dict_text):
    start_y = 0.9
    for k, v in dict_text.items():
        ax.text(0.8,start_y,'%s:%0.2f\n'% (k, v),ha="right",transform=ax.transAxes,fontsize=8)
        start_y -= 0.05

def annotate_point_arrow(ax, x, y, text, xytext=(-20,20), textcoords='offset points', color='k', fontweight='regular', size=8):
    ax.annotate(text, xy=(x,y), xytext=xytext,
            textcoords=textcoords, ha='center', va='bottom', color=color,
            bbox=dict(boxstyle='round,pad=0.2', fc='white', alpha=0.5),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2',
                            color='black'),size=size, fontweight=fontweight)

def annotate_point(ax, x, y, text, size=8):
    ax.annotate(text, xy=(x,y), xytext=(-3,3),
            textcoords='offset points', ha='center', va='bottom',
            size=size)

def add_text_adjust(ax, x, y, text, size=8, color='k', fontweight='regular', bbox=False):
    if bbox:
        bbox_props = dict(boxstyle='round,pad=0.2', fc='white', alpha=0.5, lw=1.0)
	t = ax.text(x, y, text, fontsize=size, color=color, fontweight=fontweight, bbox=bbox_props, rotation=90)
    else:
        t = ax.text(x, y, text, fontsize=size, color=color, fontweight=fontweight, rotation=90)
    return t 

def add_legend(ax, location="upper center", bbox_to_anchor=None, ncol=1, size=12, shadow=True):
    lgd = ax.legend(loc=location, bbox_to_anchor=bbox_to_anchor,
              ncol=ncol, fancybox=True, shadow=shadow, prop={'size':size})
    return lgd

def add_ver_line(ax, ymin=0, ymax=1, x=0, color='k'):

    ax.axvline(x=x, ymin=ymin, ymax=ymax, color=color)

def add_hor_line(ax, xmin=0, xmax=1, y=0, color='k'):

    ax.axhline(y=y, xmin=xmin, xmax=xmax, color=color)
