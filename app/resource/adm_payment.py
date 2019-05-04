from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource, marshal, fields, request
from app.db import db, UserPaymentModel, LotModel, UserModel
from app.resource import message, admin_required
from datetime import datetime

lot_field = {
    'id' : fields.Integer,
    'valor' : fields.Float,
    'data_criacao' : fields.DateTime(dt_format='iso8601'),
    'data_modificacao' : fields.DateTime(dt_format='iso8601'),
    'admin_nome' : fields.String(attribute=lambda x: x.user.nome)
}
lot_price_field = {
    'id' : fields.Integer,
    'valor' : fields.Float,
}
payment_field = {
    'user_nome' : fields.String(attribute=lambda x: x.user.nome),
    'lote_id' : fields.Integer,
    'valor' : fields.Float,
    'data_pagamento' : fields.DateTime(dt_format='iso8601'),
    'data_modificacao' : fields.DateTime(dt_format='iso8601'),
    'admin_nome' : fields.String(attribute=lambda x: x.user_admin.nome)
}
lot_list_fields = {
    'quantidade': fields.Integer,
    'lotes': fields.List(fields.Nested(lot_field)),
}
payment_list_fields = {
    'quantidade': fields.Integer,
    'pagamentos': fields.List(fields.Nested(payment_field)),
}


class LotAdminResource(Resource):
    @admin_required
    def get(self, lot_id=None):
        loadvalue = request.args.get('loadvalue', 0)
        if lot_id:
            lot = LotModel.query.filter_by(id=lot_id).first()
            if not lot:
                return marshal({'message':'Lote não encontrado.'}, message), 404
            return marshal(lot, lot_field), 200
        else:
            lots = LotModel.query.order_by(LotModel.id).all()
            if len(lots) == 0:
                return marshal({'message':'Nenhum lote cadastrado!'}, message), 404
            if int(loadvalue) == 1:
                return {'lotes':[marshal(lot,lot_price_field) for lot in lots]}, 200
            return marshal({
                'quantidade': len(lots),
                'lotes': lots
            },lot_list_fields), 200

    @admin_required
    def post(self):
        lot = LotModel(
            valor = request.json['valor'],
            admin_user_id = get_jwt_identity()
        )
        try:
            db.session.add(lot)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao registrar o lote'}, message), 422
        return marshal(lot, lot_field), 201

    @admin_required
    def put(self):
        lot = LotModel.query.filter_by(id=request.json['id']).first()
        if not lot:
            return marshal({'message':'Lote não encontrado!'}, message), 404
        lot.valor = request.json['valor']
        lot.data_modificacao = datetime.now()
        lot.admin_user_id = get_jwt_identity()
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal(
                {'message':'Ocorreu um erro ao atualizar informações do lote'},
                message), 422
        return marshal(lot, lot_field), 201


class PaymentAdminResource(Resource):
    @admin_required
    def get(self):
        upayment = UserPaymentModel.query.order_by(UserPaymentModel.data_pagamento).all()
        if len(upayment) == 0:
            return marshal({'message':'Nenhum pagamento foi encontrado.'}, message), 404
        return marshal({
            'quantidade': len(upayment),
            'pagamentos': upayment
        },payment_list_fields), 200

    @admin_required
    def post(self):
        lot = LotModel.query.filter_by(id=request.json['lote_id']).first()
        user = UserModel.query.filter_by(id=request.json['user_id']).first()
        if not lot:
            return marshal({'message':'Lote não encontrado.'}, message), 404
        if not user:
            return marshal({'message':'Usuário informado não encontrado.'}, message), 404
        upayment = UserPaymentModel(
            user_id = request.json['user_id'],
            lote_id = lot.id,
            valor = lot.valor,
            admin_user_id = get_jwt_identity()
        )
        user.status_pago = True
        try:
            db.session.add(upayment)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao registrar o pagamento'}, message), 422
        return marshal(upayment, payment_field), 201

    @admin_required
    def put(self):
        lot = LotModel.query.filter_by(id=request.json['lote_id']).first()
        upayment = UserPaymentModel.query.filter_by(user_id=request.json['user_id']).first()
        if not lot:
            return marshal({'message':'Lote não encontrado.'}, message), 404
        if not upayment:
            return marshal({'message':'Pagamento de usuário não encontrado.'}, message), 404
        upayment.lote_id = lot.id
        upayment.valor = lot.valor
        upayment.data_modificacao = datetime.now()
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao atualizar pagamento'}, message), 422
        return marshal(upayment, payment_field), 200

    @admin_required
    def delete(self, user_id=0):
        upayment = UserPaymentModel.query.filter_by(user_id=user_id).first()
        if not upayment:
            return marshal({'message':'Pagamento de usuário não encontrado.'}, message), 404
        user = UserModel.query.filter_by(id=upayment.user_id).first()
        user.status_pago = False
        upayment.valor = None
        upayment.lote = None
        upayment.data_modificacao = datetime.now()
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao remover pagamento'}, message), 422
        return marshal(upayment, payment_field), 200