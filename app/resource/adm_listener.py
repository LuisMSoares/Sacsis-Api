from flask_restful import Resource, request, marshal, fields
from app.db import db, UserModel, ListenerModel, ScheduleModel, CourseSubsModel
from app.resource import message, admin_required
from datetime import datetime
from sqlalchemy import and_

listener_user_field = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'nome': fields.String(attribute=lambda obj: obj.user.nome),
    'schedule_id': fields.Integer,
    'data_inicio': fields.String(attribute=lambda obj: obj.data_inicio.strftime('%H:%M')),
    'data_fim': fields.String(attribute=lambda obj: obj.data_fim.strftime('%H:%M') if obj.data_fim else None)
}
list_listeners = {
    'id': fields.Integer,
    'matricula': fields.String(attribute=lambda obj: obj.user.matricula),
    'nome': fields.String(attribute=lambda obj: obj.user.nome),
    'data_inicio': fields.String(attribute=lambda obj: obj.data_inicio.strftime('%H:%M')),
    'data_fim': fields.String(attribute=lambda obj: obj.data_fim.strftime('%H:%M') if obj.data_fim else None)
}


class ListenerAdminResource(Resource):
    @admin_required
    def get(self, schedule_id):
        listeners = ListenerModel.query.filter_by(schedule_id=schedule_id).all()
        values = []
        for listener in listeners:
            values.append(marshal(listener, list_listeners))
        return values, 200

    @admin_required
    def post(self):
        user = UserModel.query.filter_by(matricula=request.json['matricula']).first()
        if not user:
            return marshal({'message':'Participante não encontrado!'}, message), 404
        if not user.ativo:
            return marshal({'message':'Participante não ativo!'}, message), 404
        if not user.status_pago:
            return marshal({'message':'O participante ainda não realizou o pagamento!'+user.email}, message), 404

        listener = ListenerModel.query.filter(and_(
            ListenerModel.user_id == user.id,
            ListenerModel.schedule_id == request.json['schedule_id']
        )).first()

        if listener:
            schedule = ScheduleModel.query.filter_by(id=request.json['schedule_id']).first()
            result = listener.finish_validation(schedule)
            if not result:
                return marshal({'message':'Não foi possivel registrar presença no evento, verifique o horario!'}, message), 404
            listener.data_fim = result

        else:
            schedule = ScheduleModel.query.filter_by(id=request.json['schedule_id']).first()
            if not schedule:
                return marshal({'message':'Evento não encontrado!'}, message), 404
            if schedule.course_id:
                event = CourseSubsModel.query.filter_by(user_id=user.id).first()
                if not event:
                    return marshal({'message':'Usuário não registrado no evento!'}, message), 404
                if schedule.id not in [event.option1, event.option2]:
                    return marshal({'message':'Usuário não registrado no evento!'}, message), 404

            listener = ListenerModel(
                user_id = user.id,
                schedule_id = request.json['schedule_id'],
            )
            result = listener.start_validation(schedule)
            if not result:
                return marshal({'message':'Não foi possivel registrar presença no evento, verifique o horario!'}, message), 404
            listener.data_inicio = result

        try:
            db.session.add(listener)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao cadastrar a presença!'}, message), 422
        return marshal(listener, listener_user_field), 201