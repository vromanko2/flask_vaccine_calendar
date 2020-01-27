from flask import Blueprint
from flask_restful import Api
from resources.calendar import Calendar
from resources.create_user import Create_user
from resources.edit_user import Edit_user
from resources.vaccine_history import Vaccinehistory
from flask_restful_swagger import swagger


api_bp = Blueprint('api', __name__)
api = swagger.docs(Api(api_bp), apiVersion='0.1')

# Routes
api.add_resource(Calendar, '/api/')
api.add_resource(Create_user, '/api/user')
api.add_resource(Edit_user, '/api/user/<int:user_id>/')
api.add_resource(Vaccinehistory, '/api/user/vaccine_history/<int:user_id>/')