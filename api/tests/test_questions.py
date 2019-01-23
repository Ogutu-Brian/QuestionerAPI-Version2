from api.tests.base_test import BaseTest
from api.app.views import Status


class TestQuestion(BaseTest):
    """Class for testing operations on Question records"""

    def setUp(self):
        super().setUp()

    def test_correct_question_post(self)->None:
        """tests for correct creation of question"""
        self.create_question_intials()
        result = self.post_data(self.complete_url("questions"), data=self.questions_data.data,
                                headers=self.json_headers)
        self.assertEqual(Status.created, result.get("status"))

    def test_non_json_data(self)->None:
        """Tests for data that is not in json format"""
        self.create_question_intials()
        self.json_headers = self.not_json_header
        result = self.create_question()
        self.assertEqual(Status.not_json, result.get("status"))

    def test_missing_creator(self)->None:
        """tests fir data that does not contain creator of the question"""
        self.create_question_intials()
        self.questions_data.data["createdBy"] = ""
        result = self.create_question()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_body(self)->None:
        """Tests for missing body during creation of a question"""
        self.create_question_intials()
        self.questions_data.data["body"] = ""
        result = self.create_question()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_meetup(self)->None:
        """Tests for Question that is not linked to a meetup"""
        self.create_question_intials()
        self.questions_data.data["meetup"] = ""
        result = self.create_question()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_invalid_user(self)->None:
        """Tests if a user with an id exists in the database"""
        self.create_question_intials()
        self.questions_data.data["createdBy"] = -78667
        result = self.create_question()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_invalid_meetup(self)->None:
        """Tests if a meetup with the given id exists in the database"""
        self.create_question_intials()
        self.questions_data.data["meetup"] = -338738748
        result = self.create_question()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_successful_upvote(self)->None:
        """Tests the endpoint for upvoting a question in questioner"""
        result = self.upvote()
        self.assertEqual(Status.created, result.get("status"))

    def test_unexsiting_upvote_question(self)->None:
        """Tests for a patch to a question that does not exist"""
        question_id = -7878
        self.authorize_with_jwt()
        result = self.patch_data(url=self.complete_url(
            "questions/{}/upvote".format(question_id)), headers=self.json_headers)
        self.assertEqual(Status.not_found, result.get("status"))

    def test_successful_downvote(self)->None:
        """Tests test for downvote of a question"""
        result = self.downvote()
        self.assertEqual(Status.created, result.get("status"))

    def test_unexsiting_downvote_question(self)->None:
        """Tess if the id provided for downvoting a question exists"""
        question_id = -24434
        self.authorize_with_jwt()
        result = self.patch_data(url=self.complete_url(
            url="questions/{}/downvote".format(question_id)), headers=self.json_headers)
        self.assertEqual(Status.not_found, result.get("status"))

    def test_get_individual_question(self)->None:
        """"Tessts for successful get of question"""
        self.create_question_intials()
        question_id = self.create_question()["data"][0].get("id")
        result = self.get_data(
            url="questions/{}".format(question_id), headers=self.json_headers)
        print(result)
        self.assertEqual(Status.success, result.get("status"))

    def test_get_unexisting_question(self)->None:
        """Tests for a get of unexisting question"""
        result = self.get_data(url="questions/-1334",
                               headers=self.json_headers)
        self.assertEqual(Status.not_found, result.get("status"))
