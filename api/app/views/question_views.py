from .import question_view
from flask_jwt_extended import jwt_required
from flask import request, jsonify
from .import Status
from api.app.utils.validators import QuestionValidators
from typing import Tuple
from flask_jwt_extended import get_jwt_identity
from flasgger import swag_from


@question_view.route('/questions', methods=["POST"])
@jwt_required
@swag_from('docs/createquestion.yml')
def create_question()->Tuple:
    """A post endpoint for creating a question for a given meetup"""
    response = None
    if request.is_json:
        valid, errors = QuestionValidators.is_valid(request.json)
        if not valid:
            response = jsonify({
                "message": "You encountered {} errors".format(len(errors)),
                "error": errors,
                "status": Status.invalid_data
            }), Status.invalid_data
        else:
            from api.app.models.models import User
            data = request.json
            user_mail = get_jwt_identity()
            user = User.query_by_field("email", user_mail)
            meetup = data.get("meetup")
            title = data.get("title")
            body = data.get("body")
            from api.app.models.models import Meetup, Question
            if not Meetup.query_by_field("id", meetup):
                response = jsonify({
                    "error": "A meetup with that id does not exist",
                    "status": Status.invalid_data
                }), Status.invalid_data
            else:
                if Question.query_by_field("meetup",
                                           meetup) and Question.query_by_field(
                        "body", body) and Question.query_by_field("title", title):
                    response = jsonify({
                        "error": "That question has been asked before",
                        "status": Status.denied_access
                    }), Status.denied_access
                else:
                    question = Question(meet_up=meetup, title=title, body=body)
                    question.created_by = user[0].id
                    question.save()
                    response = jsonify({
                        "message": "Successfully created a question",
                        "data": [question.to_dictionary()],
                        "status": Status.created
                    }), Status.created
    else:
        response = jsonify({
            "error": "The data must be in JSON",
            "status": Status.not_json
        }), Status.not_json
    return response


@question_view.route('/questions/<question_id>/upvote', methods=["PATCH"])
@jwt_required
@swag_from('docs/vote.yml')
def upvote(question_id: str)->Tuple:
    """Increates a question's vote by 1"""
    from api.app.models.models import Question, User, Vote
    response = None
    question = Question.query_by_field("id", int(question_id))
    if not question:
        response = jsonify({
            "error": "A question with that id does not exist",
            "status": Status.not_found
        }), Status.not_found
    else:
        question = question[0]
        existing_vote = False
        user = User.query_by_field("email", get_jwt_identity())[0]
        for vote in Vote.query_all():
            if vote.question == question.id and vote.user == user.id:
                existing_vote = True
                if vote.value == -1:
                    vote.value = 1
                    question.votes += 1
                    question.upvotes += 1
                    question.downvotes -= 1
                    vote.update()
                    question.update()
                    response = jsonify({
                        "message": "successfully upvoted",
                        "status": Status.created,
                        "data": [question.to_dictionary()]
                    }), Status.created
                else:
                    response = jsonify({
                        "error": "You cannot upvote more than once",
                        "status": Status.denied_access
                    }), Status.denied_access
        if not existing_vote:
            vote = Vote(user=user.id, question=question.id, value=1)
            vote.save()
            question.votes += 1
            question.upvotes += 1
            question.update()
            response = jsonify({
                "message": "successfully upvoted",
                "status": Status.created,
                "data": [question.to_dictionary()]
            }), Status.created
    return response


@question_view.route("/questions/<question_id>/downvote", methods=["PATCH"])
@jwt_required
@swag_from('docs/vote.yml')
def downvote(question_id: str)->Tuple:
    """Downvotes question endpoint by decreamenting the number of votes"""
    from api.app.models.models import Question, User, Vote
    response = None
    question = Question.query_by_field("id", int(question_id))
    if not question:
        response = jsonify({
            "error": "A question with that id does not exist",
            "status": Status.not_found
        }), Status.not_found
    else:
        user = User.query_by_field("email", get_jwt_identity())[0]
        question = question[0]
        existing_vote = False
        for vote in Vote.query_all():
            if vote.user == user.id and vote.question == question.id:
                existing_vote = True
                if vote.value == 1:
                    vote.value = -1
                    question.votes -= 1
                    question.upvotes -= 1
                    question.downvotes += 1
                    vote.update()
                    question.update()
                    response = jsonify({
                        "message": "Successfully downvoted a question",
                        "status": Status.created,
                        "data": [question.to_dictionary()]
                    }), Status.created
                else:
                    response = jsonify({
                        "error": "You cannot downvote a question more than once",
                        "status": Status.denied_access
                    }), Status.denied_access
        if not existing_vote:
            vote = Vote(user=user.id, question=question.id, value=-1)
            vote.save()
            question.votes -= 1
            question.downvotes += 1
            question.update()
            response = jsonify({
                "message": "Successfully downvoted a question",
                "status": Status.created,
                "data": [question.to_dictionary()]
            }), Status.created
    return response


@question_view.route("questions/<question_id>", methods=["GET"])
@swag_from('docs/get_specific_question.yml')
def get_specific_question(question_id)->Tuple:
    """Gets a specific question"""
    from api.app.models.models import Question
    question_id = int(question_id)
    response = None
    question = Question.query_by_field("id", question_id)
    if not question:
        response = jsonify({
            "error": "A question with that id does not exist",
            "status": Status.not_found
        }), Status.not_found
    else:
        response = jsonify({
            "data": [question[0].to_dictionary()],
            "status": Status.success
        }), Status.success
    return response


@question_view.route("questions/<meetup_id>/", methods=["GET"])
@swag_from('docs/get_all_questions.yml')
def get_all_questions_for_meetup(meetup_id):
    """Gets all questions for a given meetup"""
    response = None
    from api.app.models.models import Question
    questions = Question.query_by_field("meetup", int(meetup_id))
    if not questions:
        response = jsonify({
            "error": "There are no questions in the daatabase",
            "status": Status.not_found
        }), Status.not_found
    else:
        response = jsonify({
            "data": sorted([question.to_dictionary() for question in questions],
                           key=lambda k: k['votes'], reverse=True),
            "status": Status.success
        }), Status.success
    return response
