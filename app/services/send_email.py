from app import mail
from app.services import ValidateUser 
from flask_mail import Message
from os import environ


class SendEmail:
    secret_key = environ.get('','Nyan_passu')

    def user_confirm(title, email):
        msg = Message(title, recipients=email)
        token = ValidateUser.token_generate(email)
        msg.body = f'''Clique no link abaixo para confirmar seu cadastro
        {token}
        '''