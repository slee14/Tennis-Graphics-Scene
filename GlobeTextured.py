""" This program displays a sphere with a picture texture-mapped onto it.

Scott D. Anderson
Scott.Anderson@acm.org

Fall 2000 original
Fall 2003 adapted for TW
Fall 2009 ported to Python
"""

import sys
import math                     # for sin and cos

try:
  from TW import *
except:
  print '''
ERROR: Couldn't import TW.
        '''

### ================================================================
### Modeling a globe/sphere.  Maybe move this into TW someday?

def wireGlobe(radius, stacks, slices):
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

def solidGlobe(radius, stacks, slices):
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

### ================================================================

GlobeRadius = 5

Wire = True     ## wire-frame mode (vs filled)
Texture = False ## texture mapping (on or off)

Stacks = 8
Slices = 8

def display():
    twDisplayInit();
    twCamera();
    glPushAttrib(GL_ALL_ATTRIB_BITS);

    glEnable(GL_LIGHTING);
    twGrayLight(GL_LIGHT0, (10,10,10,0), 0,1,1)

    twColor( (0.5, 0.5, 0.5), 0.8, 100)
    if Wire:
        wireGlobe(GlobeRadius,Stacks,Slices);
    else:
        if Texture:
            glEnable(GL_TEXTURE_2D);
        else:
            glDisable(GL_TEXTURE_2D);
        solidGlobe(GlobeRadius,Stacks,Slices);

    glFlush();
    glutSwapBuffers();
    glPopAttrib();

def keys(key, x, y):
    global Wire, Texture, Slices, Stacks
    if key == 'w': 
        Wire = not Wire
    elif key == 't': 
        Texture = not Texture
    elif key == '.': 
        Stacks += 1 
        Slices += 1
    elif key == ',': 
        Stacks -=1 
        Slices -= 1
    glutPostRedisplay();

def main():
    glutInit(sys.argv)
    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    twBoundingBox(-GlobeRadius,GlobeRadius,
                   -GlobeRadius,GlobeRadius,
                   -GlobeRadius,GlobeRadius);
    twInitWindowSize(500,500)
    glutCreateWindow(sys.argv[0])
    glutDisplayFunc(display)
    twMainInit()
    twKeyCallback('w',keys,"toggle wire frame");
    twKeyCallback('t',keys,"toggle texture mapping");
    twKeyCallback('.',keys,"increase slices and stacks");
    twKeyCallback(',',keys,"decrease slices and stacks");

    textureNumber = glGenTextures(1)

    if len(sys.argv) < 2:
        twLoadTexture(textureNumber,twPathname("USflag.ppm",False))
    else:
        twLoadTexture(textureNumber,twPathname(sys.argv[1],True))
    glutMainLoop()

if __name__ == '__main__':
    main()
