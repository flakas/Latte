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

class IdleDetector:
    ''' Tracks whether the user is idle '''

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

    def has_optional_dependencies(self):
        """ Checks whether the system has optional dependencies """
        try:
            xlib = ctypes.cdll.LoadLibrary('libX11.so')
            xss = ctypes.cdll.LoadLibrary('libXss.so')
            return True
        except OSError as e:
            return False
