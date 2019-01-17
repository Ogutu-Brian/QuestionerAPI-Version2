from .import meetup_view
from flask import request, jsonify
from api.app.views import Status
from api.app.utils.validators import MeetupValidators
from flask_jwt_extended import jwt_required

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
                "status": Status.invalid_data
            }), Status.invalid_data
        else:
            from api.app.models.models import Meetup
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
            "message": "The data should be JSON",
            "status": Status.not_json
        }), Status.not_json
    return response
