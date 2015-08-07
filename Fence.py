import sys, math, Court, Tennis
from TW import *

fenceHeight = 15.0

#draws cylindrical columns that correspond to the up to down fence margins
#is iterative, since it will make one every 10 units of distance
def drawColFence(sections):
	glRotate(-90,1,0,0)
	for i in range (0, sections):
		twCylinder(0.25,0.25,fenceHeight,10,10)
		glTranslate(10,0,0)

#draws cylindrical columns that correspond to the horizontal fencing
def drawRowFence(length,width):
	glPushMatrix()
	twCylinder(0.25,0.25,width,10,10)
	glTranslate(length,0,0)
	twCylinder(0.25,0.25,width,10,10)
	glTranslate(-length,0,0)
	glRotate(90,0,1,0)
	twCylinder(0.25,0.25,length,10,10)
	glTranslate(-width,0,-0)
	twCylinder(0.25,0.25,length,10,10)
	glPopMatrix()

#draws the full fence skeleton
def drawFull():
	twColor(Tennis.spaceCadet,0.2,0.2)
	glPushMatrix()
	glTranslate(-Court.fullLength,0,-Court.fullWidth)
	drawColFence(13)
	glPopMatrix()
	glPushMatrix()
	glTranslate(-Court.fullLength,0,Court.fullWidth)
	drawColFence(13)
	glPopMatrix()
	glPushMatrix()
	glTranslate(-Court.fullLength,0,Court.fullWidth-10)
	glRotate(90,0,1,0)
	drawColFence(5)
	glPopMatrix()
	glPushMatrix()
	glTranslate(Court.fullLength,0,Court.fullWidth-10)
	glRotate(90,0,1,0)
	drawColFence(5)
	glPopMatrix()
	glPushMatrix()
	glTranslate(-Court.fullLength,0,-Court.fullWidth)
	drawRowFence(120,60)
	glTranslate(0,15,0)
	drawRowFence(120,60)
	glPopMatrix()

#Makes the vertices for the fence plane that will surround the court
#It aligns with the center of the cylindrical fencing skeleton
#It returns an array of vertices after inputing a height parameter. 
def makeFenceVertices(height):
	return [
		[-Court.fullLength+0.125,height-0.125,Court.fullWidth-0.125],
		[-Court.fullLength+0.125,height-0.125,-Court.fullWidth+0.125],
		[Court.fullLength-0.125,height-0.125,-Court.fullWidth+0.125],
		[Court.fullLength-0.125,height-0.125,Court.fullWidth-0.125]
	]

#Same as setNetTex from the Net.py
def setFenceTex (rawfile, width, height):
	fp = open(rawfile)
	data = fp.read()
	fp.close()
	glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,data)
	glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
	glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
	glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

#Draws the full fence plane, and sets the texture to a png.raw file
#the four sides of the fence are individual quads that have been
#texture mapped
def drawFencePlane():
	upper = makeFenceVertices(fenceHeight)
	lower = makeFenceVertices(0)
	
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
	glDepthMask(GL_FALSE)
	glDisable(GL_LIGHTING)
	glEnable(GL_TEXTURE_2D)
	setFenceTex("/textures/chainlink.png.raw", 400,466)
	glColor4f(1,1,1,1)

	glBegin(GL_QUADS)
	glTexCoord2f(0,0); glVertex3fv(upper[0])
	glTexCoord2f(100,0); glVertex3fv(upper[1])
	glTexCoord2f(100,20); glVertex3fv(lower[1])
	glTexCoord2f(0,20); glVertex3fv(lower[0])
	glEnd()

	glBegin(GL_QUADS)
	glTexCoord2f(0,0); glVertex3fv(upper[0])
	glTexCoord2f(200,0); glVertex3fv(upper[3])
	glTexCoord2f(200,20); glVertex3fv(lower[3])
	glTexCoord2f(0,20); glVertex3fv(lower[0])
	glEnd()

	glBegin(GL_QUADS)
	glTexCoord2f(0,0); glVertex3fv(upper[3])
	glTexCoord2f(100,0); glVertex3fv(upper[2])
	glTexCoord2f(100,20); glVertex3fv(lower[2])
	glTexCoord2f(0,20); glVertex3fv(lower[3])
	glEnd()

	glBegin(GL_QUADS)
	glTexCoord2f(0,0); glVertex3fv(upper[2])
	glTexCoord2f(200,0); glVertex3fv(upper[1])
	glTexCoord2f(200,20); glVertex3fv(lower[1])
	glTexCoord2f(0,20); glVertex3fv(lower[2])
	glEnd()
	glDisable(GL_TEXTURE_2D)

#draws the full fence, cylindrical skeleton and all. 
def drawFullFence():
	drawFull()
	drawFencePlane()

def display():
    twDisplayInit()
    twCamera()
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glEnable(GL_DEPTH_TEST)
    drawFullFence()
    glPopAttrib()
    glFlush()
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    twBoundingBox(-Court.fullLength,Court.fullLength,0,120,-Court.fullWidth,Court.fullWidth);
    twInitWindowSize(600,600)
    glutCreateWindow(sys.argv[0])
    glutDisplayFunc(display)
    ## twSetMessages(TW_ALL_MESSAGES)
    twMainInit()
    glutMainLoop()

if __name__ == '__main__':
    main()
