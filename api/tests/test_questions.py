from api.tests.base_test import BaseTest
from api.app.views import Status


class TestQuestion(BaseTest):
    """Class for testing operations on Question records"""

    def setUp(self):
        super().setUp()

    def test_correct_question_post(self):
        """tests for correct creation of question"""
        self.create_question_intials()
        result = self.post_data(self.complete_url("questions"), data=self.questions_data.data,
                                headers=self.json_headers)
        self.assertEqual(Status.created, result.get("status"))

    def test_non_json_data(self):
        """Tests for data that is not in json format"""
        self.create_question_intials()
        self.json_headers = self.not_json_header
        result = self.create_question()
        self.assertEqual(Status.not_json, result.get("status"))

    def test_missing_creator(self):
        """tests fir data that does not contain creator of the question"""
        self.create_question_intials()
        self.questions_data.data["createdBy"] = ""
        result = self.create_question()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_body(self):
        """Tests for missing body during creation of a question"""
        self.create_question_intials()
        self.questions_data.data["body"] = ""
        result = self.create_question()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_meetup(self):
        """Tests for Question that is not linked to a meetup"""
        self.create_question_intials()
        self.questions_data.data["meetup"] = ""
        result = self.create_question()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_invalid_user(self):
        """Tests if a user with an id exists in the database"""
        self.create_question_intials()
        self.questions_data.data["createdBy"] = -78667
        result = self.create_question()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_invalid_meetup(self):
        """Tests if a meetup with the given id exists in the database"""
        self.create_question_intials()
        self.questions_data.data["meetup"] = -338738748
        result = self.create_question()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_successful_upvote(self):
        """Tests the endpoint for upvoting a question in questioner"""
        result = self.upvote()
        self.assertEqual(Status.created, result.get("status"))

    def test_unexsiting_upvote_question(self):
        """Tests for a patch to a question that does not exist"""
        question_id = -7878
        result = self.path_data(url=self.complete_url(
            "questions/{}/upvote".format(question_id)), headers=self.json_headers)
        self.assertGreaterEqual(Status.not_found, result.get("status"))

    def test_successful_downvote(self):
        """Tests test for downvote of a question"""
        result = self.downvote()
        self.assertEqual(Status.created, result.get("status"))
