class UsageTracker:
    def __init__(self, db, time_tracker, activity_tracker, tag_tracker, windows):
        self.db = db
        self.time_tracker = time_tracker
        self.activity_tracker = activity_tracker
        self.tag_tracker = tag_tracker
        self.windows = windows

    def track(self):
        if self.activity_tracker.is_inactive() and not self.time_tracker.is_tracking():
            # When inactivity has just been detected: log time once more to avoid an off-by-one.
            # Then, avoid tracking windows while inactive.
            return None

        active_window = self.windows.get_active()
        if not active_window:
            self.time_tracker.compensate_inactivity_and_stop_tracking(0)
            self.db.commit()
            return None

        log = self.time_tracker.track(active_window)
        self.tag_tracker.track(log)

        if self.activity_tracker.is_inactive():
            self.time_tracker.compensate_inactivity_and_stop_tracking(self.activity_tracker.get_inactivity_duration())

        self.db.commit()

        return log
