from flask import Flask, jsonify, Blueprint, request
from api.app.models.database import PostgresDatabase
from api.instance.config import app_config
from flask_jwt_extended import JWTManager
from api.app.views import Status
from api.app.views.user_views import user_view
from api.app.views.meetup_views import meetup_view
from api.app.views.question_views import question_view
from api.app.views.comment_views import comment_view
from flasgger import Swagger
from dotenv import load_dotenv
from typing import Tuple
from flask_cors import CORS

database = PostgresDatabase()

from migrtions import DbMigrations

load_dotenv()


def error_response(error: str, status: int)->Tuple:
    """ A function to give responses depending on an error"""
    return jsonify({
        "error": error,
        "status": status
    }), status


def create_app(application_config):
    """main flask application"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config.get(application_config))
    database.initialize_application(app)
    jwt = JWTManager(app)
    CORS(app)
    app.register_blueprint(user_view, url_prefix="/api/v2/auth")
    app.register_blueprint(meetup_view, url_prefix="/api/v2")
    app.register_blueprint(question_view, url_prefix="/api/v2")
    app.register_blueprint(comment_view, url_prefix="/api/v2")

    @jwt.token_in_blacklist_loader
    def token_in_blaclist(token):
        """Checks if the token exists in the black list table"""
        from api.app.models.models import TokenBlackList
        response = False
        jti = token["jti"]
        if TokenBlackList.query_by_field("token", jti):
            response = True
        return response

    @jwt.invalid_token_loader
    def invalid_token(error):
        return error_response(error="The token provided is not valid", status=Status.denied_access)

    @jwt.expired_token_loader
    def expired_token():
        """Checks if toen has expired"""
        response = jsonify({
            "error": [{
                "message": "Your token has expired"
            }],
            "status": Status.denied_access
        }), Status.denied_access
        return response

    @jwt.unauthorized_loader
    def unauthoriszed(error):
        response = jsonify({
            "error": [{
                "message": "Token Bearer not given"
            }],
            "status": Status.denied_access
        }), Status.denied_access
        return response

    @app.errorhandler(404)
    def resource_not_found(error):
        response = jsonify({
            "error": [{
                "message": "Resource unavalable in the url"
            }],
            "status": Status.not_found
        }), Status.not_found
        return response

    @app.errorhandler(400)
    def bad_request(error):
        response = jsonify({
            "error": "bad request",
            "status": Status.bad_requst
        }), Status.bad_requst
        return response

    @app.route('/')
    def display_documentation():
        """Renders the documentation on the index pange"""
        response = jsonify({
            "message": "Welcome to Questioner API version2",
            "status": Status.success
        }), Status.success
        return response
    template = {
        "swagger": "3.0",
        "info": {
            "title": "Questioner API version2",
            "description": "Questioner API",
            "version": "2.0"
        }
    }
    Swagger(app=app, template=template)
    return app


app = create_app("DEVELOPMENT")
DbMigrations.drop_tables()
if __name__ == "__main__":
    app.run()
