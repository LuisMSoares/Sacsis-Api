from flask_jwt_extended import create_access_token, get_jwt_identity
from flask_restful import Resource, request, marshal, fields
from app.db import UserModel
from app.resource import message, jwt_token_required_custom

user_field = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String,
    'matricula': fields.String,
    'cpf': fields.String,
    'rg': fields.String,
    'status_pago': fields.Boolean,
    'camiseta': fields.String
}


class LoginResource(Resource):
    def post(self):
        reset_user = False
        user = UserModel.query.filter_by(email=request.json['login']).first()
        if not user:
            return marshal({'message':'Login para o usuario não encontrado'}, message), 401
        # Bloqueia o acesso caso a conta não tenha sido confirmada
        if not user.ativo:
            return marshal({'message':'Cadastro não confirmado.'}, message), 403
        if not user.verify_password(request.json['senha']):
            # Verifica se existe uma
            reset_user = user.senha_temporaria
            if reset_user:
                if reset_user.verify_password(request.json['senha']):
                    reset_user = True
                else:
                    reset_user = False
            else:
                return marshal({'message':'Senha informada incorreta'}, message), 401
        jwt_token = create_access_token(identity=user.id)
        data = {'jwt_token':jwt_token, 'dados': marshal(user, user_field)}
        if user.admin:
            data['admin'] = True
        if reset_user:
            data['rsenha'] = True
        return data, 200

    #token refresh
    @jwt_token_required_custom
    def put(self):
        user_id = get_jwt_identity()
        jwt_token = create_access_token(identity=user_id)
        data = {'jwt_token':jwt_token}
        return data, 200


