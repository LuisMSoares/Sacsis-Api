from functools import wraps
from flask_restful import fields, marshal
from app.db import UserModel
from flask_jwt_extended import ( 
    verify_jwt_in_request, verify_jwt_in_request, get_jwt_identity
)
from flask_jwt_extended.exceptions import ( 
    InvalidHeaderError, NoAuthorizationError 
)

message = {
    'message': fields.String
}


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except InvalidHeaderError:
            return marshal({'message':'Token de autenticação invalido!'}, message), 422
        except NoAuthorizationError:
            return marshal({'message':'Token de autenticação não encontrado!'}, message), 422
        user = UserModel.query.filter_by(id=get_jwt_identity()).first()
        if not user:
            return marshal({'message':'Acesso restrito!'}, message), 403
        if user.admin:
            return fn(*args, **kwargs)
        else:
            return marshal({'message':'Acesso restrito!'}, message), 403
    return wrapper


def jwt_token_required_custom(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except InvalidHeaderError:
            return marshal({'message':'Token de autenticação invalido!'}, message), 422
        except NoAuthorizationError:
            return marshal({'message':'Token de autenticação não encontrado!'}, message), 422
        return fn(*args, **kwargs)
    return wrapper


from app.resource.adm_user import UserAdminResource
from app.resource.adm_speaker import SpeakerAdminResource
from app.resource.adm_courses import CourseAdminResource
from app.resource.adm_lecture import LectureAdminResource

from app.resource.users import UserResource
from app.resource.speacker import SpeakerResource

from app.resource.login import LoginResource
from app.resource.account import ResetPasswordResource