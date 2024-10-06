from datetime import datetime
from collections import deque

from src.rate_limit_rules_service.rules_store import RuleStore
from src.notification_service.notification_store import NotificationStore


class RulesService:
    def __init__(self, notification_store: NotificationStore):
        self.notification_store_service = notification_store
        self.rules_store = RuleStore()

    def evaluate_rules(self, type_: str, user_id: str) -> bool:
        """
        Evaluates whether a notification can be sent according to the rules.

        Args:
            type_: Type of the notification.
            user_id: ID of the recipient user.

        Returns:
            bool: True if the notification can be sent, False otherwise.
        """
        rule = self.rules_store.get(type_)

        # If there are no rule defined for type_, send the message
        if not rule:
            return True
        
        notifications_for_user = self.notification_store_service.get_notifications_and_remove_older(type_, user_id, rule.time_window)

        if len(notifications_for_user) < rule.max_requests:
            return True
        return False
