from migrtions import DbMigrations
from flask import Flask
from api.app.models.database import PostgresDatabase
from api.instance.config import app_config
from flask_jwt_extended import JWTManager
from flask import jsonify, Blueprint
from api.app.views import Status
from api.app.views.user_views import user_view

database = PostgresDatabase()


def create_app(application_config):
    """main flask application"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config.get(application_config))
    database.initialize_application(app)
    jwt = JWTManager(app)
    app.register_blueprint(user_view, url_prefix="/api/v2/users")

    @jwt.token_in_blacklist_loader
    def is_valid_token(token):
        """Checks if the token exists in the black list table"""
        from api.app.models.models import TokenBlackList
        return len(TokenBlackList.query_by_field("token", token['jti'])) == 0

    @jwt.invalid_token_loader
    def unauthorired_access(error):
        return jsonify({
            "message": "The token provided is not valid",
            "status": Status.denied_access,
        }), Status.denied_access

    @jwt.expired_token_loader
    def expired_token_result():
        """Checks if toen has expired"""
        return jsonify({
            "message": "Your token has expired",
            "status": Status.denied_access
        }), Status.denied_access

    @jwt.unauthorized_loader
    def unauthoriszed(error):
        return jsonify({
            "message": "Token Bearer not given",
            "status": Status.denied_access
        }), Status.denied_access

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "message": "Resource unavalable in the url",
            "status": Status.not_found
        }), Status.not_found

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "message": "Please check the request method you are using",
            "status": Status.bad_requst
        }), Status.bad_requst
    return app


app = create_app("DEVELOPMENT")
DbMigrations.makemigrations()
if __name__ == "__main__":
    app.run()
