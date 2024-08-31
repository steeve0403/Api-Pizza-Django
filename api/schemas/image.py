from ninja import Schema
from pydantic import validator, ValidationError


class ImageSchema(Schema):
    id: int
    image: str
    description: str

    @validator('image')
    def validate_image_path(cls, value):
        if not value.endswith(('.jpg', 'jpeg', 'png')):
            raise ValidationError("Invalid image format")
        return value