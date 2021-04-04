class UsageTracker:
    def __init__(self, time_tracker, activity_tracker, windows):
        self.time_tracker = time_tracker
        self.activity_tracker = activity_tracker
        self.windows = windows

    def track(self):
        if self.activity_tracker.is_inactive() and not self.time_tracker.is_tracking():
            # When inactivity has just been detected: log time once more to avoid an off-by-one.
            # Then, avoid tracking windows while inactive.
            return None

        active_window = self.windows.get_active()
        log = self.time_tracker.track(active_window)

        if self.activity_tracker.is_inactive():
            self.time_tracker.compensate_inactivity_and_stop_tracking(self.activity_tracker.get_inactivity_duration())

        return log
