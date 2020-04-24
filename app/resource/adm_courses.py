from flask_restful import Resource, request, fields, marshal
from app.db import db, CourseModel
from app.resource import message, admin_required

course_field = {
    'id': fields.Integer,
    'titulo': fields.String,
    'conteudo': fields.String,
    'ministrante': fields.String(attribute=lambda obj: obj.speaker.nome)
}
remove_course_field = {
    'id': fields.Integer,
    'titulo': fields.String,
    'conteudo': fields.String,
    'ministrante_id': fields.Integer
}
load_title_field = {
    'id': fields.Integer,
    'titulo': fields.String,
    'ministrante': fields.String(attribute=lambda obj: obj.speaker.nome)
}


class CourseAdminResource(Resource):
    @admin_required
    def get(self, course_id=None):
        loadtitle = request.args.get('loadtitle', 0)
        if int(loadtitle) == 1:
            courses = CourseModel.query.order_by(CourseModel.id).all()
            courses = [marshal(l,load_title_field) for l in courses]
            return {'values': courses}, 200
        if course_id:
            course = CourseModel.query.filter_by(id=course_id).first()
            if not course:
                return marshal({'message':'Minicurso inexistente'}, message), 404
            return marshal(course, course_field)
        else:
            courses = CourseModel.query.order_by(CourseModel.id).all()
            if len(courses) == 0:
                return marshal({'message':'Nenhum minicurso cadastrado encontrado'}, message), 404
            format_courses = [marshal(c, course_field) for c in courses]
            return {'quantidade': len(format_courses),'minicursos': format_courses}, 200

    @admin_required
    def put(self):
        course = CourseModel.query.filter_by(id=request.json['id']).first()
        if not course:
            return marshal({'message':'Minicurso inexistente'}, message), 404
        if 'titulo' in request.json:
            course.titulo = request.json['titulo']
        if 'conteudo' in request.json:
            course.conteudo = request.json['conteudo']
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(course, course_field)

    @admin_required
    def delete(self, course_id=None):
        if not course_id:
            return marshal({'message':'Informe o id do minicurso'}, message), 404
        course = CourseModel.query.filter_by(id=course_id).first()
        try:
            db.session.delete(course)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(course, remove_course_field), 201
