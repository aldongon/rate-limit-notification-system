from src.gateway.gateway import Gateway
from src.rate_limit_rules_service.rules_service import RulesService
from src.notification_service.notification_store import NotificationStore

class NotificationService:
    """
    Notification service with rate limiting.
    """

    def __init__(self, gateway: Gateway, rules_service: RulesService, notification_store: NotificationStore):
        """
        Initializes the notification service.

        Args:
            gateway: Object that handles message sending.
            rules_service: RulesService instance.
            notification_store: NotificationStore
        """
        self.gateway = gateway
        self.rules = rules_service
        self.notification_store_service = notification_store

    def send(self, type_: str, user_id: str, message: str):
        """
        Sends a notification if the rate limit has not been exceeded.

        Args:
            notification_type: Type of the notification.
            user_id: ID of the recipient user.
            message: Content of the message.
        """
        must_send_message = self.rules.evaluate_rules(type_, user_id)
        if must_send_message:
            self.gateway.send(user_id, message)
            self.notification_store_service.save_notification(type_, user_id)
        else:
            print(f'Rate limit exceeded for user {user_id} on type {type_}')
