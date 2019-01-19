from .import user_view
from flask import request, jsonify
from api.app.utils.validators import UserValidators
from .import Status
import bcrypt
from flask_jwt_extended import create_access_token
from typing import Tuple

@user_view.route("/signup", methods=["POST"])
def sign_up()->Tuple:
    """A post endpoint for creating a user account"""
    from api.app.models.models import User
    response = None
    if request.is_json:
        data = request.json
        valid, errors = UserValidators.is_valid(data)
        if not valid:
            response = jsonify({
                "message": "You encountered {} errors".format(len(errors)),
                "error": errors,
                "status": Status.invalid_data
            }), Status.invalid_data
        elif User.query_by_field("email", data.get("email")):
            response = jsonify({
                "error": "The email address has already been taken",
                "status": Status.invalid_data
            }), Status.invalid_data
        elif User.query_by_field("username", data.get("username")):
            response = jsonify({
                "error": "The username has already been taken",
                "status": Status.invalid_data
            }), Status.invalid_data
        else:
            other_name = ""
            if data.get("othername"):
                other_name = data.get("othername")
            first_name = data.get("firstname")
            last_name = data.get("lastname")
            email = data.get("email")
            phone_number = data.get("phoneNumber")
            user_name = data.get("username")
            is_admin = "False"
            if data.get("isAdmin").lower() == "true":
                is_admin = "True"
            password = bcrypt.hashpw(data.get("password").encode(
                'utf8'), bcrypt.gensalt()).decode('utf8')
            user = User(first_name=first_name, last_name=last_name, is_admin=is_admin,
                        other_name=other_name, email=email, phone_number=phone_number, user_name=user_name, password=password)
            user.save()
            response = jsonify({
                "message": "Successuflly signed up",
                "status": Status.created,
                "data": [user.to_dictionary()]
            }), Status.created
    else:
        response = jsonify({
            "error": "The data needs to be in JSON",
            "status": Status.not_json
        }), Status.not_json
    return response


@user_view.route("/login", methods=["POST"])
def login()->Tuple:
    """A post endpoint for logging a user into questioner"""
    response = None
    if request.is_json:
        data = request.json
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        if not email and not username:
            response = jsonify({
                "error": "provide either your username or password to log in",
                "status": Status.invalid_data
            }), Status.invalid_data
        elif not password:
            response = jsonify({
                "error": "Provide your password",
                "status": Status.invalid_data
            }), Status.invalid_data
        elif username:
            from api.app.models.models import User
            user = User.query_by_field("username", username)
            if not user:
                response = jsonify({
                    "error": "The username does not exist, plase sign up",
                    "status": Status.denied_access
                }), Status.denied_access
            else:
                user = user[0]
                if bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
                    token = create_access_token(identity=user.email)
                    response = jsonify({
                        "message": "You have successfully logged into Questioner",
                        "data":[{
                            "token":token,
                            "user":user.to_dictionary()
                        }],
                        "status": Status.success
                    }), Status.success
                else:
                    response = jsonify({
                        "error": "Invalid password",
                        "status": Status.denied_access
                    }), Status.denied_access
        else:
            from api.app.models.models import User
            user = User.query_by_field("email", email)
            if not user:
                response = jsonify({
                    "error": "A user with that mail does not exist, plase sign up",
                    "status": Status.denied_access
                }), Status.denied_access
            else:
                user = user[0]
                if bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
                    token = create_access_token(identity=user.email)
                    response = jsonify({
                        "message": "You have successfully logged into Questioner",
                         "data":[{
                            "token":token,
                            "user":user.to_dictionary()
                        }],
                        "status": Status.success
                    }), Status.success
                else:
                    response = jsonify({
                        "error": "Invalid password",
                        "status": Status.denied_access
                    }), Status.denied_access
    else:
        response = jsonify({
            "error": "The data needs to be in JSON",
            "status": Status.not_json
        }), Status.not_json
    return response
