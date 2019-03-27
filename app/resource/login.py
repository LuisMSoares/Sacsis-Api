from flask_jwt_extended import create_access_token
from flask_restful import Resource, request, marshal, fields
from app.db import db, UserModel
from app.resource import message

token = {
    'jwt_token':fields.String
}

class LoginResource(Resource):
    def post(self):
        user = UserModel.query.filter_by(email=request.json['login']).first()
        if not user:
            return marshal({'message':'Login para o usuario não encontrado'}, message), 401
        if not user.verify_password(request.json['senha']):
            return marshal({'message':'Senha informada incorreta'}, message), 401
        jwt_token = create_access_token(identity=user.id)
        return marshal({'jwt_token':jwt_token}, token), 200