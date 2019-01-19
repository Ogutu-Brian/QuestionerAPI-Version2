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
