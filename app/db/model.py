from app.db import db
from passlib.apps import custom_app_context as pwd_context


class UserModel(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    matricula = db.Column(db.String(10), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    rg = db.Column(db.String(15), nullable=False)
    senha = db.Column(db.String, nullable=False)

    def hash_password(self, password):
        self.password = pwd_context.encrypt(password)


    def verify_password(self, password):
        # return True or False
        return pwd_context.verify(password, self.password)