from flask_restful import Resource, request, fields, marshal, url_for
from app.resource import message
from datetime import datetime
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
        attribute=lambda obj: url_for('get_image', img_id=obj.course.speaker.id, _external=True, _scheme='https'))
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
        attribute=lambda obj: url_for('get_image', img_id=obj.lecture.speaker.id, _external=True, _scheme='https'))
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

app_course_schedule_field = {
    'titulo' : fields.String(attribute=lambda obj: obj.course.titulo),

    'id' : fields.Integer,
    'local': fields.String,
    'data_inicio' : fields.String(attribute=lambda obj: obj.data_inicio.strftime('%H:%M')),
    'data_fim' : fields.String(attribute=lambda obj: obj.data_fim.strftime('%H:%M'))
}
app_lecture_schedule_field = {
    'titulo' : fields.String(attribute=lambda obj: obj.lecture.titulo),

    'id' : fields.Integer,
    'local': fields.String,
    'data_inicio' : fields.String(attribute=lambda obj: obj.data_inicio.strftime('%H:%M')),
    'data_fim' : fields.String(attribute=lambda obj: obj.data_fim.strftime('%H:%M'))
}
app_other_schedule_field = {
    'titulo' : fields.String,

    'id' : fields.Integer,
    'local': fields.String,
    'data_inicio' : fields.String(attribute=lambda obj: obj.data_inicio.strftime('%H:%M')),
    'data_fim' : fields.String(attribute=lambda obj: obj.data_fim.strftime('%H:%M'))
}


class ScheduleResource(Resource):
    def _weekday(self, integer_day):
        today = datetime.now().weekday()
        if integer_day < today:
            return -1
        if integer_day == today:
            return 0
        if integer_day > today:
            return 1
        

    def _appValues(self):
        values = []
        dias = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira']
        for i in range(0,5):
            schedules = ScheduleModel.query.order_by(ScheduleModel.data_inicio).filter_by(dia=i).all()
            values.append( {'title': dias[i], 'status': self._weekday(i), 'data':[]} )

            if not schedules:
                continue
            for schedule in schedules:
                if not schedule.course_id and not schedule.lecture_id:
                    values[-1]['data'].append(marshal(schedule, app_other_schedule_field))
                if schedule.course_id:
                    values[-1]['data'].append(marshal(schedule, app_course_schedule_field))
                if schedule.lecture_id:
                    values[-1]['data'].append(marshal(schedule, app_lecture_schedule_field))
        return values

    def get(self):
        loadtitle = int(request.args.get('appvalues', 0))
        if(loadtitle==1):            
            return self._appValues(), 200 

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