from api.tests.base_test import BaseTest
from app.views import Status


class TestMeetups(BaseTest):
    """tests operations performed on meetups"""

    def setUp(self):
        super().setUp()

    def test_successful_meetup_creation(self):
        """Tests for successful creation of a meetup"""
        result = self.create_meetup()
        self.assertEqual(Status.created, result.get("status"))