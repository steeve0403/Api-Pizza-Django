from django.shortcuts import get_object_or_404
from ninja import Router
from django.db import transaction

from api.models.image import Image
from api.models.ingredients import Ingredient
from api.schemas.ingredients import IngredientSchema, IngredientCreateSchema, IngredientUpdateSchema
from api.exception import BadRequestError

router = Router()

@router.get("/", response=list[IngredientSchema])
def list_ingredients(request):
    ingredients = Ingredient.objects.prefetch_related('images').all()
    return ingredients


@router.get("/{ingredient_id}", response=IngredientSchema)
def get_ingredient(request, ingredient_id: int):
    ingredient = get_object_or_404(Ingredient.objects.prefetch_related('images'), id=ingredient_id)
    return ingredient


@router.post("/", response=IngredientSchema)
@transaction.atomic
def create_ingredient(request, data: IngredientCreateSchema):
    ingredient = Ingredient.objects.create(
        name=data.name,
        description=data.description,
        type=data.type,
        allergens=data.allergens
    )
    if data.images:
        images = Image.objects.filter(id__in=data.images)
        if images.count() != len(data.images):
            raise BadRequestError("Some images were not found")
        ingredient.images.set(images)
    ingredient.save()
    return ingredient


@router.put("/{ingredient_id}", response=IngredientSchema)
@transaction.atomic
def update_ingredient(request, ingredient_id: int, data: IngredientUpdateSchema):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    data_dict = data.dict(exclude_unset=True)

    for attr, value in data_dict.items():
        if value is not None:
            setattr(ingredient, attr, value)

    if "images" in data_dict:
        images = Image.objects.filter(id__in=data.images)
        if images.count() != len(data.images):
            raise BadRequestError("Some images were not found")
        ingredient.images.set(images)

    ingredient.save()
    return ingredient


@router.patch("/{ingredient_id}", response=IngredientSchema)
@transaction.atomic
def patch_ingredient(request, ingredient_id: int, data: IngredientUpdateSchema):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    for attr, value in data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(ingredient, attr, value)
    if data.images is not None:
        images = Image.objects.filter(id__in=data.images)
        if images.count() != len(data.images):
            raise BadRequestError("Some images were not found")
        ingredient.images.set(images)
    ingredient.save()
    return ingredient


@router.delete("/{ingredient_id}")
def delete_ingredient(request, ingredient_id: int):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    ingredient.delete()
    return {"success": True}


@router.get("/filter/", response=list[IngredientSchema])
def filter_ingredients(request, type: str = None):
    if type:
        ingredients = Ingredient.objects.filter(type=type).prefetch_related('images')
    else:
        ingredients = Ingredient.objects.prefetch_related('images').all()
    return ingredients


@router.get("/search/", response=list[IngredientSchema])
def search_ingredients(request, name: str):
    ingredients = Ingredient.objects.filter(name__icontains=name).prefetch_related('images')
    return ingredients


@router.post("/{ingredient_id}/add_images/", response=IngredientSchema)
@transaction.atomic
def add_images_to_ingredient(request, ingredient_id: int, image_ids: list[int]):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    images = Image.objects.filter(id__in=image_ids)
    if images.count() != len(image_ids):
        raise BadRequestError("Some images were not found")
    ingredient.images.add(*images)
    ingredient.save()
    return ingredient


@router.post("/{ingredient_id}/remove_images/", response=IngredientSchema)
@transaction.atomic
def remove_images_from_ingredient(request, ingredient_id: int, image_ids: list[int]):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    images = Image.objects.filter(id__in=image_ids)
    if images.count() != len(image_ids):
        raise BadRequestError("Some images were not found")
    ingredient.images.remove(*images)
    ingredient.save()
    return ingredient


@router.post("/{ingredient_id}/deactivate/", response=IngredientSchema)
def deactivate_ingredient(request, ingredient_id: int):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    ingredient.available = False
    ingredient.save()
    return ingredient
