from app.db import db
from passlib.apps import custom_app_context as pwd_context
from passlib import pwd
from datetime import datetime
from hashlib import md5


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

    ativo = db.Column(db.Boolean, default=False)
    status_pago = db.Column(db.Boolean, default=False)
    admin = db.Column(db.Boolean, default=False)
    senha_temporaria = db.relationship('ResetPasswordModel', uselist=False)


    def hash_password(self, senha):
        self.senha = pwd_context.encrypt(senha)
        self.senha_reset = ''

    def verify_password(self, senha):
        return pwd_context.verify(senha, self.senha)

    def activate_account(self):
        self.ativo = True


class ResetPasswordModel(db.Model):
    __tablename__ = 'senha_opcional'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), unique=True)
    senha = db.Column(db.String, nullable=False)


    def generate_password(self):
        temp_pass = pwd.genword(entropy=64)
        self.senha = pwd_context.encrypt(temp_pass)
        return temp_pass

    def verify_password(self, senha):
        return pwd_context.verify(senha, self.senha)


class SpeakerModel(db.Model):
    __tablename__ = 'ministrante'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    resumo = db.Column(db.String(250), nullable=False)
    rg = db.Column(db.String(20), nullable=False, unique=True)
    cpf = db.Column(db.String(20), nullable=False, unique=True)
    img_nome = db.Column(db.String, nullable=False)
    img_dados = db.Column(db.LargeBinary, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False)
    # redes sociais
    facebook = db.Column(db.String(50), default=None)
    twitter = db.Column(db.String(50), default=None)
    instagram = db.Column(db.String(50), default=None)
    site = db.Column(db.String(50), default=None)


    lecture = db.relationship('LectureModel', passive_deletes=True)
    course = db.relationship('CourseModel', passive_deletes=True)

    def set_created_data(self):
        self.criado_em = datetime.now()

    def set_avatar(self, image_file):
        self.img_nome = image_file.filename
        self.img_dados = image_file.read()



class CourseModel(db.Model):
    __tablename__ = 'minicurso'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    conteudo = db.Column(db.String, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False)
    
    ministrante_id = db.Column(db.Integer,
        db.ForeignKey('ministrante.id', ondelete="CASCADE"))
    speaker = db.relationship('SpeakerModel', uselist=False)

    def set_created_data(self):
        self.criado_em = datetime.now()


class LectureModel(db.Model):
    __tablename__ = 'palestra'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    conteudo = db.Column(db.String, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False)
    
    ministrante_id = db.Column(db.Integer,
        db.ForeignKey('ministrante.id', ondelete="CASCADE"))
    speaker = db.relationship('SpeakerModel', uselist=False)

    def set_created_data(self):
        self.criado_em = datetime.now()


class TokenBlacklistModel(db.Model):
    __tablename__ = 'token_blacklist'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False)


class ImagesModel(db.Model):
    __tablename__ = 'imagens'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    dados = db.Column(db.LargeBinary, nullable=False)
