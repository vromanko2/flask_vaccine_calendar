from flask_sqlalchemy import SQLAlchemy
from flask_restful_swagger import swagger
from flask_restful import fields

db = SQLAlchemy()

table_identifier = db.Table('table_identifier',
                            db.Column('table_id', db.Integer, db.ForeignKey('table.id')),
                            db.Column('data_id', db.Integer, db.ForeignKey('data.id'))
                            )
data_identifier = db.Table('data_identifier',
                           db.Column('data_id', db.Integer, db.ForeignKey('data.id')),
                           db.Column('vaccines_id', db.Integer, db.ForeignKey('vaccines.id'))
                           )
vaccines_identifier = db.Table('vaccines_identifier',
                               db.Column('vaccines_identifier', db.Integer, db.ForeignKey('vaccines.id')),
                               db.Column('contraindication_id', db.Integer, db.ForeignKey('contraindication.id'))
                               )
user_identifier = db.Table('user_identifier',
                           db.Column('user_identifier', db.Integer, db.ForeignKey('user.id')),
                           db.Column('contraindication_id', db.Integer, db.ForeignKey('contraindication.id')),
                           db.Column('history_id', db.Integer, db.ForeignKey('history.id'))
                           )


@swagger.model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    birthday_date = db.Column(db.String, nullable=False)
    contraindications = db.relationship('Contraindication', secondary=user_identifier, lazy='dynamic')
    vaccinesHistory = db.relationship('History', secondary=user_identifier)
    "A description of User model"
    def __init__(self, first_name, last_name, birthday_date, contraindications, vaccines_history):
        self.first_name = first_name
        self.last_name = last_name
        self.birthday_date = birthday_date
        self.contraindications = contraindications
        self.vaccinesHistory = vaccines_history

    def __repr__(self):
        return 'User : %r %r %r %r' % self.first_name % self.last_name % self.birthday_date % self.contraindications


@swagger.model
class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    data = db.relationship('Data', secondary=table_identifier, lazy='dynamic')

    def __init__(self, title, data):
        self.title = title
        self.data = data


@swagger.model
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age_in_months = db.Column(db.Integer, nullable=False)
    vaccines = db.relationship('Vaccines', secondary=data_identifier, lazy='dynamic')

    def __init__(self, age_in_months, vaccines):
        self.age_in_months = age_in_months
        self.vaccines = vaccines


@swagger.model
class Vaccines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    dose = db.Column(db.Integer)
    by_health = db.Column(db.Boolean)
    periodicity = db.Column(db.Integer, nullable=True)
    contraindications = db.relationship('Contraindication', secondary=vaccines_identifier, lazy='dynamic')

    def __init__(self, name, dose, contraindications, by_health, periodicity):
        self.name = name
        self.dose = dose
        self.contraindications = contraindications
        self.by_health = by_health
        self.periodicity = periodicity


@swagger.model
class Contraindication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=True)

    def __init__(self, title):
        self.title = title


@swagger.model
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vaccine = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)

    def __init__(self, vaccine, date):
        self.vaccine = vaccine
        self.date = date


@swagger.model
class ContraindicationList:
    resource_fields = {
        'contraindications': fields.List(fields.String)
    }


@swagger.model
@swagger.nested(vaccines_history=History.__name__)
class HistoryList:
    resource_fields = {
        'vaccines_history': fields.List(fields.Nested(History))
    }

