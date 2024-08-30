from ninja import Schema


class ImageSchema(Schema):
    id: int
    image: str
    description: str
