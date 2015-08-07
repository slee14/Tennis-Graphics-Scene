"""This is the main file for the TW package, which is my supplement to
PyOpenGL. TW is separately documented, but in brief, its first and
most important feature is providing automatic camera setup based on a
bounding box for the scene.  There is also a provided user-interface
that includes mouse control of the camera direction and has
pre-defined keyboard callbacks to rotate the scene, move the camera,
turn lighting on/off and so forth..  There are a number of other
conveniences for curves and surfaces, texture mapping, and the like.

Scott D. Anderson
copyright under GNU General Public License 2009
"""

import sys
import math

## To test for printable characters
try:
    from curses.ascii import isgraph
except:
    print "could not import isgraph from curses"
    # this version is not smart about unicode
    def isgraph(c):
        return ord(c) >= ord(' ') and ord(c) <= ord('~')

# ================================================================
# I used to define this in another module called which, but managing the
# multiple files became a hassle, and it's only two definitions.

'''Like the Unix 'which' command, this searches down a path (a list of directories) for a file.

Implemented based on http://code.activestate.com/recipes/52224/

Scott D. Anderson
Fall 2009
'''

import os, os.path, string

def which(filename, search_path=sys.path, verbose=False):
    """returns the element (a directory) of the path where filename is found."""
    if search_path == sys.path:
        dirs = search_path
    elif type(search_path) == type(''):
        # assume strings need parsing
        dirs = string.split(search_path, os.pathsep)
    else:
        # assume everything else is a list, pre-parsed, as with sys.path
        dirs = search_path
    if verbose:
        print "search path is", dirs
    for directory in dirs:
        candidate = os.path.join(directory, filename)
        if os.path.exists(candidate):
            if verbose:
                print 'FOUND in ',directory
            return directory
        else:
            if verbose:
                print 'not found in ',directory
    return None

def subdir(parent, child):
    """returns a pathname for a subdirectory, tacking subdir onto the parent."""
    return string.join([parent, child], os.sep)

# ================================================================

def addContribDir():
    twhomedir = which("TW.py",sys.path)
    if twhomedir == '':
        contrib = './contrib'
    else:
        contrib = subdir(twhomedir,"contrib")
    # insert after the twhomedir
    sys.path.insert(sys.path.index(twhomedir)+1,contrib)

addContribDir()
          
# ================================================================

def checkWhetherPythonIsTooOld():
    """This function is immediately invoked and never used again.  The reason
it exists is to have local variables."""
    major,minor = os.version_info
    print major, minor
    if major < 2 or (major == 2 and minor < 5):
        print "This version of Python appears to be too old:", os.version
        print "I think I need at least version 2.5"
        sys.exit(0)

#print "hi"
#checkWhetherPythonIsTooOld()
#print "bye"
#sys.exit(0)

# ================================================================

# For the arrays of Bezier control points.  There is a shape() function in
# numpy that we could use, but numpy isn't installed on the Mac, and it
# was easy to just implement it myself.
        
# This function isn't ideally coded.  It should not assume that the argument
# is a tuple (it might be a list or a wrapper of some C array type).  Also,
# it would allocate less storage if it returned a list instead of a tuple,
# but that's minor.

def shape(array):
    tupleType = type(())
    listType = type([])
    
    # base case is a non-sequence
    if type(array) != tupleType and type(array) != listType:
        return 0
    if type(array[0]) != tupleType and type(array[0]) != listType:
        return (len(array),)
    subshapes = map(shape,array)
    first = subshapes[0]
    for subsh in subshapes:
        if not subsh == first:
            print "inconsistent shape"
            return None
    this_shape = [len(subshapes)]
    this_shape.extend(first)
    return this_shape

# ================================================================

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print '''
ERROR: PyOpenGL not installed properly.  
        '''
try:
  from OpenGL.constant import Constant
except:
  print '''
ERROR: Couldn't import OpenGL.constant
'''

### Uses same symbol name as C
M_PI = Constant( 'M_PI', math.acos(-1))

### ================================================================
### introspection

def twsymbol(x):
    return x[:2] == "tw"

def twsymbols():
    return [ x for x in dir(TW) if x[:2] == "tw" ]


### ================================================================
### For the transition

