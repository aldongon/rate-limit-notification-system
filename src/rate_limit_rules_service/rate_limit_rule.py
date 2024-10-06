from datetime import timedelta


class RateLimitRule:
    def __init__(self, max_requests: int, time_window: timedelta):
        self.max_requests: int = max_requests
        self.time_window: timedelta = time_window
