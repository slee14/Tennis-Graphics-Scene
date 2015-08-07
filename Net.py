import sys, math, Court, Tennis
from TW import *

#sets the net texture so that the alpha transparency channel will 
#work. 
def setNetTex (rawfile, width, height):
	fp = open(rawfile)
	data = fp.read()
	fp.close()
	glTexImage2D(GL_TEXTURE_2D,0,GL_RGBA,width,height,0,GL_RGBA,GL_UNSIGNED_BYTE,data)
	glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_MODULATE)
	glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
	glTexParameter(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

#draws the white tape on the top of the net, as well as the black border. 
def drawTape():
	'''White tape'''
	glLineWidth(5)
	glColor3f(1,1,1)
	tapeVertices = [
		[0,3.375,Court.courtWidth+2.6],
		[0,3.375,-Court.courtWidth-2.6],
	]
	glBegin(GL_LINES)
	glVertex3fv(tapeVertices[0])
	glVertex3fv(tapeVertices[1])
	glEnd()

	'''Black border'''
	twColor(Tennis.black,0.1,0.1)
	glLineWidth(2)
	borderVertices = [
		[0,3.375,Court.courtWidth+2.6],
		[0,0.05,Court.courtWidth+2.6],
		[0,0.05,-Court.courtWidth-2.6],
		[0,3.375,-Court.courtWidth-2.6]
	]
	for i in range (0, 3):
		glBegin(GL_LINES)
		glVertex3fv(borderVertices[i])
		glVertex3fv(borderVertices[i+1])
		glEnd()

#draws the center strap white tape
def drawCenterStrap():
	glLineWidth(3)
	glColor3f(1,1,1)
	glBegin(GL_LINES)
	glVertex3f(0,3.375,0)
	glVertex3f(0,0.1,0)
	glEnd()

#draws the full net, texture maps the png.raw file on the plane
def drawNet():
	netVertices = [
		[0,3.3,Court.Court.courtWidth+2.6],
		[0,0.05,Court.Court.courtWidth+2.6],
		[0,0.05,-Court.Court.courtWidth-2.6],
		[0,3.3,-Court.Court.courtWidth-2.6]
	]
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
	glDepthMask(GL_FALSE)
	glDisable(GL_LIGHTING)
	glEnable(GL_TEXTURE_2D)
	setNetTex("TennisNet.png.raw", 156,331)
	glColor4f(1,1,1,1)

	glBegin(GL_QUADS)
	glTexCoord2f(0,0); glVertex3fv(netVertices[0])
	glTexCoord2f(0,2); glVertex3fv(netVertices[1])
	glTexCoord2f(35,2); glVertex3fv(netVertices[2])
	glTexCoord2f(35,0); glVertex3fv(netVertices[3])
	glEnd()
	glDisable(GL_TEXTURE_2D)

#Draws the full net with the tape, textured net and center strap 
def drawFullNet():
	drawTape()
	drawNet()
	drawCenterStrap()

def display():
    twDisplayInit()
    twCamera()
    glPushAttrib(GL_ALL_ATTRIB_BITS)
    glEnable(GL_DEPTH_TEST)
    drawNet()
    glPopAttrib()
    glFlush()
    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    twBoundingBox(-Court.fullLength/2,Court.fullLength/2,0,5,-Court.fullWidth/2,Court.fullWidth/2);
    twInitWindowSize(600,600)
    glutCreateWindow(sys.argv[0])
    glutDisplayFunc(display)
    ## twSetMessages(TW_ALL_MESSAGES)
    twMainInit()
    glutMainLoop()

if __name__ == '__main__':
    main()