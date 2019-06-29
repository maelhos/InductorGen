#!/usr/bin/env python3
# -.- coding: utf-8 -.-
# kickthemout.py

# <p style="text-align: right;">Maël HOSTETTLER</p>
# <h1 style="text-align: center;">Python Inductor drawing librarie </h1>
# 
# 
# ###  1) Libraries Import

# In[1]:


from ipywidgets import interact, interactive, fixed, interact_manual, interactive_output
import ipywidgets as widgets
from math import cos,sin,tan,radians,sqrt
import matplotlib.pyplot as plt
import gdspy


# ###  2) Defining user's Widgets Variables
# * #### d : length of the square 
# * #### s : number of sides of the geometry
# * #### t : number of turns
# * #### l : length of a turn
# * #### p : space between the turns
# * #### r : tapering coeficiant
# * #### deg : degrese of the crossings
# * #### o : overlap of the crossings
# * #### mv : margin between the vias and the M5 crossings

# In[ ]:


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


# ###  3) Math Calculation

# In[ ]:


def give_a(s):       # those are meaningless and useless without the context ...
    return 360/int(s)

def give_rad(d,a):
    return (d/2)/(cos(radians(a/2)))

def give_cr(l,deg): # distance betwenn the crossings
    return l/tan(radians(deg))


# ###  4) Math Formula

# In[ ]:


def L(xa,ya,xb,yb): # formula of the length between two points 
    return sqrt((xa-xb)**2+(ya-yb)**2)


# ###  5) Array convertion
# ##### Matplotlib take the points in two arrays : [x1,x2,x3,...],[y1,y2,y3,...] but gdspy uses one array of tuples : [(x1,y1),(x2,y2),(x3,y3),(...)]
# ##### This function will do the convertion

# In[ ]:


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


# ###  6) Setup the gds cell where we will write

# In[ ]:


cell = gdspy.Cell('Inductor', True)


# ###  7) Setup the gdwrite function
# ##### This function is just to make thing faster

# In[ ]:


def gdwrite(a,l):
    cell.add(gdspy.Polygon(a,layer=l))


# ###  8) Setup the fusion function
# ##### This function will help us to merge two polygons

# In[ ]:


def fusion(a,b):
    for l in a[::-1]:
        for ll in b:
            if ll == l:
                a.remove(l)
    return a[::-1] + b


# ###  9) Setup the reset_gdspy function
# ##### This function prevent gdspy from superimposing the new impetance when we genrerate more than one after running the program
# 

# In[ ]:


def reset_gdspy():
    cell.remove_polygons(lambda pts, layer, datatype:
                     layer == 0)
    cell.remove_polygons(lambda pts, layer, datatype:
                     layer == 1)
    cell.remove_polygons(lambda pts, layer, datatype:
                     layer == 2)


# ###  5) Defining the induct class wich take :
# * #### a : angle
# * #### rad : radius of the circle
# * #### t : number of turns
# * #### p : space between the turns

# In[ ]:


