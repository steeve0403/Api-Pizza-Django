from django.shortcuts import render
from ninja import Router
from .models import Pizza, Ingredient
from .schemas import PizzaSchema, IngredientSchema

# Create your views here.

router = Router()


@router.get("/pizzas", response=list[PizzaSchema])
def get_pizzas(request):
    return Pizza.objects.all()


# @router.get("/pizzas/{id}", response=list[PizzaSchema])
# def get_only_pizzas(request):
#     return Pizza.objects.get(pk=request.GET["id"])


@router.post("/pizzas", response=PizzaSchema)
def create_pizza(request, response: PizzaSchema):
    pizza_obj = Pizza.objects.create(**response.dict())
    return pizza_obj


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
