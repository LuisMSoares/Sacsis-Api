from flask_restful import Resource, marshal, fields, request
from app.db import db, TeachModel
from app.resource import message, admin_required
from sqlalchemy import or_

teach_admin_field = {
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
teach_admin_list_fields = {
    'quantidade': fields.Integer,
    'ministrantes': fields.List(fields.Nested(teach_admin_field)),
}


class TeachResource(Resource):
    @admin_required
    def get(self):
        if self.rjvfy(request):
            rg, cpf = self.jvfy(request.json,'rg'), self.jvfy(request.json,'cpf')
            teach = TeachModel.query.filter(
                or_(TeachModel.rg == rg, TeachModel.cpf == cpf)).first()
            if teach:
                return marshal(teach, teach_admin_field), 200
            return marshal({'message':'Nenhum ministrante encontrado!'}, message), 404
        else:
            qteachs = TeachModel.query.order_by(TeachModel.id).all()
            teachs = [marshal(t, teach_admin_field) for t in qteachs]
            if len(teachs) == 0:
                return marshal({'message':'Nenhum ministrante encontrado!'}, message), 404
            return marshal({
                'quantidade': len(teachs),
                'ministrantes': teachs
            },teach_admin_list_fields), 200



    @admin_required
    def post(self):
        teach = TeachModel(
            nome = request.json['nome'],
            resumo = request.json['resumo'],
            rg = request.json['rg'],
            cpf = request.json['cpf'],
            facebook = request.json['facebook'] or '',
            twitter = request.json['twitter'] or '',
            instagram = request.json['instagram'] or '',
            site = request.json['site'] or ''
        )
        teach.set_created_data()
        teach.set_gravatar(request.json['gravatar'] or '')
        try:
            db.session.add(teach)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ministrante já cadastrado no sistema'}, message), 422
        else:
            return marshal({'message':'Ministrante cadastrado'}, message), 201


    @admin_required
    def put(self):
        teach = TeachModel.query.filter_by(id=request.json['id']).first()
        if not teach:
            return marshal({'message':'Ministrante inexistente'}, message), 404
        if 'nome' in request.json:
            teach.nome = request.json['nome']
        if 'resumo' in request.json:
            teach.nome = request.json['nome']
        if 'rg' in request.json:
            teach.nome = request.json['nome']
        if 'cpf' in request.json:
            teach.nome = request.json['nome']
        if 'gravatar' in request.json:
            teach.set_gravatar(request.json['gravatar'])
        if 'facebook' in request.json:
            teach.nome = request.json['nome']
        if 'twitter' in request.json:
            teach.nome = request.json['nome']
        if 'instagram' in request.json:
            teach.nome = request.json['nome']
        if 'site' in request.json:
            teach.nome = request.json['nome']
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(teach, teach_admin_field), 201


    @admin_required
    def delete(self, teach_id=None):
        if not teach_id:
            return marshal({'message':'Informe o id do ministrante'}, message), 404
        teach = TeachModel.query.filter_by(id=teach_id).first()
        if not teach:
            return marshal({'message':'Ministrante não encontrado'}, message), 404
        try:
            db.session.delete(user)
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(teach, teach_admin_field), 201


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