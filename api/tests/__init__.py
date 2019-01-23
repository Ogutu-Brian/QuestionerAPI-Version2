class MeetupData(object):
    """Defines the test objects for meetup tests"""

    def __init__(self):
        self.data = {
            "location": "Andela Campus",
            "images": "['/images/important', '/images/meetup']",
            "topic": "Responsive Web Design",
            "Tags": "['User Interface', 'Responsive Design']",
            "happeningOn": "2018-04-23T18:25:43.511Z"
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
        }


class UserData(object):
    """Defines a blueprint for user test data"""

    def __init__(self):
        self.data = {
            "firstname": "Ogutu",
            "lastname": "Brian",
            "othername": "Okinyi",
            "phoneNumber": "+254703812914",
            "username": "Brian",
            "email": "codingbrian58@gmail.com",
            "password": "password12#B",
            "isAdmin": "True"
        }


class CommentData(object):
    """a blueprint of comment test data"""

    def __init__(self):
        self.data = {
            "question": 1,
            "comment": "That is a good question"
        }
