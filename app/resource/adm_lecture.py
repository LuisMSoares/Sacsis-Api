from flask_restful import Resource, request, fields, marshal
from app.db import db, LectureModel
from app.resource import message, admin_required

lecture_field = {
    'id': fields.Integer,
    'titulo': fields.String,
    'conteudo': fields.String,
    'ministrante': fields.String(attribute=lambda obj: obj.speaker.nome)
}
remove_lecture_field = {
    'id': fields.Integer,
    'titulo': fields.String,
    'conteudo': fields.String
}
load_title_field = {
    'id': fields.Integer,
    'titulo': fields.String,
    'ministrante': fields.String(attribute=lambda obj: obj.speaker.nome)
}


class LectureAdminResource(Resource):
    @admin_required
    def get(self, lecture_id=None):
        loadtitle = int(request.args.get('loadtitle', 0))
        if int(loadtitle) == 1:
            lectures = LectureModel.query.order_by(LectureModel.id).all()
            lectures = [marshal(l,load_title_field) for l in lectures]
            return {'values': lectures}, 200
        if lecture_id:
            lecture = LectureModel.query.filter_by(id=lecture_id).first()
            if not lecture:
                return marshal({'message':'Palestra inexistente'}, message), 404
            return marshal(lecture, lecture_field)
        else:
            lectures = LectureModel.query.order_by(LectureModel.id).all()
            if len(lectures) == 0:
                return marshal({'message':'Nenhum palestra cadastrado encontrado'}, message), 404
            format_lectures = [marshal(c, lecture_field) for c in lectures]
            return {'quantidade': len(format_lectures),'palestras': format_lectures}, 200

    @admin_required
    def put(self):
        lecture = LectureModel.query.filter_by(id=request.json['id']).first()
        if not lecture:
            return marshal({'message':'Palestra inexistente'}, message), 404
        if 'titulo' in request.json:
            lecture.titulo = request.json['titulo']
        if 'conteudo' in request.json:
            lecture.conteudo = request.json['conteudo']
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(lecture, lecture_field)

    @admin_required
    def delete(self, lecture_id=None):
        if not lecture_id:
            return marshal({'message':'Informe o id do palestra'}, message), 404
        lecture = LectureModel.query.filter_by(id=lecture_id).first()
        try:
            db.session.delete(lecture)
        except:
            db.session.rollback()
            return marshal({'message':'Erro interno'}, message), 500
        else:
            return marshal(lecture, remove_lecture_field)
