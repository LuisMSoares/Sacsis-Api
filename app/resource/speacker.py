from flask_restful import Resource, fields, marshal, request
from app.db import db, SpeakerModel, CourseModel, LectureModel
from app.resource import message


def SpeakerReg(rjson):
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


class CourseResource(Resource):
    def post(self):
        # Cadastro de ministrante
        speaker = SpeakerReg(rjson=request.json)
        if not speaker[0]:
            return marshal(
                {'message':'Ocorreu um erro ao adicionar as informações do ministrante!'}, 
                message), 422
        speaker = speaker[1]

        # Cadastro de Minicurso
        course = CourseModel(
            titulo = request.json['titulo'],
            conteudo = request.json['conteudo'],
            speaker = speaker
        )
        course.set_created_data()
        db.session.add(course)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao cadastrar o minicurso!'}, message), 422
        return marshal({'message':'Minicurso cadastrado com sucesso.'}, message), 201


class LectureResource(Resource):   
    def post(self):
        # Cadastro de ministrante
        speaker = SpeakerReg(rjson=request.json)
        if not speaker[0]:
            return marshal(
                {'message':'Ocorreu um erro ao adicionar as informações do ministrante!'}, 
                message), 422
        speaker = speaker[1]

        # Cadastro de Minicurso
        lecture = LectureModel(
            titulo = request.json['titulo'],
            conteudo = request.json['conteudo'],
            speaker = speaker
        )
        lecture.set_created_data()
        db.session.add(lecture)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return marshal({'message':'Ocorreu um erro ao cadastrar a palestra!'}, message), 422
        return marshal({'message':'Palestra cadastrada com sucesso.'}, message), 201
