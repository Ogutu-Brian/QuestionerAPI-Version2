from api.tests.base_test import BaseTest
from api.app.views import Status
import json
from api.app.models.models import User


class UserTest(BaseTest):
    """Tests sign up endpoint"""

    def setUp(self):
        super().setUp()
    def test_successful_sign_up(self):
        """Tests for a successful sign up by user"""
        result = self.sign_up()
        self.assertEqual(Status.created, result.get("status"))

    def test_missing_email(self):
        """Tets for data that does not contain an email"""
        result = self.post_data(url=self.complete_url(
            "users/sign-up"), data=self.user_data.missing_mail_data, headers=self.json_headers)
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_passworord(self):
        """tests for data that is missing password during creation of user"""
        result = self.post_data(url=self.complete_url(
            "users/sign-up"), data=self.user_data.missing_password_data, headers=self.json_headers)
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_invalid_password(self):
        """Tests for invalid passsword during sign up"""
        self.user_data.invalid_password_data["sign_up"]["password"] = "password"
        result = self.post_data(url=self.complete_url(
            "users/sign-up"), data=self.user_data.invalid_password_data.get("sign_up"), headers=self.json_headers)
        self.assertEqual(Status.invalid_data, result.get("status"))
        self.user_data.invalid_password_data["sign_up"]["password"] = "passwordA"
        result = self.post_data(url=self.complete_url(
            "users/sign-up"), data=self.user_data.invalid_password_data.get("sign_up"), headers=self.json_headers)
        self.assertEqual(Status.invalid_data, result.get("status"))
        self.user_data.invalid_password_data["sign_up"]["password"] = "passwordA"
        result = self.post_data(url=self.complete_url(
            "users/sign-up"), data=self.user_data.invalid_password_data.get("sign_up"), headers=self.json_headers)
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_first_name(self):
        """Tests for data that lacks first name during creation of user"""
        result = self.post_data(url=self.complete_url(
            "users/sign-up"), data=self.user_data.missing_first_name_data, headers=self.json_headers)
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_last_name(self):
        """Tests for data that misses last name during sign up"""
        result = self.post_data(url=self.complete_url(
            "users/sign-up"), data=self.user_data.missing_last_name_data, headers=self.json_headers)
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_phone_number(self):
        """Tests for data that misses phone number during creation of a user"""
        result = self.post_data(url=self.complete_url(
            "users/sign-up"), data=self.user_data.missing_phone_number_data, headers=self.json_headers)
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_user_name(self):
        """tests for data that misses username during creation of user"""
        result = self.post_data(url=self.complete_url(
            "users/sign-up"), data=self.user_data.missing_user_name_data, headers=self.json_headers)
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_data_not_json(self):
        """tests for data that is not in json format"""
        result = self.post_data(url=self.complete_url(
            "users/sign-up"), data=self.user_data.valid_user_data.get("sign_up"), headers=self.not_json_header)
        self.assertEqual(Status.not_json, result.get("status"))

    def test_taken_username(self):
        """Tests if a given username is already taken by another user"""
        self.sign_up()
        self.user_data.complete_data["email"] = ""
        result = self.post_data(url=self.complete_url(
            "users/sign-up"), data=self.user_data.complete_data, headers=self.json_headers)
        print(result)
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_taken_email(self):
        """Tests for signup with an email that is already taken by another user"""
        self.sign_up()
        self.user_data.complete_data["username"] = ""
        result = self.post_data(url=self.complete_url(
            "users/sign-up"), data=self.user_data.complete_data, headers=self.json_headers)
        self.assertEqual(Status.invalid_data, result.get("status"))
    def test_successful_user_login(self):
        pass