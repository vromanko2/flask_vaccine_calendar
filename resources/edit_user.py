from flask import request, abort, jsonify
from flask_restful import Resource
from models import User, Contraindication, History, db, ContraindicationList, HistoryList
from flask_restful_swagger import swagger


class Edit_user(Resource):
    @swagger.operation(
        notes='get a user by ID',
        nickname='get',
    )
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            contraindications = []
            vaccines_history = []
            current_user = {}
            vaccine_ = {}
            for cont in user.contraindications:
                contraindications.append(cont.title)
            for vaccine in user.vaccinesHistory:
                vaccine_['vaccine'] = vaccine.vaccine
                vaccine_['date'] = vaccine.date
                vaccines_history.append(vaccine_)
                vaccine_ = {}
            current_user['first_name'] = user.first_name
            current_user['last_name'] = user.last_name
            current_user['birthday_date'] = user.birthday_date
            current_user['contraindications'] = contraindications
            current_user['vaccines_history'] = vaccines_history

            return {'User': current_user}, 201
        else:
            return "There's no such a user, try again!", 400

    @swagger.operation(
        notes='edit user by ID',
        nickname='put',
        parameters=[
            {
                "name": "contraindications",
                "description": "Contraindications of patient",
                "required": True,
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
                "message": "User is updated."
            },
            {
                "code": 405,
                "message": "Invalid input"
            }
        ]
    )
    def put(self, user_id):
        if not request.json or not 'contraindications' or not 'vaccines_history' in request.json:
            abort(400)
        contraindications = []
        vaccines_history = []
        for cont in request.json['contraindications']:
            contraindications.append(Contraindication(cont))
        for element in request.json['vaccines_history']:
            vaccines_history.append(History(element['vaccine'], element['date']))
        user = User.query.get(user_id)
        if user:
            user.contraindications = contraindications
            user.vaccinesHistory = vaccines_history
            db.session.commit()
            return 'User updated', 201
        else:
            return "There's no such a user, try again!", 400
