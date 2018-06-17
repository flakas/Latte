import subprocess
import ctypes
import os

class XScreenSaverInfo(ctypes.Structure):
    """ typedef struct { ... } XScreenSaverInfo; """
    _fields_ = [('window', ctypes.c_ulong),  # screen saver window
                ('state', ctypes.c_int),  # off,on,disabled
                ('kind', ctypes.c_int),  # blanked,internal,external
                ('since', ctypes.c_ulong),  # milliseconds
                ('idle', ctypes.c_ulong),  # milliseconds
                ('event_mask', ctypes.c_ulong)]  # events

class Screen:
    def __init__(self):
        pass

    def is_available(self):
        return 'DISPLAY' in os.environ

    def get_idle_time(self):
        """ Returns idle time in seconds if available or raises exception """
        if not is_available():
            return 0

        if not self.xss_info:
            self._get_screen()

        self.xss.XScreenSaverQueryInfo(self.dpy, self.root, self.xss_info)
        return self.xss_info.contents.idle/1000

    def _get_screen(self):
        try:
            xlib = ctypes.cdll.LoadLibrary('libX11.so')
            self.dpy = xlib.XOpenDisplay(os.environ['DISPLAY'])
            self.root = xlib.XDefaultRootWindow(self.dpy)
            self.xss = ctypes.cdll.LoadLibrary('libXss.so')
            self.xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
            self.xss_info = self.xss.XScreenSaverAllocInfo()
        except OSError as e:
            self.inactive_tracking_available = False

    def get_active_window_data(self):
        """ Fetches active window title using xprop. """
        try:
            active = subprocess.Popen(["xprop", "-root", "_NET_ACTIVE_WINDOW"],
                                      stdout=subprocess.PIPE)
            active_id = active.communicate()[0].strip().split()[-1]
            window = subprocess.Popen(["xprop", "-id", active_id, "WM_NAME"],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            title = (window.communicate()[0]).decode('utf-8').strip().split('"', 1)[-1][:-1]
            wm_class = subprocess.Popen(["xprop", "-id", active_id, "WM_CLASS"], 
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE)
            wm_class_message = wm_class.communicate()[0].decode('utf-8').strip().split('"')
            window_class = wm_class_message[1]
            window_instance = wm_class_message[3]
            return [title, window_class, window_instance]
        except Exception as e:
            print(e)
            return [u'', u'', u'']

    def has_required_dependencies(self):
        """ Checks whether the system has required dependencies """
        try:
            subprocess.call(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=subprocess.PIPE)
            return True
        except OSError as e:
            return False

    def has_optional_dependencies(self):
        """ Checks whether the system has optional dependencies """
        try:
            xlib = ctypes.cdll.LoadLibrary('libX11.so')
            xss = ctypes.cdll.LoadLibrary('libXss.so')
            return True
        except OSError as e:
            return False
