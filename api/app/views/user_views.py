from .import user_view
from flask import request, jsonify
from api.app.utils.validators import UserValidators
from .import Status
import bcrypt


@user_view.route("/sign-up", methods=["POST"])
def sign_up():
    """A post endpoint for creating a user account"""
    from api.app.models.models import User
    response = None
    if request.is_json:
        data = request.json
        valid, errors = UserValidators.is_valid(data)
        if not valid:
            response = jsonify({
                "message": "You encountered {} errors".format(len(errors)),
                "status": Status.invalid_data
            }), Status.invalid_data
        elif User.query_by_field("email", data.get("email")):
            response = jsonify({
                "message": "The email address has already been taken",
                "status": Status.invalid_data
            }), Status.invalid_data
        elif User.query_by_field("username",data.get("username")):
            response=jsonify({
                "message":"The username has already been taken",
                "status":Status.invalid_data
            }),Status.invalid_data
        else:
            other_name = ""
            if data.get("othername"):
                other_name = data.get("othername")
            first_name = data.get("firstname")
            last_name = data.get("lastname")
            email = data.get("email")
            phone_number = data.get("phoneNumber")
            user_name = data.get("username")
            password = bcrypt.hashpw(data.get("password").encode(
                'utf8'), bcrypt.gensalt()).decode('utf8')
            user = User(first_name=first_name, last_name=last_name,
                        other_name=other_name, email=email, phone_number=phone_number, user_name=user_name, password=password)
            user.save()
            response = jsonify({
                "message": "Successuflly signed up",
                "status": Status.created,
                "data": [user.to_dictionary()]
            }), Status.created
    else:
        response = jsonify({
            "message": "The data needs to be in JSON",
            "status": Status.not_json
        }), Status.not_json
    return response