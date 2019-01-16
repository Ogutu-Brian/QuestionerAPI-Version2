import unittest
from run import create_app, database
from migrtions import DbMigrations


class BaseTest(unittest.TestCase):
    """Defines a Base template class for performing unit testst"""

    def setUp(self):
        """Sets up a test client for the application"""
        self.app = create_app("TESTING")
        self.client = self.app.test_client
        self.not_json_header = {}
        self.json_headers = {"Content-Type": "application/json"}
        self.url_prefix = "/api/v2"

    def complete_url(self, url=""):
        """Returns complete url endpoint that is tested by the view"""
        return self.url_prefix+url

    def tearDown(self):
        """Clears all the content in database tables"""
        DbMigrations.tear_down()
