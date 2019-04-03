from flask_jwt_extended import create_access_token
from flask_restful import Resource, request, marshal, fields
from app.db import db, UserModel
from app.services import SendEmail
from app.resource import message


class ResetPasswordResource(Resource):
    def post(self):
        user = UserModel.query.filter_by(email=request.json['login']).first()
        if not user:
            return marshal({'message':'Login para o usuario não encontrado'}, message), 401
        tpass, email = user.hash_reset_password(), user.email
        SendEmail.reset_password('SACSIS XI - Redefinição de senha', email, tpass)
        return marshal({'message':'Senha temporaria enviada por email.'}, message), 200

    @jwt_required
    def put(self):
        user = UserModel.query.filter_by(id=get_jwt_identity()).first()
        user.hash_password(request.json['senha'])
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal({'message':'Senha principal alterada com sucesso'}, message), 201