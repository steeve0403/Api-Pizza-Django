from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional
import re


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    date_joined: str
    is_active: bool
    tier: str

    class Config:
        orm_mode = True


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


class UserLoginSchema(BaseModel):
    username: str
    password: str


class UserUpdateSchema(BaseModel):
    username: constr(min_length=8, max_length=20) = None
    email: EmailStr = None
    password: constr(min_length=8) = None
    tier: str = None


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


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"


class APIUsageSchema(BaseModel):
    usage_quota: int
    request_count: int
    last_request_time: str
    tier: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str
