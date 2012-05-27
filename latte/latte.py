import time
import subprocess
import os
from TimeTracker import TimeTracker

def GetActiveWindowTitle():
        return subprocess.Popen(["xprop", "-id", subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=subprocess.PIPE).communicate()[0].strip().split()[-1], "WM_NAME"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].strip().split('"', 1)[-1][:-1]

sleepTime = 5
lattePath = '~/.latte/'

configs = {}
configs['appPath'] = lattePath
configs['statsPath'] = 'stats/'
configs['appPath'] = os.path.expanduser(configs['appPath'])
tracker = TimeTracker(sleepTime=sleepTime, configs=configs)

if not os.path.exists(lattePath):
    os.makedirs(lattePath)

while True:
    try:
        title = GetActiveWindowTitle()
        tracker.log(title)
        print title, tracker.getWindowTime(title)
    except AttributeError:
        pass
    time.sleep(sleepTime);
