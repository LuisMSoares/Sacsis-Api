from os import environ
from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.db import db, UserModel


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

from app.resource import UserResource, LoginResource, UserAdminResource

api.add_resource(UserResource, '/user', '/user/<int:user_id>')
api.add_resource(UserAdminResource, '/user/all')
api.add_resource(LoginResource, '/login')


with app.app_context():
    # remove this in production
    #db.drop_all()
    #print(' * Drop all tables!')
    db.create_all()
    
    #Master Administrator Registration
    user = UserModel.query.filter_by(nome='Administrador Mestre').first()
    if not user:
        user = UserModel(nome='Administrador Mestre',
                         matricula='0000',
                         cpf='00000000000',
                         rg='00000000000',
                         admin=True
        )
    user.email=environ.get('MASTER_ADM_LOGIN','admin')
    user.hash_password(environ.get('MASTER_ADM_PASSWORD','admin'))
    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()