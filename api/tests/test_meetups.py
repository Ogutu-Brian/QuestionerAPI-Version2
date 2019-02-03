from api.tests.base_test import BaseTest
from api.app.views import Status


class TestMeetups(BaseTest):
    """tests operations performed on meetups"""

    def setUp(self)->None:
        super().setUp()

    def test_successful_meetup_creation(self)->None:
        """Tests for successful creation of a meetup"""
        result = self.create_meetup()
        self.assertEqual(Status.created, result.get("status"))

    def test_unauthorized_user(self)->None:
        self.user_data.data["isAdmin"] = "False"
        result = self.create_meetup()
        self.assertEqual(Status.denied_access, result.get("status"))

    def test_missing_tags(self)->None:
        """Tests for data that does not contain tags"""
        self.meetup_data.data["Tags"] = ""
        result = self.create_meetup()
        self.assertEqual(Status.created, result.get("status"))
    def test_missing_body(self)->None:
        """Tests if a body is not provided for the meetup"""
        self.meetup_data.data["body"]=""
        result = self.create_meetup()
        self.assertEqual(Status.invalid_data,result.get("status"))
    def test_missing_location(self)->None:
        """tests for data that does not contain location of meetup"""
        self.meetup_data.data["location"] = ""
        result = self.create_meetup()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_meetup_date(self)->None:
        """Test data that does not contain meetup date"""
        self.meetup_data.data["happeningOn"] = ""
        result = self.create_meetup()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_invalid_meetup_date(self)->None:
        self.meetup_data.data["happeningOn"] = "82171-33133"
        result = self.create_meetup()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_passed_meetup_date(self)->None:
        """Tests for the creation of a meetup in a passed date"""
        self.meetup_data.data["happeningOn"] = "24-01-2017"
        result = self.create_meetup()
        self.assertEqual(Status.invalid_data, result.get("status"))

    def test_missing_images(self)->None:
        """Image location is optional so missing in json object should not cause failure"""
        self.meetup_data.data["images"] = ""
        result = self.create_meetup()
        self.assertEqual(Status.created, result.get("status"))

    def test_invalid_post_object(self)->None:
        """Tests if the data being posted is actually json"""
        self.authorize_with_jwt()
        result = self.post_data(self.complete_url("meetups"),
                                data=self.meetup_data.data, headers=self.not_json_header)
        self.assertEqual(Status.not_json, result.get("status"))

    def test_get_meetup_record(self)->None:
        """Tests for get request for a specific meetup given a meetup id"""
        meetup_id = self.create_meetup()["data"][0].get("id")
        result = self.get_data(
            "meetups/{}".format(meetup_id), headers=self.json_headers)
        self.assertEqual(Status.success, result.get("status"))

    def test_all_upming_meetups(self)->None:
        """Tests for the getting all upcoming meetups"""
        self.create_meetup()
        self.create_meetup()
        self.create_meetup()
        result = self.get_data("meetups/upcoming/", self.json_headers)
        self.assertEqual(Status.success, result.get("status"))

    def test_no_meetup_records(self)->None:
        self.authorize_with_jwt()
        result = self.get_data("meetups/upcoming/", self.json_headers)
        self.assertEqual(Status.success, result.get("status"))

    def test_delete_meetup(self)->None:
        """Test for delete meetup endpoint"""
        meetup_id = self.create_meetup()["data"][0]["id"]
        result = self.delete_data(
            "meetups/{}".format(meetup_id), headers=self.json_headers)
        self.assertEqual(Status.success, result.get("status"))

    def test_wrong_meetup_id_for_deletion(self)->None:
        meetup_id = self.create_meetup()["data"][0]["id"]
        result = self.delete_data(
            "meetups/{}".format(meetup_id+1), headers=self.json_headers)
        self.assertEqual(Status.not_found, result.get("status"))

    def test_user_not_admin(self)->None:
        """Tests for deletion of a meeetup by one who does not have admin rights"""
        from api.app.models.models import User
        meetup_id = self.create_meetup()["data"][0]["id"]
        User.clear()
        self.user_data.data["isAdmin"] = "False"
        self.authorize_with_jwt()
        result = self.delete_data(
            "meetups/{}".format(meetup_id), headers=self.json_headers)
        self.assertEqual(Status.denied_access, result.get("status"))

    def test_successful_rsvp_response(self)->None:
        """Tests for successful rsvp response"""
        result = self.create_rsvp()
        self.assertEqual(Status.created, result.get("status"))

    def test_duplicate_rsvp_response(self)->None:
        """Tests when a user gives similar Rsvp response to a single meetup"""
        meetup_id = self.create_meetup()["data"][0]["id"]
        self.post_data(url=self.complete_url(
            url="meetups/{}/rsvps".format(meetup_id)), data=self.rsvp_data.data, headers=self.json_headers)
        result = self.post_data(url=self.complete_url(
            url="meetups/{}/rsvps".format(meetup_id)), data=self.rsvp_data.data, headers=self.json_headers)
        self.assertEqual(Status.denied_access, result.get("status"))

    def test_invalid_meetup_for_rsvp(self)->None:
        """Tests for invalid meetup id during creation of rsvp"""
        self.create_meetup()
        result = self.post_data(url=self.complete_url(
            url="meetups/{}/rsvps".format(-1234)), data=self.rsvp_data.data, headers=self.json_headers)
        self.assertEqual(Status.not_found, result.get("status"))

    def test_post_data_not_json(self)->None:
        """Checking if rsvp data being posted is in JSON format"""
        meetup_id = self.create_meetup()["data"][0]["id"]
        self.json_headers = self.not_json_header
        result = self.post_data(url=self.complete_url(
            url="meetups/{}/rsvps".format(meetup_id)), data=self.rsvp_data.data, headers=self.json_headers)
        self.assertEqual(Status.not_json, result.get("status"))

    def test_duplicate_meetup(self)->None:
        """Test if duplicate meetups have been created"""
        self.create_meetup()
        result = self.create_meetup()
        self.assertEqual(Status.denied_access, result.get("status"))
