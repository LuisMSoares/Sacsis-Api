from app.db import db
from passlib.apps import custom_app_context as pwd_context
from passlib import pwd
from datetime import datetime
from sqlalchemy import or_


class UserModel(db.Model):
    """
    Modelo para armazenar os dados de todos os usuários cadastrados.
    """
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    matricula = db.Column(db.String(10), nullable=False)
    cpf = db.Column(db.String(11), nullable=False)
    rg = db.Column(db.String(15), nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    camiseta = db.Column(db.String(50), nullable=False)
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
    """
    Modelo para armazenar as senhas temporarias criadas pra permitir
    o acesso do usuário, esta senha e excluida quando a principal for
    redefinida apos o login.
    """
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
    """
    Modelo para armazenamento de todos os dados pessoais do ministrante
    """
    __tablename__ = 'ministrante'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    resumo = db.Column(db.String(250), nullable=False)
    rg = db.Column(db.String(20), nullable=False, unique=True)
    cpf = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    img_nome = db.Column(db.String, nullable=False)
    img_dados = db.Column(db.LargeBinary, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False)
    # redes sociais
    facebook = db.Column(db.String(50), default=None)
    twitter = db.Column(db.String(50), default=None)
    instagram = db.Column(db.String(50), default=None)
    site = db.Column(db.String(50), default=None)

    # Retorna uma lista com todas as palestras associadas ao ministrante
    lecture = db.relationship('LectureModel', passive_deletes=True)
    # Retorna uma lista com todos os minicursos associados ao ministrante
    course = db.relationship('CourseModel', passive_deletes=True)

    def occupation(self):
        """
        Retorna uma string informando se o ministrante possui ocupação de
        apenas minicurso, palestra ou ambos.
        """
        try:
            if len(self.lecture) != 0 and len(self.course) !=0:
                return 'Minicurso & Palestra'
            elif len(self.course) != 0:
                return 'Minicurso'
            elif len(self.lecture) !=0:
                return 'Palestra'
        except:
            ...
        return '-'

    def set_created_data(self):
        self.criado_em = datetime.now()

    def set_avatar(self, image_file, filename):
        self.img_nome = filename
        self.img_dados = image_file


class CourseModel(db.Model):
    """
    Modelo de armazenamento dos dados do minicurso cadastrado pelo ministrante
    """
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
    """
    Modelo de armazenamento dos dados da palestra cadastrada pelo ministrante
    """
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
    """
    Modelo que armazena uma lista negra de tokens já usados no acesso
    do formulario de cadastro do ministrante e sua palestra/minicurso 
    """
    __tablename__ = 'token_blacklist'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String, nullable=False)


class ScheduleModel(db.Model):
    """
    Modelo que armazena toda a programação do evento como: palestras,
    minicursos e outros eventos personalizados.
    """
    __tablename__ = 'programacao'

    id = db.Column(db.Integer, primary_key=True)
    local = db.Column(db.String(50), nullable=False)
    dia = db.Column(db.Integer, nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime, nullable=False)
    # Courses
    vagas = db.Column(db.Integer, default=None)
    turma = db.Column(db.String(20), default=None)
    course_id = db.Column(db.Integer, db.ForeignKey('minicurso.id'))
    # Lecture
    lecture_id = db.Column(db.Integer, db.ForeignKey('palestra.id'))
    # Other
    titulo = db.Column(db.String, default=None)
    descricao = db.Column(db.String, default=None)

    lecture = db.relationship('LectureModel', uselist=False)
    course = db.relationship('CourseModel', uselist=False)

    def vacRemaining(self):
        reserved = CourseSubsModel.query.filter(or_(
            CourseSubsModel.option1 == self.id,
            CourseSubsModel.option2 == self.id
        )).count()
        return self.vagas - reserved

    def setCourse(self, vagas, turma, course):
        self.vagas = vagas
        self.turma = turma
        self.course = course

    def setLecture(self, lecture):
        self.lecture = lecture

    def setOther(self, titulo, descricao):
        self.titulo = titulo
        self.descricao = descricao


class CourseSubsModel(db.Model):
    """
    Modelo de controle das incrições aos minicursos feitos pelo usuário
    após a confirmação do pagamento.
    """
    __tablename__ = 'usuarios_minicurso'

    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    option1 = db.Column(db.Integer, db.ForeignKey('programacao.id'))
    option2 = db.Column(db.Integer, db.ForeignKey('programacao.id'))

    user = db.relationship('UserModel', foreign_keys=[user_id])
    op1r = db.relationship('ScheduleModel', foreign_keys=[option1])
    op2r = db.relationship('ScheduleModel', foreign_keys=[option2])

    def __init__(self, user_id):
        self.user_id = user_id
        self.option1 = None
        self.option2 = None
    
    def setOption1(self, schedule_id):
        self.option1 = schedule_id

    def setOption2(self, schedule_id):
        self.option2 = schedule_id


class UserPaymentModel(db.Model):
    """
    Modelo para armazenar o pagamento realizado pelo usuário participante.
    """
    __tablename__ = 'pagamentos'

    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
    lote_id = db.Column(db.Integer, db.ForeignKey('lotes.id'))
    valor = db.Column(db.Float)
    data_pagamento = db.Column(db.DateTime, nullable=False)
    data_modificacao = db.Column(db.DateTime, nullable=False)
    admin_user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    
    user = db.relationship('UserModel',foreign_keys=[user_id], uselist=False)
    user_admin = db.relationship('UserModel',foreign_keys=[admin_user_id], uselist=False)

    def __init__(self, user_id, lote_id, valor, admin_user_id):
        self.user_id = user_id
        self.lote_id = lote_id
        self.valor = valor
        self.admin_user_id = admin_user_id
        date = datetime.now()
        self.data_pagamento = date
        self.data_modificacao = date


class LotModel(db.Model):
    """
    Modelo para armazenar todos os lotes cadastrados no sistema.
    """
    __tablename__ = 'lotes'

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    data_criacao = db.Column(db.DateTime, nullable=False)
    data_modificacao = db.Column(db.DateTime, nullable=False)
    admin_user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    user = db.relationship('UserModel', uselist=False)

    def __init__(self, valor, admin_user_id):
        self.valor = valor
        self.admin_user_id = admin_user_id
        date = datetime.now()
        self.data_criacao = date
        self.data_modificacao = date