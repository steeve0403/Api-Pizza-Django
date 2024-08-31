import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from ninja import Router

from .models import RefreshToken
from .schemas import TokenSchema, UserLoginSchema
# Create your views here.
