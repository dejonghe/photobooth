import logging 
import time
from PIL import Image, ImageDraw

logger = logging.getLogger('photobooth')


# print size is dpi * inches 
# my printer prints 300 dpi
# we're printing 4x6 inch photos
print_size = (300*4,300*6)
panel_size = (600,450)

class BoothPrint(object):
    def __init__(self, images=[]):
        self.images = images
        self.boothprint = self._combine(self.images)
        

    def _combine(self, images):
        boothprint = Image.new('RGBA', print_size)
        columns = print_size[0] / panel_size[0]
        rows  = 2 # print_size[1] / panel_size[1]
        i = 0
        for row in range(0,rows):
            for col in range(0,columns):
                resized = Image.open(images[i]).resize(panel_size)
                boothprint.paste(resized,(row*panel_size[0],col*panel_size[1],(row+1)*panel_size[0],(col+1)*panel_size[1]))
                i = i + 1
        draw = ImageDraw.Draw(boothprint)
        v_inner_panel_border = [(panel_size[0], 0),(panel_size[0],panel_size[1]*rows)]
        h_inner_panel_border = [(0, panel_size[1]),(print_size[0],panel_size[1])]
        draw.line(v_inner_panel_border, fill='#fff', width=10)
        draw.line(h_inner_panel_border, fill='#fff', width=10)
        print_name = "images/prints/{}.jpg".format(str(int(time.time())))
        boothprint.save(print_name)
