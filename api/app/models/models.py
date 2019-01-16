from typing import Dict, List
from api.app.models.object_models import BaseModel as V1Base
from api.app.models.object_models import User as V1user
from api.app.models.object_models import Question as V1Question
from api.app.models.object_models import Meetup as V1Meetup
from api.app.models.object_models import Rsvp as V1Rsvp
from api.app.models.object_models import BlackList as V1BlackList
from run import database


class BaseModel(V1Base):
    """
    A template class for other models
    """

    table_name = ""

    @classmethod
    def migrate(cls)->None:
        """
        A method for creating the tables, it is overdden by the child classes
        :return:
        """
        pass

    @classmethod
    def clear(cls)->None:
        """
        Deletes all data from the table
        """
        database.cursor.execute("DELETE FROM {}".format(cls.table_name))
        database.connection.commit()

    @classmethod
    def to_object(cls, query):
        """
        a method that converts a queried item into an object
        """
        pass

    @classmethod
    def query_all(cls)->List:
        """
        Queries all content from a table"
        """
        database.cursor.execute("SELECT * FROM {}".format(cls.table_name))
        items = database.cursor.fetchall()
        return [cls.to_object(item) for item in items]

    @classmethod
    def query_by_field(cls, field: str, value: str)->List:
        """
        Queries all items with a given field name
        """
        database.cursor.execute(
            "SELECT * FROM {} WHERE {} = {}".format(cls.table_name, field, str(value)))
        items = database.cursor.fetchall()
        return [cls.to_object(item) for item in items]

    def delete(self)->None:
        """
        Deletes an item from the database
        """
        database.cursor.execute(
            "DELETE FROM {} WHERE id={}".format(self.table_name, self.id))
        database.connection.commit()

    def save(self)->None:
        """
        Saves an item into the databasw, it is to be overridden by child classes
        """
        pass


class User(V1user, BaseModel):
    """ 
    Defines user table and operations to be perormed on the table
    """
    table_name = "users"

    @classmethod
    def migrate(cls):
        """creates users table"""
        database.cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id serial PRIMARY KEY,
            firstname varchar,
            lastname varchar,
            othernames varchar,
            email varchar,
            phone varchar,
            username varchar,
            password varchar,
            role varchar
        )""")
        database.connection.commit()

    @classmethod
    def to_object(cls, query_dict):
        """Returns queried value as an object"""
        user = User()
        user.id = query_dict.get("id")
        user.first_name = query_dict.get("firstname")
        user.last_name = query_dict.get("lastname")
        user.other_name = query_dict.get("othernames")
        user.email = query_dict.get("email")
        user.phone_number = query_dict.get("phone")
        user.user_name = query_dict.get("username")
        user.is_admin = bool(query_dict.get("role"))
        return user

    def save(self):
        """
        Saves a user object into database
        """
        database.cursor.execute(
            "INSERT INTO users(firstname,lastname,othernames,email,phone,username,password,role) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                self.first_name,
                self.last_name,
                self.other_name,
                self.email,
                self.phone_number,
                self.user_name,
                self.password,
                self.is_admin
            ))
        database.connection.commit()


class Question(V1Question, BaseModel):
    """Defines table structure and operations for Questions"""
    table_name = "questions"

    @classmethod
    def migrate(cls):
        database.cursor.execute("""CREATE TABLE IF NOT EXISTS questions (
            id serial PRIMARY KEY,
            created_date varchar,
            created_by integer,
            meetup integer,
            title varchar,
            body varchar,
            votes integer
        )""")
        database.connection.commit()

    @classmethod
    def to_object(cls, query_dict):
        """Converts query string into a question object"""
        question = Question()
        question.id = query_dict.get("id")
        question.created_date = query_dict.get("created_date")
        question.created_by = query_dict.get("created_by")
        question.meet_up = query_dict.get("meetup")
        question.title = query_dict.get("title")
        question.body = query_dict.get("body")
        question.votes = query_dict.get("votes")
        return question

    def save(self):
        """Saves a question object into the database"""
        database.cursor.execute("INSEER INTO questions(created_date,created_by,meetup,title,body,votes) VALUES(%s,%s,%s,%s,%s,%s)", (
            self.created_date,
            self.created_by,
            self.meet_up,
            self.title,
            self.body,
            self.votes
        ))
        database.connection.commit()


class Rsvp(V1Rsvp, BaseModel):
    table_name = "rsvps"

    @classmethod
    def migrate(cls):
        """Creates the rsvp table during migrations"""
        database.cursor.execute("""CREATE TABLE IF NOT EXISTS rsvps (
            creatd_date varchar,
            meetup integer,
            user_id integer,
            response varchar,
            PRIMARY KEY(meetup,user_id)
        )""")
        database.connection.commit()

    @classmethod
    def to_object(cls, query_dict):
        """Converts the query into Rsvp object"""
        rsvp = Rsvp()
        rsvp.meetup = query_dict.get("meetup")
        rsvp.user = query_dict.get("user_id")
        rsvp.response = query_dict.get("response")
        return rsvp

    def save(self):
        """Saves Rsvp object to database"""
        database.cursor.execute("INSERT INTO rsvps(created_date,meetup,user_id,response) VALUES(%s,%s,%s,%s)", (
            self.created_date,
            self.meetup,
            self.user,
            self.response
        ))
        database.connection.commit()


class Meetup(V1Meetup, BaseModel):
    table_name = "meetups"

    @classmethod
    def migrate(cls):
        """Creates meetups table during migrations"""
        database.cursor.execute("""CREATE TABLE IF NOT EXISTS meetups(
            id serial PRIMARY KEY,
            topic varchar,
            happening_date varchar,
            tags varchar,
            location varchar,
            images varchar,
            creator integer
        )""")
        database.connection.commit()

    @classmethod
    def to_object(cls, query_dict):
        """used to convert queries into meetup objects"""
        meetup = Meetup()
        meetup.topic = query_dict.get("topic")
        meetup.happening_on = query_dict.get("happening_date")
        meetup.location = query_dict.get("location")
        meetup.images = query_dict.get("images")
        meetup.created_by = query_dict.get("creator")
        return meetup

    def save(self):
        """Saves the meetup object into the database"""
        database.cursor.execute("INSERT INTO meetups(topic,happening_date,tags,location,images,creator) VALUES(%s,%s,%s,%s,%s,%s)", (
            self.topic,
            self.happening_on,
            self.tags,
            self.location,
            self.images,
            self.created_by
        ))
        database.connection.commit()


class TokenBlackList(V1BlackList, BaseModel):
    """Hodls blacklisted jwt tokens"""
    table_name = "blacklist"

    @classmethod
    def migrate(cls):
        """Creates table for holding blacklisted tokens"""
        database.cursor.execute("""CREATE TABLE IF NOT EXISTS blacklist(
            id serial PRIMARY KEY,
            token varchar
        )""")
        database.connection.commit()

    def save(self):
        """Saves a blacklist token into blacklst database"""
        database.cursor.execute(
            "INSERT INTO blacklist (token) VALUES(%s)", (self.token,))

    @classmethod
    def to_object(cls, query_dict):
        """Changes the query into a blacklist object"""
        blacklist_token = TokenBlackList()
        blacklist_token.id = query_dict.get("id")
        blacklist_token.token = query_dict.get("token")
        return blacklist_token
