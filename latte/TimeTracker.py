import time
import json
import os

class TimeTracker:

    logs = {}

    def __init__(self, configs):
        self._sleepTime = configs['sleepTime']
        self._configs = configs

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

    def dumpLogs(self):
        target_path = os.path.join(self._configs['appPath'], self._configs['statsPath'])
        if not os.path.exists(target_path):
            os.makedirs(target_path)
        filename = str(int(time.time()))
        file_path = os.path.join(target_path, filename)

        file = open(file_path, 'w')
        file.write(json.dumps(self.getLogs(), indent=4))
        file.close()

        self.clearLogs()
        return filename


