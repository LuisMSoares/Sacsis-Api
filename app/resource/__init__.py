from flask_restful import fields

message = {
    'message': fields.String
}

from app.resource.users import UserResource
from app.resource.login import LoginResource