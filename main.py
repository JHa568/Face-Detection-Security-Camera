#@author Jamie Ha
#created: 17/03/18
import time
import numpy
import threading# Use for email
import cv2 as cv
from flask import Flask, render_template, Response
from Camera import VideoCamera
from logFiles import Log
from MessageFormat import Format
from Email import Emails
'''
Inspired by Hacker Shack:
-   https://github.com/HackerShackOfficial/Smart-Security-Camera
'''
original_path = '/home/pi/Desktop/FrontDoorDetectProject/'
DateNTime = time.asctime(time.localtime(time.time()))# Time stamp on the image
logEmailSent = Log(DateNTime, original_path)
em = Emails(Format.message, original_path)# getting the image captured
piVCam = VideoCamera(original_path, DateNTime)
previousTime = 0# temporary storage of the time
app = Flask(__name__)# creation of Webserver

def get_PersonInFrame():
    # Stop sending emails of person after 9 minutes
    global previousTime
    while True:
        frame, found_person = piVCam.get_PersonInFrame()
        holdTimer = 540# 9 minute timer
        currentTime = time.time()
        if previousTime == 0:
            previousTime = currentTime
        else:
            while found_person and (currentTime - previousTime) < holdTimer:
                currentTime = time.time()
            em.runFunc("sendMail", piVCam.SaveImage())# Put the email sending into a thread
            previousTime = 0

@app.route('/')
def mainFunctions():
    # Title of the webpage
    templateData = {
        'title': 'Raspberry Pi Camera Feed'
    }
    return render_template('index.html', **templateData)# puts it into the main html file
'''
CamFeed and live_stream; from Hacker Shack
'''
def camFeed(camera):
    # Uploads the frame to webserver
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/live_stream')
def live_stream():# shows the live stream of the camera
    return Response(camFeed(video_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/live_stream/record_stream/<recording>')
def record():
    # recording the live stream here when button is pressed or not
    record = False
    message = ''
    if recording == "on":
        message = "Recording"
        record = True
    elif recording == "off":
        message = "Not recording"
        record = False

    templateData = {
        'message': message,
        'record': record
    }
    return render_template('index.html', **templateData)# put in the main html file

if __name__ == '__main__':
    t = threading.Thread(target=get_PersonInFrame, args=())
    t.daemon = True #
    t.start()
    app.run(host='0.0.0.0', debug=True)
