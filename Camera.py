import time
import cv2 as cv
from picamera import PiCamera
from logFiles import Log
from Timer import Timer

t1 = Timer(10)
class Camera:
    imageSaved = "Image Saved"
    startRecording = "Start Recording"
    stopRecording = "Stopped Recording"

    def __init__(self, original_path, DateNTime):
        self.DateNTime = DateNTime
        self.original_path = original_path

    def CVSaveImage(self, frame):# using OpenCV to capture image
        img_name = "/Images/TestImage.jpg"
        cv2.imwrite(self.original_path+img_name, frame)

    def SaveImage(self):
        logImage = Log(self.DateNTime, self.original_path)
        camera = PiCamera()
        camera.resolution = (400, 400)#resolution of image
        camera.rotation = 180
        camera.annotate_text_size = 20
        #Saving image
        imageName = '/Images/TestImage.jpg'
        logImage.File(Camera.imageSaved)#Log for saving image
        camera.annotate_text = self.DateNTime#imageDoc
        camera.capture(self.original_path+imageName)

    def Record(self, webserverButtonRequest):#Revise on this
        logRecord = Log(self.DateNTime, self.original_path)
        camera = PiCamera()
        camera.resolution = (400, 400)
        camera.framerate = 30
        camera.rotation = 180
        camera.annotate_text_size = 20
        camera.annotate_text = self.DateNTime
        #Record Video
        if webserverButtonRequest == True:# want to record video
            videoName = '/Video/video.h264
            logRecord.File(Camera.startRecording)
            camera.start_preview()
            camera.start_recording(self.original_path+videoName)
        #use a "stop" recording function
        else:
            try:
                camera.stop_recording()
                camera.stop_preview()
            except:
                pass
