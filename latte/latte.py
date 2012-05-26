import time
import subprocess
from TimeTracker import TimeTracker

def GetActiveWindowTitle():
        return subprocess.Popen(["xprop", "-id", subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=subprocess.PIPE).communicate()[0].strip().split()[-1], "WM_NAME"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].strip().split('"', 1)[-1][:-1]

sleepTime = 5
tracker = TimeTracker(sleepTime=sleepTime)

while True:
    try:
        title = GetActiveWindowTitle()
        tracker.log(title)
        print title, tracker.getWindowTime(title)
    except AttributeError:
        pass
    time.sleep(sleepTime);
