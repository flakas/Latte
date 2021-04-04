import subprocess

class ActiveWindow:
    def __init__(self, title, window_class, instance):
        self.title = title
        self.window_class = window_class
        self.instance = instance

class Windows:
    def get_active(self):
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

            return ActiveWindow(title, window_class, window_instance)
        except Exception as e:
            print(e)
            return ['', '', '']

    def has_required_dependencies(self):
        """ Checks whether the system has required dependencies """
        try:
            subprocess.call(["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=subprocess.PIPE)
            return True
        except OSError as e:
            return False
