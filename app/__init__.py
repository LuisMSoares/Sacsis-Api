from os import environ
from flask import Flask, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from app.db import db, UserModel


app = Flask(__name__)


# ORM Configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
# JSON Web Token Configuration
app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY','This is a secret key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
# Email Server Configuration
app.config['MAIL_SERVER']=environ.get('MAIL_SERVER','smtp.gmail.com')
app.config['MAIL_PORT'] = environ.get('MAIL_PORT',465)
app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME','shinodu.dev@gmail.com')
app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD','passatempodev23')
app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER','shinodu.dev@gmail.com')
app.config['MAIL_USE_TLS'] = environ.get('MAIL_USE_TLS',False)
app.config['MAIL_USE_SSL'] = environ.get('MAIL_USE_SSL',True)

# Cross Origin Resource Sharing
CORS(app)
# Database init
db.init_app(app)
# JWT init
jwt = JWTManager(app)
# Mail init
mail = Mail(app)
# Api init
api = Api(app)
api.prefix = '/api'


@app.errorhandler(404)
def not_found(error):
    return jsonify({'Error': 'Route not found'}), 404


# Resources app registration
from app.resource import (UserResource, LoginResource, 
UserAdminResource, CoursesResource, ResetPasswordResource)

api.add_resource(CoursesResource, '/admin/course', '/admin/course/<int:course_id>')
api.add_resource(UserAdminResource, '/admin/user', '/admin/user/<int:user_id>')

api.add_resource(UserResource, '/user')
api.add_resource(LoginResource, '/login')
api.add_resource(ResetPasswordResource, '/reset_password')



with app.app_context():
    try:
        # remove this in production
        #db.drop_all()
        #print(' * Drop all tables!')

        db.create_all()
    except:
        ...
    #Master Administrator Registration
    user = UserModel.query.filter_by(nome='Administrador Mestre').first()
    if not user:
        user = UserModel(
            nome='Administrador Mestre',
            matricula='0', cpf='0', rg='0',
            camiseta='0', admin=True
        )
    user.email = environ.get('MASTER_ADM_LOGIN','admin')
    user.hash_password( environ.get('MASTER_ADM_PASSWORD','admin') )
    try:
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
