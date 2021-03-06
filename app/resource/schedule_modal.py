from flask_restful import Resource, request, fields, marshal, url_for
from app.resource import message
from app.db import db, ScheduleModel

course_schedule_modal_field = {
    'tipo': fields.Integer(default='minicurso'),

    'avatar': fields.String(
        attribute=lambda obj: url_for('get_image', img_id=obj.course.speaker.id, _external=True, _scheme='https')),
    'ministrante': fields.String(attribute=lambda obj: obj.course.speaker.nome),
    'resumo': fields.String(attribute=lambda obj: obj.course.speaker.resumo),
    'facebook': fields.String(attribute=lambda obj: obj.course.speaker.parseFacebook()),
    'instagram': fields.String(attribute=lambda obj: obj.course.speaker.parseInstagram()),
    'twitter': fields.String(attribute=lambda obj: obj.course.speaker.parseTwitter()),
    'site': fields.String(attribute=lambda obj: obj.course.speaker.site),
    'titulo': fields.String(attribute=lambda obj: obj.course.titulo),
    'conteudo': fields.String(attribute=lambda obj: obj.course.conteudo)
}
lecture_schedule_modal_field = {
    'tipo': fields.Integer(default='palestra'),

    'avatar': fields.String(
        attribute=lambda obj: url_for('get_image', img_id=obj.lecture.speaker.id, _external=True, _scheme='https')),
    'ministrante': fields.String(attribute=lambda obj: obj.lecture.speaker.nome),
    'resumo': fields.String(attribute=lambda obj: obj.lecture.speaker.resumo),
    'facebook': fields.String(attribute=lambda obj: obj.lecture.speaker.parseFacebook()),
    'instagram': fields.String(attribute=lambda obj: obj.lecture.speaker.parseInstagram()),
    'twitter': fields.String(attribute=lambda obj: obj.lecture.speaker.parseTwitter()),
    'site': fields.String(attribute=lambda obj: obj.lecture.speaker.site),
    'titulo': fields.String(attribute=lambda obj: obj.lecture.titulo),
    'conteudo': fields.String(attribute=lambda obj: obj.lecture.conteudo)
}
other_schedule_modal_field = {
    'tipo': fields.Integer(default='outros'),
    
    'titulo' : fields.String,
    'descricao' : fields.String
}


class ScheduleModalResource(Resource):
    def get(self, schedule_id):
        schedule = ScheduleModel.query.filter_by(id=schedule_id).first()
        if not schedule:
            return marshal({'message':'Programação não encontrada.'}, message), 404
        if not schedule.course_id and not schedule.lecture_id:
            return marshal(schedule, other_schedule_modal_field), 200
        if schedule.course_id:
            return marshal(schedule, course_schedule_modal_field), 200
        if schedule.lecture_id:
            return marshal(schedule, lecture_schedule_modal_field), 200
