from flask_restful import Resource, marshal, fields, request
from app.db import db, SpeakerModel
from app.resource import message, admin_required
from app.services import Token
from datetime import datetime
from sqlalchemy import or_

speaker_admin_field = {
    'id' : fields.Integer,
    'nome' : fields.String,
    'resumo' : fields.String,
    'rg' : fields.String,
    'cpf' : fields.String,
    'gravatar' : fields.String,
    'facebook' : fields.String,
    'twitter' : fields.String,
    'instagram' : fields.String,
    'site' : fields.String
}
speaker_admin_list_fields = {
    'quantidade': fields.Integer,
    'ministrantes': fields.List(fields.Nested(speaker_admin_field)),
}
token_field = {
    'token': fields.String
}


class SpeakerAdminResource(Resource):
    @admin_required
    def get(self):
        if self.rjvfy(request):
            rg, cpf = self.jvfy(request.json,'rg'), self.jvfy(request.json,'cpf')
            speaker = SpeakerModel.query.filter(
                or_(SpeakerModel.rg == rg, SpeakerModel.cpf == cpf)).first()
            if speaker:
                return marshal(speaker, speaker_admin_field), 200
            return marshal({'message':'Nenhum ministrante encontrado!'}, message), 404
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
    def post(self):
        speaker = SpeakerModel(
            nome = request.json['nome'],
            resumo = request.json['resumo'],
            rg = request.json['rg'],
            cpf = request.json['cpf'],
            facebook = request.json['facebook'] or '',
            twitter = request.json['twitter'] or '',
            instagram = request.json['instagram'] or '',
            site = request.json['site'] or ''
        )
        speaker.set_created_data()
        speaker.set_gravatar(request.json['gravatar'] or '')
        try:
            db.session.add(speaker)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ministrante já cadastrado no sistema'}, message), 422
        else:
            return marshal({'message':'Ministrante cadastrado'}, message), 201


    @admin_required
    def put(self):
        speaker = SpeakerModel.query.filter_by(id=request.json['id']).first()
        if not speaker:
            return marshal({'message':'Ministrante inexistente'}, message), 404
        if 'nome' in request.json:
            speaker.nome = request.json['nome']
        if 'resumo' in request.json:
            speaker.nome = request.json['nome']
        if 'rg' in request.json:
            speaker.nome = request.json['nome']
        if 'cpf' in request.json:
            speaker.nome = request.json['nome']
        if 'gravatar' in request.json:
            speaker.set_gravatar(request.json['gravatar'])
        if 'facebook' in request.json:
            speaker.nome = request.json['nome']
        if 'twitter' in request.json:
            speaker.nome = request.json['nome']
        if 'instagram' in request.json:
            speaker.nome = request.json['nome']
        if 'site' in request.json:
            speaker.nome = request.json['nome']
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


    # verifica a existencia de uma chave no json
    def jvfy(self,json,key):
        try:
            return json[key]
        except:
            return ''

            
    # verifica se o json existe no request
    def rjvfy(self, req):
        try:
            r = request.json
            return True
        except:
            return False