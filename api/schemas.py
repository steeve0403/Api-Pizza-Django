from ninja import Schema


class ImageSchema(Schema):
    id: int
    image: str
    description: str


class IngredientSchema(Schema):
    id: int
    name: str
    description: str
    images: list[ImageSchema] = []


class PizzaSchema(Schema):
    id: int
    name: str
    description: str
    price: float
    vegetarian: bool
    available: bool
    ingredients: list[IngredientSchema] = []
    default_image: ImageSchema = None
    custom_images: list[ImageSchema] = []
