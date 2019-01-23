from api.tests.base_test import BaseTest
from api.app.views import Status


class TestComments(BaseTest):
    """Tests Comments Posted to various questions"""

    def setUp(self)->None:
        super().setUp()

    def test_successful_comment(self)->None:
        """Tests succesful creation of comments"""
        result = self.create_comment()
        self.assertEqual(Status.created, result.get("status"))

    def test_invalid_question_id(self)->None:
        """Tests if the question id provided is valid"""
        self.authorize_with_jwt()
        self.comment_data.data["question"] = -743463
        result = self.post_data(url=self.complete_url(url="comments/"),
                                data=self.comment_data.data, headers=self.json_headers)
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_non_json_object(self):
        """Test when a non json object is posted"""
        self.create_question_intials()
        question_id = self.create_question()["data"][0]["id"]
        self.comment_data.data["question"] = question_id
        result = self.post_data(url=self.complete_url(url="comments/"),
                                data=self.comment_data.data, headers=self.not_json_header)
        self.assertEqual(Status.not_json, result.get("status"))

    def test_unexisting_question(self)->None:
        """Checks for zero comments"""
        result = self.get_data(url="comments/-34437",
                               headers=self.json_headers)
        self.assertEqual(Status.not_found, result.get("status"))

    def test_existing_questions(self)->None:
        """Tests for existance of comments"""
        comment = self.create_comment()
        question_id = comment["data"]["question"]
        result = self.get_data(
            url="comments/{}".format(question_id), headers=self.json_headers)
        self.assertEqual(Status.success, result.get("status"))

    def test_zero_comments(self)->None:
        """Tests for zero comments on a question"""
        self.create_question_intials()
        question_id = self.create_question()["data"][0]["id"]
        result = self.get_data("comments/{}".format(question_id))
        self.assertEqual(Status.not_found, result.get("status"))
