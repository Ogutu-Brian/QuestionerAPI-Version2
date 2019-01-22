import re
from typing import Tuple, Dict
from validate_email import validate_email


def valid_input_string(input_string: str)->bool:
    """Checks if the input string begins wwith an empty line"""
    regex = '[a-zA-Z0-9]'
    name_regex = '[a-zA-Z]'
    response = True
    if not re.match(regex, input_string[0]):
        response = False
    if not re.match(name_regex, input_string.strip()):
        response = False
    return response


class UserValidators(object):
    """ Checks done on User data during Post"""
    @classmethod
    def is_valid(cls, item: Dict)->Tuple:
        """Validates post User data"""
        email_regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
        errors = []
        firstname = item.get("firstname")
        lastname = item.get("lastname")
        password = item.get("password")
        email = item.get("email")
        phoneNumber = item.get("phoneNumber")
        username = item.get("username")
        if not firstname:
            errors.append({
                "message": "First name must be provided"
            })
        elif not valid_input_string(firstname):
            errors.append({
                "message": "the first name you entered is not valid"
            })
        if not lastname:
            errors.append({
                "message": "Last name must be provided"
            })
        elif not valid_input_string(lastname):
            errors.append({
                "message": "The last name you provided is not valid"
            })
        if not email:
            errors.append({
                "message": "email must be provided"
            })
        elif not re.match(email_regex, email):
            errors.append({
                "message": "The email address is not valid"
            })
        if not phoneNumber:
            errors.append({
                "message": "Phone number must be provided"
            })
        elif not re.match('[0-9]', phoneNumber.strip(phoneNumber[0])) or phoneNumber[0] != '+':
            errors.append({
                "message": "The phone number is invalid"
            })
        if not username:
            errors.append({
                "message": "username must be provided"
            })
        elif not valid_input_string(username):
            errors.append({
                "message": "The username provided is not valid"
            })
        if not password:
            errors.append({
                "message": "Password must be provided"
            })
        else:
            if len(password) < 6:
                errors.append({
                    "message": "The password is too short"
                })
            elif len(password) > 12:
                errors.append({
                    "message": "Password length should be between 6 and 11"
                })
            elif not re.search('[A-Z]', password):
                errors.append({
                    "message": "The password should at least contain an Uppercase Letter"
                })
            elif not re.search('[$#@]', password):
                errors.append({
                    "message": "The password needs to contain at least #,$ or @ symbols"
                })
            elif not re.search('[0-9]', password):
                errors.append({
                    "message": "The password needs to contain a number"
                })
        return len(errors) == 0, errors


class MeetupValidators(object):
    """Validation done on Meetup data during posts"""
    @classmethod
    def is_valid(cls, item: Dict)->Tuple:
        """Validates post Meetup data"""
        errors = []
        if not item.get("location"):
            errors.append({
                "message": "Location of meetup must be provided",
            })
        elif not valid_input_string(item.get("location")):
            errors.append({
                "message": "The location you entered is not valid"
            })
        if not item.get("topic"):
            errors.append({
                "message": "topic must be provided"
            })
        elif not valid_input_string(item.get("topic")):
            errors.append({
                "message": "The topic is not valid"
            })
        if not item.get("Tags"):
            errors.append({
                "message": "Tags must be provided"
            })
        if not item.get("happeningOn"):
            errors.append({
                "message": "Happening hodling date must be provided"
            })
        return len(errors) == 0, errors


class QuestionValidators(object):
    """Validation done on Question data during Posts"""
    @classmethod
    def is_valid(cls, item: Dict)->Tuple:
        """validates Post Question data"""
        errors = []
        if not item.get("createdBy"):
            errors.append({
                "message": "User asking the question must be provided"
            })
        if not item.get("meetup"):
            errors.append({
                "message": "The meetup the question is for must be provided"
            })
        if not item.get("title"):
            errors.append({
                "message": "Title of question must be provided"
            })
        if not item.get("body"):
            errors.append({
                "message": "Body of question must be provoded"
            })
        return len(errors) == 0, errors


class RsvpValidators(object):
    """Vallidation done on Rsvp Data during post"""
    @classmethod
    def is_valid(cls, item: Dict)->Tuple:
        """Validates a post Rsvp data"""
        errors = []
        if not item.get("response"):
            errors.append({
                "message": "A response must be provided"
            })
        elif item.get("response").lower() not in ["yes", "no", "maybe"]:
            errors.append({
                "message": "The response should be either yes, no or maybe"
            })
        return len(errors) == 0, errors


class CommentValidators(object):
    """Validates Comment data during Posting"""
    @classmethod
    def is_valid(cls, item: Dict)->Tuple:
        """validates a post comment data"""
        errors = []
        if not item.get("question"):
            errors.append({
                "message": "You need to provide the question id"
            })
        elif not item.get("comment"):
            errors.append({
                "message": "You need to provide a comment to the question"
            })
        return len(errors) == 0, errors
