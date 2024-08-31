from django.shortcuts import get_object_or_404
from ninja import Router

from api.models.image import Image
from api.models.ingredients import Ingredient
from api.schemas.ingredients import IngredientSchema, IngredientCreateSchema, IngredientUpdateSchema

router = Router()

@router.get("/", response=list[IngredientSchema])
def list_ingredients(request):
    return Ingredient.objects.all()


@router.get("/{ingredient_id}", response=IngredientSchema)
def get_ingredient(request, ingredient_id: int):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    return ingredient


@router.post("/", response=IngredientSchema)
def create_ingredient(request, data: IngredientCreateSchema):
    ingredient = Ingredient.objects.create(
        name=data.name,
        description=data.description,
        type=data.type,
        allergens=data.allergens
    )
    if data.images:
        images = Image.objects.filter(id__in=data.images)
        ingredient.images.set(images)
    ingredient.save()
    return ingredient


@router.put("/{ingredient_id}", response=IngredientSchema)
def update_ingredient(request, ingredient_id: int, data: IngredientUpdateSchema):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    for attr, value in data.dict(exclude_unset=True).items():
        if value is not None:
            setattr(ingredient, attr, value)
    if data.images is not None:
        images = Image.objects.filter(id__in=data.images)
        ingredient.images.set(images)
    ingredient.save()
    return ingredient

