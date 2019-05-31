from flask_restful import Resource, request, fields, marshal, url_for
from app.resource import message
from app.db import db, ScheduleModel

course_schedule_field = {
    'id' : fields.Integer,
    'local': fields.String,
    'dia' : fields.Integer,
    'data_inicio' : fields.String(attribute=lambda obj: obj.data_inicio.strftime('%H:%M')),
    'data_fim' : fields.String(attribute=lambda obj: obj.data_fim.strftime('%H:%M')),

    'vagas' : fields.Integer,
    'turma' : fields.String,
    'minicurso' : fields.String(attribute=lambda obj: obj.course.titulo),
    'ministrante': fields.String(attribute=lambda obj: obj.course.speaker.nome),
    'avatar': fields.String(
        attribute=lambda obj: url_for('get_image', img_id=obj.course.speaker.id, _external=True))
}
lecture_schedule_field = {
    'id' : fields.Integer,
    'local': fields.String,
    'dia' : fields.Integer,
    'data_inicio' : fields.String(attribute=lambda obj: obj.data_inicio.strftime('%H:%M')),
    'data_fim' : fields.String(attribute=lambda obj: obj.data_fim.strftime('%H:%M')),

    'palestra' : fields.String(attribute=lambda obj: obj.lecture.titulo),
    'ministrante': fields.String(attribute=lambda obj: obj.lecture.speaker.nome),
    'avatar': fields.String(
        attribute=lambda obj: url_for('get_image', img_id=obj.lecture.speaker.id, _external=True))
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

speaker_field = {
    'id' : fields.Integer,
    'nome' : fields.String,
    'resumo' : fields.String,
    'facebook' : fields.String,
    'twitter' : fields.String,
    'instagram' : fields.String,
    'site' : fields.String,
    'avatar': fields.String(
        attribute=lambda o: url_for('get_image', img_id=o.id, _external=True))
}

class ScheduleResource(Resource):
    def get(self):
        values = {}
        for i in range(0,5):
            schedules = ScheduleModel.query.order_by(ScheduleModel.data_inicio).filter_by(dia=i).all()
            if not schedules:
                continue
            values[str(i)] = []
            for schedule in schedules:
                if not schedule.course_id and not schedule.lecture_id:
                    values[str(i)].append(marshal(schedule, other_schedule_field))
                if schedule.course_id:
                    values[str(i)].append(marshal(schedule, course_schedule_field))
                if schedule.lecture_id:
                    values[str(i)].append(marshal(schedule, lecture_schedule_field))
        if not values:
            return marshal({'message':'Nenhuma programação encontrada.'}, message), 404
        return values, 200