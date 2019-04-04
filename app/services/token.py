from os import environ
from itsdangerous import (
    URLSafeTimedSerializer, 
    SignatureExpired, 
    BadTimeSignature
)


class Token:
    @staticmethod
    def generate(email):
        serializer = URLSafeTimedSerializer( environ.get('TOKEN_KEY','Nyan_passu') )
        return serializer.dumps(email, salt='user-confirmation')

    @staticmethod
    def validate(token):
        serializer = URLSafeTimedSerializer( environ.get('TOKEN_KEY','Nyan_passu') )
        try:
            email = serializer.loads(
                token,
                salt='user-confirmation'
            )
        except BadTimeSignature:
            return (False, {'message': 'Token informado invalido!'})
        return (True, email)