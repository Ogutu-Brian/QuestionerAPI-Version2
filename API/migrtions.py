"""
Creates a database Schema
When the file is run directly it clears data in all the tables
"""
from app.api.v2.models.models import User, Question


class DbMigrations(object):
    """
    Class That handles migrations
    """
    @classmethod
    def tear_down(cls)->None:
        """The method clears the data within the rows"""
        User.clear()
        Question.clear()

    @classmethod
    def makemigrations(cls)->None:
        User.migrate()
        Question.migrate()


if __name__ == "__main__":
    DbMigrations.tear_down()
