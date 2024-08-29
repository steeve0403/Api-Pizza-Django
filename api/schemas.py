from ninja import Schema


class PizzaSchema(Schema):
    id: int = None
    name: str
    description: str
    price: float
    vegetarian: bool
    available: bool

class IngredientSchema(Schema):
    id: int = None
    name: str
    description: str