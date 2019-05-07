from app import mail
from app.services import Token
from flask_mail import Message


class SendEmail:
    def user_confirm(app, title, email, link):
        with app.app_context():
            try:
                msg = Message(title, recipients=[email])
                link = link.replace('token', Token.generate(email))
                msg.html = f'Clique <a href="{link}">aqui</a> para confirmar seu cadastro.'
                mail.send(msg)
            except:
                ...

    def reset_password(app, title, email, password):
        with app.app_context():
            try:
                msg = Message(title, recipients=[email])
                msg.body = f'Utilize sua senha temporaria para acessar o sistema: {password}'
                mail.send(msg)
            except:
                ...
