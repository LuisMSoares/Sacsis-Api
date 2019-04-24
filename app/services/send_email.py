from app import mail
from app.services import Token
from flask_mail import Message
from os import environ


class SendEmail:
    def user_confirm(app, title, email, link):
        with app.app_context():
            try:
                msg = Message(title, recipients=[email])
                link = link.replace('token', Token.generate(email))
                msg.body = f'''Clique no link abaixo para confirmar seu cadastro
                {link}
                '''
                mail.send(msg)
            except:
                ...

    def reset_password(app, title, email, password):
        with app.app_context():
            try:
                msg = Message(title, recipients=[email])
                msg.body = f'''
                Utilize o token abaixo para logar no sistema.
                Token de acesso: {password}

                (insira como uma senha)
                '''
                mail.send(msg)
            except:
                ...
