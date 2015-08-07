import sys, math, ScoreCard, Tennis, Fence, TennisBall, Court, Net, Yang_skyDome
from TW import *

'''--------------------VARIABLES--------------------'''
#Length of the playable court, from baseline to net
courtLength = 39.0
#Length from one of the baselines to the back of the fence 
bankLength = 21.0
#Full length of the half-court + bank
fullLength = courtLength + bankLength
#Width of the playable court, from doubles sideline center service line 
courtWidth = 18.0
#Wdith of the side bank
bankWidth = 12.0
#Full width of the half-court + bank
fullWidth = courtWidth + bankWidth 
#Length and width of the service box 
boxLength = 21.0
boxWidth = 13.5

#Draws the blue area of the court. The inner court is a lighter shade
#of blue than the outer regions. Full vertices refers to the darker area,
#while courtVertices refers to the lighter area, the actual playable part
def drawCourts():
	fullVertices = [
		[-fullLength,0,fullWidth],
		[fullLength,0,fullWidth],
		[fullLength,0,-fullWidth],
		[-fullLength,0,-fullWidth]
	]
	twColor(Tennis.persianBlue,0.0,0.0)
	glPushMatrix()
	glDepthRange(0.0,1.0)
	glBegin(GL_QUADS)
	glVertex3fv(fullVertices[0])
	glVertex3fv(fullVertices[1])
	glVertex3fv(fullVertices[2])
	glVertex3fv(fullVertices[3])
	glEnd()
	glPopMatrix()
	glDisable(GL_TEXTURE_2D)
	courtVertices = [
		[-courtLength,0,courtWidth],
		[courtLength,0,courtWidth],
		[courtLength,0,-courtWidth],
		[-courtLength,0,-courtWidth]
		]
	twColor(Tennis.agateBlue,0.0,0.0)
	glPushMatrix()
	glDepthRange(0.0,0.9)
	glBegin(GL_QUADS)
	glVertex3fv(courtVertices[0])
	glVertex3fv(courtVertices[1])
	glVertex3fv(courtVertices[2])
	glVertex3fv(courtVertices[3])
	glEnd()
	glPopMatrix()

#draw lines will draw all the white lines on the court. 
#Takes depth into consideration, since it makes a weird effect
#sometimes if two objects are superimposed on the same plane
#uses a while look to connect all of the lines together
def drawLines():
	lineVertices = [
		[-courtLength,0,courtWidth], [-courtLength,0,-courtWidth],
		[-boxLength,0,boxWidth], [-boxLength,0,-boxWidth],
		[boxLength,0,boxWidth], [boxLength,0,-boxWidth],
		[courtLength,0,courtWidth], [courtLength,0,-courtWidth],
		[-courtLength,0,courtWidth], [courtLength,0,courtWidth],
		[-courtLength,0,boxWidth], [courtLength,0,boxWidth],
		[-boxLength,0,0], [boxLength,0,0],
		[-courtLength,0,-boxWidth], [courtLength,0,-boxWidth],
		[-courtLength,0,-courtWidth], [courtLength,0,-courtWidth],
		[-courtLength,0,0], [-courtLength+0.5,0,0],
		[courtLength,0,0], [courtLength-0.5,0,0]
	]
	glLineWidth(1.3)
	twColor(Tennis.white,0.1,0.1)
	glPushMatrix()
	i = 0
	while (i < len(lineVertices)):
		glDepthRange(0.0,0.8)
		glBegin(GL_LINES)
		glVertex3fv(lineVertices[i])
		glVertex3fv(lineVertices[i+1])
		glEnd()
		i = i + 2
	glPopMatrix()

#Draws a single net post, a twClinder with a solid sphere on top
def drawSinglePost():
	glRotatef(90,1,0,0)
	twCylinder(0.25,0.25,3.5,10,10)
	glTranslate(0,0,0)
	glutSolidSphere(0.25,10,10)	

#Draws both posts, distanced from each other a little more than the width
#of the court
def drawPosts():
	twColor(Tennis.spaceCadet,0.2,0.2)
	glPushMatrix()
	glTranslate(0,3.5,-courtWidth-3.0)
	drawSinglePost()
	glPopMatrix()
	glPushMatrix()
	glTranslate(0,3.5,courtWidth+3.0)
	drawSinglePost()
	glPopMatrix()

#draws the full tennis court. Also invokes the drawFullFence from Fence class, as 
#well as brings in the skydome from Yang_skyDome. Yang_skyDome has been edited to
#contain the texture already. 
def drawTennisCourt():
    Yang_skyDome.combine()
    drawCourts()
    drawLines()
    drawPosts()
    Fence.drawFullFence()

def display():
    twDisplayInit()
    twCamera()
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    drawTennisCourt()
    glEnable(GL_DEPTH_TEST)
    Net.drawNet()
    glPopAttrib()
    glFlush()
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode( GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    #twBoundingBox(-fullLength,fullLength,0,120,-fullWidth,fullWidth);
    twBoundingBox(-50,50,0,60,-50,50)
    twInitWindowSize(600,600)
    glutCreateWindow(sys.argv[0])
    glutDisplayFunc(display)
    twMainInit()
    glutMainLoop()

if __name__ == '__main__':
    main()
