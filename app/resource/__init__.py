from functools import wraps
from flask_restful import fields, marshal
from app.db import UserModel
from flask_jwt_extended import ( 
    verify_jwt_in_request, verify_jwt_in_request, get_jwt_identity
)

message = {
    'message': fields.String
}

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = UserModel.query.filter_by(id=get_jwt_identity()).first()
        if not user:
            return marshal({'message':'Acesso restrito!'}, message), 403
        if user.admin:
            return fn(*args, **kwargs)
        else:
            return marshal({'message':'Acesso restrito!'}, message), 403
    return wrapper

#tempo maximo do token 35 minutos, validar a cada 30
def validate_token(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        user = UserModel.query.filter_by(id=get_jwt_identity()).first()
        if not user:
            return marshal({'message':'Acesso restrito!'}, message), 403
        if user.admin:
            return fn(*args, **kwargs)
        else:
            return marshal({'message':'Acesso restrito!'}, message), 403
    return wrapper



from app.resource.users import UserResource
from app.resource.login import LoginResource
from app.resource.adm_courses import CoursesResource
from app.resource.adm_user import UserAdminResource