from src.gateway.gateway import Gateway
from src.notification_service.notification_store import NotificationStore
from src.rate_limit_rules_service.rules_service import RulesService
from src.notification_service.notification_service import NotificationService



def main():
    """
    Entry point of the application.

    This function initializes the NotificationService and sends several notifications
    to demonstrate how rate limiting works.
    """
    gateway = Gateway()
    notification_store = NotificationStore()
    rules_service = RulesService(notification_store=notification_store)
    notification_service = NotificationService(
        gateway=gateway,
        rules_service=rules_service,
        notification_store=notification_store,
    )

    notification_service.send(type_='news', user_id='user', message='news_1')
    notification_service.send(type_='news', user_id='user', message='news_2')
    notification_service.send(type_='news', user_id='user', message='news_3')
    notification_service.send(type_='news', user_id='another user', message='news_1')
    notification_service.send(type_='update', user_id='user', message='update_1')


if __name__ == '__main__':
    main()
