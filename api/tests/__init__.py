class MeetupData(object):
    """Defines the test objects for meetup tests"""
    missing_tag_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "location": "Andela Campus",
            "images": ["/images/important", "/images/meetup"],
            "topic": "Responsive Web Design",
            "happeningOn": "2018-04-23T18:25:43.511Z"
        },
        "url": "/api/v2/meetups"
    }
    missing_location_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "images": ["/images/important", "/images/meetup"],
            "topic": "Responsive Web Design",
            "Tags": ["User Interface", "Responsive Design"],
            "happeningOn": "2018-04-23T18:25:43.511Z"
        },
        "url": "/api/v2/meetups"
    }
    missing_meetup_date_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "location": "Andela Campus",
            "images": ["/images/important", "/images/meetup"],
            "topic": "Responsive Web Design",
            "Tags": ["User Interface", "Responsive Design"],
        },
        "url": "/api/v2/meetups"
    }
    missing_image_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "location": "Andela Campus",
            "topic": "Responsive Web Design",
            "Tags": ["User Interface", "Responsive Design"],
            "happeningOn": "2018-04-23T18:25:43.511Z"
        },
        "url": "/api/v2/meetups"
    }
    invalid_post_object_data = {
        "headers": {
        },
        "data": {
            "location": "Andela Campus",
            "images": ["/images/important", "/images/meetup"],
            "topic": "Responsive Web Design",
            "Tags": ["User Interface", "Responsive Design"],
            "happeningOn": "2018-04-23T18:25:43.511Z"
        },
        "url": "/api/v2/meetups"
    }
    valid_meetup_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "location": "Andela Campus",
            "images": ["/images/important", "/images/meetup"],
            "topic": "Responsive Web Design",
            "Tags": ["User Interface", "Responsive Design"],
            "happeningOn": "2018-04-23T18:25:43.511Z"
        },
        "url": "/api/v2/meetups"
    }


class QuestionData(object):
    """Defines Question data used for testing"""

    def __init__(self):
        self.data = {
            "title": "Responnsive Web design",
            "createdBy": 1,
            "body": "What is the best way of getting around responsiveness of a website",
            "meetup": 1
        }


class RsvpData(object):
    """Defines test data for Rsvp"""

    def __init__(self):
        self.data = {
            "user": 1,
            "response": "yes",
            "url": ""
        }


class UserData(object):
    """Defines a blueprint for user test data"""

    def __init__(self):
        self.data = {
            "firstname": "Ogutu",
            "lastname": "Brian",
            "othername": "Okinyi",
            "phoneNumber": "0703812914",
            "username": "Brian",
            "email": "codingbrian58@gmail.com",
            "password": "password12#B"
        }
