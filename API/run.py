from flask import Flask
from app.api.v2.models.database import PostgresDatabase
from instance.config import app_config

database = PostgresDatabase()

from migrtions import DbMigrations


def create_app(application_config):
    """main flask application"""
    app = Flask(__name__)
    app.config.from_object(app_config.get(application_config))
    database.initialize_application(app)
    return app


app = create_app("DEVELOPMENT")
DbMigrations.makemigrations()
if __name__ == "__main__":
    app.run()
