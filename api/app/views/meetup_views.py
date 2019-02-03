from .import meetup_view
from flask import request, jsonify
from .import Status
from api.app.utils.validators import (
    MeetupValidators, RsvpValidators, date_checker, valid_input_date)
from flask_jwt_extended import jwt_required, get_jwt_identity
from typing import Tuple
from flasgger import swag_from
from datetime import date


@meetup_view.route("/meetups", methods=["POST"])
@jwt_required
@swag_from("docs/createmeetup.yml")
def create_meetup()->Tuple:
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
            from api.app.models.models import Meetup, User
            user_mail = get_jwt_identity()
            user = User.query_by_field("email", user_mail)[0]
            if not user.is_admin.lower() == "true":
                response = jsonify({
                    "error": [{
                        "message": "You are not an admin"
                    }],
                    "status": Status.denied_access
                }), Status.denied_access
            else:
                location = data.get("location")
                images = data.get("images")
                topic = data.get("topic")
                happening_on = data.get("happeningOn")
                body = data.get("body")
                tags = data.get("Tags")
                if Meetup.query_by_field("location",
                                         location) and Meetup.query_by_field("topic", topic) and Meetup.query_by_field("happening_date",
                                                                                                                       happening_on):
                    response = jsonify({
                        "error": [{
                            "message": "Sorry that meetup already exists"
                        }],
                        "status": Status.denied_access
                    }), Status.denied_access
                else:
                    meetup = Meetup(location=location, images=images, body=body,
                                    topic=topic, happening_on=happening_on, tags=tags)
                    meetup.save()
                    response = jsonify({
                        "message": "Successfully created a meetup",
                        "data": [meetup.to_dictionary()],
                        "status": Status.created
                    }), Status.created
    else:
        response = jsonify({
            "error": [{
                "message": "The data should be JSON"
            }],
            "status": Status.not_json
        }), Status.not_json
    return response


@meetup_view.route('/meetups/<meetup_id>', methods=["GET"])
@swag_from('docs/getspecmeetup.yml')
def get_meetup(meetup_id: str)->Tuple:
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
@swag_from('docs/upcomingmeetup.yml')
def get_upcoming_meetups()->Tuple:
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
            if date_checker(meetup.happening_on):
                result_set.append(meetup.to_dictionary())
        response = jsonify({
            "mesage": "Successfully got all upcoming meetups",
            "data": result_set,
            "status": Status.success
        }), Status.success
    return response


@meetup_view.route("/meetups/<meetup_id>", methods=["DELETE"])
@jwt_required
@swag_from('docs/delmeetup.yml')
def delete_meetup(meetup_id: str)->Tuple:
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


@meetup_view.route("/meetups/<meetup_id>/rsvps", methods=["POST"])
@jwt_required
@swag_from('docs/rsvps.yml')
def create_rsvp(meetup_id: str)->Tuple:
    """Endpoint for creatong Rsvp"""
    from api.app.models.models import Meetup, Rsvp, User
    response = None
    if request.is_json:
        data = request.json
        valid, errors = RsvpValidators.is_valid(data)
        if not valid:
            response = jsonify({
                "error": "You encountered {} errors".format(len(errors)),
                "data": errors,
                "status": Status.invalid_data
            }), Status.invalid_data
        else:
            meetup = Meetup.query_by_field("id", int(meetup_id))
            if not meetup:
                response = jsonify({
                    "error": "A meetup with that id does not exist",
                    "status": Status.not_found
                }), Status.not_found
            else:
                meetup = meetup[0]
                if not date_checker(meetup.happening_on):
                    response = jsonify({
                        "error": "The meetup date has passed",
                        "status": Status.denied_access
                    }), Status.denied_access
                else:
                    update = False
                    similar = False
                    user = User.query_by_field("email", get_jwt_identity())[0]
                    rsvp = Rsvp(meetup=meetup.id, user=user.id,
                                response=data.get("response"))
                    for item in Rsvp.query_all():
                        if user.id == item.user and meetup.id == item.meetup:
                            if item.response == data.get("response"):
                                response = jsonify({
                                    "error": "You have already given that response",
                                    "status": Status.denied_access
                                }), Status.denied_access
                                similar = True
                            else:
                                item.response = data.get("response")
                                rsvp = item
                                update = True
                                rsvp.update()
                                response = jsonify({
                                    "message": "Successfully submitted your Rsvp",
                                    "status": Status.created,
                                    "data": [{
                                        "meetup": rsvp.meetup,
                                        "topic": meetup.to_dictionary().get("topic"),
                                        "status": rsvp.response
                                    }]
                                }), Status.created
                    if not update and not similar:
                        rsvp.save()
                        response = jsonify({
                            "message": "Successfully submitted your Rsvp",
                            "status": Status.created,
                            "data": [{
                                "meetup": rsvp.meetup,
                                "topic": meetup.to_dictionary().get("topic"),
                                "status": rsvp.response
                            }]
                        }), Status.created
    else:
        response = jsonify({
            "error": "The data needs to ne in JSON",
            "status": Status.not_json
        }), Status.not_json
    return response
