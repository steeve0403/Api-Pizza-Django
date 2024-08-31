from django.shortcuts import get_object_or_404
from ninja import Router

from ..jwt_auth import JWTAuth
from ..models.category import Category
from ..models.image import Image
from ..models.ingredients import Ingredient
from ..models.pizza import Pizza
from ..schemas.pizza import PizzaSchema, PizzaCreateSchema, PizzaUpdateSchema

router = Router()
@router.get("/", response=list[PizzaSchema])
def list_pizzas(request):
    pizzas = Pizza.objects.all()
    return [PizzaSchema.from_orm(pizza) for pizza in pizzas]


@router.get("/{pizza_id}", response=PizzaSchema)
def get_only_pizzas(request, pizza_id: int):
    try:
        pizza = Pizza.objects.get(id=pizza_id)
        return pizza
    except Pizza.DoesNotExist:
        return {"error": "Pizza not found"}, 404


@router.post("/", response=PizzaSchema)
def create_pizza(request, data: PizzaCreateSchema):
    pizza = Pizza.objects.create(
        name=data.name,
        description=data.description,
        price=data.price,
        vegetarian=data.vegetarian,
        available=data.available
    )

    # Gestion des ingrédients
    for ingredient_data in data.ingredients:
        ingredient, created = Ingredient.objects.get_or_create(
            name=ingredient_data.name,
            defaults={'description': ingredient_data.description, 'type': ingredient_data.type}
        )
        pizza.ingredients.add(ingredient)

    if data.custom_images:
        pizza.custom_images.set(data.custom_images)

    pizza.save()
    return PizzaSchema.from_orm(pizza)


@router.put("/{pizza_id}", response=PizzaSchema)
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


@router.delete("/{pizza_id}", auth=JWTAuth)
def delete_pizza(request, pizza_id: int):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    pizza.delete()
    return {"success": True}
