from api.app.tests.base_test import BaseTest
from api.app.views import Status

class SignupTest(BaseTest):
    """Tests sign up endpoint"""

    def setUp(self):
        super().setUp()

    def test_successful_sign_up(self):
        """Tests for a successful sign up by user"""
        self.assertEqual(self.sign_up().status_code, Status.created)
