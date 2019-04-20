from flask_restful import Resource, request, fields, marshal
from app.db import db, LectureModel, CourseModel, ScheduleModel
from app.resource import message, admin_required
from datetime import datetime


class ScheduleAdminResource(Resource):
    @admin_required
    def post(self):
        formtype = request.args.get('formtype', None)
        if not formtype:
            return marshal({'message':'Tipo de formulario não econtrado!'}, message), 404
        schedule = ScheduleModel(
            local = request.json['local'],
            dia = request.json['dia'],
            data_inicio = datetime.now().isoformat(), #request.json['data_inicio'],
            data_fim = datetime.now().isoformat() #request.json['data_fim'],
        )
        if formtype == 'course':
            course = CourseModel.query.filter_by(id=request.json['course_id']).first()
            if not course:
                return marshal({'message':'Minicurso não encontrado!'}, message), 404
            schedule.setCourse(
                vagas = request.json['vagas'],
                turma = request.json['turma'],
                course = course
            )
        elif formtype == 'lecture':
            lecture = LectureModel.query.filter_by(id=request.json['lecture_id']).first()
            if not lecture:
                return marshal({'message':'Palestra não encontrada!'}, message), 404
            schedule.setLecture(
                lecture = lecture
            )
        elif formtype == 'other':
            schedule.setOther(
                titulo = request.json['titulo'],
                descricao = request.json['descricao']
            )
        try:
            db.session.add(schedule)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao cadastrar a programação!'}, message), 422
        else:
            return {'message':'Programação cadastrada com sucesso!'}, 201
    

