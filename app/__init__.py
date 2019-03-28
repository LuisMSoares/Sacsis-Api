from os import environ
from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.db import db


app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
db.init_app(app)

app.config['JWT_SECRET_KEY'] = environ['JWT_KEY']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'Error': 'Route not found'}), 404


api = Api(app)
api.prefix = '/api'

from app.resource import UserResource, LoginResource

api.add_resource(UserResource, '/user')
api.add_resource(LoginResource, '/login')


#remove this on heroku deploy
try:
    with app.app_context():
        # remove this in production
        #db.drop_all()
        #print(' * Drop all tables!')
        db.create_all()
except:
    db.session.rollback()