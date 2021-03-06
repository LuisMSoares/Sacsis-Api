from flask_restful import Resource, marshal, fields, request
from app.db import db, UserModel
from app.resource import message, admin_required
from os import environ

user_admin_field = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'matricula': fields.String,
    'cpf': fields.String,
    'rg': fields.String,
    'sexo': fields.String,
    'status_pago': fields.Boolean,
    'camiseta': fields.String,
    'admin': fields.Boolean
}
user_onlyname_field = {
    'id': fields.Integer,
    'matricula': fields.String,
    'nome': fields.String
}


class UserAdminResource(Resource):
    @admin_required
    def get(self, user_id=None):
        if user_id:
            user = UserModel.query.filter_by(id=user_id).first()
            if not user:
                return marshal({'message':'Usuário não encontrado'}, message), 404
            return marshal(user, user_admin_field)
        else:
            adm_filter = request.args.get('onlyadm', 0)
            loadname = request.args.get('loadname', 0)
            if int(adm_filter) == 1:
                user = UserModel.query.filter_by(admin=adm_filter).order_by(UserModel.id).all()
            else:
                user = UserModel.query.order_by(UserModel.id).all()
            admin_login = environ.get('MASTER_ADM_LOGIN','admin@admin.br')
            users = [marshal(u, user_admin_field) for u in user if u.email != admin_login]
            if len(users) == 0:
                return marshal({'message':'Nenhum usuário encontrado'}, message), 404
            if int(loadname) == 1:
                return marshal(users, user_onlyname_field), 200
            else:
                return {
                    'quantidade': len(users),
                    'usuarios': users
                }, 200

    @admin_required
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
        if 'admin' in request.json:
            user.admin = request.json['admin']
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
            return marshal(user, user_admin_field)

    @admin_required
    def delete(self, user_id=None):
        if not user_id:
            return marshal({'message':'Informe o id do usuário'}, message), 404
        user = UserModel.query.filter_by(id=user_id).first()
        if not user:
            return marshal({'message':'Usuário não encontrado'}, message), 404
        try:
            db.session.delete(user)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(user, user_admin_field), 201