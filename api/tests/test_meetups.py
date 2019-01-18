from api.tests.base_test import BaseTest
from api.app.views import Status


class TestMeetups(BaseTest):
    """tests operations performed on meetups"""

    def setUp(self):
        super().setUp()

    def test_successful_meetup_creation(self):
        """Tests for successful creation of a meetup"""
        result = self.create_meetup()
        self.assertEqual(Status.created, result.get("status"))

    def test_unauthorized_user(self):
        self.user_data.data["isAdmin"] = "False"
        result = self.create_meetup()
        self.assertEqual(Status.denied_access, result.get("status"))

    def test_missing_tags(self):
        """Tests for data that does not contain tags"""
        self.meetup_data.data["Tags"] = ""
        result = self.create_meetup()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_location(self):
        """tests for data that does not contain location of meetup"""
        self.meetup_data.data["location"] = ""
        result = self.create_meetup()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_meetup_date(self):
        """Test data that does not contain meetup date"""
        self.meetup_data.data["happeningOn"] = ""
        result = self.create_meetup()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_images(self):
        """Image location is optional so missing in json object should not cause failure"""
        self.meetup_data.data["images"] = ""
        result = self.create_meetup()
        self.assertEqual(Status.created, result.get("status"))

    def test_invalid_post_object(self):
        """Tests if the data being posted is actually json"""
        self.authorize_with_jwt()
        result = self.post_data(self.complete_url("meetups"),
                                data=self.meetup_data.data, headers=self.not_json_header)
        self.assertEqual(Status.not_json, result.get("status"))

    def test_get_meetup_record(self):
        """Tests for get request for a specific meetup given a meetup id"""
        meetup_id = self.create_meetup()["data"][0].get("id")
        result = self.get_data(
            "meetups/{}".format(meetup_id), headers=self.json_headers)
        self.assertEqual(Status.success, result.get("status"))

    def test_all_upming_meetups(self):
        """Tests for the getting all upcoming meetups"""
        self.create_meetup()
        self.create_meetup()
        self.create_meetup()
        result = self.get_data("meetups/upcoming/", self.json_headers)
        self.assertEqual(Status.success, result.get("status"))

    def test_no_meetup_records(self):
        self.authorize_with_jwt()
        result = self.get_data("meetups/upcoming/", self.json_headers)
        self.assertEqual(Status.success, result.get("status"))

    def test_delete_meetup(self):
        """Test for delete meetup endpoint"""
        meetup_id = self.create_meetup()["data"][0]["id"]
        result = self.delete_data(
            "meetups/{}".format(meetup_id), headers=self.json_headers)
        self.assertEqual(Status.success, result.get("status"))

    def test_wrong_meetup_id_for_deletion(self):
        meetup_id = self.create_meetup()["data"][0]["id"]
        result = self.delete_data(
            "meetups/{}".format(meetup_id+1), headers=self.json_headers)
        self.assertEqual(Status.not_found, result.get("status"))

    def test_user_not_admin(self):
        """Tests for deletion of a meeetup by one who does not have admin rights"""
        from api.app.models.models import User
        meetup_id = self.create_meetup()["data"][0]["id"]
        User.clear()
        self.user_data.data["isAdmin"] = "False"
        self.authorize_with_jwt()
        result = self.delete_data(
            "meetups/{}".format(meetup_id), headers=self.json_headers)
        self.assertEqual(Status.denied_access, result.get("status"))
