from flask_restful import Resource, fields, marshal, request
from app.db import db, SpeakerModel, CourseModel, LectureModel, TokenBlacklistModel
from app.resource import message, admin_required
from datetime import datetime
from app.services import Token

token_field = {
    'route_type' : fields.String,
    'expiration_days' : fields.Integer,
    'token' : fields.String
}


class SpeakerResource(Resource):
    @admin_required
    def get(self):
        route_type = request.args.get('type', None)
        expiration_days = self.limit_time(int(request.args.get('expiration', 0)))
        expiration_time = int(datetime.now().timestamp()) + expiration_days * 86400
        if route_type == None:
            return marshal({'message':'Tipo de rota não encontrado.'}, message), 404
        elif route_type == 'lecture':
            token = Token.generate( {'route_type':route_type, 'expiration':expiration_time} )
        elif route_type == 'course':
            token = Token.generate( {'route_type':route_type, 'expiration':expiration_time} )
        else:
            return marshal({'message':'Tipo de rota invalido.'}, message), 404
        response = {'route_type':route_type, 'expiration_days':expiration_days, 'token':token}
        return marshal(response, token_field), 201


    def post(self, token=None):
        # verifica a validade do token
        token_bl = TokenBlacklistModel.query.filter_by(token=token).first()
        if token_bl:
            return marshal({'message':'Token informado já foi utilizado!'}, message), 401
        if not token:
            return marshal({'message':'Informe um token valido!'}, message), 401
        token_status, token_data = Token.validate(token)
        if not token_status:
            return marshal(token_data, message), 401
        if int(datetime.now().timestamp()) > token_data['expiration']:
            return marshal({'message':'Token informado expirado!'}, message), 401
        elif token_data['route_type'] == 'lecture' == request.json['type_form']:
            return self.LectureReg(rjson=request.json ,token=token)
        elif token_data['route_type'] == 'course' == request.json['type_form']:
            return self.CourseReg(rjson=request.json ,token=token)
        return marshal({'message':'Token invalido para este tipo de formulario!'}, message), 401


    def CourseReg(self, rjson, token=None):
        # Cadastro de ministrante
        speaker = self.SpeakerReg(rjson=rjson)
        if not speaker[0]:
            return marshal(
                {'message':'Ocorreu um erro ao adicionar as informações do ministrante!'}, 
                message), 422
        speaker = speaker[1]

        # Cadastro de Minicurso
        course = CourseModel(
            titulo = rjson['titulo'],
            conteudo = rjson['conteudo'],
            speaker = speaker
        )
        course.set_created_data()
        db.session.add(course)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao cadastrar o minicurso!'}, message), 422
        self.TokenBlacklist(token=token)
        return marshal({'message':'Minicurso cadastrado com sucesso.'}, message), 201


    def LectureReg(self, rjson, token=None):
        # Cadastro de ministrante
        speaker = self.SpeakerReg(rjson=rjson)
        if not speaker[0]:
            return marshal(
                {'message':'Ocorreu um erro ao adicionar as informações do ministrante!'}, 
                message), 422
        speaker = speaker[1]

        # Cadastro de Minicurso
        lecture = LectureModel(
            titulo = rjson['titulo'],
            conteudo = rjson['conteudo'],
            speaker = speaker
        )
        lecture.set_created_data()
        db.session.add(lecture)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao cadastrar a palestra!'}, message), 422
        self.TokenBlacklist(token=token)
        return marshal({'message':'Palestra cadastrada com sucesso.'}, message), 201


    def limit_time(self, x):
        return 1 if x<=0 else 3 if x>3 else x
        
    def TokenBlacklist(self, token):
        blacklist = TokenBlacklistModel(token=token)
        try:
            db.session.add(blacklist)
            db.session.commit()
        except:
            db.session.rollback()

    def SpeakerReg(self, rjson):
        def set_speaker_data(rjson, speakerObj=SpeakerModel()):
            speakerObj.nome = rjson['nome']
            speakerObj.resumo = rjson['resumo']
            speakerObj.rg = rjson['rg']
            speakerObj.cpf = rjson['cpf']
            speakerObj.facebook = rjson['facebook'] or ''
            speakerObj.twitter = rjson['twitter'] or ''
            speakerObj.instagram = rjson['instagram'] or ''
            speakerObj.site = rjson['site'] or ''
            speakerObj.set_gravatar( rjson['gravatar'] )
            return speakerObj
        speaker = SpeakerModel.query.filter_by(cpf=rjson['cpf']).first()
        if not speaker:
            speaker = set_speaker_data(rjson=rjson)
            speaker.set_created_data()
            db.session.add(speaker)
        else:
            speaker = set_speaker_data(rjson=rjson, speakerObj=speaker)
        try:
            db.session.commit()
            return (True, speaker)
        except:
            db.session.rollback()
            return (False,)
