from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource, fields, marshal, request
from app.db import db, ScheduleModel, UserModel, CourseSubsModel
from app.resource import jwt_token_required_custom, jsonGet
from sqlalchemy import or_

course_schedule_fields = {
    'id' : fields.Integer,
    'titulo' : fields.String(attribute=lambda o: o.course.titulo),
    'descricao' : fields.String(attribute=lambda o: o.course.conteudo),
    'ministrante' : fields.String(attribute=lambda o: o.course.speaker.nome),
    # informa o total de vagas
    'vagas' : fields.Integer,
    # informa o total de vagas ainda disponivel
    'vagas_disponiveis' : fields.Integer(attribute=lambda o: o.vacRemaining())
}
course_sub_fields = {
    'option1': fields.String(default='Minicurso duplicado ou não encontrado!'),
    'option2': fields.String(default='Minicurso duplicado ou não encontrado!')
}


class CourseScheduleResource(Resource):
    def get(self):
        courses = ScheduleModel.query.filter(ScheduleModel.course_id.isnot(None)).all()
        if len(courses) == 0:
            return marshal({'message':'Nenhuma programação cadastrada foi encontrada.'}, message), 404
        format_courses = [marshal(c,course_schedule_fields) for c in courses]
        return {'quantidade': len(format_courses),'minicursos': format_courses}, 200

    @jwt_token_required_custom
    def post(self):
        def dupVerify(course_id, op1=None, op2=None):
            if op1 not in course_id and op1 != None:
                course_id[0] = op1
            if op2 not in course_id and op2 != None:
                course_id[1] = op2
            if op1 not in course_id and op1 != None:
                course_id[0] = op1
            return course_id

        user_id = get_jwt_identity()
        course_id1 = jsonGet(request.json, 'course_id1', default=0)
        course_id2 = jsonGet(request.json, 'course_id2', default=0)

        # verifica se os minicursos informados existem cadastrados na programação
        courses = ScheduleModel.query.filter(or_(course_id==course_id1, course_id==course_id2)).all()
        if len(courses) == 0:
            return marshal({'message':'Nenhum minicurso informado foi encontrado.'}, message), 404
        #cria uma lista com os ids dos minicursos/programação da consulta
        elif len(courses) == 1:
            course_id = [courses[0].id, None]
        elif len(courses) == 2:
            course_id = [courses[0].id, courses[1].id]

        # verifica se o usuario já possui alguma reserva de vagas cadastrada anteriormente.
        mysubs = CourseSubsModel.query.filter_by(user_id=user_id).all()
        # cria uma lista com os ids dos minicursos/programação encontrados pela consulta
        if len(sub) == 0:
            subs_id = [None, None]
        if len(sub) == 1:
            subs_id = [mysubs[0].schedule_id, None]
        if len(sub) == 2:
            subs_id = [mysubs[0].schedule_id, mysubs[1].schedule_id]
        
        # verifica e trata se um mesmo minicurso foi selecionado duas vezes.
        course_id = dupVerify(course_id=subs_id, *course_id)

        resp, scode = {}, 201
        # realiza a inscrição do minicurso no banco de dados, caso tenha vagas ainda disponivel.
        for i, course, mysub, cid in enumerate(zip(courses, mysubs, course_id)):
            if not course:
                resp[f'option{i+1}'] = 'Minicurso informado não encontrado'
                continue
            if course.vacRemaining() > 0:
                if not mysub:
                    mysub = CourseSubsModel(user_id=user_id)
                mysub.schedule_id = cid
                try:
                    db.session.add(mysub)
                    db.session.commit()
                    resp[f'option{i+1}'] = 'Vaga reservada com sucesso!'
                except:
                    db.session.rollback()
                    resp[f'option{i+1}'] = 'Ocorreu um erro ao registrar a inscrição.'
                    scode = 422
            else:
                resp[f'option{i+1}'] = 'Todas as vagas já foram preenchidas.'

        return marshal(response, course_sub_fields), 201