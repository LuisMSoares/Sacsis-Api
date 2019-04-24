from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource, fields, marshal, request
from app.db import db, ScheduleModel, UserModel, CourseSubsModel
from app.resource import jwt_token_required_custom, jsonGet, message
from sqlalchemy import or_, and_

course_schedule_fields = {
    'id' : fields.Integer,
    'titulo' : fields.String(attribute=lambda o: o.course.titulo),
    'descricao' : fields.String(attribute=lambda o: o.course.conteudo),
    'ministrante' : fields.String(attribute=lambda o: o.course.speaker.nome),
    'turma': fields.String,
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
        def dupVerify(actualy, op1=None, op2=None):
            if op1 not in actualy and op1 != None:
                actualy[0] = op1
            if op2 not in actualy and op2 != None:
                actualy[1] = op2
            if op1 not in actualy and op1 != None:
                actualy[0] = op1
            return actualy
        def saveOption(course_id, flambda):
            course = ScheduleModel.query.filter(and_(
                ScheduleModel.course_id.isnot(None),
                ScheduleModel.id == course_id
            )).first()
            if not course:
                return 'Minicurso selecionado não encontrado.'
            if course.vacRemaining() > 0:
                flambda(course.id)
                return 'Vaga reservada com sucesso!'
            else:
                return 'Todas as vagas foram preenchidas.'

        user_id = get_jwt_identity()
        course_id1 = jsonGet(request.json, 'option1', default=0)
        course_id2 = jsonGet(request.json, 'option2', default=0)
        # verifica se existe alguma reserva armazenada.
        course_sub = CourseSubsModel.query.filter_by(user_id=user_id).first()
        if not course_sub:
            course_sub = CourseSubsModel(user_id=user_id)
        myoptions = [course_sub.option1, course_sub.option2]
        # garante que não ocorra reservas duplicadas.
        myoptions = dupVerify(myoptions, op1=course_id1, op2=course_id2)

        # realiza as reservas das vadas dos minicursos armazenando uma resposta
        response = {
            'option1': saveOption(myoptions[0], lambda id: course_sub.setOption1(id)),
            'option2': saveOption(myoptions[1], lambda id: course_sub.setOption1(id))
        }
        # persiste as alterações/'novas informações' no banco de dados
        try:
            db.session.add(course_sub)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao salvar suas reservas.'}, message), 422
        return marshal(response, course_sub_fields), 201

    # Remove a reserva da vaga para a opção informada no json do request
    @jwt_token_required_custom
    def put(self):
        user_id = get_jwt_identity()
        course_sub = CourseSubsModel.query.filter_by(user_id=user_id).first()
        if not course_sub:
            return marshal({'message':'Não existe reservas para este usuário.'}, message), 404
        course_id1 = jsonGet(request.json, 'option1', default=False)
        course_id2 = jsonGet(request.json, 'option2', default=False)
        if course_id1 == True: course_sub.option1 = None
        if course_id2 == True: course_sub.option2 = None
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao salvar alterações.'}, message), 200
        return marshal({'message':'Alterações salvas com sucesso.'}, message), 200