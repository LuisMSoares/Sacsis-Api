from flask_jwt_extended import get_jwt_identity
from app.resource import message, jwt_token_required_custom
from flask_restful import Resource, request, marshal, fields
from flask import url_for, current_app
from app.db import db, UserModel
from app.services import SendEmail
from threading import Thread

user_field = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'matricula': fields.String,
    'cpf': fields.String,
    'rg': fields.String,
    'sexo': fields.String,
    'status_pago': fields.Boolean,
    'camiseta': fields.String
}


class UserResource(Resource):
    @jwt_token_required_custom
    def get(self):
        user = UserModel.query.filter_by(id=get_jwt_identity()).first()
        if not user:
            return marshal({'message':'Usuário não encontrado'}, message), 404
        return marshal(user, user_field)
        
    def post(self):
        user = UserModel(
            nome=request.json['nome'],
            email=request.json['email'],
            matricula=request.json['matricula'],
            cpf=request.json['cpf'],
            rg=request.json['rg'],
            camiseta=request.json['camiseta']
        )
        if request.json['sexo'] <= 0:
            user.sexo='Masculino'
        else:
            user.sexo='Feminino'
        user.hash_password(request.json['senha'])
        user.activate_account() # comment this in production
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Endereço de email já cadastrado'}, message), 422
        else:
            # Envia um email com um link de confirmação de cadastro.
            # link = url_for('activate_account', token='token', _external=True)
            # mail_app = current_app._get_current_object()
            # Thread(target=SendEmail.user_confirm, args=[
            #    mail_app,'SACSIS - Confirmação de cadastro', user.email, link
            # ]).start()
            return marshal({'message':'Usuário cadastrado'}, message), 201

    @jwt_token_required_custom
    def put(self):
        user = UserModel.query.filter_by(id=get_jwt_identity()).first()
        if not user:
            return marshal({'message':'Usuário inexistente'}, message), 404
        if 'nome' in request.json:
            user.nome = request.json['nome']
        if 'cpf' in request.json:
            user.cpf = request.json['cpf']
        if 'rg' in request.json:
            user.rg = request.json['rg']
        if 'matricula' in request.json:
            user.matricula = request.json['matricula']
        if 'camiseta' in request.json:
            user.camiseta = request.json['camiseta']
        if 'sexo' in request.json:
            user.sexo = request.json['sexo']
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(user, user_field)