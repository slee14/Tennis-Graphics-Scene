import sys

'''Displays any image file that PIL can understand.  Doesn't display
transparency well, so try showing that on a web browser.'''

try:
    # This works on the Linux machines
    from PIL import Image
except:
    print "Couldn't import PIL.Image"
    sys.exit()
    
def showimage(filename):
    img = Image.open(filename)
    print "converting %s which is format %s (%s) and dimensions %s" % (
        filename,
        img.format_description,
        img.format,
        img.getbbox())
    img.show()

if __name__ == '__main__':
    showimage(sys.argv[1])
    
