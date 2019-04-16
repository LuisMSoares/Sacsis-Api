from flask_restful import Resource, marshal, fields, request
from app.resource import message, admin_required
from app.db import db, SpeakerModel
from app.services import Token
from datetime import datetime
from sqlalchemy import or_

speaker_admin_field = {
    'id' : fields.Integer,
    'nome' : fields.String,
    'resumo' : fields.String,
    'rg' : fields.String,
    'cpf' : fields.String,
    'facebook' : fields.String,
    'twitter' : fields.String,
    'instagram' : fields.String,
    'email' : fields.String,
    'telefone' : fields.String,
    'site' : fields.String
}
speaker_admin_list_fields = {
    'quantidade': fields.Integer,
    'ministrantes': fields.List(fields.Nested(speaker_admin_field)),
}


class SpeakerAdminResource(Resource):
    @admin_required
    def get(self, speaker_id=None):
        if speaker_id:
            speaker = SpeakerModel.query.filter_by(id=speaker_id).first()
            if not speaker:
                return marshal({'message':'Ministrante informado não encontrado!'}, message), 404
            return marshal(speaker,speaker_admin_field), 200
        else:
            qspeakers = SpeakerModel.query.order_by(SpeakerModel.id).all()
            speakers = [marshal(t, speaker_admin_field) for t in qspeakers]
            if len(speakers) == 0:
                return marshal({'message':'Nenhum ministrante encontrado!'}, message), 404
            return marshal({
                'quantidade': len(speakers),
                'ministrantes': speakers
            },speaker_admin_list_fields), 200


    @admin_required
    def put(self):
        rjson = json.loads(request.form['json_data'])
        speaker = SpeakerModel.query.filter_by(id=rjson['id']).first()
        if not speaker:
            return marshal({'message':'Ministrante inexistente'}, message), 404
        if 'avatar' in request.files:
            speaker.set_avatar(request.files['avatar'])
        if 'nome' in rjson:
            speaker.nome = rjson['nome']
        if 'resumo' in rjson:
            speaker.resumo = rjson['nome']
        if 'rg' in rjson:
            speaker.rg = rjson['nome']
        if 'cpf' in rjson:
            speaker.cpf = rjson['nome']
        if 'facebook' in rjson:
            speaker.facebook = rjson['nome']
        if 'twitter' in rjson:
            speaker.twitter = rjson['nome']
        if 'instagram' in rjson:
            speaker.instagram = rjson['nome']
        if 'site' in rjson:
            speaker.site = rjson['nome']
        if 'email' in rjson:
            speaker.email = rjson['email']
        if 'telefone' in rjson:
            speaker.telefone = rjson['telefone']
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(speaker, speaker_admin_field), 201


    @admin_required
    def delete(self, speaker_id=None):
        if not speaker_id:
            return marshal({'message':'Informe o id do ministrante'}, message), 404
        speaker = SpeakerModel.query.filter_by(id=speaker_id).first()
        if not speaker:
            return marshal({'message':'Ministrante não encontrado'}, message), 404
        try:
            db.session.delete(speaker)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(speaker, speaker_admin_field), 201
