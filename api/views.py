from django.shortcuts import render
from ninja import Router
from .models import Image, Pizza, Ingredient
from .schemas import ImageSchema, PizzaSchema, IngredientSchema

# Create your views here.

router = Router()


# Display all pizzas
@router.get("/pizzas", response=list[PizzaSchema])
def get_pizzas(request):
    pizzas = Pizza.objects.select_related('default_image').prefetch_related('custom_images', 'ingredients').all()
    return pizzas

# Display only one pizza
@router.get("/pizzas/{pizza_id}", response=PizzaSchema)
def get_only_pizzas(request, pizza_id: int):
    try:
        pizza = Pizza.objects.get(id=pizza_id)
        return pizza
    except Pizza.DoesNotExist:
        return {"error": "Pizza not found"}, 404


# Create one pizza
@router.post("/pizzas", response=PizzaSchema)
def create_pizza(request, response: PizzaSchema):
    def create_pizza(request, data: PizzaSchema):
        ingredients = Ingredient.objects.filter(id__in=[ingredient.id for ingredient in data.ingredients])
        default_image = Image.objects.get(id=data.default_image.id)
        custom_images = Image.objects.filter(id__in=[image.id for image in data.custom_images])

        pizza = Pizza.objects.create(
            name=data.name,
            description=data.description,
            price=data.price,
            vegetarian=data.vegetarian,
            available=data.available,
            default_image=default_image
        )
        pizza.ingredients.set(ingredients)
        pizza.custom_images.set(custom_images)
        pizza.save()
        return pizza


@router.put("/pizzas/{pizza_id}", response=PizzaSchema)
def update_pizza(request, pizza_id: int, data: PizzaSchema):
    try:
        pizza = Pizza.objects.get(id=pizza_id)
        for attr, value in data.dict().items():
            setattr(pizza, attr, value)
        pizza.save()
        return pizza
    except Pizza.DoesNotExist:
        return {"message": "Pizza does not exist"}, 404


@router.delete("/pizzas/{pizza_id}", response={204: None})
def delete_pizza(request, pizza_id: int):
    try:
        pizza = Pizza.objects.get(id=pizza_id)
        pizza.delete()
        return 204, None
    except Pizza.DoesNotExist:
        return {"message": "Pizza does not exist"}, 404


@router.get("/ingredients", response=list[IngredientSchema])
def get_ingredients(request):
    return Ingredient.objects.all()

# @router.post("/ingredients", response=IngredientSchema)
# def create_ingredient(request, response: IngredientSchema):
