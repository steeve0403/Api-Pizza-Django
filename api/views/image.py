from django.shortcuts import get_object_or_404
from ninja import Router

from api.models.image import Image
from api.schemas.image import ImageSchema

router = Router()


@router.get("/", response=list[ImageSchema])
def list_images(request):
    return Image.objects.all()


@router.get("/{image_id}", response=ImageSchema)
def get_image(request, image_id: int):
    image = get_object_or_404(Image, id=image_id)
    return image


@router.put("/{image_id}", response=ImageSchema)
def update_image(request, image_id: int, data: ImageSchema):
    image = get_object_or_404(Image, id=image_id)
    for attr, value in data.dict().items():
        setattr(image, attr, value)
    image.save()
    return image


@router.delete("/{image_id}")
def delete_image(request, image_id: int):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return {"success": True}
