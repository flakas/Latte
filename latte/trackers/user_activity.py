class UserActivityTracker(object):
    """ Tracks how long the user has been inactive for """

    def __init__(self, idle_detector, inactivity_threshold):
        self.idle_detector = idle_detector
        self.inactivity_threshold = inactivity_threshold

    def is_tracking_available(self):
        """ Checks whether inactivity tracking is available """
        return self.idle_detector.is_available()

    def is_inactive(self):
        """ Checks whether the user is inactive based on inactivity threshold """

        return self.get_inactivity_duration() >= self.inactivity_threshold

    def get_inactivity_duration(self):
        try:
            if not self.idle_detector.is_available():
                return 0

            return self.idle_detector.get_idle_time()
        except Exception as e:
            return 0
