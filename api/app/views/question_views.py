from .import question_view
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from .import Status
from api.app.utils.validators import QuestionValidators


@question_view.route('/questions', methods=["POST"])
@jwt_required
def create_question():
    """A post endpoint for creating a question for a given meetup"""
    response = None
    if request.is_json:
        valid, errors = QuestionValidators.is_valid(request.json)
        if not valid:
            response = jsonify({
                "message": "You encountered {} errors".format(len(errors)),
                "data": errors,
                "status": Status.invalid_data,
            }), Status.invalid_data
        else:
            data = request.json
            created_by = data.get("createdBy")
            meetup = data.get("meetup")
            title = data.get("title")
            body = data.get("body")
            from api.app.models.models import User, Meetup, Question
            if not User.query_by_field("id", created_by):
                response = jsonify({
                    "error": "A user with that id does not exist",
                    "status": Status.invalid_data
                }), Status.invalid_data
            elif not Meetup.query_by_field("id", meetup):
                response = jsonify({
                    "error": "A meetup with that id does not exist",
                    "status": Status.invalid_data
                }), Status.invalid_data
            else:
                question = Question(created_by=created_by,
                                    meet_up=meetup, title=title, body=body)
                question.save()
                response = jsonify({
                    "message": "Successfully created a question",
                    "data": [question.to_dictionary()],
                    "status": Status.created
                }), Status.created
    else:
        response = jsonify({
            "error": "The data must be in JSOn",
            "status": Status.not_json
        }), Status.not_json
    return response


@question_view.route('/questions/<question_id>/upvote', methods=["PATCH"])
@jwt_required
def upvote(question_id):
    from api.app.models.models import Question
    """Increates a question's vote by 1"""
    response = None
    question = Question.query_by_field("id", int(question_id))
    if not question:
        response = jsonify({
            "error": "A question with that id does not exist",
            "status": Status.not_found
        }), Status.not_found
    else:
        question = question[0]
        question.votes += 1
        question.update()
        response = jsonify({
            "message": "successfully upvoted",
            "status": Status.created,
            "data": [question.to_dictionary()]
        }), Status.created
    return response
@question_view.route("/questions/<question_id>/downvote",methods=["PATCH"])
@jwt_required
def downvote(question_id):
    from api.app.models.models import Question
    response = None
    question = Question.query_by_field("id",int(question_id))
    if not question:
        response = jsonify({
            "error":"A question with that id does not exist",
            "status":Status.not_found
        }),Status.not_found
    else:
        question = question[0]
        question.votes-=1
        question.update()
        response = jsonify({
            "message":"Successfully downvoted a question",
            "status":Status.created
        }),Status.created
    return response