lstx = [] # lstx and lsty will be a temporary variable for each plot or fill of matplotlib and gdspy,   
lsty = []#    we use it to make the gdspy's implementation more simple
class induct:
    
    def __init__(self, angle, radius, turns, length, sides, d, p, r, deg, o, mv,cr):
        # we initialyse all the parameters
        self.a = angle
        self.rad = radius
        self.cr = cr
        
        self.t = turns
        self.l = length
        self.s = int(sides)
        
        self.d = d
        self.p = p
        self.r = r
        self.deg = deg
        self.o = o
        self.mv = mv
        
    def generate(self): # this fumction draw the natives poligon
        i = 1
        
        x = []
        y = []    
        tx = []
        ty = []
    
        rr = 0
        lenn = self.l
        while i < self.t + 1:
            
            tx,ty = poly(self.rad - rr,self.a * 360,self.a,self.s)
            rr += lenn
            lenn = lenn*self.r
            x.append(tx)
            y.append(ty)
            
            tx,ty = poly(self.rad - rr,self.a * 360,self.a,self.s)
            x.append(tx)
            y.append(ty)
            rr += self.p
        
            i += 1
        return x,y
    
    def draw_poly(self,x,y): # this function is call "draw_poly" but in fact it just delete the useless lines in the poligon
        i = 0
        while i < len(x):#    
            lstx = x[i][1:self.s//2+1]
            lsty = y[i][1:self.s//2+1]
            plt.plot(lstx,lsty,c="black") 
            
            lstx = x[i][self.s//2+1:self.s + 1]
            lsty = y[i][self.s//2+1:self.s + 1]
            plt.plot(lstx,lsty,c="black")# 
            i += 1
        i = 0
        while i < len(x):#    
            lstx = x[i][1:self.s//2+1] + [x[i+1][1]] + x[i+1][1:self.s//2+1][::-1] + [x[i+1][1]] 
            lsty = y[i][1:self.s//2+1] + [-y[i][1]] + y[i+1][1:self.s//2+1][::-1] + [y[i][1]] 
            gdwrite(ar_to_tu(lstx,lsty),2)
            
            
            lstx = x[i][self.s//2+1:self.s + 1] + [-x[i+1][1]]  + x[i+1][self.s//2+1:self.s + 1][::-1] + [-x[i+1][1]] 
            lsty = y[i][self.s//2+1:self.s + 1] + [y[i][1]] + y[i+1][self.s//2+1:self.s + 1][::-1] + [-y[i][1]] 
            gdwrite(ar_to_tu(lstx,lsty),2)
            
            i += 2
    def draw_input(self,x,y): # this function just draw LINE BY LINE the input of the inductor
        lstx1,lsty1,lstx2,lsty2 = [],[],[],[]
        
        
        lstx = [self.p+self.l,self.p+self.l]+[self.p,self.p][::-1]
        lsty = [y[0][4:6][0],y[0][4:6][0]-self.l]+[y[1][4:6][0],y[0][4:6][0]-self.l][::-1]
        plt.plot(lstx,lsty,c="black")
        
        lstx1 = [-x[1][4:6][0],self.p+self.l]
        lsty1 = [y[0][4:6][0],y[0][4:6][0]]
        plt.plot(lstx1,lsty1,c="black")
        
        
        lstx2 = [self.p,x[1][4:6][1]]
        lsty2 = [y[1][4:6][0],y[1][4:6][1]]
        plt.plot(lstx2,lsty2,c="black")
        
        gdwrite(fusion(ar_to_tu(lstx,lsty) , ar_to_tu(lstx1[::-1],lsty1[::-1]) + ar_to_tu(lstx2[::-1],lsty2[::-1])),2)
        
        
        lstx = [-self.p-self.l,-self.p-self.l]+[-self.p,-self.p][::-1]
        lsty = [y[0][4:6][0],y[0][4:6][0]-self.l]+[y[1][4:6][0],y[0][4:6][0]-self.l][::-1]
        plt.plot(lstx,lsty,c="black")
    
        
        lstx1 = [x[1][4:6][0],-self.p-self.l]
        lsty1 = [y[0][4:6][0],y[0][4:6][0]]
        plt.plot(lstx1,lsty1,c="black")
                                                  
        lstx2 = [-self.p,x[1][4:6][0]]
        lsty2 = [y[1][4:6][0],y[1][4:6][0]]  
        plt.plot(lstx2,lsty2,c="black")
 
        gdwrite(fusion(ar_to_tu(lstx,lsty) , ar_to_tu(lstx1[::-1],lsty1[::-1]) + ar_to_tu(lstx2[::-1],lsty2[::-1])),2)

    
        lstx1,lsty1,lstx2,lsty2 = [],[],[],[]
        
        
        lstx = [self.p+self.l,self.p+self.l]+[self.p,self.p][::-1]
        lsty = [y[0][4:6][0],y[0][4:6][0]-self.l]+[y[1][4:6][0],y[0][4:6][0]-self.l][::-1]
        plt.plot(lstx,lsty,c="black")
        
        lstx1 = [-x[0][4:6][0],self.p+self.l]
        lsty1 = [y[0][4:6][0],y[0][4:6][0]]
        plt.plot(lstx1,lsty1,c="black")
        
        
        lstx2 = [self.p,x[1][4:6][1]]
        lsty2 = [y[1][4:6][0],y[1][4:6][1]]
        plt.plot(lstx2,lsty2,c="black")
                
        
        lstx = [-self.p-self.l,-self.p-self.l]+[-self.p,-self.p][::-1]
        lsty = [y[0][4:6][0],y[0][4:6][0]-self.l]+[y[1][4:6][0],y[0][4:6][0]-self.l][::-1]
        plt.plot(lstx,lsty,c="black")
    
        
        lstx1 = [x[0][4:6][0],-self.p-self.l]
        lsty1 = [y[0][4:6][0],y[0][4:6][0]]
        plt.plot(lstx1,lsty1,c="black")
                                                  
        lstx2 = [-self.p,x[1][4:6][0]]
        lsty2 = [y[1][4:6][0],y[1][4:6][0]]  
        plt.plot(lstx2,lsty2,c="black")    
    
    
    
        
    def draw_cross_edge(self,x,y):# this function just calculate and draw how far the middles lines should go before the crossing
        ab = 0
        i = 0
        crr = self.cr
        if self.t % 2 == 0:
            coe = 1
        else:
            coe = 2
        while i < 2*self.t - coe: # forward the top to the cross
            
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])

            lstx = [x[i][4:6][0] , x[i][4:6][0] + (xy-crr)/2 ]
            lsty = [-y[i][4:6][0] , -y[i][4:6][0]]
            plt.plot( lstx , lsty ,c="black")
            gdwrite(ar_to_tu(lstx,lsty),2)
            
            
            lstx1 = [x[i][4:6][1] , x[i][4:6][1] - (xy-crr)/2 ]
            lsty1 = [-y[i][4:6][1] , -y[i][4:6][1]]
            plt.plot( lstx1 , lsty1 ,c="black")
            gdwrite(ar_to_tu(lstx1,lsty1),2)
            i += 1
            if ab == 1:
                crr = crr*self.r
                ab -= 1
            else:
                ab +=1
        i = 0
        ab = 0
        crr = self.cr
        while i < 2*self.t -coe :
            
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])
            xy1 = L(x[i+1][4:6][0],y[i+1][4:6][0],-(x[i+1][4:6][0]),y[i+1][4:6][0])
            
            lstx = [x[i+1][4:6][0] , x[i+1][4:6][0] + (xy1-crr)/2 ]
            lsty = [-y[i][4:6][0] , -y[i][4:6][0]]
            
            lstx1 = [x[i+1][4:6][0] , x[i+1][4:6][0] + (xy1-crr)/2 ]
            lsty1 = [-y[i+1][4:6][0] , -y[i+1][4:6][0]]
            
            gdwrite(ar_to_tu(lstx + lstx1[::-1],lsty + lsty1[::-1]),2)
            
            lstx = [-x[i+1][4:6][0] , -x[i+1][4:6][0] - (xy1-crr)/2 ]
            lsty = [-y[i][4:6][0] , -y[i][4:6][0]]
            
            lstx1 = [-x[i+1][4:6][0] , -x[i+1][4:6][0] - (xy1-crr)/2 ]
            lsty1 = [-y[i+1][4:6][0] , -y[i+1][4:6][0]]
            
            gdwrite(ar_to_tu(lstx + lstx1[::-1],lsty + lsty1[::-1]),2)           
            i += 2
            if ab == 1:
                crr = crr*self.r
                ab -= 1
            else:
                ab +=1
        i = 2
        ab = 0
        
        if self.t % 2 == 0:
            coe = 1
        else:
            coe = 0
        ab = 0
        crr = self.cr
        while i < 2*self.t - coe: # forward the bottom to the cross
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])

            plt.plot( [x[i][4:6][0] , x[i][4:6][0] + (xy-crr)/2 ] , [y[i][4:6][0] , y[i][4:6][0]] ,c="black")
            plt.plot( [x[i][4:6][1] , x[i][4:6][1] - (xy-crr)/2 ] , [y[i][4:6][1] , y[i][4:6][1]] ,c="black")

            i += 1
            if ab == 1:
                crr = crr*self.r
                ab -= 1
            else:
                ab +=1
        i = 2
        ab = 0
        if self.t % 2 == 0:
            coe = 2
        else:
            coe = 1
        ab = 0
        crr = self.cr
        while i < 2*self.t - coe: 
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])
            xy1 = L(x[i+1][4:6][0],y[i+1][4:6][0],-(x[i+1][4:6][0]),y[i+1][4:6][0])
            
            lstx = [x[i+1][4:6][0] , x[i][4:6][0] + (xy-crr)/2 ]
            lsty = [y[i][4:6][0] , y[i][4:6][0]]
            
            lstx1 = [x[i+1][4:6][0] , x[i][4:6][0] + (xy-crr)/2 ]
            lsty1 = [y[i+1][4:6][0] , y[i+1][4:6][0]]
            
            gdwrite(ar_to_tu(lstx  + lstx1[::-1] ,lsty + lsty1[::-1]),2)
            
            
            
            lstx = [-x[i+1][4:6][0] , -x[i][4:6][0] - (xy-crr)/2 ]
            lsty = [y[i][4:6][0] , y[i][4:6][0]]
            
            lstx1 = [-x[i+1][4:6][0] , -x[i][4:6][0] - (xy-crr)/2 ]
            lsty1 = [y[i+1][4:6][0] , y[i+1][4:6][0]]
            
            gdwrite(ar_to_tu(lstx  + lstx1[::-1] ,lsty + lsty1[::-1]),2)
            
            if ab == 1:
                crr = crr*self.r
                ab -= 1
            else:
                ab +=1

            i += 2
    
    def draw_cross(self,x,y): # this HUGE function draw the cross (both colored and uncolored)
        topcrossx = []
        topcrossy = []
        i = 2
        ab = 0
        abb = 0
        crr = self.cr
        jk = 0
        comp = self.t*2

        while i < comp  : # draw top cross on M6 and generating M5 (M5 is the colored one ...)
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])

            if ab == 0 or ab == 1 :  

                plt.plot( [ x[i][4:6][0] + (xy-crr)/2 , x[i][4:6][0] + (xy-crr)/2 + crr ] , [-(y[i-2][4:6][0]) , -(y[i][4:6][0])] ,c="black")
                if jk == 0 or jk == 2:
                    tempx = []
                    tempy = []

                    tempx.append(-(x[i][4:6][0]+(xy-crr)/2))
                    tempx.append(-(x[i][4:6][0]+(xy-crr)/2+crr ))

                    tempy.append(-(y[i-2][4:6][0]))
                    tempy.append(-(y[i][4:6][0]))
                    jk += 1
                elif jk == 1:

                    tempx.append(-(x[i][4:6][0]+(xy-crr)/2))
                    tempx.insert(len(tempx),-(x[i][4:6][0]+(xy-crr)/2+crr ))

                    tempy.append(-(y[i-2][4:6][0]))
                    tempy.insert(len(tempy),-(y[i][4:6][0]))

                    topcrossx.append(tempx)
                    topcrossy.insert(len(topcrossy),tempy)
                    jk += 1
                elif jk == 3:


                    tempx.append(-(x[i][4:6][0]+(xy-crr)/2))
                    tempx.insert(len(tempx),-(x[i][4:6][0]+(xy-crr)/2+crr ))

                    tempy.append(-(y[i-2][4:6][0]))
                    tempy.insert(len(tempy),-(y[i][4:6][0]))

                    topcrossx.append(tempx)
                    topcrossy.insert(len(topcrossy),tempy)
                    jk = 0

                ab += 1
            elif ab == 2:
                ab = 3
            elif ab == 3:  
                ab = 0
            i += 1 
            if abb == 1:
                crr = crr*self.r
                abb -= 1
            else:
                abb +=1
        
        i = 2
        ab = 0
        jk = 0
        crr = self.cr
        comp = self.t*2
        current = self.l
        while i < comp  : # draw top cross on M6 on gdspy
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])
            xy1 = L(x[i+1][4:6][0],y[i+1][4:6][0],-(x[i+1][4:6][0]),y[i+1][4:6][0])
            #############################3
            lstx = [ x[i][4:6][0] + (xy-crr)/2 , x[i][4:6][0] + (xy-crr)/2 + crr + (current-(current*self.r))]
            lsty = [-(y[i-2][4:6][0]) , -(y[i][4:6][0])]
            if ab == 1:
                crr = crr*self.r
                ab -= 1
            else:
                ab +=1    
            lstx1 = [ x[i+1][4:6][0] + (xy1-crr)/2 , x[i+1][4:6][0] + (xy1-crr)/2 + crr ]
            lsty1 = [-(y[i-1][4:6][0]) , -(y[i+1][4:6][0])]
                
            ptx = x[i][4:6][0] + (xy-crr)/2 + crr + (current-(current*self.r))
            pty = -(y[i+1][4:6][0])
            
            gdwrite(ar_to_tu(lstx+[ptx]+lstx1[::-1],lsty+[pty]+lsty1[::-1]),2)    

            i += 4
            if ab == 1:
                crr = crr*self.r
                ab -= 1
            else:
                ab +=1
            current = current*self.r
        i = 0
        
        
        
        while i < len(topcrossx): # draw top cross on M5 on matplotlib       
            plt.fill(topcrossx[i][:len(topcrossx[i])//2] + topcrossx[i][len(topcrossx[i])//2:][::-1] , topcrossy[i][:len(topcrossy[i])//2] + topcrossy[i][len(topcrossy[i])//2:][::-1],color="orange")
            
            plt.fill([topcrossx[i][0]] + [topcrossx[i][2]] + [topcrossx[i][2]+self.o] + [topcrossx[i][0]+self.o], [topcrossy[i][0]] + [topcrossy[i][2]]*2 + [topcrossy[i][0]],color="orange")
            plt.fill([topcrossx[i][1]] + [topcrossx[i][3]] + [topcrossx[i][3]-self.o] + [topcrossx[i][1]-self.o], [topcrossy[i][1]] + [topcrossy[i][3]]*2 + [topcrossy[i][1]],color="orange")
            
            plt.fill([topcrossx[i][0] + self.mv] + [topcrossx[i][2] + self.mv] + [topcrossx[i][2]+self.o - self.mv] + [topcrossx[i][0]+ self.o - self.mv], [topcrossy[i][0] - self.mv] + [topcrossy[i][2] + self.mv]*2 + [topcrossy[i][0] - self.mv],color="red")
            plt.fill([topcrossx[i][1] - self.mv] + [topcrossx[i][3] - self.mv] + [topcrossx[i][3]-self.o + self.mv] + [topcrossx[i][1]- self.o + self.mv], [topcrossy[i][1] - self.mv] + [topcrossy[i][3] + self.mv]*2 + [topcrossy[i][1] - self.mv],color="red")
             
            i += 1  
        i = 2
        comp = self.t*2
        ab = 0
        crr = self.cr
        current = self.l
        while i < comp  : # draw bottom cross on M5  on gdspy
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])
            xy1 = L(x[i+1][4:6][0],y[i+1][4:6][0],-(x[i+1][4:6][0]),y[i+1][4:6][0])

            lstx2 = [ -x[i][4:6][0] - (xy-crr)/2 + self.o, -x[i+1][4:6][0] - (xy1-crr)/2  + self.o] 
            lsty2 = [-(y[i-2][4:6][0]) , -(y[i-1][4:6][0])]
            if ab == 1:
                crr = crr*self.r
                ab -= 1
            else:
                ab +=1
            lstx3 = [ x[i][4:6][0] + (xy-crr)/2 - self.o, x[i+1][4:6][0] + (xy1-crr)/2  - self.o] 
            lsty3 = [-(y[i+1][4:6][0]) , -(y[i][4:6][0])]
                
            
            lstx = [ -x[i][4:6][0] - (xy-crr)/2 , -x[i][4:6][0] - (xy-crr)/2 - crr - (current-(current*self.r))] 
            lsty = [-(y[i-2][4:6][0]) , -(y[i][4:6][0])] 
            lstx1 = [ -x[i+1][4:6][0] - (xy1-crr)/2 , -x[i+1][4:6][0] - (xy1-crr)/2 - crr ] 
            lsty1 = [-(y[i-1][4:6][0]) , -(y[i+1][4:6][0])]
            
            gdwrite(ar_to_tu(lstx2[::-1]+lstx+lstx3[::-1]+lstx1[::-1],lsty2[::-1]+lsty+lsty3[::-1]+lsty1[::-1]),0)                        
            
            i += 4  
            current = current*self.r
            if ab == 1:
                crr = crr*self.r
                ab -= 1
            else:
                ab +=1
        i = 0
        plus = 0
        while i < len(topcrossx): # draw top vias on M5 on matplotlib   
            
            lstx = [topcrossx[i][0] + self.mv + plus] + [topcrossx[i][2] + self.mv+ plus] + [topcrossx[i][2]+self.o - self.mv+ plus] + [topcrossx[i][0]+ self.o - self.mv+ plus]
            lsty = [topcrossy[i][0] - self.mv] + [topcrossy[i][2] + self.mv]*2 + [topcrossy[i][0] - self.mv]
            gdwrite(ar_to_tu(lstx,lsty),1)
            
            lstx = [topcrossx[i][1] - self.mv - plus] + [topcrossx[i][3] - self.mv - plus] + [topcrossx[i][3]-self.o + self.mv- plus] + [topcrossx[i][1]- self.o + self.mv- plus]
            lsty = [topcrossy[i][1] - self.mv] + [topcrossy[i][3] + self.mv]*2 + [topcrossy[i][1] - self.mv]
            gdwrite(ar_to_tu(lstx,lsty),1)
            
            i += 1  
            plus += self.mv
        i = 2
        ab = 2
        topcrossx = []
        topcrossy = []
        jk = 0
        abb = 0
        crr = self.cr
        while i < comp  : # draw bottom cross on M6 on matplotlib and generate M5 
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])
            if ab == 0 or ab == 1 :  
                lstx = [ x[i][4:6][0] + (xy-crr)/2 , x[i][4:6][0] + (xy-crr)/2 + crr ] 
                lsty = [(y[i-2][4:6][0]) , (y[i][4:6][0])]
                plt.plot( lstx,lsty  ,c="black")

                if jk == 0 or jk == 2:
                    tempx = []
                    tempy = []

                    tempx.append(-(x[i][4:6][0]+(xy - self.cr)/2))
                    tempx.append(-(x[i][4:6][0]+(xy - self.cr)/2+self.cr ))

                    tempy.append(y[i-2][4:6][1])
                    tempy.append(y[i][4:6][1])
                    jk += 1
                elif jk == 1:

                    tempx.append(-(x[i][4:6][0]+(xy - self.cr)/2))
                    tempx.append(-(x[i][4:6][0]+(xy - self.cr)/2+self.cr ))

                    tempy.append(y[i-2][4:6][1])
                    tempy.append(y[i][4:6][1])

                    topcrossx.append(tempx)
                    topcrossy.append(tempy)
                    jk += 1
                elif jk == 3:


                    tempx.append(-(x[i][4:6][0]+(xy - self.cr)/2))
                    tempx.append(-(x[i][4:6][0]+(xy - self.cr)/2+self.cr ))

                    tempy.append(y[i-2][4:6][1])
                    tempy.append(y[i][4:6][1])

                    topcrossx.append(tempx)
                    topcrossy.insert(len(topcrossy),tempy)
                    jk = 0


                ab += 1
            elif ab == 2:
                ab = 3
            elif ab == 3:  
                ab = 0

            i += 1
            if abb == 1:
                crr = crr*self.r
                abb -= 1
            else:
                abb +=1
             
        
        i = 4
        ab = 0
        crr = self.cr
        current = self.l
        while i < comp  : # draw bottom cross on M6  on gdspy
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])
            xy1 = L(x[i+1][4:6][0],y[i+1][4:6][0],-(x[i+1][4:6][0]),y[i+1][4:6][0])

                
            lstx = [ x[i][4:6][0] + (xy-crr)/2 , x[i][4:6][0] + (xy-crr)/2 + crr + (current-(current*self.r))] 
            lsty = [(y[i-2][4:6][0]) , (y[i][4:6][0])]
        
            if ab == 1:
                crr = crr*self.r
                ab -= 1
            else:
                ab +=1    
                
            lstx1 = [ x[i+1][4:6][0] + (xy1-crr)/2 , x[i+1][4:6][0] + (xy1-crr)/2 + crr ] 
            lsty1 = [(y[i-1][4:6][0]) , (y[i+1][4:6][0])]
            
            ptx = x[i][4:6][0] + (xy-crr)/2 + crr + (current-(current*self.r))
            pty = (y[i+1][4:6][0])
            
            gdwrite(ar_to_tu(lstx+[ptx]+lstx1[::-1],lsty+[pty]+lsty1[::-1]),2)                        
            
            i += 4
            if ab == 1:
                crr = crr*self.r
                ab -= 1
            else:
                ab +=1
            current = current*self.r
        i = 0 # 
        while i < len(topcrossx): # draw bottom cross on M5 on matplotlib
            
            plt.fill(topcrossx[i][:len(topcrossx[i])//2] + topcrossx[i][len(topcrossx[i])//2:][::-1] , topcrossy[i][:len(topcrossy[i])//2] + topcrossy[i][len(topcrossy[i])//2:][::-1],color="orange")
            
            plt.fill([topcrossx[i][0]] + [topcrossx[i][2]] + [topcrossx[i][2]+ self.o] + [topcrossx[i][0]+ self.o], [topcrossy[i][0]] + [topcrossy[i][2]]*2 + [topcrossy[i][0]],color="orange")
            plt.fill([topcrossx[i][1]] + [topcrossx[i][3]] + [topcrossx[i][3]- self.o] + [topcrossx[i][1]- self.o], [topcrossy[i][1]] + [topcrossy[i][3]]*2 + [topcrossy[i][1]],color="orange")
                
            # draw the vias   
            plt.fill([topcrossx[i][0] + self.mv] + [topcrossx[i][2] + self.mv] + [topcrossx[i][2]+ self.o - self.mv] + [topcrossx[i][0]+ self.o - self.mv], [topcrossy[i][0] +  self.mv] + [topcrossy[i][2] - self.mv]*2 + [topcrossy[i][0] + self.mv],color="red")
            plt.fill([topcrossx[i][1] - self.mv] + [topcrossx[i][3] - self.mv] + [topcrossx[i][3]- self.o + self.mv] + [topcrossx[i][1]- self.o + self.mv], [topcrossy[i][1] +  self.mv] + [topcrossy[i][3] - self.mv]*2 + [topcrossy[i][1] + self.mv],color="red")
             
            i += 1

        i = 4
        comp = self.t*2
        crr = self.cr
        ab = 0
        current = self.l
        while i < comp  : # draw bottom cross on M5  on gdspy
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])
            xy1 = L(x[i+1][4:6][0],y[i+1][4:6][0],-(x[i+1][4:6][0]),y[i+1][4:6][0])

            lstx2 = [ -x[i][4:6][0] - (xy-crr)/2 + self.o, -x[i+1][4:6][0] - (xy1-crr)/2  + self.o] 
            lsty2 = [(y[i-2][4:6][0]) , (y[i-1][4:6][0])]
            if ab == 1:
                crr = crr*self.r
                ab -= 1
            else:
                ab +=1
            lstx3 = [ x[i][4:6][0] + (xy-crr)/2 - self.o, x[i+1][4:6][0] + (xy1-crr)/2  - self.o] 
            lsty3 = [(y[i+1][4:6][0]) , (y[i][4:6][0])]
                
                
            lstx = [ -x[i][4:6][0] - (xy-crr)/2 , -x[i][4:6][0] - (xy-crr)/2 - crr - (current-(current*self.r))] 
            lsty = [(y[i-2][4:6][0]) , (y[i][4:6][0])] 
            lstx1 = [ -x[i+1][4:6][0] - (xy1-crr)/2 , -x[i+1][4:6][0] - (xy1-crr)/2 - crr ] 
            lsty1 = [(y[i-1][4:6][0]) , (y[i+1][4:6][0])]
            
            gdwrite(ar_to_tu(lstx2[::-1]+lstx+lstx3[::-1]+lstx1[::-1],lsty2[::-1]+lsty+lsty3[::-1]+lsty1[::-1]),0)                        
            
            current = current*self.r
            if ab == 1:
                crr = crr*self.r
                ab -= 1
            else:
                ab +=1

             
            
            
            i += 4   
        i = 0 # 

        plus = 0
        while i < len(topcrossx): # draw bottom vias on M5 on pygds 
            
            lstx = [topcrossx[i][0] + self.mv - plus] + [topcrossx[i][2] + self.mv - plus] + [topcrossx[i][2]+ self.o - self.mv - plus] + [topcrossx[i][0]+ self.o - self.mv - plus]
            lsty = [topcrossy[i][0] +  self.mv] + [topcrossy[i][2] - self.mv]*2 + [topcrossy[i][0] + self.mv]
            gdwrite(ar_to_tu(lstx,lsty),1)
            
            lstx = [topcrossx[i][1] - self.mv + plus] + [topcrossx[i][3] - self.mv+ plus] + [topcrossx[i][3]- self.o + self.mv + plus] + [topcrossx[i][1]- self.o + self.mv + plus]
            lsty = [topcrossy[i][1] +  self.mv] + [topcrossy[i][3] - self.mv]*2 + [topcrossy[i][1] + self.mv]
            
            gdwrite(ar_to_tu(lstx,lsty),1)    
                    
            plus += self.mv
            i += 1
            
    def draw_end(self,x,y): # this fumction draw the "end" by connecting the 2 last cable
        lstx1,lsty1,lstx2,lsty2 = [],[],[],[]
        if self.t % 2 == 0: # connect the last turn in top or bottom depending on the nb of turns ( even or odd number of turns)
            xy = L(x[(self.s + (2*self.t- self.s)-1)][4:6][0],y[(self.s + (2*self.t- self.s)-1)][4:6][1],-(x[(self.s + (2*self.t- self.s)-1)][4:6][0]),y[(self.s + (2*self.t- self.s)-1)][4:6][1])
            
            lstx = [-xy/2 , xy/2 ]
            lsty = [y[(self.s + (2*self.t- self.s))-1][4:6][1] , y[(self.s + (2*self.t- self.s)-1)][4:6][1]]
            plt.plot( lstx , lsty ,c="black")
            
            
            lstx1 = [-xy/2 , xy/2 ]
            lsty1 = [y[(self.s + (2*self.t- self.s))-2][4:6][1] , y[(self.s + (2*self.t- self.s)-2)][4:6][1]]
            plt.plot( lstx1 , lsty1 ,c="black")

            gdwrite(ar_to_tu(lstx + lstx1[::-1] , lsty + lsty1[::-1] ),2)
        else:
            xy = L(x[(self.s + (2*self.t- self.s)-1)][4:6][0],y[(self.s + (2*self.t- self.s)-1)][4:6][0],-(x[(self.s + (2*self.t- self.s)-1)][4:6][0]),y[(self.s + (2*self.t- self.s)-1)][4:6][0])
            
            lstx = [-xy/2 , xy/2 ]
            lsty = [-y[(self.s + (2*self.t- self.s))-1][4:6][0] , -y[(self.s + (2*self.t- self.s)-1)][4:6][0]]
            plt.plot( lstx , lsty ,c="black")
            
            #xy = L(x[(self.s + (2*selft- self.s)-2)][4:6][0],y[(self.s + (2*self.t- self.s)-2)][4:6][0],-(x[(self.s + (2*self.t- self.s)-2)][4:6][0]),y[(self.s + (2*self.t- self.s)-2)][4:6][0])
            
            lstx1 = [-xy/2 , xy/2 ]
            lsty1 = [-y[(self.s + (2*self.t- self.s))-2][4:6][0] , -y[(self.s + (2*self.t- self.s)-2)][4:6][0]]
            plt.plot( lstx1 , lsty1 ,c="black")
        
            gdwrite(ar_to_tu(lstx + lstx1[::-1] , lsty + lsty1[::-1] ),2)
            
            
    def draw(self,x,y): # this function just draw everything by calling all the overs ...
        self.draw_poly(x,y)  

        self.draw_input(x,y)
    
        self.draw_cross_edge(x,y)    
    
        self.draw_cross(x,y)
    
        self.draw_end(x,y)  


