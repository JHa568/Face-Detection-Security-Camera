#@author Jamie Ha
#created: 17/03/18
import time
import numpy as np
import threading
import cv2 as cv
import imutils
from flask import Flask, render_template, Response, abort, request
from Camera import VideoCamera
from logFiles import Log
from MessageFormat import Format
from Email import Emails
'''
Acknowledgements:
-   Hacker Shack
-   PyImageSearch blog posts
-   StackOverflow community
'''
record = None
message = ""
DateNTime = time.asctime(time.localtime(time.time()))# Time stamp on the image
logAction = Log(DateNTime)# logs: errors or successes
em = Emails(Format.message)# getting the image captured
piVCam = VideoCamera(DateNTime, record)
previousTime = 0# temporary storage of the time
app = Flask(__name__)# creation of Webserver
Threading = False

def get_PersonInFrame():
    # Stop sending emails of person after 9 minutes
    global timeCaptured
    timeCaptured = time.time()
    threadLock = threading.Lock()
    print("Person in frame" + str(record))
    while True:
        while record != True:
            try:
                frame, found_person = piVCam.get_PersonInFrame()
                holdTimer = 10# 4min timer
                currentTime = time.time()
                if found_person and (currentTime - timeCaptured) >= holdTimer:
                    print("Sending")
                    threadLock.acquire()
                    em.sendMail(piVCam.get_frame())# send frame to client
                    threadLock.release()
                    print("Done!!!")
                    timeCaptured = currentTime
            except:
                print("Error with detecting person")
                logAction.File("[Error] Detecting person")
                break

@app.route('/')
def mainFunctions():
    # Title of the webpage
    templateData = {
        'title': 'Raspberry Pi Camera Feed'
    }
    return render_template('index.html', **templateData)# puts it into the main html file
'''
CamFeed and live_stream activation: from Hacker Shack
'''
def camFeed():
    # Uploads the frame to webserver
    while True:
        #frame, _ = piVCam.get_PersonInFrame()# with rectangle outline
        frame =  piVCam.get_frame()#without rectangle outline
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/live_stream')
def live_stream():# shows the live stream of the camera
    return Response(camFeed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def RecordStream():
    # records the video stream
    try:
        fourcc = cv.VideoWriter_fourcc(*"MJPG")# video compression format and color/pixel format of video
        writer = None
        prevTime = time.time()
        currentTime = 0
        while (currentTime - prevTime) <= 300 and record == True:
            # record for 5 minutes or until the not recording hyperlink is pressed
            currentTime = time.time()
            frame = piVCam.get_frame0()# gets the frame from stream
            frame = imutils.rotate(frame, angle=180)
            frame = imutils.resize(frame, width=256)
            if writer == None:
                # initate the setting for writer when recording module is activated
                (h, w) = frame.shape[:2]
                writer = cv.VideoWriter("Video/Video.avi", fourcc, 25, (w, h), True)
            output = np.zeros((h,w,3), dtype='uint8')
            output[0:h, 0:w] = frame
            writer.write(output)# Test this module if it works or not
        writer.release()# stop writing to file
        record = False# leave this here
        message = "Not Recording"# get rid of this if you dont need it
        logAction.File("[Sucess]: Recorded Video")# log it is recording
        print("Not Recording")
    except:
        # This will occur when an error has occured
        logAction.File("[Error]: Recording Video")
        record = False
        message = "Not Recording"
        print("Error has occured")

@app.route('/live_stream/record_stream/<recording>')
def Record(recording):
    # recording the live stream here when button is pressed or not
    global record
    global message
    recThread = threading.Thread(target=RecordStream)
    if recording == "on":
        message = "Recording"
        record = True
        recThread.start()# recording has started

    elif recording == "off":
        message = "Not Recording"
        record = False# flag to terminates live stream

    templateData = {
        'message': message,
        'record': record
    }

    return render_template('index.html', **templateData)# put in the main html file

if __name__ == '__main__':
    t = threading.Thread(target=get_PersonInFrame)
    t.daemon = True
    t.start()# start getting people from the frame
    app.run(host='0.0.0.0', debug=False)
