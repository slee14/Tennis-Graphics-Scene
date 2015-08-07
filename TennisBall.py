import sys, math, GlobeTextured, random, Court
from TW import *

#Draws a tennis ball that has been textured with TennisBallTexture.ppm
#Makes use of the GL_DECAL, since we just want to wrap it with our texture
#The texture is mapped onto a solidGlobe from GlobeTextured class, which
#we looked at in class. 
def drawBall():
    twColor((1,1,1),0.4,0.1)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 2)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    twLoadTexture(2, "/textures/TennisBallTexture.ppm")
    GlobeTextured.solidGlobe(.2,20,20)    #Tennis ball with a radius of 0.11 feet, or 1.35 inches
    glDisable(GL_TEXTURE_2D)

positions = []

#Sets up the random coordinates for the ball placement, and puts the locations in an array called
#positions. Temp1 refers to the x axis coordinate, while temp2 refers to the y axis coordinate. 
#Uses a for loop to iteratively append locations to an array. Call setupCoords in the main method
#of the file you open in linux, in this case, Tennis.py
def setupCoords(n):
    for i in range (0,n):
        temp1 = random.randrange(-Court.courtLength,0)
        temp2 = random.randrange(-Court.fullWidth,Court.fullWidth)
        positions.append([temp1,0,temp2])
     
#draws n balls for each location in the positions array. You translate by the x and y values,
#then draw ball.    
def drawBalls(n):
    for p in positions:
        glPushMatrix()
        glTranslate(*p)
        drawBall()
        glPopMatrix()

def display():
    twDisplayInit()
    twCamera()
    drawBall()
    drawBalls(5)
    glFlush()
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    twBoundingBox(-.5,0.5,-0.5,0.5,-0.5,0.5)
    twInitWindowSize(500,500)
    glutCreateWindow(sys.argv[0])
    glutDisplayFunc(display)
    setupCoords(5)
    ## twSetMessages(TW_ALL_MESSAGES)
    twMainInit()
    glutMainLoop()

if __name__ == '__main__':
    main()