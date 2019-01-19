import unittest
import json
from run import create_app
from migrtions import DbMigrations
from .import UserData, MeetupData, QuestionData, RsvpData,CommentData
from flask_jwt_extended import get_jwt_identity
from typing import Dict

class BaseTest(unittest.TestCase):
    """Defines a Base template class for performing unit testst"""

    def setUp(self)->None:
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
        self.rsvp_data = RsvpData()
        self.comment_data = CommentData()

    def complete_url(self, url:str="")->str:
        """Returns complete url endpoint that is tested by the view"""
        return self.url_prefix+url

    def post_data(self, url:str="", data={}, headers:Dict={}):
        """
        Posts data to various endpoints
        """
        result = self.client().post(url, data=json.dumps(data), headers=headers)
        return json.loads(result.get_data(as_text=True))

    def patch_data(self, url:str="", headers:Dict={}):
        """Performs the patch operations on data"""
        result = self.client().patch(url, headers=headers)
        return json.loads(result.get_data(as_text=True))

    def get_data(self, url:str="", headers:Dict={}):
        """used to get data at given urls"""
        result = json.loads(self.client().get(self.complete_url(
            url=url), headers=headers).get_data(as_text=True))
        return result

    def delete_data(self, url:str="", headers:Dict={}):
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

    def authorize_with_jwt(self)->Dict:
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
        self.create_question_intials()
        question_id = self.create_question()["data"][0]["id"]
        result = self.patch_data(url=self.complete_url(
            "questions/{}/upvote".format(question_id)), headers=self.json_headers)
        return result

    def downvote(self):
        self.create_question_intials()
        question_id = self.create_question()["data"][0]["id"]
        result = self.patch_data(url=self.complete_url(
            "questions/{}/downvote".format(question_id)), headers=self.json_headers)
        return result

    def create_rsvp(self):
        """Successfully creates an rsvp"""
        meetup_id = self.create_meetup()["data"][0]["id"]
        result = self.post_data(url=self.complete_url(
            url="meetups/{}/rsvps".format(meetup_id)), data=self.rsvp_data.data, headers=self.json_headers)
        return result

    def post_commet(self):
        """Posts a comment to a given question"""
        question_id = self.create_question()["data"][0]["id"]
        self.comment_data.data["question"] = question_id
        result = self.post_data(url=self.complete_url(url="comments/"),
                                data=self.comment_data.data, headers=self.json_headers)
        return result

    def tearDown(self):
        """Clears all the content in database tables and instantiates data objects"""
        DbMigrations.tear_down()
        self.user_data = UserData()
        self.meetup_data = MeetupData()
        self.questions_data = QuestionData()
        self.rsvp_data=RsvpData()
        self.comment_data= CommentData()
        self.json_headers = {"Content-Type": "application/json"}
        self.not_json_header = {}
