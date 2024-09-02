import jwt
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from ninja import Router
from ninja.errors import HttpError
from .models import CustomUser, RefreshToken, APIKey, UserActivityLog, ServicePlan, UserSession, UserNotification
from .schemas import UserSchema, UserCreateSchema, TokenSchema, RefreshTokenSchema, APIKeySchema, UserActivityLogSchema, \
    UserSessionSchema, UserNotificationSchema, ServicePlanSchema

router = Router()


def log_user_activity(user, action, request):
    UserActivityLog.objects.create(
        user=user,
        action=action,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT'),
    )


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


@router.post("/", response=UserSchema)
def register(request, data: UserCreateSchema):
    if CustomUser.objects.filter(username=data.username).exists():
        raise HttpError(400, "Username already taken")
    if CustomUser.objects.filter(email=data.email).exists():
        raise HttpError(400, "Email already taken")

    user = CustomUser.objects.create_user(
        username=data.username,
        password=make_password(data.password),
        email=data.email,
        service_plan=ServicePlan.objects.get(name='free')  # Associer un plan par défaut
    )
    log_user_activity(user, 'register', request)
    return user


@router.post("/", response=TokenSchema)
def login(request, data: UserSessionSchema):
    user = authenticate(username=data.username, password=data.password)
    if not user:
        raise HttpError(401, "Invalid credentials")

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user)
    log_user_activity(user, 'login', request)

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh", response=TokenSchema)
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
        log_user_activity(refresh_token_obj.user, 'token_refresh', request)

        return {"access_token": access_token, "refresh_token": new_refresh_token}
    except jwt.ExpiredSignatureError:
        raise HttpError(401, "Refresh token has expired")
    except jwt.InvalidTokenError:
        raise HttpError(401, "Invalid token")


@router.post("/")
def logout(request, data: RefreshTokenSchema):
    try:
        refresh_token_obj = RefreshToken.objects.get(token=data.refresh_token)
        refresh_token_obj.revoked = True
        refresh_token_obj.save()
        log_user_activity(refresh_token_obj.user, 'logout', request)
        return {"detail": "Successfully logged out"}
    except RefreshToken.DoesNotExist:
        raise HttpError(401, "Invalid refresh token")


# Gestion des clés API
@router.post("/", response=APIKeySchema)
def create_api_key(request):
    user = request.user
    if APIKey.objects.filter(user=user, is_active=True).count() >= user.service_plan.max_api_keys:
        raise HttpError(400, "API key limit reached")

    api_key = APIKey.objects.create(user=user)
    log_user_activity(user, 'api_key_creation', request)
    return api_key


@router.get("/", response=list[APIKeySchema])
def list_api_keys(request):
    return APIKey.objects.filter(user=request.user, is_active=True)


@router.delete("/{key_id}", response=dict)
def revoke_api_key(request, key_id: int):
    api_key = APIKey.objects.filter(id=key_id, user=request.user).first()
    if not api_key:
        raise HttpError(404, "API key not found")
    api_key.is_active = False
    api_key.save()
    log_user_activity(request.user, 'api_key_revoke', request)
    return {"detail": "API key revoked"}


# Gestion des sessions utilisateur
@router.get("/", response=list[UserSessionSchema])
def list_sessions(request):
    return UserSession.objects.filter(user=request.user, expires_at__gt=datetime.now())


@router.delete("/{session_id}", response=dict)
def revoke_session(request, session_id: int):
    session = UserSession.objects.filter(id=session_id, user=request.user).first()
    if not session:
        raise HttpError(404, "Session not found")
    session.expires_at = datetime.now()  # Marquer comme expirée
    session.save()
    log_user_activity(request.user, 'session_revoke', request)
    return {"detail": "Session revoked"}


# Gestion des notifications utilisateur
@router.get("/notifications", response=list[UserNotificationSchema])
def list_notifications(request):
    return UserNotification.objects.filter(user=request.user)


@router.post("/notifications/mark-as-read/{notification_id}", response=dict)
def mark_notification_as_read(request, notification_id: int):
    notification = UserNotification.objects.filter(id=notification_id, user=request.user).first()
    if not notification:
        raise HttpError(404, "Notification not found")
    notification.is_read = True
    notification.save()
    log_user_activity(request.user, 'notification_read', request)
    return {"detail": "Notification marked as read"}


# Gestion des plans de service
@router.get("/service-plans", response=list[ServicePlanSchema])
def list_service_plans(request):
    return ServicePlan.objects.all()


@router.post("/change-plan/{plan_id}", response=UserSchema)
def change_service_plan(request, plan_id: int):
    user = request.user
    plan = ServicePlan.objects.get(id=plan_id)
    user.service_plan = plan
    user.save()
    log_user_activity(user, 'change_service_plan', request)
    return user
