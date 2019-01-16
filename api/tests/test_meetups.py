from api.tests.base_test import BaseTest
from .import meetup_data
from api.app.models.models import Meetup
from .import rsvp_data
from api.app.views import Status


class TestMeetup(BaseTest):
    """Tests the operations perfomed on meetup records"""

    def setUp(self):
        super().setUp()

    def test_successful_meetup_creation(self):
        """Tests for successful creation of meetup"""
        self.assertEqual(self.create_meetup().status_code, 201)

    def tes_successful_rsvp_response(self):
        """Tests for successful creation of rsvp"""
        self.sign_up()
        self.create_meetup()
        rsvp_data.valid_rsvp_data["data"]["response"] = "yes"
        rsvp_data.valid_rsvp_data["data"]["user"] = 1
        self.assertEqual(Status.created, self.client().post(self.complete_url(
            "/meetups/1/rsvps"), data=rsvp_data.valid_rsvp_data.get("data"), headers=self.json_headers).status_code)
