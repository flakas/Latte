class TimeTracker:

    logs = {}

    def __init__(self, sleepTime):
        self._sleepTime = sleepTime

    def getSleepTime(self):
        return self._sleepTime

    def getWindowTime(self, window):
        if window in self.logs.keys():
            return self.logs[window]
        else:
            return None

    def log(self, window):
        if not window in self.logs.keys():
            self.logs[window] = 0
        self.logs[window] += self.getSleepTime()

    def getLogs(self):
        return self.logs

    def clearLogs(self):
        self.logs = {}
        return
