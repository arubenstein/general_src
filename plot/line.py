#!/usr/bin/env python

"""Convenience module to plot various line functions"""
import conv
import matplotlib.pyplot as plt

def plot_series(ax, lines, title, x_axis, y_axis, marker='o', linestyle='-', legend=True): 
    ax.set_title(title)

    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)

    #not in use currently
    patterns = ('>', 'o', 'D', '*', '^','s')
    colors = ('cyan', 'orange', 'greenyellow', 'steelblue', 'crimson', 'gold', 'yellow', 'greenyellow',
		'aquamarine', 'teal', 'cyan', 'steelblue', 'darkblue', 'slateblue', 'darkorchid',
		'deeppink', 'crimson') 
    for (x,y,label), color in zip(lines, colors):
        draw_actual_plot( x, y, label, ax, color=color, marker=marker, linestyle=linestyle) 

    if legend:
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
              ncol=3, fancybox=True, shadow=True)

def draw_actual_plot( x, y, label, ax, color = None, marker='o', linestyle='-', title=None, x_axis=None, y_axis=None):
    if color is None:
     	color = ax._get_lines.color_cycle.next()
    ax.plot(y, label=label, color=color, marker=marker, linestyle=linestyle)

    if title is not None:
        ax.set_title(title)
    if x_axis is not None:
        ax.set_xlabel(x_axis)
    if y_axis is not None:
        ax.set_ylabel(y_axis)
    
    ax.set_xticks(range(len(x)), x)


