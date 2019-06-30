#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# InductorGen

from math import cos,tan,radians,sqrt
from module.inductor import induct,reset_gdspy,write,preview
import matplotlib.pyplot as plt
from module.utils import *
import argparse
import gdspy



# Defining user's argument Variables
# and parsing the argument

#  Required
# -l or --length -> d : Length of the inscribed square 
# -s or --sides -> s : Number of sides of the geometry (only 4 or 8)
# -t or --turns -> t : Number of turns of the inductor
# -lt or --lenturn -> l : Length of a turn
# -p or --space -> p : Space between the turns
# -r or --tap -> r : Tapering coeficiant
# -v or --overlap -> o : Overlap of the crossings
# -m or --margin -> mv : Margin between the vias and the M5 crossings
# ------------------------------ #
#  Optional
# -d or --deg -> deg : Degrese of the crossings (45° by default)
# -o or --output -> Filename of the gds out (keep empty if you only want preview)
# --disable-preview -> Disable GDS output preview
# --disable-save -> Disable GDS file saving 

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--length", type=float,help="Length of the inscribed square ", required=True)
parser.add_argument("-s", "--sides", type=int, choices=[4,8],help="Number of sides of the geometry (only 4 or 8)", required=True)
parser.add_argument("-t", "--turns", type=int,help="Number of turns of the inductor", required=True)
parser.add_argument("-lt", "--lenturn", type=float,help="Length of a turn", required=True)
parser.add_argument("-p", "--space", type=float,help="Space between the turns", required=True)
parser.add_argument("-r", "--tap", type=float,help="Tapering coeficiant", required=True)
parser.add_argument("-v", "--overlap", type=float,help="Overlap of the crossings", required=True)
parser.add_argument("-m", "--margin", type=float,help=" Margin between the vias and the M5 crossings", required=True)


parser.add_argument("-d", "--deg", type=float,help="Degrese of the crossings",default=45)
parser.add_argument("-o", "--output", type=str,help="Filename of the gds out")
parser.add_argument("--disablepreview", help="Disable GDS output preview",action="store_true")
parser.add_argument("--disablesave", help="Disable GDS file saving ",action="store_true")
args = parser.parse_args()


s = args.sides
d = args.length
t = args.turns
l = args.lenturn
p = args.space
r = args.tap
deg = args.deg
o = args.overlap
mv = args.margin

filename = args.output
if not filename[-3:] == ".gds": # if the correct extention isn't already set, set it
    filename += ".gds"


# Generating the finale inductor :

reset_gdspy()
a = give_a(s)
rad = give_rad(d,a) # the math things are recalcuated each time because of slider's change 
cr = give_cr(l,deg)
    
inductor = induct(a,rad,t,l,s,d,p,r,deg,o,mv,cr)
        
x,y = inductor.generate()
inductor.draw(x,y) 
if not args.disablepreview:  
    gdspy.LayoutViewer(cells=[preview()])

    #plt.axis('equal') 
    #plt.title("Drawing of the inductor")
    #plt.xticks([])
    #plt.yticks([])
    #plt.show() 
plt.close()

print("\x1b[31mBe Careful !! For the vias area and the angles MatPlotLib \nisn't representative !!\nDue to the length of the lines\x1b[0m")
    
    
if not args.disablesave:
    write(filename)

