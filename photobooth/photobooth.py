
import os
import pygame
import random
import sys
import time


try:
    from picam import Camera
except:
    Camera = None
    print('No pi cam')
    
# Init some pygame util stuff 
pygame.init()
width = pygame.display.Info().current_w
height = pygame.display.Info().current_h
size = width, height
black = 0,0,0
white = 255,255,255

chbkg_event = pygame.USEREVENT + 1
chbkg_time = 2000

class PhotoBooth(object):
    def __init__(self):
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace",24)
        self.img_prefix = os.path.join(os.getcwd(),'images')
        self._ensure_img_path()
        if Camera:
            self.camera = Camera()
        else:
            self.camera = None
        pygame.time.set_timer(chbkg_event, chbkg_time)

    '''
        Runs the pygame application
    '''
    def run(self):
        self._display_image(self._random_file())
        pygame.display.flip()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: pygame.display.toggle_fullscreen()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.camera:
                        self.camera.preview()
                elif event.type == chbkg_event:
                    self._display_image(self._random_file())
                    pygame.display.flip()

    '''
        Displays text on the screen
    '''
    def _display_text(self, text):
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

