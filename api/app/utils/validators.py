import re
from typing import Tuple, Dict
from datetime import date


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


def date_checker(item_date: str)->bool:
    """Checks if the previous date is greater than or equal to today"""
    response = False
    today_list = date.today().strftime('%d-%m-%Y').split('-')
    happening_list = item_date.split('-')
    if int(happening_list[2]) >= int(today_list[2]):
            if int(happening_list[1]) >= int(today_list[1]):
                if int(happening_list[0]) >= int(today_list[0]):
                    response = True
    return response


def valid_input_date(date_string: str)->bool:
    """Checks if the input date is of the right format"""
    response = False
    if len(date_string.split('-')) == 3:
        date_list = date_string.split('-')
        if date_list[0].isdigit() and date_list[1].isdigit() and date_list[2].isdigit():
            if int(date_list[0])<=31 and int(date_list[1])<=12 and int(date_list[2]) <=3000:
                response = True
    return response


class UserValidators(object):
    """ Checks done on User data during Post"""
    @classmethod
    def is_valid(cls, item: Dict)->Tuple:
        """Validates post User data"""
        email_regex = '[^@]+@[^@]+\.[^@]+'
        errors = []
        firstname = item.get("firstname")
        lastname = item.get("lastname")
        password = item.get("password")
        confirmPassword = item.get("confirmpassword")
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
        elif len(phoneNumber) == 9:
            if phoneNumber[0] != '7':
                errors.append({
                    "message": "The phone number is invalid"
                })
                if not re.match('[0-9]', phoneNumber):
                    errors.append({
                        "message": "The phone number is invalid"
                    })
        elif len(phoneNumber) == 10:
            if not re.match('[0-9]', phoneNumber):
                errors.append({
                    "message": "The phone number is invalid"
                })
        elif len(phoneNumber) == 13:
            if not re.match('[0-9]', phoneNumber.strip(phoneNumber[0])) or phoneNumber[0] != '+':
                errors.append({
                    "message": "The phone number is invalid"
                })
        elif len(phoneNumber) > 13:
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
            if not confirmPassword:
                errors.append({
                    "message": "Please confirm password"
                })
            else:
                if password != confirmPassword:
                    errors.append({
                        "message": "The password does not match"
                    })
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
        elif not valid_input_date(item.get("happeningOn")):
            errors.append({
                "message":"The date format is invalid, please use the format dd-mm-yy"
            })
        elif not valid_input_date(item.get("happeningOn")):
            errors.append({
                "message": "The date format given is invalid"
            })
        elif not date_checker(item.get("happeningOn")):
            errors.append({
                "message": "You cannot create a meetup in a passed day"
            })
        if not item.get("body"):
            errors.append({
                "message": "Please provide the body of the meetup"
            })
        elif not valid_input_string(item.get("body")):
            errors.append({
                "message": "Please enter a valid data in the body"
            })
        return len(errors) == 0, errors


class QuestionValidators(object):
    """Validation done on Question data during Posts"""
    @classmethod
    def is_valid(cls, item: Dict)->Tuple:
        """validates Post Question data"""
        errors = []
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
