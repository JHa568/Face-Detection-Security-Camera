import time
import smtplib
from logFiles import Log
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
'''
Have the email service run through this class
Have perminent email addresses usrname&passwrds in the module
Sources:
- https://stackoverflow.com/questions/13070038/attachment-image-to-send-by-mail-using-python
- http://naelshiab.com/tutorial-send-email-python/
- https://www.tutorialspoint.com/python3/python_sending_email.html
'''
# Make sure the this class is threaded/processed
class Emails:
    host = 'smtp.gmail.com'
    port = 465 # port for gmail
    login = 'e9261733@gmail.com'
    password = 'emailpassword'
    clients = ['e94282861@gmail.com']
    localTime = time.asctime(time.localtime(time.time()))

    def __init__(self, message):
        self.message = message
        self.imageFileName = imageFileName
        self.path = path
        #The message of the email
    def sendVideo(self):
        # find a way to send a video over the gmail webserver
        print('SentVideo')
    def sendMail(self, frame):
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
            print('Sucessfully sent!!!! ' + str(Emails.localTime))
            lgEmail.File("Email[SENT]")# log: sent email
            server.quit()

        except:
            ErrorMess = "Email: Connection Error or SSL Error has occured"
            print(ErrorMess)# get rid of this
            lgEmail.File("Email[ERROR]")# log: email not sent
            pass
