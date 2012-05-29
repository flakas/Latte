import time
import subprocess
import os
import atexit

from TimeTracker import TimeTracker
from Categories.Categorizer import Categorizer

def GetActiveWindowTitle():
        return subprocess.Popen(["xprop", "-id", subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=subprocess.PIPE).communicate()[0].strip().split()[-1], "WM_NAME"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].strip().split('"', 1)[-1][:-1]

sleepTime = 5
lattePath = '~/.latte/'

configs = {}
configs['appPath'] = lattePath
configs['statsPath'] = 'stats/'
configs['appPath'] = os.path.expanduser(configs['appPath'])
configs['sleepTime'] = sleepTime
configs['autosaveTime'] = 3600
tracker = TimeTracker(configs=configs)

# Catch exit signal and force save logs
atexit.register(tracker.dumpLogs)

if not os.path.exists(lattePath):
    os.makedirs(lattePath)

duration = 0
while True:
    try:
        title = GetActiveWindowTitle()
        tracker.log(title)
        stats = tracker.getWindowStats(title)
        print title, stats['category'], stats['project'], stats['time']
    except AttributeError:
        pass

    time.sleep(configs['sleepTime']);
    duration += configs['sleepTime']
    if duration >= configs['autosaveTime']:
        duration = 0
        tracker.dumpLogs()