# ###  6) Defining the "poly" function wich take :
# * #### rad : radius of the circle 
# * #### s : number of sides of the geometry
# 

# In[ ]:


def poly(radius, sides,a,s): # this function return an array on point for one geometry (one polygon)
        
    x = []
    y = []
    i = 1
    
    
    if s == 4 : # i2 is weird but here are some values of it ... (in fact too much values are useless because we only do octagon )
        i2 = 45+90
    elif s == 8:
        i2 = 22.5
    
    while i < sides + 1 :

        x.append(radius*cos(radians(a+i2)))
        y.append(radius*sin(radians(a+i2)))
                 
        i += 1
        i2 += a
    return x,y
      


# ###  7) Generating the finale inductor :

# In[ ]:


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


# ###  8) Prepare the export of the finale inductor to a .gdc file :

# In[ ]:


def save(a): # when the button trigger this function, it give a positionnal argument so we need to recive it in order to make it work ...
    writer = gdspy.write_gds(save_txtbox.value,cells=[cell], unit=1.0e-6,precision=1.0e-9)


# ### 9) Wrap everything into a widget and display it

# In[ ]:


save_btn.on_click(save) 
finale_widget = widgets.Accordion(children=[widgets.VBox([widgets.HBox([iorealtime,ui]),save_box])])
display(finale_widget)

