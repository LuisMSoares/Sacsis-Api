from flask_restful import Resource, marshal, request, fields
from app.db import CourseModel, LectureModel
from app.resource import message


class ScheduleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vagas = db.Column(db.Integer)
    local = db.Column(db.String)
    hora_inicio = db.Column(db.DateTime, nullable=False)
    hora_termino = db.Column(db.DateTime, nullable=False)
    lecture_id = db.Column(db.Integer)
    course_id = db.Column(db.Integer)


class ScheduleAdminResource(Resource):
    def get(self):
        
    def post(self):

    def put(self):

    def delete(self):