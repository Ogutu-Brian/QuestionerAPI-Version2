from .import comment_view, Status
from typing import Tuple
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.app.utils.validators import CommentValidators
from flasgger import swag_from


@comment_view.route("/comments/", methods=["POST"])
@jwt_required
@swag_from('index.yml')
def create_comment()->Tuple:
    """Creates a comment to a Question"""
    response = None
    if request.is_json:
        data = request.json
        valid, errors = CommentValidators.is_valid(data)
        if valid:
            from api.app.models.models import Comment
            from api.app.models.models import Question
            from api.app.models.models import User
            question = Question.query_by_field("id", data.get("question"))
            if not question:
                response = jsonify({
                    "error": "A question with that id does not exist",
                    "status": Status.invalid_data
                }), Status.invalid_data
            else:
                question = question[0]
                user = User.query_by_field("email", get_jwt_identity())[0]
                comment = Comment(question=question.id, user=user.id, comment=data.get(
                    "comment"), title=question.title, body=question.body)
                comment.save()
                response = jsonify({
                    "data": comment.to_dictionary(),
                    "status": Status.created
                }), Status.created
        else:
            response = jsonify({
                "message": "You encoutered {} error(s)".format(len(errors)),
                "error": errors,
                "status": Status.invalid_data
            }), Status.invalid_data
    else:
        response = jsonify({
            "error": "Your data need to be in json format",
            "status": Status.not_json
        }), Status.not_json
    return response
