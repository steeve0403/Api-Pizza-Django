from ninja import Schema

class CategorySchema(Schema):
    id: int
    name: str
    description: str

    class Config:
        orm_mode = True



