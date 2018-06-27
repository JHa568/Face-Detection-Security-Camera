#@author Jamie Ha
#created: 17/03/18
import threading
import time
import smtplib
from logFiles import Log
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
'''
CHECK BEFORE THE COMPLETED PROJECT:
        - Test if the threading of the email and main files work together
        - Test if it records and sends the video
Have the email service run through this class
Have perminent email addresses usrname&passwrds in the module
Sources:
- https://stackoverflow.com/questions/13070038/attachment-image-to-send-by-mail-using-python
- http://naelshiab.com/tutorial-send-email-python/
- https://www.tutorialspoint.com/python3/python_sending_email.html
'''

# The email is threaded for optimal efficiency.
# Check if this module works
class Emails(threading.Thread):#fully thread this module
    host = 'smtp.gmail.com'
    port = 465# port for gmail
    login = 'e9261733@gmail.com'# email login for entering in the gmail webserver
    password = 'emailpassword'
    clients = ['e94282861@gmail.com']# recipients
    localTime = time.asctime(time.localtime(time.time()))

    def __init__(self, message=None):
        threading.Thread.__init__(self)# threading the email module
        self.message = message
        #The message of the email

    def sendVideo(self):# create button to send mail
        # Send a video over through email
        lgEmail = Log(Emails.localTime)
        mainMessage = 'Video Recorded:- ' + Emails.localTime
        filename = 'Video.avi'
        try:
            msg = MIMEMultipart()
            msg['Subject'] = mainMessage
            msg['From'] = Emails.login# login into the email
            msg['To'] = ', '.join(Emails.clients)
            text = MIMEText(mainMessage)
            video = MIMEBase('application', "octet-stream")
            file = open('Video/'+filename, "rb")# read in binary format
            video.set_payload(file.read())
            encoders.encode_base64(video)# encode the video in a sendable format
            video.add_header("Content-Disposition", 'attachment; filename"%s"' % filename)# make it as a readable/accessible file to the recipient
            msg.attach(video)# attach video (encoded) to email
            server = smtplib.SMTP_SSL(Emails.host, Emails.port)
            server.login(Emails.login, Emails.password)
            server.sendmail(Emails.login, Emails.clients, msg.as_string())#sends the email (with attachmemnts and texts)
            lgEmail.File("SendingVideo[SENT]")# log: sent email
            server.quit()
        except:
            lgEmail.File("SendingVideo[ERROR]")# log: email not sent
            pass

    def sendMail(self, frame):
        # send the email with frame
        lgEmail = Log(Emails.localTime)
        try:
            msg = MIMEMultipart()# sending multiple attachments e.g. images, texts
            msg['Subject'] = 'PERSON AT FRONT DOOR:-  ' + Emails.localTime
            msg['From'] = Emails.login# login into the email
            msg['To'] = ', '.join(Emails.clients)
            text = MIMEText(self.message)# txt of the email
            image = MIMEImage(frame)# image of the email
            msg.attach(text)#send text over email
            msg.attach(image)#attach the image to the email
            server = smtplib.SMTP_SSL(Emails.host, Emails.port)
            server.login(Emails.login, Emails.password)
            server.sendmail(Emails.login, Emails.clients, msg.as_string())#sends the email (with attachmemnts and texts)
            lgEmail.File("Email[SENT]")# log: sent email
            server.quit()
        except:
            lgEmail.File("SendingEmail [ERROR]")# log: email not sent
            pass

'''
Status:
runFunc:
- Test if the thread releases or not
sendVideo func:
- Testing this function
sendMail func:
- Make sure this works
'''
