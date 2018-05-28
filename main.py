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
original_path = '/home/pi/Desktop/FrontDoorDetectProject/'
DateNTime = time.asctime(time.localtime(time.time()))# Time stamp on the image
logEmailSent = Log(DateNTime, original_path)
em = Emails(Format.message)# getting the image captured
piVCam = VideoCamera(orginal_path, DateNTime)
ended = False

def get_PersonInFrame():
    global ended
    while True:
        frame, found_person = piVCam.get_PersonInFrame()
        timeInterval = 540# 9 minutes timer
        currentTime = time.time()
        previousTime = 0
        if previousTime == 0:
            previousTime = currentTime
        else:
            while found_person and (currentTime - previousTime) < timeInterval:
                currentTime = time.time()
            previousTime = currentTime
            ended = True
            if ended = True:
                logEmailSent.File("Email Sent")# test this under threading
                em.sendmail(piVCam.SaveImage())# Put the email sending into another thread
                previousTime = 0
                break


if __name__ == '__main__':
    get_PersonInFrame()# thread this
    # apply all multithreading applications here
    # Webserver and email are multithreaded