class NotYetImplementedError (Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "this function is not yet implemented"

def nyi():
    raise NotYetImplementedError


### ================================================================
### tw-utils

# these are basically cached values
twLoadPath = None
twLoadPathDefault = None

def twPathname(filename, verbose=True):
    """converts a simple filename into an absolute pathname that can be opened

The function searches the directories on the TWLOADPATH environment
variable to find an existing file and returns the absolute pathname.
The default value of TWLOADPATH is:

    .:$TWHOMEDIR/textures:$TWHOMEDIR/objects

where TWHOMEDIR is determined by the location of TW.py on PYTHONPATH.

If verbose is true, the function reports each load directory it searches.
"""
    if verbose:
        print "Trying to find path for ",filename
    global twLoadPath, twLoadPathDefault
    if type(filename) != type("filename"):
        print "twPathname needs a string, got ",filename
        raise TypeError(filename)
    # don't do anything for absolute pathnames
    if '/' == filename[0]:
        return filename
    if twLoadPath == None:
        twLoadPath = os.getenv('TWLOADPATH')
        if twLoadPath == None:
            # if it's *still* none, we have to construct it
            if twLoadPathDefault == None:
                twhomedir = which("TW.py",sys.path)
                twLoadPathDefault = [ os.getcwd(),
                                      subdir(twhomedir,'textures'),
                                      subdir(twhomedir,'objects')
                                      ]
            # set it to the default value
            twLoadPath = twLoadPathDefault
    if verbose:
        print 'twLoadPath is', twLoadPath
    directory = which(filename,twLoadPath,verbose)
    if directory != None:
        return subdir(directory,filename)
    else:
        return filename

### ================================================================
### tw-messages.cc messages, for debugging and inspection

TW_NO_MESSAGES   = Constant( 'TW_NO_MESSAGES',  0 )
TW_GEOMETRY      = Constant( 'TW_GEOMETRY',     1 )
TW_BOUNDING_BOX  = Constant( 'TW_BOUNDING_BOX', 2 )
TW_WINDOW        = Constant( 'TW_WINDOW',       4 )
TW_CAMERA        = Constant( 'TW_CAMERA',       8 )
TW_COLOR         = Constant( 'TW_COLOR',       16 )
TW_MATERIAL      = Constant( 'TW_MATERIAL',    32 )
TW_LIGHTING      = Constant( 'TW_LIGHTING',    64 )
TW_FONTS         = Constant( 'TW_FONTS',      128 )
TW_ALL_MESSAGES  = Constant( 'TW_ALL_MESSAGES', 255 )

# This variable is the messages that are currently on.
twMessageKinds = 0

### Like print, but can be turned on/off using twSetMessages.
def twMessage( messageKind, format, *args):
    global twMessageKinds
    if messageKind & twMessageKinds :
        print format % args
        
### To turn messages on and off, call this function with some bitwise
### combination of the constants above.

def twSetMessages( messages ):
    global twMessageKinds
    twMessageKinds = messages

### ================================================================
### tw-menu.cc
    
AXES = Constant('AXES',1)       # whether axes are drawn
BB = Constant('BB',2)           # whether the bounding box is drawn
IMMERSE = Constant('IMMERSE',3) # whether to reduce radius so eye is closer
LIGHTING = Constant('LIGHTING',4) # whether lighting is on
LIGHTS = Constant('LIGHTS',5)     # whether lights are shown
SMOOTH = Constant('SMOOTH',6)     # whether shading is flat or smooth
FULL_SCREEN = Constant('FULL_SCREEN',7) # whether to use the whole screen
FILTER_NEAREST = Constant('FILTER_NEAREST',8) # mag and min filter: linear (default) or nearest
ORIGIN = Constant('ORIGIN',9) # show the origin
NUM_TOGGLES = Constant('NUM_TOGGLES',10)       # used only for array limits

##  A bunch of booleans we might want
Toggles = [ False for x in range(NUM_TOGGLES) ]
    
def rightMenuCallback(id):
    global Toggles
    Toggles[id] = not Toggles[id]
    ## remake the menu
    makeToggleMenu()
    if IMMERSE == id:
        twZview()
    if FULL_SCREEN == id:
        if Toggles[FULL_SCREEN]:
            twFullScreen()
        else:
            twWindow()
    glutPostRedisplay()
    return id

## holds the menu GLUT object
RightMenu = 0




def makeToggleMenu():
    global Toggles, RightMenu
    if RightMenu != 0:
        glutDestroyMenu(RightMenu)
    RightMenu = glutCreateMenu(rightMenuCallback)
    glutAddMenuEntry("Hide Axes" if Toggles[AXES] else "Show Axes",AXES)
    glutAddMenuEntry("Hide Bounding Box" if Toggles[BB] else "Show Bounding Box",BB)
    glutAddMenuEntry("Hide Origin" if Toggles[ORIGIN] else "Show Origin",ORIGIN)
    glutAddMenuEntry("Back up" if Toggles[IMMERSE] else "Immerse",IMMERSE)
    glutAddMenuEntry("Disable Lighting" if Toggles[LIGHTING] else "Enable Lighting",LIGHTING)
    glutAddMenuEntry("Hide Lights" if Toggles[LIGHTS] else "Show Lights",LIGHTS)
    glutAddMenuEntry("Flat Shading" if Toggles[SMOOTH] else "Smooth Shading",SMOOTH)
    glutAddMenuEntry("Window" if Toggles[FULL_SCREEN] else "Full Screen",FULL_SCREEN)
    glutAddMenuEntry("FILTER NEAREST" if Toggles[FILTER_NEAREST] else "Filter: Nearest",FILTER_NEAREST)
    glutAttachMenu(GLUT_RIGHT_BUTTON)


### ================================================================  
### tw-color.cc

### The following color names are defined in TW.  You can switch to one of
### these colors using the twColorName function, giving one of the symbols
### below as the argument.  


TW_BLACK   = 0
TW_WHITE   = 1
TW_YELLOW  = 2
TW_ORANGE  = 3
TW_MAGENTA = 4
TW_RED     = 5
TW_SILVER  = 6
TW_GRAY    = 7
TW_OLIVE   = 8
TW_PURPLE  = 9
TW_MAROON  = 10
TW_CYAN    = 11
TW_TEAL    = 12
TW_GREEN   = 13
TW_BLUE    = 14
TW_DARK_BLUE = 15
TW_LIGHT_BLUE = 16
TW_PINK    = 17
TW_BROWN   = 18

TW_NUM_COLORS = 19

twColors = [
    (0,0,0),                    # 0 black
    (1,1,1),                    # 1 white
    (1,1,0),                    # 2 yellow
    (1,0.5,0),                  # 3 orange
    (1,0,1),                    # 4 magenta
    (1,0,0),                    # 5 red
    (0.8,0.8,0.8),              # silver
    (0.5,0.5,0.5),              # gray
    (0.5,0.5,0),                # olive
    (0.5,0,0.5),                # purple
    (0.7,0.19,0.38),            # maroon
    (0,1,1),                    # cyan
    (0,0.5,0.5),                # teal
    (0,1,0),                    # green
    (0,0,1),                    # blue
    (0,0,0.5),                  # dark blue
    (0.7,0.7,1),                # light blue
    (1,0.75,0.8),               # pink
    (0.8,0.5,0.3),              # brown
    ()
    ]

def twHSV2RGB( hsv ):
    '''Convert HSV to RGB values, both specified as tuples.  Hue is
specified as an angle in degrees from pure red.  Code adapted from
Foley & van Dam, page 593'''
    h,s,v = hsv
    if s == 0.0:
        rgb = (v, v, v)
    else:
        ## Color with a hue, since S is non-zero
        if h==360.0:
            h = 0.0             # 360 degrees is the same as zero
        h = h / 60.0            # h is now in [0,6)
        i = math.floor(h)       # Floor is largest integer <= h
        f = h-i                 # f is the fractional part of h
        p = v*(1.0-s)
        q = v*(1.0-(s*f))
        t = v*(1.0-(s*(1.0-f)))
        ## i essentially tells us which of the six vertices we are closest to.
        ## More precisely, it tells us which triangular wedge we are in.
        ## p is our distance in from the edge of the hexagon.
        if i==0:  rgb = (v,t,p)
        if i==1:  rgb = (q,v,p)
        if i==2:  rgb = (p,v,t)
        if i==3:  rgb = (p,q,v)
        if i==4:  rgb = (t,p,v)
        if i==5:  rgb = (v,p,q)
    return rgb

def twColorOkay( color ):
    return (0.0 <= color[0] and color[0] <= 1.0 ) and \
        (0.0 <= color[1] and color[1] <= 1.0 ) and \
        (0.0 <= color[2] and color[2] <= 1.0 )

def twColorToString( color ):
    return "color:  %f %f %f" % (color[0], color[1], color[2] )

### Remember that RGB color and material are mutually exclusive, so if
### lighting is enabled, RGB color is ignored, and if lighting is disabled,
### material is ignored.  This function does both, so that your object
### looks approximately right whether or not lighting is enabled.

### Note, there is a risk here, because the color is supposed to be a
### four-place tuple, and we're using a three-place tuple.  So far, that's
### been okay.

def twColor( color, spec, shininess, face=GL_FRONT):
    '''Sets the material properties using a reduced amount of information.
Both ambient and diffuse is set to 'color,' and specularity is set to a
triple using 'spec.' Finally, the shininess exponent is set to the last
parameter.  The properties are set to the front face unless otherwise 
specified by the last parameter.'''
    if not twColorOkay(color) :
        print "color does not have valid components (between 0 and 1):  %f %f %f" % (color[0], color[1], color[2] )
    
    if  shininess < 0 or shininess > 128 :
        print "shininess is not between 0 and 128:  %f" % ( shininess )

    ##print "switching color to " + twColorToString( color )

    ## The following is if lighting is off
    glColor3fv(color)
    ##  The rest is if lighting is on.
    if True: 
        matSpecular = ( spec, spec, spec )
        glMaterialfv(face,GL_AMBIENT_AND_DIFFUSE,color)
        glMaterialfv(face,GL_SPECULAR,matSpecular)
        glMaterialf(face,GL_SHININESS,shininess)


def twColorName( i ):
    if 0 <= i and i < TW_NUM_COLORS :
        twColor(twColors[i], 0, 0)
    else:
        print "invalid color number:  %d, must be less than %d" % (i, TW_NUM_COLORS)



### ================================================================
### tw-bounding-box.cc code

BoundingBoxInitialized = False

BBCenter = (None, None, None)       # the center point of the bounding box.
BBMin = (None, None, None)          # the min corner
BBMax = (None, None, None)          # the max corner
OuterRadius = None                  # radius of the bounding sphere
InnerRadius = None                  # radius of the inner sphere

def twBoundingBox(xmin, xmax, ymin,  ymax, zmin,  zmax):
    '''computes near and far using bounding box coordinates'''  
    global BBMin, BBMax, BBCenter, OuterRadius, InnerRadius, BoundingBoxInitialized, twMessageKinds
    if( xmin > xmax ):
        print "xmax (%f) must be greater than or equal to xmin (%f)" % (xmax,xmin)
    if( ymin > ymax ):
        print "ymax (%f) must be greater than or equal to ymin (%f)" % (ymax,ymin)
    if( zmin > zmax ):
        print "zmax (%f) must be greater than or equal to zmin (%f)" % (zmax,zmin)
    ## store the box
    BBMin = (xmin,ymin,zmin)
    BBMax = (xmax,ymax,zmax)
    BBCenter = ((xmax+xmin)*0.5,(ymax+ymin)*0.5,(zmax+zmin)*0.5)
    OuterRadius = twPointDistance(BBMin,BBMax)*0.5
    InnerRadius = min(min(xmax-xmin,ymax-ymin),zmax-zmin)*0.5
    BoundingBoxInitialized = True
    if(TW_BOUNDING_BOX & twMessageKinds):
        twTriplePrint("BB Center",BBCenter)
        twTriplePrint("BB Min",BBMin)
        twTriplePrint("BB Max",BBMax)
        print "Outer radius = %f, inner = %f" % (OuterRadius,InnerRadius)

def twVertexArray(va):
    '''Takes the student's array va with n points and computes the bounding
   box, then calls twBoundingBox.'''

    xs = map( lambda elt: elt[0], va )
    ys = map( lambda elt: elt[1], va )
    zs = map( lambda elt: elt[2], va )
    maxx = max(xs)
    minx = min(xs)
    miny = min(ys)
    maxy = max(ys)
    minz = min(zs)
    maxz = max(zs)
    twBoundingBox(minx, maxx, miny, maxy, minz, maxz)

def twDrawBoundingBox():
    global BBMin, BBMax
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glLineWidth(1)
    glBegin(GL_LINES)
    glColor3f(1,0,0)            # red for lines parallel to x
    glVertex3f(BBMin[0],BBMin[1],BBMin[2])
    glVertex3f(BBMax[0],BBMin[1],BBMin[2])

    glVertex3f(BBMin[0],BBMax[1],BBMin[2])
    glVertex3f(BBMax[0],BBMax[1],BBMin[2])

    glVertex3f(BBMin[0],BBMin[1],BBMax[2])
    glVertex3f(BBMax[0],BBMin[1],BBMax[2])

    glVertex3f(BBMin[0],BBMax[1],BBMax[2])
    glVertex3f(BBMax[0],BBMax[1],BBMax[2])

    glColor3f(0,1,0);           # // for lines parallel to y
    glVertex3f(BBMin[0],BBMin[1],BBMin[2])
    glVertex3f(BBMin[0],BBMax[1],BBMin[2])

    glVertex3f(BBMax[0],BBMin[1],BBMin[2])
    glVertex3f(BBMax[0],BBMax[1],BBMin[2])

    glVertex3f(BBMin[0],BBMin[1],BBMax[2])
    glVertex3f(BBMin[0],BBMax[1],BBMax[2])

    glVertex3f(BBMax[0],BBMin[1],BBMax[2])
    glVertex3f(BBMax[0],BBMax[1],BBMax[2])

    glColor3f(0,0,1);           # blue for lines parallel to z
    glVertex3f(BBMin[0],BBMin[1],BBMin[2])
    glVertex3f(BBMin[0],BBMin[1],BBMax[2])

    glVertex3f(BBMax[0],BBMin[1],BBMin[2])
    glVertex3f(BBMax[0],BBMin[1],BBMax[2])

    glVertex3f(BBMin[0],BBMax[1],BBMin[2])
    glVertex3f(BBMin[0],BBMax[1],BBMax[2])

    glVertex3f(BBMax[0],BBMax[1],BBMin[2])
    glVertex3f(BBMax[0],BBMax[1],BBMax[2])

    glEnd()
    glPopAttrib()
        
### ================================================================
### tw-lighting.cc

### We define this as a global so that we can initialize it in twMainInit.
### Furthermore, making it global also allows other TW functions to
### reference it, if desired.

GlobalAmbient = 0.3             # OpenGL default value is 0.2

def twAmbient(value):
  '''Sets the global ambient light to a gray light with given value'''
  global GlobalAmbient
  GlobalAmbient = value;
  matGlobalAmbient = (GlobalAmbient,GlobalAmbient,GlobalAmbient)
  glLightModelfv(GL_LIGHT_MODEL_AMBIENT,matGlobalAmbient)

def twGrayLightCore(lightId, position, ambient, diffuse, specular, quiet=False):
    '''sets up a light source from given position and gray light with
    given ambient, diffuse and specular values

    position is a four-place tuple or list.  Checks for values between
    0 and 1.  If you're using values outside that range and you don't
    want it to complain, set the optional last argument to true.  This
    version is for TW-internal use; users should invoke
    twGrayLight()'''
    global Toggles, OuterRadius
    pos = position
    a = ambient
    d = diffuse
    s = specular

    if len(position) < 4:
        raise IndexError, "light position should be a four element list/tuple: %s" % ( str(position) )
    lightColor = [0, 0, 0, 1]   # the default

    if lightId < GL_LIGHT0 or lightId >= GL_LIGHT0+GL_MAX_LIGHTS:
        print ("invalid light ID: %d" %  lightId)
        return
    if pos[3] != 0.0 and pos[3] != 1.0:
        print "w component of light position should be 0 or 1" % (pos[3])
        return
    if not quiet:
        if not ((0 <= a and a <= 1.0) and
                (0 <= d and d <= 1.0) and
                (0 <= s and s <= 1.0) ):
            if( a < 0.0 ): print "ambient should be at least 0.0:  %f" % (a)
            if( a > 1.0 ): print "ambient should be at most  1.0:  %f" % (a)
            if( d < 0.0 ): print "diffuse should be at least 0.0:  %f" % (d)
            if( d > 1.0 ): print "diffuse should be at most  1.0:  %f" % (d)
            if( s < 0.0 ): print "specular should be at least 0.0:  %f" % (s)
            if( s > 1.0 ): print "specular should be at most  1.0:  %f" % (s)
    glLightfv(lightId, GL_POSITION, pos)
    lightColor[0] = lightColor[1] = lightColor[2] = a
    glLightfv(lightId, GL_AMBIENT, lightColor)
    lightColor[0] = lightColor[1] = lightColor[2] = d
    glLightfv(lightId, GL_DIFFUSE, lightColor)
    lightColor[0] = lightColor[1] = lightColor[2] = s
    glLightfv(lightId, GL_SPECULAR, lightColor)
 
    glEnable(lightId)

def twGrayLight(lightId, position, ambient, diffuse, specular, quiet=False):
    '''sets up a light source from given position and gray light with
    given ambient, diffuse and specular values

    position is a four-place tuple or list.  Checks for values between
    0 and 1.  If you're using values outside that range and you don't
    want it to complain, set the optional last argument to true.'''
    global Toggles, OuterRadius
    pos = position
    a = ambient
    d = diffuse
    s = specular

    twGrayLightCore(lightId, position, ambient, diffuse, specular, quiet)
    if Toggles[ LIGHTS ]:
        glPushAttrib(GL_ALL_ATTRIB_BITS)
        glDisable(GL_LIGHTING)
        if pos[3] == 1.0:
            ## positional light
            glColor3f(a,d,s)    # for lack of a better idea.
            glPointSize(5)
            glBegin(GL_POINTS)
            glVertex4fv(pos)
            glEnd()
        elif pos[3] == 0.0:
            ## directional light
            glLineWidth(1)
            dir = twVectorNormalize(pos)
            dir = twVectorScale(dir,OuterRadius); # long enough to leave the BB
            end = twPoint(BBCenter,dir)           # compute end point
            dir = twVectorScale(dir,-1)           # reverse it
            start = twPoint(BBCenter,dir)         # compute starting point
            
            glBegin(GL_LINES)
            glColor3f(1,1,1)
            glVertex3fv(start)
            glColor3f(0,0,0)
            glVertex3fv(end)
            glEnd()
        else:
            print "This light seems to be neither positional nor directional"
        glPopAttrib()

def twLightCutoffOkay( cutoff ):
    '''true if the cutoff in the Phong lighting model is in [0,90] degrees or exactly 180'''
    return (0.0 <= cutoff and cutoff <= 90.0 ) or cutoff == 180.0

def twLightExponentOkay( exponent ):
    '''true if the exponent for the Phong lighting model is in [0,128]'''
    return (0.0 <= exponent and exponent <= 128 )

def twGraySpotlight(lightId, position, ambient, diffuse, specular,
                    direction, cutoff, spot_exponent):
    '''sets up a spotlight with given parameters and gray light
with given ambient, diffuse and specular values

    position is a four-place tuple or list.  Direction is a 3 or 4 place
    tuple or list.  Cutoff and spot_exponent are scalars.'''
    a = ambient
    d = diffuse
    s = specular
    pos = position
    if pos[3] == 0.0:
        print "Spotlights shouldn't be directional:  ", pos
        return
    twGrayLightCore(lightId, pos, a, d, s)
    glLightfv(lightId, GL_SPOT_DIRECTION, direction)
    if not twLightCutoffOkay(cutoff):
        print "Spotlight cutoffs must be in [0,90] or equal to 180: %f" % (cutoff)
        return
    glLightf(lightId, GL_SPOT_CUTOFF, cutoff)
    if not twLightExponentOkay(spot_exponent):
        print "Spotlight exponents must be in [0,128]: %f" % (spot_exponent)
        return
    glLightf(lightId, GL_SPOT_EXPONENT, spot_exponent)
    lightColor = (0, 0, 0, 1) # the default
    glEnable(lightId)
    if Toggles[ LIGHTS ]:
        glPushAttrib(GL_ALL_ATTRIB_BITS);
        glDisable(GL_LIGHTING);
        ## ideally, draw a cone at the light source, facing the correct
        ## way.  The technique should be to compute the cross product and
        ## dot product between the vector of a conventional cone
        ## (e.g. twCylinder) and the direction of the light, and then
        ## rotate the coordinate system around that axis and at that
        ## angle, then draw a cone.  Let's see if it works.  We'll use a
        ## unit-high cone; scale the world if you want it bigger.
        before = ( 0, 0, 1 )
        dirnorm = twVectorNormalize(direction)
        axis = twCrossProduct(before,direction)
        angle = twRadiansToDegrees(math.acos(twDot(before,dirnorm)))
        coneHeight = 1
        coneTop = coneHeight*math.tan(twDegreesToRadians(cutoff))
        if False:
          print "dot is ", twDot(before,dirnorm)
          print "spotlight direction angle is %f" % (angle)
          print "spotlight axis to rotate around is %f %f %f" % (axis[0],axis[1],axis[2])

        glPushMatrix()
        twTranslate(pos)        # move light to position
        glRotatef(angle,axis[0],axis[1],axis[2])
        glColor3f(a,d,s)
        twCylinder(0,coneTop,coneHeight,8,1)
        glPopMatrix()
        glPopAttrib()
        

### ================================================================
### tw-window.cc

### The following is the aspect ratio of the top of the frustum, which
### will result in no distortion if it matches the aspect ratio of the
### viewport.

AspectRatio = None

## Records the dimensions of the current window as a pair.  Should always be integers

WindowSize  = (None,None)

## and saved values of those dimensions

WindowSizeOld  = (None,None)

def twGetWindowSize():
    """returns the window dimensions as a pair of integers"""
    ## tuples are immutable, so safe to return this
    global WindowSize
    return WindowSize


def setWindowSize( ww, wh ):
    """informs TW of the window dimensions; useful if they have changed"""
    global WindowSize, AspectRatio
    WindowSize = (ww,wh)
    AspectRatio = float(ww)/float(wh)
    twMessage(TW_WINDOW,"window = (%d,%d), aspect ratio = %f",
              ww,wh,AspectRatio)

def twReshapeFunction(w, h):
    """A function suitable to be a reshape callback function for OpenGL"""
    setWindowSize(w,h)

def twInitWindowSize(xsize,ysize):
    """Sets the initial size of a GLUT window"""
    global WindowSize
    glutInitWindowSize(xsize,ysize)
    setWindowSize(xsize,ysize)

def twFullScreen():
    """Switch to full-screen mode"""
    global WindowSize, WindowSizeOld
    twMessage(TW_WINDOW,"switch to full screen, saving %d x %d",
              _WindowSize[0],WindowSize[1])
    _WindowSizeOld  = WindowSize
    glutFullScreen()

def twWindow():
    """Switched out of full-screen mode to the previous size window"""
    global WindowSize, WindowSizeOld
    twMessage(TW_WINDOW,"back to %d x %d window",
              WindowSizeOld[0],WindowSizeOld[1])
    glutReshapeWindow(WindowSizeOld[0],WindowSizeOld[1])
    glutPositionWindow(0,0)

### ================================================================
### tw-camera.cc 

LETTERBOX = Constant( 'LETTERBOX', 0 )
DISTORT   = Constant( 'DISTORT',   1 )
CLIP      = Constant( 'CLIP',      2 )

DEFAULT_FOVY = 90.0

### values for the current camera. The default values are unnecessary, as
### the actual values are computed below

_near = 1
_far  = 1000

_VPN = (0,0,-1)              # View Plane Normal
_VUP = (0,1,0)               # the ``up'' vector
_VRP = (0,0,1)               # the View Reference Point (the eye location)

_FieldOfView  = DEFAULT_FOVY    # for square frustum
_FieldOfViewY = DEFAULT_FOVY    # arg for gluPerspective

DEPTH_BITS_TO_LOSE = Constant( 'DEPTH_BITS_TO_LOSE', 5 )   # see doc.tex for more info

### spinning stuff.  We can spin around any of the three major axes

X_AXIS = Constant( 'X_AXIS', 0 )
Y_AXIS = Constant( 'Y_AXIS', 1 )
Z_AXIS = Constant( 'Z_AXIS', 2 )

_SpinAxis = X_AXIS              # default is to spin around X

_twSpinAngle = 0.5              # default angle per frame

def twNearFarSet():
    """Return a tuple of the current 'near' and 'far' values"""
    global _near,_far
    return (_near,_far)

def twFovySet():
    """Return the FieldOfViewY"""
    global _FieldOfViewY
    return _FieldOfViewY

def twSpin():
    """Rotates the viewpoint by one step around the current spin axis

    This function can be used by itself, maybe in debugging, but is mostly
    registered as an idle callback by startSpinning to start the object
    spinning."""
    global _twSpinAngle, _SpinAxis
    if _SpinAxis == X_AXIS:
        twRotateViewpoint(_twSpinAngle,(1,0,0))
    if _SpinAxis == Y_AXIS:
        twRotateViewpoint(_twSpinAngle,(0,1,0))
    if _SpinAxis == Z_AXIS:
        twRotateViewpoint(_twSpinAngle,(0,0,1))
    glutPostRedisplay()

def startSpinning( axis ):
    """Start the object spinning around the given axis, one of _X, _Y, _Z"""
    global _SpinAxis
    _SpinAxis = axis
    twIdleFunc(twSpin)

def twSpinCommand (key, x, y):
    """A keyboard callback for the various spin commands"""
    global _twSpinAngle
    if key == '-':
        _twSpinAngle *= 0.5      # halves the speed
        print "twSpinAngle=%f" % (_twSpinAngle)
    if key == '+':
        _twSpinAngle *= 2.0      # doubles the speed
        print "twSpinAngle=%f" % (_twSpinAngle)
    if key == 'x':
        startSpinning(X_AXIS)
    if key == 'y':
        startSpinning(Y_AXIS)
    if key == 'z':
        startSpinning(Z_AXIS)

def twGetModelView():
    """Return the modelview matrix"""
    return glGetDoublev(GL_MODELVIEW_MATRIX)

def twGetProjection():
    """Return the projection matrix"""
    return glGetDoublev(GL_PROJECTION_MATRIX)

### 
def twGetViewport():
    """return the viewport array"""
    glGetIntegerv(GL_VIEWPORT)

def twProject(v):
    """return the window projection of the vertex v

    That is, this function computes where on the screen, in window coordinates, V will project"""
    ### Python buys us a lot here!
    x, y, z = v
    return gluProject(x,y,z)

def twUnProject(w):
    """return a world vertex coordinate corresponding to window location w"""
    x, y, z = w
    return gluUnProject(x,y,z)

### ================================================================

### Stores into M a rotation matrix of angle degrees around vector (x,y,z).
### Normalizes the vector.  If the vector is zero length, returns
### immediately without modifying M.  From the GL reference manual for
### glRotate.
def rotationMatrix(angle, x, y, z):
    """return a rotation matrix of angle degrees around vector (x,y,z)

    Normalizes the vector.  If the vector is zero length, return
    false. From the GL reference manual for glRotate"""
    
    r = twDegreesToRadians(angle)
    c = math.cos(r)
    s = math.sin(r)
    l = x*x+y*y+z*z
    
    if l==0.0:
        return False

    x=x/l
    y=y/l
    z=z/l

    M = [
        x*x*(1-c)+c,
        y*x*(1-c)+z*s,
        x*z*(1-c)-y*s,
        0,
        x*y*(1-c)-z*s,
        y*y*(1-c)+c,
        y*z*(1-c)+x*s,
        0,
        x*z*(1-c)+y*s,
        y*z*(1-c)-x*s,
        z*z*(1-c)+c,
        0,
        0,
        0,
        0,
        1]
    return M
        

### ================================================================
### Done to here.  There rest is cherry-picked
### ================================================================

def twRotateViewpoint( angle,  r):
    '''Rotates the viewpoint (changing the VRP, VPN and VUP so that it
still looks at the center, but from a different place) by the given
angle around the given rotation vector.  Returns if angle is zero.'''
    global _VRP, _VPN, _VUP

    if 0==angle:
        return
    if not BoundingBoxInitialized:
        print "Bounding Box not initialized"
        return
    r = twVectorNormalize(r)
    ### printf("rotate by %f around %f %f %f\n",angle, r[0],r[1],r[2]);
    if not Toggles[IMMERSE]:
        _VPN = twVector(BBCenter,_VRP)
    M = rotationMatrix(angle,r[0],r[1],r[2])
    _VPN = mult3(M,_VPN)
    _VUP = mult3(M,_VUP)
    if( not Toggles[IMMERSE] ):
        ### recalculate VRP
        VPN_reverse = twVectorScale(_VPN,-1)
        _VRP = twPoint(BBCenter,VPN_reverse);
    glutPostRedisplay();    


def twRotateVPN(angle,  rotationVector):
    '''Rotates the view plane normal (VPN), keeping the VRP fixed, so
that we are tilting or panning the camera. Rotates by the given angle
(in degrees) around the given rotation vector.  Returns if angle is
zero.  Leaves VUP unchanged.  If the VPN would end up outside the
original frustum, it is limited to that angle.  This is done by
limiting to 45 degrees from the vector from the VPN to the Center.'''
    global _VPN
    if 0==angle:
        return
    if( not BoundingBoxInitialized):
        print ("Bounding Box not initialized")
        return
    r = twVectorNormalize(rotationVector)
    ### printf("tilt/pan by %f around %f %f %f\n",angle, r[0],r[1],r[2]);
    M = rotationMatrix(angle,r[0],r[1],r[2])
    newVPN = mult3(M,_VPN)

    ### Code to check limits on rotation
    originalVPN = twVector(BBCenter,_VRP)
    cosTotalAngle = twCosAngle(originalVPN,newVPN);
    if cosTotalAngle < math.cos(M_PI/4.0):
        ### printf("limiting rotation to 45 degrees\n");
        M = rotationMatrix(45,r[0],r[1],r[2])
        newVPN = mult3(M,originalVPN)
    ### finally, modify the global VPN
    _VPN = newVPN
    glutPostRedisplay()

def twTrackballOrientation( Ax,  Ay,  Bx,  By):
    """Rotates the viewpoint by an angle defined by two window locations (Ax,Ay) and (Bx,By).

    The y coordinate of the window locations should
    already have been subtracted from the window height."""
    global BoundingBoxInitialized
    if not BoundingBoxInitialized:
        print "Bounding Box not initialized"
        return
    winA = (Ax, Ay, 0)
    winB = (Bx, By, 0)
    A = twUnProject(winA)
    B = twUnProject(winB)
    V = twVector(A,BBCenter)
    W = twVector(B,BBCenter)
    angle = twRadiansToDegrees(math.acos(twCosAngle(V,W)))
    n = twCrossProduct(V,W)
    twRotateViewpoint(-angle,n)

### ================================================================

def twOrientVPN(x, y):
    '''Modify the VPN so that the (x,y) pixel coordinates are in the center of
the screen.  Ultimately calls RotateVPN.'''
    win = (x,y,0)               # window coordinates of click
    C = twUnProject(win)        # world coordinates of click
    v = twVector(C,_VRP)        # vector from VRP to location of click
    angle = twRadiansToDegrees(math.acos(twCosAngle(v,_VPN))) # angle to turn, in degrees
    axis = twCrossProduct(_VPN,v) # axis to turn around
    axis = twVectorNormalize(axis)
    twRotateVPN(angle,axis)
    
def twPerspective( fovy, ar, kind):
    global _near,_far, _FieldOfViewY, TW_CAMERA

    twMessage(TW_CAMERA,"gluPerspective: fovy = %f ar = %f near = %f far = %f",
              fovy,ar,_near,_far)
    gluPerspective(fovy,ar,_near,_far)
    _FieldOfViewY = fovy        ### store into global
    ### yes, I know this recomputes things that are already computed, but I
    ### think the modularity is best this way.
    fh = math.tan(fovy/2)*_near*2
    fw = fh*ar
    ww, wh = twGetWindowSize()
    twMessage(TW_CAMERA,"frustum WxH = %f x %f window %4d x %4d", fw, fh, ww, wh)


### This converts FOVX into FOVY, both in degrees
def twFOVX2FOVY(fovx):
    global AspectRatio
    
    ### For our code, this is a common special case.  tan(90)=1
    if 90.0==fovx:
        frustumWidth = _near*2
    else:
        ### convert to radians
        frustumWidth = _near*2*math.tan(twDegreesToRadians(fovx/2))
    frustumHeight=frustumWidth/AspectRatio
    fovy = 2*twRadiansToDegrees(math.atan(frustumHeight/2/_near))
    if fovy < 0:
        print "ack! fovy<0.  fovx=%f fovy=%f" % (fovx,fovy)
        print "frustumWidth=%f frustumHeight=%f AR=%f" % (frustumWidth,frustumHeight,AspectRatio)
    return fovy

FrustumMode = LETTERBOX

### 
def twFrustumMode(mode):
    """Sets the frustum mode to LETTERBOX, DISTORT, or CLIP"""
    global FrustumMode
    FrustumMode = mode
    print ('Letterbox mode','Clipping mode','Distorting mode')[mode]

### function to set up the camera shape, based on global variables
### AspectRatio, twfrustumMode, _near.  If the argument is non-zero, the
### frustum shape is printed.

def twCameraShape():
    """set camera shape based on globals AspectRatio, FrustumMode and Near"""
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    if FrustumMode == DISTORT:
        twMessage( TW_CAMERA, "Distorting Mode" )
        twPerspective(_FieldOfView,1,"DISTORT")
    elif FrustumMode == LETTERBOX:
        twMessage( TW_CAMERA, "Letterbox Mode" )
        ### To letterbox, the smaller angle of the frustum is determined by
        ### the radius of the bounding sphere, thereby guaranteeing that
        ### everything is inside it.  The larger angle will capture empty
        ### space.
        if AspectRatio < 1:
            ### portrait, so the vertical angle is larger, and we have to
            ### calculate it from the smaller angle, which is 90.
            twPerspective(twFOVX2FOVY(_FieldOfView),AspectRatio,"LETTERBOX")
        else:
            ### landscape
            twPerspective(_FieldOfView,AspectRatio,"LETTERBOX")
    elif FrustumMode == CLIP:
        ### To clip, the larger angle of the frustum is determined by the
        ### radius of the bounding sphere, so that the other angle is
        ### smaller than 90, cutting off part of the sphere.
        if AspectRatio < 1:
            ### portrait, so the vertical angle is 90 degrees
            twPerspective(_FieldOfView,AspectRatio,"CLIP")
        else:
            ### landscape, so the vertical angle is determined from the
            ### smaller, which is 90 degrees.
            twPerspective(twFOVX2FOVY(_FieldOfView),AspectRatio,"LETTERBOX")
    else:
        print 'invalid value of FrustumMode: ',FrustumMode


def twTranslate(p):
     '''Translate origin to location/point p.'''
     if len(p) < 3:
         print "point should be (at least) a triple: ", p
         return
     if len(p) == 3:
         x, y, z = p
     else:
         x, y, z, w = p
     glTranslatef(x,y,z)

def twAxes():
    '''Draws the three major axes of the coordinate system: an X axis in red,
a Y axis in green and a Z axis in blue.  The axes emanate from the center
of the bounding box, so they should always be visible.  They do not
emanate from the origin.'''
    global OuterRadius
    if not BoundingBoxInitialized:
        print "Bounding Box not initialized"
        return
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glDisable(GL_LIGHTING)
    glPushMatrix()
    twTranslate(BBCenter)
    glEnable(GL_LINE_STIPPLE);
    glLineStipple(3, 0xcccc);
    glBegin(GL_LINES);
    glColor3f(1,0,0); ### red for x axis
    glVertex3f(OuterRadius,0,0);
    glVertex3f(0,0,0);
    glColor3f(0,1,0); ### green for y axis
    glVertex3f(0,OuterRadius,0);
    glVertex3f(0,0,0);
    glColor3f(0,0,1); ### blue for z axis
    glVertex3f(0, 0,OuterRadius);
    glVertex3f(0, 0,0);
    glEnd();
    glDisable(GL_LINE_STIPPLE);
    glPopMatrix();
    glPopAttrib();


twDefaultOriginPointSize = 5

def twSetOriginPointSize(size):
    '''Sets the size that the origin will be drawn, in pixels'''
    global twDefaultOriginPointSize
    twDefaultOriginPointSize = size

def twDrawOrigin():
    '''Draws a big white dot at the origin of the "global" coordinate
system.  Depending on your bounding box, the origin may not be visible
at all; that's up to you.  To adjust the size of the dot, see
twSetOriginPointSize; value is in pixels.'''
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glDisable(GL_LIGHTING)
    glPointSize(twDefaultOriginPointSize)
    glColor(1,1,1)              # origin in white
    glBegin(GL_POINTS)
    glVertex3f(0,0,0)
    glEnd()
    glPopAttrib()


def twOriginalView():
    global Toggles, OuterRadius, InnerRadius, _VRP, _VPN, _VUP
    global _FieldOfView, _FieldOfViewY, _near,_far
    if not BoundingBoxInitialized:
        print ("Bounding Box not initialized")
        return
    _FieldOfView = _FieldOfViewY = DEFAULT_FOVY;
    eyeRadius = OuterRadius * math.sqrt(2)
    _far  = eyeRadius + OuterRadius;
    _VRP = BBCenter
    if Toggles[IMMERSE]:
        ### InnerRadius/M_SQRT2 is the largest possible value of near.
        ### Smaller means less stuff is cut off, at the price of, maybe
        ### some problems with the depth buffer.
        ### near = InnerRadius/M_SQRT2/2;
        _near = _far/(1<<DEPTH_BITS_TO_LOSE)
        twMessage(TW_CAMERA,
                  "twCameraPosition: INSIDE InnerRadius = %f, near = %f far = %f",
                  InnerRadius, _near, _far)
    else:
        _VRP[2] += eyeRadius;
        _near = eyeRadius-OuterRadius
        twMessage(TW_CAMERA,
                  "twCameraPosition: OUTSIDE OuterRadius = %f, near = %f far = %f",
                  OuterRadius, _near, _far)
    _VPN = (0,0,-1)
    _VUP = (0,1,0)

def twInitView(axis):
    global _near, _far, _VRP, OuterRadius
    if not BoundingBoxInitialized:
        print ("Bounding Box not initialized")
        return
    _FieldOfView = _FieldOfViewY = DEFAULT_FOVY;
    eyeRadius = OuterRadius*math.sqrt(2)
    _far  = eyeRadius+OuterRadius;
    _VRP = BBCenter
    if Toggles[IMMERSE]:
        ### InnerRadius/M_SQRT2 is the largest possible value of near.
        ### Smaller means less stuff is cut off, at the price of, maybe
        ### some problems with the depth buffer.
        ### near = InnerRadius/M_SQRT2/2;
        _near = _far/math.pow(2,DEPTH_BITS_TO_LOSE)
        twMessage(TW_CAMERA,
                  "twCameraPosition: INSIDE InnerRadius = %f, near = %f far = %f",
                  InnerRadius, _near, _far)
    else:
        ## Move the VRP from the BBCenter to a point outside, at a distance of eyeRadius
        _VRP = list(_VRP)
        _VRP[axis] += eyeRadius
        _near = eyeRadius-OuterRadius
        twMessage(TW_CAMERA,
                  "twCameraPosition: OUTSIDE OuterRadius = %f, near = %f far = %f",
                  OuterRadius, _near, _far)

def twZview():
    global _VPN, _VUP
    twInitView(2);
    _VPN = (0,0,-1)
    _VUP = (0,1,0)


def twYview():
    global _VPN, _VUP
    twInitView(1);
    _VPN = (0,-1,0)
    _VUP = (0,0,-1)


def twXview():
    global _VPN, _VUP
    twInitView(0);
    _VPN = (-1,0,0)
    _VUP = (0,1,0)

def twViewCommand (key, x, y):
    if key == 'X':
        twXview()
    elif key == 'Y':
        twYview()
    elif key == 'Z':
        twZview()
    else:
        print "illegal value of key for twViewCommand: ", key
    glutPostRedisplay()

def twCameraPosition():
    global _VRP, _VPN, _VUP, twMessageKinds
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if TW_CAMERA & twMessageKinds:
        twTriplePrint("VRP",_VRP)
        twTriplePrint("VPN",_VPN)
        twTriplePrint("VUP",_VUP)
    gluLookAt(_VRP[0],        _VRP[1],        _VRP[2],
              _VRP[0]+_VPN[0],_VRP[1]+_VPN[1],_VRP[2]+_VPN[2],
              _VUP[0],        _VUP[1],        _VUP[2])


def twCoordinateFrameCues():
    '''Optionally displays visual cues as to the coordinate frame.

The cues are the bounding box, the axes and the origin.  All can be enabled/disabled with the keyboard or the right mouse button menu.'''
    if Toggles[AXES]:
        twAxes()
    if Toggles[BB]:
        twDrawBoundingBox();
    if Toggles[ORIGIN]:
        twDrawOrigin();

def twCamera():
    '''Configures the camera based on the bounding box, but allows the camera to move around with keyboard callbacks and mouse movement'''
    global _near,_far
    ws = twGetWindowSize()
    glViewport(0,0,ws[0],ws[1])
    if Toggles[IMMERSE]:
        twMessage(TW_CAMERA,"immerse:  InnerRadius = %f, near=%f far=%f",
            InnerRadius, _near, _far)
    else:
        twMessage(TW_CAMERA,"back off:  OuterRadius = %f, near=%f far=%f",
                  OuterRadius, _near, _far)
    twCameraShape()
    twCameraPosition()
    twCoordinateFrameCues()

### ================================================================
### tw-geometry.cc

def twTriplePrint( name, v):
    '''prints a triple to stdout. The first argument can be used to label it'''
    print "%s=(%f,%f,%f)" % (name,v[0],v[1],v[2])

def twDot( v, w):
    '''returns the dot product of vector v and vector w.'''
    return v[0]*w[0]+v[1]*w[1]+v[2]*w[2]

def twCosAngle( v,  w):
    '''returns the cosine of the angle between vector v and vector w.
does not assume that they are normalized'''
    return twDot(v,w)/math.sqrt(twDot(v,v)*twDot(w,w))

def twRadiansToDegrees(radians):
    '''returns the argument, converted from radians to degrees'''
    return radians*180/M_PI

def twDegreesToRadians(degrees):
    '''returns the argument, converted from degrees to radians'''
    return degrees*M_PI/180

def twVectorLength( v ):
    '''returns the length of the vector v'''
    return math.sqrt(twDot(v,v))


def twVectorScale( w, k):
    '''returns a vector that is a scalar multiple of w, multiplying each
component by k.'''
    # This is a change from the C version of TW. 
    return (w[0]*k, w[1]*k, w[2]*k)

def twVectorNormalize(v):
    '''returns a new vector of unit length.  Returns with v unmodified if
v is the zero vector.  '''
    # This is a change from the C version of TW. 
    len = twVectorLength(v)
    if len == 0.0:
        return v
    else:
        return twVectorScale(v,1/len)

def twCrossProduct( v, w):
    '''returns u=v x w, the cross product of vectors v and w, in that order'''
    # This is a change from the C version of TW. 
    return [ v[1]*w[2]-v[2]*w[1],
             v[2]*w[0]-v[0]*w[2],
             v[0]*w[1]-v[1]*w[0] ]


def twVector( A, B):
    '''returns v=A-B, the vector from point B to point A'''
    # This is a change from the C version of TW. 
    return [ a-b for a,b in zip(A,B) ]

def twPoint( A, V):
    '''returns A+v, the point that is the sum of point A and vector v'''
    # This is a change from the C version of TW. 
    return [ a+v for a,v in zip(A,V) ]

def twPointDistance2( A, B):
    '''returns the squared distance between points A and B'''
    v = twVector(A,B)
    return twDot(v,v)

def twPointDistance( A, B): 
    '''returns the distance between points A and B'''
    return math.sqrt(twPointDistance2(A,B))

def twPlaneNormal( C, D, E, verify=False): 
    '''Returns the normal to a plane defined by the three points C, D, E

Find the plane normal, N, given three points on the plane, C, D, and
E. The vectors are v=D-C and w=E-C and the normal is computed as v x w.
If you give C,D,E in counterclockwise order, the normal will point out
from the front of the plane.  The result is not normalized (unit length)'''

    V = twVector(D,C)
    W = twVector(E,C)
    N = twCrossProduct(V,W)

    if verify:
        d1 = twDot(N,V)
        d2 = twDot(N,W)
        if d1 != 0 or d2 != 0 :
            twMessage(TW_GEOMETRY,"Plane Normal %s isn't perpendicular: %f %f",
                      N, d1, d2)
    return N

def twPointOnLine( P, V, t):
    '''Computes P+Vt, a point on the line defined by point P and vector V'''
    return [ p+v*t for p,v in zip(P,V) ]

class DifferentDimensions(Exception):
    def __init__(self,obj1,obj2):
        self.obj1=obj1
        self.obj2=obj2
    def __str__(self):
        return repr(self.obj1) + " and " + repr(self.obj2)

def twWeightedAverage( A, B, w ):
    '''Returns wA+(1-w)B, the weighted average of the two vectors/points'''
    if len(A) != len(B):
        print "Can't compute weighted average of object with different dimensions:",A,B
        raise DifferentDimensions(A,B)
    return [ w*a+(1-w)*b for a,b in zip(A,B) ]

### ================================================================
### Matrix multiplication

def mult3( M, V):
    """Returns M x V, where M is a 4x4 matrix and V is a triple (3x1)

    M should be a list/tuple in column major order. The last row and column of M are ignored."""
    result = [0, 0, 0]
    
    i = 0
    while i < 3:
        j = 0
        while j < 3:
            result[i] += M[j*4+i]*V[j]
            j += 1
        i += 1
    return result


### ================================================================

def twLinePlaneIntersection( P, V, Q, N):
    """Returns the intersection of line P, V with plane Q, N.

Returns true if a normal intersection, false otherwise.  See the
documentation in doc.tex.  P and V define the line; Q and N define the
plane.  Computed values are IP (the intersection point) and t, the
parameter of the intersection point.  Returns a
### tuple of (True, IP, t) or (False, False, False), if there's no
### intersection."""
    vn = twDot(V,N);
    if 0 == vn:
        return False,False,False
    w = twVector(Q,P);
    t = twDot(w,N)/vn;
    IP = twPointOnLine(P,V,t);
    return True, IP, t

def twPointInTriangle( I, P, U, V ):
    """Computes the parameters, s and t, of point I lying in the plane defined
// by point P and vectors U and V.  

The caller has to interpret the parameters to determine if I is
contained in the triangle (0<t && 0<s && s+t<1) or in the
parallelogram (0<t<1 && 0<s<1).  For documentation on the computation,
see doc.tex.  Returns false if the computation is invalid, such as the
triangle being degenerate (u or v is zero, or they are colinear."""

    W = twVector(I,P);

    uu = twDot(U,U);
    uv = twDot(U,V);
    vv = twDot(V,V);
    wu = twDot(W,U);
    wv = twDot(W,V);
    denom = uv*uv-uu*vv;

    if(0 == uu or 0 == vv ):
        print "zero length vectors"
        return False,False,False
    if(0 == denom ):
        print "Degenerate triangle:  u and v point the same way."
        return False,False,False

    s = (uv*wv-vv*wu)/denom;
    t = (uv*wu-uu*wv)/denom;
    return True, s, t
    # test code.  Comment out the "return" statement on the previous
    # line to print the computed value of W2 to compare with the
    # original W.
    if False:
        W2 = (s*U[0]+t*V[0],
              s*U[1]+t*V[1],
              s*U[2]+t*V[2])
        # these two should be equal
        twTriplePrint("W",W);
        twTriplePrint("W2",W2);
    return True;

def twLineTriangleIntersection( P, lineV, A, B, C):
    """Returns the intersection of the line P,V and the triangle ABC, if any.

Computes r, s, and t, where r is the parameter of point IP=P+r*lineV
with the plane defined by triangle A,B,C.  Also computes IP.  Returns
true if the computation is valid (that is, A,B,C define a plane and
P+r*lineV intersects the plane).  Returns a tuple of the intersection
point, the r, s and t, parameters, where r is the parameter on the
line and s,t are the triangle parameters."""
    U = twVector(B,A);
    V = twVector(C,A);
    N = twCrossProduct(U,V);

    result, IP, r = twLinePlaneIntersection(P, lineV, A, N)
    if (result == False):
        twMessage(TW_GEOMETRY,
                  "Line from (%f,%f,%f) in dir (%f,%f,%f) doesn't intersect plane through triangle (%f,%f,%f), (%f,%f,%f), (%f,%f,%f)\n" % (
            P[0],P[1],P[2],
            lineV[0],lineV[1],lineV[2],
            A[0],A[1],A[2],
            B[0],B[1],B[2],
            C[0],C[1],C[2]))
        return False
    else: 
        result2, s, t = twPointInTriangle(IP, A, U, V)
        if result2:
            return True, IP, r, s, t
        else:
            return False, False, False, False, False


def twNearestFragment(fragments, P, V):
    """Given a list of fragments (triangles) and line defined by P and V, returns the nearest fragment that is intersected.

Returns a tuple of three values: a boolean saying whether any fragment
was intersected, the Intersection Point and the parameter of the
intersection point."""

    direction = twVectorNormalize(V)
    minr = 999999999.9
    found = False;
    for frag in fragments:
        result, IP, r, s, t = twLineTriangleIntersection(P,direction,
                                                         frag[0],
                                                         frag[1],
                                                         frag[2])
        # print ("frag %d at %f",i,r);
        # negative intersections are not interesting
        if (r<0):
            continue;
        # we want to find the nearest intersection
        if (r>minr):
            continue;
        # printf("s=%f t=%f\n",s,t);
        if (0 <= s and s <= 1 and 0 <= t and t <= 1):
            found=True;
            minr = r;
            # printf("new nearest: frag=%d r=%f s=%f t=%f\n",i,r,s,t);
    r=minr;
    IP = twPointOnLine(P,direction,minr);
    return found, IP, minr

### ===============================================================
### tw-keyboard.cc

KeyCallbacksInitialized = False
twKeyCallbackArray = [ None for x in range(128) ]
twKeyCallbackDoc   = [ None for x in range(128) ]

##keyboard settings
def twKeyCallback(key, fun, doc):
    global twKeyCallbackArray, twKeyCallbackDoc
    if type(key) == type('a'):
        key = ord(key)
    if KeyCallbacksInitialized:
        twKeyCallbackArray[key] = fun;
        twKeyCallbackDoc[key] = doc;
    else:
        print "Keyboard Callbacks not yet initialized. Call this after twMainInit"

def twHelp(key, x, y):
    print '''
This software is designed to help in learning and teaching
about using OpenGL to build 3D graphics programs.
Copyright (C) 2012 Scott D. Anderson
scott.anderson@acm.org
This is free software distributed under the GNU General Public License.
'''
    for i in range(128):
        if twKeyCallbackArray[i] != None:
            if isgraph(i):
                print "%3c: %s" % (i,twKeyCallbackDoc[i])
            elif i == 32:
              print "SPC: %s" %(twKeyCallbackDoc[i])
            elif i == 9:
                print "TAB: %s" % (twKeyCallbackDoc[i])
            elif i == 27:
                print "ESC: %s" % (twKeyCallbackDoc[i])
            else:
                print "^%c : %s" % (i+64,twKeyCallbackDoc[i])

def twQuit(key, x, y):
    sys.exit(0)

def twStopAndRefresh(key, x, y):
    glutIdleFunc(None)
    glutPostRedisplay()

def twPause(key, x, y):
    glutIdleFunc(None)

def twAxesToggle(key, x, y):
    global Toggles
    Toggles[AXES] = not Toggles[AXES]
    glutPostRedisplay()

def twBoundingBoxToggle(key, x, y):
    global Toggles
    Toggles[BB] = not Toggles[BB]
    glutPostRedisplay()

def twOriginToggle(key, x, y):
    global Toggles
    Toggles[ORIGIN] = not Toggles[ORIGIN]
    glutPostRedisplay()

def twLightingToggle(key, x, y):
    global Toggles
    Toggles[LIGHTING] = not Toggles[LIGHTING]
    glutPostRedisplay()

def twShadingToggle(key, x, y):
    global Toggles
    Toggles[SMOOTH] = not Toggles[SMOOTH]
    glutPostRedisplay()

def twReset (key, x, y):
    glutIdleFunc(None)
    twZview()
    glutPostRedisplay()

## does a 10 degree rotation around y axis
def twRotViewY(key, x, y):
    yAxis = (0,1,0)
    twRotateViewpoint(10,yAxis)

## does a 10 degree rotation around x axis
def twRotViewX(key, x, y):
    xAxis = (1,0,0)
    twRotateViewpoint(10,xAxis)

## does a 10 degree pan (yaw) around y axis
def twPanView(key, x, y):
    yAxis = (0,1,0)
    twRotateVPN(10,yAxis)

## Zoom in by the given number of degrees, relative to current
## FieldOfView.  If the field of view would drop to zero or less, it
## returns, leaving the field of view unchanged.  If the field of view
def twZoom(degrees):
    global _FieldOfView
    newFOV = _FieldOfView - degrees;
    if newFOV <= 0: return;
    _FieldOfView = newFOV
    glutPostRedisplay()

def twZoom1():
    twZoom(1)

def twStartZooming(key, x, y):
    glutIdleFunc(twZoom1)

def twNextFrameCallback(key, x, y):
    twNextFrame()

def twKeyboardCallback (key, x, y):
    global twKeyCallbackArray
    keycode = ord(key)
    if keycode > 128:
        return
    fun = twKeyCallbackArray[keycode];
    if fun == None:
        print "No callback for %c (%d)" %(key,keycode)
        return
    fun(key,x,y)

def twSaveFrame(fname, verbose=False):
    """Saves the current framebuffer (viewport) to the given filename, using twReadFramebuffer()"""
    img = twReadFramebuffer()
    if img == None:
        return
    fp = open(fname,"w")
    if (not fp):
        print "Unable to open file '%s'" % (fname)
        return
    fp.writelines("P6\n")
    fp.writelines("%d %d\n" % (img.width, img.height))
    fp.writelines("255\n")     # max value
    fp.write(img.data)
    fp.close()
    if verbose: 
        print "Saved image (%d x %d) PPM image to %s"%(img.width,img.height,fname)

def twReadFramebuffer():
    """Reads and returns the entire framebuffer (really, the viewport) as an twImage object

"""
    x, y, width, height = glGetIntegerv(GL_VIEWPORT)
    data = ''
    for row in range(height):
        rowdata = glReadPixels(0,height-row,width,1, GL_RGB, GL_UNSIGNED_BYTE)
        if type(rowdata) == type(data):
            data += rowdata
        else:
            # there's a more efficient way...
            str = ''
            for row in rowdata:
                for pixel in row:
                    for byte in pixel:
                        str += chr(byte)
            data += str
    if len(data) != width * height * 3:
        print "data is not correct length: %d versus %d=(%d,%d,%d); not returning it" % (len(data), width * height * 3, width, height, 3)
        return None
    else:
        return twImage(width,height,255,data)

frameNumber = 1

def twSave(key, x, y):
    global frameNumber;
    file = "saved-frame%03d.ppm" % (frameNumber)
    frameNumber += 1
    twSaveFrame(file, False)

def twKeyInit():
    global twKeyCallbackArray, KeyCallbacksInitialized
    for i in range(128): twKeyCallbackArray[i] = None
    KeyCallbacksInitialized = True;
    twKeyCallback(27,  twQuit, "Quit");
    twKeyCallback(32,  twStopAndRefresh, "Stop animation, if any, and refresh");
    twKeyCallback('+', twSpinCommand, "double spin step");
    twKeyCallback('-', twSpinCommand, "halve spin step");
    twKeyCallback('a', twAxesToggle, "Toggle Axes");
    twKeyCallback('b', twBoundingBoxToggle, "Toggle Bounding Box");
    twKeyCallback('l', twLightingToggle, "Toggle Lighting");
    twKeyCallback('o', twOriginToggle, "Toggle Origin");
    twKeyCallback('s', twShadingToggle, "Toggle Smooth Shading");
    twKeyCallback('q', twQuit, "Quit");
    twKeyCallback('p', twPause, "Pause animation");
    twKeyCallback('r', twReset, "Reset to original screen");
    twKeyCallback('n', twNextFrameCallback, "next frame of animation");
    twKeyCallback('x', twSpinCommand, "Spin around the x axis");
    twKeyCallback('y', twSpinCommand, "Spin around the y axis");
    twKeyCallback('z', twSpinCommand, "Spin around the z axis");
    twKeyCallback('X', twViewCommand, "View from positive X axis");
    twKeyCallback('Y', twViewCommand, "View from positive Y axis");
    twKeyCallback('Z', twViewCommand, "View from positive Z axis");
    ## twKeyCallback('s', twRotViewY, "10 degrees around y");
    ## twKeyCallback('t', twRotViewX, "10 degrees around x");
    ## twKeyCallback('P', twPanView, "10 degrees pan around y");
    twKeyCallback('?', twHelp,"Help");
    twKeyCallback('i', twStartZooming, "start zooming in");
    twKeyCallback('S', twSave, "save frame")

### ===============================================================
### tw-textures

def twDrawUnitSquare(xSteps, zSteps):
    '''1*1 unit square drawn with triangle_strips in the Y=0 plane.  

The square's normal points in +Y direction.  The square is drawn as
xSteps x zSteps little squares, each with its own texture
coordinate. The texture coordinates are all 0 or 1, so you're getting
repetitions of the texture.  Use Bezier surfaces for more flexibility.
Actually, it uses triangle strip, so there are two triangles in each
little cell.  Allows for lighting effects with textures.'''

    dx = 1.0/xSteps;
    dz = 1.0/zSteps;
    glNormal3f(0,1,0);
    for i in range(int(xSteps)):
        glBegin(GL_TRIANGLE_STRIP);
        for j in range(int(zSteps)+1):
            if j&1:
                glTexCoord2f(1,0) 
            else:
                glTexCoord2f(0,0);
            # could optimize this by summing instead of multiplying
            glVertex3f(dx*i,0,dz*j);
            if j&1:
                glTexCoord2f(1,1); 
            else:
                glTexCoord2f(0,1);
            glVertex3f(dx*(i+1),0,dz*j);
        glEnd();

### ================================================================
# Checkerboard Textures.  The checkerboard texture is an array of
# unsigned 8-bit values (GLubyte) which are interpreted as a grayscale
# value.  We only use 255 and 0, namely white and black, respectively.

def twMakeCheckTexture(width,height):
    '''Creates, if necessary, a checkerboard of the given
dimensions, and returns it.'''
    ## How to allocate an array/list/tuple in Python?  Here's one way,
    ## and this one computes the values as you go.  It uses a "clever"
    ## ternary operator in Python: X if C else Y, which returns either
    ## X or Y, depending on C, the condition.
    powers = [ 1 << p for p in range(1,31) ]
    if width not in powers or height not in powers:
        print "width and height must be a power of two"
        return
    # The following makes each row at least four bytes long, which
    # byte-aligns the data
    if width == 2:
        width = 4
    flag = [ [ 255 if (i+j)&1 else 0 
               for i in range(width) ]
             for j in range(height) ]
    return flag

### ================================================================

def twMakeGrays(width,height):
    '''Make a steadily brightening luminance texture of the given dimensions'''
    length = width*height
    ## linearly interpolate from black to white, give 1D result
    if False:
        bytes = [ int(255*(i/float(length-1))) 
                  for i in range(0,length) ]
    # New improved code, borrowing from checkerboard
    powers = [ 1 << p for p in range(1,31) ]
    if width not in powers or height not in powers:
        print "width and height must be a power of two"
        return
    # The following makes each row at least four bytes long, which
    # byte-aligns the data
    array_width = width if width > 2 else 4
    max = float(width * height - 1)
    flag = [ [ int(255*(j*width+i)/max) for i in range(array_width) ]
             for j in range(height) ]
    return flag

## ======================================================================
## US Flag texture.  It's computed and sent down the graphics pipeline
## when you call twUSFlag().  This caches the flag, so it's not
## inefficient to call more than once, but you should still consider
## using texture binding.

## We use RGBA to avoid alignment issues.  That is, this is an array of
## four-byte values, where each bytes is a color dimension: red, green,
## blue and alpha.  Because they are all four bytes, we don't have to
## worry about how C aligns these things in memory.

def setRGB(texture, row, col, RR, GG, BB):
    '''set an element of the texture to a particular RGBA color value'''
    texture[row][col][0] = RR;
    texture[row][col][1] = GG;
    texture[row][col][2] = BB;
    texture[row][col][3] = 255;

def setStar(flag, row, col):
    '''Each star is in a 5x5 box.  With no anti-aliasing, pixels are
either white or blue.  The args are the offset within the flag array.

The star looks like:
..W..
WWWWW
.WWW.
WW.WW
.....
'''
    ## Assume the flag is all blue, so all we do is set elts to white
    def setWhite(row,col):
        setRGB(flag,row,col,255,255,255)

    setWhite(row,col+2)
    for i in [0, 1, 2, 3, 4]:
        setWhite(row+1,col+i)
    for i in [1, 2, 3]:
        setWhite(row+2,col+i)
    for i in [0, 1, 3, 4]:
        setWhite(row+3,col+i)

def makeUSFlag(flagWidth, flagHeight, stripeHeight):
    '''This creates a new flag each time, based on the supplied
dimensions, which are in texels.  The flagWidth and flagHeight should
be powers of 2, since they are used for the texture array dimensions.
Given that the star is hard-coded to be 5x5 texels, it really only
makes sense to use 256,128,8, but this is at least a start on a more
abstract definition.

The flag itself has max texture coordinates of (h,w) where

h = stripeHeight*13/flagHeight = 0.8125
w = 1.9*h * flagHeight/flagWidth = 0.77'''
    # See http://cs.wellesley.edu/~cs307/flagspec.htm
    print "making US flag"
    height = stripeHeight*13;  # the flag is 13 stripes high
    width  = int(height*1.9);  # the flag's aspect ratio is 1.9
    if height > flagHeight or width > flagWidth:
        print "can't make a flag with these specifications:", flagWidth, flagHeight, stripeHeight
        return
    unionHeight = 7*stripeHeight; # the union is 7 stripes high
    # fly of the union is 0.76
    unionWidth  = int(unionHeight*(0.76/(7.0/13.0)));
    starSize = 5;               # each star's size, in texels

    ## initial every texel to 50% solid gray
    flag = [ [ [ 128, 128, 128, 255 ] for j in range(flagWidth) ]
             for i in range(flagHeight) ]

    ## 7 red stripes, 
    for i in range(7):
        for offset in range(stripeHeight):
            row=i*2*stripeHeight+offset # *2 because every other stripe
            for col in range(width):
                setRGB(flag,row,col, 255,0,0); # set to RED
    ## 6 white stripes, 
    for i in range(6):
        for offset in range(stripeHeight):
            row=(i*2+1)*stripeHeight+offset # *2 because every other stripe
            for col in range(width):
                setRGB(flag,row,col, 255,255,255); # set to WHITE
    ## Fill in the union with blue.
    for row in range(unionHeight):
        for col in range(unionWidth):
            setRGB(flag,row,col, 0,0,255); # set to BLUE
    ## 5 rows of 6 stars.  There's one blue border row and col,
    ## one row between star rows and one col between star cols
    for i in range(5):
        for j in range(6):
            setStar(flag, 
                    i*2*(starSize+1)+1,
                    j*2*(starSize+2)+1)
    ## 4 rows of 5 stars
    for i in range(4):
        for j in range(5):
            setStar(flag,
                    (i*2+1)*(starSize+1)+1,
                    (j*2+1)*(starSize+2)+1)
    return flag

def printUSFlag(flag,rows,cols):
    '''We don't really need this, but it's useful to show the flag
    texture.  Only prints part of the flag.'''
    # this implementation is not space-efficient, but I don't care
    def colorchar(texel):
        if texel == [255, 0, 0, 255]:
            return "R"
        elif texel == [255, 255, 255, 255]:
            return "W"
        elif texel == [0, 0, 255, 255]:
            return "B"
        elif texel == [128, 128, 128, 255]:
            return "."
        else:
            print "Unknown texel: ", texel
            return
        
    for row in flag[:rows]:
        line = ""
        for texel in row:
            line += colorchar(texel)
        print line[:cols]        # a bit shorter

USFlagArray = None

def twUSFlag():
    '''Builds the USFlag, if necessary, and sends it down the pipeline'''
    global USFlagArray
    USFlagWidth  = 256
    USFlagHeight = 128
    USFlagStripeHeight = 8

    if USFlagArray == None:
        USFlagArray = makeUSFlag(USFlagWidth,USFlagHeight,USFlagStripeHeight)

    ## Finally done computing the flag array.  Now time to send it down
    ## the graphics pipeline.  
    glTexImage2D(GL_TEXTURE_2D, 0, 3, USFlagWidth, USFlagHeight, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, USFlagArray)

_powers2 = [ 1 << i for i in range(17) ]

def twPow2(x):
    '''True iff x is a power of two less than or equal to 2^16'''
    return x in _powers2

class twImage():
    def __init__(self,width,height,maxval,data):
        self.width = width
        self.height = height
        self.maxval = maxval
        self.data = data
    # I'm too lazy to define getters and setters that don't do
    # anything interesting

def readNonCommentLine(file):
    """returns the first line that doesn't start with a #."""
    while True:
        line = file.readline()
        if line[0] != '#':
            return line

def twLoadPPMimage(ppm_filename, verbose=False):
    '''Load an image from a PPM file and return it

The returned value is a data structure with the following attributes:
   width   of the image, in pixels,
   height  of the image, in pixels,
   maxval  of the image, the number of distinct colors,
   data    an array of the pixel values. 

You can send this image down the OpenGL pipeline by 

    img = twLoadPPMimage(filename,False)
    if twPow2(img.width) and twPow2(img.height):
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
        glTexImage2D(GL_TEXTURE_2D, 0, 3, img.width, img.height, 0,
                     GL_RGB, GL_UNSIGNED_BYTE, img.data)

This function doesn't handle all PPM files; only type P6; see "man
ppm" for the exact file format.  Ideally, we should use PIL, but
that's broken in Python 2.6 under Mac OS X.
'''
    if verbose:
        print 'loading texture from',ppm_filename
    try:
        FILE = open(ppm_filename,'r')
    except IOError, e:
        print 'Cannot read image file ', ppm_filename
        print 'Did you set TWLOADPATH?  Did you call twPathname()?'
        # try to be more helpful, by using the exception object, but then
        # we re-raise the exception, and let the debugger handle it
        try:
            (errno, strerror) = e
            print "I/O error({0}): {1}".format(errno, strerror)
            raise e             
        except:
            raise e
    ## Finally, get some real work done

    magic = FILE.readline()
    if magic != 'P6\n':
        print 'Sorry, I can\'t read file format for ', ppm_filename, '; it\'s not P6:',magic
        return
    dimens = readNonCommentLine(FILE)
    width, height = map(int, dimens.split())
    maxval = int(readNonCommentLine(FILE))
    filedata = FILE.read()
    expectedlen = width*height*3
    if len(filedata) < expectedlen:
        print "PPM file %s doesn't seem to have enough data: %d x %d x 3 = %d < %d" % (
            ppm_filename, width, height, expectedlen, len(filedata))
    if verbose:
        print 'PPM image file %s has dimensions %d by %d with maxval %d' % (
          ppm_filename, width, height, maxval)
    return twImage(width, height, maxval, filedata)

def twPPM_Tex2D(filename):
    '''Loads an image file (PPM format P6) and uses it as an OpenGL texture.  

Calls glTexImage2D.  The image filename should be ready to load,
meaning you've already called twPathname on the filename if
desired.'''
    img = twLoadPPMimage(filename)

    if twPow2(img.width) and twPow2(img.height):
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, img.width, img.height, 0, 
                     GL_RGB, GL_UNSIGNED_BYTE, img.data)
    else:
        print "Could not use image %s as texture:  dimensions are not powers of two:  %d x %d" % (filename, img.width, img.height)
    return img

