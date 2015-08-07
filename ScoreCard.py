import sys, math
from TW import *

standSize = 1.5
standRadius = 0.02
silver = (131/255.0, 137/255.0, 150/255.0)

#Draws one card, given the parameters of width and height 
#Each card has two torus objects on it, serving as rings to hook it 
#on the stand. 
def card (width, height):
	twColor(silver,0.5,0.3)
	glPushMatrix()
	glTranslate(0.75*width,standRadius,0)
	glRotate(90,0,1,0)
	glutSolidTorus(0.01,0.04,10,10)
	glPopMatrix()
	
	glPushMatrix()
	glTranslate(0.25*width,standRadius,0)
	glRotate(90,0,1,0)
	glutSolidTorus(0.01,0.04,10,10)
	glPopMatrix()
	vertices = [
		[0,0,0],
		[width,0,0],
		[width,-height,0],
		[0,-height,0]
	]
	twColor((1,1,1),0.1,0.1)
	glBegin(GL_QUADS)
	glTexCoord2f(0,0); glVertex3fv(vertices[0])
	glTexCoord2f(1,0); glVertex3fv(vertices[1])
	glTexCoord2f(1,1); glVertex3fv(vertices[2])
	glTexCoord2f(0,1); glVertex3fv(vertices[3])
	glEnd()

#draws the silver stand, which is composed of two twCylinders. It will hold four cards
def stand():
	twColor(silver,0.8,0.5)
	glPushMatrix()
	glTranslate(-standSize/2.0,0,0)
	glRotate(90,0,1,0)
	twCylinder(standRadius,standRadius,standSize,10,10)
	glPopMatrix()
	glPushMatrix()
	glRotate(90,1,0,0)
	twCylinder(standRadius,standRadius,standSize,10,10)
	glPopMatrix()

#draws all four cards, given the sizes of the two different types of cards
#binds textures by referring to an integer, since there are four 
#different textures
def drawCards(smallSize, bigSize):
	glEnable(GL_TEXTURE_2D)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
	glPushMatrix()
	glTranslate(-0.7,-2*standRadius,0)
	glBindTexture(GL_TEXTURE_2D,1)
	card(bigSize, 1.75*bigSize)
	glPopMatrix()
	glPushMatrix()
	glTranslate(-2*standRadius-smallSize,-2*standRadius,0)
	glBindTexture(GL_TEXTURE_2D,2)
	card(smallSize,1.75*smallSize)
	glPopMatrix()
	glPushMatrix()
	glTranslate(2*standRadius,-2*standRadius,0)
	glBindTexture(GL_TEXTURE_2D,3)
	card(smallSize,1.75*smallSize)
	glTranslate(smallSize+2*standRadius,0,0)
	glBindTexture(GL_TEXTURE_2D,4)
	card(bigSize,1.75*bigSize)
	glPopMatrix()
	glDisable(GL_TEXTURE_2D)

#Draws the whole stand+cards
#Loads multiple textures, which were custom made for this
#The size of the set cards are 0.2 units, and the size of the game 
#cards is 0.4 unites
def drawAll():
	stand()
	twLoadTexture(1, "gameBlack.ppm")
	twLoadTexture(4, "gameRed.ppm")
	twLoadTexture(2, "setBlack.ppm")
	twLoadTexture(3, "setRed.ppm")

	drawCards(0.2,0.4)

def display():
    twDisplayInit()
    twCamera()
    drawAll()
    glFlush()
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    twBoundingBox(-0.5,0.5,-1,0,-1,1);
    twInitWindowSize(500,500)
    glutCreateWindow(sys.argv[0])
    glutDisplayFunc(display)
    ## twSetMessages(TW_ALL_MESSAGES)
    twMainInit()
    glutMainLoop()

if __name__ == '__main__':
    main()

