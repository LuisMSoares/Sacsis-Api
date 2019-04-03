from os import environ
from itsdangerous import (
    URLSafeTimedSerializer, 
    SignatureExpired, 
    BadTimeSignature
)


class Token:
    secret_key = environ.get('TOKEN_KEY','Nyan_passu')
    token_age = int(environ.get('TOKEN_AGE', 60*60*24))
    serializer = URLSafeTimedSerializer(secret_key)

    @staticmethod
    def generate(email):
        return serializer.dumps(email, salt='user-confirmation')

    @staticmethod
    def validate(token):
        try:
            email = serializer.loads(
                token,
                salt='user-confirmation',
                max_age=token_age
            )
        except SignatureExpired:
            return (False, {'message': 'Token expirado!'})
        except BadTimeSignature:
            return (False, {'message': 'Token invalido!'})
        return (True, email)