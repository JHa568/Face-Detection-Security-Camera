# @author Jamie Ha
# created: 17/03/18
from imutils.video import VideoStream# to be more efficient directly call 'PiVideoStream'
from Email import Emails
import cv2 as cv
import numpy as np
import imutils
import time
import threading

pxl = 256
res = (pxl,pxl)
fps = 25
haarcascade = "haarcascade_frontalface.xml"# Use a different model
recThreadAlive = False
activeRecording = False

class VideoCamera(object):
    
    def __init__(self, date_n_time, activeRecording):
        self.date_n_time = date_n_time
        self.activeRecording = activeRecording
        self.picam = VideoStream(usePiCamera=True, resolution=(400,304), framerate=25).start()
        # ^ Activate the camera
        print("{CPU INFO}: Camera warming up......")
        time.sleep(2)
        print("Starting......")

    def get_frame(self):
        # Captures the image
        frame = self.picam.read()# get frame
        frame = imutils.rotate(frame, angle=180)
        _, jpeg = cv.imencode(".jpg", frame)# convert the frame to a jpeg file
        return jpeg.tobytes()

    def get_frame0(self):
        frame = self.picam.read()
        return frame
    
    def get_PersonInFrame(self):
        # find the person in the camara stream
        frame = self.picam.read()
        frame = imutils.rotate(frame, angle=180)
        frame = imutils.resize(frame, width=pxl)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        personDetected = False
        haarcascadeClassifier = cv.CascadeClassifier(haarcascade)# face detection
        detectPerson = haarcascadeClassifier.detectMultiScale(gray,
                                                          scaleFactor=1.2,
                                                          minNeighbors=3,
                                                          minSize=(30,30),
                                                          flags=cv.CASCADE_SCALE_IMAGE)
        if len(detectPerson) > 0:# finding face on the camera
            personDetected = True# return found face

        for (x,y,w,h) in detectPerson:
            cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
            
        _, jpeg = cv.imencode('.jpg', frame)# image of frame w/ rectangle

        return (jpeg.tobytes(), personDetected)
