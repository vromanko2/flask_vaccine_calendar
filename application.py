from flask import Flask, redirect, jsonify, request, make_response
from flask_cors import CORS
from app import api_bp
from models import db


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    app.config['SECRET_KEY'] = '####'

    CORS(app)

    app.register_blueprint(api_bp)

    db.init_app(app)

    app.debug = True
    return app


application = create_app("config")
if __name__ == "__main__":
    application.run('0.0.0.0')
