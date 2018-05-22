
from photobooth import PhotoBooth
from logger import console_logger, logging


__version__ = '0.0.1'

def main():
    pb = PhotoBooth()
    pb.run()

if __name__ == '__main__':
    try: main()
    except: raise
