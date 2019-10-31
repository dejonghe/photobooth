# photobooth
Yet another raspberry pi photobooth 


## Setup

To build use the setup file:
```
python setup.py sdist
```

## Installation 

1. Pip install the dist package built in the prior step
```
pip install dist/photobooth.<version>.tar.gz
```
2. If you're using a picamera install the picamera module separately, by not including it in the pip package we can test on laptops. 
```
pip install picamera
```

3. *Note*
To for the DSLR cameras to start up automatically with an SD card in I had to disable the service that tries to mount them as a mass storage device
```
systemctl --user mask gvfs-gphoto2-volume-monitor.service
```

## Use
```
$ photobooth
```




# To Do 
[x] Do math on image sizes 
[x] Hookup DSLR option
[x] Img Stitch 
[x] Print 
[x] Handle Errors

# Setting up the pi

* Install raspbian with all the bells and whistles on SD
* Install LCD Screen
* Flip LCD Touchscrren (Optional) `sudo echo 'lcd_rotate=2' >> /boot/config.txt; sudo reboot`
* Enable PiCamera
* Clone repo `git clone git@github.com:dejonghe/photobooth.git`
* Install deb pkgs `sudo bash apt-requirements`
* Build / install (I've been using `pip install -e .` so i can tweak as i use)

