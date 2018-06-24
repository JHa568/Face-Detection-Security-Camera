# @author Jamie Ha
# created: 17/03/18
from imutils.video import VideoStream# to be more efficient directly call 'PiVideoStream'
from Email import Emails
import cv2 as cv
import numpy as np
import imutils
import time

pxl = 256
res = (pxl,pxl)
fps = 25
haarcascade = "haarcascade_frontalface.xml"# Use a different model

class VideoCamera(object):
    def __init__(self, date_n_time):
        self.date_n_time = date_n_time
        self.picam = VideoStream(usePiCamera=True, resolution=(256,256), framerate=25).start()
        print("{CPU INFO}: Camera warming up......")
        time.sleep(2)
        print("Starting......")

    def get_frame(self):
        # Captures the image
        frame = self.picam.read()
        frame = imutils.rotate(frame, angle=180)
        _, jpeg = cv.imencode(".jpg", frame)
        return jpeg.tobytes()

    def RecordStream(self, record):
        # Record the live stream
        #em = Emails()
        fourcc = cv.VideoWriter_fourcc(*"MJPG")# video compression format and color/pixel format of video
        writer = None
        prevTime = time.time()
        currentTime = 0
        while (currentTime - prevTime) <= 300:
            # record for 5 mins
            currentTime = time.time()
            frame = self.picam.read()# gets the frame from stream
            frame = imutils.rotate(frame, angle=180)
            frame = imutils.resize(frame, width=pxl)
            if writer == None:
                (h, w) = frame.shape[:2]
                writer = cv.VideoWriter("Video/Video.avi", fourcc, fps, (w, h), True)
            output = np.zeros((h,w,3), dtype='uint8')
            output[0:h, 0:w] = frame
            writer.write(output)# Test this module if it works or not

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
