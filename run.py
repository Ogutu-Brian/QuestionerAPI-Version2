from flask import Flask
from api.app.models.database import PostgresDatabase
from api.instance.config import app_config
from flask_jwt_extended import JWTManager

database = PostgresDatabase()

from migrtions import DbMigrations


def create_app(application_config):
    """main flask application"""
    app = Flask(__name__)
    app.config.from_object(app_config.get(application_config))
    database.initialize_application(app)
    jwt = JWTManager(app)
    return app


app = create_app("DEVELOPMENT")
DbMigrations.makemigrations()
if __name__ == "__main__":
    app.run()
