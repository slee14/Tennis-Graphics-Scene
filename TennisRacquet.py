#Sojung Lee
#Homework 6 - Creative Scene
'''Notes:some of the content is creatively based off of JShawGuitar.
         Wasn't able to do the cylindrical method that we discussed.'''          

import sys
import math
from TW import *

#Variables
scale = 1.0
cRAD = 3.8*scale  #cross radius
mRAD = 5*scale #main radius
beamWidth1 = 0.5*scale    #z width
beamWidth2 = 0.3*scale  #x width

''' -------------------- Ellipses --------------------
    The following functions finds the corresponding x or y function, given a y or x coordinate. 
    Given a y coordinate, findX will calculate the point on the ellipse that is x, and vice versa
    for findY '''
def findX (y):
    a = 4 * (y**2)
    b = (mRAD*2)**2
    c = (1 - (a/b))
    d = math.sqrt(c)
    e = (cRAD)*d
    return e

def findY (x):
    a = 4*(x**2)
    b = (cRAD*2)**2
    c = (1 - (a/b))
    d = math.sqrt(c)
    e = (mRAD)*d
    return e

''' -------------------- THE RACQUET HEAD & SIDES -------------------- '''
def makeOuterHead(zcoord):
    ''' makeOuterHead takes in a zcoord parameter that sets the z coordinate. 
        The z coordinate moves TOWARD the viewer. 
        makeOuter creates an array, arbitrarily named "tennis" here, and 
        it specifies the coordinates for the "outside" frame of a tennis racquet. 
        The origin is at the center of this racquet head. 
    '''
    tennis = [
    [0,0,zcoord], #origin at the middle of the face                 #0
    [0,mRAD,zcoord], #start at top of the racquet face              #1
    [-(1.0/19.0)*cRAD,findY((1.0/19.0)*cRAD),zcoord],               #2
    [-(2.0/19.0)*cRAD,findY((2.0/19.0)*cRAD),zcoord],               #3
    [-(3.0/19.0)*cRAD,findY((3.0/19.0)*cRAD),zcoord],               #4
    [-(4.0/19.0)*cRAD,findY((4.0/19.0)*cRAD),zcoord],               #5
    [-(5.0/19.0)*cRAD,findY((5.0/19.0)*cRAD),zcoord],               #6
    [-(6.0/19.0)*cRAD,findY((6.0/19.0)*cRAD),zcoord],               #7
    [-(7.0/19.0)*cRAD,findY((7.0/19.0)*cRAD),zcoord],               #8
    [-(8.0/19.0)*cRAD,findY((8.0/19.0)*cRAD),zcoord],               #9
    [-(9.0/19.0)*cRAD,findY((9.0/19.0)*cRAD),zcoord],               #10
    [-(10.0/19.0)*cRAD,findY((10.0/19.0)*cRAD),zcoord],             #11
    [-(11.0/19.0)*cRAD,findY((11.0/19.0)*cRAD),zcoord],             #12
    [-(12.0/19.0)*cRAD,findY((12.0/19.0)*cRAD),zcoord],             #13
    [-(13.0/19.0)*cRAD,findY((13.0/19.0)*cRAD),zcoord],             #14   
    [-(14.0/19.0)*cRAD,findY((14.0/19.0)*cRAD),zcoord],             #15 
    [-(15.0/19.0)*cRAD,findY((15.0/19.0)*cRAD),zcoord],             #16   
    [-(16.0/19.0)*cRAD,findY((16.0/19.0)*cRAD),zcoord],             #17  
    [-(17.0/19.0)*cRAD,findY((17.0/19.0)*cRAD),zcoord],             #18
    [-(18.0/19.0)*cRAD,findY((18.0/19.0)*cRAD),zcoord],             #19
    [-(18.3/19.0)*cRAD,findY((18.3/19.0)*cRAD),zcoord],             #20
    [-(18.7/19.0)*cRAD,findY((18.7/19.0)*cRAD),zcoord],             #21  
    [-(19.0/19.0)*cRAD,0,zcoord],                                   #22        
    
    
    #end of top left quarter, beginning bottom left quarter
    #since raquet is symmetrical, x points come back toward 1 at same interval
    #y coordinates go into the negatives, since the origin is at the 
    # middle of the face              
    [-(18.7/19.0)*cRAD,-findY((18.7/19.0)*cRAD),zcoord],            #23
    [-(18.3/19.0)*cRAD,-findY((18.3/19.0)*cRAD),zcoord],            #24
    [-(18.0/19.0)*cRAD,-findY((18.0/19.0)*cRAD),zcoord],            #25
    [-(17.0/19.0)*cRAD,-findY((17.0/19.0)*cRAD),zcoord],            #26
    [-(16.0/19.0)*cRAD,-findY((16.0/19.0)*cRAD),zcoord],            #27
    [-(15.0/19.0)*cRAD,-findY((15.0/19.0)*cRAD),zcoord],            #28
    [-(14.0/19.0)*cRAD,-findY((14.0/19.0)*cRAD),zcoord],            #29
    [-(13.0/19.0)*cRAD,-findY((13.0/19.0)*cRAD),zcoord],            #30
    [-(12.0/19.0)*cRAD,-findY((12.0/19.0)*cRAD),zcoord],            #31  NECK JOIN
    [-(11.0/19.0)*cRAD,-findY((11.0/19.0)*cRAD),zcoord],            #32
    [-(10.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD),zcoord],            #33
    [-(9.0/19.0)*cRAD,-findY((9.0/19.0)*cRAD),zcoord],              #34
    [-(8.0/19.0)*cRAD,-findY((8.0/19.0)*cRAD),zcoord],              #35
    [-(7.0/19.0)*cRAD,-findY((7.0/19.0)*cRAD),zcoord],              #36
    [-(6.0/19.0)*cRAD,-findY((6.0/19.0)*cRAD),zcoord],              #37
    [-(5.0/19.0)*cRAD,-findY((5.0/19.0)*cRAD),zcoord],              #38
    [-(4.0/19.0)*cRAD,-findY((4.0/19.0)*cRAD),zcoord],              #39
    [-(3.0/19.0)*cRAD,-findY((3.0/19.0)*cRAD),zcoord],              #40
    [-(2.0/19.0)*cRAD,-findY((2.0/19.0)*cRAD),zcoord],              #41
    [-(1.0/19.0)*cRAD,-findY((1.0/19.0)*cRAD),zcoord],              #42       
    [0,-mRAD,zcoord],                                               #43

    #end of bottom left quarter, beginning bottom right quarter
    #bottom right quarter should be exactly the same as bottom left
    #quarter, except for the x values should be opposite sign.  
    [(1.0/19.0)*cRAD ,-findY((1.0/19.0)*cRAD),zcoord],                 #44
    [(2.0/19.0)*cRAD ,-findY((2.0/19.0)*cRAD),zcoord],                 #45
    [(3.0/19.0)*cRAD ,-findY((3.0/19.0)*cRAD),zcoord],                 #46
    [(4.0/19.0)*cRAD ,-findY((4.0/19.0)*cRAD),zcoord],                 #47
    [(5.0/19.0)*cRAD ,-findY((5.0/19.0)*cRAD),zcoord],                 #48
    [(6.0/19.0)*cRAD ,-findY((6.0/19.0)*cRAD),zcoord],                 #49
    [(7.0/19.0)*cRAD ,-findY((7.0/19.0)*cRAD),zcoord],                 #50
    [(8.0/19.0)*cRAD ,-findY((8.0/19.0)*cRAD),zcoord],                 #51
    [(9.0/19.0)*cRAD ,-findY((9.0/19.0)*cRAD),zcoord],                 #52
    [(10.0/19.0)*cRAD ,-findY((10.0/19.0)*cRAD),zcoord],                #53
    [(11.0/19.0)*cRAD ,-findY((11.0/19.0)*cRAD),zcoord],                #54
    [(12.0/19.0)*cRAD ,-findY((12.0/19.0)*cRAD),zcoord],                #55 NECK JOIN
    [(13.0/19.0)*cRAD ,-findY((13.0/19.0)*cRAD),zcoord],                #56  
    [(14.0/19.0)*cRAD ,-findY((14.0/19.0)*cRAD),zcoord],                #57
    [(15.0/19.0)*cRAD ,-findY((15.0/19.0)*cRAD),zcoord],                #58 
    [(16.0/19.0)*cRAD ,-findY((16.0/19.0)*cRAD),zcoord],                #59
    [(17.0/19.0)*cRAD ,-findY((17.0/19.0)*cRAD),zcoord],                #60
    [(18.0/19.0)*cRAD ,-findY((18.0/19.0)*cRAD),zcoord],                #61
    [(18.3/19.0)*cRAD ,-findY((18.3/19.0)*cRAD),zcoord],                #62
    [(18.7/19.0)*cRAD ,-findY((18.7/19.0)*cRAD),zcoord],                #63  
    [(19.0/19.0)*cRAD ,0,zcoord],                                       #64    
                            
    #end of bottom right quarter, beginning top right quarter
    #top right quarter should be same as top left quarter,
    #except for changes in X sign 
    [(18.7/19.0)*cRAD ,findY((18.7/19.0)*cRAD),zcoord],                 #65
    [(18.3/19.0)*cRAD ,findY((18.3/19.0)*cRAD),zcoord],                 #66
    [(18.0/19.0)*cRAD ,findY((18.0/19.0)*cRAD),zcoord],                 #67
    [(17.0/19.0)*cRAD ,findY((17.0/19.0)*cRAD),zcoord],                 #68
    [(16.0/19.0)*cRAD ,findY((16.0/19.0)*cRAD),zcoord],                 #69
    [(15.0/19.0)*cRAD ,findY((15.0/19.0)*cRAD),zcoord],                 #70
    [(14.0/19.0)*cRAD ,findY((14.0/19.0)*cRAD),zcoord],                 #71
    [(13.0/19.0)*cRAD ,findY((13.0/19.0)*cRAD),zcoord],                 #72
    [(12.0/19.0)*cRAD ,findY((12.0/19.0)*cRAD),zcoord],                 #73
    [(11.0/19.0)*cRAD ,findY((11.0/19.0)*cRAD),zcoord],                 #74
    [(10.0/19.0)*cRAD ,findY((10.0/19.0)*cRAD),zcoord],                 #75
    [(9.0/19.0)*cRAD ,findY((9.0/19.0)*cRAD),zcoord],                  #76
    [(8.0/19.0)*cRAD ,findY((8.0/19.0)*cRAD),zcoord],                  #77
    [(7.0/19.0)*cRAD ,findY((7.0/19.0)*cRAD),zcoord],                  #78
    [(6.0/19.0)*cRAD ,findY((6.0/19.0)*cRAD),zcoord],                  #79
    [(5.0/19.0)*cRAD ,findY((5.0/19.0)*cRAD),zcoord],                  #80
    [(4.0/19.0)*cRAD ,findY((4.0/19.0)*cRAD),zcoord],                  #81
    [(3.0/19.0)*cRAD ,findY((3.0/19.0)*cRAD),zcoord],                  #82
    [(2.0/19.0)*cRAD ,findY((2.0/19.0)*cRAD),zcoord],                  #83
    [(1.0/19.0)*cRAD,findY((1.0/19.0)*cRAD),zcoord],                  #84
    [0,mRAD,zcoord],                                                   #85
    [0,0,zcoord]                                                       #86
    ]  
    return tennis

