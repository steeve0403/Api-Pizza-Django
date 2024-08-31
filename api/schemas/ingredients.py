from ninja import Schema
from pydantic import validator
from enum import Enum

from api.schemas.image import ImageSchema

class IngredientType(str, Enum):
    vegetable = 'vegetable'
    meat = 'meat'
    dairy = 'dairy'
    other = 'other'


class IngredientCreateSchema(Schema):
    name: str
    description: str
    type: IngredientType
    allergens: str = ''
    images: list[int] = []

    @validator('allergens', pre=True, always=True)
    def validate_allergens(cls, value):
        if isinstance(value, str):
            return [allergen.strip() for allergen in value.split(',')]
        return value


class IngredientUpdateSchema(Schema):
    name: str = None
    description: str = None
    type: IngredientType = None
    allergens: str = None
    images: list[int] = None


class IngredientSchema(Schema):
    id: int
    name: str
    description: str
    type: IngredientType
    allergens: str
    images: list[ImageSchema] = []

    @validator('allergens', pre=True, always=True)
    def validate_allergens(cls, value):
        if isinstance(value, str):
            return [allergen.strip for allergen in value.split(',')]
        return value



