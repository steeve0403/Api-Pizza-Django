import jwt
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from ninja import Router
from ninja.errors import HttpError

from .models import CustomUser, RefreshToken
from .schemas import UserSchema, UserCreateSchema, UserLoginSchema, TokenSchema, RefreshTokenSchema

router = Router()


def create_access_token(user_id: int):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + settings.JWT_SETTINGS['ACCESS_TOKEN_LIFETIME'],
        'iat': datetime.utcnow(),
    }
    return jwt.encode(payload, settings.JWT_SETTINGS['SECRET_KEY'])


def create_refresh_token(user):
    token = jwt.encode({
        'user_id': user.id,
        'exp': datetime.utcnow() + settings.JWT_SETTINGS['REFRESH_TOKEN_LIFETIME'],
        'iat': datetime.utcnow(),
    }, settings.JWT_SETTINGS['SECRET_KEY'], algorithm=settings.JWT_SETTINGS['ALGORITHM'])
    RefreshToken.objects.create(user=user, token=token)
    return token


@router.post("/register", response=UserSchema)
def register(request, data: UserCreateSchema):
    if CustomUser.objects.filter(username=data.username).exists():
        raise HttpError(400, "Username already taken")
    if CustomUser.objects.filter(email=data.email).exists():
        raise HttpError(400, "Email already taken")

    user = CustomUser.objects.create_user(
        username=data.username,
        password=make_password(data.password),
        email=data.email,
    )
    return user


@router.post("/login", response=TokenSchema)
def login(request, data: UserLoginSchema):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        raise HttpError(401, "Invalid credentials")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/token/refresh", response=TokenSchema)
def token_refresh(request, data: RefreshTokenSchema):
    try:
        payload = jwt.decode(data.refresh_token, settings.JWT_SETTINGS['SIGNING_KEY'],
                             algorithms=[settings.JWT_SETTINGS['ALGORITHM']])
        refresh_token_obj = RefreshToken.objects.filter(token=data.refresh_token, revoked=False).first()
        if not refresh_token_obj or payload['user_id'] != refresh_token_obj.user_id:
            raise HttpError(401, "Invalid refresh token")

        refresh_token_obj.revoked = True
        refresh_token_obj.save()

        new_refresh_token = create_refresh_token(refresh_token_obj.user)

        access_token = create_access_token(payload['user_id'])
        return {"access_token": access_token, "refresh_token": new_refresh_token}
    except jwt.ExpiredSignatureError:
        raise HttpError(401, "Refresh token has expired")
    except jwt.InvalidTokenError:
        raise HttpError(401, "Invalid token")


@router.post("/logout")
def logout(request, data: RefreshTokenSchema):
    try:
        refresh_token_obj = RefreshToken.objects.get(token=data.refresh_token)
        refresh_token_obj.revoked = True
        refresh_token_obj.save()
        return {"detail": "Successfully logged out"}
    except RefreshToken.DoesNotExist:
        raise HttpError(401, "Invalid refresh token")
