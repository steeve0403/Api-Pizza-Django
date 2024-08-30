from ninja import Schema
from pydantic import validator

from api.schemas.image import ImageSchema


class IngredientCreateSchema(Schema):
    name: str
    description: str
    type: str
    allergens: str = ''
    images: list[int] = []


class IngredientUpdateSchema(Schema):
    name: str = None
    description: str = None
    type: str = None
    allergens: str = None
    images: list[int] = None


class IngredientSchema(Schema):
    id: int
    name: str
    description: str
    type: str
    allergens: str
    images: list[ImageSchema] = []

    @validator('allergens', pre=True, always=True)
    def validate_allergens(cls, value):
        if not value:
            return ''
        if ', ' not in value:
            raise ValueError("'allergens' must be a comma-separated list")
        return value

