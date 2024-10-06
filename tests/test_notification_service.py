from unittest import TestCase
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

from src.rate_limit_rules_service.rules_service import RulesService
from src.rate_limit_rules_service.rules_store import RuleStore
from src.notification_service.notification_store import NotificationStore
from src.notification_service.notification_service import NotificationService
from src.gateway.gateway import Gateway


class TestNotificationService(TestCase):
    def setUp(self):
        gateway = Gateway()
        gateway.send = MagicMock()
        notification_store = NotificationStore()
        rules_service = RulesService(notification_store)
        self.notification_service = NotificationService(
            gateway=gateway,
            rules_service=rules_service,
            notification_store=notification_store,
        )

    def test_limit_not_exceeded(self):
        self.notification_service.send('status', 'user_1', 'Status uptade 1')
        self.notification_service.send('status', 'user_1', 'Status uptade 2')
        self.assertEqual(self.notification_service.gateway.send.call_count, 2)

    def test_limit_exceeded(self):
        self.notification_service.send('marketing', 'user_1', 'Marketing message')
        self.notification_service.send('marketing', 'user_1', 'Marketing message')
        self.notification_service.send('marketing', 'user_1', 'Marketing message')
        self.notification_service.send('marketing', 'user_1', 'Marketing message')
        self.assertEqual(self.notification_service.gateway.send.call_count, 3)

    def test_multiple_users_limit_not_exceeded(self):
        self.notification_service.send('news', 'user_1', 'News message')
        self.notification_service.send('news', 'user_2', 'News message')
        self.notification_service.send('news', 'user_3', 'News message')
        self.notification_service.send('news', 'user_4', 'News message')
        self.assertEqual(self.notification_service.gateway.send.call_count, 4)

    def test_type_with_no_rule(self):
        N = 10
        for _ in range(N):
            self.notification_service.send('compliance', 'user_2', 'Complance notification')
        self.assertEqual(self.notification_service.gateway.send.call_count, N)

    @patch('src.notification_service.notification_store.datetime')
    def test_limit_reset_after_time_window(self, mock_datetime):
        initial_time = datetime(year=2024, month=10, day=5)
        mock_datetime.now.return_value = initial_time
        self.notification_service.send('news', 'user_1', 'Status uptade 1')
        self.notification_service.send('news', 'user_1', 'Status uptade 1')
        mock_datetime.now.return_value = initial_time + timedelta(days=1)
        self.notification_service.send('news', 'user_1', 'Status uptade 1')
        self.assertEqual(self.notification_service.gateway.send.call_count, 2)
