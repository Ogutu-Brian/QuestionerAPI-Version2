from .import meetup_view
from flask import request, jsonify
from api.app.views import Status
from api.app.models.object_models import Meetup

@meetup_view.route("/meetups", methods=["POST"])
def create_meetup():
    """A post endpoint for creating a meetup by an administrator"""
    response = None
    if request.is_json:
        valid, errors =  M
    else:
        response = jsonify({
            "message": "The data should be JSON",
            "status": Status.not_json
        }), Status.not_json
    return response
