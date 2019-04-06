from flask_restful import Resource, request, fields, marshal
from app.db import db, CourseModel, TeachModel
from app.resource import message


class CourseResource(Resource):   
    def post(self):
        # tenta procurar por dados anteriores do ministrante
        teach = TeachModel.query.filter_by(cpf=request.json['cpf']).first()
        # realiza o registro caso não encontre nada relacionado
        if not teach:
            teach = TeachModel(
                nome = request.json['nome'],
                resumo = request.json['resumo'],
                rg = request.json['rg'],
                cpf = request.json['cpf'],
                facebook = request.json['facebook'] or '',
                twitter = request.json['twitter'] or '',
                instagram = request.json['instagram'] or '',
                site = request.json['site'] or ''
            )
            teach.set_gravatar(request.json['gravatar'])
            teach.set_created_data()

            db.session.add(teach)
        # atualiza as informações do ministrante ja cadastrados.
        else:
            teach.nome = request.json['nome']
            teach.resumo = request.json['resumo']
            teach.rg = request.json['rg']
            teach.cpf = request.json['cpf']
            teach.facebook = request.json['facebook'] or ''
            teach.twitter = request.json['twitter'] or ''
            teach.instagram = request.json['instagram'] or ''
            teach.site = request.json['site'] or ''
            teach.set_gravatar(request.json['gravatar'])

        # realiza a criação do minicurso
        course = CourseModel(
            titulo = request.json['titulo'],
            conteudo = request.json['conteudo'],
            ministrante = request.json['cpf']
        )
        course.set_created_data()
        db.session.add(course)
        # persiste as alterações e pendencias no banco de dados
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao cadastrar o minicurso!'}, message), 422
        return marshal({'message':'Minicurso cadastrado com sucesso.'}, message), 201