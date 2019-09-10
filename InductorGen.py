#!/usr/bin/env python3
# -.- coding: utf-8 -.-
#  InductorGen


from math import cos,tan,radians,sqrt
from module.utils import *
from module.polygon import poly

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
# -m or --margin -> mv : Margin between the vias area and the M5 crossings
# ------------------------------ #
#  Optional
# -o or --output -> Filename of the gds out (keep empty if you only want preview)
# --disablepreview -> Disable GDS output preview
# --disablesave -> Disable GDS file saving (seems useless cause of the behavior or -o but is usefull for the GUI)

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--length", type=float,help="Length of the inscribed square ", required=True)
parser.add_argument("-s", "--sides", type=int, choices=[4,8],help="Number of sides of the geometry (only 4 or 8)", required=True)
parser.add_argument("-t", "--turns", type=int,help="Number of turns of the inductor", required=True)
parser.add_argument("-lt", "--lenturn", type=float,help="Length of a turn", required=True)
parser.add_argument("-p", "--space", type=float,help="Space between the turns", required=True)
parser.add_argument("-r", "--tap", type=float,help="Tapering coeficiant", required=True)
parser.add_argument("-v", "--overlap", type=float,help="Overlap of the crossings", required=True)
parser.add_argument("-m", "--margin", type=float,help=" Margin between the vias and the M5 crossings", required=True)


parser.add_argument("-g", "--grid", type=float,help="Eneble snap to grid with given lenth (1*10-6 m by default)", required=True)
parser.add_argument("-dg", "--drawgrid",help="Draw the grid (with lenth given in -g wich is required) IN THE GDS", action="store_true")


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
o = args.overlap
mv = args.margin


grid = args.grid

save = True

filename = args.output
if filename:
    if not filename[-4:] == ".gds": # if the correct extention isn't already set, set it
        filename += ".gds"
else:
    save = False
if args.disablesave:
    save = False

cell = gdspy.Cell('Inductor', True)


def write(filename):
    writer = gdspy.write_gds(filename,cells=[cell], unit=1.0e-6,precision=1.0e-9)

# Setup the reset_gdspy function
# This function prevent gdspy from superimposing the new impetance when we genrerate more than one after running the program
def reset_gdspy():
    cell.remove_polygons(lambda pts, layer, datatype:
                     layer == 0)
    cell.remove_polygons(lambda pts, layer, datatype:
                     layer == 1)
    cell.remove_polygons(lambda pts, layer, datatype:
                     layer == 2)
# Setup the gdwrite function
# This function is just to make thing faster
def gdwrite(a,l):
    cell.add(gdspy.Polygon(a,layer=l))

