import time
import subprocess

def GetActiveWindowTitle():
        return subprocess.Popen(["xprop", "-id", subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=subprocess.PIPE).communicate()[0].strip().split()[-1], "WM_NAME"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].strip().split('"', 1)[-1][:-1]

timeSpent = {}

sleepTime = 5

while True:
    try:
        title = GetActiveWindowTitle()
        if not title in timeSpent.keys():
            timeSpent[title] = 0
        timeSpent[title] += sleepTime
        print title, timeSpent[title]
    except AttributeError:
        pass
    time.sleep(sleepTime);