def makeInnerHead(zcoord):
    ''' makeInnerHead takes in a zcoord parameter that sets the z coordinate. 
        The z coordinate moves TOWARD the viewer. 
        makeOuter creates an array, arbitrarily named "tennis" here, and 
        it specifies the coordinates for the "inside" frame of a tennis racquet. 
        The origin is at the center of this racquet head. 
    '''
    tennis = [
    [0,0,zcoord], #origin at the middle of the face                 #0
    [0,mRAD,zcoord], #start at top of the racquet face              #1
    [-(1.0/19.0)*cRAD+beamWidth2,findY((1.0/19.0)*cRAD)-beamWidth2,zcoord],               #2
    [-(2.0/19.0)*cRAD+beamWidth2,findY((2.0/19.0)*cRAD)-beamWidth2,zcoord],               #3
    [-(3.0/19.0)*cRAD+beamWidth2,findY((3.0/19.0)*cRAD)-beamWidth2,zcoord],               #4
    [-(4.0/19.0)*cRAD+beamWidth2,findY((4.0/19.0)*cRAD)-beamWidth2,zcoord],               #5
    [-(5.0/19.0)*cRAD+beamWidth2,findY((5.0/19.0)*cRAD)-beamWidth2,zcoord],               #6
    [-(6.0/19.0)*cRAD+beamWidth2,findY((6.0/19.0)*cRAD)-beamWidth2,zcoord],               #7
    [-(7.0/19.0)*cRAD+beamWidth2,findY((7.0/19.0)*cRAD)-beamWidth2,zcoord],               #8
    [-(8.0/19.0)*cRAD+beamWidth2,findY((8.0/19.0)*cRAD)-beamWidth2,zcoord],               #9
    [-(9.0/19.0)*cRAD+beamWidth2,findY((9.0/19.0)*cRAD)-beamWidth2,zcoord],               #10
    [-(10.0/19.0)*cRAD+beamWidth2,findY((10.0/19.0)*cRAD)-beamWidth2,zcoord],             #11
    [-(11.0/19.0)*cRAD+beamWidth2,findY((11.0/19.0)*cRAD)-beamWidth2,zcoord],             #12
    [-(12.0/19.0)*cRAD+beamWidth2,findY((12.0/19.0)*cRAD)-beamWidth2,zcoord],             #13
    [-(13.0/19.0)*cRAD+beamWidth2,findY((13.0/19.0)*cRAD)-beamWidth2,zcoord],             #14   
    [-(14.0/19.0)*cRAD+beamWidth2,findY((14.0/19.0)*cRAD)-beamWidth2,zcoord],             #15 
    [-(15.0/19.0)*cRAD+beamWidth2,findY((15.0/19.0)*cRAD)-beamWidth2,zcoord],             #16   
    [-(16.0/19.0)*cRAD+beamWidth2,findY((16.0/19.0)*cRAD)-beamWidth2,zcoord],             #17  
    [-(17.0/19.0)*cRAD+beamWidth2,findY((17.0/19.0)*cRAD)-beamWidth2,zcoord],             #18
    [-(18.0/19.0)*cRAD+beamWidth2,findY((18.0/19.0)*cRAD)-beamWidth2,zcoord],             #19
    [-(18.3/19.0)*cRAD+beamWidth2,findY((18.3/19.0)*cRAD)-beamWidth2,zcoord],             #20
    [-(18.7/19.0)*cRAD+beamWidth2,findY((18.7/19.0)*cRAD)-beamWidth2,zcoord],             #21  
    [-(19.0/19.0)*cRAD+beamWidth2,0,zcoord],                                   #22        
    
    
    #end of top left quarter, beginning bottom left quarter
    #since raquet is symmetrical, x points come back toward 1 at same interval
    #y coordinates go into the negatives, since the origin is at the 
    # middle of the face              
    [-(18.7/19.0)*cRAD+beamWidth2,-findY((18.7/19.0)*cRAD)+beamWidth2,zcoord], 
    [-(18.3/19.0)*cRAD+beamWidth2,-findY((18.3/19.0)*cRAD)+beamWidth2,zcoord],            #23
    [-(18.0/19.0)*cRAD+beamWidth2,-findY((18.0/19.0)*cRAD)+beamWidth2,zcoord],            #24
    [-(17.0/19.0)*cRAD+beamWidth2,-findY((17.0/19.0)*cRAD)+beamWidth2,zcoord],            #25
    [-(16.0/19.0)*cRAD+beamWidth2,-findY((16.0/19.0)*cRAD)+beamWidth2,zcoord],            #26
    [-(15.0/19.0)*cRAD+beamWidth2,-findY((15.0/19.0)*cRAD)+beamWidth2,zcoord],            #27
    [-(14.0/19.0)*cRAD+beamWidth2,-findY((14.0/19.0)*cRAD)+beamWidth2,zcoord],            #28
    [-(13.0/19.0)*cRAD+beamWidth2,-findY((13.0/19.0)*cRAD)+beamWidth2,zcoord],            #29
    [-(12.0/19.0)*cRAD+beamWidth2,-findY((12.0/19.0)*cRAD)+beamWidth2,zcoord],            #30
    [-(11.0/19.0)*cRAD+beamWidth2,-findY((11.0/19.0)*cRAD)+beamWidth2,zcoord],            #31
    [-(10.0/19.0)*cRAD+beamWidth2,-findY((10.0/19.0)*cRAD)+beamWidth2,zcoord],            #32
    [-(9.0/19.0)*cRAD+beamWidth2,-findY((9.0/19.0)*cRAD)+beamWidth2,zcoord],              #33
    [-(8.0/19.0)*cRAD+beamWidth2,-findY((8.0/19.0)*cRAD)+beamWidth2,zcoord],              #34
    [-(7.0/19.0)*cRAD+beamWidth2,-findY((7.0/19.0)*cRAD)+beamWidth2,zcoord],              #35
    [-(6.0/19.0)*cRAD+beamWidth2,-findY((6.0/19.0)*cRAD)+beamWidth2,zcoord],              #36
    [-(5.0/19.0)*cRAD+beamWidth2,-findY((5.0/19.0)*cRAD)+beamWidth2,zcoord],              #37
    [-(4.0/19.0)*cRAD+beamWidth2,-findY((4.0/19.0)*cRAD)+beamWidth2,zcoord],              #38
    [-(3.0/19.0)*cRAD+beamWidth2,-findY((3.0/19.0)*cRAD)+beamWidth2,zcoord],              #39
    [-(2.0/19.0)*cRAD+beamWidth2,-findY((2.0/19.0)*cRAD)+beamWidth2,zcoord],              #40
    [-(1.0/19.0)*cRAD+beamWidth2,-findY((1.0/19.0)*cRAD)+beamWidth2,zcoord],              #41       
    [0,-mRAD+beamWidth2,zcoord],                                               #42

    #end of bottom left quarter, beginning bottom right quarter
    #bottom right quarter should be exactly the same as bottom left
    #quarter, except for the x values should be opposite sign.  
    [(1.0/19.0)*cRAD-beamWidth2,-findY((1.0/19.0)*cRAD)+beamWidth2,zcoord],                 #62
    [(2.0/19.0)*cRAD-beamWidth2,-findY((2.0/19.0)*cRAD)+beamWidth2,zcoord],                 #63
    [(3.0/19.0)*cRAD-beamWidth2,-findY((3.0/19.0)*cRAD)+beamWidth2,zcoord],                 #64
    [(4.0/19.0)*cRAD-beamWidth2,-findY((4.0/19.0)*cRAD)+beamWidth2,zcoord],                 #65
    [(5.0/19.0)*cRAD-beamWidth2,-findY((5.0/19.0)*cRAD)+beamWidth2,zcoord],                 #66
    [(6.0/19.0)*cRAD-beamWidth2,-findY((6.0/19.0)*cRAD)+beamWidth2,zcoord],                 #67
    [(7.0/19.0)*cRAD-beamWidth2,-findY((7.0/19.0)*cRAD)+beamWidth2,zcoord],                 #68
    [(8.0/19.0)*cRAD-beamWidth2,-findY((8.0/19.0)*cRAD)+beamWidth2,zcoord],                 #69
    [(9.0/19.0)*cRAD-beamWidth2,-findY((9.0/19.0)*cRAD)+beamWidth2,zcoord],                 #70
    [(10.0/19.0)*cRAD-beamWidth2,-findY((10.0/19.0)*cRAD)+beamWidth2,zcoord],                #71
    [(11.0/19.0)*cRAD-beamWidth2,-findY((11.0/19.0)*cRAD)+beamWidth2,zcoord],                #72
    [(12.0/19.0)*cRAD-beamWidth2,-findY((12.0/19.0)*cRAD)+beamWidth2,zcoord],                #73
    [(13.0/19.0)*cRAD-beamWidth2,-findY((13.0/19.0)*cRAD)+beamWidth2,zcoord],                #74  
    [(14.0/19.0)*cRAD-beamWidth2,-findY((14.0/19.0)*cRAD)+beamWidth2,zcoord],                #75
    [(15.0/19.0)*cRAD-beamWidth2,-findY((15.0/19.0)*cRAD)+beamWidth2,zcoord],                #76 
    [(16.0/19.0)*cRAD-beamWidth2,-findY((16.0/19.0)*cRAD)+beamWidth2,zcoord],                #77
    [(17.0/19.0)*cRAD-beamWidth2,-findY((17.0/19.0)*cRAD)+beamWidth2,zcoord],                #78
    [(18.0/19.0)*cRAD-beamWidth2,-findY((18.0/19.0)*cRAD)+beamWidth2,zcoord],      
    [(18.3/19.0)*cRAD-beamWidth2,-findY((18.3/19.0)*cRAD)+beamWidth2,zcoord], 
    [(18.7/19.0)*cRAD-beamWidth2,-findY((18.7/19.0)*cRAD)+beamWidth2,zcoord],          #80  
    [(19.0/19.0)*cRAD-beamWidth2,0,zcoord],                                #93
                            
    #end of bottom right quarter, beginning top right quarter
    #top right quarter should be same as top left quarter,
    #except for changes in X sign 
    [(18.7/19.0)*cRAD-beamWidth2 ,findY((18.7/19.0)*cRAD)-beamWidth2,zcoord],
    [(18.3/19.0)*cRAD-beamWidth2 ,findY((18.3/19.0)*cRAD)-beamWidth2,zcoord],   
    [(18.0/19.0)*cRAD-beamWidth2 ,findY((18.0/19.0)*cRAD)-beamWidth2,zcoord],              #103
    [(17.0/19.0)*cRAD-beamWidth2 ,findY((17.0/19.0)*cRAD)-beamWidth2,zcoord],                 #105
    [(16.0/19.0)*cRAD-beamWidth2 ,findY((16.0/19.0)*cRAD)-beamWidth2,zcoord],                 #106
    [(15.0/19.0)*cRAD-beamWidth2 ,findY((15.0/19.0)*cRAD)-beamWidth2,zcoord],                 #107
    [(14.0/19.0)*cRAD-beamWidth2 ,findY((14.0/19.0)*cRAD)-beamWidth2,zcoord],                 #108
    [(13.0/19.0)*cRAD-beamWidth2 ,findY((13.0/19.0)*cRAD)-beamWidth2,zcoord],                 #109
    [(12.0/19.0)*cRAD-beamWidth2 ,findY((12.0/19.0)*cRAD)-beamWidth2,zcoord],                 #110
    [(11.0/19.0)*cRAD-beamWidth2 ,findY((11.0/19.0)*cRAD)-beamWidth2,zcoord],                 #111
    [(10.0/19.0)*cRAD-beamWidth2 ,findY((10.0/19.0)*cRAD)-beamWidth2,zcoord],                 #112
    [(9.0/19.0)*cRAD-beamWidth2 ,findY((9.0/19.0)*cRAD)-beamWidth2,zcoord],                  #113
    [(8.0/19.0)*cRAD-beamWidth2 ,findY((8.0/19.0)*cRAD)-beamWidth2,zcoord],                  #114
    [(7.0/19.0)*cRAD-beamWidth2 ,findY((7.0/19.0)*cRAD)-beamWidth2,zcoord],                  #115
    [(6.0/19.0)*cRAD-beamWidth2 ,findY((6.0/19.0)*cRAD)-beamWidth2,zcoord],                  #116
    [(5.0/19.0)*cRAD-beamWidth2 ,findY((5.0/19.0)*cRAD)-beamWidth2,zcoord],                  #117
    [(4.0/19.0)*cRAD-beamWidth2 ,findY((4.0/19.0)*cRAD)-beamWidth2,zcoord],                  #118
    [(3.0/19.0)*cRAD-beamWidth2 ,findY((3.0/19.0)*cRAD)-beamWidth2,zcoord],                  #119
    [(2.0/19.0)*cRAD-beamWidth2 ,findY((2.0/19.0)*cRAD)-beamWidth2,zcoord],                  #120
    [(1.0/19.0)*cRAD-beamWidth2,findY((1.0/19.0)*cRAD)-beamWidth2,zcoord],                  #121
    [0,mRAD-beamWidth2,zcoord], 
    [0,0,zcoord]                                        #122
    ]  
    return tennis

