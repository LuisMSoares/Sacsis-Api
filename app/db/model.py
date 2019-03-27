from app.db import db
from passlib.apps import custom_app_context as pwd_context


class UserModel(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    matricula = db.Column(db.String(10), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    rg = db.Column(db.String(15), nullable=False)
    senha = db.Column(db.String, nullable=False)
    
    status_pago = db.Column(db.Boolean, default=False)

    admin = db.relationship('AdminModel', backref='user')
    

    def hash_password(self, senha):
        self.senha = pwd_context.encrypt(senha)


    def verify_password(self, senha):
        # return True or False
        return pwd_context.verify(senha, self.senha)


class AdminModel(db.Model):
    __tablename__ = 'administradores'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    activate = db.Column(db.Boolean, default=False)


class CoursesModel(db.Model):
    __tablename__ = 'minicursos'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String, nullable=False)
    slots = db.Column(db.Integer, default=0)
    start_datetime = db.Column(db.DateTime, nullable=False)
    finish_datetime = db.Column(db.DateTime, nullable=False)


class ShirtModel(db.Model):
    __tablename__ = 'camisetas'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    size = db.Column(db.String(20), nullable=False)


