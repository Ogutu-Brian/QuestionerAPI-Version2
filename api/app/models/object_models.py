from typing import Dict
from datetime import date
import datetime


class BaseModel(object):
    """Contains properties shared accorss all the models"""

    def __init__(self, id_="", created_on=date.today()):
        self.id = id_
        self.created_on = created_on

    def to_dictionary(self)->Dict:
        """Method to be overriden by child classes to return object properties in to dictionary
        format
        """
        pass

    def created_date(self):
        """Reeturns date created as a formatted string (day-month-year) if date is provided"""
        return self.created_on.strftime('%d-%m-%Y')


class User(BaseModel):
    """A model for user information"""

    def __init__(self, id_="", created_on=datetime.date.today(), first_name="", last_name="",
                 other_name="", email="", phone_number="", user_name="", is_admin="False", password=""):
        super().__init__(id_=id_, created_on=created_on)
        self.first_name = first_name
        self.last_name = last_name
        self.other_name = other_name
        self.email = email
        self.phone_number = phone_number
        self.user_name = user_name
        self.registred = self.created_date()
        self.is_admin = is_admin
        self.password = password
        self.id = id_

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

    def __init__(self, id_="", created_on=datetime.date.today(), location="", images=[],
                 topic="", happening_on="", tags=[], creaed_by=""):
        super().__init__(id_=id_, created_on=created_on)
        self.topic = topic
        self.happening_on = happening_on
        self.tags = tags
        self.location = location
        self.images = images
        self.created_by = creaed_by
        self.id = id_

    def to_dictionary(self)->Dict:
        """
        Overrides the method from Basemodel to convert object properties into a dictionary
        data structure
        """
        return {
            "id": self.id,
            "createdOn": self.created_date(),
            "location": self.location,
            "images": self.images,
            "topic": self.topic,
            "happendingOn": self.happening_on,
            "tags": self.tags,
        }


class Question(BaseModel):
    """Defines the properties specific to a Question object"""

    def __init__(self, id_="", created_on=date.today(), created_by="", meet_up="",
                 title="", body="", votes=0):
        super().__init__(id_=id_, created_on=created_on)
        self.created_by = created_by
        self.meet_up = meet_up
        self.title = title
        self.body = body
        self.votes = votes
        self.id = id_

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

    def __init__(self, id_="", creatd_om=date.today(), meetup="", user="", response=""):
        super().__init__(id_=id_, created_on=creatd_om)
        self.meetup = meetup
        self.user = user
        self.response = response
        self.primary = (self.meetup, self.user)
        self.id = id_

    def to_dictionary(self)->Dict:
        """Overrides the basemodel method to represent an Rsvp object in a dictionary format"""
        return {
            "id": self.id,
            "primaryKey": self.primary,
            "meetup": self.meetup,
            "user": self.user,
            "response": self.response
        }


class BlackList(BaseModel):
    def __init__(self, id="", created_on=date.today(), token=""):
        super().__init__(id_=id, created_on=created_on)
        self.token = token

    def to_dictionary(self)->Dict:
        """Returns the token object as a dictionary"""
        return {
            "id": self.id,
            "token": self.token
        }
