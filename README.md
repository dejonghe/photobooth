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

## Use
```
$ photobooth
```



# To Do 
[] Do math on image sizes 
[] Hookup DSLR option
[] Img Stitch 
[] Print 
