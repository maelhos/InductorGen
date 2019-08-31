#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# InductorGen.polygon
from module.utils import snaptogrid
from math import cos,sin,radians
# Defining the "poly" function wich take :
# rad : radius of the circle 
# s : number of sides of the geometry


def poly(radius, sides,a,s,ggg): # this function return an array on point for one geometry (one polygon)
        
    x = []
    y = []
    i = 1
    
    
    if s == 4 : # i2 is weird but here are some values of it ... (in fact too much values are useless because we only do octagon )
        i2 = 45+90
    elif s == 8:
        i2 = 22.5
    
    while i < sides + 1 :

        x.append(snaptogrid(radius*cos(radians(a+i2)),ggg))
        y.append(snaptogrid(radius*sin(radians(a+i2)),ggg))
                 
        i += 1
        i2 += a
    return x,y

