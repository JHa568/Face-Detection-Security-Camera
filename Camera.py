from imutils.video import VideoStream# to be more efficient directly call 'PiVideoStream'
import cv2 as cv
import numpy as np
import imutils
import time

pxl = 256
res = (pxl,pxl)
fps = 25
haarcascadeHeadNShoulders = "HS.xml"# Use a different model

class VideoCamera(object):
    def __init__(self, original_path, date_n_time):
        self.original_path = orginal_path
        self.date_n_time = date_n_time
        self.picam = VideoStream(usePiCamera=True, resolution=res, framerate=fps).start()
        self.picam = imutils.rotate(self.picam, angle=180)# rotates the camera 180 degrees
        print("{CPU INFO}: Camera warming up......")
        time.sleep(2)
        print("Starting......")

    def SaveImage(self):
        #Capture the image
        frame = self.picam.read()
        _, jpeg = cv.imencode(".jpg", frame)
        return jpeg.tobytes()

    def RecordStream(self, buttonPressed):
        #Record the stream
        frame = self.picam.read()
        frame = imutils.resize(frame, width=pxl)
        fourcc = cv.VideoWriter_fourcc("MJPG")# video compression format and color/pixel format of video
        (h, w) = frame.shape[:2]
        writer = cv.VideoWriter("Video/Video.avi", fourcc, fps, (w, h), True)
        writer.write(frame)# Test this module if it works or not
        if buttonPressed == True:
            writer.released()
            pass

    def get_Person(self):
        #find the person in the stream
        frame = self.picam.read()# get the camera from the stream
        frame = imutils.resize(frame, width=pxl)
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        personDetected = False
        haarcascadeClassifier = cv.CascadeClassifier(haarcascadeHeadNShoulders)
        detectPerson = haarcascadeClassifier.detectMultiScale(gray,
                                                          scaleFactor=1.2,
                                                          minNeighbors=3,
                                                          minSize=(30,30),
                                                          flags=cv.CASCADE_SCALE_IMAGE)
        if len(detectPerson) > 0:
            personDetected = True# if detected return True

        for (x,y,w,h) in detectPerson:
            cv.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

        _, jpeg = cv.imencode('.jpg', frame)# image of frame w/ rectangle

        return (jpeg.tobytes(), personDetected)
