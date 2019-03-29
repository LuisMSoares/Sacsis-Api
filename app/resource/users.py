from flask_restful import Resource, request, marshal, fields
from os import environ
from app.db import db, UserModel
from app.resource import message

user_field = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'matricula': fields.String,
    'cpf': fields.String,
    'rg': fields.String
}
user_admin_field = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'matricula': fields.String,
    'cpf': fields.String,
    'rg': fields.String,
    'status_pago': fields.Boolean,
    'admin': fields.Boolean
}
user_admin_list_fields = {
    'quantidade': fields.Integer,
    'usuarios': fields.List(fields.Nested(user_admin_field)),
}

class UserResource(Resource):
    def post(self):
        user = UserModel(nome=request.json['nome'],
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
            return marshal({'message':'Usuário cadastrado'}, message), 200


    def put(self):
        user = UserModel.query.filter_by(id=request.json['id']).first()
        if not user:
            return marshal({'message':'Usuário inexistente'}, message), 404
        if 'nome' in request.json:
            user.nome = request.json['nome']
        if 'cpf' in request.json:
            user.nome = request.json['cpf']
        if 'rg' in request.json:
            user.nome = request.json['rg']
        if 'matricula' in request.json:
            user.nome = request.json['matricula']
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
        


class UserAdminResource(Resource):
    def get(self):
        user = UserModel.query.order_by(UserModel.id).all()
        try:
            admin_login = environ.get('MASTER_ADM_LOGIN','admin')
            users = [marshal(u, user_admin_field) for u in user if u.email != admin_login]
            if len(users) == 0:
                return marshal({'message':'Nenhum usuário encontrado'}, message), 404
            return marshal({
                'quantidade': len(users),
                'usuarios': users
            }, user_admin_list_fields)
        except:
            return marshal({'message':'Erro interno'}, message), 500