from os import environ
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from app.db.model import *


def AdminMasterRegistration():
    pass