def twLoadTexture(textureNumber, filename):
    '''uses image file as a texture (see twPPM_Tex2D) and binds to it to the given textureNumber.'''
    glBindTexture(GL_TEXTURE_2D, int(textureNumber))
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    twPPM_Tex2D(filename)

### ================================================================
### Bezier curves and surfaces

def twDrawBezierCurve(cp,steps,mode=GL_LINE):
    """Draw the complete Bezier curve using 'steps' linear segments

Default mode is GL_LINE, but could also be GL_POINT"""
    # glMap1f(target, u_min, u_max, stride, order, point_array);
    glMap1f(GL_MAP1_VERTEX_3, 0, 1, cp);
    glEnable(GL_MAP1_VERTEX_3);
    glMapGrid1f(steps,0,1);
    glEvalMesh1(mode,0,steps);


def twDrawBezierControlPoints(cp):
    """Graphically display the control points of a curve or surface.

Each point is drawn in a different color.  The colors are
systematically chose using color dimensions.  For 1D curves, we map
the parameter onto the blue dimension, so the first control point is
yellow (1,1,0) and the last is white (1,1,1). For 2D surfaces, we map
the s and t dimensions onto the red and green color dimensions, so
that the upper left CP will be blue (0,0,1), the upper right CP will
be magenta (1,0,1), the lower left CP will be cyan (0,1,1) and the
lower right CP will be white (1,1,1).  Draws using current point size;
Use glPointSize() to make the points bigger/smaller."""

    ## so that the lighting, current color, point size and line width are not changed:
    glPushAttrib(GL_ALL_ATTRIB_BITS);
    glDisable(GL_LIGHTING);

    shapetuple = shape(cp)
    if len(shapetuple) == 2:
        # 1D curve
        num_cp = shapetuple[0]
        glBegin(GL_POINTS)
        for i in range(num_cp):
            u = i/float(num_cp-1)
            glColor3f( 0, 0, u )
            glVertex3fv(cp[i])
        glEnd()
    elif len(shapetuple) == 3:
        # 2D surface
        num_cp_u = shapetuple[0]
        num_cp_v = shapetuple[1]
        glBegin(GL_POINTS)
        for i in range(num_cp_u):
            u = i/float(num_cp_u-1)
            for j in range(num_cp_v):
                v = j/float(num_cp_v-1)
                glColor3f(u,v,1)
                glVertex3fv(cp[i][j])
        glEnd()
    else: 
        print "can't handle this shape for control points: ", shapetuple
    glPopAttrib()


