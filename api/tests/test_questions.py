from api.tests.base_test import BaseTest
from api.app.views import Status


class TestQuestion(BaseTest):
    """Class for testing operations on Question records"""

    def setUp(self):
        super().setUp()

    def test_correct_question_post(self):
        """tests for correct creation of question"""
        result = self.create_question()
        self.assertEqual(Status.created, result.get("status"))
