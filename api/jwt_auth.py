from typing import Optional, Any

import jwt
from django.conf import settings
from django.http import HttpRequest
from ninja.security import HttpBearer
from ninja.errors import AuthenticationError

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token is expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")


jwt_auth = JWTAuth()