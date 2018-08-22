import ast
import logging
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import pygame
import random
import sys
import time

import gphoto2 as gp

try:
    from configparser import ConfigParser
except ImportError:
    # Python < 3
    from ConfigParser import ConfigParser


logger = logging.getLogger('photobooth')

#try:
#    from picam import Camera
#except:
#    Camera = None
#    logger.debug('No pi cam')

from picam import Camera
from boothprint import BoothPrint
    
config_file_name = './.photobooth.cfg'
# Init some pygame util stuff 
logger.debug('Initializing GUI')
pygame.init()
width = pygame.display.Info().current_w
height = pygame.display.Info().current_h
size = width, height
black = 0,0,0
white = 255,255,255

# Setup the change background event
chbkg_event = pygame.USEREVENT + 1
chbkg_time = 3000
# Setup the Touch to start event
tts_event = pygame.USEREVENT + 2
tts_time = 2000

class PhotoBooth(object):
    def __init__(self):
        logger.debug('Building Photobooth')
        self.config = ConfigParser()
        self.config.read(config_file_name)
        font = self.config.get('photobooth','font')
        font_size = ast.literal_eval(self.config.get('photobooth','font_size'))
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(font,font_size,bold=True)
        self.img_prefix = os.path.join(os.getcwd(),'images')
        self.show_images = ast.literal_eval(self.config.get('photobooth','show_images'))
        self._ensure_img_path()
        if Camera:
            logger.debug('cam init')
            self.camera = Camera(pygame,self.screen,self.img_prefix,width,height)
        else:
            logger.debug('No cam')
            self.camera = None
        pygame.time.set_timer(chbkg_event, chbkg_time)
        pygame.time.set_timer(tts_event, tts_time)
        pygame.display.toggle_fullscreen()
        pygame.mouse.set_visible(False)

    '''
        Runs the pygame application
    '''
    def run(self):
        try:
            logger.debug('Entering main event loop')
            self._display_image(self._random_file())
            pygame.display.flip()
            while 1:
                for event in pygame.event.get():
                    self.config.read(config_file_name)
                    paper_count = ast.literal_eval(self.config.get('prints','paper_count'))
                    ink_count = ast.literal_eval(self.config.get('prints','ink_count'))
                    self._check_empty(paper_count,18,'paper')
                    self._check_empty(ink_count,36,'ink')
                    if event.type == pygame.QUIT: sys.exit()
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: pygame.display.toggle_fullscreen()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.camera:
                            images = self.camera.preview()
                            boothprint = BoothPrint(images)
                            paper_count = paper_count - 1
                            ink_count = ink_count - 1
                            self._display_image(boothprint.boothprint)
                            printed = boothprint.printer()
                            if printed:
                                self.config.set('prints','paper_count',str(paper_count))
                                self.config.set('prints','ink_count',str(ink_count))
                                with open(config_file_name, 'wb') as f:
                                    self.config.write(f)
                            time.sleep(10)
                    elif self.show_images and event.type == chbkg_event:
                        self._display_image(self._random_file())
                        pygame.display.flip()
                    elif event.type == tts_event:
                        self._display_text("Touch screen to start")
                        pygame.display.flip()
        except gp.GPhoto2Error as e:
            logger.error(e.string)
            self._display_text(e.string)
            time.sleep(5)
            self.run()
        except Exception as e:
            logger.error(e)
            self._display_text(e)
            time.sleep(5)
            self.run()

    '''
    Displays text on the screen
    '''
    def _display_text(self, text):
        self.screen.fill(black)
        text = self.font.render(text,True,(white))
        textrect = text.get_rect()
        textrect.centerx = self.screen.get_rect().centerx
        textrect.centery = self.screen.get_rect().centery
        self.screen.blit(text,textrect)
        pygame.display.flip()

    '''
    Ensures that image directory is avaliable
    ''' 
    def _ensure_img_path(self):
        if not os.path.exists(self.img_prefix):
            os.makedirs(self.img_prefix)

    '''
    This function finds a random file in the images bank
    '''
    def _random_file(self):
        files = [os.path.join(path, filename)
            for path, dirs, files in os.walk(self.img_prefix)
            for filename in files]
        return random.choice(files)

    '''
    Displays an image to the screen
    '''
    def _display_image(self,file_path):
        self.screen.fill((0,0,0))
        img = pygame.image.load(file_path)
        img = pygame.transform.scale(img,(width,height)) # Make the image full screen
        self.screen.blit(img,(0,0))
        pygame.display.flip() # update the display


    '''
    Checks for empty supplies 
    '''
    def _check_empty(self,supply_count,refill_size,supply_name):
        if supply_count == 0:
            supply_empty = True
            logger.debug("In {} empty catch".format(supply_name))
            if supply_name == 'ink':
                self._display_text("Out of ink. Remove ink from side. Insert new ink. Touch to clear")
            elif supply_name == 'paper':
                self._display_text("Out of paper. Remove tray. Add paper pack. Touch to clear") 
            while supply_empty:
                for supply_event in pygame.event.get():
                    if supply_event.type == pygame.QUIT: sys.exit()
                    elif supply_event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: pygame.display.toggle_fullscreen()
                    elif supply_event.type == pygame.MOUSEBUTTONDOWN:
                        logger.debug('Out of {} dismissed'.format(supply_name))
                        supply_count = refill_size
                        self.config.set('prints',"{}_count".format(supply_name),str(supply_count))
                        logger.debug('Set {} count to {}'.format(supply_name,supply_count))
                        with open(config_file_name, 'w') as f:
                            self.config.write(f)
                        logger.debug('Wrote to config {} count'.format(supply_name))
                        supply_empty = False
                        break