def twDrawBezierSurface(cp, u_steps, v_steps, mode=GL_FILL):
    """Draw the whole Bezier surface, default mode is GL_FILL

Assumes each element is a triple, so you don't need to worry about
strides."""

    umin = 0
    umax = 1
    vmin = 0
    vmax = 1

    glMap2f(GL_MAP2_VERTEX_3, umin, umax, vmin, vmax, cp);
    glEnable(GL_MAP2_VERTEX_3);
    
    glMapGrid2f(u_steps,0,1,
                v_steps,0,1);
    glEvalMesh2( mode, 0, u_steps, 0, v_steps )


def twDrawBezierSurfaceTextured(cp, tcp, u_steps, v_steps, mode=GL_FILL):
    """Draw the whole Bezier surface with texture coordinates.  

Assumes each element is a triple, so you don't need to worry about
strides.  Assumes GL_FILL mode. Assumes the texture coordinates are in
a 2x2x2 array."""

    umin = 0
    umax = 1
    vmin = 0
    vmax = 1

    glMap2f(GL_MAP2_VERTEX_3, umin, umax, vmin, vmax, cp);
    glMap2f(GL_MAP2_TEXTURE_COORD_2, umin, umax, vmin, vmax, tcp);
    glEnable(GL_MAP2_VERTEX_3);
    glEnable(GL_MAP2_TEXTURE_COORD_2);
    
    glMapGrid2f(u_steps,0,1,
                v_steps,0,1);
    glEvalMesh2( mode, 0, u_steps, 0, v_steps );


