from flask import Flask,jsonify, Blueprint,request
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

database = PostgresDatabase()

from migrtions import DbMigrations

load_dotenv()
def create_app(application_config):
    """main flask application"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config.get(application_config))
    database.initialize_application(app)
    jwt = JWTManager(app)
    app.register_blueprint(user_view, url_prefix="/api/v2/auth")
    app.register_blueprint(meetup_view, url_prefix="/api/v2")
    app.register_blueprint(question_view, url_prefix="/api/v2")
    app.register_blueprint(comment_view, url_prefix="/api/v2")
    Swagger(app=app)

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
        return jsonify({
            "error": "The token provided is not valid",
            "status": Status.denied_access,
        }), Status.denied_access

    @jwt.expired_token_loader
    def expired_token():
        """Checks if toen has expired"""
        return jsonify({
            "error": "Your token has expired",
            "status": Status.denied_access
        }), Status.denied_access

    @jwt.unauthorized_loader
    def unauthoriszed(error):
        return jsonify({
            "error": "Token Bearer not given",
            "status": Status.denied_access
        }), Status.denied_access

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "error": "Resource unavalable in the url",
            "status": Status.not_found
        }), Status.not_found

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "bad request",
            "status": Status.bad_requst
        }), Status.bad_requst
    return app
app = create_app("DEVELOPMENT")
DbMigrations.makemigrations()
if __name__ == "__main__":
    app.run()
