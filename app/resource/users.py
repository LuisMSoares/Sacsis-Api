from flask_restful import Resource, request, marshal
from app.db import db, UserModel
from app.resource import message


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

