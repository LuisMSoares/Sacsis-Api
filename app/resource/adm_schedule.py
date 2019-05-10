from flask_restful import Resource, request, fields, marshal
from app.db import db, LectureModel, CourseModel, ScheduleModel, CourseSubsModel
from app.resource import message, admin_required
from app.services.excel import Excel
from datetime import datetime
from sqlalchemy import or_

schedule_field = {
    'id' : fields.Integer,
    'local' : fields.String,
    'dia' : fields.String,
    'data_inicio' : fields.DateTime(dt_format='iso8601'),
    'data_fim' : fields.DateTime(dt_format='iso8601'),
    'vagas' : fields.Integer,
    'turma' : fields.String,
    'titulo' : fields.String,
    'descricao' : fields.String,
    'course_id' : fields.Integer,
    'lecture_id' : fields.Integer
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
        format_schedules = [marshal(s, schedule_field) for s in schedules]
        return {'quantidade': len(format_schedules),'programacao': format_schedules}, 200

    @admin_required
    def post(self):
        def dt(x): return datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f')
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

    @admin_required
    def put(self):
        def dt(x): return datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f')
        formtype = request.args.get('formtype', None)
        if not formtype:
            return marshal({'message':'Tipo de formulario não econtrado!'}, message), 404
        schedule = ScheduleModel.query.filter_by(id=request.json['id']).first()
        schedule.local = request.json['local']
        schedule.dia = dt(request.json['data_inicio']).weekday()
        schedule.data_inicio = request.json['data_inicio']
        schedule.data_fim = request.json['data_fim']

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
            return {'message':'Programação cadastrada com sucesso!'}, 20

    @admin_required
    def delete(self, schedule_id):
        schedule = ScheduleModel.query.filter_by(id=schedule_id).first()
        if not schedule:
            return marshal({'message':'Programação não encontrada!'}, message), 404
        try:
            db.session.delete(schedule)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao excluir a programação selecionada!'}, message), 404
        else:
            return marshal({'message':'Programação excluida com sucesso!'}, message), 200