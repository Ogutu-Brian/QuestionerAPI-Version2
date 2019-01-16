import psycopg2
from psycopg2.extras import DictCursor


class PostgresDatabase(object):
    """Initializees the database"""

    def __init__(self):
        self.app = None
        self.connection = None
        self.cursor = None

    def initialize_application(self, app)->None:
        """Initializes the database connection"""
        self.app = app
        self.connection = psycopg2.connect(dbname=app.config.get("DATABASE_NAME"), user=app.config.get(
            "DATABASE_USER"), password=app.config.get("DATABASE_PASSWORD"), host=app.config.get("DATABASE_HOST"))
        self.cursor = self.connection.cursor(cursor_factory=DictCursor)