outer_front_head = makeOuterHead(0)
outer_back_head = makeOuterHead(-beamWidth1)
inner_front_head = makeInnerHead(0)
inner_back_head = makeInnerHead(-beamWidth1)

def drawSides(a,b): 
    '''drawSides uses two parameters to connect vertices together. This is helpful for 
    connecting different polygons together, for example, the outerframe vertices connected with
    inner frame vertices'''
    #Makes the side of the frame connecting inner with outer (front side)
    glColor3ub(255,0,0)     #red
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3fv(outer_front_head[a])
    glVertex3fv(outer_front_head[b])
    glVertex3fv(inner_front_head[b])
    glVertex3fv(inner_front_head[a])
    glEnd()
    glPopMatrix()

    #Makes the side of the frame connecting inner with outer (back side)
    glColor3ub(255,0,0)     #red
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3fv(outer_back_head[a])
    glVertex3fv(outer_back_head[b])
    glVertex3fv(inner_back_head[b])
    glVertex3fv(inner_back_head[a])
    glEnd()
    glPopMatrix()
    
    #Makes the outer frame
    glColor3ub(255,0,0)     #red
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3fv(outer_front_head[a])
    glVertex3fv(outer_back_head[a])
    glVertex3fv(outer_back_head[b])
    glVertex3fv(outer_front_head[b])
    glEnd()
    glPopMatrix()
    
    #Makes the inner frame
    glColor3ub(255,0,0)     #white
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3fv(inner_front_head[a])
    glVertex3fv(inner_back_head[a])
    glVertex3fv(inner_back_head[b])
    glVertex3fv(inner_front_head[b])
    glEnd()
    glPopMatrix() 
    
