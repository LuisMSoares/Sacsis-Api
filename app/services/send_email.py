from app import mail
from app.services import Token
from flask_mail import Message
from flask_restful import url_for
#from app.resource import ActiveAccountResource
from os import environ


class SendEmail:
    secret_key = environ.get('','Nyan_passu')

    def user_confirm(title, email, link):
        msg = Message(title, recipients=[email])
        link = link.replace('token', Token.generate(email))
        msg.body = f'''Clique no link abaixo para confirmar seu cadastro
        {link}
        '''
        mail.send(msg)

    def reset_password(title, email, password):
        msg = Message(title, recipients=[email])
        msg.body = f'''
        Utilize o token abaixo para logar no sistema.
        Token de acesso: {password}

        (insira como uma senha)
        '''
        mail.send(msg)