### ================================================================
### tw-fonts
### Adapted from code by Nate Robins for tw 

TWFontStyle = GLUT_BITMAP_8_BY_13; # current font

def twSetFont(name, size):
    if name == "helvetica":
        if size == 12:
            TWFontStyle = GLUT_BITMAP_HELVETICA_12;
        elif size == 18:
            TWFontStyle = GLUT_BITMAP_HELVETICA_18;
        else:
            twMessage(TW_FONTS,"Warning, no helvetica font at size %d, using 12\n",size);
            TWFontStyle = GLUT_BITMAP_HELVETICA_12;
    elif name == "times roman":
        if size == 10:
            TWFontStyle = GLUT_BITMAP_TIMES_ROMAN_10;
        elif size == 24:
            TWFontStyle = GLUT_BITMAP_TIMES_ROMAN_24;
        else:
            twMessage(TW_FONTS,"Warning, no times roman font at size %d, using 10\n",size);
            TWFontStyle = GLUT_BITMAP_TIMES_ROMAN_10;
    elif name == "8x13":
        TWFontStyle = GLUT_BITMAP_8_BY_13;
    elif name == "9x15":
        TWFontStyle = GLUT_BITMAP_9_BY_15;
    else:
        twMessage(TW_FONTS,"Warning:  no font matches %s; using default 8x13\n",name);
        TWFontStyle = GLUT_BITMAP_8_BY_13;

