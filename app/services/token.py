from os import environ
from itsdangerous import (
    URLSafeTimedSerializer,
    BadTimeSignature,
    BadSignature
)


class Token:
    @staticmethod
    def generate(data):
        serializer = URLSafeTimedSerializer( environ.get('TOKEN_KEY','Nyan_passu') )
        return serializer.dumps(data, salt='#d%@iHl&')

    @staticmethod
    def validate(token):
        serializer = URLSafeTimedSerializer( environ.get('TOKEN_KEY','Nyan_passu') )
        try:
            data = serializer.loads(token, salt='#d%@iHl&')
        except (BadTimeSignature, BadSignature):
            return (False, {'message': 'Token informado invalido!'})
        return (True, data)