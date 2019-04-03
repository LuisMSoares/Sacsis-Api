from flask_jwt_extended import create_access_token
from flask_restful import Resource, request, marshal, fields
from app.db import db, UserModel, ResetPasswordModel
from app.services import SendEmail
from app.resource import message


class ResetPasswordResource(Resource):
    def post(self):
        user = UserModel.query.filter_by(email=request.json['login']).first()
        if not user:
            return marshal({'message':'Login para o usuario não encontrado'}, message), 401
        reset_user = ResetPasswordModel.query.filter_by(usuario_id=user.id).first()
        try:
            if not user_user:
                tpass = reset_user.generate_password()
            else:
                reset_user = ResetPasswordModel(usuario_id=user.id)
                tpass = reset_user.generate_password()
                db.session.add(reset_user)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        SendEmail.reset_password('SACSIS XI - Redefinição de senha', user.email, tpass)
        return marshal({'message':'Senha temporaria enviada por email.'}, message), 200

    @jwt_required
    def put(self):
        reset_user = ResetPasswordModel.query.filter_by(usuario_id=user.id).first()
        user = UserModel.query.filter_by(id=get_jwt_identity()).first()
        user.hash_password(request.json['senha'])
        try:
            db.session.delete(reset_user)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal({'message':'Senha principal alterada com sucesso'}, message), 201