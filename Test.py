import time
import threading #Organise tasks
from picamera import PiCamera
from time import sleep, gmtime, strftime
from logFiles import Log

DateNTime = strftime("%Y-%m-%d@%H:%M:%S GMT", gmtime())


#Saving image
origDir = '/home/pi/Desktop/FrontDoorDetectProject/'
imageName = '/Images/%s.jpg' % (DateNTime)
log = Log(DateNTime, origDir)
log.File("Saved camera")#Log when email is sent

#activation of camera
camera = PiCamera()
camera.resolution = (900, 600)
camera.framerate = 30
camera.rotation = 180
#capture the image
def saveImage():    
    camera.annotate_text = DateNTime#imageDoc
    camera.capture(origDir+imageName)
#saveImage()

#preview livefeed
camera.start_preview()
camera.start_recording('/home/pi/Desktop/FrontDoorDetectProject/Video/video.h264')
sleep(10)
camera.stop_recording()
camera.stop_preview()#end livefeed

