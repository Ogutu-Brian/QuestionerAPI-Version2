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
    valid_question_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "title": "Responnsive Web design",
            "createdBy": 1,
            "body": "What is the best way of getting around responsiveness of a website",
            "meetup": 1
        },
        "url": "/api/v2/questions"
    }
    missing_creator_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "title": "Responnsive Web design",
            "body": "What is the best way of getting around responsiveness of a website",
            "meetup": 1
        },
        "url": "/api/v2/questions"
    }
    missing_body_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "title": "Responnsive Web design",
            "createdBy": 1,
            "meetup": 1
        },
        "url": "/api/v2/questions"
    }
    missing_meetup_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "title": "Responnsive Web design",
            "createdBy": 1,
            "body": "What is the best way of getting around responsiveness of a website",
        },
        "url": "/api/v2/questions"
    }
    invalid_user_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "title": "Responnsive Web design",
            "createdBy": -2,
            "body": "What is the best way of getting around responsiveness of a website",
            "meetup": 1
        },
        "url": "/api/v2/questions"
    }
    invalid_meetup_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "title": "Responnsive Web design",
            "createdBy": 1,
            "body": "What is the best way of getting around responsiveness of a website",
            "meetup": -2
        },
        "url": "/api/v2/questions"
    }
    valid_upvote_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "title": "Responnsive Web design",
            "createdBy": 1,
            "body": "What is the best way of getting around responsiveness of a website",
            "meetup": 1
        },
        "url": "/api/v2/questions"
    }
    unexsiting_query_upvote_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "title": "Responnsive Web design",
            "createdBy": 1,
            "body": "What is the best way of getting around responsiveness of a website",
            "meetup": 1
        },
        "url": "/api/v2/questions"
    }
    valid_downvote_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "title": "Responnsive Web design",
            "createdBy": 1,
            "body": "What is the best way of getting around responsiveness of a website",
            "meetup": 1
        },
        "url": "/api/v2/questions"
    }
    unexisting_downvote_query_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "title": "Responnsive Web design",
            "createdBy": 1,
            "body": "What is the best way of getting around responsiveness of a website",
            "meetup": 1
        },
        "url": "/api/v2/questions"
    }


class RsvpData(object):
    """Defines test data for Rsvp"""
    valid_rsvp_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "user": 1,
            "response": "yes",
            "url": ""
        }
    }
    missing_user_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "response": "yes",
            "url": ""
        }
    }
    missing_response_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "data": {
            "user": 1,
            "url": ""
        }
    }


class UserData(object):
    """Defines a blueprint for user test data"""
    valid_user_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "sign_up": {
            "firstname": "Ogutu",
            "lastname": "Brian",
            "othername": "Okinyi",
            "phoneNumber": "0703812914",
            "username": "Brian",
            "email": "codingbrian58@gmail.com",
            "password": "password12#B"
        },
        "sign_up_url": "/api/v2/users/sign-up",
        "log_in_url": "/api/v2/users/log-in"
    }
    missing_mail_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "firstname": "Ogutu",
        "lastname": "Brian",
        "othername": "Okinyi",
        "phoneNumber": "0703812914",
        "username": "Brian",
        "password": "password12#B"
    }
    missing_password_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "firstname": "Ogutu",
        "lastname": "Brian",
        "othername": "Okinyi",
        "phoneNumber": "0703812914",
        "username": "Brian",
    }
    invalid_password_data = {
        "headers": {
            "Content-Type": "application/json"
        },
        "sign_up": {
            "firstname": "Ogutu",
            "lastname": "Brian",
            "othername": "Okinyi",
            "phoneNumber": "0703812914",
            "username": "Brian",
            "email": "codingbrian58@gmail.com",
            "password": ""
        },
        "sign_up_url": "/api/v2/users/sign-up",
        "log_in_url": "/api/v2/users/log-in"
    }
    missing_first_name_data = {
        "lastname": "Brian",
        "othername": "Okinyi",
        "phoneNumber": "0703812914",
        "username": "Brian",
        "email": "codingbrian58@gmail.com",
        "password": "password12#B"
    }
    missing_last_name_data = {
        "firstname": "Ogutu",
        "othername": "Okinyi",
        "phoneNumber": "0703812914",
        "username": "Brian",
        "email": "codingbrian58@gmail.com",
        "password": "password12#B"
    }
    missing_phone_number_data = {
        "firstname": "Ogutu",
        "lastname": "Brian",
        "othername": "Okinyi",
        "username": "Brian",
        "email": "codingbrian58@gmail.com",
        "password": "password12#B"
    }
    missing_user_name_data = {
        "firstname": "Ogutu",
        "lastname": "Brian",
        "othername": "Okinyi",
        "phoneNumber": "0703812914",
        "email": "codingbrian58@gmail.com",
        "password": "password12#B"
    }
    complete_data = {
        "firstname": "Ogutu",
        "lastname": "Brian",
        "othername": "Okinyi",
        "phoneNumber": "0703812914",
        "username": "Brian",
        "email": "codingbrian58@gmail.com",
        "password": "password12#B"
    }
    valid_login_data = {
        "firstname": "Ogutu",
        "lastname": "Brian",
        "othername": "Okinyi",
        "phoneNumber": "0703812914",
        "username": "Brian",
        "email": "codingbrian58@gmail.com",
        "password": "password12#B"
    }
    missing_user_name_and_mail_data = {
        "password": "password12#B"
    }
    missing_log_in_password_data = {
        "email": "codingbrian58@gmail.com",
    }
    log_in_data = {
        "email": "codingbrian58@gmail.com",
        "password": "password12#B4"
    }
    wrong_log_password_data = {
        "email": "codingbrian58@gmail.com",
        "password": "passwoeoefoen"
    }
    unexisting_user_name_data = {
        "username": "TeSTm",
        "password": "password12#B4"
    }
    unexsiting_mail_data = {
        "email": "testmaiddl.@gmail.com",
        "password": "password12#B"
    }


user_data = UserData()
rsvp_data = RsvpData()
meetup_data = MeetupData()
question_data = QuestionData()