def twDrawString2(x, y, string):
    '''puts a string at location x, y on the window, where x and y are
    in window (raster) coordinates'''
    twDrawString(x,y,0,string)

def twDrawString(x, y, z, string):
    '''puts a string at location x, y, z on the image, where x,y,z are
    in window coordinates'''
    glRasterPos3f(x, y, z);
    for s in string:
        glutBitmapCharacter(TWFontStyle, ord(s))

### ================================================================
### tw-objects.cc  Definitions of new tw objects 

### Vertex array for a unit twBarn (dimensions 1*1*1) 

### Should the following be a parameter of twSolidBarn, instead?
BarnShoulderHeight = 0.7

twBarn = (
  (0,0,0),                      # 0, left, bottom, front 
  (1,0,0),                      # 1, right, bottom, front 
  (1,BarnShoulderHeight,0),     # 2, right front shoulder
  (0.5,1,0),                    # 3, ridge, front 
  (0,BarnShoulderHeight,0),     # 4, left front shoulder
  (0,0,-1),                     # 5, echo of 0
  (1,0,-1),                     # 6, echo of 1
  (1,BarnShoulderHeight,-1),    # 7, echo of 2
  (0.5,1,-1),                   # 8, echo of 3
  (0,BarnShoulderHeight,-1),    # 9, echo of 4
  )

