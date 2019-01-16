from api.tests.base_test import BaseTest
from api.app.views import Status
from .import UserData,user_data
import json


class UserTest(BaseTest):
    """Tests sign up endpoint"""

    def setUp(self):
        super().setUp()

    def post_data(self, url, data={}, headers={}):
        """
        Posts data to various endpoints
        """
        result = self.client().post(url, data=json.dumps(data), headers=self.json_headers)
        return json.loads(result.get_data(as_text=True))

    def test_successful_sign_up(self):
        """Tests for a successful sign up by user"""
        result = self.sign_up()
        self.assertEqual(Status.created, result.get("status"))
    def test_missing_email(self):
        """Tets for data that does not contain an email"""
        user_data = UserData()
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.missing_mail_data, headers=user_data.missing_mail_data.get("headers"))
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_passworord(self):
        """tests for data that is missing password during creation of user"""
        user_data = UserData()
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.missing_password_data, headers=user_data.missing_password_data.get("headers"))
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_invalid_password(self):
        """Tests for invalid passsword during sign up"""
        user_data.invalid_password_data["sign_up"]["password"] = "password"
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.invalid_password_data.get("sign_up"), headers=user_data.valid_user_data.get("headers"))
        self.assertEqual(Status.invalid_data, result.get("status"))
        user_data.invalid_password_data["sign_up"]["password"] = "passwordA"
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.invalid_password_data.get("sign_up"), headers=user_data.valid_user_data.get("headers"))
        self.assertEqual(Status.invalid_data, result.get("status"))
        user_data.invalid_password_data["sign_up"]["password"] = "passwordA"
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.invalid_password_data.get("sign_up"), headers=user_data.valid_user_data.get("headers"))
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_first_name(self):
        """Tests for data that lacks first name during creation of user"""
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.missing_first_name_data, headers=user_data.valid_user_data.get("headers"))
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_last_name(self):
        """Tests for data that misses last name during sign up"""
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.missing_last_name_data, headers=user_data.valid_user_data.get("headers"))
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_phone_number(self):
        """Tests for data that misses phone number during creation of a user"""
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.missing_phone_number_data, headers=user_data.valid_user_data.get("headers"))
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_user_name(self):
        """tests for data that misses username during creation of user"""
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.missing_user_name_data, headers=user_data.valid_user_data.get("headers"))
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_data_not_json(self):
        """tests for data that is not in json format"""
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.valid_user_data.get("sign_up"), headers=self.not_json_header)
        print(result)
        self.assertEqual(Status.not_json, result.get("status"))

    def test_taken_username(self):
        """Tests if a given username is already taken by another user"""
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.complete_data, headers=user_data.valid_user_data.get("headers"))
        self.assertEqual(Status.created, result.get("status"))
        user_data.complete_data["email"] = "test@gmail.com"
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.complete_data, headers=user_data.valid_user_data.get("headers"))
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_taken_email(self):
        """Tests for signup with an email that is already taken by another user"""
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.complete_data, headers=user_data.valid_user_data.get("headers"))
        self.assertEqual(Status.created, result.get("status"))
        user_data.complete_data["username"] = "test"
        result = self.post_data(url=user_data.valid_user_data.get(
            "sign_up_url"), data=user_data.complete_data, headers=user_data.valid_user_data.get("headers"))