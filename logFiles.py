#from message import Format#Format of message
class Log:
    def __init__(self, DateNTime):
        self.DateNTime = DateNTime

    def File(self, message):# forwarding the parameter "message" to make a custom judgement of logging
        tempArray = []#store temporary logs in file
        del tempArray[:]
        logName = 'Logs/logsDetection'# location of logFile
        fileLog =  open(logName, 'r').read().split('\n')
        for evryLog in fileLog:
            tempArray.append(evryLog)# List all lines of txt
        noOfLogs = len(tempArray)# elements within a temporary array
        logString = "%s) %s: %s" % (noOfLogs, message, self.DateNTime)
        fileLog = open(logName, 'a')
        fileLog.write(str(logString)+'\n')
        fileLog.close()
