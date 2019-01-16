import re


class UserValidators(object):
    """ Checks done on User data during Post"""

    def is_valid(self, item):
        errors = []
        if not item.get("firstname"):
            errors.append({
                "message": "First name must be provided"
            })
        if not item.get("lastname"):
            errors.append({
                "message": "Last name must be provided"
            })
        if not item.get("email"):
            errors.append({
                "message": "email must be provided"
            })
        else:
            for object_ in self.data.values():
                if object_.to_dictionary().get("email") == item.get("email"):
                    errors.append({
                        "message": "The email address has already been taken"
                    })
        if not item.get("phoneNumber"):
            errors.append({
                "message": "Phone number must be provided"
            })
        if not item.get("username"):
            errors.append({
                "message": "username must be provided"
            })
        else:
            for object_ in self.data.values():
                if object_.to_dictionary().get("username") == item.get("username"):
                    errors.append({
                        "message": "The username has already been taken"
                    })
                    break
        if not item.get("password"):
            errors.append({
                "message": "Password must be provided"
            })
        else:
            password = item.get("password")
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

    def is_valid(self, item):
        errors = []
        if not item.get("location"):
            errors.append({
                "message": "Location of meetup must be provided",
            })
        if not item.get("topic"):
            errors.append({
                "message": "topic must be provided"
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

    def is_valid(self, item):
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

    def is_valid(self, item):
        errors = []
        if not item.get("user"):
            errors.append({
                "message": "A user responding to rsvp must be provided",
            })
        if not item.get("response"):
            errors.append({
                "message": "A response must be provided"
            })
        elif item.get("response").lower() not in ["yes", "no", "maybe"]:
            errors.append({
                "message": "The response should be either yes, no or maybe"
            })
        return len(errors) == 0, errors