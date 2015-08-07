# File Name: dome.py
# Purpose: CS307 Computer Graphics assignment #6 Creative Scene
# Written By: Hye Soo Yang & Dana Bullister Group Project
# Date Created: May 4, 2012
# Description: creates sky dome

'''
Description:

This module creates a sky dome with a sky texture map.
It uses twDrawBezierSurfaceTextured().
It is a single bezier surface so that the mapped texture
does not repeat.
As a result, the dome is not a perfect dome, but a little
bit enlongated.
The left and right ends of the texture lines up perfectly
so there one cannot really tell where the edges meet. 
'''
from TW import *
        
def createCP():
    '''Creates bezier surface control points for the dome'''

    sqr = 0.707
    lv2 = 0.886
    lv3 = 0.707
    lv4 = 0.5
    lv5 = 0.05

    y1 = 0.6
    y2 = 0.6
    y3 = 0.8
    y4 = 0.8
    cpArray = [[[1,0,0],
                [1,0,-1],
                [0,0,-1],
                [-1,0,-1],
                [-1,0,0],
                [-1,0,1],
                [0,0,1],
                [1,0,1],
                [1,0,0]],

               [[1*lv2,y1,0],
                [1*lv2,y1,-1*lv2],
                [0,y1,-1*lv2],
                [-1*lv2,y1,-1*lv2],
                [-1*lv2,y1,0],
                [-1*lv2,y1,1*lv2],
                [0,y1,1*lv2],
                [1*lv2,y1,1*lv2],
                [1*lv2,y1,0]],
               
               [[1*lv3,y2,0],
                [1*lv3,y2,-1*lv3],
                [0,y2,-1*lv3],
                [-1*lv3,y2,-1*lv3],
                [-1*lv3,y2,0],
                [-1*lv3,y2,1*lv3],
                [0,y2,1*lv3],
                [1*lv3,y2,1*lv3],
                [1*lv3,y2,0]],

               [[1*lv4,y3,0],
                [1*lv4,y3,-1*lv4],
                [0,y3,-1*lv4],
                [-1*lv4,y3,-1*lv4],
                [-1*lv4,y3,0],
                [-1*lv4,y3,1*lv4],
                [0,y3,1*lv4],
                [1*lv4,y3,1*lv4],
                [1*lv4,y3,0]],

               [[1*lv5,y4,0],
                [1*lv5,y4,-1*lv5],
                [0,y4,-1*lv5],
                [-1*lv5,y4,-1*lv5],
                [-1*lv5,y4,0],
                [-1*lv5,y4,1*lv5],
                [0,y4,1*lv5],
                [1*lv5,y4,1*lv5],
                [1*lv5,y4,0]]]
    
    return cpArray

def drawSky(u_steps,v_steps, textureFile="skydome.ppm"):
    """Draws sky dome with default texture of a clear sky.
    User can specify the texture by giving the .ppm file name as
    a parameter when calling this method.

    Adjust the dome size in your scene by using glPushMatirx() scalef()

    It creates the dome around the origin.
    """
    glPushAttrib(GL_ALL_ATTRIB_BITS);
    lightPos = (0,100,20,0)
    twGrayLight(GL_LIGHT0, lightPos, .7,1,.9);
    glEnable(GL_LIGHTING)
    turquoise3 = [ c/255.0 for c in (255, 255, 255) ]
    
    twColor(turquoise3,0.9,10)
    arrays = createCP()
    sky_tid = glGenTextures(1);

    '''
    Sky Texture Choices (names of .ppm files):

    sky_cirrus1.ppm
    sky_cirrus2.ppm
    sky_clear1.ppm
    sky_clear2.ppm
    sky_clear3.ppm
    sky_clouded1.ppm
    sky_clouded2.ppm
    sky_dusk1.ppm
    sky_sunset1.ppm
    sky_sunset2.ppm
    sky_sunset3.ppm
    sky_sunset4.ppm
    sky1.ppm               # Somewhat dusky sky
    sky2.ppm               # Somewhat clear/clouded sky

    '''
    # Replace the name of the sky texture file below with the one of your choice
    # from the list of .ppm file above
    # You can also give it as a parameter when calling it in your other module
    # (when calling drawSky() in another module file)
    twLoadTexture(sky_tid, twPathname(textureFile,False))

    glEnable(GL_AUTO_NORMAL)
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBindTexture(GL_TEXTURE_2D,sky_tid)
    twDrawBezierSurfaceTextured(arrays,(((0,1), (1,1)),((0,0), (1,0))),u_steps,v_steps, GL_FILL)
    glDisable(GL_TEXTURE_2D)
    glPopAttrib()

def combine():
    glPushMatrix()
    glTranslate(-20,0,0)
    glScalef(90,100,90)
    drawSky(30,30, "skydome7.ppm")
    glPopMatrix()

def display():
    twDisplayInit();
    twCamera();
    #place_camera()
    '''
    Sky Texture Choices (names of .ppm files):

    sky_cirrus1.ppm
    sky_cirrus2.ppm
    sky_clear1.ppm
    sky_clear2.ppm
    sky_clear3.ppm
    sky_clouded1.ppm
    sky_clouded2.ppm
    sky_dusk1.ppm
    sky_sunset1.ppm
    sky_sunset2.ppm
    sky_sunset3.ppm
    sky_sunset4.ppm
    sky1.ppm               # Somewhat dusky sky
    sky2.ppm               # Somewhat clear/clouded sky

    '''
    #drawSky(30,30, "sky_sunset1.ppm")  # You can specify the name of texture file here
                                       # otherwise, it would have a default clear sky
                                       # texture.
    #drawSky(30,30, "skydome.ppm")
    combine()


    glFlush();
    glutSwapBuffers();

def main():
    glutInit(sys.argv)
    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    #twBoundingBox(-200,200,0,200,-200,200)

    twInitWindowSize(500,500)
    glutCreateWindow(sys.argv[0])
    glutDisplayFunc(display)
    twMainInit()
    glutMainLoop()

if __name__ == '__main__':
    main()
