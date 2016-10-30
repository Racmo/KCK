#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division             # Division in Python 2.7
import matplotlib
matplotlib.use('Agg')                       # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np
import colorsys as col

from matplotlib import colors

def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    #rc('text', usetex=True) 
    #rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400         # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)


    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3]/2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.jpg')


def hsv2rgb(h, s, v):
    if s == 0.0:
        return v, v, v

    i = int(h/60)
    f = (h/60) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6

    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q


def gradient_rgb_bw(v):
    return (v, v, v)


def gradient_rgb_gbr(v):
    if v < (1/2):
        return (0, 1-2*v, v*2)
    if v >= (1/2):
        return ((v-0.5)*2, 0, 1-2*(v-0.5))


def gradient_rgb_gbr_full(v):
    if v <= (1/4):
        #green->cyan
        return (0, 1, v*4)
    elif v <= (2/4):
        #cyan->blue
        return(0, 1-4*(v-0.25), 1)
    elif v <= (3/4) :
        #blue->magenta
        return(4*(v-0.5), 0, 1)
    else:
        #magenta->red
        return(1, 0, 1-4*(v-0.75))


def gradient_rgb_wb_custom(v):
    if v <=(1/7):
        #white->magenta
        return (1, 1-v*7, 1)
    elif v <=(2/7):
        #magenta->blue
        return (1-7*(v-(1/7)), 0, 1)
    elif v <=(3/7):
        #blue->cyan
        return (0, 7*(v-(2/7)), 1)
    elif v <=(4/7):
        #cyan->green
        return (0, 1, 1-7*(v-(3/7)))
    elif v <=(5/7):
        #green->yellow
        return (7*(v-(4/7)), 1, 0)
    elif v <=(6/7):
        #yellow->red
        return (1, 1-7*(v-(5/7)), 0)
    else:
        #red->black
        return (1-7*(v-(6/7)), 0, 0)



def gradient_hsv_bw(v):
    h=0
    s=0
    val=v

    return hsv2rgb(h, s, val)


def gradient_hsv_gbr(v):
    s=1
    val=1
    h= ((v*240)+120)  #zielony to 120 a czerwony to 1, dzieli je kąt 240 stopni, dodajemy 120 bo chcemy zacząć od zielonego
    return hsv2rgb(h, s, val)

def gradient_hsv_unknown(v):
    s=0.5
    val=1
    h= (120 - (v*120))
    print("h: ", h)
    return hsv2rgb(h, s, val)


def gradient_hsv_custom(v):
    s=1-v
    print("s:", s)
    val=1
    h=v*360
    return hsv2rgb(h, s, val)


if __name__ == '__main__':
    def toname(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [toname(g) for g in gradients])
