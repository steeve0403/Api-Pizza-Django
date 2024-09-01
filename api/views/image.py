from django.shortcuts import get_object_or_404
from ninja import Router
from django.db import transaction

from api.models.image import Image
from api.models.pizza import Pizza  # Importation pour l'association avec des pizzas
from api.schemas.image import ImageSchema
from api.exception import BadRequestError

router = Router()

@router.get("/", response=list[ImageSchema])
def list_images(request):
    images = Image.objects.filter(is_deleted=False)
    return images


@router.get("/{image_id}", response=ImageSchema)
def get_image(request, image_id: int):
    image = get_object_or_404(Image, id=image_id, is_deleted=False)
    return image


@router.post("/", response=ImageSchema)
@transaction.atomic
def create_image(request, data: ImageSchema):
    try:
        image = Image.objects.create(
            image=data.image,
            description=data.description,
            is_default=data.is_default
        )
        thumbnail_path = image.create_thumbnail()  # Supposant que la méthode existe dans le modèle
        image.thumbnail = thumbnail_path
        image.save()
        return image
    except Exception as e:
        raise BadRequestError(f"Failed to create image: {str(e)}")


@router.put("/{image_id}", response=ImageSchema)
@transaction.atomic
def update_image(request, image_id: int, data: ImageSchema):
    image = get_object_or_404(Image, id=image_id, is_deleted=False)
    for attr, value in data.dict().items():
        setattr(image, attr, value)
    image.save()
    return image


@router.delete("/{image_id}")
def delete_image(request, image_id: int):
    image = get_object_or_404(Image, id=image_id, is_deleted=False)
    image.delete()  # Suppression logique
    return {"success": True}


@router.post("/{image_id}/restore/", response=ImageSchema)
def restore_image(request, image_id: int):
    image = get_object_or_404(Image, id=image_id, is_deleted=True)
    image.is_deleted = False
    image.save()
    return image


@router.post("/{image_id}/associate_with_pizza/", response=ImageSchema)
def associate_image_with_pizza(request, image_id: int, pizza_id: int):
    image = get_object_or_404(Image, id=image_id, is_deleted=False)
    pizza = get_object_or_404(Pizza, id=pizza_id, is_deleted=False)
    pizza.custom_images.add(image)
    pizza.save()
    return image


@router.post("/{image_id}/dissociate_from_pizza/", response=ImageSchema)
def dissociate_image_from_pizza(request, image_id: int, pizza_id: int):
    image = get_object_or_404(Image, id=image_id, is_deleted=False)
    pizza = get_object_or_404(Pizza, id=pizza_id, is_deleted=False)
    pizza.custom_images.remove(image)
    pizza.save()
    return image


@router.get("/search/", response=list[ImageSchema])
def search_images(request, query: str):
    images = Image.objects.filter(description__icontains=query, is_deleted=False)
    return images


@router.get("/filter/", response=list[ImageSchema])
def filter_images(request, is_deleted: bool = None):
    if is_deleted is not None:
        images = Image.objects.filter(is_deleted=is_deleted)
    else:
        images = Image.objects.filter(is_deleted=False)
    return images


@router.post("/{image_id}/generate_thumbnail/", response=ImageSchema)
def generate_thumbnail(request, image_id: int):
    image = get_object_or_404(Image, id=image_id, is_deleted=False)
    thumbnail_path = image.create_thumbnail()  # Supposant que la méthode existe dans le modèle
    image.thumbnail = thumbnail_path
    image.save()
    return image


@router.post("/{image_id}/clone/", response=ImageSchema)
@transaction.atomic
def clone_image(request, image_id: int):
    image = get_object_or_404(Image, id=image_id, is_deleted=False)
    cloned_image = Image.objects.create(
        image=image.image,
        description=f"Copy of {image.description}",
        is_default=image.is_default
    )
    return cloned_image
