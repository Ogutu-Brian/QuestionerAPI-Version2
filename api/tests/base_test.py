import unittest
import json
from run import create_app
from migrtions import DbMigrations
from api.app.models.object_models import User
from .import meetup_data, user_data


class BaseTest(unittest.TestCase):
    """Defines a Base template class for performing unit testst"""

    def setUp(self):
        """Sets up a test client for the application"""
        self.app = create_app("TESTING")
        self.client = self.app.test_client
        self.not_json_header = {}
        self.migration = DbMigrations()
        self.json_headers = {"Content-Type": "application/json"}
        self.url_prefix = "/api/v2/"
        self.migration.makemigrations()

    def complete_url(self, url=""):
        """Returns complete url endpoint that is tested by the view"""
        return self.url_prefix+url

    def sign_up(self):
        data = json.dumps(user_data.valid_user_data.get("sign_up"))
        result = json.loads(self.client().post(self.complete_url(
            "users/sign-up"), data=data, headers=self.json_headers).get_data(as_text=True))
        return result

    def create_meetup(self):
        data = meetup_data.valid_meetup_data.get("data")
        result = json.loads(self.client().post(self.complete_url(
            "/meetups"), data=data, headers=self.json_headers).get_data(as_text=True))
        return result

    def tearDown(self):
        """Clears all the content in database tables"""
        self.migration.tear_down()
