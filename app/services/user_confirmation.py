from os import environ
from itsdangerous import (
    URLSafeTimedSerializer, 
    SignatureExpired, 
    BadTimeSignature
)


class ValidateUser:
    secret_key = environ.get('USER_CONFIRM_TOKEN_KEY','Nyan_passu')
    token_age = int(environ.get('USER_CONFIRM_TOKEN_AGE', 60*60*24))
    serializer = URLSafeTimedSerializer(secret_key)

    @staticmethod
    def token_generate(email):
        return serializer.dumps(email, salt='user-confirmation')

    @staticmethod
    def token_validation(token):
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