import jwt
from django.conf import settings
from ninja.security import HttpBearer
from ninja.errors import HttpError
from .models import RefreshToken

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.JWT_SETTINGS['SIGNING_KEY'], algorithms=[settings.JWT_SETTINGS['ALGORITHM']])
            if RefreshToken.objects.filter(token=token, revoked=True).exists():
                raise HttpError(401, "Token has been revoked")
            return payload
        except jwt.ExpiredSignatureError:
            raise HttpError(401, "Token has expired")
        except jwt.InvalidTokenError:
            raise HttpError(401, "Token is invalid")
