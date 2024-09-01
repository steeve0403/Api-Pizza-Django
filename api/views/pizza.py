from django.shortcuts import get_object_or_404
from ninja import Router
from django.db import transaction

from ..models.category import Category
from ..models.image import Image
from ..models.ingredients import Ingredient
from ..models.pizza import Pizza
from ..schemas.pizza import PizzaSchema, PizzaCreateSchema, PizzaUpdateSchema
from ..exception import NotFoundError, BadRequestError

router = Router()


@router.get("/", response=list[PizzaSchema])
def list_pizzas(request):
    pizzas = Pizza.objects.select_related('category').prefetch_related('ingredients', 'custom_images').all()
    return pizzas


@router.get("/{pizza_id}", response=PizzaSchema)
def get_only_pizzas(request, pizza_id: int):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    return pizza


@router.post("/", response=PizzaSchema)
@transaction.atomic
def create_pizza(request, data: PizzaCreateSchema):
    try:
        pizza = Pizza.objects.create(
            name=data.name,
            description=data.description,
            price=data.price,
            vegetarian=data.vegetarian,
            available=data.available
        )

        ingredients = []
        for ingredient_data in data.ingredients:
            ingredient, _ = Ingredient.objects.get_or_create(
                name=ingredient_data.name,
                defaults={'description': ingredient_data.description, 'type': ingredient_data.type}
            )
            ingredients.append(ingredient)
        pizza.ingredients.add(*ingredients)

        if data.custom_images:
            images = Image.objects.filter(id__in=data.custom_images)
            if len(images) != len(data.custom_images):
                raise BadRequestError("Some images were not found")
            pizza.custom_images.set(images)

        pizza.save()
        return PizzaSchema.from_orm(pizza)
    except Exception as e:
        raise BadRequestError(str(e))


@router.put("/{pizza_id}", response=PizzaSchema)
@transaction.atomic
def update_pizza(request, pizza_id: int, data: PizzaUpdateSchema):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    data_dict = data.dict(exclude_unset=True)

    try:
        for attr, value in data_dict.items():
            if value is not None:
                setattr(pizza, attr, value)

        if "ingredients" in data_dict:
            ingredients = Ingredient.objects.filter(id__in=data.ingredients)
            if ingredients.count() != len(data.ingredients):
                raise BadRequestError("Some ingredients were not found")
            pizza.ingredients.set(ingredients)

        if "categories" in data_dict:
            categories = Category.objects.filter(id__in=data.categories)
            if categories.count() != len(data.categories):
                raise BadRequestError("Some categories were not found")
            pizza.category.set(categories)

        if "custom_images" in data_dict:
            custom_images = Image.objects.filter(id__in=data.custom_images)
            if custom_images.count() != len(data.custom_images):
                raise BadRequestError("Some custom images were not found")
            pizza.custom_images.set(custom_images)

        pizza.save()
        return PizzaSchema.from_orm(pizza)
    except Exception as e:
        raise BadRequestError(str(e))


@router.delete("/{pizza_id}")
def delete_pizza(request, pizza_id: int):
    pizza = get_object_or_404(Pizza, id=pizza_id)
    pizza.delete()
    return {"success": True}
