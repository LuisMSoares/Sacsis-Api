from flask_restful import Resource, marshal, fields, request
from app.resource import message, admin_required
from app.services.excel import Excel
from app.db import db, SpeakerModel
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
    'site' : fields.String,
    'ocupacao' : fields.String(attribute=lambda x: x.occupation())
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
            # relatorio de ministrantes cadastrados
            report = request.args.get('report', 0)
            if int(report) == 1:
                file_type = request.args.get('csvformat', 0)
                file_type = 'csv' if int(file_type) == 1 else 'xls'
                return Excel.report_from_records(speakers, file_type=file_type, 
                                                 file_name='relatorio-ministrantes')
            else:
                return {
                    'quantidade': len(speakers),
                    'ministrantes': speakers
                }, 200

    @admin_required
    def delete(self, speaker_id=None):
        if not speaker_id:
            return marshal({'message':'Informe o id do ministrante'}, message), 404
        speaker = SpeakerModel.query.filter_by(id=speaker_id).first()
        if not speaker:
            return marshal({'message':'Ministrante não encontrado'}, message), 404
        try:
            db.session.delete(speaker)
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(speaker, speaker_admin_field), 201
