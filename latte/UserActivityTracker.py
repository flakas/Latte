class UserActivityTracker(object):

    def __init__(self, time_tracker, config, screen):
        self.time_tracker = time_tracker
        self.config = config
        self.screen = screen
        self.user_inactive = False

    def is_tracking_available(self):
        """ Checks whether inactivity tracking is available """
        return self.screen.is_available()

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
        try:
            if not self.screen.is_available():
                return 0

            return self.screen.get_idle_time()
        except Exception as e:
            return 0
