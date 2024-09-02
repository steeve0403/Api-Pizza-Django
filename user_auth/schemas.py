from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional, List
import re


# Schéma pour les plans de service
class ServicePlanSchema(BaseModel):
    id: int
    name: str
    max_requests_per_day: int
    max_api_keys: int
    price: float
    description: str

    class Config:
        orm_mode = True


# Schéma pour les utilisateurs
class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    date_joined: str
    is_active: bool
    tier: str
    service_plan: Optional[ServicePlanSchema]
    api_key: str
    api_key_expires_at: str
    usage_quota: int
    last_request_time: Optional[str]
    request_count: int
    last_login_ip: Optional[str]
    last_login_device: Optional[str]

    class Config:
        orm_mode = True


# Schéma pour la création d'utilisateurs
class UserCreateSchema(BaseModel):
    username: constr(min_length=8, max_length=20)
    email: EmailStr
    password: constr(min_length=8)

    @validator('username')
    def validate_username(cls, value):
        if not re.match(r"^[a-zA-Z0-9_]+$", value):
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return value

    @validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r"[A-Z]", value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r"[a-z]", value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r"\d", value):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError('Password must contain at least one special character')
        return value


# Schéma pour la mise à jour des utilisateurs
class UserUpdateSchema(BaseModel):
    username: constr(min_length=8, max_length=20) = None
    email: EmailStr = None
    password: constr(min_length=8) = None
    tier: str = None
    service_plan: Optional[int] = None  # ID du plan de service


# Schéma pour le changement de mot de passe
class PasswordChangeSchema(BaseModel):
    old_password: str
    new_password: constr(min_length=8)

    @validator('new_password')
    def validate_new_password(cls, value):
        if len(value) < 8:
            raise ValueError('New password must be at least 8 characters long')
        if not re.search(r"[A-Z]", value):
            raise ValueError('New password must contain at least one uppercase letter')
        if not re.search(r"[a-z]", value):
            raise ValueError('New password must contain at least one lowercase letter')
        if not re.search(r"\d", value):
            raise ValueError('New password must contain at least one digit')
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError('New password must contain at least one special character')
        return value


# Schéma pour les tokens
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


# Schéma pour l'usage de l'API
class APIUsageSchema(BaseModel):
    usage_quota: int
    request_count: int
    last_request_time: str
    tier: str


# Schéma pour le token de rafraîchissement
class RefreshTokenSchema(BaseModel):
    refresh_token: str


# Schéma pour les logs d'activités utilisateur
class UserActivityLogSchema(BaseModel):
    user_id: int
    action: str
    timestamp: str
    ip_address: Optional[str]
    user_agent: Optional[str]

    class Config:
        orm_mode = True


# Schéma pour les sessions utilisateur
class UserSessionSchema(BaseModel):
    user_id: int
    session_token: str
    created_at: str
    last_activity: str
    expires_at: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    is_expired: bool

    class Config:
        orm_mode = True


# Schéma pour les clés API
class APIKeySchema(BaseModel):
    user_id: int
    key: str
    created_at: str
    expires_at: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True


# Schéma pour les notifications utilisateur
class UserNotificationSchema(BaseModel):
    user_id: int
    message: str
    created_at: str
    is_read: bool

    class Config:
        orm_mode = True


# Schéma pour l'archivage des utilisateurs
class ArchivedUserSchema(BaseModel):
    original_user_id: int
    archived_data: dict
    archived_at: str

    class Config:
        orm_mode = True
