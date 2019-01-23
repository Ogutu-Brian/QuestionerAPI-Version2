from api.tests.base_test import BaseTest
from api.app.views import Status
import json
from api.app.models.models import User


class UserTest(BaseTest):
    """Tests sign up endpoint"""

    def setUp(self):
        super().setUp()

    def test_successful_sign_up(self)->None:
        """Tests for a successful sign up by user"""
        result = self.sign_up()
        self.assertEqual(Status.created, result.get("status"))

    def test_invalid_phone_number(self)->None:
        self.user_data.data["phoneNumber"] = "2932329742749797492472"
        result = self.sign_up()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_email(self)->None:
        """Tets for data that does not contain an email"""
        self.user_data.data["email"] = ""
        result = self.sign_up()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_passworord(self)->None:
        """tests for data that is missing password during creation of user"""
        self.user_data.data["password"] = ""
        result = self.sign_up()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_invalid_password(self)->None:
        """Tests for invalid passsword during sign up"""
        self.user_data.data["password"] = "password"
        result = self.sign_up()
        self.assertEqual(Status.invalid_data, result.get("status"))
        self.user_data.data["password"] = "passwordA"
        self.sign_up()
        self.assertEqual(Status.invalid_data, result.get("status"))
        self.user_data.data["password"] = "passwordA"
        result = self.sign_up()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_first_name(self)->None:
        """Tests for data that lacks first name during creation of user"""
        self.user_data.data["firstname"] = ""
        result = self.sign_up()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_last_name(self)->None:
        """Tests for data that misses last name during sign up"""
        self.user_data.data["lastname"] = ""
        result = self.sign_up()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_phone_number(self)->None:
        """Tests for data that misses phone number during creation of a user"""
        self.user_data.data["phoneNumber"] = ""
        result = self.sign_up()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_user_name(self)->None:
        """tests for data that misses username during creation of user"""
        self.user_data.data["username"] = ""
        result = self.sign_up()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_data_not_json(self)->None:
        """tests for data that is not in json format"""
        self.json_headers = self.not_json_header
        result = self.sign_up()
        self.assertEqual(Status.not_json, result.get("status"))

    def test_taken_username(self)->None:
        """Tests if a given username is already taken by another user"""
        self.sign_up()
        self.user_data.data["email"] = ""
        result = self.sign_up()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_taken_email(self)->None:
        """Tests for signup with an email that is already taken by another user"""
        self.sign_up()
        self.user_data.data["username"] = ""
        result = self.sign_up()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_successful_user_login(self)->None:
        self.sign_up()
        result = self.login()
        self.assertEqual(Status.success, result.get("status"))

    def test_missing_log_in_username_and_email(self)->None:
        """Tests log in without the provision of both username and email"""
        self.sign_up()
        self.user_data.data["email"] = ""
        self.user_data.data["username"] = ""
        result = self.login()
        self.assertEqual(result.get("status"), Status.invalid_data)

    def test_missing_login_password(self)->None:
        """Tests for missing password during login"""
        self.sign_up()
        self.user_data.data["password"] = ""
        result = self.login()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_wrong_login_password(self)->None:
        """Tests for invalid password during login"""
        self.sign_up()
        self.user_data.data["password"] = "efnoewnfonw@134A"
        result = self.login()
        self.assertEqual(Status.denied_access, result.get("status"))

    def test_unexisting_username(self)->None:
        """Tests attempt to log in with unexisting username"""
        self.sign_up()
        self.user_data.data["email"] = ""
        self.user_data.data["username"] = "TestUser"
        result = self.login()
        self.assertEqual(Status.denied_access, result.get("status"))

    def test_non_json_login_data(self)->None:
        """tests if the post data is json"""
        self.json_headers = self.not_json_header
        self.sign_up()
        result = self.login()
        self.assertEqual(Status.not_json, result.get("status"))

    def test_token_generation(self)->None:
        """Tests whether a token is generated during login"""
        self.sign_up()
        result = self.login()
        self.assertEqual((result["data"][0].get("token") != None), True)

    def test_successful_logout(self)->None:
        """Tests when a user successfully logs out"""
        self.authorize_with_jwt()
        result = self.logout()
        self.assertEqual(Status.success, result.get("status"))
