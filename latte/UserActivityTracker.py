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


class UserActivityTracker(object):

    def __init__(self, time_tracker, config):
        self.time_tracker = time_tracker
        self.config = config
        self.user_inactive = False
        self.inactive_tracking_available = 'DISPLAY' in os.environ
        if self.inactive_tracking_available:
            try:
                xlib = ctypes.cdll.LoadLibrary('libX11.so')
                self.dpy = xlib.XOpenDisplay(os.environ['DISPLAY'])
                self.root = xlib.XDefaultRootWindow(self.dpy)
                self.xss = ctypes.cdll.LoadLibrary('libXss.so')
                self.xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
                self.xss_info = self.xss.XScreenSaverAllocInfo()
            except OSError, e:
                self.inactive_tracking_available = False

    def is_inactive_tracking_available(self):
        """ Checks whether inactivity tracking is available """
        return self.inactive_tracking_available

    def is_user_inactive(self):
        """ Checks whether the user is inactive based on inactivity threshold """
        inactivity_duration = self.get_inactivity_time()
        if inactivity_duration > self.config.get('user_inactive_threshold'):
            if not self.user_inactive:
                self.time_tracker.reduce_time(inactivity_duration)
                self.user_inactive = True
        else:
            self.user_inactive = False
        return self.user_inactive

    def get_inactivity_time(self):
        if self.is_inactive_tracking_available():
            self.xss.XScreenSaverQueryInfo(self.dpy, self.root, self.xss_info)
            return self.xss_info.contents.idle/1000
        else:
            return 0
