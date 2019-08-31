#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# InductorGen

from math import cos,sin,tan,radians,sqrt
# Array convertion
# Matplotlib take the points in two arrays : [x1,x2,x3,...],[y1,y2,y3,...] but gdspy uses one array of tuples : [(x1,y1),(x2,y2),(x3,y3),(...)]
# This function will do the convertion

# Snap to Grid
def snaptogrid(coo,ggg):
    if type(coo) == int or type(coo) == float:
        return round(coo / ggg) * ggg
    elif type(coo) == list:
        r = []
        for l in coo:
            r.append(snaptogrid(l,ggg))
        return ''.join(r)

def ar_to_tu(x,y,ggg):
    if len(x) == len(y):
        i = 0
        result = []
        while i < len(x):
            result.append((snaptogrid(x[i],ggg),snaptogrid(y[i],ggg)))
            i += 1
        return result
    else:
        raise ValueError('Length of x and y should be same .')

# Setup the fusion function
# This function will help us to merge two polygons
def fusion(a,b):
    for l in a[::-1]:
        for ll in b:
            if ll == l:
                a.remove(l)
    return a[::-1] + b


# Math Calculation
def give_a(s):       # those are meaningless and useless without the context ...
    return 360/s
def snaptogrid(coo,ggg):
    return round(coo / ggg) * ggg

def give_rad(d,a):
    return (d/2)/(cos(radians(a/2)))


# Math Formula
def L(xa,ya,xb,yb): # formula of the length between two points 
    return sqrt((xa-xb)**2+(ya-yb)**2)





















