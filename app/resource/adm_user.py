from flask_restful import Resource, marshal, fields
from app.db import db, UserModel
from os import environ
from app.resource import message

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