def twSolidBarn(endColor, sideColor, roofColor, specular=0.1, shininess=10):
    '''Draws a solid unit barn with colors specified for the ends
(front and back), sides and roof.  These use twColor, so it also works
with lighting.  The default specularity and shininess are 0.1 and 10,
respectively for all surfaces.  The lower left front of the barn is
anchored at (0,0,0); drawn in +x,+y,-z direction.  The height of the
side of the barn is 0.7.  Normals are also defined for all surfaces.'''
    twColor(endColor,specular,shininess)
    glNormal3f(0,0,1)
    glBegin(GL_POLYGON);        # front 
    if True:
        glVertex3fv(twBarn[0]);
        glVertex3fv(twBarn[1]);
        glVertex3fv(twBarn[2]);
        glVertex3fv(twBarn[3]);
        glVertex3fv(twBarn[4]);
    glEnd();
    glNormal3f(0,0,-1);
    glBegin(GL_POLYGON);        # back 
    if True:
        glVertex3fv(twBarn[5]);
        glVertex3fv(twBarn[9]);
        glVertex3fv(twBarn[8]);
        glVertex3fv(twBarn[7]);
        glVertex3fv(twBarn[6]);
    glEnd();
    twColor(sideColor,specular,shininess);
    glNormal3f(-1,0,0);
    glBegin(GL_POLYGON);        # left side 
    if True:
      glVertex3fv(twBarn[0]);
      glVertex3fv(twBarn[4]);
      glVertex3fv(twBarn[9]);
      glVertex3fv(twBarn[5]);
    glEnd();
    glNormal3f(1,0,0);
    glBegin(GL_POLYGON);        # right side 
    if True:
      glVertex3fv(twBarn[1]);
      glVertex3fv(twBarn[6]);
      glVertex3fv(twBarn[7]);
      glVertex3fv(twBarn[2]);
    glEnd();
    twColor(roofColor,specular,shininess);
    ## These perpendicular vectors aren't normalized.  I'm using the
    ## perp idea as found in Hill's graphics book, namely to find the
    ## perpendicular to a vector in the z=0 plane by swapping x and y
    ## and negating the x coordinate
    glNormal3f(BarnShoulderHeight-1,0.5,0);
    glBegin(GL_POLYGON);        # left side roof 
    if True:
      glVertex3fv(twBarn[4]);
      glVertex3fv(twBarn[3]);
      glVertex3fv(twBarn[8]);
      glVertex3fv(twBarn[9]);
    glEnd();
    glNormal3f(1-BarnShoulderHeight,0.5,0);
    glBegin(GL_POLYGON);        # right side roof 
    if True:
      glVertex3fv(twBarn[2]);
      glVertex3fv(twBarn[7]);
      glVertex3fv(twBarn[8]);
      glVertex3fv(twBarn[3]);
    glEnd();

def twWireBarn(xColor, yColor, zColor):
    '''Draws a wireframe barn, defined like the solid barn, but wire.
Draws the lines parallel to x in xColor, y in yColor and z in zColor.
Diagonals of the roof are drawn in xColor.'''
    twColor(xColor,0,0);
    glBegin(GL_LINES);
    if True:
        # front horizontals
        glVertex3fv(twBarn[0]);
        glVertex3fv(twBarn[1]);
        glVertex3fv(twBarn[2]);
        glVertex3fv(twBarn[3]);
        glVertex3fv(twBarn[2]);
        glVertex3fv(twBarn[4]);
        glVertex3fv(twBarn[3]);
        glVertex3fv(twBarn[4]);
        # back horizonals
        glVertex3fv(twBarn[0+5]);
        glVertex3fv(twBarn[1+5]);
        glVertex3fv(twBarn[2+5]);
        glVertex3fv(twBarn[3+5]);
        glVertex3fv(twBarn[2+5]);
        glVertex3fv(twBarn[4+5]);
        glVertex3fv(twBarn[3+5]);
        glVertex3fv(twBarn[4+5]);
    glEnd();
    twColor(yColor,0,0);
    glBegin(GL_LINES);
    if True:
        # front
        glVertex3fv(twBarn[0]);
        glVertex3fv(twBarn[4]);
        glVertex3fv(twBarn[1]);
        glVertex3fv(twBarn[2]);
        # back
        glVertex3fv(twBarn[0+5]);
        glVertex3fv(twBarn[4+5]);
        glVertex3fv(twBarn[1+5]);
        glVertex3fv(twBarn[2+5]);
    glEnd();
    twColor(zColor,0,0);
    glBegin(GL_LINES);
    if True:
        glVertex3fv(twBarn[0]);
        glVertex3fv(twBarn[0+5]);
        glVertex3fv(twBarn[1]);
        glVertex3fv(twBarn[1+5]);
        glVertex3fv(twBarn[2]);
        glVertex3fv(twBarn[2+5]);
        glVertex3fv(twBarn[3]);
        glVertex3fv(twBarn[3+5]);
        glVertex3fv(twBarn[4]);
        glVertex3fv(twBarn[4+5]);
    glEnd();

### It isn't particularly efficient to allocate some memory just to use it
### and discard it.  It would be cleaner to allocate the memory once for
### each disk at the beginning of the program, and use the quadrics during
### the display function, but that's more awkward to code. The following
### function trades efficiency for convenience. */

def twDisk(radius, slices):
    '''Creates a disk of given radius with the specified number of slices.
This is just a wrapper for gluDisk, so it lies in the z=0 plane, with
the center of the disk at the origin, and the normal vector is +z. Only
uses one loop, so the subdivision really is like a pizza. '''
    tmpquad = gluNewQuadric();
    if tmpquad == 0:
        print "Can't allocate another quadric"
    else:
        gluQuadricDrawStyle(tmpquad,GL_POLYGON);
        gluDisk(tmpquad,0,radius,slices,1);
        gluDeleteQuadric(tmpquad);

### Similar efficiency comments as for twDisk.

def twCylinder(base, top, height, slices, stacks):
    '''Creates a cylinder with the given radii for the base and the top, and
the given height.  The cylinder is drawn solid (as opposed to wire
frame) and has normal vectors generated. The cylinder does not have
ends; for that, use twTube.

The cylinder has the base in the z=0 plane and extends along the
positive z axis.  This function is a wrapper for gluCylinder, so see
the man page of that for more info. You probably want to use 1 for
"stacks," since there's no curvature along the axis of the cylinder.'''
    myCylinder = gluNewQuadric();
    if myCylinder == 0:
        print "Can't allocate another quadric"
    else:
        gluQuadricDrawStyle(myCylinder,GL_POLYGON)
        gluQuadricNormals(myCylinder,GL_SMOOTH)
        gluCylinder(myCylinder,base,top,height,slices,stacks)
        gluDeleteQuadric(myCylinder)

def twTube(base, top, height, slices, stacks):
    '''Like twCylinder, but draws the ends as well, using twDisk, so
it's a closed tube, not an open one.'''
    glPushMatrix();
    # must flip sides so we see the correct side for shading
    glRotatef(180,1,0,0); 
    twDisk(base,slices);
    glPopMatrix();
    twCylinder(base,top,height,slices,stacks);
    # translate length of cylinder to draw bottom
    glPushMatrix();
    glTranslatef(0,0,height); 
    twDisk(top,slices);
    glPopMatrix();

def twSolidCylinder(top, base, height, slices, stacks):
    '''Like twCylinder, but draws the cylinder with closed ends; drawn from
center in x and z; oriented so that it is drawn downward from y = 0.  This
function is deprecated; use twTube instead.'''
    glPushMatrix();
    glRotatef(90,1,0,0);
    glPushMatrix();
    # must flip sides so we see the correct side for shading
    glRotatef(180,1,0,0); 
    twDisk(top,slices);
    glPopMatrix();
    twCylinder(top,base,height,slices,stacks);
    # translate length of cylinder to draw bottom
    glTranslatef(0,0,height); 
    twDisk(base,slices);
    glPopMatrix();

def twWireGlobe(radius, stacks, slices):
    """Draw a texture-mappable sphere or globe.  

's' is the longitude (slices) and 't' goes from north pole to south
pole (stacks)."""
    ## i is the longitude counter, j is the latitude counter i goes
    ## from 0-slices while longitude goes from 0 to 2PI j goes from
    ## 0-stacks while latitude goes from -PI to +PI, where 0,0 is on
    ## the positive x axis and negative latitude is the southern
    ## hemisphere (negative y).  we generate vertices in groups of 4,
    ## the lower (lo) one and the higher (hi) one, and the previous
    ## pair.  Each stack is a pair of circles. The radius of each
    ## circle is determined by the latitude, and is just the cosine of
    ## the latitude.
    lat_lo = -M_PI/2;                # latitude of south pole 
    cos_lat_lo = 0;                  # radius at that latitude 
    ny_lo = -1;                      # same as sin_lat_lo
    for j in range(1,stacks+1):
        # j corresponds
        lat_hi = (M_PI * j)/stacks - M_PI/2.0;
        ny_hi = math.sin(lat_hi);
        cos_lat_hi = math.cos(lat_hi);
        prev = False
        glBegin(GL_LINES);
        for i in range(0,slices+1):
            longitude = (2*M_PI * i)/slices;
            cos_longitude = math.cos(longitude);
            sin_longitude = math.sin(longitude);
            nx = cos_lat_lo*cos_longitude;
            nz = cos_lat_lo*sin_longitude;
            x_lo=nx*radius;
            y_lo=ny_lo*radius;
            z_lo=nz*radius;

            glVertex3f(x_lo,y_lo,z_lo);

            nx = cos_lat_hi*cos_longitude;
            nz = cos_lat_hi*sin_longitude;
            x_hi=nx*radius;
            y_hi=ny_hi*radius;
            z_hi=nz*radius;

            glVertex3f(x_hi,y_hi,z_hi);

            if prev:
                glVertex3f(oldx_lo,oldy_lo,oldz_lo);
                glVertex3f(x_lo,y_lo,z_lo);
            
                glVertex3f(oldx_hi,oldy_hi,oldz_hi);
                glVertex3f(x_hi,y_hi,z_hi);

            # copy values to "old" values, to avoid having to re-compute them
            oldx_lo=x_lo;
            oldx_hi=x_hi;
            oldy_lo=y_lo;
            oldy_hi=y_hi;
            oldz_lo=z_lo;
            oldz_hi=z_hi;
            prev = True
        glEnd();
        lat_lo = lat_hi;
        ny_lo = ny_hi;
        cos_lat_lo = cos_lat_hi;

def twSolidGlobe(radius, stacks, slices):
    """Draw a texture-mappable sphere or globe.  

's' is the longitude (slices) and 't' goes from north pole to south
pole (stacks)."""
    ## i is the longitude counter, j is the latitude counter
    ## i goes from 0-slices while longitude goes from 0 to 2PI
    ## j goes from 0-stacks while latitude goes from -PI to +PI,
    ## where 0,0 is on the positive x axis and negative latitude
    ## is the southern hemisphere (negative y).
    lat_lo = -M_PI/2.0;                # latitude of south pole
    cos_lat_lo = 0;                    # radius at that latitude 
    ny_lo = -1;                        # same as sin_lat_lo 
    for j in range(1,stacks+1):
        lat_hi = (M_PI * j)/stacks - M_PI/2.0;
        ny_hi = math.sin(lat_hi);
        cos_lat_hi = math.cos(lat_hi);
        glBegin(GL_QUAD_STRIP);
        for i in range(0,slices+1):
            longitude = (2*M_PI * i)/slices;
            cos_longitude = math.cos(longitude);
            sin_longitude = math.sin(longitude);
            nx = cos_lat_lo*cos_longitude;
            nz = cos_lat_lo*sin_longitude;
            ## The 1- on the s is because we go from east to west around
            ## the globe, so we want the right hand edge of our texture to
            ## map to the eastern silhouette, and so forth.  The 1- on the
            ## t is so that the top of the image is at the north pole.
            glTexCoord2f(1-longitude/(2*M_PI),1-lat_lo/M_PI+0.5);
            glNormal3f(nx,ny_lo,nz);
            glVertex3f(nx*radius,ny_lo*radius,nz*radius);
            nx = cos_lat_hi*cos_longitude;
            nz = cos_lat_hi*sin_longitude;
            glTexCoord2f(1-longitude/(2*M_PI),1-lat_hi/M_PI+0.5);
            glNormal3f(nx,ny_hi,nz);
            glVertex3f(nx*radius,ny_hi*radius,nz*radius);
        glEnd();
        lat_lo = lat_hi;
        ny_lo = ny_hi;
        cos_lat_lo = cos_lat_hi;

def twTextureSphere(radius=1,
                    slices=30,
                    stacks=30,
                    texture=True,
                    wireframe=False):
    '''Draw a texture-mapped sphere.

The caller should load/bind the texture.  Both 'texture' and 'wire' are
boolean, to request that texturemapping be turned off (false) or that
wireframe be turned on (true).'''
    if wireframe:
        twWireGlobe(radius,stacks,slices)
    else:
        if texture:
            glEnable(GL_TEXTURE_2D)
        else:
            glDisable(GL_TEXTURE_2D)
        twSolidGlobe(radius,stacks,slices)

