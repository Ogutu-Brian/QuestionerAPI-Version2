from .import meetup_view
from flask import request, jsonify
from .import Status
from api.app.utils.validators import MeetupValidators
from flask_jwt_extended import jwt_required, get_jwt_identity


@meetup_view.route("/meetups", methods=["POST"])
@jwt_required
def create_meetup():
    """A post endpoint for creating a meetup by an administrator"""
    response = None
    if request.is_json:
        data = request.json
        valid, errors = MeetupValidators.is_valid(data)
        if not valid:
            response = jsonify({
                "message": "You encountered {} errors".format(len(errors)),
                "error": errors,
                "status": Status.invalid_data
            }), Status.invalid_data
        else:
            from api.app.models.models import Meetup
            from api.app.models.models import User
            user_mail = get_jwt_identity()
            user = User.query_by_field("email", user_mail)[0]
            if not user.is_admin.lower() == "true":
                response = jsonify({
                    "error": "You are not an admin",
                    "status": Status.denied_access
                }), Status.denied_access
            else:
                location = data.get("location")
                images = data.get("images")
                topic = data.get("topic")
                happening_on = data.get("happeningOn")
                tags = data.get("Tags")
                meetup = Meetup(location=location, images=images,
                                topic=topic, happening_on=happening_on, tags=tags)
                meetup.save()
                response = jsonify({
                    "message": "Successfully created a meetup",
                    "data": [meetup.to_dictionary()],
                    "status": Status.created
                }), Status.created
    else:
        response = jsonify({
            "error": "The data should be JSON",
            "status": Status.not_json
        }), Status.not_json
    return response


@meetup_view.route('/meetups/<meetup_id>', methods=["GET"])
@jwt_required
def get_meetup(meetup_id):
    """ A get endpoint for getting a specific meetup given an id"""
    from api.app.models.models import Meetup
    meetup = Meetup.query_by_field("id", int(meetup_id))
    response = None
    if not meetup:
        response = jsonify({
            "error": "A meetup with that id does not exist",
            "status": Status.not_found
        }), Status.not_found
    else:
        meetup = meetup[0]
        response = jsonify({
            "message": "A meetup was successfully found",
            "data": [meetup.to_dictionary()],
            "status": Status.success
        }), Status.success
    return response


@meetup_view.route("/meetups/upcoming/", methods=["GET"])
@jwt_required
def get_upcoming_meetups():
    """A GET endpoint for getting all the upcoming meetups"""
    from api.app.models.models import Meetup
    response = None
    meetups = Meetup.query_all()
    if not meetups:
        response = jsonify({
            "error": "There are no meetups in the record",
            "status": Status.success
        }), Status.success
    else:
        result_set = []
        for meetup in meetups:
            result_set.append(meetup.to_dictionary())
        response = jsonify({
            "mesage": "Successfullyy got all upcoming meetups",
            "data": result_set,
            "status": Status.success
        }), Status.success
    return response


@meetup_view.route("/meetups/<meetup_id>", methods=["DELETE"])
@jwt_required
def delete_meetup(meetup_id):
    """A delete endpoint for deleting meetups"""
    from api.app.models.models import Meetup, User
    meetup = Meetup.query_by_field("id", int(meetup_id))
    response = None
    if not meetup:
        response = jsonify({
            "error": "A meetup with that id does not exist",
            "status": Status.not_found,
        }), Status.not_found
    else:
        user_mail = get_jwt_identity()
        user = User.query_by_field("email", user_mail)[0]
        if not user.is_admin.lower() == "true":
            response = jsonify({
                "error": "You are not an admin",
                "status": Status.denied_access
            }), Status.denied_access
        else:
            meetup = meetup[0]
            meetup.delete()
            response = jsonify({
                "data": ["Successfully deleted the meetup"],
                "status": Status.success
            }), Status.success
    return response
