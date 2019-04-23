from flask_restful import Resource, request, fields, marshal
from app.db import db, ScheduleModel
from app.resource import message, admin_required

course_schedule_field = {
    'id' : fields.Integer,
    'local': fields.String,
    'dia' : fields.Integer,
    'data_inicio' : fields.String(attribute=lambda obj: obj.data_inicio.strftime('%H:%M')),
    'data_fim' : fields.String(attribute=lambda obj: obj.data_fim.strftime('%H:%M')),

    'vagas' : fields.Integer,
    'turma' : fields.String,
    'minicurso' : fields.String(attribute=lambda obj: obj.course.titulo)
}
lecture_schedule_field = {
    'id' : fields.Integer,
    'local': fields.String,
    'dia' : fields.Integer,
    'data_inicio' : fields.String(attribute=lambda obj: obj.data_inicio.strftime('%H:%M')),
    'data_fim' : fields.String(attribute=lambda obj: obj.data_fim.strftime('%H:%M')),

    'palestra' : fields.String(attribute=lambda obj: obj.lecture.titulo)
}
other_schedule_field = {
    'id' : fields.Integer,
    'local': fields.String,
    'dia' : fields.Integer,
    'data_inicio' : fields.String(attribute=lambda obj: obj.data_inicio.strftime('%H:%M')),
    'data_fim' : fields.String(attribute=lambda obj: obj.data_fim.strftime('%H:%M')),

    'titulo' : fields.String,
    'descricao' : fields.String
}
#fields.DateTime(dt_format='iso8601')

class ScheduleResource(Resource):
    def get(self):
        values = {}
        for i in range(1,8):
            schedules = ScheduleModel.query.order_by(ScheduleModel.data_inicio).filter_by(dia=i).all()
            if not schedules:
                continue
            values[str(i)] = []
            for schedule in schedules:
                if schedule.course_id:
                    values[str(i)].append(marshal(schedule, course_schedule_field))
                if schedule.lecture_id:
                    values[str(i)].append(marshal(schedule, lecture_schedule_field))
                if not schedule.course_id and not schedule.lecture_id:
                    values[str(i)].append(marshal(schedule, other_schedule_field))
        return values, 200