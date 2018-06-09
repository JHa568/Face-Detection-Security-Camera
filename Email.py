import threading
import time
import smtplib
from logFiles import Log
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
'''
Have the email service run through this class
Have perminent email addresses usrname&passwrds in the module
Sources:
- https://stackoverflow.com/questions/13070038/attachment-image-to-send-by-mail-using-python
- http://naelshiab.com/tutorial-send-email-python/
- https://www.tutorialspoint.com/python3/python_sending_email.html
'''
# Make sure the this class is threaded/processed
class Emails(threading.Thread):
    host = 'smtp.gmail.com'
    port = 465# port for gmail
    login = 'e9261733@gmail.com'
    password = 'emailpassword'
    clients = ['e94282861@gmail.com']
    localTime = time.asctime(time.localtime(time.time()))

    def __init__(self, message):
        threading.Thread.__init__(self)# threading the email module
        self.message = message
        self.imageFileName = imageFileName
        self.path = path
        #The message of the email
    '''
    def sendVideo(self, orginal_path):
        # find a way to send a video over the gmail webserver
        threadLock.acquire()
        mainMessage = 'Video Recorded:- ' + Emails.localTime
        filename = 'Video.avi'
        try:
            msg = MIMEMultipart()
            msg['Subject'] = mainMessage
            msg['From'] = Emails.login# login into the email
            msg['To'] = ', '.join(Emails.clients)
            text = MIMEText(mainMessage)
            video = MIMEBase('application', "octet-stream")
            file = open(orginal_path+filename, "rb")
            video.set_payload(file.read())
            Encoders.encode_base64(video)
            msg.attach(video)
            server = smtplib.SMTP_SSL(Emails.host, Emails.port)
            server.login(Emails.login, Emails.password)
            server.sendmail(Emails.login, Emails.clients, msg.as_string())#sends the email (with attachmemnts and texts)
            lgEmail.File("Video[SENT]")# log: sent email
            server.quit()
        except:
            lgEmail.File("SendingVideo[ERROR]")# log: email not sent
            pass
        threadLock.release()
        thread.join()
    '''
    def sendMail(self, frame):
        threadLock.acquire()
        lgEmail = Log(Emails.localTime, self.path)
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
        threadLock.release()
        thread.join()
