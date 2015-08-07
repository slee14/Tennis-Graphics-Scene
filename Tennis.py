import sys, math, Court, TennisBall, TennisRacquet, random, GlobeTextured, Tennis, ScoreCard, Fence, Net, Yang_skyDome
from TW import *

aspect_ratio = None

# This is the height of the window, in pixels 

window_height=600
window_width=800

# Initialize the fovy to always be 90 degrees. In fact, we never
#   change it, but we could.

fovy=90
near=1
far=300

#colors
mantisGreen = (116/255.0,195/255.0,101/255.0)   
persianBlue = (0.0,103/255.0,165/255.0)
midnightBlue = (25/255.0,25/255.0,122/255.0)
spaceCadet = (29/255.0, 41/255.0, 81/255.0)
agateBlue = (68/255.0, 113/255.0, 155/255.0)
appleGreen = (123/255.0, 160/255.0, 91.0/255.0)
white = (1.0,1.0,1.0)
black = (0,0,0)

# the dimensions of the top of the frustum, in world coordinates
image_rectangle_height = None
image_rectangle_width  = None

# The reshape callback is executed whenever the window changes size.
def myReshape(w, h):
    """ The math here is a simple mapping from window coordinates
       (pixels) to world coordinates.  The height of the image
       rectangle is proportional to the height of the window, and
       the ratio of half the image height to near equals the
       tangent of the field of view angle.

       tan(fovy/2) = (irh/2)/near

       Solve that for irh.  Remember that we have to deal with
       degrees and radians as well.
    """
    global aspect_ratio, window_width, window_height
    global image_rectangle_width, image_rectangle_height
    aspect_ratio = float(w)/float(h)
    window_width=w
    window_height=h
    # use the whole window as the viewport
    glViewport(0,0,w,h)
    # set up the camera again, using new aspect ratio
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(fovy,aspect_ratio,near,far);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    # dimensions of top of frustum, in world units
    # the height is actually a constant, and the width varies by the
    # aspect ratio of the window
    image_rectangle_height = 2*near*math.tan(fovy*((M_PI/180)/2));
    image_rectangle_width = image_rectangle_height*aspect_ratio;

def cameraDrawing():
    '''Draws stuff in the camera frame, as if on the lens of the camera

The following code will put in our viewport and the cross-hairs.
We're still in a coordinate system where the camera is at the
origin and the image rectangle is centered about the negative z
axis at a distance of near. '''
    glDisable(GL_LIGHTING)
    glColor3f(0,0,0);

    # this draws the cross hairs
    glBegin(GL_LINES);
    cx=image_rectangle_width/2;
    cy=image_rectangle_height/2;
    glVertex3f(-cx,0,-near-5);
    glVertex3f(+cx,0,-near-5);
    glVertex3f(0,-cy,-near-5);
    glVertex3f(0,+cy,-near-5);
    glEnd();
    


""" The first is the view reference point (VRP), which is the same as the
eye location for the gluLookAt function.  The second is the view plane
normal (VPN).  The VRP is modified by moving forward and backward in the
scene.  The VPN is modified by turning left and right. 
"""

VRP = [30,5.5,0]
VPN = [-1,0,0]

def place_camera():
    gluLookAt(VRP[0],VRP[1],VRP[2],
              VRP[0]+VPN[0],VRP[1]+VPN[1],VRP[2]+VPN[2],
              0,1,0)
    
def lighting():
    twGrayLight(GL_LIGHT0,(1,1,1,0),0.3, 0.6, .5)
    glShadeModel(GL_SMOOTH);
    twAmbient(0.3);
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER,GL_TRUE);
    glEnable(GL_LIGHTING);

