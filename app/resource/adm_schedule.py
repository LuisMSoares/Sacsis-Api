from flask_restful import Resource, request, fields, marshal
from app.db import db, LectureModel, CourseModel, ScheduleModel, CourseSubsModel
from app.resource import message, admin_required
from app.services.excel import Excel
from datetime import datetime
from sqlalchemy import or_

schedule_course_field = {
    'id' : fields.Integer,
    'local' : fields.String,
    'dia' : fields.Integer,
    'data_inicio' : fields.String(attribute=lambda x: x.data_inicio.strftime('%d/%m/%Y %H:%M')),
    'data_fim' : fields.String(attribute=lambda x: x.data_fim.strftime('%d/%m/%Y %H:%M')),

    'titulo' : fields.String(attribute=lambda obj: obj.course.titulo),
    'ministrante': fields.String(attribute=lambda obj: obj.course.speaker.nome),
    'vagas' : fields.Integer,
    'turma' : fields.String,
    'course_id' : fields.Integer,
}
schedule_lecture_field = {
    'id' : fields.Integer,
    'local' : fields.String,
    'dia' : fields.Integer,
    'data_inicio' : fields.String(attribute=lambda x: x.data_inicio.strftime('%d/%m/%Y %H:%M')),
    'data_fim' : fields.String(attribute=lambda x: x.data_fim.strftime('%d/%m/%Y %H:%M')),

    'titulo' : fields.String(attribute=lambda obj: obj.lecture.titulo),
    'ministrante': fields.String(attribute=lambda obj: obj.lecture.speaker.nome),
    'lecture_id' : fields.Integer
}
schedule_other_field = {
    'id' : fields.Integer,
    'local' : fields.String,
    'dia' : fields.Integer,
    'data_inicio' : fields.String(attribute=lambda x: x.data_inicio.strftime('%d/%m/%Y %H:%M')),
    'data_fim' : fields.String(attribute=lambda x: x.data_fim.strftime('%d/%m/%Y %H:%M')),

    'titulo' : fields.String,
    'descricao' : fields.String,
}
user_course_schedule_report_field = {
    'nome' : fields.String(attribute=lambda x: x.user.nome),
    'matricula' : fields.String(attribute=lambda x: x.user.matricula),
}


class ScheduleAdminResource(Resource):
    def user_course_schedule_report(self, schedule_id, request):
        ucsr = CourseSubsModel.query.filter(or_(
            CourseSubsModel.option1 == schedule_id,
            CourseSubsModel.option2 == schedule_id
        )).all()
        if len(ucsr) == 0:
            return marshal({'message':'Nenhum participante encontrado'}, message), 404
        ucsr = [marshal(u,user_course_schedule_report_field) for u in ucsr]
        file_name = request.args.get('filename', 'export-data')
        file_type = request.args.get('csvformat', 0)
        file_type = 'csv' if int(file_type) == 1 else 'xls'
        return Excel.report_from_records(ucsr, file_type=file_type,
                                         file_name=file_name)
    @admin_required
    def get(self, schedule_id=None):
        # relatorio de participantes associados ao minicurso
        report = request.args.get('report', 0)
        if int(report) == 1:
            if not schedule_id:
                return marshal({'message':'Codigo do minicurso não encontrado!'}, message), 404
            return self.user_course_schedule_report(schedule_id, request)

        if schedule_id:
            schedule = ScheduleModel.query.filter_by(id=schedule_id).first()
            if not schedule:
                return marshal({'message':'Programação não encontrada!'}, message), 404
            return marshal(schedule, schedule_field), 200
        schedules = ScheduleModel.query.order_by(ScheduleModel.id).all()
        if len(schedules) == 0:
            return marshal({'message':'Nenhuma programação cadastrada foi encontrada.'}, message), 404
        other_schedule, course_schedule, lecture_schedule = [], [], []
        for s in schedules:
            if not s.course_id and not s.lecture_id:
                other_schedule.append(marshal(s, schedule_other_field))
            elif s.course_id:
                course_schedule.append(marshal(s, schedule_course_field))
            elif s.lecture_id:
                lecture_schedule.append(marshal(s, schedule_lecture_field))

        return {'course' : course_schedule,
                'lecture': lecture_schedule,
                'other': other_schedule}, 200

    @admin_required
    def post(self):
        def dt(x): return datetime.strptime(x, '%d/%m/%Y %H:%M')
        formtype = request.args.get('formtype', None)
        if not formtype:
            return marshal({'message':'Tipo de formulario não econtrado!'}, message), 404
        schedule = ScheduleModel(
            local = request.json['local'],
            dia = dt(request.json['data_inicio']).weekday(),
            data_inicio = dt(request.json['data_inicio']),
            data_fim = dt(request.json['data_fim'])
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
            marshal_field = schedule_course_field
        elif formtype == 'lecture':
            lecture = LectureModel.query.filter_by(id=request.json['lecture_id']).first()
            if not lecture:
                return marshal({'message':'Palestra não encontrada!'}, message), 404
            schedule.setLecture(
                lecture = lecture
            )
            marshal_field = schedule_lecture_field
        elif formtype == 'other':
            schedule.setOther(
                titulo = request.json['titulo'],
                descricao = request.json['descricao']
            )
            marshal_field = schedule_other_field
        try:
            db.session.add(schedule)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao cadastrar a programação!'}, message), 422
        else:
            return marshal(schedule, marshal_field), 201

    @admin_required
    def put(self):
        def dt(x): return datetime.strptime(x, '%d/%m/%Y %H:%M')
        formtype = request.args.get('formtype', None)
        if not formtype:
            return marshal({'message':'Tipo de formulario não econtrado!'}, message), 404
        schedule = ScheduleModel.query.filter_by(id=request.json['id']).first()
        schedule.local = request.json['local']
        schedule.dia = dt(request.json['data_inicio']).weekday()
        schedule.data_inicio = dt(request.json['data_inicio'])
        schedule.data_fim = dt(request.json['data_fim'])

        if formtype == 'course':
            course = CourseModel.query.filter_by(id=request.json['course_id']).first()
            if not course:
                return marshal({'message':'Minicurso não encontrado!'}, message), 404
            schedule.setCourse(
                vagas = request.json['vagas'],
                turma = request.json['turma'],
                course = course
            )
            marshal_field = schedule_course_field
        elif formtype == 'lecture':
            lecture = LectureModel.query.filter_by(id=request.json['lecture_id']).first()
            if not lecture:
                return marshal({'message':'Palestra não encontrada!'}, message), 404
            schedule.setLecture(
                lecture = lecture
            )
            marshal_field = schedule_lecture_field
        elif formtype == 'other':
            schedule.setOther(
                titulo = request.json['titulo'],
                descricao = request.json['descricao']
            )
            marshal_field = schedule_other_field
        try:
            db.session.add(schedule)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao cadastrar a programação!'}, message), 422
        else:
            return marshal(schedule, marshal_field), 200

    @admin_required
    def delete(self, schedule_id):
        schedule = ScheduleModel.query.filter_by(id=schedule_id).first()
        if not schedule:
            return marshal({'message':'Programação não encontrada!'}, message), 404
        try:
            db.session.delete(schedule)
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao excluir a programação selecionada!'}, message), 404
        else:
            return marshal({'message':'Programação excluida com sucesso!'}, message), 200
