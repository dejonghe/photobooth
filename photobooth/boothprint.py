import ast
import cups
import logging 
import time
from PIL import Image, ImageDraw, ImageFont

try:
    from configparser import ConfigParser
except ImportError:
    # Python < 3
    from ConfigParser import ConfigParser

logger = logging.getLogger('photobooth')

class BoothPrint(object):
    def __init__(self, images=[], config_file='./.photobooth.cfg'):
        self.images = images
        logger.info('Booth print loading config')
        config = ConfigParser()
        config.read(config_file)
        self.print_size = ast.literal_eval(config.get('prints','print_size'))
        self.image_size = ast.literal_eval(config.get('prints','image_size'))
        self.panel_size = ast.literal_eval(config.get('prints','panel_size'))
        self.title_border = ast.literal_eval(config.get('prints','title_border'))
        self.title_message = config.get('prints','title_message')
        self.print_images = ast.literal_eval(config.get('prints','print_images'))
        self.printer_name = config.get('prints','printer_name')
        self.boothprint = self._combine(self.images)
        
        

    def _combine(self, images):
        boothprint = Image.new('RGBA', self.print_size)
        columns = self.print_size[0] / self.panel_size[0]
        rows  = 2 # self.print_size[1] / self.panel_size[1]
        i = 0
        for row in range(0,rows):
            for col in range(0,columns):
                resized = Image.open(images[i]).resize(self.image_size)
                crop_height = ( self.image_size[1] - self.panel_size[1] ) / 2
                resized = resized.crop((0,crop_height,self.image_size[0],self.image_size[1] - crop_height))
                boothprint.paste(resized,(row*self.panel_size[0],col*self.panel_size[1],(row+1)*self.panel_size[0],(col+1)*self.panel_size[1]))
                i = i + 1
        draw = ImageDraw.Draw(boothprint)
        v_inner_panel_border = [(self.panel_size[0], 0),(self.panel_size[0],self.panel_size[1]*rows)]
        h_inner_panel_border = [(0, self.panel_size[1]),(self.print_size[0],self.panel_size[1])]
        draw.line(v_inner_panel_border, fill='#fff', width=10)
        draw.line(h_inner_panel_border, fill='#fff', width=10)
        font = ImageFont.truetype("/usr/share/fonts/truetype/piboto/Piboto-Bold.ttf", 100)
        draw.text((50, self.print_size[1] - self.title_border[1] + 40),"Derek & Tanya's Wedding 08/04/2018",'#fff',font=font)
        print_name = "images/prints/{}.jpg".format(str(int(time.time())))
        boothprint.save(print_name)
        return print_name

    def printer(self):
        if self.print_images:
            conn = cups.Connection()
            print_id = conn.printFile(self.printer_name, self.boothprint, 'PhotoBooth', {})
            while conn.getJobs().get(print_id):
                time.sleep(1)
