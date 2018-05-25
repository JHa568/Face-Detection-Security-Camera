from Email import Emails

class Format:
    #breakers to split text up
    breaker0 = '#' * 30
    breaker1 = '-' * 40

    #Sentences that are broken up to create the full message
    sen1 = "'This is a message to alert the user that there has been a security breach.'"
    sen2 = "A person has been detected at the front door"
    sen3 = "Press the link below to see the live feed"

    #Format of the message:
    message = '''
SECURITY UPDATE: (%s):\n
%s
From: [%s]
%s
To: %s
%s\n
%s\n\n%s. %s.\n
Link to live feed: www.google.com [example of link]
    ''' % (Emails.localTime, breaker0, Emails.login, breaker1, Emails.clients, breaker0,
    sen1, sen2, sen3)
