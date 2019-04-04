from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource, request, fields, marshal
from app.db import db, CoursesModel
from app.resource import message, admin_required

course_field = {
    'id': fields.Integer,
    'titulo': fields.String,
    'descricao': fields.String,
    'data_inicio': fields.DateTime(dt_format='iso8601'),
    'data_fim': fields.DateTime(dt_format='iso8601'),
    'vagas': fields.Integer,
    'ministrante_id': fields.Integer
}


class CoursesResource(Resource):
    @admin_required
    def post(self):
        course = CoursesModel(
            titulo=request.json['titulo'],
            descricao=request.json['descricao'],
            vagas=request.json['vagas'],
            ministrante_id=request.json['ministrante_id']
        )
        course.inserir_datas(request.json['data_inicio'], request.json['data_fim'])
        try:
            db.session.add(course)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao realizar o cadastro'}, message), 422
        else:
            return marshal({'message':'Minicurso cadastrado'}, message), 201


    @admin_required
    def put(self):
        course = CoursesModel.query.filter_by(id=request.json['id']).first()
        if not course:
            return marshal({'message':'Minicurso inexistente'}, message), 404
        if 'titulo' in request.json:
            course.titulo = request.json['titulo']
        if 'descricao' in request.json:
            course.descricao = request.json['descricao']
        if 'data_inicio' in request.json:
            course.start_datetime = request.json['data_inicio']
        if 'data_fim' in request.json:
            course.finish_datetime = request.json['data_fim']
        if 'vagas' in request.json:
            course.vagas = request.json['vagas']
        if 'ministrante_id' in request.json:
            course.ministrante_id = request.json['ministrante_id']
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(course, course_field)


    @admin_required
    def get(self, course_id=None):
        if course_id:
            course = CoursesModel.query.filter_by(id=course_id).first()
            if not course:
                return marshal({'message':'Minicurso inexistente'}, message), 404
            return marshal(course, course_field)
        else:
            courses = CoursesModel.query.order_by(CoursesModel.id).all()
            if len(courses) == 0:
                return marshal({'message':'Nenhum minicurso cadastrado encontrado'}, message), 404
            format_courses = [marshal(c, course_field) for c in courses]
            return {'quantidade': len(format_courses),'minicursos': format_courses}, 200


    @admin_required
    def delete(self, course_id=None):
        if not course_id:
            return marshal({'message':'Informe o id do minicurso'}, message), 404
        course = CoursesModel.query.filter_by(id=course_id).first()
        try:
            db.session.delete(course)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(course, course_field)
