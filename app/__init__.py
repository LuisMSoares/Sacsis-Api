from os import environ
from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.db import db


app = Flask(__name__)
api = Api(app)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
db.init_app(app)

app.config['JWT_SECRET_KEY'] = environ['JWT_KEY']
#app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)


@app.errorhandler(404)
def not_found(error):
    return jsonify({'Error': 'Route not found'}), 404




import views, models, resources