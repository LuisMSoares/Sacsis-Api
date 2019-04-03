from app.db import db
from passlib.apps import custom_app_context as pwd_context
from passlib import pwd
from datetime import datetime
from random import randint


class UserModel(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    matricula = db.Column(db.String(10), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    rg = db.Column(db.String(15), nullable=False)
    camiseta = db.Column(db.String(25), nullable=False)
    senha = db.Column(db.String, nullable=False)
    senha_reset = db.Column(db.String)

    ativo = db.Column(db.Boolean, default=False)
    status_pago = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)


    def hash_reset_password(self):
        temp_pass = pwd.genword(entropy=86)
        self.senha_reset = pwd_context.encrypt(temp_pass)
        return temp_pass

    def hash_password(self, senha):
        self.senha = pwd_context.encrypt(senha)
        self.senha_reset = ''

    def verify_password(self, senha):
        return pwd_context.verify(senha, self.senha)


class CoursesModel(db.Model):
    __tablename__ = 'minicursos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.String, nullable=False)
    data_inicio = db.Column(db.DateTime)#, nullable=False)
    data_fim = db.Column(db.DateTime)#, nullable=False)
    vagas = db.Column(db.Integer, default=0)

    ministrante_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    ministrante = db.relationship('UserModel', backref='ministrante')

    #date format '2019-03-29 15:50'
    def inserir_datas(self, data_inicio, data_fim):
        self.data_inicio = datetime.strptime(str(data_inicio),"%Y-%m-%d %H:%M:%S")
        self.data_fim = datetime.strptime(str(data_fim),"%Y-%m-%d %H:%M:%S")
