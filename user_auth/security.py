import jwt
from django.conf import settings
from ninja.security import HttpBearer
from ninja.errors import HttpError

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.JWT_SETTINGS['SIGING_KEY'], algorithms=[settings.JWT_SETTINGS['ALGORITHM']])
            return payload
        except jwt.ExpiredSignatureError:
            raise HttpError(401, "Token has expired")
        except jwt.InvalidTokenError:
            raise HttpError(401, "Token is invalid")
