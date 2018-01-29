
import picamera

class Camera(object):
    def __init__(self,width,height):
        self.width = width
        self.height = height

    def preview(self):
        with picamera.PiCamera() as camera:
            camera.resolution(self.width,self.height)
            camera.hflip = True
            camera.start_preview()
