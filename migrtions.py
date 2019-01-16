"""
Creates a database Schema
When the file is run directly it clears data in all the tables
"""
from api.app.models.models import User, Question, Rsvp, Meetup


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

    @classmethod
    def makemigrations(cls)->None:
        User.migrate()
        Question.migrate()
        Meetup.migrate()
        Rsvp.migrate()


if __name__ == "__main__":
    DbMigrations.tear_down()
