import logging
import picamera
import time

logger = logging.getLogger('photobooth')

class Camera(object):
    def __init__(self,img_path,width,height):
        logger.debug('Building camera object')
        self.img_path = img_path
        self.width = width
        self.height = height

    def preview(self):
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
                camera.capture( os.path.join(self.img_path, 'image', str(pNum), '.jpg') )
                time.sleep(.5)

            # Stop the camera preview so we can return to the pygame surface
            camera.stop_preview()

