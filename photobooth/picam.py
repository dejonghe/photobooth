import logging
import picamera
import time

logger = logging.getLogger('photobooth')

class Camera(object):
    def __init__(self,width,height):
        logger.debug('Building camera object')
        self.width = width
        self.height = height

    def preview(self):
        with picamera.PiCamera() as camera:
            logger.debug('Camera started')
            camera.resolution = (self.width,self.height)
            camera.hflip = True
            camera.start_preview()
            logger.debug('Camera preview started')
            time.sleep(5)
            camera.stop_preview()
