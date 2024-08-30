from ninja import Schema
from pydantic import validator

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
    ingredients: list[IngredientCreateSchema]
    categories: list[int] = []
    custom_images: list[int] = []

    @validator('price')
    def check_price(cls, v):
        if v <= 0:
            raise ValueError("Price must be positive")
        return v

    @validator('ingredients')
    def check_ingredients(cls, v):
        if len(v) < 3:
            raise ValueError("A pizza must have at least 3 ingredients.")
        return v


class PizzaUpdateSchema(Schema):
    name: str = None
    description: str = None
    price: float = None
    vegetarian: bool = None
    available: bool = None
    ingredients: list[int] = None  # IDs des ingrédients
    categories: list[int] = None  # IDs des catégories
    default_image: int = None  # ID de l'image par défaut
    custom_images: list[int] = None  # IDs des images personnalisées

    @validator('price', pre=True, always=True)
    def check_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Price must be positive")
        return v

    @validator('ingredients', pre=True, always=True)
    def check_ingredients(cls, v):
        if v is not None and len(v) < 3:
            raise ValueError("A pizza must have at least 3 ingredients.")
        return v


class PizzaSchema(Schema):
    id: int
    name: str
    description: str
    price: float
    vegetarian: bool
    available: bool
    ingredients: list[IngredientSchema] = []
    image: ImageSchema
    categories: list[CategorySchema] = []

    @staticmethod
    def from_orm(obj: Pizza):
        return PizzaSchema(
            id=obj.id,
            name=obj.name,
            description=obj.description,
            price=obj.price,
            vegetarian=obj.vegetarian,
            available=obj.available,
            ingredients=obj.ingredients,
            image=ImageSchema.from_orm(obj.get_image())
        )

