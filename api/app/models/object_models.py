from typing import Dict
from datetime import date
import datetime


class BaseModel(object):
    """Contains properties shared accorss all the models"""

    def __init__(self):
        self.id = None
        self.created_on = date.today().strftime('%d-%m-%Y')

    def to_dictionary(self)->Dict:
        """Method to be overriden by child classes to return object properties in to dictionary
        format
        """
        pass


class User(BaseModel):
    """A model for user information"""

    def __init__(self, email="", user_name="", is_admin="False", password=""):
        super().__init__()
        self.first_name = ""
        self.last_name = ""
        self.other_name = ""
        self.email = email
        self.phone_number = ""
        self.user_name = user_name
        self.registred = self.created_on
        self.is_admin = is_admin
        self.password = password

    def __str__(self):
        return self.first_name + " "+self.last_name

    def to_dictionary(self)->Dict:
        """Overrides the basemodel's method to present user object data in dictionary format"""
        return {
            "id": self.id,
            "firstname": self.first_name,
            "lastname": self.last_name,
            "othername": self.other_name,
            "email": self.email,
            "phoneNumber": self.phone_number,
            "username": self.user_name,
            "registered": self.registred,
            "isAdmin": self.is_admin
        }


class Meetup(BaseModel):
    """Defines the properties specific to a Meetup"""

    def __init__(self, location="", images=[],
                 topic="", happening_on="", tags=[], creaed_by="", body=""):
        super().__init__()
        self.topic = topic
        self.happening_on = happening_on
        self.tags = tags
        self.location = location
        self.images = images
        self.created_by = creaed_by
        self.body = body

    def to_dictionary(self)->Dict:
        """
        Overrides the method from Basemodel to convert object properties into a dictionary
        data structure
        """
        return {
            "id": self.id,
            "createdOn": self.created_on,
            "location": self.location,
            "images": self.images,
            "topic": self.topic,
            "happeningOn": self.happening_on,
            "tags": self.tags,
            "body": self.body
        }


class Question(BaseModel):
    """Defines the properties specific to a Question object"""

    def __init__(self, meet_up="", title="", body="", votes=0):
        super().__init__()
        self.created_by = None
        self.meet_up = meet_up
        self.title = title
        self.body = body
        self.votes = votes

    def to_dictionary(self)->Dict:
        """
        Overrides the BaseModel's method to return a dictionary representation of question
        object
        """
        return {
            "id": self.id,
            "createdOn": self.created_on,
            "createdBy": self.created_by,
            "meetup": self.meet_up,
            "title": self.title,
            "body": self.body,
            "votes": self.votes
        }


class Rsvp(BaseModel):
    """Defines attributes specific to Rsvp object"""

    def __init__(self, meetup="", user="", response=""):
        super().__init__()
        self.meetup = meetup
        self.user = user
        self.response = response
        self.primary = (self.meetup, self.user)

    def to_dictionary(self)->Dict:
        """Overrides the basemodel method to represent an Rsvp object in a dictionary format"""
        return {
            "id": self.id,
            "primaryKey": self.primary,
            "meetup": self.meetup,
            "user": self.user,
            "response": self.response
        }


class Comment(BaseModel):
    """Defines a template object class for Questions"""

    def __init__(self, question="", user="", comment="", title="", body=""):
        super().__init__()
        self.question = question
        self.comment = comment
        self.user = user
        self.title = title
        self.body = body

    def to_dictionary(self):
        """Displays the object in a dictionary format"""
        return {
            "question": self.question,
            "title": self.title,
            "body": self.body,
            "comment": self.comment
        }


class BlackList(BaseModel):
    """Stores blacklisted token"""

    def __init__(self, id="", token=""):
        super().__init__()
        self.token = token

    def to_dictionary(self)->Dict:
        """Returns the token object as a dictionary"""
        return {
            "id": self.id,
            "token": self.token
        }


class Vote(BaseModel):
    """A bluprint for Vote object"""

    def __init__(self, user="", question="", value=0):
        super().__init__()
        self.user = user
        self.question = question
        self.value = value
