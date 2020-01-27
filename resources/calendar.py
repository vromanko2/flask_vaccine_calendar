from flask import jsonify, abort, request
from flask_restful import Resource
from models import *
import datetime
from collections import Counter
from flask_restful_swagger import swagger


required_vaccines_adult = ["АДП", "АДП", "АДП", "Гепатит В", "Гепатит В", "Гепатит В", "КПК", "КПК"]


def get_made_vaccines(in_set, vaccines_title):
    result_list = []
    for element in in_set:
        for vaccine in vaccines_title:
            if vaccine == element:
                result_list.append(vaccine)
    return result_list


def get_last_vaccine_period(vaccine_title):
    vac = Vaccines.query.filter_by(name=vaccine_title)[0]
    period = vac.periodicity
    return period


class Calendar(Resource):
    @swagger.operation(
        notes='Create a vaccine calendar',
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
                "required": False,
                "allowMultiple": True,
                "dataType": HistoryList.__name__
            }
        ],
        responseMessages=[
            {
                "code": 201,
                "message": "Calendar is created."
            },
            {
                "code": 405,
                "message": "Invalid input"
            }
        ]
    )
    def post(self):
        if not request.json or not 'age' or not 'is_alive' or not 'contraindications' in request.json:
            abort(400)

        good_data, vaccines, vaccines_age, calendar, calendar_aray = [], [], [], {}, []

        if request.json['is_alive']:
            if request.json['by_health']:
                data = Data.query.all()
                good_data = list(filter(lambda x: x.age_in_months <= int(request.json['age']), data))
                for data in good_data:
                    for vacine in data.vaccines:
                        if not (set(request.json['contraindications']) & set(
                                map(lambda x: x.title, vacine.contraindications))) and vacine.by_health:
                            i = 0
                            while i < int(request.json['age']) + 50:
                                key = (datetime.date.today() + datetime.timedelta(i * 365 /
                                                                                  12)).isoformat()
                                calendar.setdefault(key, [])
                                calendar[key].append(vacine.name)
                                i += int(vacine.periodicity)
            else:
                vaccines_title = []
                for element in request.json['vaccines_history']:
                    vaccines_title.append(element['vaccine'])
                if int(request.json['age']) >= 192:
                    set_result = set(vaccines_title) & set(required_vaccines_adult)
                    if not set_result:
                        i = 0
                        for vaccine in required_vaccines_adult:
                            vac = Vaccines.query.filter_by(name=vaccine)[0]
                            vaccines.append(vaccine)
                            calendar[(datetime.date.today() + datetime.timedelta(i * 365 / 12)).isoformat()] = vaccines
                            i += int(vac.periodicity)
                            vaccines = []
                    elif set_result:
                        i = 0
                        to_do = (Counter(required_vaccines_adult) - Counter(
                            get_made_vaccines(set_result, vaccines_title))).elements()
                        for vaccine in to_do:
                            vac = Vaccines.query.filter_by(name=vaccine)[0]
                            vaccines.append(vaccine)
                            calendar[(datetime.date.today() + datetime.timedelta(i * 365 / 12)).isoformat()] = vaccines
                            i += int(vac.periodicity)
                            vaccines = []
                    if not calendar:
                        start_date = datetime.date.today()
                    else:
                        selected_month_rec = list(calendar.keys())[-1]
                        start_date = datetime.date(int(selected_month_rec.split('-')[0]),
                                                   int(selected_month_rec.split('-')[1]),
                                                   int(selected_month_rec.split('-')[2]))
                        start_date = start_date + datetime.timedelta(
                            get_last_vaccine_period(calendar[selected_month_rec][0]) * 365 / 12)
                    data = Data.query.filter_by(age_in_months=192).first()
                    vaccines = list(map(lambda x: x.name, data.vaccines))
                    i = int(request.json['age'])
                    k = 0
                    while i <= 1200:
                        calendar[(start_date + datetime.timedelta(
                            k * 365 / 12)).isoformat()] = vaccines
                        i += 120
                        k += 120
                    return ({'Calendar': calendar}), 201
                else:
                    data_1 = Data.query.all()
                    required_vaccines_child = []
                    good_data_1 = list(filter(lambda x: x.age_in_months < int(request.json['age']), data_1))
                    for data in good_data_1:
                        for vaccine in data.vaccines:
                            if not vaccine.by_health:
                                required_vaccines_child.append(vaccine.name)
                    set_result = list(set(vaccines_title) & set(required_vaccines_child))
                    to_do = list((Counter(required_vaccines_child) - Counter(
                        get_made_vaccines(set_result, vaccines_title))).elements())

                    i = 0
                    for vaccine in to_do:
                        vac = Vaccines.query.filter_by(name=vaccine)[0]
                        vaccines.append(vaccine)
                        calendar[(datetime.date.today() + datetime.timedelta(i * 365 / 12)).isoformat()] = vaccines
                        i += int(vac.periodicity)
                        vaccines = []

                    if not calendar:
                        start_date = datetime.date.today()
                    else:
                        selected_month_rec = list(calendar.keys())[-1]
                        start_date = datetime.date(int(selected_month_rec.split('-')[0]),
                                                   int(selected_month_rec.split('-')[1]),
                                                   int(selected_month_rec.split('-')[2]))
                        start_date = start_date + datetime.timedelta(
                            get_last_vaccine_period(calendar[selected_month_rec][0]) * 365 / 12)

                    data = Data.query.all()
                    good_data = list(filter(lambda x: x.age_in_months >= int(request.json['age']), data))
                    for data in good_data:
                        for vacine in data.vaccines:
                            if not (set(request.json['contraindications']) & set(
                                    map(lambda x: x.title, vacine.contraindications))):
                                if not vacine.by_health:
                                    vaccines.append(vacine.name)
                                    calendar[(start_date + datetime.timedelta((data.age_in_months - int(
                                        request.json['age'])) * 365 / 12)).isoformat()] = vaccines
                        vaccines = []
            return ({'Calendar': calendar}), 201