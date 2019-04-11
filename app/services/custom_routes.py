from flask import jsonify, request, send_file
from io import BytesIO
from app.db import db, UserModel, SpeakerModel
from app.services import Token
from app import app


@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Route not found'}), 404


@app.route('/activate/<token>')
def activate_account(token):
    try:
        if not token:
            return '<h1> Token de validação não encontrado! </h1>'
        status, msg_mail = Token.validate(token)
        if status:
            user = UserModel.query.filter_by(email=msg_mail).first()
            user.activate_account()
            db.session.commit()
            return '<h1> Conta ativada com sucesso! </h1>'
        else:
            return f'<h1> {msg_mail} </h1>'
    except:
        return '<h1> Ocorreu um erro ao confirmar sua conta! </h1>'


@app.route('/speaker/images/<int:img_id>')
def get_image(img_id=None):
    if img_id:
        speaker = SpeakerModel.query.filter_by(id=img_id).first()
        return send_file(BytesIO(speaker.img_dados), 
                attachment_filename=speaker.img_nome, 
                as_attachment=False
        )
    return jsonify({'message': 'Id do ministrante não encontrado.'}), 404 