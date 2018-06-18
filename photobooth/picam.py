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
    def __init__(self,img_path,width,height):
        logger.debug('Building camera object')
        self.img_path = img_path
        self.width = width
        self.height = height

    def preview(self):
        images = []
        with picamera.PiCamera() as camera:
            logger.debug('Camera started')
            camera.resolution = (self.width,self.height)
            camera.hflip = True
            camera.start_preview()
            logger.debug('Camera preview started')
            # Loop through the 4 photo taking sequences
            for pNum in range (1,5):
                camera.annotate_text = 'Photo ' + str(pNum) + ' of 4'
                time.sleep(1)

                for countDown in range (3,0,-1):
                    camera.annotate_text = str(countDown)
                    time.sleep(.5)

                camera.annotate_text = ''
                filename = os.path.join(self.img_path, "{}.jpg".format(str(int(time.time()))))
                images.append(filename)
                logger.debug('trying dslr')
                if DSLR:
                    logger.debug('DSLR in use')
                    dslr = DSLR(self.img_path, self.width, self.height)
                    dslr.capture( filename )
                else:
                    logger.debug('PiCam in use')
                    camera.capture( filename )
                time.sleep(.5)

            # Stop the camera preview so we can return to the pygame surface
            camera.stop_preview()
            return images
