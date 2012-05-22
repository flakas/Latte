import time
import subprocess

def GetActiveWindowTitle():
        return subprocess.Popen(["xprop", "-id", subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=subprocess.PIPE).communicate()[0].strip().split()[-1], "WM_NAME"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0].strip().split('"', 1)[-1][:-1]

while True:
    try:
        #title = wnck.screen_get_default().get_active_window().get_name()
        title = GetActiveWindowTitle()
        print title
    except AttributeError:
        pass
    time.sleep(1);

