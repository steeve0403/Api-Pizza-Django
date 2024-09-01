from django.shortcuts import get_object_or_404
from ninja import Router
from django.db import transaction
from django.db.models import Q

from api.models.category import Category
from api.models.image import Image
from api.models.ingredients import Ingredient
from api.models.pizza import Pizza, PizzaHistory
from api.schemas.pizza import PizzaSchema, PizzaCreateSchema, PizzaUpdateSchema
from api.exception import NotFoundError, BadRequestError

router = Router()


@router.get("/", response=list[PizzaSchema])
def list_pizzas(request):
    pizzas = Pizza.objects.filter(is_deleted=False).select_related('category').prefetch_related('ingredients',
                                                                                                'custom_images').all()
    return pizzas


@router.get("/{pizza_id}", response=PizzaSchema)
def get_only_pizzas(request, pizza_id: int):
    pizza = get_object_or_404(Pizza, id=pizza_id, is_deleted=False)
    return pizza


@router.post("/", response=PizzaSchema)
@transaction.atomic
def create_pizza(request, data: PizzaCreateSchema):
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
        if images.count() != len(data.custom_images):
            raise BadRequestError("Some images were not found")
        pizza.custom_images.set(images)

    pizza.save()
    return PizzaSchema.from_orm(pizza)


@router.put("/{pizza_id}", response=PizzaSchema)
@transaction.atomic
def update_pizza(request, pizza_id: int, data: PizzaUpdateSchema):
    pizza = get_object_or_404(Pizza, id=pizza_id, is_deleted=False)

    PizzaHistory.objects.create(
        pizza=pizza,
        name=pizza.name,
        description=pizza.description,
        price=pizza.price,
        vegetarian=pizza.vegetarian,
        available=pizza.available
    )

    data_dict = data.dict(exclude_unset=True)
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


@router.delete("/{pizza_id}")
def delete_pizza(request, pizza_id: int):
    pizza = get_object_or_404(Pizza, id=pizza_id, is_deleted=False)
    pizza.delete()
    return {"success": True}


@router.post("/{pizza_id}/restore/", response=PizzaSchema)
def restore_pizza(request, pizza_id: int):
    pizza = get_object_or_404(Pizza, id=pizza_id, is_deleted=True)
    pizza.is_deleted = False
    pizza.save()
    return pizza


@router.post("/{pizza_id}/add_ingredients/", response=PizzaSchema)
def add_ingredients_to_pizza(request, pizza_id: int, ingredient_ids: list[int]):
    pizza = get_object_or_404(Pizza, id=pizza_id, is_deleted=False)
    ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
    if ingredients.count() != len(ingredient_ids):
        raise BadRequestError("Some ingredients were not found")
    pizza.ingredients.add(*ingredients)
    pizza.save()
    return pizza


@router.post("/{pizza_id}/remove_ingredients/", response=PizzaSchema)
def remove_ingredients_from_pizza(request, pizza_id: int, ingredient_ids: list[int]):
    pizza = get_object_or_404(Pizza, id=pizza_id, is_deleted=False)
    ingredients = Ingredient.objects.filter(id__in=ingredient_ids)
    if ingredients.count() != len(ingredient_ids):
        raise BadRequestError("Some ingredients were not found")
    pizza.ingredients.remove(*ingredients)
    pizza.save()
    return pizza


@router.get("/search/", response=list[PizzaSchema])
def search_pizzas(request, query: str):
    pizzas = Pizza.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query),
        is_deleted=False
    ).select_related('category').prefetch_related('ingredients', 'custom_images')
    return pizzas


@router.get("/filter/", response=list[PizzaSchema])
def filter_pizzas(request, min_price: float = None, max_price: float = None, ingredient_type: str = None):
    pizzas = Pizza.objects.filter(is_deleted=False)

    if min_price is not None:
        pizzas = pizzas.filter(price__gte=min_price)
    if max_price is not None:
        pizzas = pizzas.filter(price__lte=max_price)
    if ingredient_type:
        pizzas = pizzas.filter(ingredients__type=ingredient_type)

    pizzas = pizzas.select_related('category').prefetch_related('ingredients', 'custom_images').distinct()
    return pizzas


@router.post("/{pizza_id}/clone/", response=PizzaSchema)
@transaction.atomic
def clone_pizza(request, pizza_id: int, new_name: str):
    pizza = get_object_or_404(Pizza, id=pizza_id, is_deleted=False)
    cloned_pizza = Pizza.objects.create(
        name=new_name,
        description=pizza.description,
        price=pizza.price,
        vegetarian=pizza.vegetarian,
        available=pizza.available
    )
    cloned_pizza.ingredients.set(pizza.ingredients.all())
    cloned_pizza.custom_images.set(pizza.custom_images.all())
    cloned_pizza.category.set(pizza.category.all())
    cloned_pizza.save()
    return cloned_pizza


@router.post("/{pizza_id}/apply_discount/", response=PizzaSchema)
def apply_discount_to_pizza(request, pizza_id: int, discount_percentage: float):
    if not 0 <= discount_percentage <= 100:
        raise BadRequestError("Discount percentage must be between 0 and 100")

    pizza = get_object_or_404(Pizza, id=pizza_id, is_deleted=False)
    discount_amount = pizza.price * (discount_percentage / 100)
    pizza.price -= discount_amount
    pizza.save()
    return pizza
