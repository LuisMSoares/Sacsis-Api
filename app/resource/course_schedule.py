from flask_restful import Resource, fields, marshal
from app.db import ScheduleModel, UserModel

course_schedule_fields = {
    'id' : fields.Integer,
    'titulo' : fields.String(attribute=lambda o: o.course.titulo),
    'descricao' : fields.String(attribute=lambda o: o.course.conteudo),
    'ministrante' : fields.String(attribute=lambda o: o.course.speaker.nome),
    'vagas' : fields.Integer
}


class CourseScheduleResource(Resource):
    def get(self):
        courses = ScheduleModel.query.all()
        if len(courses) == 0:
            return marshal({'message':'Nenhuma programação cadastrada foi encontrada.'}, message), 404
        format_courses = [marshal(c,course_schedule_fields) for c in courses if c.course_id]
        return {'quantidade': len(format_courses),'minicursos': format_courses}, 200

    def post(self):
        pass
