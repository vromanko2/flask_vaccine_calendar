from flask import request, abort, jsonify
from flask_restful import Resource
from models import User, Contraindication, History, db, ContraindicationList, HistoryList
from flask_restful_swagger import swagger


class Create_user(Resource):
    @swagger.operation(
        notes='Create a user',
        nickname='post',
        parameters=[
            {
                "name": "first_name",
                "description": "First name of patient",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string'
            },
            {
                "name": "last_name",
                "description": "Last name of patient",
                "required": True,
                "allowMultiple": False,
                "dataType": 'string'
            },
            {
                "name": "birthday_date",
                "description": "Birthday date of patient in a form Y-m-d",
                "required": True,
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
                "required": False,
                "allowMultiple": True,
                "dataType": HistoryList.__name__
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "User is created."
            },
            {
                "code": 405,
                "message": "Invalid input"
            }
        ]
    )
    def post(self):
        if not request.json or not 'birthday_date' or not 'contraindications' or not 'first_name' \
                or not 'last_name' in request.json:
            abort(400)
        contraindications = []
        vaccines_history = []
        for cont in request.json['contraindications']:
            contraindications.append(Contraindication(cont))
        for element in request.json['vaccines_history']:
            vaccines_history.append(History(element['vaccine'], element['date']))
        user = User(first_name=request.json['first_name'], last_name=request.json['last_name'],
                    birthday_date=request.json['birthday_date'], contraindications=contraindications,
                    vaccines_history=vaccines_history)
        db.session.add(user)
        db.session.commit()
        new_user_id = user.id
        return ({'User_id': new_user_id}), 201
