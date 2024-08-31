from pydantic import BaseModel, EmailStr, constr
from typing import Optional


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