# Defining the induct class wich take :
# a : angle
# rad : radius of the circle
# t : number of turns
# p : space between the turns
lstx = [] # lstx and lsty will be a temporary variable for each plot or fill of matplotlib and gdspy,   
lsty = []#   we use it to make the gdspy's implementation more simple
class induct:
    
    def __init__(self, angle, radius, turns, length, sides, d, p, r, o, mv,grid):
        # we initialyse all the parameters
        self.grid = grid
        self.a = angle
        self.rad = radius
        self.l = length
        
        self.t = turns
        self.l = length
        self.s = sides
        
        self.d = d
        self.p = p
        self.r = r
       
        self.o = o
        self.mv = mv
        
        

    def generate(self): # this function draw the natives poligon
        i = 1
        
        x = []
        y = []    
        tx = []
        ty = []
    
        rr = 0
        lenn = self.l+1
        while i < self.t + 1:
            
            tx,ty = poly(self.rad - rr,self.a * 360,self.a,self.s,self.grid)
            rr += lenn
            lenn = lenn*self.r
            x.append(tx)
            y.append(ty)
            
            tx,ty = poly(self.rad - rr,self.a * 360,self.a,self.s,self.grid)
            x.append(tx)
            y.append(ty)
            rr += self.p
        
            i += 1
        y2 = []
        rr = 0
        lenn = self.l+1
        i = 1
        while i < self.t + 2:
            
            tx,ty = poly(self.rad - rr,self.a * 360,self.a,self.s,self.grid)
            rr += lenn
            lenn = lenn*self.r
            y2.append(ty)
            
            tx,ty = poly(self.rad - rr,self.a * 360,self.a,self.s,self.grid)
            y2.append(ty)
            rr += self.p
        
            i += 1
        return x,y,y2
    
    def draw_poly(self,x,y): # this function is call "draw_poly" but in fact it just delete the useless lines in the poligon
        i = 0
        while i < len(x):#   
            lstx = x[i][1:self.s//2+1]
            lsty = y[i][1:self.s//2+1]
            
            
            lstx = x[i][self.s//2+1:self.s + 1]
            lsty = y[i][self.s//2+1:self.s + 1]
            
            i += 1
        i = 0
        while i < len(x):#   
            lstx = x[i][1:self.s//2+1] + [x[i+1][1]] + x[i+1][1:self.s//2+1][::-1] + [x[i+1][1]] 
            lsty = y[i][1:self.s//2+1] + [-y[i][1]] + y[i+1][1:self.s//2+1][::-1] + [y[i][1]] 
            gdwrite(ar_to_tu(lstx,lsty,self.grid),2)
            
            
            lstx = x[i][self.s//2+1:self.s + 1] + [-x[i+1][1]]  + x[i+1][self.s//2+1:self.s + 1][::-1] + [-x[i+1][1]] 
            lsty = y[i][self.s//2+1:self.s + 1] + [y[i][1]] + y[i+1][self.s//2+1:self.s + 1][::-1] + [-y[i][1]] 
            gdwrite(ar_to_tu(lstx,lsty,self.grid),2)
            
            i += 2
    def draw_input(self,x,y): # this function just draw LINE BY LINE the input of the inductor
        lstx1,lsty1,lstx2,lsty2 = [],[],[],[]
        
        l2 = snaptogrid(self.l,self.grid)

        lstx = [ self.p+l2 , self.p+l2 ]+[ self.p , self.p ][::-1]
        lsty = [y[0][4:6][0],y[0][4:6][0]-l2]+[y[1][4:6][0],y[0][4:6][0]-l2][::-1]
        
        
        lstx1 = [-x[1][4:6][0],self.p+l2]
        lsty1 = [y[0][4:6][0],y[0][4:6][0]]
        
        
        
        lstx2 = [self.p,x[1][4:6][1]]
        lsty2 = [y[1][4:6][0],y[1][4:6][1]]
        
        
        gdwrite(fusion(ar_to_tu(lstx,lsty,self.grid) , ar_to_tu(lstx1[::-1],lsty1[::-1],self.grid) + ar_to_tu(lstx2[::-1],lsty2[::-1],self.grid)),2)
        
        
        lstx = [-self.p-l2,-self.p-l2]+[-self.p,-self.p][::-1]
        lsty = [y[0][4:6][0],y[0][4:6][0]-l2]+[y[1][4:6][0],y[0][4:6][0]-l2][::-1]
        
    
        
        lstx1 = [x[1][4:6][0],-self.p-l2]
        lsty1 = [y[0][4:6][0],y[0][4:6][0]]
        
                                                  
        lstx2 = [-self.p,x[1][4:6][0]]
        lsty2 = [y[1][4:6][0],y[1][4:6][0]]  
        
 
        gdwrite(fusion(ar_to_tu(lstx,lsty,self.grid) , ar_to_tu(lstx1[::-1],lsty1[::-1],self.grid) + ar_to_tu(lstx2[::-1],lsty2[::-1],self.grid)),2)

    def draw_cross_edge(self,x,y):# this function just calculate and draw how far the middles lines should go before the crossing
        
        ab = 0
        i = 0
        
        if self.t % 2 == 0:
            coe = 1
        else:
            coe = 2
        while i < 2*self.t - coe: # forward the top to the cross
            
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])

            lstx = [x[i][4:6][0] , x[i][4:6][0] + (xy-self.l)/2 ]
            lsty = [-y[i][4:6][0] , -y[i][4:6][0]]
            
            gdwrite(ar_to_tu(lstx,lsty,self.grid),2)
            
            
            lstx1 = [x[i][4:6][1] , x[i][4:6][1] - (xy-self.l)/2 ]
            lsty1 = [-y[i][4:6][1] , -y[i][4:6][1]]
            
            gdwrite(ar_to_tu(lstx1,lsty1,self.grid),2)
            i += 1
            if ab == 1:
                ab -= 1
            else:
                ab +=1
        i = 0
        ab = 0
        
        while i < 2*self.t -coe :
            
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])
            xy1 = L(x[i+1][4:6][0],y[i+1][4:6][0],-(x[i+1][4:6][0]),y[i+1][4:6][0])
            
            lstx = [x[i+1][4:6][0] , x[i+1][4:6][0] + (xy1-self.l)/2 ]
            lsty = [-y[i][4:6][0] , -y[i][4:6][0]]
            
            lstx1 = [x[i+1][4:6][0] , x[i+1][4:6][0] + (xy1-self.l)/2 ]
            lsty1 = [-y[i+1][4:6][0] , -y[i+1][4:6][0]]
            
            gdwrite(ar_to_tu(lstx + lstx1[::-1],lsty + lsty1[::-1],self.grid),2)
            
            lstx = [-x[i+1][4:6][0] , -x[i+1][4:6][0] - (xy1-self.l)/2 ]
            lsty = [-y[i][4:6][0] , -y[i][4:6][0]]
            
            lstx1 = [-x[i+1][4:6][0] , -x[i+1][4:6][0] - (xy1-self.l)/2 ]
            lsty1 = [-y[i+1][4:6][0] , -y[i+1][4:6][0]]
            
            gdwrite(ar_to_tu(lstx + lstx1[::-1],lsty + lsty1[::-1],self.grid),2)           
            i += 2
            if ab == 1:
                ab -= 1
            else:
                ab +=1
        i = 2
        ab = 0
        
        if self.t % 2 == 0:
            coe = 1
        else:
            coe = 0
        
        i = 2
        ab = 0

        if self.t % 2 == 0:
            coe = 2
        else:
            coe = 1
        ab = 0
        
        while i < 2*self.t - coe: 
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])
            xy1 = L(x[i+1][4:6][0],y[i+1][4:6][0],-(x[i+1][4:6][0]),y[i+1][4:6][0])
            
            lstx = [x[i+1][4:6][0] , x[i][4:6][0] + (xy-self.l)/2 ]
            lsty = [y[i][4:6][0] , y[i][4:6][0]]
            
            lstx1 = [x[i+1][4:6][0] , x[i][4:6][0] + (xy-self.l)/2 ]
            lsty1 = [y[i+1][4:6][0] , y[i+1][4:6][0]]
            
            gdwrite(ar_to_tu(lstx  + lstx1[::-1] ,lsty + lsty1[::-1],self.grid),2)
            
            
            
            lstx = [-x[i+1][4:6][0] , -x[i][4:6][0] - (xy-self.l)/2 ]
            lsty = [y[i][4:6][0] , y[i][4:6][0]]
            
            lstx1 = [-x[i+1][4:6][0] , -x[i][4:6][0] - (xy-self.l)/2 ]
            lsty1 = [y[i+1][4:6][0] , y[i+1][4:6][0]]
            
            gdwrite(ar_to_tu(lstx  + lstx1[::-1] ,lsty + lsty1[::-1],self.grid),2)
            
            if ab == 1:
                ab -= 1
            else:
                ab +=1

            i += 2
    
    def draw_cross(self,x,y,y2): # this HUGE function draw the cross (both colored and uncolored)
        i = 2
  
        comp = self.t*2
        
        while i < comp  : # draw top cross on M5 on gdspy (blue)
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])
            xy1 = L(x[i+1][4:6][0],y[i+1][4:6][0],-(x[i+1][4:6][0]),y[i+1][4:6][0])
            xxxx1 = (-x[i][4:6][0] - (xy-self.l)/2) + ((y[i-2][4:6][0]) + (-(y[i][4:6][0])) ) 
            


            lstx = [ x[i][4:6][0] + (xy-self.l)/2 , -xxxx1]
            lsty = [-(y[i-2][4:6][0]) , -(y[i][4:6][0]) ]

         

            xxxx2 = x[i+1][4:6][0] + (xy1-self.l)/2 + (-(y[i-1][4:6][0]) -  -(y[i+1][4:6][0]))

            lstx1 = [ x[i+1][4:6][0] + (xy1-self.l)/2 , xxxx2 ]
            lsty1 = [-(y[i-1][4:6][0])  , -(y[i+1][4:6][0])]
            
            lstyy = [-(y[i][4:6][0])]
            if (-xxxx1 > -x[i][4:6][0] - (xy-self.l)/2):
                lstxx = [-xxxx1]
                ptx =  -xxxx1
            else:
                
                ptx =  x[i][4:6][0] + (xy-self.l)/2 + self.l + (self.l-(self.l*self.r))
                lstxx = [ptx]
            pty = -(y[i+1][4:6][0])
            
            gdwrite(ar_to_tu(lstx+lstxx+[ptx]+lstx1[::-1],lsty+lstyy+[pty]+lsty1[::-1],self.grid),2)    

            i += 4
          
        i = 2
        
        while i < comp  : # draw top crossings on M6 and vias (red) 
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])
            xy1 = L(x[i+1][4:6][0],y[i+1][4:6][0],-(x[i+1][4:6][0]),y[i+1][4:6][0])

            lstx2 = [ -x[i][4:6][0] - (xy-self.l)/2 + self.o, -x[i+1][4:6][0] - (xy1-self.l)/2  + self.o]
            lsty2 = [-(y[i-2][4:6][0]) , -(y[i-1][4:6][0])]                                         

            lstx3 = [ x[i][4:6][0] + (xy-self.l)/2 - self.o, x[i+1][4:6][0] + (xy1-self.l)/2  - self.o] #####
            lsty3 = [-(y[i+1][4:6][0]) , -(y[i][4:6][0])]
                
            xxxx = (-x[i][4:6][0] - (xy-self.l)/2) + ((y[i-2][4:6][0]) + (-(y[i][4:6][0])) ) 
            lstx = [ -x[i][4:6][0] - (xy-self.l)/2 , xxxx] # IMPORTANT
            lsty = [-(y[i-2][4:6][0]) , -(y[i][4:6][0])] 


            xxxx = (-x[i][4:6][0] - (xy-self.l)/2) + ((y[i-1][4:6][0]) + (-(y[i+1][4:6][0])) ) 
            lstx1 = [ -x[i+1][4:6][0] - (xy1-self.l)/2 , xxxx] # IMPORTANT
            lsty1 = [-(y[i-1][4:6][0]) , -(y[i+1][4:6][0])]
            
            gdwrite(ar_to_tu(lstx2[::-1]+lstx+lstx3[::-1]+lstx1[::-1],lsty2[::-1]+lsty+lsty3[::-1]+lsty1[::-1],self.grid),0) # draw corssings

            lstx = [ -x[i][4:6][0] - (xy-self.l)/2 , x[i][4:6][0] + (xy-self.l)/2]
            lstx1 = [ -x[i+1][4:6][0] - (xy1-self.l)/2 ,-x[i][4:6][0] - (xy-self.l)/2]       
                 #draw vias
            gdwrite(ar_to_tu([lstx2[1]-self.mv,lstx2[0]-self.mv] + [lstx[0]+self.mv]*2 ,[lsty2[1] + self.mv,lsty2[0] - self.mv] + [lsty[0] - self.mv] + [lsty2[1] + self.mv],self.grid),1)
            gdwrite(ar_to_tu([lstx3[0]+self.mv,lstx3[1]+self.mv] + [lstx[1]-self.mv]*2 ,[lsty3[0]+self.mv, lsty3[1]-self.mv] + [lsty[1] - self.mv] + [lsty3[0] + self.mv],self.grid),1)

            i += 4  

        i = 4

        while i < comp  : # draw bottom cross on M5
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])
            xy1 = L(x[i+1][4:6][0],y[i+1][4:6][0],-(x[i+1][4:6][0]),y[i+1][4:6][0])
            xxxx1 = (-x[i][4:6][0] - (xy-self.l)/2) + ((y[i-2][4:6][0]) + (-(y[i][4:6][0])) ) 
            


            lstx = [ x[i][4:6][0] + (xy-self.l)/2 , -xxxx1]
            lsty = [(y[i-2][4:6][0]) , (y[i][4:6][0]) ]

            

            xxxx2 = (-x[i][4:6][0] - (xy-self.l)/2) + (-(y2[i+2][4:6][0]) - (-(y[i][4:6][0])) )  
            lstx1 = [ x[i+1][4:6][0] + (xy1-self.l)/2 , -xxxx2]
            lsty1 = [(y[i-1][4:6][0]) , (y[i+1][4:6][0])]
            
            lstyy = [(y[i][4:6][0])]
            if xxxx2 > -(-x[i][4:6][0] - (xy-self.l)/2):

                vari = (-x[i][4:6][0] - (xy-self.l)/2)
                lstxx = [vari]
                ptx =  vari
            else:
                
                ptx =  x[i][4:6][0] + (xy-self.l)/2 + self.l + (self.l-(self.l*self.r))
                lstxx = [ptx]
            pty = (y[i+1][4:6][0])


            gdwrite(ar_to_tu(lstx+lstxx+[ptx]+lstx1[::-1],lsty+lstyy+[pty]+lsty1[::-1],self.grid),2)                       

            i += 4
  
        i = 4
        
        while i < comp  : # draw bottom cross on M6
            xy = L(x[i][4:6][0],y[i][4:6][0],-(x[i][4:6][0]),y[i][4:6][0])
            xy1 = L(x[i+1][4:6][0],y[i+1][4:6][0],-(x[i+1][4:6][0]),y[i+1][4:6][0])

            lstx2 = [ -x[i][4:6][0] - (xy-self.l)/2 + self.o, -x[i+1][4:6][0] - (xy1-self.l)/2  + self.o] ##### X = -x[i][4:6][0] - (xy-self.l)/2
            lsty2 = [(y[i-2][4:6][0]) , (y[i-1][4:6][0])]                                             # Y = -(y[i-2][4:6][0])

            lstx3 = [ x[i][4:6][0] + (xy-self.l)/2 - self.o, x[i+1][4:6][0] + (xy1-self.l)/2  - self.o] #####
            lsty3 = [(y[i+1][4:6][0]) , (y[i][4:6][0])]
                
            xxxx = (-x[i][4:6][0] - (xy-self.l)/2) + ((y[i-2][4:6][0]) + (-(y[i][4:6][0])) ) 
            lstx = [ -x[i][4:6][0] - (xy-self.l)/2 , xxxx] # IMPORTANT
            lsty = [(y[i-2][4:6][0]) ,(y[i][4:6][0])] 


            xxxx = (-x[i][4:6][0] - (xy-self.l)/2) + ((y[i-1][4:6][0]) + (-(y[i+1][4:6][0])) ) 
            lstx1 = [ -x[i+1][4:6][0] - (xy1-self.l)/2 , xxxx] # IMPORTANT
            lsty1 = [(y[i-1][4:6][0]) , (y[i+1][4:6][0])]
            
            
            gdwrite(ar_to_tu(lstx2[::-1]+lstx+lstx3[::-1]+lstx1[::-1],lsty2[::-1]+lsty+lsty3[::-1]+lsty1[::-1],self.grid),0)                        
        
            lstx = [ -x[i][4:6][0] - (xy-self.l)/2 , x[i][4:6][0] + (xy-self.l)/2]
            lstx1 = [ -x[i+1][4:6][0] - (xy1-self.l)/2 ,-x[i][4:6][0] - (xy-self.l)/2] 

            #draw vias
            gdwrite(ar_to_tu([lstx2[1]-self.mv,lstx2[0]-self.mv] + [lstx[0]+self.mv]*2 ,[lsty2[1] - self.mv,lsty2[0] + self.mv] + [lsty[0] + self.mv] + [lsty2[1] - self.mv],self.grid),1)
            gdwrite(ar_to_tu([lstx3[0]+self.mv,lstx3[1]+self.mv] + [lstx[1]-self.mv]*2 ,[lsty3[0] - self.mv, lsty3[1] + self.mv] + [lsty[1] + self.mv] + [lsty3[0] - self.mv],self.grid),1)

            i += 4   
        

    def draw_grid(self):
        px = round(self.d+1)

        g = 0
        while g < px+2:
            gdwrite(ar_to_tu([g]*2,[px,-px],self.grid),3)
            g += self.grid
        g = 0
        while g > -px-2:
            gdwrite(ar_to_tu([g]*2,[px,-px],self.grid),3)
            g -= self.grid
        g = 0
        while g < px+2:
            gdwrite(ar_to_tu([px,-px],[g]*2,self.grid),3)
            g += self.grid
        g = 0
        while g > -px-2:
            gdwrite(ar_to_tu([px,-px],[g]*2,self.grid),3)
            g -= self.grid
    def draw_end(self,x,y): # this fumction draw the "end" by connecting the 2 last cable

        lstx1,lsty1,lstx2,lsty2 = [],[],[],[]
        if self.t % 2 == 0: # connect the last turn in top or bottom depending on the nb of turns ( even or odd number of turns)
            xy = L(x[(self.s + (2*self.t- self.s)-1)][4:6][0],y[(self.s + (2*self.t- self.s)-1)][4:6][1],-(x[(self.s + (2*self.t- self.s)-1)][4:6][0]),y[(self.s + (2*self.t- self.s)-1)][4:6][1])
            
            lstx = [-xy/2 , xy/2 ]
            lsty = [y[(self.s + (2*self.t- self.s))-1][4:6][1] , y[(self.s + (2*self.t- self.s)-1)][4:6][1]]
            
            lstx1 = [-xy/2 , xy/2 ]
            lsty1 = [y[(self.s + (2*self.t- self.s))-2][4:6][1] , y[(self.s + (2*self.t- self.s)-2)][4:6][1]]
            

            gdwrite(ar_to_tu(lstx + lstx1[::-1] , lsty + lsty1[::-1] ,self.grid),2)
        else:
            xy = L(x[(self.s + (2*self.t- self.s)-1)][4:6][0],y[(self.s + (2*self.t- self.s)-1)][4:6][0],-(x[(self.s + (2*self.t- self.s)-1)][4:6][0]),y[(self.s + (2*self.t- self.s)-1)][4:6][0])
            
            lstx = [-xy/2 , xy/2 ]
            lsty = [-y[(self.s + (2*self.t- self.s))-1][4:6][0] , -y[(self.s + (2*self.t- self.s)-1)][4:6][0]]
                     
            lstx1 = [-xy/2 , xy/2 ]
            lsty1 = [-y[(self.s + (2*self.t- self.s))-2][4:6][0] , -y[(self.s + (2*self.t- self.s)-2)][4:6][0]]
            
        
            gdwrite(ar_to_tu(lstx + lstx1[::-1] , lsty + lsty1[::-1] ,self.grid),2)
            

    def draw(self,x,y,y2): # this function just draw everything by calling all the overs ...

        self.draw_poly(x,y)  

        self.draw_input(x,y)
    
        self.draw_cross_edge(x,y)
    
        self.draw_cross(x,y,y2)
    
        self.draw_end(x,y)  



# Generating the finale inductor :

reset_gdspy() # Prevent gdspy from superposing inductors
a = give_a(s)
rad = give_rad(d,a) 
    
inductor = induct(a,rad,t,l,s,d,p,r,o,mv,grid)
        
x,y,y2 = inductor.generate()
inductor.draw(x,y,y2) 
 
if args.drawgrid:
    inductor.draw_grid() # if dg than we draw the grid before writing so it apear in the GDS file
if save:
    write(filename)


inductor.draw_grid()

if not args.disablepreview:  
    gdspy.LayoutViewer(library=None, cells=[cell])