def motion(mx,my):
    # convert to first quadrant
    my=window_height-my;
    # measure from center
    mx=mx-(window_width/2);
    my=my-(window_height/2);
    """ Figure out what angle to rotate.  This computation is based
       on the fact that the tangent of the angle of rotation equals
       x/near, after x has been scaled to image_rectangle
       units. That scaling is easy, because:

       x : window_width :: ix : image_rectangle_width

       Solve that for ix. """

    ix = (image_rectangle_width*mx)/window_width;
    # Now, do the rotation of the view plane normal (VPN) 
    theta=-math.atan(ix/near);       # flip the sign

    global VPN, VRP

    # temporary values 
    x = VPN[0];
    z = VPN[2];
    # for efficiency and brevity, compute these once
    c = math.cos(theta)
    s = math.sin(theta)

    VPN[0] =  x*c+z*s;
    VPN[2] = -x*s+z*c;

    """Now, move forward, if necessary. The math here is simpler;
       we just move forward by an amount proportional to the
       distance above the midline.  """

    factor=(20.0*my)/window_height;
    VRP[0] += factor*VPN[0];
    VRP[2] += factor*VPN[2];
    glutPostRedisplay();

def mouse(btn, state, mx, my):
    if not (btn==GLUT_LEFT_BUTTON and state==GLUT_DOWN):
        return
    # same a the motion function
    motion(mx,my)

def key(k, x, y):
    if k == 'q':
        exit(0);
    glutPostRedisplay();

#Positions the racquet at some location, sets it down, and then calls drawRacquet()
#from the TennisRacquet class. 
def positionRacquet():
    glPushMatrix()
    glTranslate(Court.boxLength,0.1,-(Court.boxWidth)/2.0)
    glRotatef(-90,1,0,0)
    glScalef(0.25,0.25,0.25)
    TennisRacquet.drawRacquet()
    glPopMatrix()

#Places the score cards, with the stand, at the left net post. Have to rotate it so that 
#the writing is the right way facing in  - did not double texture it 
def placeScoreCards():
    glPushMatrix()
    glTranslate(0,5,Court.courtWidth+3.0)
    glRotatef(180,0,1,0)
    ScoreCard.drawAll()
    glPopMatrix()

#Draws the ground outside the tennis court but inside the dome. Makes it so that it tries
#to match the color of the grass on the sky texture. 
def drawGround():
    glPushMatrix()
    twColor(appleGreen,0.1,0.1)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 2)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    twLoadTexture(2, "grass2.ppm")

    glBegin(GL_QUADS)
    glTexCoord2f(0,10); glVertex3f(-200,-.01,-200)
    glTexCoord2f(0,0); glVertex3f(-200,-.01,200)
    glTexCoord2f(10,0); glVertex3f(200,-.01,200)
    glTexCoord2f(10,10); glVertex3f(200,-.01,-200)
    glEnd()
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def display():
    glPushAttrib(GL_ALL_ATTRIB_BITS);
    glClearColor(1,1,1,1);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glPushMatrix();     
    place_camera(); 
    lighting()
    drawGround()
    Court.drawTennisCourt() 
    placeScoreCards()
    positionRacquet()
    TennisBall.drawBalls(20)   
    Net.drawFullNet()
    glPopMatrix()
    cameraDrawing() 
    glFlush();
    glutSwapBuffers();
    glPopAttrib();

def main():
    glutInit(sys.argv)
    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    twInitWindowSize(window_width,window_height)
    glutCreateWindow(sys.argv[0])
    glutDisplayFunc(display)
#    glEnable(GL_NORMALIZE)      # twMainInit does this
    twBoundingBox(0,1,0,1,0,1)   # fake, just to avoid complaints
    twMainInit()
    myReshape(window_width,window_height)
    glutReshapeFunc(myReshape);
    glutKeyboardFunc(key);
    glutMouseFunc(mouse);
    glutMotionFunc(motion);
    TennisBall.setupCoords(20)
#    glEnable(GL_DEPTH_TEST);    # twMainInit does this
    glutMainLoop();

if __name__ == '__main__':
    main()