from os import environ
from datetime import timedelta
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_mail import Mail
from app.db import db


app = Flask(__name__)

# Handling excetions
app.config['PROPAGATE_EXCEPTIONS'] = True
# ORM Configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
# JSON Web Token Configuration
app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY','This is a secret key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=environ.get('JWT_EXPIRES_DAYS', 1))
# Email Server Configuration
app.config['MAIL_SERVER']=environ.get('MAIL_SERVER','smtp.gmail.com')
app.config['MAIL_PORT'] = environ.get('MAIL_PORT',465)
app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME','shinodu.dev@gmail.com')
app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD','passatempodev23')
app.config['MAIL_DEFAULT_SENDER'] = environ.get('MAIL_DEFAULT_SENDER','shinodu.dev@gmail.com')
app.config['MAIL_USE_TLS'] = environ.get('MAIL_USE_TLS',False)
app.config['MAIL_USE_SSL'] = environ.get('MAIL_USE_SSL',True)
app.confif['PREFERRED_URL_SCHEME'] = 'https'


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
# Admin api init
adm_api = Api(app)
adm_api.prefix = '/api/admin'

# Custom routes from application
from app.services.custom_routes import *

# Resources app registration
from app.resource import (UserResource, LoginResource, UserAdminResource,
SpeakerResource, ResetPasswordResource, SpeakerAdminResource, ScheduleResource,
CourseAdminResource, LectureAdminResource, ScheduleAdminResource, CourseScheduleResource,
LotAdminResource, PaymentAdminResource, ScheduleModalResource)

adm_api.add_resource(UserAdminResource, '/user', '/user/<int:user_id>')
adm_api.add_resource(SpeakerAdminResource, '/speaker', '/speaker/<int:speaker_id>')
adm_api.add_resource(CourseAdminResource, '/course', '/course/<int:course_id>')
adm_api.add_resource(LectureAdminResource, '/lecture', '/lecture/<int:lecture_id>')
adm_api.add_resource(ScheduleAdminResource, '/schedule', '/schedule/<int:schedule_id>')
adm_api.add_resource(LotAdminResource, '/payment/lot', '/payment/lot/<int:lot_id>')
adm_api.add_resource(PaymentAdminResource, '/payment', '/payment/<int:user_id>')

api.add_resource(UserResource, '/user')
api.add_resource(SpeakerResource, '/speaker', '/speaker/')
api.add_resource(ScheduleResource, '/schedule')
api.add_resource(ScheduleModalResource, '/schedule/info/<int:schedule_id>')
api.add_resource(CourseScheduleResource, '/schedule/course')

api.add_resource(LoginResource, '/login')
api.add_resource(ResetPasswordResource, '/reset_password')

# Database init tables
with app.app_context():
    try:
        # remove this in production
        # db.drop_all()
        # print(' * Drop all tables!')
        db.create_all()
    except:
        ...

# Master administrator registration
from app.services.adm_master import *