import logging
import picamera
import os
import time
#try:
    #from dslr import DSLR
#except ImportError:
    #DSLR = None
    #pass
from dslr import DSLR


logger = logging.getLogger('photobooth')

class Camera(object):
    def __init__(self,pygame,screen,img_path,width,height):
        logger.debug('Building camera object')
        self.pygame = pygame
        self.screen = screen
        self.img_path = img_path
        self.width = width
        self.height = height

    def preview(self):
        images = []
        with picamera.PiCamera() as camera:
            logger.debug('Camera started')
            camera.resolution = (self.width,self.height)
            camera.hflip = True
            camera.annotate_background = picamera.Color('black')
            camera.annotate_text_size = 64
            logger.debug('Camera preview started')
            # Loop through the 4 photo taking sequences
            for pNum in range (1,5):
                camera.start_preview()
                camera.annotate_text = 'Photo ' + str(pNum) + ' of 4'
                time.sleep(1)

                for countDown in range (3,0,-1):
                    camera.annotate_text = str(countDown)
                    time.sleep(.5)

                camera.annotate_text = ''
                filename = os.path.join(self.img_path, "{}.jpg".format(str(int(time.time()))))
                images.append(filename)
                logger.debug('trying dslr')
                try:
                    logger.debug('DSLR in use')
                    dslr = DSLR(self.img_path, self.width, self.height)
                    dslr.capture( filename )
                except:
                    logger.debug('PiCam in use')
                    camera.capture( filename )
                self._display_image(filename)
                # Stop the camera preview so we can return to the pygame surface 
                # to show the last shot
                camera.stop_preview()
                time.sleep(1)

            camera.stop_preview()
            return images

    '''
    Displays an image to the screen
    '''
    def _display_image(self,file_path):
        self.screen.fill((0,0,0))
        img = self.pygame.image.load(file_path)
        img = self.pygame.transform.scale(img,(self.width,self.height)) # Make the image full screen
        self.screen.blit(img,(0,0))
        self.pygame.display.flip() # update the display


