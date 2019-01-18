import unittest
import json
from run import create_app
from migrtions import DbMigrations
from .import UserData, MeetupData, QuestionData


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
        DbMigrations.makemigrations()
        self.user_data = UserData()
        self.meetup_data = MeetupData()
        self.questions_data = QuestionData()

    def complete_url(self, url=""):
        """Returns complete url endpoint that is tested by the view"""
        return self.url_prefix+url

    def post_data(self, url="", data={}, headers={}):
        """
        Posts data to various endpoints
        """
        result = self.client().post(url, data=json.dumps(data), headers=headers)
        return json.loads(result.get_data(as_text=True))

    def path_data(self, url="", headers={}):
        """Performs the patch operations on data"""
        result = self.client().patch(url, headers=headers)
        return json.loads(result.get_data(as_text=True))

    def get_data(self, url="", headers={}):
        """used to get data at given urls"""
        result = json.loads(self.client().get(self.complete_url(
            url=url), headers=headers).get_data(as_text=True))
        return result

    def delete_data(self, url, headers={}):
        result = json.loads(self.client().delete(
            self.complete_url(url), headers=headers).get_data(as_text=True))
        return result

    def sign_up(self):
        """Signs up a user into the system"""
        result = self.post_data(url=self.complete_url(
            "auth/signup"), data=self.user_data.data, headers=self.json_headers)
        return result

    def login(self):
        """Logs in auser into the system"""
        self.sign_up()
        result = self.post_data(url=self.complete_url(
            "auth/login"), data=self.user_data.data, headers=self.json_headers)
        return result

    def create_meetup(self):
        """Successfully creates a meetup Record"""
        self.authorize_with_jwt()
        result = self.post_data(url=self.complete_url("meetups"),
                                data=self.meetup_data.data, headers=self.json_headers)
        return result

    def authorize_with_jwt(self):
        """Generates token that is used to secure endpoints"""
        result = self.login()
        token = result["data"][0].get("token")
        self.json_headers["Authorization"] = 'Bearer {}'.format(token)
        self.not_json_header["Authorization"] = 'Bearer {}'.format(token)
        return result["data"][0]["user"]

    def create_question_intials(self)->None:
        """Sets up intial variables needed for creation of a queestion"""
        meetup_id = self.create_meetup()["data"][0].get("id")
        user_id = self.authorize_with_jwt()["id"]
        self.questions_data.data["createdBy"] = user_id
        self.questions_data.data["meetup"] = meetup_id

    def create_question(self):
        """A method for creating a question after settomg up question intials"""
        result = self.post_data(self.complete_url("questions"), data=self.questions_data.data,
                                headers=self.json_headers)
        return result

    def upvote(self):
        """Upvotes a question"""
        self.authorize_with_jwt()
        self.create_question_intials()
        question_id = self.create_question()["data"]["id"]
        result = self.path_data(url=self.complete_url(
            "questions/{}".format(question_id)), headers=self.json_headers)
        return result

    def tearDown(self):
        """Clears all the content in database tables and instantiates data objects"""
        DbMigrations.tear_down()
        self.user_data = UserData()
        self.meetup_data = MeetupData()
        self.questions_data = QuestionData()
        self.json_headers = {"Content-Type": "application/json"}
        self.not_json_header = {}
