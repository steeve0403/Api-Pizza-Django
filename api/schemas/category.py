from ninja import Schema
from typing import Optional, List
from pydantic import validator


class CategorySchema(Schema):
    id: int
    name: str
    description: Optional[str] = ""
    is_active: bool
    is_deleted: bool
    parent_id: Optional[int] = None
    children: List['CategorySchema'] = []  # Gestion des sous-catégories
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True


class CategoryCreateSchema(Schema):
    name: str
    description: Optional[str] = ""
    parent_id: Optional[int] = None
    is_active: bool = True

    @validator('name')
    def validate_name(cls, value):
        if len(value.strip()) == 0:
            raise ValueError("Name cannot be empty")
        return value


class CategoryUpdateSchema(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None
