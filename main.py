import time
import numpy
import multiprocessing as process# both multithreading and processing, simultaneous operation
import threading as silk#Organise tasks
import cv2 as cv
from Camera import Camera
from picamera import PiCamera
from logFiles import Log
from MessageFormat import Format
from Email import Emails
from Timer import Timer
from picamera.array import PiRGBArray

haarcascadeHeadnShoulders = 'HS.xml'# name of haarcascade
camera = PiCamera()
camera.resolution = (250, 250)# resolution of the camera
camera.rotation = 180
camera.framerate = 25
rawCapture = PiRGBArray(camera, size=(250, 250))
cam1 = Camera(orginal_path, DateNTime)

original_path = '/home/pi/Desktop/FrontDoorDetectProject/'
filename = open((original_path+"Images/TestImage.jpg"), 'rb').read()# read image in binary mode
em = Emails(Format.message, filename, original_path)#creating a new object

timeNotDetect = Timer(120)
DateNTime = t1.TimeStamp()# Time stamp on the image
time.sleep(1)#let the camrera 'warm up'

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

def DetectPerson():
    for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
        image = frame.array
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        haarcascadeClassifier = cv.CascadeClassifier(haarcascadeHeadnShoulders)
        personDetect = haarcascadeClassifier.detectMultiScale(gray,
                        scaleFactor=1.2,
                        minNeighbors=3,
                        minSize=(100,100),
                        flags=cv.CASCADE_SCALE_IMAGE)#change
        # multiprocess the person detection
        for (x, y, w, h) in personDetect:
            cv.rectangle(image, (x,y), (w+x, h+y), (0,255,0), 2)# border around the object
            Notify(image)# Notify the owner of the house, 1 thread

        cv.imshow("Frame", image)# show a video in colour

        # This key mechanism should be obsolete
        key = cv.waitKey(1) & 0xFF
        rawCapture.truncate(0)

        if key == ord("q"):# when pressed 'q' on keyboard
            break# end program


if __name__ == '__main__':
    # apply all multithreading applications here,
    DetectPerson()# 2 threads, multiprocessing
    # Webserver and email are multithreaded
