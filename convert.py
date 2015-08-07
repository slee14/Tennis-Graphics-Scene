import sys

'''Converts any image file that PIL can understand into a very raw format:
just a sequence of bytes.  You'd better know the width and height and
such.'''

try:
    # This works on the Linux machines
    from PIL import Image
except:
    print "Couldn't import PIL.Image"
    sys.exit()
    
def writeimage(filename):
    img = Image.open(filename)
    outfile = filename+'.raw'
    print '''converting %s which is format %s (%s)
and dimensions %s
to raw file %s''' % (
        filename,
        img.format_description,
        img.format,
        img.getbbox(),
        outfile)
    fp = open(outfile,'w')
    fp.write(img.tostring())
    fp.close()

if __name__ == '__main__':
    writeimage(sys.argv[1])
    
