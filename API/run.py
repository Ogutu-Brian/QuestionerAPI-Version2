from flask import Flask
from app.api.v2.models.database import PostgresDatabase
from instance.config import app_config

database = PostgresDatabase()


def create_app(application_config):
    """main flask application"""
    app = Flask(__name__)
    app.config.from_object(app_config.get(application_config))
    return app


app = create_app("DEVELOPMENT")
if __name__ == "__main__":
    app.run()
