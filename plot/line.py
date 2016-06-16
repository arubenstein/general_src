#!/usr/bin/env python

"""Convenience module to plot various line functions"""
import conv
import matplotlib.pyplot as plt

def draw_actual_plot(ax, lines, title, x_axis, y_axis): 
    ax.set_title(title)

    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)

    #not in use currently
    patterns = ('>', 'o', 'D', '*', '^','s')
    colors = ('black', 'darkgrey', 'lightcoral', 'orangered', 'orange', 'gold', 'yellow', 'greenyellow',
		'aquamarine', 'teal', 'cyan', 'steelblue', 'darkblue', 'slateblue', 'darkorchid',
		'deeppink', 'crimson') 
    for (x,y,label), color in zip(lines, colors):
        plot_line( x, y, label, ax, color=color) 

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
              ncol=3, fancybox=True, shadow=True)

def plot_line ( x, y, label, ax, color = None):
    if color is None:
     	color = ax._get_lines.color_cycle.next()
    ax.plot(y, label=label, color=color)
    
#    x_tick_marks=[0]
#    x_tick_marks.extend(x)
#    x_tick_marks.append(x[len(x)-1]+1)
    ax.set_xticks(range(len(x)), x)

    plt.legend(loc='upper right')

