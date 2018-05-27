import time
import numpy
import threading as thrd# Use for email, webserver and maybe detecting object
import cv2 as cv
from Camera import Camera
from picamera import PiCamera
from logFiles import Log
from MessageFormat import Format
from Email import Emails
from Timer import Timer
from picamera.array import PiRGBArray

# Modify this and clean this up
cam1 = Camera(orginal_path, DateNTime)
original_path = '/home/pi/Desktop/FrontDoorDetectProject/'
filename = open((original_path+"Images/TestImage.jpg"), 'rb').read()# read image in binary mode
em = Emails(Format.message, filename, original_path)#creating a new object
timeNotDetect = Timer(120)
DateNTime = t1.TimeStamp()# Time stamp on the image
time.sleep(1)#let the camrera 'warm up'
'''
def Notify(image):# test this on the Pi
    if emailSent == True:
        t1.Relay()# timer for 3 minute duration to not spam the user w/ email
        emailSent = False
        pass
    else:
        # capture image from the camera & sent image
        cam1.SaveImage()# Using the Pi camera capturing image
        #cam1.CVSaveImage(image)# Using OpenCV capturing image
        em.sendMail()
        emailSent = True
        pass
'''

if __name__ == '__main__':
    # apply all multithreading applications here
    # Webserver and email are multithreaded
