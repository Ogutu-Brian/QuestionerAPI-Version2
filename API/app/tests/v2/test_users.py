from app.tests.v2.base_test import BaseTest


class SignupTest(BaseTest):
    """Tests sign up endpoint"""

    def setUp(self):
        super().setUp()

    def test_successful_sign_up(self):
        """Tests for a successful sign up by user"""
        self.assertEqual(self.sign_up().status_code, 201)
