from flask_restful import Resource, request, marshal
from app.db import db, UserModel
from app.resource import message


class UserResource(Resource):
    def post():
        user = UserModel(nome=request.json['nome'],
                         email=request.json['email'],
                         matricula=request.json['matricula'],
                         cpf=request.json['cpf'],
                         rg=request.json['rg'],
                         senha=hash_password(request.json['senha']))
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'úsuario cadastrado'}, message)
        