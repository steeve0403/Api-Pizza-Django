from typing import Optional

from ninja import Schema
from pydantic import conlist, validator

from ..models.pizza import Pizza
from ..schemas.category import CategorySchema
from ..schemas.image import ImageSchema
from ..schemas.ingredients import IngredientCreateSchema, IngredientSchema


class PizzaCreateSchema(Schema):
    name: str
    description: str
    price: float
    vegetarian: bool
    available: bool
    ingredients: conlist(int, min_length=3)
    categories: list[int] = []
    custom_images: list[int] = []

    @validator('price')
    def check_price(cls, value):
        if value <= 0:
            raise ValueError("Price must be positive")
        return value

    @validator('ingredients')
    def check_ingredients(cls, value):
        if len(value) < 3:
            raise ValueError("A pizza must have at least 3 ingredients.")
        return value


class PizzaUpdateSchema(Schema):
    name: str = None
    description: str = None
    price: float = None
    vegetarian: bool = None
    available: bool = None
    ingredients: conlist(int, min_length=3) = None
    categories: list[int] = None
    default_image: int = None
    custom_images: list[int] = None

    @validator('price', pre=True, always=True)
    def check_price(cls, value):
        if value is not None and value <= 0:
            raise ValueError("Price must be positive")
        return value

    @validator('ingredients', pre=True, always=True)
    def check_ingredients(cls, value):
        if value is not None and len(value) < 3:
            raise ValueError("A pizza must have at least 3 ingredients.")
        return value


class PizzaSchema(Schema):
    id: int
    name: str
    description: str
    price: float
    vegetarian: bool
    available: bool
    ingredients: list[IngredientSchema] = []
    image: Optional[ImageSchema] = None
    categories: list[CategorySchema] = []

    class Config:
        orm_mode = True

