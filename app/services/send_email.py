from app import mail
from app.services import Token
from flask_mail import Message
from os import environ


class SendEmail:
    secret_key = environ.get('','Nyan_passu')

    def user_confirm(title, email):
        msg = Message(title, recipients=email)
        token = Token.generate(email)
        msg.body = f'''Clique no link abaixo para confirmar seu cadastro
        {token}
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
