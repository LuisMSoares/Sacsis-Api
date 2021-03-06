from flask_restful import Resource, fields, marshal, request
from app.db import db, SpeakerModel, CourseModel, LectureModel, TokenBlacklistModel
from app.resource import message, admin_required, jsonGet
from app.services import Token
from datetime import datetime
from io import BytesIO
from PIL import Image
import base64

token_field = {
    'route_type' : fields.String,
    'expiration_days' : fields.Integer,
    'token' : fields.String
}


class SpeakerResource(Resource):
    @admin_required
    def get(self):
        route_type = request.args.get('type', None)
        expiration_days = self.limit_time(int(request.args.get('expiration', 7)))
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

    def post(self):
        token = request.args.get('token', None)
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
        # realiza o cadastro dos dados do ministrante
        rjson = request.json
        avatar = self.ImagetoBytes( rjson['avatar'] )
        if token_data['route_type'] == 'lecture' == rjson['type_form']:
            return self.LectureReg(rjson, avatar, token)
        elif token_data['route_type'] == 'course' == rjson['type_form']:
            return self.CourseReg(rjson, avatar, token)
        return marshal({'message':'Token invalido para este tipo de formulario!'}, message), 401


    #------------------------------------------------------------------------------------------------
    def ImagetoBytes(self, avatar):
        # Converte uma imagem de base64 em bytes
        file64 = avatar[avatar.find(',')+1:]
        fileBytes = bytes(file64, encoding="ascii")
        fileAvatar = Image.open(BytesIO(base64.b64decode(fileBytes)))
        # cria um buffer da imagem
        bufferAvatar = BytesIO()
        fileAvatar.save(bufferAvatar, format='png')
        return bufferAvatar.getvalue()

    def CourseReg(self, rjson, avatar, token=None):
        # Cadastro de ministrante
        speaker = self.SpeakerReg(rjson, avatar)
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

    def LectureReg(self, rjson, avatar, token=None):
        # Cadastro de ministrante
        speaker = self.SpeakerReg(rjson, avatar)
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

    def SpeakerReg(self, rjson, avatar):
        def set_speaker_data(rjson, speakerObj=SpeakerModel()):
            speakerObj.nome = rjson['nome']
            speakerObj.resumo = rjson['resumo']
            speakerObj.rg = rjson['rg']
            speakerObj.cpf = rjson['cpf']
            speakerObj.email = rjson['email']
            speakerObj.telefone = rjson['telefone']
            # optional values
            speakerObj.facebook = jsonGet(rjson, 'facebook')
            speakerObj.twitter = jsonGet(rjson, 'twitter')
            speakerObj.instagram = jsonGet(rjson,'instagram')
            speakerObj.site = jsonGet(rjson, 'site')
            return speakerObj
        
        speaker = SpeakerModel.query.filter_by(cpf=rjson['cpf']).first()
        if not speaker:
            speaker = set_speaker_data(rjson)
            speaker.set_created_data()
            speaker.set_avatar(avatar, 'avatar.png')
            db.session.add(speaker)
        else:
            speaker = set_speaker_data(rjson, speakerObj=speaker)
            speaker.set_avatar(avatar, 'avatar.png')
        try:
            db.session.commit()
            return (True, speaker)
        except:
            db.session.rollback()
            return (False,)
            
    def limit_time(self, x):
        return 1 if x<=0 else 7 if x>7 else x
        
    def TokenBlacklist(self, token):
        blacklist = TokenBlacklistModel(token=token)
        try:
            db.session.add(blacklist)
            db.session.commit()
        except:
            db.session.rollback()