def drawFrame():
    '''drawFrame calles drawSides in a for loop, to continually connect vertices until the array index 
    goes through the whole array'''
    for i in range (2,86):
        drawSides(i,i-1)

''' -------------------- THE RACKET NECK -------------------- '''
def makeOuterNeck(zcoord):
    '''makeOuterNeck returns an array of the vertices making the neck of the racquet.'''
    tennis = [
        [0,0,zcoord],
        [-(10.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD),zcoord],            
        [-(9.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-(mRAD/12.0),zcoord],           
        [-(8.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-2*(mRAD/12.0),zcoord],           
        [-(7.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-3*(mRAD/12.0),zcoord],              
        [-(6.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-4*(mRAD/12.0),zcoord],              
        [-(5.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-5*(mRAD/12.0),zcoord],              
        [-(4.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-6*(mRAD/12.0),zcoord],              
        [-(3.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-7*(mRAD/12.0),zcoord],              
        [-(2.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-(8+2*beamWidth2)*(mRAD/12.0),zcoord],

        [-(1.5/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-(8+2*beamWidth2)*(mRAD/12.0),zcoord], 
                                    
        [(2.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-(8+2*beamWidth2)*(mRAD/12.0),zcoord],                 
        [(3.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-7*(mRAD/12.0),zcoord],                 
        [(4.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-6*(mRAD/12.0),zcoord],                 
        [(5.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-5*(mRAD/12.0),zcoord],                 
        [(6.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-4*(mRAD/12.0),zcoord],                 
        [(7.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-3*(mRAD/12.0),zcoord],                 
        [(8.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-2*(mRAD/12.0),zcoord],                 
        [(9.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD)-(mRAD/12.0),zcoord],                 
        [(10.0/19.0)*cRAD,-findY((10.0/19.0)*cRAD),zcoord],
        [0,0,zcoord]] 
    return tennis

def makeInnerNeck(zcoord):
    tennis = [
        [0,0,zcoord],
        [-(10.0/19.0)*cRAD+beamWidth2,-findY((10.0/19.0)*cRAD),zcoord],            
        [-(9.0/19.0)*cRAD+beamWidth2,-findY((10.0/19.0)*cRAD)-(mRAD/12.0),zcoord],            
        [-(8.0/19.0)*cRAD+beamWidth2,-findY((10.0/19.0)*cRAD)-2*(mRAD/12.0),zcoord],            
        [-(7.0/19.0)*cRAD+beamWidth2,-findY((10.0/19.0)*cRAD)-3*(mRAD/12.0),zcoord],              
        [-(6.0/19.0)*cRAD+beamWidth2,-findY((10.0/19.0)*cRAD)-4*(mRAD/12.0),zcoord],             
        [-(5.0/19.0)*cRAD+beamWidth2,-findY((10.0/19.0)*cRAD)-5*(mRAD/12.0),zcoord],              
        [-(4.0/19.0)*cRAD+beamWidth2,-findY((10.0/19.0)*cRAD)-6*(mRAD/12.0),zcoord],              
        [-(3.0/19.0)*cRAD+beamWidth2,-findY((10.0/19.0)*cRAD)-7*(mRAD/12.0),zcoord],              
        [-(2.0/19.0)*cRAD+beamWidth2,-findY((10.0/19.0)*cRAD)-8*(mRAD/12.0),zcoord], 
                     
        [-(1.5/19.0)*cRAD+beamWidth2,-findY((10.0/19.0)*cRAD)-8*(mRAD/12.0),zcoord], 
                       
        [(2.0/19.0)*cRAD-beamWidth2,-findY((10.0/19.0)*cRAD)-8*(mRAD/12.0),zcoord],                 
        [(3.0/19.0)*cRAD-beamWidth2,-findY((10.0/19.0)*cRAD)-7*(mRAD/12.0),zcoord],                 
        [(4.0/19.0)*cRAD-beamWidth2,-findY((10.0/19.0)*cRAD)-6*(mRAD/12.0),zcoord],                 
        [(5.0/19.0)*cRAD-beamWidth2,-findY((10.0/19.0)*cRAD)-5*(mRAD/12.0),zcoord],                 
        [(6.0/19.0)*cRAD-beamWidth2,-findY((10.0/19.0)*cRAD)-4*(mRAD/12.0),zcoord],                 
        [(7.0/19.0)*cRAD-beamWidth2,-findY((10.0/19.0)*cRAD)-3*(mRAD/12.0),zcoord],                 
        [(8.0/19.0)*cRAD-beamWidth2,-findY((10.0/19.0)*cRAD)-2*(mRAD/12.0),zcoord],                 
        [(9.0/19.0)*cRAD-beamWidth2,-findY((10.0/19.0)*cRAD)-(mRAD/12.0),zcoord],  
        [(10.0/19.0)*cRAD-beamWidth2,-findY((10.0/19.0)*cRAD),zcoord],              
        [0,0,zcoord]]
    return tennis 

outer_front_neck = makeOuterNeck(0.0)
outer_back_neck = makeOuterNeck(-beamWidth1)
inner_front_neck = makeInnerNeck(0.0)
inner_back_neck = makeInnerNeck(-beamWidth1)

def drawSidesNeck(a,b):
    '''Same as drawSides, but makes the neck'''

    glColor3ub(255,0,0)     #red
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3fv(outer_front_neck[a])
    glVertex3fv(outer_front_neck[b])
    glVertex3fv(outer_back_neck[b])
    glVertex3fv(outer_back_neck[a])
    glEnd()
    glPopMatrix()

    glColor3ub(255,0,0)     #white
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3fv(inner_front_neck[a])
    glVertex3fv(inner_front_neck[b])
    glVertex3fv(inner_back_neck[b])
    glVertex3fv(inner_back_neck[a])
    glEnd()
    glPopMatrix()

    glColor3ub(255,0,0)     #red
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3fv(outer_front_neck[a])
    glVertex3fv(outer_front_neck[b])
    glVertex3fv(inner_front_neck[b])
    glVertex3fv(inner_front_neck[a])
    glEnd()
    glPopMatrix()

    #Makes the side of the frame connecting inner with outer (back side)
    glColor3ub(255,0,0)     #red
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3fv(outer_back_neck[a])
    glVertex3fv(outer_back_neck[b])
    glVertex3fv(inner_back_neck[b])
    glVertex3fv(inner_back_neck[a])
    glEnd()
    glPopMatrix()

def drawNeck():
    for i in range (2,20):
        drawSidesNeck(i,i-1)

''' -------------------- RACQUET STRINGS -------------------- '''
def pointStrings(zcoord):
    '''pointStrings returns the array of vertices making the strings. Main strings
    go up and down, while crosses go from side to side.'''
    tennis = [
    #''' ---------- MAINS (UP AND DOWN) ------------'''
    #left side strings
    [-(1.0/19.0)*cRAD,findY((1.0/19.0)*cRAD)-beamWidth2,zcoord], 
    [-(1.0/19.0)*cRAD,-findY((1.0/19.0)*cRAD)+beamWidth2,zcoord], 
                 
    [-(3.0/19.0)*cRAD,findY((3.0/19.0)*cRAD)-beamWidth2,zcoord],
    [-(3.0/19.0)*cRAD,-findY((3.0/19.0)*cRAD)+beamWidth2,zcoord],
                   
    [-(5.0/19.0)*cRAD,findY((5.0/19.0)*cRAD)-beamWidth2,zcoord],   
    [-(5.0/19.0)*cRAD,-findY((5.0/19.0)*cRAD)+beamWidth2,zcoord],
                
    [-(7.0/19.0)*cRAD,findY((7.0/19.0)*cRAD)-beamWidth2,zcoord],
    [-(7.0/19.0)*cRAD,-findY((7.0/19.0)*cRAD)+beamWidth2,zcoord],               

    [-(9.0/19.0)*cRAD,findY((9.0/19.0)*cRAD)-beamWidth2,zcoord],  
    [-(9.0/19.0)*cRAD,-findY((9.0/19.0)*cRAD)+beamWidth2,zcoord],             
    
    [-(11.0/19.0)*cRAD,findY((11.0/19.0)*cRAD)-beamWidth2,zcoord], 
    [-(11.0/19.0)*cRAD,-findY((11.0/19.0)*cRAD)+beamWidth2,zcoord],            
    
    [-(13.0/19.0)*cRAD,findY((13.0/19.0)*cRAD)-beamWidth2,zcoord],    
    [-(13.0/19.0)*cRAD,-findY((13.0/19.0)*cRAD)+beamWidth2,zcoord],           
    
    [-(15.0/19.0)*cRAD,findY((15.0/19.0)*cRAD)-beamWidth2,zcoord],
    [-(15.0/19.0)*cRAD,-findY((15.0/19.0)*cRAD)+beamWidth2,zcoord],                

    #right side strings
    [(1.0/19.0)*cRAD,findY((1.0/19.0)*cRAD)-beamWidth2,zcoord], 
    [(1.0/19.0)*cRAD,-findY((1.0/19.0)*cRAD)+beamWidth2,zcoord], 
                 #2
    [(3.0/19.0)*cRAD,findY((3.0/19.0)*cRAD)-beamWidth2,zcoord],
    [(3.0/19.0)*cRAD,-findY((3.0/19.0)*cRAD)+beamWidth2,zcoord],
                   #4  
    [(5.0/19.0)*cRAD,findY((5.0/19.0)*cRAD)-beamWidth2,zcoord],   
    [(5.0/19.0)*cRAD,-findY((5.0/19.0)*cRAD)+beamWidth2,zcoord],
                #6
    [(7.0/19.0)*cRAD,findY((7.0/19.0)*cRAD)-beamWidth2,zcoord],
    [(7.0/19.0)*cRAD,-findY((7.0/19.0)*cRAD)+beamWidth2,zcoord],              

    [(9.0/19.0)*cRAD,findY((9.0/19.0)*cRAD)-beamWidth2,zcoord],  
    [(9.0/19.0)*cRAD,-findY((9.0/19.0)*cRAD)+beamWidth2,zcoord],             
    
    [(11.0/19.0)*cRAD,findY((11.0/19.0)*cRAD)-beamWidth2,zcoord], 
    [(11.0/19.0)*cRAD,-findY((11.0/19.0)*cRAD)+beamWidth2,zcoord],            
    
    [(13.0/19.0)*cRAD,findY((13.0/19.0)*cRAD)-beamWidth2,zcoord],    
    [(13.0/19.0)*cRAD,-findY((13.0/19.0)*cRAD)+beamWidth2,zcoord],            
    
    [(15.0/19.0)*cRAD,findY((15.0/19.0)*cRAD)-beamWidth2,zcoord],
    [(15.0/19.0)*cRAD,-findY((15.0/19.0)*cRAD)+beamWidth2,zcoord],

    #''' ----------- CROSSES (SIDE TO SIDE) -----------'''

    #upper side strings         
    [-findX(0)+beamWidth2, 0, zcoord],
    [findX(0)-beamWidth2,0,zcoord],

    [-findX(mRAD*1.0/10.0)+beamWidth2, (1.0/10.0)*mRAD, zcoord],
    [findX(mRAD*1.0/10.0)-beamWidth2, (1.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*2.0/10.0)+beamWidth2, (2.0/10.0)*mRAD, zcoord],
    [findX(mRAD*2.0/10.0)-beamWidth2, (2.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*3.0/10.0)+beamWidth2, (3.0/10.0)*mRAD, zcoord],
    [findX(mRAD*3.0/10.0)-beamWidth2, (3.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*4.0/10.0)+beamWidth2, (4.0/10.0)*mRAD, zcoord],
    [findX(mRAD*4.0/10.0)-beamWidth2, (4.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*5.0/10.0)+beamWidth2, (5.0/10.0)*mRAD, zcoord],
    [findX(mRAD*5.0/10.0)-beamWidth2, (5.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*6.0/10.0)+beamWidth2, (6.0/10.0)*mRAD, zcoord],
    [findX(mRAD*6.0/10.0)-beamWidth2, (6.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*7.0/10.0)+beamWidth2, (7.0/10.0)*mRAD, zcoord],
    [findX(mRAD*7.0/10.0)-beamWidth2, (7.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*8.0/10.0)+beamWidth2, (8.0/10.0)*mRAD, zcoord],
    [findX(mRAD*8.0/10.0)-beamWidth2, (8.0/10.0)*mRAD, zcoord],

    #bottom side strings         
    [-findX(mRAD*1.0/10.0)+beamWidth2, -(1.0/10.0)*mRAD, zcoord],
    [findX(mRAD*1.0/10.0)-beamWidth2, -(1.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*2.0/10.0)+beamWidth2, -(2.0/10.0)*mRAD, zcoord],
    [findX(mRAD*2.0/10.0)-beamWidth2, -(2.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*3.0/10.0)+beamWidth2, -(3.0/10.0)*mRAD, zcoord],
    [findX(mRAD*3.0/10.0)-beamWidth2, -(3.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*4.0/10.0)+beamWidth2, -(4.0/10.0)*mRAD, zcoord],
    [findX(mRAD*4.0/10.0)-beamWidth2, -(4.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*5.0/10.0)+beamWidth2, -(5.0/10.0)*mRAD, zcoord],
    [findX(mRAD*5.0/10.0)-beamWidth2, -(5.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*6.0/10.0)+beamWidth2, -(6.0/10.0)*mRAD, zcoord],
    [findX(mRAD*6.0/10.0)-beamWidth2, -(6.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*7.0/10.0)+beamWidth2, -(7.0/10.0)*mRAD, zcoord],
    [findX(mRAD*7.0/10.0)-beamWidth2, -(7.0/10.0)*mRAD, zcoord],

    [-findX(mRAD*8.0/10.0)+beamWidth2, -(8.0/10.0)*mRAD, zcoord],
    [findX(mRAD*8.0/10.0)-beamWidth2, -(8.0/10.0)*mRAD, zcoord],
    ]
    return tennis

strings = pointStrings(-beamWidth1/2.0)

def loopStrings(a,b):
    '''Strings are just lines connected by using vertices in the array'''
    glColor3ub(0,0,0)     #black
    glPushMatrix()
    glBegin(GL_LINES)
    glVertex3fv(strings[a])
    glVertex3fv(strings[b])
    glEnd()
    glPopMatrix()  

def drawStrings():
    i = 0
    while (i < 66):
        loopStrings(i,i+1)
        i = i + 2
''' -------------------- RACQUET HILT --------------------'''
def drawHilt(zcoord):
    '''Draws the hilt/handle of the racuqet. Temp are the coordinates at which the neck
    squares off. Uses this coordinate to connect to the handle'''
    temp = [(2.0/19.0)*cRAD,findY((10.0/19.0)*cRAD)+(8+2*beamWidth2)*(mRAD/12.0),zcoord]
    x = temp[0]
    y = temp[1]

    handle = [
        [-x, -y, zcoord],       #0 left top
        [-x,-y-cRAD,zcoord],     #1 left butt shoulder
        [-x-(0.5/19.0)*cRAD,(-y-cRAD)-((1.0/19.0)*cRAD),zcoord],   #2 left butt bottom
        [x+(0.5/19.0)*cRAD, (-y-cRAD)-((1.0/19.0)*cRAD),zcoord],   #3 right butt bottom
        [x+(0.5/19.0)*cRAD, (-y-cRAD), zcoord],                    #4 right butt shoulder
        [x,-y,zcoord]]              #5 right top
    return handle

def drawFullHandle():
    '''Draws the full handle of the racquet by connecting the sides, front and back vertices'''
    front = drawHilt(0)
    back = drawHilt(-beamWidth1)

    '''Front handle'''
    glColor3ub(0,0,0)                 
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3fv(front[0])
    glVertex3fv(front[1])
    glVertex3fv(front[2])
    glVertex3fv(front[3])
    glVertex3fv(front[4])
    glVertex3fv(front[5])
    glEnd()
    glPopMatrix()
    '''Back Handle'''   
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3fv(back[0])
    glVertex3fv(back[1])
    glVertex3fv(back[2])
    glVertex3fv(back[3])
    glVertex3fv(back[4])
    glVertex3fv(back[5])
    glEnd()
    glPopMatrix()
    '''Left Handle'''
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3fv(back[0])
    glVertex3fv(front[0])
    glVertex3fv(front[1])
    glVertex3fv(front[2])
    glVertex3fv(back[2])
    glVertex3fv(back[1])
    glEnd()
    glPopMatrix()
    '''Right Handle'''
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3fv(front[3])
    glVertex3fv(back[3])
    glVertex3fv(back[4])
    glVertex3fv(back[5])
    glVertex3fv(front[5])
    glVertex3fv(front[4])
    glVertex3fv(front[3])
    glEnd()
    glPopMatrix()
    '''Butt - slightly wider than the handle'''
    glPushMatrix()
    glBegin(GL_POLYGON)
    glVertex3fv(front[2])
    glVertex3fv(front[3])
    glVertex3fv(back[3])
    glVertex3fv(back[2])
    glEnd()
    glPopMatrix()

def drawRacquet():
    '''Combines the frame, neck, strings and handle all together. '''
    drawFrame()
    drawNeck()
    drawStrings()
    drawFullHandle()

def display():
    twDisplayInit()
    twCamera()
    drawRacquet()
    glFlush()
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    twBoundingBox(-cRAD,cRAD,-2*mRAD,mRAD,-5,5);
    twInitWindowSize(500,500)
    glutCreateWindow(sys.argv[0])
    glLineWidth(2);
    glutDisplayFunc(display)
    ## twSetMessages(TW_ALL_MESSAGES)
    twMainInit()
    glutMainLoop()

if __name__ == '__main__':
    main()
