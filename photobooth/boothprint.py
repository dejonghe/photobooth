import cups
import logging 
import time
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger('photobooth')


# print size is dpi * inches 
# my printer prints 300 dpi
# we're printing 4x6 inch photos
print_size = (300*6,300*4)
image_size = (900,600)
panel_size = (900,500)
title_border = (300*4,200)
print_images = False
printer_name = 'selphy'

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
                resized = Image.open(images[i]).resize(image_size)
                crop_height = ( image_size[1] - panel_size[1] ) / 2
                resized = resized.crop((0,crop_height,image_size[0],image_size[1] - crop_height))
                boothprint.paste(resized,(row*panel_size[0],col*panel_size[1],(row+1)*panel_size[0],(col+1)*panel_size[1]))
                i = i + 1
        draw = ImageDraw.Draw(boothprint)
        v_inner_panel_border = [(panel_size[0], 0),(panel_size[0],panel_size[1]*rows)]
        h_inner_panel_border = [(0, panel_size[1]),(print_size[0],panel_size[1])]
        draw.line(v_inner_panel_border, fill='#fff', width=10)
        draw.line(h_inner_panel_border, fill='#fff', width=10)
        font = ImageFont.truetype("/usr/share/fonts/truetype/piboto/Piboto-Bold.ttf", 100)
        draw.text((50, print_size[1] - title_border[1] + 40),"Derek & Tanya's Wedding 08/04/2018",'#fff',font=font)
        print_name = "images/prints/{}.jpg".format(str(int(time.time())))
        boothprint.save(print_name)
        return print_name

    def printer(self):
        if print_images:
            conn = cups.Connection()
            print_id = conn.printFile(printer_name, self.boothprint, 'PhotoBooth', {})
            while conn.getJobs().get(print_id):
                time.sleep(1)
