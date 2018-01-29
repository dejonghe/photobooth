
from photobooth import PhotoBooth

__version__ = '0.0.0'

def main():
    pb = PhotoBooth()
    pb.run()

if __name__ == '__main__':
    try: main()
    except: raise
