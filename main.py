#@author Jamie Ha
#created: 17/03/18
import time
import numpy as np
import threading
import cv2 as cv
from flask import Flask, render_template, Response, abort, request
from Camera import VideoCamera
from logFiles import Log
from MessageFormat import Format
from Email import Emails
'''
Inspired by Hacker Shack:
-   https://github.com/HackerShackOfficial/Smart-Security-Camera
'''
DateNTime = time.asctime(time.localtime(time.time()))# Time stamp on the image
logAction = Log(DateNTime)
em = Emails(Format.message)# getting the image captured
piVCam = VideoCamera(DateNTime)
previousTime = 0# temporary storage of the time
app = Flask(__name__)# creation of Webserver
record = None
def get_PersonInFrame():
    # Stop sending emails of person after 9 minutes
    global timeCaptured
    global record
    timeCaptured = time.time()
    threadLock = threading.Lock()
    while True:
        try:
            frame, found_person = piVCam.get_PersonInFrame()
            holdTimer = 240# 4min timer
            currentTime = time.time()
            if found_person and (currentTime - timeCaptured) >= holdTimer:
                print("Sending")
                threadLock.acquire()
                em.sendMail(piVCam.get_frame())
                threadLock.release()
                print("Done!!!")
                timeCaptured = currentTime
        except:
            print("Error with detecting person")
            logAction.File("[Error] with detecting person")
            break

@app.route('/')
def mainFunctions():
    # Title of the webpage
    templateData = {
        'title': 'Raspberry Pi Camera Feed'
    }
    return render_template('index.html', **templateData)# puts it into the main html file
'''
CamFeed and live_stream: from Hacker Shack
'''
def camFeed():
    # Uploads the frame to webserver
    while True:
        #frame, _ = piVCam.get_PersonInFrame()#with rect
        frame =  piVCam.get_frame()#without rect
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/live_stream')
def live_stream():# shows the live stream of the camera
    return Response(camFeed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/live_stream/record_stream/<recording>')
def Record(recording):# Test the logic of this function
    # recording the live stream here when button is pressed or not
    global record
    message = ""
    #threadLock = threading.Lock()
    locked = False
    if recording == "on":
        message = "Finished Recording"
        record = True
        print("Thread Acquired.............")
        recThread = threading.Thread(target=piVCam.RecordStream, args=(record,))
        recThread.start()
        recThread.join()
        print("Thread Finished.............")
    elif recording == "off":
        message = "Press once to record video for 5 mins"
        record = False
        print("Resetted..........")

    templateData = {
        'message': message,
        'record': record
    }
    return render_template('index.html', **templateData)# put in the main html file

if __name__ == '__main__':
    t = threading.Thread(target=get_PersonInFrame, args=())
    t.daemon = True
    t.start()
    app.run(host='0.0.0.0', debug=False)
