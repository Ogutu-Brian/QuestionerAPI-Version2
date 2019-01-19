"""
Creates a database Schema
When the file is run directly it clears data in all the tables
"""
from api.app.models.models import (
    User, Question, Rsvp, Meetup, TokenBlackList, Comment)


class DbMigrations(object):
    """
    Class That handles migrations
    """
    @classmethod
    def tear_down(cls)->None:
        """The method clears the data within the rows"""
        User.clear()
        Question.clear()
        Meetup.clear()
        Rsvp.clear()
        TokenBlackList.clear()
        Comment.clear()

    @classmethod
    def drop_tables(cls)->None:
        """Drops all the tables in the database"""
        User.drop_table()
        Question.drop_table()
        Meetup.drop_table()
        Rsvp.drop_table()
        TokenBlackList.drop_table()
        Comment.drop_table()

    @classmethod
    def makemigrations(cls)->None:
        """Creates tables in QUestioner database"""
        User.migrate()
        Question.migrate()
        Meetup.migrate()
        Rsvp.migrate()
        TokenBlackList.migrate()
        Comment.migrate()


if __name__ == "__main__":
    DbMigrations.tear_down()
