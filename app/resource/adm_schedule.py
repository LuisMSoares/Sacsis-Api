from flask_restful import Resource, request, fields, marshal
from app.db import db, LectureModel, CourseModel, ScheduleModel
from app.resource import message, admin_required
from datetime import datetime

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
#parse temporario de iso8601
dt = lambda x: datetime(int(x[:4]), int(x[5:7]), int(x[8:10]), int(x[11:13]), int(x[14:16]), int(x[17:19]), int(x[20:26]))
class ScheduleAdminResource(Resource):
    @admin_required
    def post(self):
        formtype = request.args.get('formtype', None)
        if not formtype:
            return marshal({'message':'Tipo de formulario não econtrado!'}, message), 404
        schedule = ScheduleModel(
            local = request.json['local'],
            dia = dt(request.json['data_inicio']).weekday(),
            data_inicio = dt(request.json['data_inicio']), #parse temporario
            data_fim = dt(request.json['data_fim']) #parse temporario
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

    @admin_required
    def get(self, schedule_id=None):
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