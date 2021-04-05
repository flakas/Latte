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
        if not self.is_available():
            return 0

        try:
            # Get the window pointer
            xlib = ctypes.cdll.LoadLibrary('libX11.so')
            display = xlib.XOpenDisplay(None) # None uses the DISPLAY env variable
            root_window = xlib.XDefaultRootWindow(display)

            # Get the screensaver info
            xss = ctypes.cdll.LoadLibrary('libXss.so')
            xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
            screensaver_info = xss.XScreenSaverAllocInfo()
            xss.XScreenSaverQueryInfo(display, root_window, screensaver_info)

            idle_time = screensaver_info.contents.idle/1000

            # Don't forget to clean up
            xss.XFree(screensaver_info)
            xss.XCloseDisplay(display)

            return idle_time
        except OSError as e:
            return 0

    def has_optional_dependencies(self):
        """ Checks whether the system has optional dependencies """
        try:
            xlib = ctypes.cdll.LoadLibrary('libX11.so')
            xss = ctypes.cdll.LoadLibrary('libXss.so')
            return True
        except OSError as e:
            return False
