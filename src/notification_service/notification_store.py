from collections import deque
from datetime import datetime


class NotificationStore:
    def __init__(self):
        self.sent_notifications = {}

    def save_notification(self, type_, user_id):
        """
        Updates the record of sent notifications.

        Args:
            type_: Type of the notification.
            user_id: ID of the recipient user.
        """
        if user_id not in self.sent_notifications:
            self.sent_notifications[user_id] = {}
        if type_ not in self.sent_notifications[user_id]:
            self.sent_notifications[user_id][type_] = deque()
        self.sent_notifications[user_id][type_].append(datetime.now())

    def get_notifications_and_remove_older(self, type_, user_id, rule_time_window):
        """
        Retrieves the timestamps of sent notifications for
        a user and a notification type, and removes from
        storage the timestamps outside the rule_time_window.

        Args:
            type_: Type of the notification
            user_id: ID of the recipient user
            rule_time_window: Time window to keep timestamps
        """
        notifications_for_user = self.sent_notifications.get(user_id, {}).get(type_, deque())
        self._remove_older_notifications(notifications_for_user, rule_time_window)
        return notifications_for_user
    
    def _remove_older_notifications(self, notifications_for_user, rule_time_window):
        """
        Removes timestamps that are outside the rule_time_window.

        Args:
            - notifications_for_user (deque): A deque containing the timestamps of sent notifications.
            - rule_time_window (timedelta): A timedelta representing the time window to retain timestamps.
        """
        start_time = datetime.now() - rule_time_window
        while notifications_for_user and notifications_for_user[0] <= start_time:
            notifications_for_user.popleft()