def twTeddyBear():
    '''Draws a solid teddybear within a 1*1*1 box, with reference
    point at lower left front and the y-axis parallel to the teddy
    bear's non-existent spine.'''

    lightBrown = (0.8,0.5,0.3)
    darkBrown  = (0.7,0.4,0.2)
    black      = (0.0,0.0,0.0)

    glPushMatrix();
    twColor(lightBrown,0,0);
    glScalef(0.1,0.1,0.1);
    glTranslated(0,3,0);
    glPushMatrix();
    glTranslated(-0.6,0.7,0.2);
    glScaled(1,1,0.5);
    glutSolidSphere(0.4,20,20); # left ear
    glPopMatrix();
    glPushMatrix();
    glTranslated(0.6,0.7,0.2);
    glScaled(1,1,0.5);
    glutSolidSphere(0.4,20,20); # right ear
    glPopMatrix();

    # draw head, slightly darker brown
    twColor(darkBrown,0,0);     # dark brown
    glPushMatrix();
    glutSolidSphere(1,30,30);
    glTranslated(-0.25,0.1,0.9);
    twColor(black,1,64);         # shiny black
    glutSolidSphere(0.12,20,20); # left eye
    glTranslated(0.5,0,0);
    glutSolidSphere(0.12,20,20); # right eye
    glTranslated(-0.25,-0.4,0);
    glutSolidSphere(0.2,10,10); # nose
    glPopMatrix();
  
    # draw body
    twColor(lightBrown,0,0);    # light brown again
    glTranslated(0,-3.8,0);
    glPushMatrix();
    glScaled(1.3,2,1);
    glutSolidSphere(1.5,30,30); # body
    glPopMatrix();
  
    # legs and arms are in darker brown
    twColor(darkBrown,0,0);     # dark brown
    # draw right leg
    glTranslated(0.9,-1.9,0);
    glPushMatrix();
    glRotated(35,-1,0,1);
    twSolidCylinder(0.7,0.6,2,20,1);
    glPopMatrix();
  
    # draw left leg
    glTranslated(-1.8,0,0);
    glPushMatrix();
    glRotated(-35,1,0,1);
    twSolidCylinder(0.7,0.6,2,20,1); 
    glPopMatrix();
  
    # draw left arm
    glTranslated(0,3.8,0);
    glPushMatrix();
    glRotated(-90,0,0,1);
    twSolidCylinder(0.5,0.4,2,20,1); 
    glPopMatrix();

    # draw right arm
    glTranslated(2,0,0);
    glPushMatrix();
    glRotated(90,0,0,1);
    twSolidCylinder(0.5,0.4,2,20,1); 
    glPopMatrix();
    glPopMatrix();

def twGround(color=(0.13,0.55,0.13)):
    '''draws a quad in given color (default forest green) at min y of scene's bounding box.  This uses RGB color, not material and lighting.'''
    glPushAttrib(GL_POLYGON_BIT | GL_CURRENT_BIT | GL_ENABLE_BIT | GL_TEXTURE_BIT )
    glEnable(GL_CULL_FACE)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_1D)
    glDisable(GL_TEXTURE_2D)
    glColor3fv(color)
    glBegin(GL_QUADS)
    # y=BBMin[1].  The other coordinates change in the usual way.  The
    # order is important, because we want the polygon to be facing the
    # center, so that it's culled when we look up at it, but not when we
    # look down on it.
    glNormal3f(0,1,0)
    glVertex3f(BBMin[0],BBMin[1],BBMax[2])
    glVertex3f(BBMax[0],BBMin[1],BBMax[2])
    glVertex3f(BBMax[0],BBMin[1],BBMin[2])
    glVertex3f(BBMin[0],BBMin[1],BBMin[2])
    glEnd()
    glPopAttrib()

def twSky(color=(0.53, 0.81, 0.92)):
    '''draws quads in given color (default light sky blue) on every side of the
bounding box except for the min y side, which is the ground.  This uses RGB color, not material and lighting.  See
twGround().'''
    glPushAttrib(GL_POLYGON_BIT | GL_CURRENT_BIT | GL_ENABLE_BIT | GL_TEXTURE_BIT )
    glEnable(GL_CULL_FACE)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_1D)
    glDisable(GL_TEXTURE_2D)
    glColor3fv(color)
    glBegin(GL_QUADS);
    # y=BBMax[1]
    glNormal3f(0,-1,0)
    glVertex3f(BBMin[0],BBMax[1],BBMax[2]);
    glVertex3f(BBMin[0],BBMax[1],BBMin[2]);
    glVertex3f(BBMax[0],BBMax[1],BBMin[2]);
    glVertex3f(BBMax[0],BBMax[1],BBMax[2]);
    # x=BBMin[0]
    glNormal3f(1,0,0)
    glVertex3f(BBMin[0],BBMin[1],BBMin[2]);
    glVertex3f(BBMin[0],BBMax[1],BBMin[2]);
    glVertex3f(BBMin[0],BBMax[1],BBMax[2]);
    glVertex3f(BBMin[0],BBMin[1],BBMax[2]);
    # x=BBMax[0]
    glNormal3f(-1,0,0)
    glVertex3f(BBMax[0],BBMin[1],BBMin[2]);
    glVertex3f(BBMax[0],BBMin[1],BBMax[2]);
    glVertex3f(BBMax[0],BBMax[1],BBMax[2]);
    glVertex3f(BBMax[0],BBMax[1],BBMin[2]);
    # z=BBMax[2]
    glNormal3f(0,0,-1)
    glVertex3f(BBMin[0],BBMin[1],BBMax[2]);
    glVertex3f(BBMin[0],BBMax[1],BBMax[2]);
    glVertex3f(BBMax[0],BBMax[1],BBMax[2]);
    glVertex3f(BBMax[0],BBMin[1],BBMax[2]);
    # z=BBMin[2]
    glNormal3f(0,0,1)
    glVertex3f(BBMin[0],BBMin[1],BBMin[2]);
    glVertex3f(BBMax[0],BBMin[1],BBMin[2]);
    glVertex3f(BBMax[0],BBMax[1],BBMin[2]);
    glVertex3f(BBMin[0],BBMax[1],BBMin[2]);
    glEnd();
    glPopAttrib();

def drawTable(width, height, depth, topThickness, legSize):
    """Draws a parson's table

The origin is at the outer lower corner of the back left leg, because
the table lies in the +++ octant. The table is drawn in the current
color, with the given dimensions. The height corresponds to the y
axis, x and z are width and depth, respectively. The legs are square,
with the given size.
"""

    # draw the top
    glPushMatrix();
    # divide by two because the origin of the cube is in its center
    glTranslatef(float(width)/2,height-float(topThickness)/2,float(depth)/2);
    glScalef(width,topThickness,depth);
    glutSolidCube(1);
    glPopMatrix();

    def drawleg(legX,legZ):
        legY=float(height-legSize)/2;    # y coord of cube origin for a leg
        legH=height-legSize;             # height of a leg
        glPushMatrix()
        glTranslatef(legX,legY,legZ)
        glScalef(legSize,legH,legSize)
        glutSolidCube(1)
        glPopMatrix()

        
    halfLegSize = legSize*0.5        # half the thickness of a leg
    drawleg(halfLegSize,halfLegSize) # back left leg, at origin
    drawleg(width-halfLegSize,halfLegSize) # back right leg
    drawleg(halfLegSize,depth-halfLegSize) # front left leg
    drawleg(width-halfLegSize,depth-halfLegSize) # front right leg

### ================================================================
### tw-mouse.cc

### previous values of mouse location
MousePosition = (None, None)

## This function 
def twMouseFunction(button, state, x, y):
    '''records the current mouse location when the button goes
down, facilitating the motion function.'''
    global WindowSize, MousePosition
    y = WindowSize[1] - y;
    if button == GLUT_LEFT_BUTTON:
        if GLUT_DOWN==state:
            MousePosition = (x,y)
    elif button == GLUT_MIDDLE_BUTTON:
        if GLUT_DOWN==state:
            twOrientVPN(x,y)
    elif button == GLUT_RIGHT_BUTTON:
        pass
    else:
        print "invalid button in mouse callback: %d" % (button)
    ## I hoped this would fix the area around the mouse that isn't
    ## updated, but no luck.
    glutPostRedisplay()
    
def twMotionFunction(x, y):
    global WindowSize, MousePosition
    y = WindowSize[1] - y;
    mx, my = MousePosition
    twTrackballOrientation(mx,my,x,y);
    MousePosition = (x,y)

    
### ================================================================
### tw-animation.cc

twIdleFunction = None           # the current idle function

def twIdleFunc(func):
    global twIdleFunction
    twIdleFunction = func
    glutIdleFunc(func)

def twNextFrame():
    global twIdleFunction
    if twIdleFunction != None:
        twIdleFunction()        # invoke the idle function once

### ================================================================
### Accumulation buffer stuff

# From the OpenGL Programming Guide, first edition, table 10-5
twJitterTable = (
    (0.5625, 0.4375),
    (0.0625, 0.9375),
    (0.3125, 0.6875),
    (0.6875, 0.8124),
    (0.8125, 0.1875),
    (0.9375, 0.5625),
    (0.4375, 0.0625),
    (0.1875, 0.3125))

def twAntiAliasingFrustum(left,right,bottom,top,near,far, 
                          pixdx, pixdy, verbose=False):
    """Set up anti-aliasing frustum.  

The pix args are the sub-pixel jitter values."""
    viewport = glGetIntegerv(GL_VIEWPORT);

    windowWidth=viewport[2];
    windowHeight=viewport[3];
    frustumWidth=right-left;
    frustumHeight=top-bottom;
    
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    dx = pixdx*frustumWidth/windowWidth;
    dy = pixdy*frustumHeight/windowHeight;
    if verbose:
        print "Camera jitter in world units = %f %f" % (dx,dy)
    glFrustum(left+dx,right+dx,bottom+dy,top+dy,near,far);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();

def twDepthOfFieldFrustum(left,right,bottom,top,near,far, 
                          eyedx, eyedy, focusDist, verbose=False):
    """Set up depth-of-field frustum.  

eye dx and dy are the eye 'movement' and focusDist is the distance
from the eyes that is most in focus.  This computes the amount by
which to jitter the frustum so that 'focusDist' is most in focus."""
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    dx = (eyedx/focusDist)*(focusDist-near);
    dy = (eyedy/focusDist)*(focusDist-near);
    if verbose:
        print "dofFrustum: dx =  %.5f, dy = %.5f\n" % (dx, dy)
    glFrustum(left+dx,right+dx,bottom+dy,top+dy,near,far);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    # Translating the coordinate system by (eyedx,eyedy) is the same as
    # moving the eye by (-eyedx,-eyedy).
    glTranslatef(eyedx,eyedy,0.0);

def twDepthOfFieldEyeMovement(near, focusDist, depthOfField, blurAmount, verbose=False):
    """Compute the eye movement for depth of field

the focusDist is the depth (from the eye) that is most in-focus, and
depthOfField is a displacement from that.  'blurAmount' is the
sub-pixel distance that determines the eye movement.  This function just does the formula from the reading."""
    term1 = float(focusDist-depthOfField-near)/float(focusDist-depthOfField);
    term2 = float(focusDist-near)/focusDist;
    result = -blurAmount/float(term1-term2);
    if verbose:
        print "E = %f as a function of %f %f %f" % (result,focusDist,depthOfField,blurAmount)
    return result;

def twDepthOfFieldCamera(left,right,bottom,top,near,far,
                         blurAmount, focusDist, depthOfField,
                         verbose=False):
    """Set up a depth-of-field camera

the focusDist is the depth (from the eye) that is most in-focus, and
depthOfField is a displacement from that.  We'll achieve a certain
amount of blurriness by jittering the whole setup several times,
varying the first argument, blurAmount, which is an (x,y) tuple in
sub-pixel distances.  That amount is *like* the frustum jitter in
motion blur and so forth, but is in this case used to compute the eye
movement and the frustum jitter.  See the math in the reading."""
    viewport = glGetIntegerv(GL_VIEWPORT);

    windowWidth=viewport[2];
    windowHeight=viewport[3];
    frustumWidth=right-left;
    frustumHeight=top-bottom;

    # cx,cy are the conversion factors from pixels to world coordinates.
    cx = float(frustumWidth)/float(windowWidth)
    cy = float(frustumHeight)/float(windowHeight)

    # compute the eye movement
    eyedx = twDepthOfFieldEyeMovement(near,focusDist,depthOfField,(blurAmount[0]-0.5)*2*cx,verbose);
    eyedy = twDepthOfFieldEyeMovement(near,focusDist,depthOfField,(blurAmount[1]-0.5)*2*cy,verbose);

    twDepthOfFieldFrustum(left,right,bottom,top,near,far,eyedx,eyedy,focusDist,
                          verbose);

### ================================================================
### tw.cc (main stuff)

def twDisplayInit( bgR=0.75, bgG=0.75, bgB=0.75):
    global Toggles
    glClearColor(bgR,bgG,bgB,1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDisable(GL_LIGHTING)
    if Toggles[LIGHTING]:
        glEnable(GL_LIGHTING)
    else:
        glDisable(GL_LIGHTING)
    if Toggles[SMOOTH]:
        glShadeModel(GL_SMOOTH)
    else:
        glShadeModel(GL_FLAT)
    if Toggles[FILTER_NEAREST]:
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    else:
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

def twMainInit():
    global _FieldOfView, _FieldOfViewY, GlobalAmbient
    glEnable(GL_AUTO_NORMAL)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glDepthFunc(GL_LEQUAL) 
    twKeyInit()
    glutKeyboardFunc(twKeyboardCallback)
    glutMouseFunc(twMouseFunction)
    glutMotionFunc(twMotionFunction)
    glutReshapeFunc(twReshapeFunction)
    twIdleFunc(None)
    _FieldOfView = _FieldOfViewY
    ## All our toggles default to false
    for i in range(len(Toggles)):
        Toggles[i] = False;
        makeToggleMenu();
    ## irrelevant if lighting is off
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)
    twAmbient(GlobalAmbient) 
    twZview()
    
if __name__ == '__main__':
    print "TW loaded"
    
