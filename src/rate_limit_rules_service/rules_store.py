from datetime import timedelta

from src.rate_limit_rules_service.rate_limit_rule import RateLimitRule


class RuleStore:
    def __init__(self):
        """
        Service to store rate limit rules.
        """
        self._rules = {
            'status': RateLimitRule(max_requests=2, time_window=timedelta(minutes=1)),
            'news': RateLimitRule(max_requests=1, time_window=timedelta(days=1)),
            'marketing': RateLimitRule(max_requests=3, time_window=timedelta(hours=1)),
        }

    def get(self, type_):
        return self._rules.get(type_)
