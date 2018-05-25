import time

class Timer:
    def __init__(self, timeLimit):
        self.timeLimit = timeLimit

    def TimeStamp(self):
        localTime = time.asctime(time.localtime(time.time()))
        return localTime# computer localTime

    def Relay(self):
        previous = 0
        timeLimit = self.timeLimit# time limit
        ended = False
        while True:
            currentTime = time.time()# current time in seconds
            if previous == 0:
                previous = currentTime
            else:
                while(currentTime - previous) < timeLimit:
                    currentTime = time.time()
                    ended = False
                    # Processing Stops
                    return ended
                previous = currentTime
                ended = True
                return ended
                # Processors continue
                if ended == True:
                    return ended
                    break
