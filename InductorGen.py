#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# kickthemout.py

from classes.inductor import induct
from classes.polygon import poly
from math import cos,sin,tan,radians,sqrt
import matplotlib.pyplot as plt
import gdspy


# Defining user's Widgets Variables
# d : length of the square 
# s : number of sides of the geometry
# t : number of turns
# l : length of a turn
# p : space between the turns
# r : tapering coeficiant
# deg : degrese of the crossings
# o : overlap of the crossings
# mv : margin between the vias and the M5 crossings

s = widgets.Dropdown( # Defining all the sliders 
        options=['4', '8'],
        value='8',
        disabled=False, 
    )
d = widgets.IntSlider(
        value=250,
        min=1,
        max=1000,
        step=1,
        disabled=False,
    )
t = widgets.IntSlider(
        value=5,
        min=1,
        max=20,
        step=1,
        disabled=False,
    )
l = widgets.IntSlider(
        value=10,
        min=1,
        max=35,
        step=1,
        disabled=False,
    )
p = widgets.IntSlider(
        value=4,
        min=1,
        max=10,
        step=1,
        disabled=False,
    )
r = widgets.FloatSlider(
        value=0.8,
        min=0.1,
        max=1,
        step=0.01,
        disabled=False,
    )
deg = widgets.IntSlider(
        value=45,
        min=1,
        max=90,
        step=1,
        disabled=False,
    )
o = widgets.IntSlider(
        value=10,
        min=1,
        max=30,
        step=1,
        disabled=False,
    )
mv = widgets.FloatSlider(
        value=0.80,
        min=0.1,
        max=10,
        step=0.01,
        disabled=False,
    )

ui = widgets.VBox([ # because the descriptions are too long and make the sider too short, we concat each slider with a label
        widgets.HBox([widgets.Label('Number of sides (s): '),s]), 
        widgets.HBox([widgets.Label('Length of the inscribed square (d): '),d]), 
        widgets.HBox([widgets.Label('Number of turns of the inductor (t): '),t]), 
        widgets.HBox([widgets.Label('Lenght of a turn (l): '),l]), 
        widgets.HBox([widgets.Label('Space between the turns (p): '),p]), 
        widgets.HBox([widgets.Label('Tapering coefficiant (r): '),r]), 
        widgets.HBox([widgets.Label('Degres of the crossings (deg): '),deg]), 
        widgets.HBox([widgets.Label('Overlap of the crossings (o): '),o]), 
        widgets.HBox([widgets.Label('Margin between the vias and the M5 crossings (mv): '),mv])
    ])


save_btn = widgets.Button(description="Export as gds") # Making the savefile form
save_label = widgets.Label("Export inducance with filename :")
save_txtbox = widgets.Text(
    value='out-file.gds',
    placeholder='Name of the file with .gds',
    description='',
    disabled=False
)
save_box = widgets.HBox([save_label,save_txtbox,save_btn]) # And wrap each element 


widgets.jsdlink((l, 'value'), (mv, 'max')) # because physicaly the margin can not exceed the length






# Math Calculation
def give_a(s):       # those are meaningless and useless without the context ...
    return 360/int(s)

def give_rad(d,a):
    return (d/2)/(cos(radians(a/2)))

def give_cr(l,deg): # distance betwenn the crossings
    return l/tan(radians(deg))



# Math Formula
def L(xa,ya,xb,yb): # formula of the length between two points 
    return sqrt((xa-xb)**2+(ya-yb)**2)


# Array convertion
# Matplotlib take the points in two arrays : [x1,x2,x3,...],[y1,y2,y3,...] but gdspy uses one array of tuples : [(x1,y1),(x2,y2),(x3,y3),(...)]
# This function will do the convertion
def ar_to_tu(x,y):
    if len(x) == len(y):
        i = 0
        result = []
        while i < len(x):
            result.append((x[i],y[i]))
            i += 1
        return result
    else:
        raise ValueError('Length of x and y should be same .')


#  Setup the gds cell where we will write
cell = gdspy.Cell('Inductor', True)



# Setup the gdwrite function
# This function is just to make thing faster
def gdwrite(a,l):
    cell.add(gdspy.Polygon(a,layer=l))


# Setup the fusion function
# This function will help us to merge two polygons
def fusion(a,b):
    for l in a[::-1]:
        for ll in b:
            if ll == l:
                a.remove(l)
    return a[::-1] + b



# Setup the reset_gdspy function
# This function prevent gdspy from superimposing the new impetance when we genrerate more than one after running the program
def reset_gdspy():
    cell.remove_polygons(lambda pts, layer, datatype:
                     layer == 0)
    cell.remove_polygons(lambda pts, layer, datatype:
                     layer == 1)
    cell.remove_polygons(lambda pts, layer, datatype:
                     layer == 2)



# Generating the finale inductor :
def inrealtime(s,d,l,deg,t,p,r,o,mv): # this function is executed each time we change the value of a slider an it updates the drawing
    reset_gdspy()
    a = give_a(int(s))
    rad = give_rad(d,a) # the math things are recalcuated each time because of slider's change 
    cr = give_cr(l,deg)
    
    if not "inductor" in dir(): # ckeck if the class have ever been instancied (we gain some time by just updating the already instancied class)
        inductor = induct(a,rad,t,l,int(s),d,p,r,deg,o,mv,cr)
    else:
        
        inductor.a = a
        inductor.rad = rad
        inductor.cr = cr
        inductor.t = t
        inductor.l = l
        inductor.s = int(sp)

        inductor.d = d
        inductor.p = p
        inductor.r = r
        inductor.deg = deg
        inductor.o = o
        inductor.mv = mv
        
    x,y = inductor.generate()
    inductor.draw(x,y) 
    
    plt.axis('equal') 
    plt.title("Drawing of the inductor")
    plt.xticks([])
    plt.yticks([])
    plt.show() 
    plt.close()

    print("\x1b[31mBe Careful !! For the vias area and the angles MatPlotLib \nisn't representative !!\nDue to the length of the lines\x1b[0m")
    
    
     
iorealtime = interactive_output(inrealtime,{
    "s" : s, 
    "d" : d, 
    "l" : l, 
    "deg" : deg, 
    "t" : t, 
    "p" : p, 
    "r" : r,
    "o" : o,
    "mv" : mv,
})


# Prepare the export of the finale inductor to a .gdc file :



def save(a): # when the button trigger this function, it give a positionnal argument so we need to recive it in order to make it work ...
    writer = gdspy.write_gds(save_txtbox.value,cells=[cell], unit=1.0e-6,precision=1.0e-9)


# Wrap everything into a widget and display it



save_btn.on_click(save) 
finale_widget = widgets.Accordion(children=[widgets.VBox([widgets.HBox([iorealtime,ui]),save_box])])
display(finale_widget)

