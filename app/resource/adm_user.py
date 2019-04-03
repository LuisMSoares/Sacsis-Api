from flask_jwt_extended import ( jwt_required, get_jwt_identity )
from flask_restful import Resource, marshal, fields, request
from app.db import db, UserModel
from os import environ
from app.resource import message, admin_required

user_admin_field = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'matricula': fields.String,
    'cpf': fields.String,
    'rg': fields.String,
    'status_pago': fields.Boolean,
    'camiseta': fields.String,
    'admin': fields.Boolean
}
user_admin_list_fields = {
    'quantidade': fields.Integer,
    'usuarios': fields.List(fields.Nested(user_admin_field)),
}


class UserAdminResource(Resource):
    @admin_required
    def get(self, user_id=None):
        if user_id:
            user = UserModel.query.filter_by(id=user_id).first()
            if not user:
                return marshal({'message':'Usuário não encontrado'}, message), 404
            return marshal(user, user_admin_list_fields)
        else:
            adm_filter = request.args.get('onlyadm', None)
            if adm_filter != None:
                user = UserModel.query.filter_by(admin=adm_filter).order_by(UserModel.id).all()
            else:
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
        if 'status_pago' in request.json:
            user.status_pago = request.json['status_pago']
        if 'admin' in request.json:
            user.admin = request.json['admin']
        if 'camiseta' in request.json:
            user.matricula = request.json['camiseta']
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
        try:
            db.session.delete(user)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(user, user_admin_field)