import io
import logging
import os
import time
import subprocess
import sys

from PIL import Image

logger = logging.getLogger('photobooth')

import gphoto2 as gp

class DSLR(object):
    def __init__(self, img_path, width, height):
        logger.debug('Building camera object')
        self.img_path = img_path
        self.width = width
        self.height = height
        

    def capture(self, target):
        orig_target = '{}_{}'.format(target.rstrip('.jpg'),'orig.jpg')
        gp.check_result(gp.use_python_logging())
        camera = gp.check_result(gp.gp_camera_new())
        gp.check_result(gp.gp_camera_init(camera))
        logger.debug('Capturing image')
        file_path = gp.check_result(gp.gp_camera_capture(
            camera, gp.GP_CAPTURE_IMAGE))
        logger.debug('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        logger.debug('Copying image to: {}'.format(orig_target))
        camera_file = gp.check_result(gp.gp_camera_file_get(
                camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
        gp.check_result(gp.gp_file_save(camera_file, orig_target))
        gp.check_result(gp.gp_camera_exit(camera))
        self.flip(orig_target,target)
        return 0


    def flip(self,image_filename,output_filename):
        logger.debug('Flipping: {} to {}'.format(image_filename,output_filename))
        image = Image.open(image_filename)
        flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)
        flipped_image.save(output_filename)
        return True
