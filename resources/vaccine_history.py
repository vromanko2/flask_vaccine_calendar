from flask import request, abort
from flask_restful import Resource
from models import *
from flask_restful_swagger import swagger


class Vaccinehistory(Resource):
    @swagger.operation(
        notes='get a vaccine history by user ID',
        responseClass=History.__name__,
        nickname='get'
    )
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            history = {}
            print("Hello")
            for element in user.vaccinesHistory:
                history[element.date] = element.vaccine
            return ({'User_history': history}), 201
        else:
            return "There's no such a user, try again!", 400

    @swagger.operation(
        notes='Create a vaccine history by user ID',
        nickname='post',
        parameters=[
            {
                "name": "first_name",
                "description": "First name of patient",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "path"
            },
            {
                "name": "last_name",
                "description": "Last name of patient",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string',
                "paramType": "path"
            },
            {
                "name": "birthday_date",
                "description": "Birthday date of patient in a form Y-m-d",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string'
            },
            {
                "name": "age",
                "description": "Age of patient in a month",
                "required": False,
                "allowMultiple": False,
                "dataType": 'string'
            },
            {
                "name": "contraindications",
                "description": "Contraindications of patient",
                "required": False,
                "allowMultiple": True,
                "dataType": ContraindicationList.__name__
            },
            {
                "name": "vaccines_history",
                "description": "vaccines history of patient",
                "required": True,
                "allowMultiple": True,
                "dataType": HistoryList.__name__
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Vaccine history is created."
            },
            {
                "code": 405,
                "message": "Invalid input"
            }
        ]
    )
    def post(self, user_id):
        if not request.json or not 'vaccines_history' in request.json:
            abort(400)

        vaccines_history = []
        for element in request.json['vaccines_history']:
            vaccines_history.append(History(element['vaccine'], element['date']))
        user = User.query.get(user_id)
        if user:
            current_user = {}
            user.vaccinesHistory = vaccines_history
            db.session.commit()
            current_user['first_name'] = user.first_name
            current_user['last_name'] = user.last_name
            current_user['birthday_date'] = user.birthday_date
            return current_user, 201
        else:
            return "There's no such a user, try again!", 400
