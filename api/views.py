from django.shortcuts import get_object_or_404
from ninja import Router

from .models import Image, Pizza, Ingredient, Category
from .schemas import PizzaSchema, PizzaCreateSchema, PizzaUpdateSchema, IngredientSchema, IngredientCreateSchema, \
    IngredientUpdateSchema, ImageSchema

# Create your views here.

router = Router()


# ---------- PIZZAS ---------- #
@router.get("/pizzas", response=list[PizzaSchema])
def list_pizzas(request):
    pizzas = Pizza.objects.all()
    return [PizzaSchema.from_orm(pizza) for pizza in pizzas]


@router.get("/pizzas/{pizza_id}", response=PizzaSchema)
def get_only_pizzas(request, pizza_id: int):
    try:
        pizza = Pizza.objects.get(id=pizza_id)
        return pizza
    except Pizza.DoesNotExist:
        return {"error": "Pizza not found"}, 404


@router.post("/pizzas", response=PizzaSchema)
@router.post("/pizzas", response=PizzaSchema)
def create_pizza(request, data: PizzaCreateSchema):
    ingredients = Ingredient.objects.filter(id__in=data.ingredients)
    categories = Category.objects.filter(id__in=data.categories)
    default_image = Image.objects.get(id=1)
    pizza = Pizza.objects.create(
        name=data.name,
        description=data.description,
        price=data.price,
        vegetarian=data.vegetarian,
        available=data.available,
        default_image=default_image
    )
    pizza.ingredients.set(ingredients)
    pizza.categories.set(categories)
    if data.custom_images:
        custom_images = Image.objects.filter(id__in=data.custom_images)
        pizza.custom_images.set(custom_images)
    pizza.save()
    return pizza


@router.put("/pizzas/{pizza_id}", response=PizzaSchema)
def update_pizza(request, pizza_id: int, data: PizzaUpdateSchema):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    for attr, value in data.dict().items():
        if value is not None:
            setattr(pizza, attr, value)
    if data.ingredients is not None:
        ingredients = Ingredient.objects.filter(id__in=data.ingredients)
        pizza.ingredients.set(ingredients)
    if data.categories is not None:
        categories = Category.objects.filter(id__in=data.category)
        pizza.category.set(categories)
    if data.custom_images is not None:
        custom_images = Image.objects.filter(id__in=data.custom_images)
        pizza.custom_images.set(custom_images)
    pizza.save()
    return pizza


@router.delete("/pizzas/{pizza_id}")
def delete_pizza(request, pizza_id: int):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    pizza.delete()
    return {"success": True}


# ---------- INGREDIENTS ---------- #

@router.get("/ingredients", response=list[IngredientSchema])
def list_ingredients(request):
    return Ingredient.objects.all()


@router.get("/ingredients/{ingredient_id}", response=IngredientSchema)
def get_ingredient(request, ingredient_id: int):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    return ingredient


@router.post("/ingredients", response=IngredientSchema)
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


@router.put("/ingredients/{ingredient_id}", response=IngredientSchema)
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


# ---------- IMAGES ---------- #

@router.get("/images", response=list[ImageSchema])
def list_images(request):
    return Image.objects.all()


@router.get("/images/{image_id}", response=ImageSchema)
def get_image(request, image_id: int):
    image = get_object_or_404(Image, id=image_id)
    return image


@router.put("/images/{image_id}", response=ImageSchema)
def update_image(request, image_id: int, data: ImageSchema):
    image = get_object_or_404(Image, id=image_id)
    for attr, value in data.dict().items():
        setattr(image, attr, value)
    image.save()
    return image


@router.delete("/images/{image_id}")
def delete_image(request, image_id: int):
    image = get_object_or_404(Image, id=image_id)
    image.delete()
    return {"success": True}
