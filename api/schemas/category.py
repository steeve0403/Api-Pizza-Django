from ninja import Schema

class CategorySchema(Schema):
    id: int
    name: str
    description: str

