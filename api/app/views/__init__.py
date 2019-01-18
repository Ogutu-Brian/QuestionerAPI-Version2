from flask import Blueprint


class Status(object):
    """Defines my status codes"""
    not_json = 422
    created = 201
    invalid_data = 406
    success = 200
    not_found = 404
    no_content = 204
    method_not_allowed = 405
    denied_access = 401
    timeout = 408
    bad_requst = 400
    internal_server_error = 500


user_view = Blueprint('views.userviews', '__name__')
meetup_view = Blueprint('views.meetupviews', '__name__')
question_view = Blueprint('views.questionviews', '__name__')
