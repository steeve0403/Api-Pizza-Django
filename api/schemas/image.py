from ninja import Schema
from pydantic import validator


class ImageSchema(Schema):
    id: int
    image: str
    description: str = ""
    is_default: bool = False
    thumbnail: str = None  # Ajout du champ pour la miniature

    @validator('image')
    def validate_image_path(cls, value):
        if not value.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
            raise ValueError("Invalid image format. Allowed formats: .jpg, .jpeg, .png, .gif")
        return value

    @validator('description')
    def validate_description(cls, value):
        if len(value.strip()) == 0:
            raise ValueError("Description cannot be empty")
        return value
