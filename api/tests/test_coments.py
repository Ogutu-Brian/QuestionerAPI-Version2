from api.tests.base_test import BaseTest
from api.app.views import Status


class TestComments(BaseTest):
    """Tests Comments Posted to various questions"""

    def setUp(self)->None:
        super().setUp()

    def test_successful_comment(self)->None:
        """Tests succesful creation of comments"""
        result = self.create_commet()
        self.assertEqual(Status.created, result.get("status"))
