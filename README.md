# Questioner
Questioner API using Python Flask and PostgreSQL  
[![Build Status](https://travis-ci.com/Ogutu-Brian/QuestionerAPI-Version2.svg?branch=develop)](https://travis-ci.com/Ogutu-Brian/QuestionerAPI-Version2)
[![Coverage Status](https://coveralls.io/repos/github/Ogutu-Brian/QuestionerAPI-Version2/badge.svg?branch=develop)](https://coveralls.io/github/Ogutu-Brian/QuestionerAPI-Version2?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/8689fc6f2c1aae58a9f4/maintainability)](https://codeclimate.com/github/Ogutu-Brian/QuestionerAPI-Version2/maintainability)   
## Project Overview
Questioner is an application used by meetup organizers to plan well for meetups and to prioritize what to discuss during the meetup.

## Required Features
1. A user should be able to sign up to Questioner 
2. A user with an account should be able to log into Questioner
3. An administrator should be able to crete a meetup in Questioner
4. A user with an account should be able to post Questions to specific meetups
5. A user should be able to post a question agains a specific meetup
6. A user should be able to get a specific meetup record
7. A user should be able to get all meetup recods
8. A user should be able to upvote or downvote a question
9. A user should be able to give an rsvp for a meetup

# Installation and Setup
Clone the repository.
```bash
git https://github.com/Ogutu-Brian/QuestionerAPI-Version2
```

## Create a virtual environment

```bash
$ python3 -m venv venv;
$ source venv/bin/activate
```
On Windows
```bash
py -3 -m venv venv
```
If you need to install virtualenv because you are on an older version of Python:
```bash
virtualenv venv
```
On Windows
```bash
\Python27\Scripts\virtualenv.exe venv
```

## Activate the virtual environment
Before you begin you will need to activate the corresponding environment
```bash
source venv/bin/activate
```
On Windows
```bash
venv\Scripts\activate
```

## Install requirements
```bash
$ pip install -r requirements.txt
```

## Running the application
After the configuration, you will run the app 
```bash
$ cd api
$ export FLASK_APP=run.py
$ flask run
```

## Endpoints
All endpoints can be now accessed from the following url on your local computer
```
http://localhost:5000/api/v2/
``````

## Testing
After successfully installing the application, the endpoints can be tested by running.
```bash
pytest tests/*
```

## Available endpoints
| Method        |  Endpoint                                   |  Description                                           |
| ------------- |  -------------                              |  -------------                                         |
| `POST`        | `/api/v2/meetups`                           |  Creates a meetup record by admin                      |
| `GET`         | `/api/v2/meetups/<meetup-id>`               |  Fetch a specific meetup record                        |
| `GET`         | `/api/v2/meetups/upcomng/`                  |  Fetch all upcoming meetup records                     |
| `POST`        | `/api/v2/questions`                         |  Create a question for a specific meetup               |
| `PATCH`       | `/api/v2/questions/<question-id>/upvote`    |  Upvotes a specific question                           |
| `PATCH`       | `/api/v2/questions/<question-id>/downvote`  |  Downvotest a specific question                        |
| `POST`        | `/api/v2/meetups/<meetup-id>/rsvps`         |  Responds to a meetup Rsvp                             |
| `POST`        | `/api/v2/auth/signup`                       |  Creates a new user to Questioner                      | 
| `POST`        | `/api/v2/auth/login`                        |  Allows a user with an account to log in               |
| `DELETE`      | `/api/v2/meetups/<meetup-id>`               |  Allows an admin to delete a meetup                    |
| `POST`        | `/api/v2/comments/`                         |  Allows a user to make comments                        |
| `DELETE`      | `/api/v2/auth/logout`                       |  Allows a logged in user to logout                     |
| `GET`         | `/api/v2/comments/question-id`              |  Allows a user to get all comments for a questi        |
| `GET`         | `/api/v2/questions/`                        |  Gets all questions from questioner                    |
| `GET`         | `/api/v2/questions/question-id`             |  Gets a specific question from questione               |
      
# Resources and Documentation
1. [Swagger UI documentation](http://questioner-api-v2.herokuapp.com/apidocs/) 
2. [PostmanDocumentation](https://documenter.getpostman.com/view/5179699/RznLHcQ2)

### Pivotal Tracker Project
You can view the [Pivotal Tracker stories](https://www.pivotaltracker.com/n/projects/2235331)

### Research Materials   

1. [Flask](http://flask.pocoo.org/docs/1.0/)
