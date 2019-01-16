from api.tests.base_test import BaseTest
from api.app.views import Status

class SignupTest(BaseTest):
    """Tests sign up endpoint"""

    def setUp(self):
        super().setUp()

    def test_successful_sign_up(self):
        """Tests for a successful sign up by user"""
        result = self.sign_up()
        self.assertEqual(Status.created, result.get("status"))