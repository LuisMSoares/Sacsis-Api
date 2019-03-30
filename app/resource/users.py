from flask_restful import Resource, request, marshal, fields
from app.db import db, UserModel
from app.resource import message

user_field = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'matricula': fields.String,
    'cpf': fields.String,
    'rg': fields.String,
    'status_pago': fields.Boolean
}


class UserResource(Resource):
    def post(self):
        user = UserModel(
            nome=request.json['nome'],
            email=request.json['email'],
            matricula=request.json['matricula'],
            cpf=request.json['cpf'],
            rg=request.json['rg']
        )
        user.hash_password(request.json['senha'])
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Endereço de email já cadastrado'}, message), 422
        else:
            return marshal({'message':'Usuário cadastrado'}, message), 201


    def put(self):
        user = UserModel.query.filter_by(id=request.json['id']).first()
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
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(user, user_field)


    def get(self, user_id):
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            return marshal({'message':'Usuário não encontrado'}, message), 404
        return marshal(user, user_field)