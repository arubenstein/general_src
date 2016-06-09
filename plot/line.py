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

    for x,y,label in lines:
        plot_line( x, y, label, ax):        

def plot_line ( x, y, label, ax,pattern, color = ax._get_lines.color_cycle.next() ):
    ax.plot(x, y, label=label)
    
    x_tick_marks=[0]
    x_tick_marks.extend(x)
    x_tick_marks.append(x[len(x)-1]+1)
    ax.set_xticks(x_tick_marks)

    ax.set_xticks(x_tick_marks)
    plt.legend(loc='upper right')

